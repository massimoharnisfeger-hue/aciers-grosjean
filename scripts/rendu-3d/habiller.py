"""
Habillage 2D des rendus Blender.

  python scripts/rendu-3d/habiller.py <slug>            visuel caracteristiques : cotes + fiche technique
  python scripts/rendu-3d/habiller.py --studio <nom>    photo studio : fond blanc pur, ombre douce

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

from PIL import Image, ImageDraw, ImageFont

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


def affichable(p, cle):
    """Valeur formatée pour l'image, ou None si absente ou supposée."""
    d = p["valeurs"].get(cle)
    if not d or d.get("supposee"):
        return None
    v, unite = d["valeur"], d.get("unite", "")
    if isinstance(v, (int, float)):
        texte = f"{v:.2f}" if unite == "kg/m" else f"{v:g}"
        return f"{texte.replace('.', ',')} {unite}".strip()
    return str(v)


# ---------------------------------------------------------------- tracé

def pt(p):
    return (p[0] * S, p[1] * S)


TRACES = []  # tracés en deux passes, halo blanc puis trait
PASTILLES = []


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


def cote(a, b, rappels, lettre, valeur):
    for r0, r1 in rappels:
        ligne(r0, r1, ACIER, 1.6)
    ligne(a, b, ENCRE)
    fleche(a, b, ENCRE)
    fleche(b, a, ENCRE)
    PASTILLES.append((((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), lettre, valeur))


def decale(p, dx, dy):
    return (p[0] + dx, p[1] + dy)


def rendu_sur_blanc(chemin):
    rendu = Image.open(chemin).convert("RGBA")
    # ombre allégée : la pièce est opaque, l'ombre du sol est semi-transparente
    r_, g_, b_, a_ = rendu.split()
    a_ = a_.point(lambda v: v if v >= 250 else int(v * 0.55))
    rendu = Image.merge("RGBA", (r_, g_, b_, a_))
    fond = Image.new("RGBA", rendu.size, BLANC + (255,))
    return Image.alpha_composite(fond, rendu)


def enregistrer(image, base):
    image = image.convert("RGB")
    image.save(base + ".png", optimize=True)
    image.save(base + ".webp", quality=82, method=6)
    print("OK", base + ".webp", round(os.path.getsize(base + ".webp") / 1024), "Ko")


# ---------------------------------------------------------------- compositions

def studio(nom):
    dossier = os.path.join(TRAVAIL, "final")
    enregistrer(rendu_sur_blanc(os.path.join(dossier, nom + ".png")), os.path.join(dossier, nom + "-studio"))


def caracteristiques(slug):
    dossier = os.path.join(TRAVAIL, "final")
    image = rendu_sur_blanc(os.path.join(dossier, slug + ".png"))
    with open(os.path.join(dossier, slug + ".json"), encoding="utf-8") as f:
        geo = json.load(f)
    P, W, H = geo["points"], geo["largeur"], geo["hauteur"]
    p = fiche(slug)

    calque = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    h_val, b_val = affichable(p, "h"), affichable(p, "b")
    tw_val, tf_val = affichable(p, "tw"), affichable(p, "tf")

    if h_val:
        cote(P["cote_h_bas"], P["cote_h_haut"],
             [(P["rappel_h_bas_debut"], P["rappel_h_bas_fin"]), (P["rappel_h_haut_debut"], P["rappel_h_haut_fin"])],
             "h", h_val)
    if b_val:
        cote(P["cote_b_gauche"], P["cote_b_droit"],
             [(P["rappel_b_gauche_debut"], P["rappel_b_gauche_fin"]), (P["rappel_b_droit_debut"], P["rappel_b_droit_fin"])],
             "b", b_val)
    if tw_val:  # deux flèches qui pincent l'âme, étiquette à droite
        ag, ad = P["ame_gauche"], P["ame_droite"]
        ligne(decale(ag, -34, 0), ag, ENCRE)
        fleche(ag, decale(ag, -34, 0), ENCRE)
        ligne(decale(ad, 34, 0), ad, ENCRE)
        fleche(ad, decale(ad, 34, 0), ENCRE)
        ligne(decale(ad, 34, 0), decale(ad, 64, 0), ENCRE)
        PASTILLES.append((decale(ad, 150, 0), "tw", tw_val))
    if tf_val:  # deux flèches qui pincent l'aile supérieure, étiquette au-dessus
        ext, inte = P["aile_haut_ext"], P["aile_haut_int"]
        ligne(decale(ext, 0, -34), ext, ENCRE)
        fleche(ext, decale(ext, 0, -34), ENCRE)
        ligne(decale(inte, 0, 34), inte, ENCRE)
        fleche(inte, decale(inte, 0, 34), ENCRE)
        ligne(decale(ext, 0, -34), decale(ext, 0, -58), ENCRE)
        PASTILLES.append((decale(ext, 0, -80), "tf", tf_val))

    dessiner_traces(d)
    boites = [pastille(d, centre, lettre, valeur) for centre, lettre, valeur in PASTILLES]

    # ---- fiche technique, colonne de droite
    x0 = int(W * 0.655) * S
    x1 = (W - 64) * S
    univers, famille = [s for s in p["categorie"].split("/") if s][:2]
    surtitre = f"{univers.upper()}  ·  {famille.replace('-', ' ').upper()}"
    titre = re.sub(r"\s+en acier$", "", p["nom"].strip())

    f_sur = police("Questrial-Regular.ttf", 17)
    f_titre = police("Poppins-SemiBold.ttf", 44)
    f_label = police("Questrial-Regular.ttf", 19)
    f_valeur = police("IBMPlexMono-Medium.ttf", 19)
    f_note = police("Questrial-Regular.ttf", 14)

    finition = p["valeurs"].get("finition")
    finition = FINITIONS.get(finition["valeur"], finition["valeur"]) if finition and not finition.get("supposee") else None
    lignes = [
        ("Hauteur", "h", h_val),
        ("Largeur d'aile", "b", b_val),
        ("Épaisseur d'âme", "tw", tw_val),
        ("Épaisseur d'aile", "tf", tf_val),
        ("Poids", "", affichable(p, "poids")),
        ("Nuance", "", affichable(p, "nuance")),
        ("Norme", "", affichable(p, "norme")),
        ("Procédé", "", affichable(p, "procede")),
        ("Finition", "", finition),
    ]
    lignes = [l for l in lignes if l[2]]

    pas = 54 * S
    hauteur_bloc = 30 * S + 64 * S + 34 * S + pas * len(lignes)
    y = (H * S - hauteur_bloc) // 2

    d.text((x0, y), surtitre, font=f_sur, fill=GRIS_TEXTE, anchor="lt")
    y += 30 * S
    d.text((x0, y), titre, font=f_titre, fill=ENCRE, anchor="lt")
    largeur_titre = d.textlength(titre, font=f_titre) / S
    y += 64 * S
    d.rectangle([x0, y, x0 + 56 * S, y + 6 * S], fill=JAUNE)
    y += 34 * S

    for label, lettre, valeur in lignes:
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
    if x0 / S + largeur_titre > W - 40:
        problemes.append("titre trop long pour la colonne")

    calque = calque.resize((W, H), Image.LANCZOS)
    image = Image.alpha_composite(image, calque)
    enregistrer(image, os.path.join(dossier, slug + "-caracteristiques"))
    print("CONTROLES :", "; ".join(problemes) if problemes else "aucun problème")


if __name__ == "__main__":
    if sys.argv[1] == "--studio":
        studio(sys.argv[2])
    else:
        caracteristiques(sys.argv[1])
