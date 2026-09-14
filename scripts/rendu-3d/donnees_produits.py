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
    norme = re.search(r"\b(?:EN|NF EN|norme)\s*:?\s*(10025(?:-\d)?|10034|10279|10219|10210|10056|10058|10059|1090|10130|10346|10088(?:-\d)?)\b",
                      texte, re.I)
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
        elif serie in ("HEA", "HEB"):
            # la fiche fournisseur publiée cite les tolérances EN 10034 : poutrelles I et H laminées à chaud
            v["procede"] = valeur("Laminé à chaud", "", f"{src_vm} — tolérances EN 10034 (profilés I et H laminés à chaud)")
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


def nuance_inox(v, alertes, nom, texte):
    """Nuance inox du nom et de la description (même règle que specs_inox du générateur de catalogue) :
    « 304 » → 304 (1.4301), « 304L » → 304L (1.4307) (numéros EN 10088) ; les deux sur la page : non affichée."""
    en_304l = re.search(r"\b304\s?L\b", nom + " " + texte, re.I)
    en_304 = re.search(r"\b304\b(?!\s?L)", nom + " " + texte, re.I)
    if en_304 and en_304l:
        alertes.append("nom ou description : 304 et 304L sur la même page : nuance non affichée (question en attente)")
    elif en_304 or en_304l:
        v["nuance"] = valeur("304 (1.4301)" if en_304 else "304L (1.4307)", "",
                             "nom ou description ; numéro EN 10088 de la nuance")


# tôles planes : catégorie -> (famille, matière du rendu, masse volumique kg/dm³, source de la matière)
TOLES_PLANES = {
    "/acier/toles/tole-laminee-a-chaud": ("tole-laminee-a-chaud", "BRUT", 7.85),
    "/acier/toles/tole-quarto": ("tole-quarto", "BRUT", 7.85),
    "/acier/toles/tole-laminee-a-froid": ("tole-laminee-a-froid", "FROID", 7.85),
    "/acier/toles/tole-galvanisee": ("tole-galvanisee", "GALVA", 7.85),
    "/acier/toles/tole-corten": ("tole-corten", "CORTEN", 7.85),
    "/aluminium/toles/tole-plane": ("tole-aluminium", "ALU", 2.70),
    "/inox/toles/tole-plane-304-brossee": ("tole-inox-brossee", "INOX", 7.93),
}


