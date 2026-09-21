"""
Inventaire du catalogue de www.aciersgrosjean.be - etape 2 : analyse et livrables.

Lit les sorties de explorer.py, telecharge les PDF, detecte doublons et similaires,
ecrit les fichiers dans le projet (_DOCS/catalogue-site-actuel) et les PDF dans _DEPOT.
Options : --sans-pdf (ne telecharge pas les PDF).
"""
import csv
import difflib
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

# Donnees de travail (cache HTML, JSON intermediaires) hors OneDrive et hors Git.
ICI = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "crawl"
ICI.mkdir(parents=True, exist_ok=True)
PROJET = Path(__file__).resolve().parents[2]  # racine du depot, ou qu'il vive (ADR-0005)
SORTIE = PROJET / "_DOCS" / "catalogue-site-actuel"
DOSSIER_PDF = PROJET / "_DEPOT" / "documents" / "pdf-site-actuel"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 AciersGrosjean-refonte-inventaire")


def journal(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def normaliser(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("×", "x")
    s = re.sub(r"[^a-z0-9x,.]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def signature_dimensions(nom):
    """Cotes du nom : '2000x1000x2mm' -> '2000x1000x2' ; 'diametre 10mm' -> '10'."""
    n = normaliser(nom).replace(",", ".")
    blocs = re.findall(r"\d+(?:\.\d+)?(?:\s*x\s*\d+(?:\.\d+)?)+", n)
    if blocs:
        return "|".join(re.sub(r"\s+", "", b) for b in blocs)
    return "|".join(re.findall(r"\d+(?:\.\d+)?", n))


def slug_de(url):
    return unquote(urlsplit(url).path).strip("/").lower()


def lien_document(href, depuis):
    """URL absolue si le lien vise un document du site (.pdf ou /documentation/), sinon None."""
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    absolu = urljoin(depuis, quote(unquote(href.strip()), safe="/:-._~?=&%"))
    sp = urlsplit(absolu)
    if not sp.netloc.endswith("aciersgrosjean.be"):
        return None
    chemin = unquote(sp.path).lower()
    if chemin.endswith(".pdf") or chemin.startswith("/documentation/"):
        return absolu.split("#")[0]
    return None


def ecrire_csv(chemin, lignes, colonnes):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for l in lignes:
            w.writerow(l)


def main():
    avec_pdf = "--sans-pdf" not in sys.argv
    produits = json.loads((ICI / "produits_bruts.json").read_text(encoding="utf-8"))
    categories = json.loads((ICI / "categories_brutes.json").read_text(encoding="utf-8"))
    pages = json.loads((ICI / "pages.json").read_text(encoding="utf-8"))
    journal(f"{len(produits)} fiches produit, {len(categories)} pages categorie, {len(pages)} pages")

    par_id = {p["id"]: p for p in produits}
    cle_vers_id = {p["cle"]: p["id"] for p in produits}
    for p in produits:
        for autre in p.get("autres_urls", []):
            cle_vers_id[unquote(urlsplit(autre).path).rstrip("/").lower()] = p["id"]

    # ---------- documents (PDF) : liens de toutes les pages ----------
    pdf_sources = defaultdict(lambda: {"produits": set(), "pages": set(), "libelle": ""})
    pdfs_par_produit = defaultdict(dict)
    for cle, info in pages.items():
        if info.get("type") in (None, "non-html-ou-erreur"):
            continue
        f = ICI / "html" / (hashlib.sha1(cle.encode("utf-8")).hexdigest() + ".html")
        if not f.exists():
            continue
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
        depuis = info.get("url_finale") or info["url"]
        pid = cle_vers_id.get(cle) if info["type"] == "product-details-page" else None
        for el in soup.select("a[href], iframe[src], embed[src], object[data]"):
            doc = lien_document(el.get("href") or el.get("src") or el.get("data"), depuis)
            if not doc:
                continue
            libelle = el.get_text(" ", strip=True)
            if pid is not None:
                pdf_sources[doc]["produits"].add(pid)
                pdfs_par_produit[pid][doc] = libelle or unquote(doc).rsplit("/", 1)[-1]
            else:
                pdf_sources[doc]["pages"].add(unquote(info["url"]))
            pdf_sources[doc]["libelle"] = pdf_sources[doc]["libelle"] or libelle
        soup.decompose()
    for p in produits:
        p["pdfs"] = [{"url": u, "libelle": l} for u, l in pdfs_par_produit.get(p["id"], {}).items()]
    journal(f"{len(pdf_sources)} documents references")

    # ---------- categories : arbre et appartenance ----------
    noeuds = {}
    for cle, c in categories.items():
        base = cle.split("?")[0]
        n = noeuds.setdefault(base, {"cle": base, "url": None, "type": c["type"], "nom": "", "chemin": [],
                                     "sous_categories": [], "ids": [], "pages": 0})
        n["pages"] += 1
        if "?" not in cle:
            n["url"] = c["url"]
            n["nom"] = c["nom"]
            n["chemin"] = [m["nom"] for m in c["fil_ariane"] if m["nom"].lower() != "accueil"]
            n["sous_categories"] = [s["nom"] for s in c["sous_categories"]]
        for p in c["produits"]:
            if p["id"] and p["id"].isdigit() and int(p["id"]) not in n["ids"]:
                n["ids"].append(int(p["id"]))
    appartenances = defaultdict(list)
    for n in noeuds.values():
        if n["type"] != "category-page":
            continue
        for pid in n["ids"]:
            appartenances[pid].append(" > ".join(n["chemin"]) or n["nom"])
    ids_listes = {pid for n in noeuds.values() for pid in n["ids"]}
    ids_non_ouverts = sorted(ids_listes - set(par_id))

    # ---------- produits ----------
    lignes = []
    for p in produits:
        chemin = [m["nom"] for m in p["fil_ariane"] if m["nom"].lower() != "accueil"][:-1]
        variantes = [f'{v["attribut"]} : {" / ".join(v["options"])}' for v in p["variantes_attributs"]]
        variantes += [f'{v["nom"]} ({v["prix"]})' for v in p["variantes_groupees"]]
        m = re.search(r"€\s*(.*)$", p["prix_texte"] or "")
        unite = m.group(1).strip() if m else ""
        p["_chemin"] = chemin
        lignes.append({
            "id": p["id"],
            "nom": p["nom"],
            "univers": chemin[0] if len(chemin) > 0 else "",
            "categorie": chemin[1] if len(chemin) > 1 else "",
            "sous_categorie": chemin[2] if len(chemin) > 2 else "",
            "niveau_4": " > ".join(chemin[3:]),
            "autres_categories": " | ".join(sorted(set(appartenances.get(p["id"], [])) - {" > ".join(chemin)})),
            "reference_interne_sku": p["sku"],
            "reference_fabricant": p["reference_fabricant"],
            "prix_ttc": (f'{p["prix_ttc"]:.2f}'.replace(".", ",") if p["prix_ttc"] is not None else ""),
            "prix_affiche": p["prix_texte"],
            "unite": unite,
            "disponibilite": (p["disponibilite"] or "").replace("https://schema.org/", ""),
            "variantes": " || ".join(variantes),
            "specifications": " | ".join(f"{k} : {v}" for k, v in p["specifications"].items()),
            "nb_images": len(p["images"]),
            "images": " | ".join(p["images"]),
            "nb_pdf": len(p["pdfs"]),
            "pdf": " | ".join(unquote(x["url"]).rsplit("/", 1)[-1] for x in p["pdfs"]),
            "url": unquote(p["url"]),
            "decouvert_via": p["origine_decouverte"],
        })
    lignes.sort(key=lambda l: (l["univers"], l["categorie"], l["sous_categorie"], l["niveau_4"], l["nom"]))

    # ---------- doublons ----------
    # Les noms ne suffisent pas : IPE 180 / HEA 180, ou tole brute / galvanisee de meme format,
    # sont des produits differents. On ne retient que des signaux forts.
    groupes = []
    par_nom = defaultdict(list)
    for p in produits:
        par_nom[normaliser(p["nom"])].append(p)
    for lst in par_nom.values():
        if len(lst) > 1:
            groupes.append(("doublon : meme nom exact", lst))
    for p in produits:
        if p.get("autres_urls"):
            groupes.append(("meme produit accessible par plusieurs adresses", [p]))
    ranges = [p for p in produits if p["_chemin"]]
    for orphelin in (p for p in produits if not p["_chemin"]):
        dims = signature_dimensions(orphelin["nom"])
        meilleurs = sorted(
            ((difflib.SequenceMatcher(None, normaliser(orphelin["nom"]), normaliser(x["nom"])).ratio(), x)
             for x in ranges if dims and signature_dimensions(x["nom"]) == dims),
            key=lambda t: -t[0])
        if meilleurs and meilleurs[0][0] >= 0.5:
            groupes.append(("doublon probable : produit hors categorie, meme cotes qu'un produit du catalogue",
                            [orphelin, meilleurs[0][1]]))
        else:
            groupes.append(("produit hors categorie (invisible dans la navigation)", [orphelin]))
    lignes_doublons = []
    deja = set()
    num = 0
    for raison, lst in groupes:
        signature = (raison, tuple(sorted(x["id"] for x in lst)))
        if signature in deja:
            continue
        deja.add(signature)
        num += 1
        for x in lst:
            lignes_doublons.append({"groupe": num, "raison": raison, "id": x["id"], "nom": x["nom"],
                                    "categorie": " > ".join(x["_chemin"]) or "(aucune)",
                                    "prix_affiche": x["prix_texte"], "url": unquote(x["url"]),
                                    "autres_urls": " | ".join(unquote(u) for u in x.get("autres_urls", []))})

    # ---------- familles : meme produit decline en plusieurs cotes ----------
    def motif(nom):
        n = normaliser(nom)
        n = re.sub(r"\d+(?:[.,]\d+)?", "#", n)
        n = re.sub(r"#(?:\s*[x/]\s*#)+", "#", n)
        return re.sub(r"\s+", " ", n).strip()

    familles = defaultdict(list)
    for p in produits:
        familles[(" > ".join(p["_chemin"]) or "(aucune)", motif(p["nom"]))].append(p)
    lignes_familles = []
    for (cat, mot), lst in sorted(familles.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        prix = [x["prix_ttc"] for x in lst if x["prix_ttc"] is not None]
        lignes_familles.append({
            "categorie": cat, "motif_du_nom": mot, "nb_produits": len(lst),
            "prix_min_ttc": f"{min(prix):.2f}".replace(".", ",") if prix else "",
            "prix_max_ttc": f"{max(prix):.2f}".replace(".", ",") if prix else "",
            "exemple": lst[0]["nom"],
            "declinaisons": " | ".join(sorted({signature_dimensions(x["nom"]) or x["nom"] for x in lst})),
            "ids": " ".join(str(x["id"]) for x in lst)})

    # ---------- telechargement des PDF (reprenable) ----------
    index_f = ICI / "pdf_index.json"
    index = json.loads(index_f.read_text(encoding="utf-8")) if index_f.exists() else {}
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    par_hash = {v["sha1"]: v["fichier"] for v in index.values() if v.get("sha1") and v.get("fichier")}
    DOSSIER_PDF.mkdir(parents=True, exist_ok=True)
    lignes_pdf = []
    for i, (url, src) in enumerate(sorted(pdf_sources.items()), 1):
        nom_origine = unquote(urlsplit(url).path).rsplit("/", 1)[-1]
        if not nom_origine.lower().endswith(".pdf"):
            nom_origine += ".pdf"
        if avec_pdf and url not in index:
            res = {"statut": "", "sha1": "", "taille_ko": "", "fichier": "", "identique_a": ""}
            try:
                r = session.get(url, timeout=90)
                time.sleep(0.5)
                res["statut"] = r.status_code
                if r.status_code == 200 and r.content[:4] == b"%PDF":
                    h = hashlib.sha1(r.content).hexdigest()
                    res["sha1"] = h
                    res["taille_ko"] = round(len(r.content) / 1024)
                    if h in par_hash:
                        res["identique_a"] = par_hash[h]
                    else:
                        nom_local = re.sub(r'[<>:"/\\|?*]+', "_", nom_origine)
                        cible = DOSSIER_PDF / nom_local
                        if cible.exists() and hashlib.sha1(cible.read_bytes()).hexdigest() != h:
                            ident = urlsplit(url).path.rstrip("/").split("/")[-2]
                            cible = DOSSIER_PDF / f"{Path(nom_local).stem}__{ident}{Path(nom_local).suffix}"
                        cible.write_bytes(r.content)
                        par_hash[h] = cible.name
                        res["fichier"] = cible.name
                elif r.status_code == 200:
                    res["statut"] = "200 mais pas un PDF"
            except requests.RequestException as e:
                res["statut"] = f"erreur {e.__class__.__name__}"
            index[url] = res
            if i % 20 == 0:
                index_f.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
        res = index.get(url, {})
        lignes_pdf.append({
            "fichier_local": res.get("fichier") or (res["identique_a"] + " (contenu identique)" if res.get("identique_a") else ""),
            "nom_origine": nom_origine, "url": unquote(url), "statut": res.get("statut", ""),
            "taille_ko": res.get("taille_ko", ""), "sha1": res.get("sha1", ""), "nb_produits": len(src["produits"]),
            "ids_produits": " ".join(str(x) for x in sorted(src["produits"])),
            "produits": " | ".join(par_id[x]["nom"] for x in sorted(src["produits"]) if x in par_id),
            "pages_non_produit": " | ".join(sorted(src["pages"]))})
        if i % 50 == 0:
            journal(f"PDF {i}/{len(pdf_sources)}")
    index_f.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")

    # ---------- images ----------
    lignes_images = [{"id_produit": p["id"], "produit": p["nom"], "rang": rang, "url": img}
                     for p in produits for rang, img in enumerate(p["images"], 1)]

    # ---------- comparaison avec la refonte (lib/catalogue.ts) ----------
    refonte = []
    cat_ts = PROJET / "lib" / "catalogue.ts"
    if cat_ts.exists():
        refonte = re.findall(r'nom: "((?:[^"\\]|\\.)*)", categorie:', cat_ts.read_text(encoding="utf-8"))
    noms_site = {normaliser(p["nom"]) for p in produits}
    noms_refonte = {normaliser(n) for n in refonte}

    # ---------- ecriture ----------
    SORTIE.mkdir(parents=True, exist_ok=True)
    col_prod = ["id", "nom", "univers", "categorie", "sous_categorie", "niveau_4", "autres_categories",
                "reference_interne_sku", "reference_fabricant", "prix_ttc", "prix_affiche", "unite", "disponibilite",
                "variantes", "specifications", "nb_images", "nb_pdf", "pdf", "url", "images", "decouvert_via"]
    ecrire_csv(SORTIE / "produits.csv", lignes, col_prod)
    lignes_cat = []
    for n in sorted(noeuds.values(), key=lambda x: (x["type"], x["chemin"])):
        lignes_cat.append({"type": "categorie" if n["type"] == "category-page" else "marque",
                           "chemin": " > ".join(n["chemin"]) or n["nom"], "niveau": len(n["chemin"]),
                           "nom_page": n["nom"], "nb_produits_listes": len(n["ids"]), "pages_pagination": n["pages"],
                           "sous_categories": " | ".join(n["sous_categories"]), "url": unquote(n["url"] or n["cle"])})
    ecrire_csv(SORTIE / "categories.csv", lignes_cat,
               ["type", "chemin", "niveau", "nom_page", "nb_produits_listes", "pages_pagination", "sous_categories", "url"])
    ancien = SORTIE / "doublons-et-similaires.csv"
    if ancien.exists():
        ancien.unlink()
    ecrire_csv(SORTIE / "doublons.csv", lignes_doublons,
               ["groupe", "raison", "id", "nom", "categorie", "prix_affiche", "url", "autres_urls"])
    ecrire_csv(SORTIE / "familles.csv", lignes_familles,
               ["categorie", "motif_du_nom", "nb_produits", "prix_min_ttc", "prix_max_ttc", "exemple", "declinaisons", "ids"])
    ecrire_csv(SORTIE / "pdfs.csv", lignes_pdf,
               ["fichier_local", "nom_origine", "statut", "taille_ko", "nb_produits", "ids_produits", "produits",
                "pages_non_produit", "url", "sha1"])
    ecrire_csv(SORTIE / "images.csv", lignes_images, ["id_produit", "produit", "rang", "url"])
    propres = [{k: v for k, v in p.items() if not k.startswith("_")} for p in produits]
    (SORTIE / "produits.json").write_text(json.dumps(propres, ensure_ascii=False, indent=1), encoding="utf-8")

    stats = {
        "produits": len(produits),
        "ids_listes_non_ouverts": ids_non_ouverts,
        "sans_prix": sum(1 for p in produits if p["prix_ttc"] is None),
        "sans_image": sum(1 for p in produits if not p["images"]),
        "sans_pdf": sum(1 for p in produits if not p["pdfs"]),
        "avec_variantes": sum(1 for p in produits if p["variantes_attributs"] or p["variantes_groupees"]),
        "hors_categorie": sum(1 for p in produits if p["id"] not in appartenances),
        "images_total": sum(len(p["images"]) for p in produits),
        "images_uniques": len({i for p in produits for i in p["images"]}),
        "pdf_urls": len(lignes_pdf),
        "pdf_fichiers_uniques": len(par_hash),
        "pdf_poids_mo": round(sum(int(l["taille_ko"] or 0) for l in lignes_pdf if l["fichier_local"] and "identique" not in l["fichier_local"]) / 1024, 1),
        "pdf_erreurs": [l["url"] for l in lignes_pdf if avec_pdf and not l["sha1"]],
        "groupes_doublons": num,
        "familles": len(lignes_familles),
        "familles_multi": sum(1 for f in lignes_familles if f["nb_produits"] > 1),
        "produits_dans_familles_multi": sum(f["nb_produits"] for f in lignes_familles if f["nb_produits"] > 1),
        "noms_en_majuscules": [p["nom"] for p in produits if sum(c.isupper() for c in p["nom"]) > 0.6 * sum(c.isalpha() for c in p["nom"])],
        "slugs_suffixes": sum(1 for p in produits if re.search(r"-(\d+)$", slug_de(p["url"])) and re.search(r"-(\d+)$", slug_de(p["url"])).group(1) not in re.sub(r"\D+", " ", p["nom"]).split()),
        "leaf_categories": len({" > ".join(p["_chemin"]) for p in produits if p["_chemin"]}),
        "refonte_total": len(noms_refonte),
        "communs_refonte": len(noms_site & noms_refonte),
        "site_seulement": len(noms_site - noms_refonte),
        "refonte_seulement": len(noms_refonte - noms_site),
        "types_pages": dict(Counter(p["type"] for p in pages.values())),
        "par_univers": dict(Counter(l["univers"] for l in lignes)),
        "par_categorie": dict(Counter(f'{l["univers"]} > {l["categorie"]}' for l in lignes)),
        "par_sous_categorie": dict(Counter(" > ".join(x for x in (l["univers"], l["categorie"], l["sous_categorie"], l["niveau_4"]) if x) for l in lignes)),
        "unites": dict(Counter(l["unite"] for l in lignes)),
        "raisons_doublons": dict(Counter(l["raison"] for l in lignes_doublons)),
        "decouverte": dict(Counter(l["decouvert_via"] for l in lignes)),
    }
    (ICI / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    journal("FIN analyse : " + json.dumps({k: v for k, v in stats.items() if not isinstance(v, (dict, list))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
