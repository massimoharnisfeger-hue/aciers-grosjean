"""
Habillage 2D des rendus Blender.

  python scripts/rendu-3d/habiller.py <slug>            visuel caracteristiques : cotes + fiche technique
  python scripts/rendu-3d/habiller.py --studio <nom>    photo studio : fond blanc pur, ombre douce
  --essai (avant les arguments) : lit et ecrit dans rendu3d/essais/ au lieu de rendu3d/final/

Lit    %LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/final/<slug>.png et <slug>.json (rendu_profil.py)
       scripts/rendu-3d/donnees/produits.json : seules les valeurs sourcees (non « supposees ») s'affichent
Ecrit  final/<slug>-caracteristiques.png/.webp ou final/<nom>-studio.png/.webp
Polices (Google Fonts, OFL) dans rendu3d/polices : Poppins-SemiBold, Questrial-Regular,
IBMPlexMono-Medium, IBMPlexMono-SemiBold.
"""

import json
import math
import os
import re
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, "donnees", "produits.json")
# rendus et polices hors OneDrive (fichiers lourds, non versionnés)
TRAVAIL = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "SiteAciersGrosjean", "rendu3d")
POLICES = os.path.join(TRAVAIL, "polices")

# charte (tailwind.config.ts)
ENCRE = (51, 54, 66)
JAUNE = (255, 213, 0)
ACIER = (170, 176, 179)
BRUME = (209, 214, 218)
GRIS_TEXTE = (110, 115, 124)
BLANC = (255, 255, 255)

S = 2  # suréchantillonnage du tracé

# libellés affichés d'une finition (définitions données par les descriptions du site actuel)
FINITIONS = {"GPP": "GPP — grenaillé, primaire", "BRUT": "Brut — calamine"}


def police(nom, taille):
    return ImageFont.truetype(os.path.join(POLICES, nom), taille * S)


def fiche(slug):
    with open(DONNEES, encoding="utf-8") as f:
        produits = json.load(f)
    if slug not in produits:
        raise SystemExit(f"Produit absent de {DONNEES} : {slug}")
    return produits[slug]


def titre_image(nom):
    """Nom du produit sans la matière ni le procédé, déjà donnés par le surtitre et la fiche
    (« Cornière égale 50x50x5mm Acier LAC » -> « Cornière égale 50x50x5mm »)."""
    nom = re.sub(r"\s+en\s+acier\s+brut(?=\s+série)", "", nom.strip(), flags=re.I)  # « … en acier brut série légère »
    # « Large plat en acier laminé à chaud 160x10mm » : matière au milieu du nom
    nom = re.sub(r"\s+en\s+acier\s+lamin[ée]+e?\s+à\s+(?:chaud|froid)(?=\s+\d)", "", nom, flags=re.I)
    return re.sub(r"\s+(?:en\s+)?acier(?:\s+LAC|\s+lamin[ée]+e?\s+à\s+(?:chaud|froid))?$", "", nom, flags=re.I)


NOMS_CATEGORIES = {}


def surtitre_image(categorie):
    """« ACIER  ·  PROFILÉS » : noms de l'univers et de la famille tels qu'affichés par le site (lib/catalogue.ts)."""
    if not NOMS_CATEGORIES:
        with open(os.path.join(ICI, "..", "..", "lib", "catalogue.ts"), encoding="utf-8") as f:
            for m in re.finditer(r'^\s*"(/[^"]+)": \{ chemin: "[^"]+", segment: "[^"]*", nom: "([^"]+)"', f.read(), re.M):
                NOMS_CATEGORIES[m.group(1)] = m.group(2)
    segments = [s for s in categorie.split("/") if s]
    noms = [NOMS_CATEGORIES.get("/" + "/".join(segments[:i + 1]), segments[i].replace("-", " ")) for i in range(2)]
    return "  ·  ".join(n.upper() for n in noms)


def affichable(p, cle):
    """Valeur formatée pour l'image, ou None si absente ou supposée."""
    d = p["valeurs"].get(cle)
    if not d or d.get("supposee"):
        return None
    v, unite = d["valeur"], d.get("unite", "")
    if isinstance(v, (int, float)):
        texte = f"{v:.2f}" if unite.startswith("kg") else f"{v:g}"  # poids : deux décimales, comme la page
        return f"{texte.replace('.', ',')} {unite}".strip()
    return str(v)