def toles(cat, reel, desc):
    """Tôles planes vendues à la plaque : format et épaisseur du nom, recoupés avec les cotes A/B/C du site ;
    poids de la plaque comparé au poids théorique (masse volumique de la matière)."""
    familles = {c: f for c, (f, _, _) in TOLES_PLANES.items()}
    produits = {}
    for slug, c in cat.items():
        famille = familles.get(c["categorie"])
        d_nom = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
        if not famille or not d_nom:
            continue
        _, matiere, densite = TOLES_PLANES[c["categorie"]]
        L, l, e = int(d_nom.group(1)), int(d_nom.group(2)), nombre(d_nom.group(3))
        v, alertes = {"serie": valeur("TOLE", "", SRC_NOM), "L": valeur(L, "mm", SRC_NOM), "l": valeur(l, "mm", SRC_NOM),
                      "e": valeur(e, "mm", SRC_NOM)}, []
        r = reel.get(slug, {})
        if r.get("kg") is not None:
            theorique = L * l * e * densite * 1e-6
            v["poids"] = valeur(r["kg"], "kg/plaque", SRC_SITE)
            if abs(theorique - r["kg"]) / theorique > 0.03:
                alertes.append(f"poids site {r['kg']} kg ≠ théorique {theorique:.1f} kg (écart > 3 %) : non affiché")
                v["poids"]["supposee"] = True
        texte = texte_description(desc, slug)
        if matiere in ("BRUT", "FROID", "GALVA", "CORTEN"):  # nuances d'acier (les alliages alu/inox : plus bas)
            nuance, norme = nuance_et_norme(texte)
            if nuance and matiere == "FROID":
                # « Norme : EN 10130 • Matière : Acier S235JR ou équivalent » : EN 10130 couvre les aciers DC01…,
                # pas le S235JR ; la fiche fournisseur publiée dit EN 10130 → nuance non affichée (question en attente)
                v["nuance"] = valeur(nuance, "", SRC_DESC + " — contredite par la norme EN 10130 citée, non affichée", supposee=True)
            elif nuance:
                v["nuance"] = valeur(nuance, "", SRC_DESC)
            if norme and matiere == "FROID":
                v["norme"] = valeur(norme, "", SRC_DESC + " et fiche fournisseur publiée (ACIERS GROSJEAN - TOLES LAC)")
        if matiere == "INOX":
            nuance_inox(v, alertes, c["nom"], texte)
            if re.search(r"GR\s?320", c["nom"], re.I) and re.search(r"grain 320", texte, re.I) and re.search(r"sur 1 face", texte, re.I):
                v["surface"] = valeur("Brossée grain 320, 1 face", "", SRC_DESC + " (« Finition Brossée Grain 320 (K320) sur 1 face »)")
        if "laserpress" in slug:
            v["marque"] = valeur("LaserpressPlus® 240 skinpass", "", SRC_DESC)
        if procede(texte) or famille == "tole-laminee-a-chaud" and re.search(r"lamin\w+ à chaud", c["nom"], re.I):
            v["procede"] = valeur("Laminé à chaud", "", SRC_DESC if procede(texte) else SRC_NOM)
        elif re.search(r"lamin\w+ à froid", c["nom"], re.I):
            v["procede"] = valeur("Laminé à froid", "", SRC_NOM)
        # matière du rendu, jamais affichée (le nom de la tôle la donne déjà : galvanisée, Corten, aluminium, inox)
        v["finition"] = valeur(matiere, "", f"catégorie « {c['categorie']} » — matière du rendu, non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), {"A": "L", "B": "l", "C": "e"})
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": famille, "valeurs": v, "alertes": alertes}
    return produits


# tôles à relief : catégorie -> (famille, matière du rendu, masse volumique, motif du rendu, source du motif)
TOLES_RELIEF = {
    "/acier/toles/tole-larmee": ("tole-larmee", "BRUT", 7.85, "LARMES",
                                 "vraie photo du site actuel (groupe G038) ; larme EN 10363 type T ≈ 30 × 10 mm (catalogue ArcelorMittal A90)"),
    "/aluminium/toles/tole-striee": ("tole-aluminium-striee", "ALU", 2.70, "QUINTETTE",
                                     "vraie photo du site actuel (groupe G060) et description (« motif de 5 larmes (quintet) »)"),
}


def toles_relief(cat, reel, desc):
    """Tôles larmées (acier) et striées (aluminium) : « 3/5 mm » = épaisseur de la tôle de base / épaisseur au sommet
    du relief (description du site). Poids de la fiche affiché s'il est compris entre le poids de la tôle de base et
    +25 % (le relief ajoute environ 10 à 15 %) ; motif du relief : forme du rendu seulement, jamais affiché."""
    produits = {}
    for slug, c in cat.items():
        if c["categorie"] not in TOLES_RELIEF:
            continue
        famille, matiere, densite, motif, src_motif = TOLES_RELIEF[c["categorie"]]
        m = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)\s*/\s*(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
        if not m:
            continue
        L, l, e, e_total = int(m.group(1)), int(m.group(2)), nombre(m.group(3)), nombre(m.group(4))
        v, alertes = {"serie": valeur("TOLE-RELIEF", "", SRC_NOM), "L": valeur(L, "mm", SRC_NOM), "l": valeur(l, "mm", SRC_NOM),
                      "e": valeur(e, "mm", SRC_NOM + " (épaisseur de la tôle de base)"),
                      "e_total": valeur(e_total, "mm", SRC_NOM + " (épaisseur au sommet du relief)")}, []
        r = reel.get(slug, {})
        if r.get("kg") is not None:
            base = L * l * e * densite * 1e-6
            v["poids"] = valeur(r["kg"], "kg/plaque", SRC_SITE)
            if not base <= r["kg"] <= base * 1.25:
                alertes.append(f"poids site {r['kg']} kg hors de [{base:.1f} ; {base * 1.25:.1f}] kg (tôle de base à +25 %) : non affiché")
                v["poids"]["supposee"] = True
        texte = texte_description(desc, slug)
        if procede(texte):
            v["procede"] = valeur(procede(texte), "", SRC_DESC)
        v["motif"] = valeur(motif, "", src_motif + " — forme du rendu, non affichée", supposee=True)
        v["finition"] = valeur(matiere, "", f"catégorie « {c['categorie']} » — matière du rendu, non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), {"A": "L", "B": "l"})
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": famille, "valeurs": v, "alertes": alertes}
    return produits


def toles_perforees(cat, reel, desc):
    """Tôles perforées : format et épaisseur du nom ; perforation du code du nom (R = trous ronds de diamètre R,
    T = entraxe en quinconce ; C = trous carrés de côté C, U = pas en rangées droites), recoupée avec la description
    (« Trous ronds en quinconce (R10 T15) », « Diamètre des trous (R) : 10 mm »…). Motif aléatoire : aucune cote.
    Le site ne donne pas de poids (1 kg factice écarté) : rien d'affiché."""
    produits = {}
    for slug, c in cat.items():
        if c["categorie"] != "/acier/toles/tole-perforee":
            continue
        m = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)", c["nom"], re.I)
        if not m:
            continue
        L, l, e = int(m.group(1)), int(m.group(2)), nombre(m.group(3))
        texte = texte_description(desc, slug)
        v, alertes = {"serie": valeur("TOLE-PERFOREE", "", SRC_NOM), "L": valeur(L, "mm", SRC_NOM), "l": valeur(l, "mm", SRC_NOM),
                      "e": valeur(e, "mm", SRC_NOM)}, []
        code = re.search(r"\b([RC])\s*(\d+(?:,\d+)?)\s*([TU])\s*(\d+(?:,\d+)?)\b", c["nom"])
        if code:
            forme, cote, disposition, pas = code.group(1), nombre(code.group(2)), code.group(3), nombre(code.group(4))
            src = SRC_NOM + f" (code {code.group(0)})"
            if re.search(rf"\({re.escape(code.group(0))}\)", texte):
                src += " et description"
            v["perforation"] = valeur({"forme": "RONDE" if forme == "R" else "CARREE", "cote": cote, "pas": pas,
                                       "disposition": "QUINCONCE" if disposition == "T" else "LIGNE"}, "", src + " — géométrie du rendu",
                                      supposee=True)
            if forme == "R":
                v["trous"] = valeur(f"ronds Ø {texte_nombre(cote)} mm", "", src)
                v["entraxe"] = valeur(f"{texte_nombre(pas)} mm en quinconce", "", src)
            else:
                v["trous"] = valeur(f"carrés {texte_nombre(cote)} × {texte_nombre(cote)} mm", "", src)
                v["entraxe"] = valeur(f"{texte_nombre(pas)} mm en rangées droites", "", src)
            if disposition == "T" and re.search(r"rang[ée]es droites", texte, re.I) or disposition == "U" and re.search(r"quinconce", texte, re.I):
                alertes.append("disposition du code ≠ description : perforation non affichée")
                v["trous"]["supposee"] = v["entraxe"]["supposee"] = True
        elif re.search(r"al[ée]atoire", c["nom"], re.I):
            v["perforation"] = valeur({"forme": "ALEATOIRE"}, "", SRC_NOM + " — géométrie du rendu", supposee=True)
            v["trous"] = valeur("aléatoires, diamètres variables", "", SRC_DESC + " (« diamètres variables et disposition irrégulière »)")
        else:
            alertes.append("perforation introuvable dans le nom")
            continue
        nuance, _ = nuance_et_norme(texte)
        if nuance and "galva" not in slug:
            v["nuance"] = valeur(nuance, "", SRC_DESC)
        v["finition"] = valeur("GALVA" if "galva" in slug else "BRUT", "",
                               SRC_NOM + " / description (acier brut ou galvanisé) — matière du rendu, non affichée", supposee=True)
        produits[slug] = {"nom": c["nom"], "categorie": c["categorie"], "famille": "tole-perforee", "valeurs": v, "alertes": alertes}
    return produits


def texte_nombre(x):
    return f"{x:g}".replace(".", ",")


def armatures(cat, reel, desc):
    """Ronds à béton crénelés et treillis soudés : cotes du nom (et cotes A–E du site pour les dépassants),
    poids comparé au poids nominal des aciers pour béton (0,00617 × d² kg/m, EN 10080 publié sur le site).
    Nuance (B500A ou B500B) non tranchée par le site : jamais affichée."""
    src_texte = "site actuel — description (« surface crenelée »)"
    produits = {}
    for slug, c in cat.items():
        cat_ = c["categorie"]
        texte = texte_description(desc, slug)
        r = reel.get(slug, {})
        v, alertes = {}, []
        if cat_.startswith("/acier/armatures-beton/rond-a-beton"):
            d_nom = re.search(r"(\d+(?:,\d+)?)\s*mm", c["nom"], re.I)
            d = nombre(d_nom.group(1))
            v["serie"] = valeur("ROND-BETON", "", SRC_NOM)
            v["d"] = valeur(d, "mm", SRC_NOM)
            poids_et_controle(v, alertes, r, theorique=0.00617 * d * d)
            if re.search(r"cr[ée]nel", texte + c["nom"], re.I):
                v["surface"] = valeur("Crénelée", "", src_texte)
            procede = re.search(r"lamin\w*\s+à\s+(chaud|froid)", c["nom"], re.I)
            if procede:
                v["procede"] = valeur(f"Laminé à {procede.group(1).lower()}", "", SRC_NOM)
            famille = cat_.rsplit("/", 1)[-1]  # une famille par catégorie (laminé à chaud / à froid) : une photo studio chacune
        elif cat_.startswith("/acier/armatures-beton/treillis-soudes"):
            m = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+(?:,\d+)?)\s*mm\s+(\d+(?:,\d+)?)\s*m\s*x\s*(\d+(?:,\d+)?)\s*m", c["nom"], re.I)
            if not m:
                continue
            a, b, d = int(m.group(1)), int(m.group(2)), nombre(m.group(3))
            L, l = round(nombre(m.group(4)) * 1000), round(nombre(m.group(5)) * 1000)
            v["serie"] = valeur("TREILLIS", "", SRC_NOM)
            v["maille_a"], v["maille_b"] = valeur(a, "mm", SRC_NOM), valeur(b, "mm", SRC_NOM)
            v["maille"] = valeur(f"{a} × {b} mm", "", SRC_NOM)
            v["d"] = valeur(d, "mm", SRC_NOM)
            v["L"], v["l"] = valeur(L, "mm", SRC_NOM), valeur(l, "mm", SRC_NOM)
            v["format"] = valeur(f"{L / 1000:g} × {l / 1000:g} m".replace(".", ","), "", SRC_NOM)
            # pas de référence fiable pour le poids d'un panneau (nombre de fils et débords propres au fabricant,
            # fiches fournisseurs publiées en image) : poids de la fiche affiché sans comparaison
            poids_et_controle(v, alertes, r)
            if v.get("poids"):
                v["poids"]["unite"] = "kg/panneau"
            if "depassant" in slug:
                v["depassants"] = valeur(True, "", SRC_NOM)
            if "galvanis" in slug:  # matière du rendu ; déjà écrit dans le titre, la page n'a pas de ligne finition
                v["finition"] = valeur("GALVA", "", SRC_NOM + " — non affichée (déjà dans le titre)", supposee=True)
            if re.search(r"cr[ée]nel", texte, re.I):
                v["surface"] = valeur("Crénelée", "", src_texte)
            famille = "treillis-soude-depassants" if "depassant" in slug else "treillis-soude"
            controle_cotes_site(v, alertes, desc.get(slug, {}), {"A": "L", "B": "l", "C": "maille_a", "D": "maille_b", "E": "d"})
            for k in ("L", "l", "maille_a", "maille_b", "d"):  # nom et cotes du site en désaccord : valeur non affichée
                if any(re.search(rf"≠ {k} \(", a_) for a_ in alertes):
                    v[k]["supposee"] = True
        else:
            continue
        v.setdefault("finition", valeur("BRUT", "", "vraies photos du site actuel (treillis, groupes G002 à G005) — non affichée", supposee=True))
        produits[slug] = {"nom": c["nom"], "categorie": cat_, "famille": famille, "valeurs": v, "alertes": alertes}
    return produits


