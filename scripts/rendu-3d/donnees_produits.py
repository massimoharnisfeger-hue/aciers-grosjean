"""
Donnees sourcees des produits, pour les rendus 3D et l'habillage des visuels.

Chaque valeur porte sa source. Une valeur « supposee » ne s'affiche jamais sur un visuel.
Ordre de confiance pour la finition : site-actuel.json (option du site), description du site,
vraie photo, sinon la finition la plus courante de la famille, marquee supposee.

Entrees : lib/catalogue.ts, lib/site-actuel.json, lib/descriptions-site-actuel.json,
          _DEPOT/documents/pdf-site-actuel/ (tableaux fournisseurs VM 2013)
Sorties : scripts/rendu-3d/donnees/produits.json  (lu par les scripts de rendu)
          _DOCS/rendus-3d/donnees-produits.csv    (lecture humaine, une ligne par valeur)

Usage : python scripts/rendu-3d/donnees_produits.py [famille ...]   (defaut : toutes les familles traitees)
"""
import csv
import json
import re
import sys
from pathlib import Path

import pdfplumber

PROJET = Path(__file__).resolve().parents[2]
PDF = PROJET / "_DEPOT" / "documents" / "pdf-site-actuel"
SORTIE_JSON = Path(__file__).resolve().parent / "donnees" / "produits.json"
SORTIE_CSV = PROJET / "_DOCS" / "rendus-3d" / "donnees-produits.csv"

SRC_SITE = "site actuel — fiche produit"
SRC_OPTION = "site actuel — option de la fiche"
SRC_DESC = "site actuel — description de la fiche"
SRC_NOM = "nom du produit"


def nombre(txt):
    return float(str(txt).replace(",", ".").strip())


def valeur(v, unite, source, supposee=False):
    d = {"valeur": v, "source": source}
    if unite:
        d["unite"] = unite
    if supposee:
        d["supposee"] = True
    return d


# ---------------------------------------------------------------- lectures
def catalogue():
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'^\s*"([^"]+)": \{ slug: "[^"]+", nom: ("(?:[^"\\]|\\.)*"), categorie: "([^"]+)"', ts, re.M):
        out[m.group(1)] = {"nom": json.loads(m.group(2)), "categorie": m.group(3)}
    return out


def tableau_vm2013(motif_fichier, motif_designation, colonnes):
    """Lignes d'un tableau VM 2013 : {designation: {colonne: nombre}}.
    `colonnes` : noms des colonnes numeriques dans l'ordre, a partir de la 2e colonne du tableau."""
    fichier = next(p for p in PDF.iterdir() if re.search(motif_fichier, p.name, re.I))
    lignes = {}
    with pdfplumber.open(fichier) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or not row[0]:
                        continue
                    designation = re.sub(r"\s+", " ", row[0]).strip()
                    # le premier tableau est celui des dimensions ; les suivants (valeurs statiques)
                    # reprennent les memes designations avec d'autres colonnes
                    if not re.fullmatch(motif_designation, designation) or designation in lignes:
                        continue
                    cellules = [c for c in row[1:1 + len(colonnes)]]
                    try:
                        valeurs = {k: nombre(c) for k, c in zip(colonnes, cellules)}
                    except (TypeError, ValueError):
                        continue
                    nominal = int(re.search(r"\d+", designation).group())
                    if "h" in valeurs and not (0.85 * nominal <= valeurs["h"] <= 1.15 * nominal):
                        continue  # ligne d'un autre tableau : hauteur sans rapport avec la designation
                    lignes[designation] = valeurs
    return fichier.name, lignes


NUANCE = r"S\s?(?:235|275|355)(?:\s?(?:JR|J0|J2))?"


def nuance_et_norme(texte):
    """Nuances telles qu'ecrites sur le site (« S275/S355 », « S235 ou S275 » : decision du proprietaire
    du 14/09/2026) et premiere norme citee (« norme 10025 » -> « EN 10025 », norme europeenne des produits
    lamines a chaud en aciers de construction)."""
    nuance = re.search(rf"\b{NUANCE}(?:\s*(?:/|,|ou|et)\s*{NUANCE})*\b", texte)
    norme = re.search(r"\b(?:EN|NF EN|norme)\s*(10025(?:-\d)?|10034|10279|10219|10210|10056|10058|10059|1090)\b", texte, re.I)
    return (nuance.group(0) if nuance else None, f"EN {norme.group(1)}" if norme else None)


def procede(texte):
    return "Laminé à chaud" if re.search(r"lamin\w*\s+à\s+chaud", texte, re.I) else None


