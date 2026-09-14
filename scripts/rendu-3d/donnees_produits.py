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
import math
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


def tableau_vm2013(motif_fichier, motif_designation, colonnes, sauter_vides=False):
    """Lignes d'un tableau VM 2013 : {designation: {colonne: nombre}}.
    `colonnes` : noms des colonnes numeriques dans l'ordre, a partir de la 2e colonne du tableau.
    `sauter_vides` : ignore les cellules vides (colonnes fantomes de certains PDF, ex. fers T)."""
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
                    cellules = ([c for c in row[1:] if c not in ("", None)] if sauter_vides else row[1:])[:len(colonnes)]
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
        poids_et_controle(v, alertes, r, table=ligne and ligne["kg_m"])
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


def cornieres(cat, reel, desc):
    """Cornieres egales et inegales en acier lamine a chaud : tableaux fournisseur EN 10056 publies sur le site."""
    series = {
        "egale": (r"^CE EGALE LAC", ["kg_m", "a", "t", "r1", "r2"]),
        "inegale": (r"^CI-3", ["kg_m", "a", "b", "t", "r1", "r2"]),
    }
    tables = {k: tableau_vm2013(f, r"\d+x\d+x\d+(?:,\d+)?", cols) for k, (f, cols) in series.items()}
    # finition : ni option ni description sur le site ; seule la vraie photo des cornieres inegales (G020) la montre
    src_photo = "vraie photo du site actuel (cornière inégale, groupe G020) — non affichée : la fiche du site ne précise pas la finition"
    produits = {}
    for slug, c in cat.items():
        m = re.match(r"/acier/profiles/corniere-(egale|inegale)$", c["categorie"])
        d_nom = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
        if not m or not d_nom:
            continue
        sorte = m.group(1)
        nom_pdf, lignes = tables[sorte]
        cle = f"{d_nom.group(1)}x{d_nom.group(2)}x{d_nom.group(3)}"
        ligne = lignes.get(cle)
        v, alertes = {"serie": valeur("L", "", SRC_NOM)}, []
        a, b, t = int(d_nom.group(1)), int(d_nom.group(2)), nombre(d_nom.group(3))
        src_vm = f"fiche fournisseur publiée sur le site — {nom_pdf} (EN 10056)"
        if ligne:
            v["a"] = valeur(ligne["a"], "mm", src_vm)
            v["b"] = valeur(ligne.get("b", ligne["a"]), "mm", src_vm)
            v["t"] = valeur(ligne["t"], "mm", src_vm)
            v["r1"] = valeur(ligne["r1"], "mm", src_vm)
            v["r2"] = valeur(ligne["r2"], "mm", src_vm)
            if (ligne["a"], ligne.get("b", ligne["a"]), ligne["t"]) != (a, b, t):
                alertes.append(f"cotes du nom {cle} ≠ fournisseur")
        else:
            # hors tableau : cotes du nom et des cotes A/B/C du site ; rayons du format le plus proche (forme seulement)
            v["a"], v["b"], v["t"] = valeur(a, "mm", SRC_NOM), valeur(b, "mm", SRC_NOM), valeur(t, "mm", SRC_NOM)
            voisin = min(lignes, key=lambda k: (abs(lignes[k]["a"] - a) + abs(lignes[k].get("b", lignes[k]["a"]) - b),
                                                abs(lignes[k]["t"] - t)))
            src_voisin = f"format voisin {voisin} de {nom_pdf} (forme du modèle, non affiché)"
            v["r1"] = valeur(lignes[voisin]["r1"], "mm", src_voisin, supposee=True)
            v["r2"] = valeur(lignes[voisin]["r2"], "mm", src_voisin, supposee=True)
            alertes.append(f"{cle} absent du tableau fournisseur : rayons supposés ({voisin})")
        r = reel.get(slug, {})
        aire = t * (a + b - t) + (1 - math.pi / 4) * (v["r1"]["valeur"] ** 2 - 2 * v["r2"]["valeur"] ** 2)
        poids_et_controle(v, alertes, r, theorique=aire * 7.85e-3, table=ligne and ligne["kg_m"])
        if r.get("finition"):
            v["finition"] = valeur(r["finition"], "", SRC_OPTION)
        else:
            v["finition"] = valeur("BRUT", "", src_photo, supposee=True)
        d = desc.get(slug, {})
        texte = d.get("courte", "") + " " + " ".join(b_.get("texte", " ".join(b_.get("items", []))) for b_ in d.get("blocs", []))
        nuance, norme = nuance_et_norme(texte)
        if nuance:
            v["nuance"] = valeur(nuance, "", SRC_DESC)
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        # controle croise : cotes A/B/C du site = a/b/t
        lettres = {"A": "a", "B": "b", "C": "t"}
        for cote in d.get("cotes", []):
            k = lettres.get(cote["lettre"])
            if k and k in v:
                site = nombre(re.sub(r"[^\d,.]", "", cote["valeur"]))
                if abs(site - v[k]["valeur"]) > 0.05:
                    alertes.append(f"cote {cote['lettre']} du site ({cote['valeur']}) ≠ {k} ({v[k]['valeur']} mm)")
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": f"corniere-{sorte}",
                          "valeurs": v, "alertes": alertes}
    return produits


