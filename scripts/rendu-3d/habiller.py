"""
Habillage 2D d'un rendu Blender : cotes sur la section + fiche technique.

Usage : python scripts/rendu-3d/habiller.py <slug>
Lit    %LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/final/<slug>.png et <slug>.json,
       et la fiche dans lib/catalogue.ts
Écrit  final/<slug>-caracteristiques.png et .webp (même dossier)
Polices (Google Fonts, OFL) attendues dans rendu3d/polices : Poppins-SemiBold,
Questrial-Regular, IBMPlexMono-Medium, IBMPlexMono-SemiBold.
"""

import json
import math
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
CATALOGUE = os.path.join(os.path.dirname(os.path.dirname(ICI)), "lib", "catalogue.ts")
# rendus et polices hors OneDrive (fichiers lourds, non versionnés)
TRAVAIL = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "SiteAciersGrosjean", "rendu3d")
POLICES = os.path.join(TRAVAIL, "polices")

# charte (tailwind.config.ts)
ENCRE = (51, 54, 66)
JAUNE = (255, 213, 0)
ACIER = (170, 176, 179)
BRUME = (209, 214, 218)
GRIS_TEXTE = (110, 115, 124)

S = 2  # suréchantillonnage du tracé


def police(nom, taille):
    return ImageFont.truetype(os.path.join(POLICES, nom), taille * S)


def lire_fiche(slug):
    with open(CATALOGUE, encoding="utf-8") as f:
        for ligne in f:
            if ligne.lstrip().startswith(f'"{slug}": {{'):
                nom = re.search(r'nom: "(.*?)"', ligne).group(1)
                categorie = re.search(r'categorie: "(.*?)"', ligne).group(1)
                specs = re.findall(r'\{ label: "(.*?)", valeur: "(.*?)" \}', ligne)
                return {"nom": nom, "categorie": categorie, "specs": specs}
    raise SystemExit(f"Produit introuvable dans le catalogue : {slug}")


def spec(fiche, debut):
    for label, valeur in fiche["specs"]:
        if label.startswith(debut):
            return valeur
    return None


# ---------------------------------------------------------------- tracé

def pt(p):
    return (p[0] * S, p[1] * S)


BLANC = (255, 255, 255)
TRACES = []  # (type, args) : tracés en deux passes, halo blanc puis trait


def fleche(d, pointe, depuis, couleur, long_=13, larg=5.5):
    TRACES.append(("fleche", pointe, depuis, couleur, long_, larg))


def ligne(d, a, b, couleur, ep=2.2):
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


def pastille(d, centre, lettre, valeur, fond=JAUNE):
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
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=fond)
    d.text((x0 + pad_x, cy), lettre, font=f_l, fill=ENCRE, anchor="lm")
    d.text((x0 + pad_x + wl + esp, cy + 1 * S), valeur, font=f_v, fill=ENCRE, anchor="lm")


PASTILLES = []