# ---------------------------------------------------------------- familles
def poutrelles(cat, reel, desc):
    series = {
        "IPE": (r"POUTRELLE IPE", r"IPE \d+", ["kg_m", "h", "b", "tw", "tf", "r"]),
        "HEA": (r"VM2013 - HEA", r"HE ?\d+ ?A|HEA ?\d+", ["kg_m", "h", "b", "tw", "tf", "r"]),
        "HEB": (r"VM2013 - HEB", r"HE ?\d+ ?B|HEB ?\d+", ["kg_m", "h", "b", "tw", "tf", "r"]),
        "UPN": (r"VM2013 - UPN", r"UPN ?\d+", ["kg_m", "h", "b", "tw", "tf", "r1", "r2"]),
    }
    tables = {}
    for serie, (fichier, motif, colonnes) in series.items():
        nom_pdf, lignes = tableau_vm2013(fichier, motif, colonnes)
        # « HE 200 A » -> 200
        tables[serie] = (nom_pdf, {int(re.search(r"\d+", k).group()): v for k, v in lignes.items()})
    produits = {}
    for slug, c in cat.items():
        m = re.search(r"\b(IPE|HEA|HEB|UPN)\s*(\d+)", c["nom"], re.I)
        if not c["categorie"].startswith("/acier/poutrelles/") or not m:
            continue
        serie, h_nom = m.group(1).upper(), int(m.group(2))
        nom_pdf, lignes = tables[serie]
        src_vm = f"fiche fournisseur VM 2013 — {nom_pdf}"
        ligne = lignes.get(h_nom)
        v, alertes = {}, []
        v["serie"] = valeur(serie, "", SRC_NOM)
        if ligne:
            for k in ("h", "b", "tw", "tf", "r", "r1", "r2"):
                if k in ligne:
                    v[k] = valeur(ligne[k], "mm", src_vm)
            # une HEA 200 mesure 190 mm de haut (norme) : l'ecart n'est anormal que pour IPE, HEB, UPN
            if serie != "HEA" and ligne["h"] != h_nom:
                alertes.append(f"h du nom ({h_nom}) different de h fournisseur ({ligne['h']})")
        else:
            alertes.append(f"{serie} {h_nom} absent du tableau fournisseur")
        r = reel.get(slug, {})
        if r.get("kg") is not None:
            v["poids"] = valeur(r["kg"], "kg/m", SRC_SITE)
            if ligne and abs(ligne["kg_m"] - r["kg"]) / ligne["kg_m"] > 0.03:
                alertes.append(f"poids site {r['kg']} kg/m ≠ fournisseur {ligne['kg_m']} kg/m (écart > 3 %)")
        if r.get("finition"):
            v["finition"] = valeur(r["finition"], "", SRC_OPTION)
        if r.get("longueurs"):
            v["longueurs"] = valeur(r["longueurs"], "m", SRC_OPTION)
        d = desc.get(slug, {})
        texte = d.get("courte", "") + " " + " ".join(b.get("texte", " ".join(b.get("items", []))) for b in d.get("blocs", []))
        nuance, norme = nuance_et_norme(texte)
        if nuance:
            v["nuance"] = valeur(nuance, "", SRC_DESC)
        if norme:
            v["norme"] = valeur(norme, "", SRC_DESC)
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        if serie == "UPN":
            # pente des faces interieures d'aile : non chiffree par la fiche, definie par la norme qu'elle cite
            v["pente_aile"] = valeur(8, "%", f"norme DIN 1026-1 citée par {nom_pdf} (forme du modèle, non affichée)")
        # contrôle croise : cotes A/B/C/D du site = h/b/tw/tf du fournisseur
        lettres = {"A": "h", "B": "b", "C": "tw", "D": "tf"}
        for cote in d.get("cotes", []):
            k = lettres.get(cote["lettre"])
            if k and k in v:
                site = nombre(re.sub(r"[^\d,.]", "", cote["valeur"]))
                if abs(site - v[k]["valeur"]) > 0.05:
                    alertes.append(f"cote {cote['lettre']} du site ({cote['valeur']}) ≠ {k} fournisseur ({v[k]['valeur']} mm)")
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": f"poutrelle-{serie.lower()}",
                          "valeurs": v, "alertes": alertes}
    return produits


FAMILLES = {"poutrelles": poutrelles}


def main():
    demandees = sys.argv[1:] or list(FAMILLES)
    cat = catalogue()
    reel = json.loads((PROJET / "lib" / "site-actuel.json").read_text(encoding="utf-8"))
    desc = json.loads((PROJET / "lib" / "descriptions-site-actuel.json").read_text(encoding="utf-8"))
    tous = json.loads(SORTIE_JSON.read_text(encoding="utf-8")) if SORTIE_JSON.exists() else {}
    for famille in demandees:
        nouveaux = FAMILLES[famille](cat, reel, desc)
        tous.update(nouveaux)
        print(f"{famille} : {len(nouveaux)} produits, {sum(1 for p in nouveaux.values() if p['alertes'])} avec alerte")
    SORTIE_JSON.parent.mkdir(parents=True, exist_ok=True)
    SORTIE_JSON.write_text(json.dumps(dict(sorted(tous.items())), ensure_ascii=False, indent=1), encoding="utf-8")
    SORTIE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(SORTIE_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["slug", "nom", "famille", "donnee", "valeur", "unite", "source", "supposee", "alertes"])
        for slug, p in sorted(tous.items()):
            for k, d in p["valeurs"].items():
                val = d["valeur"]
                val = " / ".join(f"{x:g}" for x in val) if isinstance(val, list) else (f"{val:g}" if isinstance(val, float) else val)
                w.writerow([slug, p["nom"], p["famille"], k, str(val).replace(".", ","), d.get("unite", ""),
                            d["source"], "oui" if d.get("supposee") else "", " | ".join(p["alertes"])])


if __name__ == "__main__":
    main()