# ---------------------------------------------------------------- tracé

def pt(p):
    return (p[0] * S, p[1] * S)


TRACES = []  # tracés en deux passes, halo blanc puis trait
PASTILLES = []
TRAITS_COTES = []  # extrémités du trait de chaque étiquette de cote (même rang que PASTILLES), None pour les pinces


def fleche(pointe, depuis, couleur, long_=13, larg=5.5):
    TRACES.append(("fleche", pointe, depuis, couleur, long_, larg))


def ligne(a, b, couleur, ep=2.2):
    TRACES.append(("ligne", a, b, couleur, ep))


def dessiner_traces(d):
    """Passe 1 : halo blanc (lisible sur l'acier foncé). Passe 2 : trait."""
    for passe in (0, 1):
        for t in TRACES:
            if t[0] == "ligne":
                _, a, b, couleur, ep = t
                d.line([pt(a), pt(b)], fill=BLANC if passe == 0 else couleur,
                       width=round((ep + 3.2 if passe == 0 else ep) * S))
            else:
                _, pointe, depuis, couleur, long_, larg = t
                if passe == 0:
                    long_, larg = long_ + 4, larg + 2.5
                (x1, y1), (x0, y0) = pt(pointe), pt(depuis)
                ang = math.atan2(y1 - y0, x1 - x0)
                if passe == 0:
                    x1, y1 = x1 + 2 * S * math.cos(ang), y1 + 2 * S * math.sin(ang)
                L, W = long_ * S, larg * S
                bx, by = x1 - L * math.cos(ang), y1 - L * math.sin(ang)
                nx, ny = -math.sin(ang) * W, math.cos(ang) * W
                d.polygon([(x1, y1), (bx + nx, by + ny), (bx - nx, by - ny)],
                          fill=BLANC if passe == 0 else couleur)


def pastille(d, centre, lettre, valeur):
    """Étiquette de cote : lettre en Poppins, valeur en mono, fond jaune arrondi."""
    f_l = police("Poppins-SemiBold.ttf", 21)
    f_v = police("IBMPlexMono-SemiBold.ttf", 21)
    wl = d.textlength(lettre, font=f_l)
    wv = d.textlength(valeur, font=f_v)
    esp = 9 * S
    pad_x, h = 15 * S, 40 * S
    w = pad_x * 2 + wl + esp + wv
    cx, cy = pt(centre)
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=JAUNE)
    d.text((x0 + pad_x, cy), lettre, font=f_l, fill=ENCRE, anchor="lm")
    d.text((x0 + pad_x + wl + esp, cy + 1 * S), valeur, font=f_v, fill=ENCRE, anchor="lm")
    return (x0 / S, y0 / S, (x0 + w) / S, (y0 + h) / S)


def cote(a, b, rappels, lettre, valeur, cle, position=0.5):
    """Trait de cote de a à b, étiquette à `position` (0,5 = milieu) le long du trait."""
    for r0, r1 in rappels:
        ligne(r0, r1, ACIER, 1.6)
    ligne(a, b, ENCRE)
    fleche(a, b, ENCRE)
    fleche(b, a, ENCRE)
    TRAITS_COTES.extend([None] * (len(PASTILLES) - len(TRAITS_COTES)))  # étiquettes sans trait (pinces)
    TRAITS_COTES.append((a, b))
    PASTILLES.append(((a[0] + (b[0] - a[0]) * position, a[1] + (b[1] - a[1]) * position), lettre, valeur, cle))


# Par type de section (rendu_profil.py) : (lettre, clé des données) des cotes verticale, horizontale, d'épaisseur
# pincée et d'aile supérieure ; lignes de la fiche (libellé, lettre, clé). Lettres des tableaux fournisseurs.
_I = (("h", "h"), ("b", "b"), ("tw", "tw"), ("tf", "tf"),
      [("Hauteur", "h", "h"), ("Largeur d'aile", "b", "b"), ("Épaisseur d'âme", "tw", "tw"), ("Épaisseur d'aile", "tf", "tf")])
