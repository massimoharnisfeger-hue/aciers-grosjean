"""
Integre au nouveau site les donnees reelles relevees sur www.aciersgrosjean.be.

Entrees : _DOCS/catalogue-site-actuel (produits.json, pdfs.csv), le cache HTML de l'exploration
          (%LOCALAPPDATA%/SiteAciersGrosjean/crawl/html) et lib/catalogue.ts (structure de la refonte).
Sorties : lib/site-actuel.json               prix, poids, longueurs, finition, unite, fiches PDF par slug
          lib/descriptions-site-actuel.json  descriptions structurees par slug (pages produit uniquement)
          lib/documents.json                 index des documents publies
          public/documents/*.pdf             fiches techniques renommees proprement

Relancer apres un nouveau releve : explorer.py -> analyser.py -> integrer.py.
"""
import csv
import filecmp
import hashlib
import json
import os
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, NavigableString, Tag

PROJET = Path(__file__).resolve().parents[2]
RELEVE = PROJET / "_DOCS" / "catalogue-site-actuel"
PDF_SOURCE = PROJET / "_DEPOT" / "documents" / "pdf-site-actuel"
CRAWL = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "crawl"
TVA = 1.21  # TVA belge 21 %
# Produits renommes dans la refonte (NOMS_CORRIGES de scripts/generer-catalogue.py) : nom encore utilise par le site actuel
NOMS_SITE_ACTUEL = {
    "poteau-de-cloture-clogriff-64-2m50-vert-ral-7016": "POTEAU DE CLÔTURE CLOGRIFF 64 – 2M50 - VERT RAL 7016",
}