def texte_description(desc, slug):
    d = desc.get(slug, {})
    return d.get("courte", "") + " " + " ".join(b.get("texte", " ".join(b.get("items", []))) for b in d.get("blocs", []))


def poids_et_controle(v, alertes, r, theorique=None, table=None):
    """Poids de la fiche du site, comparé au tableau fournisseur, sinon au poids théorique.
    Écart ≤ 3 % : affiché (décision du 14/09 : l'image dit la même chose que la page).
    Écart > 3 % : les sources se contredisent, poids non affiché et question en attente (CLAUDE.md)."""
    if r.get("kg") is None:
        return
    v["poids"] = valeur(r["kg"], "kg/m", SRC_SITE)
    reference, nom = (table, "fournisseur") if table is not None else (theorique, "théorique")
    if reference and abs(reference - r["kg"]) / reference > 0.03:
        alertes.append(f"poids site {r['kg']} kg/m ≠ {nom} {reference:.2f} kg/m (écart > 3 %) : non affiché")
        v["poids"] = valeur(r["kg"], "kg/m", f"{SRC_SITE} — écart > 3 % avec le poids {nom} {reference:.2f} kg/m, "
                                              "non affiché (questions en attente)", supposee=True)


def controle_cotes_site(v, alertes, d, lettres):
    """Cotes A/B/C… affichées par le site actuel = valeurs retenues."""
    for cote in d.get("cotes", []):
        k = lettres.get(cote["lettre"])
        if k and k in v:
            site = nombre(re.sub(r"[^\d,.]", "", cote["valeur"]))
            if abs(site - v[k]["valeur"]) > 0.05:
                alertes.append(f"cote {cote['lettre']} du site ({cote['valeur']}) ≠ {k} ({v[k]['valeur']} mm)")