COTES = {
    "I": _I,
    "U": _I,
    "T": (("h", "h"), ("b", "b"), ("t", "t"), None, [("Hauteur", "h", "h"), ("Largeur", "b", "b"), ("Épaisseur", "t", "t")]),
    "PLAT": (("b", "b"), None, ("t", "t"), None, [("Largeur", "b", "b"), ("Épaisseur", "t", "t")]),
    "ROND": (("d", "d"), None, None, None, [("Diamètre", "d", "d")]),
    "CARRE": (("a", "a"), ("a", "a"), None, None, [("Côté", "a", "a")]),
    "TC": (("b", "h"), ("b", "b"), ("t", "t"), None, [("Côté", "b", "b"), ("Épaisseur", "t", "t")]),
    "TR": (("h", "h"), ("b", "b"), ("t", "t"), None, [("Hauteur", "h", "h"), ("Largeur", "b", "b"), ("Épaisseur", "t", "t")]),
    "TUBE-ROND": (("d", "d"), None, ("t", "t"), None, [("Diamètre extérieur", "d", "d"), ("Épaisseur", "t", "t")]),
    "ROND-BETON": (("d", "d"), None, None, None, [("Diamètre nominal", "d", "d")]),
    # treillis : mailles a (le long) et b (en travers) entre axes des fils, diamètre des fils pincé
    "TREILLIS": (("a", "maille_a"), ("b", "maille_b"), ("d", "d"), None,
                 [("Maille", "", "maille"), ("Diamètre des fils", "d", "d"), ("Panneau", "", "format")]),
    # tôle : cote « verticale » = longueur (bord gauche, au sol), horizontale = largeur (devant) ; épaisseur en loupe
    "TOLE": (("L", "L"), ("l", "l"), None, None, [("Longueur", "L", "L"), ("Largeur", "l", "l"), ("Épaisseur", "e", "e")]),
}
DIAMETRE_LOUPE = 300


def placer_loupe(d, image_brute, W, H, P, geo, p, fleches_pince):
    """Loupe ronde sur le chant de la tôle : gros plan rendu par Blender (<slug>-loupe.png), placé là où il couvre
    le moins la pièce et les étiquettes, relié au point montré, avec la cote d'épaisseur pincée dedans."""
    D, r = DIAMETRE_LOUPE, DIAMETRE_LOUPE / 2
    alpha = image_brute.split()[3].point(lambda v: 255 if v >= 250 else 0)
    zones = [(c[0] - 95, c[1] - 30, c[0] + 95, c[1] + 30) for c, *_ in PASTILLES]
    # loupe dans la colonne de gauche laissée libre au cadrage, étiquette e dessous
    candidats = [(r + 30, y) for y in (H * 0.30, H * 0.40, H * 0.50, H * 0.60) if y + r + 80 < H - 60]
    ancres = P.get("loupe_ancres") or [P["loupe_ancre"]]

    def dans_zone(x, y):
        return any(a0 - 6 <= x <= a1 + 6 and b0 - 6 <= y <= b1 + 6 for a0, b0, a1, b1 in zones)

    def cout(cx, cy, ancre):
        masque = Image.new("L", (W, H), 0)
        ImageDraw.Draw(masque).ellipse([cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20], fill=255)
        piece = sum(ImageStat.Stat(Image.composite(alpha, Image.new("L", (W, H), 0), masque)).sum) / 255
        etiquettes = sum(1 for a0, b0, a1, b1 in zones if a0 < cx + r + 20 and cx - r - 20 < a1 and b0 < cy + r + 20 and cy - r - 20 < b1)
        # trait de liaison : court, hors des étiquettes et hors de la pièce (le dernier pixel touche le chant)
        dist = math.hypot(ancre[0] - cx, ancre[1] - cy) - r
        pts = [(cx + (ancre[0] - cx) * k / 40, cy + (ancre[1] - cy) * k / 40) for k in range(38)]
        pts = [q for q in pts if math.hypot(q[0] - cx, q[1] - cy) > r]
        croise = sum(1 for q in pts if dans_zone(*q))
        sur_piece = sum(1 for q in pts if 0 <= q[0] < W and 0 <= q[1] < H and alpha.getpixel((int(q[0]), int(q[1]))))
        return piece + (etiquettes + croise) * 1e6 + sur_piece * 400 + dist * 2

    cx, cy, ancre = min(((cx, cy, a) for cx, cy in candidats for a in ancres), key=lambda c: cout(*c))
    T = geo["loupe"]
    s = D / T
    loupe = rendu_sur_blanc(geo["chemin_loupe"]).resize((D, D), Image.LANCZOS)
    masque = Image.new("L", (D, D), 0)
    ImageDraw.Draw(masque).ellipse([0, 0, D - 1, D - 1], fill=255)
    fond = Image.new("RGBA", (D, D), (0, 0, 0, 0))  # transparent hors du disque
    fond.paste(loupe, (0, 0), masque)

    def dans_loupe(q):
        return (cx - r + q[0] * s, cy - r + q[1] * s)

    # liaison : du point du chant au bord de la loupe
    vx, vy = ancre[0] - cx, ancre[1] - cy
    n = math.hypot(vx, vy) or 1.0
    ligne(ancre, (cx + vx / n * (r + 4), cy + vy / n * (r + 4)), ACIER, 1.6)
    # épaisseur pincée dans la loupe (deux flèches verticales), étiquette sous la loupe
    haut, bas = dans_loupe(P["loupe_haut"]), dans_loupe(P["loupe_bas"])
    ligne(decale(haut, 0, -34), haut, ENCRE)
    fleche(haut, decale(haut, 0, -34), ENCRE)
    ligne(decale(bas, 0, 34), bas, ENCRE)
    fleche(bas, decale(bas, 0, 34), ENCRE)
    fleches_pince.append(("e", haut[0] - 7, haut[1] - 34, haut[0] + 7, haut[1]))
    fleches_pince.append(("e", bas[0] - 7, bas[1], bas[0] + 7, bas[1] + 34))
    PASTILLES.append(((cx, cy + r + 42), "e", affichable(p, "e"), "e"))
    return fond, (int(cx - r), int(cy - r)), (cx, cy, r)