def normaliser(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("×", "x")
    s = re.sub(r"[^a-z0-9x,.]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def slugifier(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def texte(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


# ---------------------------------------------------------------- refonte
def produits_refonte():
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    motif = re.compile(r'^\s*"([^"]+)": \{ slug: "[^"]+", nom: ((?:"(?:[^"\\]|\\.)*")), categorie: "([^"]+)", '
                       r'univers: "([^"]+)", kg: ([^,]+), unitePoids: "([^"]*)", unite: "([^"]*)", '
                       r'uniteCourte: "([^"]*)", prix: ([^,]+),', re.M)
    out = {}
    for m in motif.finditer(ts):
        ligne = ts[m.start():ts.find("\n", m.start())]
        out[m.group(1)] = {"slug": m.group(1), "nom": json.loads(m.group(2)), "categorie": m.group(3),
                           "unitePoids": m.group(6), "unite": m.group(7), "uniteCourte": m.group(8),
                           "kg": None if m.group(5) == "null" else float(m.group(5)),
                           "prix": None if m.group(9) == "null" else float(m.group(9)),
                           "specs": dict(re.findall(r'\{ label: "([^"]+)", valeur: "([^"]*)" \}', ligne))}
    return out


def unite_refonte_hors_metre(r):
    """Produit vendu a la piece, a la plaque ou au panneau (pas au metre) : un poids de plus d'une tonne est factice."""
    return r["unite"] != "au mètre"


def masse_surfacique_contredite(r, kg):
    """« Masse surfacique » calculée par la refonte (épaisseur × densité) : fausse pour une tôle perforée (trous) et
    contredite par le poids réel de la plaque ou du panneau au-delà de 3 % (tôles larmées et striées : relief)."""
    valeur = r["specs"].get("Masse surfacique")
    if not valeur:
        return False
    if r["categorie"].endswith("/tole-perforee"):
        return True
    dims = re.findall(r"[\d.,]+", r["specs"].get("Format") or r["specs"].get("Panneau") or "")
    if kg is None or len(dims) != 2:
        return False
    facteur = 1e-6 if "Format" in r["specs"] else 1.0  # « 2000 × 1000 mm » ou « 5 × 2 m »
    surface = float(dims[0].replace(",", ".")) * float(dims[1].replace(",", ".")) * facteur
    kg_m2 = float(re.search(r"[\d.,]+", valeur).group(0).replace(",", "."))
    return abs(kg_m2 * surface - kg) / kg > 0.03


# ---------------------------------------------------------------- descriptions
COTE = re.compile(r"\b([A-F])\s*:\s*([\d.,]+\s*(?:mm|cm|m)\b)", re.I)
SUPPLEMENT = re.compile(r"^\*?\s*attention,? un suppl[ée]ment de coupe.*?panier\.?\s*", re.I)


def blocs_description(html_bloc):
    """Paragraphes, intertitres et listes, en texte brut (aucun HTML repris du site)."""
    blocs = []

    def ajouter_paragraphe(t):
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            blocs.append({"t": "p", "texte": t})

    for el in html_bloc.children:
        if isinstance(el, NavigableString):
            ajouter_paragraphe(str(el))
            continue
        if not isinstance(el, Tag):
            continue
        if el.name in ("ul", "ol"):
            items = [texte(li) for li in el.find_all("li") if texte(li)]
            if items:
                blocs.append({"t": "ul", "items": items})
        elif el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if texte(el):
                blocs.append({"t": "h", "texte": texte(el)})
        elif el.name in ("p", "div", "span", "section"):
            if el.find(["ul", "ol", "p", "h2", "h3", "h4"]):
                blocs.extend(blocs_description(el))
                continue
            t = texte(el)
            enfants = [c for c in el.contents if not (isinstance(c, NavigableString) and not c.strip())]
            if t and len(enfants) == 1 and getattr(enfants[0], "name", None) in ("strong", "b") and len(t) < 90:
                blocs.append({"t": "h", "texte": t.rstrip(" :")})
            else:
                ajouter_paragraphe(t)
        elif el.name != "br":
            ajouter_paragraphe(texte(el))
    propres = []
    for b in blocs:  # paragraphes a puces "•" -> listes
        if b["t"] == "p" and b["texte"].count("•") >= 2:
            morceaux = [x.strip() for x in b["texte"].split("•")]
            if morceaux[0]:
                propres.append({"t": "p", "texte": morceaux[0]})
            propres.append({"t": "ul", "items": [x for x in morceaux[1:] if x]})
        else:
            propres.append(b)
    return structurer(propres)


# Le site source met chaque puce dans son propre <p> et ses intertitres en <p> nu
# (« Points forts », « Caractéristiques Techniques »...). Le 21/09, 4 776 blocs
# sur 4 776 sortaient en paragraphes. Controle : tests/test_produit.py (D1-D3).
MARQUEUR_PUCE = re.compile(r"^\s*(?:[•\-–·▪]|\d{1,2}[.)])\s+(.*)$")
LEXIQUE_TITRE = re.compile(
    r"caract[ée]ristique|sp[ée]cification|utilisation|application|usage|exemple|domaine"
    r"|point[s]? fort|avantage|atout|b[ée]n[ée]fice|conseil|service|description|pr[ée]sentation"
    r"|dimension|finition|norme|composition|mise en [oœ]uvre|entretien|livraison|garantie",
    re.I,
)


# « Finition Brossée Grain 320 », « Usage Intérieur et extérieur », « Caractéristique Détail » :
# un libellé au singulier suivi d'une valeur en majuscule est une ligne de tableau aplati, pas un titre.
LIBELLE_VALEUR = re.compile(
    r"^(finition|usage|longueurs?|poids|mati[èe]re|mat[ée]riau|[ée]paisseur|largeur|hauteur|diam[èe]tre"
    r"|section|caract[ée]ristique|dimension|norme|couleur|profil)\s+[A-ZÉÈ0-9]",
    re.I,
)


def ressemble_a_un_titre(texte, suivant):
    """Court, sans ponctuation de phrase, pas une donnee ni une ligne « libellé valeur », et suivi de contenu."""
    t = texte.strip().rstrip(" :")
    if not (3 <= len(t) <= 60) or t.endswith((".", "!", "?", ";")):
        return False
    mots = t.split()
    if LIBELLE_VALEUR.match(t) and len(mots) >= 3 and not re.match(r"^caract[ée]ristiques", t, re.I):
        return False
    if re.search(r"\d", t) and not LEXIQUE_TITRE.search(t):
        return False
    if LEXIQUE_TITRE.search(t):
        return len(mots) <= 8
    # un intertitre sans mot du lexique : seulement s'il precede une liste, et s'il en a la forme
    # (pas une phrase d'accroche : « Grâce à ses propriétés, la tôle striée est très polyvalente »)
    return bool(suivant) and bool(MARQUEUR_PUCE.match(suivant)) and len(mots) <= 6 and "," not in t


def structurer(blocs):
    """Puces par paragraphe -> items d'une meme liste ; <p> courts -> intertitres."""
    resultat = []
    i = 0
    while i < len(blocs):
        b = blocs[i]
        if b["t"] != "p":
            resultat.append(b)
            i += 1
            continue
        m = MARQUEUR_PUCE.match(b["texte"])
        if m:
            items = []
            while i < len(blocs) and blocs[i]["t"] == "p" and MARQUEUR_PUCE.match(blocs[i]["texte"]):
                items.append(MARQUEUR_PUCE.match(blocs[i]["texte"]).group(1).strip())
                i += 1
            if resultat and resultat[-1]["t"] == "ul":
                resultat[-1]["items"].extend(items)
            else:
                resultat.append({"t": "ul", "items": items})
            continue
        suivant = blocs[i + 1]["texte"] if i + 1 < len(blocs) and blocs[i + 1]["t"] == "p" else ""
        if ressemble_a_un_titre(b["texte"], suivant):
            titre = re.sub(r"^[^\w«\"']+", "", b["texte"].strip()).rstrip(" :")
            # « Caractéristique Détail » : en-tête d'un tableau a deux colonnes aplati par le site source.
            if re.fullmatch(r"caract[ée]ristique\s+d[ée]tail", titre, re.I):
                titre = "Caractéristiques"
            resultat.append({"t": "h", "texte": titre})
        else:
            resultat.append(b)
        i += 1
    return resultat


def description(cle):
    f = CRAWL / "html" / (hashlib.sha1(cle.encode("utf-8")).hexdigest() + ".html")
    if not f.exists():
        return None
    soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
    courte = texte(soup.select_one(".short-description")) if soup.select_one(".short-description") else ""
    supplement = bool(SUPPLEMENT.search(courte))
    courte = SUPPLEMENT.sub("", courte).strip()
    longue = soup.select_one(".full-description")
    blocs = blocs_description(longue) if longue else []
    # Les cotes (A: 40 mm, B: ...) ouvrent la description, en un ou plusieurs paragraphes :
    # sans le schema du site actuel elles ne veulent rien dire, on les range a part.
    cotes, gardes = [], []
    for b in blocs:
        if b["t"] == "p" and COTE.match(b["texte"].strip()):
            for l, v in COTE.findall(b["texte"]):
                if l.upper() not in {c["lettre"] for c in cotes}:
                    cotes.append({"lettre": l.upper(), "valeur": v.strip()})
            reste = COTE.sub("", b["texte"]).strip(" :;,-")
            if not reste:
                continue
            b = {"t": "p", "texte": reste}
        gardes.append(b)
    blocs = gardes
    blocs = [b for b in blocs if not (b["t"] == "h" and normaliser(b["texte"]) == "description")]
    # mention propre aux photos du site actuel, que le nouveau site ne reprend pas
    blocs = [b for b in blocs if not (b["t"] == "p" and re.match(r"^\*?\s*photos?\s+non[\s-]contractuelles?\.?$", b["texte"], re.I))]
    # la description courte reprend souvent la premiere phrase de la longue : ne pas la repeter
    if blocs and courte and normaliser(blocs[0].get("texte", ""))[:80] == normaliser(courte)[:80]:
        blocs.pop(0)
    soup.decompose()
    return {"courte": courte, "blocs": blocs, "cotes": cotes, "supplementCoupe": supplement}


# ---------------------------------------------------------------- documents
def titres_liens_documentation():
    """Texte des liens vers des PDF sur les pages du site (pour nommer les documents sans produit)."""
    titres = {}
    pages = json.loads((CRAWL / "pages.json").read_text(encoding="utf-8"))
    for cle, info in pages.items():
        if info.get("type") in (None, "non-html-ou-erreur", "product-details-page"):
            continue
        f = CRAWL / "html" / (hashlib.sha1(cle.encode("utf-8")).hexdigest() + ".html")
        if not f.exists():
            continue
        contenu = f.read_text(encoding="utf-8")
        if "documentation/" not in contenu and ".pdf" not in contenu.lower():
            continue
        soup = BeautifulSoup(contenu, "lxml")
        for a in soup.select("a[href]"):
            chemin = unquote(urlsplit(a["href"]).path).lower()
            if chemin.startswith("/documentation/") or chemin.endswith(".pdf"):
                t = texte(a)
                if t and len(t) > 3:
                    titres.setdefault(chemin.rsplit("/", 1)[-1], t)
        soup.decompose()
    return titres


def main():
    refonte = produits_refonte()
    releve = json.loads((RELEVE / "produits.json").read_text(encoding="utf-8"))
    par_nom = defaultdict(list)
    for p in releve:
        p["_feuille"] = [m["nom"] for m in p["fil_ariane"][1:-1]]
        par_nom[normaliser(p["nom"])].append(p)

    lignes_pdf = list(csv.DictReader(open(RELEVE / "pdfs.csv", encoding="utf-8-sig"), delimiter=";"))
    sha_par_url = {l["url"]: l["sha1"] for l in lignes_pdf if l["sha1"]}
    fichier_par_sha = {l["sha1"]: l["fichier_local"] for l in lignes_pdf
                       if l["sha1"] and l["fichier_local"] and "identique" not in l["fichier_local"]}

    # ---- appariement refonte <-> site actuel
    donnees, descriptions, non_apparies, poids_factices = {}, {}, [], []
    produits_par_sha = defaultdict(list)
    changements_unite = Counter()
    for slug, r in refonte.items():
        candidats = par_nom.get(normaliser(NOMS_SITE_ACTUEL.get(slug, r["nom"])), [])
        candidats = [c for c in candidats if c["_feuille"]] or candidats
        if not candidats:
            non_apparies.append(r["nom"])
            continue
        p = candidats[0]
        longueurs, finition = [], None
        for v in p["variantes_attributs"]:
            if v["attribut"].startswith("Longueur") and not longueurs:
                longueurs = [float(x.strip().lower().rstrip("m").replace(",", ".")) for x in v["options"]
                             if re.fullmatch(r"\d+(?:[.,]\d+)?\s*m", x.strip().lower())]
            elif v["attribut"].startswith("Finition") and v["options"]:
                finition = " / ".join(v["options"])
        kg = None
        m = re.search(r"([\d.,]+)\s*kg", p["specifications"].get("Poids", ""), re.I)
        if m:
            kg = float(m.group(1).replace(",", "."))
        # Le site actuel met 1,0 kg par defaut sur certaines fiches (toles perforees, clotures, marches...), 0 kg
        # sur les caillebotis et des milliers de kg sur les toles profilees (2 100 kg pour une tole de 2 m) :
        # poids inconnu, jamais affiche. Un vrai kilo (« ZINGA 1KG ») reste un kilo.
        # (un plat 25x5 vendu au metre pese vraiment 1,00 kg/m : la regle du kilo ne vaut qu'a la piece ou a la plaque)
        poids_factice = kg is not None and (kg <= 0 or (unite_refonte_hors_metre(r) and (kg >= 1000 or (
            kg == 1.0 and not re.search(r"\b1\s*KG\b", p["nom"], re.I)))))
        if poids_factice:
            kg = None
            poids_factices.append(r["nom"])
        if longueurs:
            unite, uniteCourte, unitePoids = "au mètre", "€/m", "kg/m"
        elif r["unite"] in ("à la plaque", "au panneau", "à l'unité"):
            unite, uniteCourte, unitePoids = r["unite"], r["uniteCourte"], r["unitePoids"]
        else:
            unite, uniteCourte, unitePoids = "à l'unité", "€/pce", ""
        if unite != r["unite"]:
            changements_unite[f'{r["unite"]} -> {unite}'] += 1
        shas = []
        for d in p["pdfs"]:
            sha = sha_par_url.get(unquote(d["url"]))
            if sha and sha not in shas:
                shas.append(sha)
                produits_par_sha[sha].append((slug, p))
        donnees[slug] = {
            "id": p["id"],
            "url": p["url"],
            "prixTtc": p["prix_ttc"],
            "prixHtva": round(p["prix_ttc"] / TVA, 2) if p["prix_ttc"] is not None else None,
            "kg": kg,
            # poids calcule de la refonte garde seulement si l'unite ne change pas et qu'aucun poids reel n'existe
            "remplacerPoids": kg is not None or poids_factice or unite != r["unite"],
            "unite": unite, "uniteCourte": uniteCourte, "unitePoids": unitePoids,
            "longueurs": longueurs,
            "finition": finition,
            "_shas": shas,
            "_prixRefonte": r["prix"],
        }
        d = description(p["cle"])
        if d:
            descriptions[slug] = d
        # Specifications ajoutees d'office par la refonte, gardees seulement si le site actuel les confirme.
        texte_reel = normaliser(p["nom"] + " " + p["description_courte"] + " " + p["description_longue"])
        retirer = []
        if r["categorie"].startswith("/aluminium") and "6060" not in texte_reel:
            retirer.append("Alliage")
        if r["categorie"].startswith("/inox") and "304" not in texte_reel:
            retirer.append("Nuance")
        if masse_surfacique_contredite(r, kg):
            retirer.append("Masse surfacique")
        donnees[slug]["specsRetirees"] = retirer

    # ---- publication des PDF sous des noms lisibles
    titres_doc = titres_liens_documentation()
    dossier_public = PROJET / "public" / "documents"
    dossier_public.mkdir(parents=True, exist_ok=True)
    # dossier entierement genere par ce script, mais synchronise par OneDrive qui verrouille des fichiers : on ne
    # recopie que les PDF changes et on ne supprime qu'a la fin ceux qui ne sont plus publies (le 14/09, vider le
    # dossier d'abord a laisse 51 PDF supprimes quand un verrou a arrete le script)
    anciens = {f.name for f in dossier_public.glob("*.pdf")}
    documents, noms_pris, doc_par_sha = [], set(), {}

    def reserver(base):
        nom, i = base, 2
        while nom in noms_pris:
            nom = f"{base}-{i}"
            i += 1
        noms_pris.add(nom)
        return nom

    uniques = []
    for l in sorted(lignes_pdf, key=lambda x: (-int(x["nb_produits"] or 0), x["nom_origine"])):
        if l["sha1"] and l["sha1"] in fichier_par_sha and l["sha1"] not in {u["sha1"] for u in uniques}:
            uniques.append(l)
    noms_origine = defaultdict(set)
    for l in lignes_pdf:
        if l["sha1"]:
            noms_origine[l["sha1"]].add(l["nom_origine"])

    def sujet_de(sha):
        lies = produits_par_sha.get(sha, [])
        slugs = {s for s, _ in lies}
        feuilles = Counter(p["_feuille"][-1] for _, p in lies if p["_feuille"])
        if len(slugs) == 1 or not feuilles:
            return lies[0][1]["nom"].strip()
        return feuilles.most_common(1)[0][0]

    def prefixe_commun(sha):
        """Debut de nom commun aux produits d'un document, sans les cotes : « Vis à bois », « ZINGA »..."""
        noms = [re.sub(r"\s*[\d,.x×/]+\s*(mm|m|ml|l|kg|cm)?\b", " ", p["nom"]).split() for _, p in produits_par_sha[sha]]
        commun = []
        for mots in zip(*noms):
            if len({m.lower() for m in mots}) != 1:
                break
            commun.append(mots[0])
        return " ".join(commun).strip(" -–")

    compte_sujets = Counter(sujet_de(l["sha1"]) for l in uniques if produits_par_sha.get(l["sha1"]))
    # Documents dont le titre automatique serait trompeur (d'apres leur nom de fichier sur le site actuel).
    TITRES_PAR_ORIGINE = [
        ("TOLES LAC", "Fiche technique — Tôles acier"),
        ("TUBE CARRE ACIERS GROSJEAN", "Fiche technique — Tubes carrés et rectangulaires acier"),
        ("CLOPLUS 40 - NOTICE", "Notice de pose — Clôture CLOPLUS 40"),
        ("CLOGRIFF 64 - NOTICE", "Notice de pose — Clôture CLOGRIFF 64"),
        ("FT-CP40", "Fiche technique — Poteaux de clôture CLOPLUS 40"),
        ("FT-CG64", "Fiche technique — Poteaux de clôture CLOGRIFF 64"),
        ("- BOIS - VIS", "Fiche technique — Vis à bois tête hexagonale"),
        ("- ACIER - VIS", "Fiche technique — Vis autoforantes pour acier"),
        ("FT-ZINGA-FR", "Fiche technique — ZINGA film galvanisant"),
        ("ZINGATARFREE", "Fiche technique — ZINGATARFREE"),
        ("VIBOL COATING", "Fiche technique — Primaire VIBOL Coating"),
        ("MARCHES D'ESCALIERS", "Fiche technique — Marches d'escalier ACHIL O2"),
        ("TASSEAU-40X40", "Fiche technique — Tasseau 40×40 maxi imitation bois"),
        ("EUROCOPRE-MONOLAMIERA", "Fiche technique — Panneau Eurocopre Monolamiera (ECO)"),
    ]

    def titre_impose(sha):
        for motif_nom, titre in TITRES_PAR_ORIGINE:
            if any(motif_nom in n.upper() for n in noms_origine[sha]):
                return titre
        return None
    TITRES_FIXES = {"rapport-esg": "Rapport ESG",
                    "ag-lattonedil-ttack-2023-manuel-technique-fr": "Manuel technique TTACK® (2023)"}

    for l in uniques:
        sha = l["sha1"]
        lies = produits_par_sha.get(sha, [])
        if lies:
            sujet = sujet_de(sha)
            if compte_sujets[sujet] > 1:
                precision = prefixe_commun(sha)
                if precision and precision.lower() != sujet.lower():
                    sujet = f"{sujet} — {precision}"
                else:
                    origine = sorted(noms_origine[sha])[0]
                    sujet = f"{sujet} — {re.sub(r'[-_]+', ' ', Path(origine).stem).strip()}"
            genre = "Notice de pose" if any("NOTICE" in n.upper() for n in noms_origine[sha]) else "Fiche technique"
            titre = titre_impose(sha) or f"{genre} — {sujet}"
            base = slugifier(titre.replace(" — ", " "))
            groupe = "fiches-produits"
        else:
            slug_url = unquote(urlsplit(l["url"]).path).rsplit("/", 1)[-1]
            brut = titres_doc.get(slug_url.lower(), "")
            brut = re.sub(r"^[^\wÀ-ÿ]+", "", brut).rstrip(" ›»>").strip()  # emojis de tete, fleches
            if not brut or re.match(r"(t[ée]l[ée]charger|d[ée]couvrez)", brut, re.I):
                brut = re.sub(r"[-_]+", " ", Path(slug_url).stem).strip().capitalize()
            titre = TITRES_FIXES.get(slug_url.lower(), brut)
            base = slugifier(Path(slug_url).stem)
            groupe = "entreprise" if "esg" in slug_url.lower() else "toiture-bardage"
        nom = reserver(base[:80]) + ".pdf"
        source, cible = PDF_SOURCE / fichier_par_sha[sha], dossier_public / nom
        if not (cible.exists() and filecmp.cmp(source, cible, shallow=False)):
            shutil.copyfile(source, cible)
        doc = {"fichier": f"/documents/{nom}", "titre": titre, "groupe": groupe,
               "tailleKo": int(l["taille_ko"] or 0), "produits": len({s for s, _ in lies})}
        doc_par_sha[sha] = doc
        documents.append(doc)
    for perime in sorted(anciens - {Path(d["fichier"]).name for d in documents}):
        try:
            (dossier_public / perime).unlink()
        except PermissionError:
            print("PDF perime verrouille (OneDrive ?), a supprimer plus tard :", perime)

    ecarts = []
    for d in donnees.values():
        d["pdfs"] = [{"fichier": doc_par_sha[s]["fichier"], "titre": doc_par_sha[s]["titre"]}
                     for s in d.pop("_shas") if s in doc_par_sha]
        ancien = d.pop("_prixRefonte")
        if ancien and d["prixHtva"]:
            ecarts.append(d["prixHtva"] / ancien)

    # ---- ecriture (une entree par ligne : diffs lisibles)
    def ecrire(chemin, dico):
        lignes = [f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in dico.items()]
        chemin.write_text("{\n" + ",\n".join(lignes) + "\n}\n", encoding="utf-8")

    ecrire(PROJET / "lib" / "site-actuel.json", dict(sorted(donnees.items())))
    ecrire(PROJET / "lib" / "descriptions-site-actuel.json", dict(sorted(descriptions.items())))
    (PROJET / "lib" / "documents.json").write_text(
        json.dumps(sorted(documents, key=lambda d: (d["groupe"], d["titre"])), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    # ---- rapport
    ecarts.sort()
    print(f"produits refonte : {len(refonte)} | apparies : {len(donnees)} | non apparies : {len(non_apparies)} {non_apparies[:5]}")
    print(f"descriptions : {len(descriptions)} | avec cotes : {sum(1 for d in descriptions.values() if d['cotes'])} "
          f"| supplement de coupe : {sum(1 for d in descriptions.values() if d['supplementCoupe'])} "
          f"| blocs moyens : {sum(len(d['blocs']) for d in descriptions.values()) / max(1, len(descriptions)):.1f}")
    print(f"avec longueurs : {sum(1 for d in donnees.values() if d['longueurs'])} | finition : {sum(1 for d in donnees.values() if d['finition'])} "
          f"| poids reel : {sum(1 for d in donnees.values() if d['kg'] is not None)} | avec PDF : {sum(1 for d in donnees.values() if d['pdfs'])}")
    print("changements d'unite :", dict(changements_unite))
    print(f"poids factices ecartes ({len(poids_factices)}) :", poids_factices)
    print("specifications non confirmees retirees :", dict(Counter(s for d in donnees.values() for s in d["specsRetirees"])))
    if ecarts:
        n = len(ecarts)
        print(f"prix reel HTVA / prix refonte : min {ecarts[0]:.2f}, mediane {ecarts[n // 2]:.2f}, max {ecarts[-1]:.2f}")
    print(f"documents publies : {len(documents)} ({sum(d['tailleKo'] for d in documents) / 1024:.1f} Mo) "
          f"| par groupe : {dict(Counter(d['groupe'] for d in documents))}")
    for doc in sorted(documents, key=lambda d: (d["groupe"], d["titre"])):
        print(f"   {doc['groupe'][:10]:10s} | {doc['produits']:3d} | {doc['titre'][:75]:75s} | {doc['fichier'][11:]}")


if __name__ == "__main__":
    main()