def profils_alu_inox(cat, reel, desc):
    """Profilés et tubes en aluminium et en inox : cotes du nom (recoupées avec les cotes du site), poids de la fiche
    comparé au poids théorique (alu 2,70 ; inox 7,93 kg/dm³). Pas de tableau fournisseur publié : rayons des angles
    pris à des valeurs usuelles de filage ou de pliage, marqués « supposés » (forme seulement, jamais affichés)."""
    produits = {}
    for slug, c in cat.items():
        m = re.match(r"/(aluminium|inox)/(profiles|tubes)/([a-z-]+)$", c["categorie"])
        if not m:
            continue
        univers, sorte = m.group(1), m.group(3)
        rho, matiere = (2.70, "ALU") if univers == "aluminium" else (7.93, "INOX")
        nom = c["nom"]
        nombres_nom = [nombre(x) for x in re.findall(r"\d+(?:,\d+)?", re.sub(r"(?i)inox\s*304|304", "", nom))]
        v, alertes = {}, []
        src_forme = "valeur usuelle — forme du modèle, non affichée"
        r = reel.get(slug, {})
        lettres = {}
        if sorte == "corniere-egale":
            a, t = nombres_nom[0], nombres_nom[2]
            v.update(serie=valeur("L", "", SRC_NOM), a=valeur(a, "mm", SRC_NOM), b=valeur(a, "mm", SRC_NOM), t=valeur(t, "mm", SRC_NOM),
                     r1=valeur(t * (0.5 if matiere == "ALU" else 1.0), "mm", src_forme, supposee=True),
                     r2=valeur(0.0 if matiere == "ALU" else t * 0.5, "mm", src_forme, supposee=True))
            theorique = t * (2 * a - t) * rho * 1e-3
            lettres = {"A": "a", "B": "b", "C": "t"}
        elif sorte == "plat":
            b, t = nombres_nom[0], nombres_nom[1]
            v.update(serie=valeur("PLAT", "", SRC_NOM), b=valeur(b, "mm", SRC_NOM), t=valeur(t, "mm", SRC_NOM))
            theorique = b * t * rho * 1e-3
            lettres = {"A": "b", "B": "t"}
        elif sorte == "profil-t":
            h, b, t = nombres_nom[0], nombres_nom[1], nombres_nom[2]
            v.update(serie=valeur("T", "", SRC_NOM), h=valeur(h, "mm", SRC_NOM), b=valeur(b, "mm", SRC_NOM), t=valeur(t, "mm", SRC_NOM),
                     r=valeur(t * 0.5, "mm", src_forme, supposee=True), r1=valeur(0.0, "mm", src_forme, supposee=True),
                     r2=valeur(0.0, "mm", src_forme, supposee=True))
            theorique = t * (b + h - t) * rho * 1e-3
            lettres = {"A": "h", "B": "b", "C": "t"}
        elif sorte == "profil-u":
            h, b, t = nombres_nom[0], nombres_nom[1], nombres_nom[3]  # « 20x20x20x2 » : fond, ailes, épaisseur
            v.update(serie=valeur("U-ALU", "", SRC_NOM), h=valeur(h, "mm", SRC_NOM), b=valeur(b, "mm", SRC_NOM),
                     tw=valeur(t, "mm", SRC_NOM), tf=valeur(t, "mm", SRC_NOM),
                     r1=valeur(t * 0.5, "mm", src_forme, supposee=True), r2=valeur(0.0, "mm", src_forme, supposee=True))
            theorique = t * (h + 2 * b - 2 * t) * rho * 1e-3
        elif sorte == "rond-plein":
            d = nombres_nom[0]
            v.update(serie=valeur("ROND", "", SRC_NOM), d=valeur(d, "mm", SRC_NOM))
            theorique = math.pi * d * d / 4 * rho * 1e-3
            lettres = {"A": "d"}
        elif sorte in ("tube-carre", "tube-rectangulaire"):
            h, b, t = nombres_nom[0], nombres_nom[1], nombres_nom[2]
            v.update(serie=valeur("TC" if h == b else "TR", "", SRC_NOM), h=valeur(h, "mm", SRC_NOM), b=valeur(b, "mm", SRC_NOM),
                     t=valeur(t, "mm", SRC_NOM), r1=valeur(t * (0.75 if matiere == "ALU" else 1.5), "mm", src_forme, supposee=True))
            theorique = (h * b - (h - 2 * t) * (b - 2 * t)) * rho * 1e-3
            lettres = {"A": "h", "B": "b", "C": "t"}
        elif sorte == "tube-rond":
            d, t = nombres_nom[0], nombres_nom[1]
            v.update(serie=valeur("TUBE-ROND", "", SRC_NOM), d=valeur(d, "mm", SRC_NOM), t=valeur(t, "mm", SRC_NOM))
            theorique = math.pi * t * (d - t) * rho * 1e-3
            lettres = {"A": "d", "B": "t"}
        else:
            continue
        poids_et_controle(v, alertes, r, theorique=theorique)
        if matiere == "INOX":
            nuance_inox(v, alertes, nom, texte_description(desc, slug))
        v["finition"] = valeur(matiere, "", f"univers {univers} — matière du rendu, non affichée", supposee=True)
        controle_cotes_site(v, alertes, desc.get(slug, {}), lettres)
        produits[slug] = {"nom": nom, "categorie": c["categorie"], "famille": f"{univers}-{sorte}", "valeurs": v, "alertes": alertes}
    return produits


FAMILLES = {"poutrelles": poutrelles, "cornieres": cornieres, "fers-t": fers_t, "plats": plats,
            "pleins": pleins, "tubes": tubes, "toles": toles, "armatures": armatures, "alu-inox": profils_alu_inox,
            "toles-relief": toles_relief, "toles-perforees": toles_perforees}


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