def cotes_du_type(typ, p):
    if typ == "L":  # cornière (EN 10056) : ailes a et b, épaisseur t
        if p["valeurs"]["a"]["valeur"] == p["valeurs"]["b"]["valeur"]:
            return ("a", "a"), ("a", "b"), ("t", "t"), None, [("Aile", "a", "a"), ("Épaisseur", "t", "t")]
        return (("a", "a"), ("b", "b"), ("t", "t"), None,
                [("Grande aile", "a", "a"), ("Petite aile", "b", "b"), ("Épaisseur", "t", "t")])
    return COTES[typ]


def decale(p, dx, dy):
    return (p[0] + dx, p[1] + dy)


def rendu_sur_blanc(chemin, fondu=90, fiche=False):
    """Rendu sur fond blanc. `fiche` : l'ombre s'efface aussi avant la colonne de la fiche technique (x ≥ 0,655 W),
    pour que le texte reste sur un fond clair (grandes sections HEA/HEB, vérification du 14/09)."""
    rendu = Image.open(chemin).convert("RGBA")
    # ombre allégée : la pièce est opaque, l'ombre du sol est semi-transparente
    r_, g_, b_, a_ = rendu.split()
    piece = a_.point(lambda v: 255 if v >= 250 else 0)
    ombre = a_.point(lambda v: int(v * 0.55))
    if fondu:  # l'ombre s'efface vers le bord et disparaît sur les 24 derniers px : marges d'un blanc pur
        w, h = rendu.size

        def rampe(i, n):
            return min(255, int(255 * max(0, min(i, n - 1 - i) - 24) / (fondu - 24)))

        bord_x = Image.new("L", (w, 1))
        bord_x.putdata([rampe(x, w) for x in range(w)])
        bord_y = Image.new("L", (1, h))
        bord_y.putdata([rampe(y, h) for y in range(h)])
        masque = ImageChops.darker(bord_x.resize((w, h), Image.NEAREST), bord_y.resize((w, h), Image.NEAREST))
        if fiche:
            debut, fin = int(w * 0.58), int(w * 0.645)
            colonne = Image.new("L", (w, 1))
            colonne.putdata([255 if x < debut else max(0, int(255 * (fin - x) / (fin - debut))) for x in range(w)])
            masque = ImageChops.darker(masque, colonne.resize((w, h), Image.NEAREST))
        ombre = ImageChops.multiply(ombre, masque)
    a_ = Image.composite(a_, ombre, piece)
    rendu = Image.merge("RGBA", (r_, g_, b_, a_))
    fond = Image.new("RGBA", rendu.size, BLANC + (255,))
    return Image.alpha_composite(fond, rendu)


def enregistrer(image, base):
    image = image.convert("RGB")
    image.save(base + ".png", optimize=True)
    image.save(base + ".webp", quality=82, method=6)
    print("OK", base + ".webp", round(os.path.getsize(base + ".webp") / 1024), "Ko")