def fers_t(cat, reel, desc):
    """Fers T (EN 10055) : cotes et rayons du tableau fournisseur publié sur la fiche."""
    nom_pdf, lignes = tableau_vm2013(r"^FER-T", r"T\s?\d+", ["kg_m", "h", "b", "t", "r", "r1", "r2"], sauter_vides=True)
    src_vm = f"fiche fournisseur publiée sur le site — {nom_pdf} (EN 10055)"
    produits = {}
    for slug, c in cat.items():
        m = re.search(r"(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
        if c["categorie"] != "/acier/profiles/fer-t" or not m:
            continue
        h_nom, t_nom = int(m.group(1)), nombre(m.group(2))
        ligne = lignes.get(f"T{h_nom}") or lignes.get(f"T {h_nom}")
        v, alertes = {"serie": valeur("T", "", SRC_NOM)}, []
        if ligne:
            for k in ("h", "b", "t", "r", "r1", "r2"):
                v[k] = valeur(ligne[k], "mm", src_vm)
            if ligne["t"] != t_nom or ligne["h"] != h_nom:
                alertes.append(f"cotes du nom {h_nom}x{t_nom:g} ≠ fournisseur {ligne['h']:g}x{ligne['t']:g}")
        else:
            alertes.append(f"T{h_nom} absent du tableau fournisseur")
            continue
        poids_et_controle(v, alertes, reel.get(slug, {}), table=ligne["kg_m"])
        texte = texte_description(desc, slug)
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        v["finition"] = valeur("BRUT", "", "vraie photo du site actuel (fer T, groupe G023) — non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), {"A": "h", "B": "b", "C": "t"})
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": "fer-t", "valeurs": v, "alertes": alertes}
    return produits


def plats(cat, reel, desc):
    """Plats et larges plats : cotes du nom (confirmées par les cotes A/B du site), poids du site vs théorique."""
    produits = {}
    for slug, c in cat.items():
        m = re.match(r"/acier/profiles/(plat|large-plat)$", c["categorie"])
        d_nom = re.search(r"(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
        if not m or not d_nom:
            continue
        b, t = int(d_nom.group(1)), nombre(d_nom.group(2))
        v, alertes = {"serie": valeur("PLAT", "", SRC_NOM),
                      "b": valeur(b, "mm", SRC_NOM), "t": valeur(t, "mm", SRC_NOM)}, []
        poids_et_controle(v, alertes, reel.get(slug, {}), theorique=b * t * 7.85e-3)
        texte = texte_description(desc, slug)
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        v["finition"] = valeur("BRUT", "", "vraie photo du site actuel (plats, groupes G026 et G028) — non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), {"A": "b", "B": "t"})
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": m.group(1), "valeurs": v, "alertes": alertes}
    return produits


def pleins(cat, reel, desc):
    """Ronds lisses et carrés pleins : cote du nom, poids du site vs tableau fournisseur publié (EN 10060 / 10059)."""
    pdf_rond, t_rond = tableau_vm2013(r"^ROND LISSE", r"\d+(?:,\d+)?", ["kg_m"], sauter_vides=True)
    pdf_carre, t_carre = tableau_vm2013(r"^CARRE PLEIN", r"\d+(?:,\d+)?", ["kg_m"], sauter_vides=True)
    produits = {}
    for slug, c in cat.items():
        v, alertes = {}, []
        r = reel.get(slug, {})
        texte = texte_description(desc, slug)
        if c["categorie"] == "/acier/profiles/rond-plein":
            d_nom = re.search(r"(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
            d = nombre(d_nom.group(1))
            v["serie"] = valeur("ROND", "", SRC_NOM)
            v["d"] = valeur(d, "mm", SRC_NOM)
            ligne = t_rond.get(f"{d:g}".replace(".", ","))
            poids_et_controle(v, alertes, r, theorique=math.pi * d * d / 4 * 7.85e-3,
                              table=ligne and ligne["kg_m"])
            famille = "rond-plein"
            lettres = {"A": "d"}
            # « sa qualité spécifique, comme la qualité S235 ou S275 » : formulation trop vague pour être affichée
            nuance, _ = nuance_et_norme(texte)
            if nuance:
                v["nuance"] = valeur(nuance, "", SRC_DESC + " (« comme la qualité… » : formulation vague)", supposee=True)
        elif c["categorie"] == "/acier/profiles/carre-plein":
            d_nom = re.search(r"(\d+)\s*x\s*(\d+)\s*mm", c["nom"], re.I)
            a = int(d_nom.group(1))
            v["serie"] = valeur("CARRE", "", SRC_NOM)
            v["a"] = valeur(a, "mm", SRC_NOM)
            ligne = t_carre.get(str(a))
            poids_et_controle(v, alertes, r, theorique=a * a * 7.85e-3, table=ligne and ligne["kg_m"])
            famille = "carre-plein"
            lettres = {"A": "a"}
        else:
            continue
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        v["finition"] = valeur("BRUT", "", "aucune photo du site actuel : finition des barres laminées à chaud — non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), lettres)
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": famille, "valeurs": v, "alertes": alertes}
    return produits


def tubes(cat, reel, desc):
    """Tubes carrés, rectangulaires (EN 10219 : rayon extérieur r1 du tableau publié) et ronds."""
    src = "fiche fournisseur publiée sur le site — {} (EN 10219)"
    pdf_c, carres = tableau_vm2013(r"^TUBE CARRE", r"(\d+)x\1x\d+(?:,\d+)?", ["kg_m", "b", "t", "r1"], sauter_vides=True)
    _, rects = tableau_vm2013(r"^TUBE CARRE", r"(\d+)x(?!\1x)\d+x\d+(?:,\d+)?", ["kg_m", "h", "b", "t", "r1"], sauter_vides=True)
    pdf_r, ronds = tableau_vm2013(r"^TUBE ROND", r"[\d,]+\s*[xX]\s*[\d,]+", ["kg_m", "d", "t"], sauter_vides=True)
    ronds = {(l["d"], l["t"]): l for l in ronds.values()}
    produits = {}
    for slug, c in cat.items():
        m = re.match(r"/acier/tubes/tube-(carre|rectangulaire|rond)$", c["categorie"])
        if not m:
            continue
        sorte = m.group(1)
        v, alertes = {}, []
        r = reel.get(slug, {})
        texte = texte_description(desc, slug)
        if sorte == "rond":
            # « 17,2(18)x2mm » : diamètre 17,2 (désignation courante 18 entre parenthèses)
            d_nom = re.search(r"(\d+(?:,\d+)?)(?:\(\d+\))?\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
            d, t = nombre(d_nom.group(1)), nombre(d_nom.group(2))
            v["serie"] = valeur("TUBE-ROND", "", SRC_NOM)
            v["d"], v["t"] = valeur(d, "mm", SRC_NOM), valeur(t, "mm", SRC_NOM)
            ligne = ronds.get((d, t))
            poids_et_controle(v, alertes, r, theorique=math.pi * t * (d - t) * 7.85e-3,
                              table=ligne and ligne["kg_m"])
            famille, lettres = "tube-rond", {"A": "d", "B": "t"}
        else:
            d_nom = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
            h, b, t = int(d_nom.group(1)), int(d_nom.group(2)), nombre(d_nom.group(3))
            cle = f"{h}x{b}x{t:g}".replace(".", ",")
            ligne = (carres if h == b else rects).get(cle)
            v["serie"] = valeur("TC" if h == b else "TR", "", SRC_NOM)
            v["h"], v["b"], v["t"] = valeur(h, "mm", SRC_NOM), valeur(b, "mm", SRC_NOM), valeur(t, "mm", SRC_NOM)
            if ligne:
                v["r1"] = valeur(ligne["r1"], "mm", src.format(pdf_c) + " — rayon extérieur, non affiché")
            else:
                # rayon extérieur ≈ 2 t (EN 10219), forme seulement
                v["r1"] = valeur(2 * t, "mm", "≈ 2 × épaisseur (EN 10219, forme du modèle, non affichée)", supposee=True)
                alertes.append(f"{cle} absent du tableau fournisseur : rayon extérieur supposé (2 t)")
            aire = h * b - (h - 2 * t) * (b - 2 * t)  # sans les congés : légère surestimation
            poids_et_controle(v, alertes, r, theorique=aire * 7.85e-3 * 0.99, table=ligne and ligne["kg_m"])
            famille, lettres = f"tube-{'carre' if h == b else 'rectangulaire'}", {"A": "h", "B": "b", "C": "t"}
        if procede(texte) and sorte != "rond":
            v["procede"] = valeur("Formé à froid", "", SRC_DESC + " (« formage à froid à partir de tôles laminées à chaud »)")
        v["finition"] = valeur("BRUT", "", "vraies photos du site actuel (tubes, groupes G045 et G048) — non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), lettres)
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": famille, "valeurs": v, "alertes": alertes}
    return produits


FAMILLES = {"poutrelles": poutrelles, "cornieres": cornieres, "fers-t": fers_t, "plats": plats,
            "pleins": pleins, "tubes": tubes}


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