def cote(d, a, b, rappels, lettre, valeur):
    for r0, r1 in rappels:
        ligne(d, r0, r1, ACIER, 1.6)
    ligne(d, a, b, ENCRE)
    fleche(d, a, b, ENCRE)
    fleche(d, b, a, ENCRE)
    PASTILLES.append((((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), lettre, valeur))


def milieu(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def decale(p, dx, dy):
    return (p[0] + dx, p[1] + dy)


# ---------------------------------------------------------------- composition

def main():
    slug = sys.argv[1]
    dossier = os.path.join(TRAVAIL, "final")
    rendu = Image.open(os.path.join(dossier, slug + ".png")).convert("RGBA")
    # ombre allégée : la pièce est opaque, l'ombre du sol est semi-transparente
    r_, g_, b_, a_ = rendu.split()
    a_ = a_.point(lambda v: v if v >= 250 else int(v * 0.55))
    rendu = Image.merge("RGBA", (r_, g_, b_, a_))
    with open(os.path.join(dossier, slug + ".json"), encoding="utf-8") as f:
        geo = json.load(f)
    P = geo["points"]
    W, H = geo["largeur"], geo["hauteur"]
    fiche = lire_fiche(slug)

    image = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    image = Image.alpha_composite(image, rendu)

    calque = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    h_val = spec(fiche, "Hauteur")
    b_val = spec(fiche, "Largeur")
    tw_val = spec(fiche, "Épaisseur d'âme")
    tf_val = spec(fiche, "Épaisseur d'aile")

    # h : à gauche de la section
    cote(d, P["cote_h_bas"], P["cote_h_haut"],
         [(P["rappel_h_bas_debut"], P["rappel_h_bas_fin"]),
          (P["rappel_h_haut_debut"], P["rappel_h_haut_fin"])],
         "h", h_val)

    # b : sous la section
    cote(d, P["cote_b_gauche"], P["cote_b_droit"],
         [(P["rappel_b_gauche_debut"], P["rappel_b_gauche_fin"]),
          (P["rappel_b_droit_debut"], P["rappel_b_droit_fin"])],
         "b", b_val)

    # tw : deux flèches qui pincent l'âme, étiquette à droite
    ag, ad = P["ame_gauche"], P["ame_droite"]
    ligne(d, decale(ag, -34, 0), ag, ENCRE)
    fleche(d, ag, decale(ag, -34, 0), ENCRE)
    ligne(d, decale(ad, 34, 0), ad, ENCRE)
    fleche(d, ad, decale(ad, 34, 0), ENCRE)
    ligne(d, decale(ad, 34, 0), decale(ad, 64, 0), ENCRE)
    PASTILLES.append((decale(ad, 150, 0), "tw", tw_val))

    # tf : deux flèches qui pincent l'aile supérieure, étiquette au-dessus
    ext, inte = P["aile_haut_ext"], P["aile_haut_int"]
    ligne(d, decale(ext, 0, -34), ext, ENCRE)
    fleche(d, ext, decale(ext, 0, -34), ENCRE)
    ligne(d, decale(inte, 0, 34), inte, ENCRE)
    fleche(d, inte, decale(inte, 0, 34), ENCRE)
    ligne(d, decale(ext, 0, -34), decale(ext, 0, -58), ENCRE)
    PASTILLES.append((decale(ext, 0, -80), "tf", tf_val))

    dessiner_traces(d)
    for centre, lettre, valeur in PASTILLES:
        pastille(d, centre, lettre, valeur)

    # ---- fiche technique, colonne de droite
    x0 = int(W * 0.655) * S
    x1 = (W - 64) * S
    univers, famille = [s for s in fiche["categorie"].split("/") if s][:2]
    surtitre = f"{univers.upper()}  ·  {famille.replace('-', ' ').upper()}"
    titre = re.sub(r"\s+en acier$", "", fiche["nom"])

    f_sur = police("Questrial-Regular.ttf", 17)
    f_titre = police("Poppins-SemiBold.ttf", 44)
    f_label = police("Questrial-Regular.ttf", 19)
    f_valeur = police("IBMPlexMono-Medium.ttf", 19)
    f_note = police("Questrial-Regular.ttf", 14)

    nuance = spec(fiche, "Nuance") or ""
    nuance_seule, _, norme = nuance.partition(" — ")
    lignes = [
        ("Hauteur", "h", h_val),
        ("Largeur d'aile", "b", b_val),
        ("Épaisseur d'âme", "tw", tw_val),
        ("Épaisseur d'aile", "tf", tf_val),
        ("Poids", "", spec(fiche, "Poids")),
        ("Nuance", "", nuance_seule),
        ("Norme", "", norme),
        ("Procédé", "", spec(fiche, "Procédé")),
    ]
    lignes = [l for l in lignes if l[2]]

    pas = 54 * S
    hauteur_bloc = 30 * S + 64 * S + 34 * S + pas * len(lignes)
    y = (H * S - hauteur_bloc) // 2

    d.text((x0, y), surtitre, font=f_sur, fill=GRIS_TEXTE, anchor="lt")
    y += 30 * S
    d.text((x0, y), titre, font=f_titre, fill=ENCRE, anchor="lt")
    y += 64 * S
    d.rectangle([x0, y, x0 + 56 * S, y + 6 * S], fill=JAUNE)
    y += 34 * S

    for label, lettre, valeur in lignes:
        d.line([(x0, y), (x1, y)], fill=BRUME, width=S)
        cy = y + pas // 2
        d.text((x0, cy), label, font=f_label, fill=GRIS_TEXTE, anchor="lm")
        if lettre:
            wl = d.textlength(label, font=f_label)
            d.text((x0 + wl + 10 * S, cy), lettre, font=police("Poppins-SemiBold.ttf", 15),
                   fill=ACIER, anchor="lm")
        # chiffres en mono, texte courant en Questrial
        if re.search(r"\d", valeur):
            d.text((x1, cy + 1 * S), valeur, font=f_valeur, fill=ENCRE, anchor="rm")
        else:
            d.text((x1, cy), valeur, font=police("Questrial-Regular.ttf", 20), fill=ENCRE, anchor="rm")
        y += pas
    d.line([(x0, y), (x1, y)], fill=BRUME, width=S)

    d.text((64 * S, (H - 44) * S), "Rendu 3D aux cotes nominales — illustration non contractuelle",
           font=f_note, fill=ACIER, anchor="lm")

    calque = calque.resize((W, H), Image.LANCZOS)
    image = Image.alpha_composite(image, calque).convert("RGB")

    base = os.path.join(dossier, slug + "-caracteristiques")
    image.save(base + ".png", optimize=True)
    image.save(base + ".webp", quality=82, method=6)
    print("OK", base + ".webp", round(os.path.getsize(base + ".webp") / 1024), "Ko")


main()