# ---------------------------------------------------------------- compositions

def studio(nom, dossier):
    enregistrer(rendu_sur_blanc(os.path.join(dossier, nom + ".png")), os.path.join(dossier, nom + "-studio"))


def caracteristiques(slug, dossier):
    image = rendu_sur_blanc(os.path.join(dossier, slug + ".png"), fiche=True)
    # fond de la colonne de la fiche, mesuré avant le texte : il doit rester clair
    fond_fiche = ImageStat.Stat(image.convert("L").crop((int(image.width * 0.655), 60, image.width - 40, image.height - 60))).extrema[0][0]
    with open(os.path.join(dossier, slug + ".json"), encoding="utf-8") as f:
        geo = json.load(f)
    P, W, H = geo["points"], geo["largeur"], geo["hauteur"]
    p = fiche(slug)

    calque = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    # (lettre, valeur, clé) des cotes : verticale, horizontale, épaisseur pincée, aile supérieure
    c_vert, c_horiz, c_pince, c_aile, c_fiche = cotes_du_type(geo.get("type", "I"), p)

    def cote_de(cfg):
        return (cfg[0], affichable(p, cfg[1]), cfg[1]) if cfg else (None, None, None)

    verticale, horizontale, pince, aile = (cote_de(c) for c in (c_vert, c_horiz, c_pince, c_aile))
    lignes_cotes = [(libelle, lettre, cle, affichable(p, cle)) for libelle, lettre, cle in c_fiche]

    if verticale[1]:
        # étiquette au milieu, descendue au tiers si la flèche d'épaisseur passe à sa hauteur (petites sections)
        bas_v, haut_v = P["cote_h_bas"], P["cote_h_haut"]
        position = 0.5
        milieu = ((bas_v[0] + haut_v[0]) / 2, (bas_v[1] + haut_v[1]) / 2)
        if pince[1]:
            ag = P["ame_gauche"]
            if abs(milieu[1] - ag[1]) < 48 and milieu[0] + 80 > ag[0] - 40:
                position = 0.28
        cote(bas_v, haut_v,
             [(P["rappel_h_bas_debut"], P["rappel_h_bas_fin"]), (P["rappel_h_haut_debut"], P["rappel_h_haut_fin"])],
             *verticale, position=position)
    if horizontale[1]:
        cote(P["cote_b_gauche"], P["cote_b_droit"],
             [(P["rappel_b_gauche_debut"], P["rappel_b_gauche_fin"]), (P["rappel_b_droit_debut"], P["rappel_b_droit_fin"])],
             *horizontale)
    fleches_pince = []  # zones des flèches d'épaisseur, qu'aucune étiquette ne doit couvrir
    if pince[1]:  # deux flèches qui pincent l'âme (ou la paroi), étiquette à droite
        ag, ad = P["ame_gauche"], P["ame_droite"]
        fleches_pince.append((pince[0], ag[0] - 34, ag[1] - 7, ag[0], ag[1] + 7))
        ligne(decale(ag, -34, 0), ag, ENCRE)
        fleche(ag, decale(ag, -34, 0), ENCRE)
        ligne(decale(ad, 34, 0), ad, ENCRE)
        fleche(ad, decale(ad, 34, 0), ENCRE)
        ligne(decale(ad, 34, 0), decale(ad, 64, 0), ENCRE)
        PASTILLES.append((decale(ad, 150, 0), *pince))
    if aile[1]:  # deux flèches qui pincent l'aile supérieure, étiquette au-dessus
        ext, inte = P["aile_haut_ext"], P["aile_haut_int"]
        fleches_pince.append((aile[0], inte[0] - 7, inte[1], inte[0] + 7, inte[1] + 34))
        ligne(decale(ext, 0, -34), ext, ENCRE)
        fleche(ext, decale(ext, 0, -34), ENCRE)
        ligne(decale(inte, 0, 34), inte, ENCRE)
        fleche(inte, decale(inte, 0, 34), ENCRE)
        ligne(decale(ext, 0, -34), decale(ext, 0, -58), ENCRE)
        PASTILLES.append((decale(ext, 0, -80), *aile))
    loupe = None
    if geo.get("type") == "TOLE":  # épaisseur en loupe : trop fine à l'échelle de la plaque entière
        geo["chemin_loupe"] = os.path.join(dossier, slug + "-loupe.png")
        with Image.open(os.path.join(dossier, slug + ".png")) as brute:
            fond_loupe, coin, loupe = placer_loupe(d, brute.convert("RGBA"), W, H, P, geo, p, fleches_pince)
        image.alpha_composite(fond_loupe, dest=coin)

    dessiner_traces(d)
    if loupe:  # anneau blanc et filet gris autour de la loupe
        cx, cy, r = loupe
        d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], outline=BLANC, width=7 * S)
        d.ellipse([(cx - r - 5) * S, (cy - r - 5) * S, (cx + r + 5) * S, (cy + r + 5) * S], outline=BRUME, width=2 * S)
    boites = [pastille(d, centre, lettre, valeur) for centre, lettre, valeur, _ in PASTILLES]

    # ---- fiche technique, colonne de droite
    x0 = int(W * 0.655) * S
    x1 = (W - 64) * S
    surtitre = surtitre_image(p["categorie"])
    titre = titre_image(p["nom"])

    f_sur = police("Questrial-Regular.ttf", 17)
    # titre : lignes remplies mot à mot dans la largeur de la colonne (3 au plus), corps réduit si besoin
    for taille in (44, 38, 34):
        f_titre = police("Poppins-SemiBold.ttf", taille)
        lignes_titre = []
        # « 5m x 2m » reste sur une ligne : le « x » est lié à ses voisins
        for mot in re.sub(r" x (?=\S)", " x ", titre).split(" "):
            essai = f"{lignes_titre[-1]} {mot}" if lignes_titre else mot
            if lignes_titre and d.textlength(essai, font=f_titre) <= x1 - x0:
                lignes_titre[-1] = essai
            else:
                lignes_titre.append(mot)
        lignes_titre = [t.replace(" ", " ") for t in lignes_titre]
        if len(lignes_titre) <= 3 and all(d.textlength(t, font=f_titre) <= x1 - x0 for t in lignes_titre):
            break
    interligne_titre = round(taille * 1.25) * S
    f_label = police("Questrial-Regular.ttf", 19)
    f_valeur = police("IBMPlexMono-Medium.ttf", 19)
    f_note = police("Questrial-Regular.ttf", 14)

    finition = p["valeurs"].get("finition")
    finition = FINITIONS.get(finition["valeur"], finition["valeur"]) if finition and not finition.get("supposee") else None
    lignes = lignes_cotes + [
        ("Poids", "", "poids", affichable(p, "poids")),
        ("Nuance", "", "nuance", affichable(p, "nuance")),
        ("Norme", "", "norme", affichable(p, "norme")),
        ("Surface", "", "surface", affichable(p, "surface")),
        ("Procédé", "", "procede", affichable(p, "procede")),
        ("Finition", "", "finition", finition),
    ]
    lignes = [l for l in lignes if l[3]]

    pas = 54 * S
    hauteur_titre = 64 * S + interligne_titre * (len(lignes_titre) - 1)
    hauteur_bloc = 30 * S + hauteur_titre + 34 * S + pas * len(lignes)
    y = (H * S - hauteur_bloc) // 2

    d.text((x0, y), surtitre, font=f_sur, fill=GRIS_TEXTE, anchor="lt")
    y += 30 * S
    for i, t in enumerate(lignes_titre):
        d.text((x0, y + i * interligne_titre), t, font=f_titre, fill=ENCRE, anchor="lt")
    largeur_titre = max(d.textlength(t, font=f_titre) for t in lignes_titre) / S
    y += hauteur_titre
    d.rectangle([x0, y, x0 + 56 * S, y + 6 * S], fill=JAUNE)
    y += 34 * S

    for label, lettre, _, valeur in lignes:
        d.line([(x0, y), (x1, y)], fill=BRUME, width=S)
        cy = y + pas // 2
        d.text((x0, cy), label, font=f_label, fill=GRIS_TEXTE, anchor="lm")
        if lettre:
            wl = d.textlength(label, font=f_label)
            d.text((x0 + wl + 10 * S, cy), lettre, font=police("Poppins-SemiBold.ttf", 15), fill=ACIER, anchor="lm")
        if re.search(r"\d", valeur) and not re.search(r"[a-zé]{4,}", valeur):
            d.text((x1, cy + 1 * S), valeur, font=f_valeur, fill=ENCRE, anchor="rm")
        else:
            d.text((x1, cy), valeur, font=police("Questrial-Regular.ttf", 20), fill=ENCRE, anchor="rm")
        y += pas
    d.line([(x0, y), (x1, y)], fill=BRUME, width=S)

    d.text((64 * S, (H - 44) * S), "Rendu 3D aux cotes nominales — illustration non contractuelle",
           font=f_note, fill=ACIER, anchor="lm")

    # contrôles : étiquettes dans l'image, sans chevauchement entre elles ni avec la fiche
    problemes = []
    for i, (a0, b0, a1, b1) in enumerate(boites):
        if a0 < 8 or b0 < 8 or a1 > W - 8 or b1 > H - 8:
            problemes.append(f"étiquette {PASTILLES[i][1]} hors cadre")
        if a1 > W * 0.655 - 12:
            problemes.append(f"étiquette {PASTILLES[i][1]} empiète sur la fiche")
        for j in range(i):
            c0, e0, c1, e1 = boites[j]
            if a0 < c1 and c0 < a1 and b0 < e1 and e0 < b1:
                problemes.append(f"étiquettes {PASTILLES[j][1]} et {PASTILLES[i][1]} se chevauchent")
        # flèche d'épaisseur (côté extérieur) couverte ou touchée par une étiquette : marge de 6 px
        for lettre, f0, g0, f1, g1 in fleches_pince:
            if a0 - 6 < f1 and f0 < a1 + 6 and b0 - 6 < g1 and g0 < b1 + 6:
                problemes.append(f"flèche {lettre} sous l'étiquette {PASTILLES[i][1]}")
    if loupe:
        cx, cy, r = loupe
        if cx - r < 8 or cy - r < 8 or cy + r > H - 8 or cx + r > W * 0.655 - 12:
            problemes.append("loupe hors de la zone de dessin")
        for i, (a0, b0, a1, b1) in enumerate(boites):
            if a0 < cx + r + 5 and cx - r - 5 < a1 and b0 < cy + r + 5 and cy - r - 5 < b1:
                problemes.append(f"loupe sous l'étiquette {PASTILLES[i][1]}")
    # pointes de flèche de chaque cote visibles : hors de sa propre étiquette (cotes courtes : cornières, T, plats)
    for i, (centre, lettre, _, _) in enumerate(PASTILLES):
        if i < len(TRAITS_COTES) and TRAITS_COTES[i]:
            a0, b0, a1, b1 = boites[i]
            for pointe in TRAITS_COTES[i]:
                if a0 - 6 < pointe[0] < a1 + 6 and b0 - 6 < pointe[1] < b1 + 6:
                    problemes.append(f"pointe de la cote {lettre} sous son étiquette")
    if fond_fiche < 238:
        problemes.append(f"fond de la fiche technique trop sombre ({fond_fiche}/255)")
    if x0 / S + largeur_titre > x1 / S:
        problemes.append("titre trop long pour la colonne")
    if y / S > H - 70:
        problemes.append("fiche technique trop haute : elle touche la note de bas de page")

    calque = calque.resize((W, H), Image.LANCZOS)
    image = Image.alpha_composite(image, calque)
    enregistrer(image, os.path.join(dossier, slug + "-caracteristiques"))
    # textes réellement écrits et contrôles, relus par controler_rendus.py
    with open(os.path.join(dossier, slug + "-caracteristiques.controles.json"), "w", encoding="utf-8") as f:
        json.dump({"surtitre": surtitre, "titre": titre,
                   "fiche": [[label, lettre, cle, valeur] for label, lettre, cle, valeur in lignes],
                   "pastilles": [[lettre, cle, valeur] for _, lettre, valeur, cle in PASTILLES], "problemes": problemes},
                  f, ensure_ascii=False, indent=1)
    print("CONTROLES :", "; ".join(problemes) if problemes else "aucun problème")


if __name__ == "__main__":
    args = sys.argv[1:]
    # --essai : rendus d'essai (rendu3d/essais/), jamais melanges a la production (rendu3d/final/)
    dossier = os.path.join(TRAVAIL, "essais" if "--essai" in args else "final")
    args = [a for a in args if a != "--essai"]
    if args[0] == "--studio":
        studio(args[1], dossier)
    else:
        caracteristiques(args[0], dossier)
