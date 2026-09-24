"""
Controles automatiques des visuels 3D, sur toutes les images d'une ou plusieurs familles, avant la verification
independante (agent verificateur-rendus) et l'integration sur le site.

  python scripts/rendu-3d/controler_rendus.py poutrelle-ipe [poutrelle-hea ...]

Pour chaque famille (cle `famille` de scripts/rendu-3d/donnees/produits.json) :
- fichiers : <slug>.png (rendu brut), <slug>-caracteristiques.png/.webp/.controles.json par fiche,
  studio-<famille>.png et studio-<famille>-studio.png/.webp pour la categorie ;
- images finales en 1600 x 1200 ou 2400 x 1800 (barres, profilés et tubes refaits le 24/09, ADR-0012), WebP < 200 Ko ;
  les seuils en pixels, réglés en 1600 px, suivent la taille du rendu ;
- piece entierement dans le cadre (rendu brut), et a gauche de la fiche technique sur le visuel caracteristiques ;
- photo studio : marges d'un blanc pur ;
- fiches et photo studio servies : bord de la piece net, sans lisere clair (large plat, 24/09 ; V15) ;
- visuel caracteristiques : aucun probleme d'etiquette releve par habiller.py ; chaque texte ecrit = donnee sourcee
  non supposee ; meme valeur que la fiche produit du site (lib/catalogue.ts + lib/site-actuel.json).
Ecrit des planches contact (12 images) dans %LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/controle/.
Code de sortie 1 s'il reste un ecart.
"""
import json
import os
import re
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat

import recadrer_visuels
from habiller import FINITIONS, LARGEUR_REFERENCE, texte_longueurs, titre_image

ICI = Path(__file__).resolve().parent
PROJET = ICI.parents[1]
TRAVAIL = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "rendu3d"
FINAL, CONTROLE = TRAVAIL / "final", TRAVAIL / "controle"
LARGEUR, HAUTEUR, WEBP_MAX_KO = 1600, 1200, 200
TAILLES = {(1600, 1200), (2400, 1800)}  # 2400 px : barres, profilés et tubes refaits le 24/09 (ADR-0012)
COLONNE_FICHE = 0.655  # debut de la fiche technique (habiller.py)

# libelles des specifications de la page produit -> cles des donnees (plusieurs cles : « 100 × 50 mm »)
PAGE = {"Hauteur (h)": ["h"], "Largeur d'aile (b)": ["b"], "Épaisseur d'âme (tw)": ["tw"], "Épaisseur d'aile (tf)": ["tf"],
        "Ailes": ["a", "b"], "Section": ["h", "b"], "Largeur": ["b"], "Épaisseur": ["t"], "Diamètre": ["d"],
        "Diamètre extérieur": ["d"], "Surface": ["surface"], "Nuance": ["nuance"], "Norme": ["norme"]}
PAGE_PAR_SERIE = {"CARRE": {"Section": ["a", "a"]}, "TOLE": {"Format": ["L", "l"], "Épaisseur": ["e"]},
                  "TREILLIS": {"Maille": ["maille"], "Fil": ["d"], "Panneau": ["format"]},
                  "U-ALU": {"Section": ["b", "h", "b"], "Épaisseur": ["tw"]},
                  "TOLE-RELIEF": {"Format": ["L", "l"], "Épaisseur": ["e", "e_total"]},
                  "TOLE-PERFOREE": {"Format": ["L", "l"], "Épaisseur": ["e"]},
                  # libellés ajoutés par specs_sourcees() du générateur (15/09) : la page reprend les valeurs sourcées de l'image
                  "BORDURE": {"Hauteur": ["h"], "Pli": ["pli"], "Longueur": ["L"], "Épaisseur": ["e"]},
                  "TOLE-PROFILEE": {"Longueur": ["L"], "Largeur": ["l"], "Couleur": ["couleur"], "Largeur utile": ["l_utile"],
                                    "Hauteur de nervure": ["h"], "Pas des nervures": ["pas"], "Épaisseur": ["e"],
                                    "Masse surfacique": ["masse"], "Revêtement": ["revetement"]},
                  "PANNEAU-ISOLE": {"Longueur": ["L"], "Largeur": ["l"], "Épaisseur": ["e"], "Couleur": ["couleur"],
                                    "Largeur utile": ["l_utile"], "Nervures": ["nervures"], "Face externe": ["face_externe"],
                                    "Face interne": ["face_interne"], "Âme": ["ame"]},
                  "TASSEAU": {"Longueur": ["L"], "Largeur": ["l_utile"], "Tasseau": ["tasseau"], "Teinte": ["teinte"],
                              "Hauteur d'onde": ["h"], "Épaisseur": ["e"], "Masse surfacique": ["masse"],
                              "Revêtement": ["revetement"]},
                  "PANNEAU-CLOTURE": {"Modèle": ["modele"], "Hauteur": ["H"], "Fils": ["fil_h", "fil_v"], "Couleur": ["couleur"],
                                      "Largeur": ["l"], "Maille": ["maille"], "Revêtement": ["revetement"]},
                  "POTEAU": {"Modèle": ["modele"], "Longueur": ["L"], "Couleur": ["couleur"], "Section": ["b", "h"],
                             "Matière": ["matiere"], "Revêtement": ["revetement"]},
                  # « Barreaux porteurs 30 × 2 mm » = hauteur h × épaisseur t du barreau (la pastille h est donc sur la page)
                  "CAILLEBOTIS": {"Dimensions": ["L", "l"], "Maille": ["maille"], "Barreaux porteurs": ["h", "t"],
                                  "Revêtement": ["revetement"]},
                  "MARCHE-CAILLEBOTIS": {"Dimensions": ["L", "l"], "Revêtement": ["revetement"]},
                  "MARCHE-O2": {"Dimensions": ["L", "l"], "Trous emboutis": ["trous"], "Trous de drainage": ["drainage"],
                                "Entraxe": ["entraxe"]},
                  "PLANCHER-O2": {"Dimensions": ["L", "l"], "Hauteur": ["h"], "Épaisseur": ["t"], "Trous emboutis": ["trous"],
                                  "Trous de drainage": ["drainage"], "Entraxe": ["entraxe"], "Revêtement": ["revetement"]}}
COTES_AFFICHABLES = {"h", "b", "tw", "tf", "a", "t", "d", "L", "l", "e", "e_total", "nuance", "norme", "H", "pli"}


def nombre(texte):
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(texte))
    return float(m.group(0).replace(",", ".")) if m else None


def meme_valeur(a, b):
    na, nb = nombre(a), nombre(b)
    if isinstance(a, (int, float)) or isinstance(b, (int, float)):
        return na is not None and nb is not None and abs(na - nb) < 1e-6
    return str(a).strip() == str(b).strip()


def specs_page():
    """slug -> {libelle: valeur} tel qu'affiche par la page (specs du catalogue, poids et finition du site actuel)."""
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    reel = json.loads((PROJET / "lib" / "site-actuel.json").read_text(encoding="utf-8"))
    desc = json.loads((PROJET / "lib" / "descriptions-site-actuel.json").read_text(encoding="utf-8"))
    pages = {}
    for m in re.finditer(r'^\s*"([^"]+)": \{ slug: .*?specs: \[(.*)\] \},$', ts, re.M):
        specs = dict(re.findall(r'\{ label: "([^"]+)", valeur: "([^"]*)" \}', m.group(2)))
        r = reel.get(m.group(1), {})
        specs.pop("Poids", None)  # remplace a la fusion quand le site actuel donne un poids
        for cle in r.get("specsRetirees", []):
            specs.pop(cle, None)
        if r.get("kg") is not None:
            specs["Poids"] = r["kg"]
        if r.get("finition"):
            specs["Finition"] = r["finition"]
        if r.get("longueurs"):  # « Longueurs standard » de la page (app/p/[slug]/page.tsx)
            specs["Longueurs"] = r["longueurs"]
        d = desc.get(m.group(1), {})  # la description est affichée sur la page, sous les spécifications
        specs["_texte"] = d.get("courte", "") + " " + " ".join(b.get("texte", " ".join(b.get("items", [])))
                                                             for b in d.get("blocs", []))
        pages[m.group(1)] = specs
    return pages


def seuil_opaque(alpha):
    """Seuil d'alpha de la pièce : 250 d'ordinaire ; 128 pour les pièces en fils fins, dont presque aucun pixel n'est
    entièrement opaque (studio des panneaux MEDIUM 3D : alpha maximal 240 ; les ombres restent sous 50). 15/09."""
    histo = alpha.histogram()
    return 250 if sum(histo[250:]) >= 2000 else 128


def cadre_piece(chemin):
    """Boite des pixels opaques du rendu brut (la piece, sans l'ombre) ; None si aucun."""
    with Image.open(chemin) as img:
        alpha = img.convert("RGBA").split()[3]
    s = seuil_opaque(alpha)
    return alpha.point(lambda v: 255 if v >= s else 0).getbbox()


def part_noire(chemin, creux=False):
    """Part des pixels quasi noirs dans la silhouette de la pièce (rendu brut). Une géométrie cassée (faces
    retournées, arrondi plus grand que l'épaisseur) donne de grandes zones noires ; l'intérieur d'un tube est
    sombre à bon droit, d'où un seuil plus haut pour les sections creuses."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    clair = ImageChops.lighter(ImageChops.lighter(r, g), b)
    dans_piece = sum(1 for v in a.tobytes() if v >= 250)
    noirs = sum(1 for v, al in zip(clair.tobytes(), a.tobytes()) if al >= 250 and v <= 6)
    return noirs / max(dans_piece, 1)


def part_claire(chemin, x0, y0, x1, y1, seuil=90):
    """Part des pixels de pièce (rendu brut, opaques) plus clairs que `seuil` dans un rectangle de l'image."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA").crop((int(x0), int(y0), int(x1) + 1, int(y1) + 1))
    gris, alpha = rgba.convert("L"), rgba.split()[3]
    n = rgba.width * rgba.height
    return sum(1 for v, a in zip(gris.getdata(), alpha.getdata()) if a >= 250 and v > seuil) / max(n, 1)


def luminance_piece(chemin, moitie_arriere=False, seuil_sombre=80, x_max=None):
    """(luminance moyenne, part des pixels sous `seuil_sombre`) de la silhouette de la pièce (rendu brut) ; avec
    `moitie_arriere`, seulement la moitié droite de sa boîte (le corps de la barre, sans la face coupée) ; avec
    `x_max` (fraction de la largeur), seulement ce qui est à gauche de x_max : la partie servie d'une barre en débord.
    Vérification indépendante du 15/09 : métal trop lisse = reflet du studio sombre (dessus des tubes carrés inox à
    61/255, tôle à froid en miroir noir), invisible aux autres contrôles. Audit du 23/09 : la partie de la barre
    cachée sous la fiche incrustée faussait la mesure des plats (contrôles V3 et V4, tests/test_rendus_3d.py)."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    s = seuil_opaque(rgba.split()[3])
    if x_max is not None:
        rgba = rgba.crop((0, 0, int(x_max * rgba.width), rgba.height))
    boite = rgba.split()[3].point(lambda v: 255 if v >= s else 0).getbbox()
    if not boite:
        return None, None  # mesure impossible (plus de « 0 » pris pour une luminance)
    if moitie_arriere:
        boite = ((boite[0] + boite[2]) // 2, boite[1], boite[2], boite[3])
    zone = rgba.crop(boite)
    masque = zone.split()[3].point(lambda v: 255 if v >= s else 0)
    gris = zone.convert("L")
    n = ImageStat.Stat(masque).sum[0] / 255
    if not n:
        return None, None
    sombres = ImageStat.Stat(ImageChops.multiply(gris.point(lambda v: 255 if v < seuil_sombre else 0), masque)).sum[0] / 255
    return ImageStat.Stat(gris, mask=masque).mean[0], sombres / n


def contraste_coupe(chemin, ag, ad):
    """(médiane de la face sciée, médiane de la face longue voisine) sur la rangée de la pince du rendu brut : face sciée
    entre les points de pince `ag` et `ad`, face longue de 6 à 30 px à droite de `ad`. (None, None) si une zone est vide.
    Plat inox 20x3, 23/09 : coupe claire à 179 contre 183, section illisible en vignette (contrôle V9)."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    gris, alpha = rgba.convert("L").load(), rgba.split()[3].load()
    y0 = int(round(ag[1]))
    coupe, longue = [], []
    for y in range(max(0, y0 - 6), min(rgba.height, y0 + 7)):
        for x in range(max(0, int(ag[0]) + 2), min(rgba.width, int(ad[0]) - 1)):
            if alpha[x, y] >= 250:
                coupe.append(gris[x, y])
        for x in range(max(0, int(ad[0]) + 6), min(rgba.width, int(ad[0]) + 30)):
            if alpha[x, y] >= 250:
                longue.append(gris[x, y])
    if not coupe or not longue:
        return None, None
    return statistics.median(coupe), statistics.median(longue)


def contraste_paroi_opposee(chemin, ag, ad):
    """Tube carré ou rectangulaire : (médiane de la paroi opposée sur la face sciée, médiane du flanc voisin) sur la
    rangée de la pince. La paroi pincée (`ag` → `ad`) donne sur la cavité : la paroi opposée commence au premier pixel
    clair (> 90) après la cavité et a la même épaisseur. Tubes inox, 23/09 : paroi à 176 contre 183 (contrôle V10)."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    gris, alpha = rgba.convert("L").load(), rgba.split()[3].load()
    y0 = int(round(ad[1]))
    x, fin = int(ad[0]) + 2, min(rgba.width - 1, int(ad[0]) + 900)
    while x < fin and (alpha[x, y0] < 250 or gris[x, y0] <= 90):
        x += 1
    if x >= fin:
        return None, None
    e = max(4, int(ad[0] - ag[0]))
    paroi, flanc = [], []
    for y in range(max(0, y0 - 6), min(rgba.height, y0 + 7)):
        for xx in range(x + 2, min(rgba.width, x + e - 1)):
            if alpha[xx, y] >= 250:
                paroi.append(gris[xx, y])
        for xx in range(x + e + 6, min(rgba.width, x + e + 30)):
            if alpha[xx, y] >= 250:
                flanc.append(gris[xx, y])
    if not paroi or not flanc:
        return None, None
    return statistics.median(paroi), statistics.median(flanc)


def contraste_aile_basse(chemin, ext, int_):
    """Profil U : (médiane de la coupe de l'aile basse, médiane du fond du U vu au-dessus d'elle), sur les colonnes des
    points de l'aile haute (`ext` → `int_`, même épaisseur que l'aile basse). L'aile basse est la bande du bas de la pièce
    sur ces colonnes ; le fond est mesuré de 6 à 30 px au-dessus. (None, None) si une zone est vide.
    U alu, 24/09 : aile basse à 149–155 contre 156–157 pour le fond, épaisseur illisible ; V9 ne mesure que l'âme (V12)."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    gris, alpha = rgba.convert("L").load(), rgba.split()[3].load()
    x0, e = int(round(ext[0])), max(4, int(round(int_[1] - ext[1])))
    coupe, fond = [], []
    for x in range(max(0, x0 - 6), min(rgba.width, x0 + 7)):
        bas = next((y for y in range(rgba.height - 1, int(int_[1]), -1) if alpha[x, y] >= 250), None)
        if bas is None:
            continue
        for y in range(max(0, bas - e + 2), bas - 1):
            if alpha[x, y] >= 250:
                coupe.append(gris[x, y])
        for y in range(max(0, bas - e - 30), max(0, bas - e - 6)):
            if alpha[x, y] >= 250:
                fond.append(gris[x, y])
    if not coupe or not fond:
        return None, None
    return statistics.median(coupe), statistics.median(fond)


def noir_pur_servi(chemin, x_max=None):
    """Pixels de pièce en noir pur (RVB ≤ 12) dans la partie servie du rendu brut (à gauche de 0,615 W). Ronds à béton,
    24/09 : bouchons de nervures dans le plan de la coupe, 297 px sur le 12 mm (1 avant l'audit), invisibles au contrôle
    « part de noir pur » qui ne s'alerte qu'au-delà de 2 % de la pièce (contrôle V11)."""
    x_max = recadrer_visuels.CADRE[2] if x_max is None else x_max
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    r, g, b, a = rgba.crop((0, 0, int(x_max * rgba.width), rgba.height)).split()
    noir = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: 255 if v <= 12 else 0)
    opaque = a.point(lambda v: 255 if v >= 250 else 0)
    return round(ImageStat.Stat(ImageChops.multiply(noir, opaque)).sum[0] / 255)


def lisere_bord(brut, servie, minimum=20):
    """Écart médian, en niveaux de gris, entre l'image servie et le rendu brut posé normalement sur le blanc, sur le bord
    de la pièce : pixels qu'elle ne couvre qu'en partie (0 < alpha < 250, voisins d'un pixel opaque) et qui ont la
    couleur de la pièce voisine (bord posé sur le fond, sans part d'ombre ; l'ombre, noire, est allégée à dessein).
    Large plat, 24/09 : l'habillage traitait ce bord en ombre, 64 niveaux trop clair, en escalier (contrôle V15).
    None si l'image servie n'a pas la taille du rendu ou si moins de `minimum` pixels de bord se mesurent."""
    with Image.open(brut) as img:
        rgba = img.convert("RGBA")
    with Image.open(servie) as img:
        vue = img.convert("L")
    if vue.size != rgba.size:
        return None
    lum, alpha = rgba.convert("RGB").convert("L"), rgba.getchannel("A")
    opaque = alpha.point(lambda v: 255 if v >= 250 else 0)
    bord = ImageChops.multiply(opaque.filter(ImageFilter.MaxFilter(3)), alpha.point(lambda v: 255 if 0 < v < 250 else 0))
    boite = bord.getbbox()
    if not boite:
        return None
    L, O, A, V = lum.load(), opaque.load(), alpha.load(), vue.load()
    w, h = rgba.size
    x0, y0, x1, _ = boite
    ecarts = []
    for i, dedans in enumerate(bord.crop(boite).tobytes()):  # octets du masque L : 0 ou 255
        if not dedans:
            continue
        x, y = x0 + i % (x1 - x0), y0 + i // (x1 - x0)
        voisins = [L[u, v] for u in range(max(0, x - 1), min(w, x + 2)) for v in range(max(0, y - 1), min(h, y + 2)) if O[u, v]]
        if not voisins or L[x, y] < 0.9 * sum(voisins) / len(voisins):
            continue  # bord posé sur l'ombre : sa part d'ombre est allégée, l'écart est voulu
        normale = L[x, y] * A[x, y] / 255 + 255 * (1 - A[x, y] / 255)
        ecarts.append(V[x, y] - normale)
    return statistics.median(ecarts) if len(ecarts) >= minimum else None


def teinte_piece(chemin):
    """Couleur moyenne normalisée (r, g, b) / (r + g + b) de la pièce : distingue une Corten d'une galvanisée ou deux RAL
    dans une même famille, pour comparer la photo studio aux seules fiches de sa teinte (15/09)."""
    with Image.open(chemin) as img:
        rgba = img.convert("RGBA")
    a = rgba.split()[3]
    s = seuil_opaque(a)
    masque = a.point(lambda v: 255 if v >= s else 0)
    if not masque.getbbox():
        return None
    r, g, b = ImageStat.Stat(rgba.convert("RGB"), mask=masque).mean
    somme = (r + g + b) or 1
    return (r / somme, g / somme, b / somme)


def jours_rappel(chemin, points, echelle=1.0):
    """Écart en pixels entre le début de chaque ligne de rappel et le pixel de pièce le plus proche (transparence du
    rendu brut). Vérification indépendante des cornières : rappels à 67 px de la pièce sur les images rendues avant
    le correctif du jour. Distance au plus proche plutôt que le long du trait : sur les petites sections, le talon
    chanfreiné passe à côté du prolongement du trait. -> {clé: (jour ou None au-delà de la fenêtre, longueur)}"""
    with Image.open(chemin) as img:
        alpha = img.convert("RGBA").split()[3]
    jours = {}
    for cle, debut in points.items():
        fin = points.get(cle[:-len("_debut")] + "_fin") if cle.startswith("rappel_") and cle.endswith("_debut") else None
        if not fin:
            continue
        longueur = ((debut[0] - fin[0]) ** 2 + (debut[1] - fin[1]) ** 2) ** 0.5
        if longueur < 1:
            continue
        rayon = int(max(40 * echelle, min(3 * longueur, 200 * echelle)))  # 1,5 en 2400 px
        x0, y0 = int(debut[0]) - rayon, int(debut[1]) - rayon
        cote = 2 * rayon + 1
        fenetre = alpha.crop((x0, y0, x0 + cote, y0 + cote)).tobytes()  # hors image : transparent
        meilleur = None
        for i, v in enumerate(fenetre):
            if v >= 250:
                yy, xx = divmod(i, cote)
                d2 = (x0 + xx - debut[0]) ** 2 + (y0 + yy - debut[1]) ** 2
                if meilleur is None or d2 < meilleur:
                    meilleur = d2
        jour = round(meilleur ** 0.5) if meilleur is not None and meilleur <= rayon * rayon else None
        jours[cle] = (jour, longueur)
    return jours


def fond_enclos(chemin):
    """Part du fond enfermé par la pièce (zones transparentes non reliées au bord), rapportée à la pièce : fond visible à
    travers un tube trop court (tube carré 250x250x6, 4,3 %, vérification indépendante du 15/09). Calcul sur l'image
    réduite de moitié."""
    with Image.open(chemin) as img:
        alpha = img.convert("RGBA").split()[3]
    petite = alpha.resize((alpha.width // 2, alpha.height // 2), Image.NEAREST).point(lambda v: 255 if v >= 250 else 0)
    piece = sum(1 for v in petite.tobytes() if v)
    if not piece:
        return 0.0
    remplie = petite.convert("L")
    w, h = remplie.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if remplie.getpixel((x, y)) == 0:
            ImageDraw.floodfill(remplie, (x, y), 128)
    enclos = sum(1 for v in remplie.tobytes() if v == 0)
    return enclos / piece


# types dont la silhouette ne doit enfermer aucun fond (grilles, perforations, caillebotis : trous voulus)
SANS_FOND_ENCLOS = {"I", "U", "L", "T", "PLAT", "ROND", "CARRE", "TC", "TR", "TUBE-ROND", "ROND-BETON", "UPN", "IPE", "HEA", "HEB",
                    "U-ALU"}
# familles rendues avant l'empreinte du code (14/09 soir), vérifiées à l'œil par la vérification indépendante
FINITIONS_CLAIRES = {"INOX", "ALU"}  # contrôle des faces assombries par le reflet du studio
EMPREINTE_ABSENTE_VERIFIEE = {"poutrelle-ipe", "poutrelle-hea", "poutrelle-heb", "poutrelle-upn",
                              "fer-t", "plat", "large-plat", "rond-plein", "carre-plein"}


def marges_blanches(chemin, bande=16):
    with Image.open(chemin) as img:
        rgb = img.convert("RGB")
    w, h = rgb.size
    zones = [(0, 0, w, bande), (0, h - bande, w, h), (0, 0, bande, h), (w - bande, 0, w, h)]
    total = 0
    for z in zones:
        r, g, b = rgb.crop(z).split()
        total += sum(1 for v in ImageChops.darker(ImageChops.darker(r, g), b).tobytes() if v < 255)
    return total


def planches(famille, images):
    CONTROLE.mkdir(parents=True, exist_ok=True)
    for vieille in CONTROLE.glob(f"{famille}-planche-*.jpg"):
        vieille.unlink()
    tw, th, legende = 520, 390, 26
    police = ImageFont.load_default(size=16)
    for n in range(0, len(images), 12):
        lot = images[n:n + 12]
        lignes = (len(lot) + 2) // 3
        planche = Image.new("RGB", (3 * tw, lignes * (th + legende)), "white")
        d = ImageDraw.Draw(planche)
        for i, chemin in enumerate(lot):
            x, y = (i % 3) * tw, (i // 3) * (th + legende)
            with Image.open(chemin) as img:
                planche.paste(img.convert("RGB").resize((tw - 8, th - 6), Image.LANCZOS), (x + 4, y + 3))
            d.text((x + 6, y + th + 3), chemin.stem, fill=(60, 60, 60), font=police)
        planche.save(CONTROLE / f"{famille}-planche-{n // 12 + 1:02d}.jpg", quality=88)
    return sorted(CONTROLE.glob(f"{famille}-planche-*.jpg"))


def controler(famille, produits, pages):
    ecarts = []
    slugs = sorted(s for s, p in produits.items() if p["famille"] == famille)
    if not slugs:
        return [f"{famille} : aucune fiche dans produits.json"], []

    def fichier(nom):
        chemin = FINAL / nom
        if not chemin.exists():
            ecarts.append(f"{nom} : manquant")
            return None
        return chemin

    def image_finale(nom):
        png, webp = fichier(nom + ".png"), fichier(nom + ".webp")
        if png:
            with Image.open(png) as img:
                if img.size not in TAILLES:
                    ecarts.append(f"{png.name} : {img.size[0]} x {img.size[1]} au lieu de 1600 x 1200 ou 2400 x 1800")
        if webp and webp.stat().st_size > WEBP_MAX_KO * 1024:
            ecarts.append(f"{webp.name} : {webp.stat().st_size // 1024} Ko (> {WEBP_MAX_KO} Ko)")
        return png

    # photo studio de la categorie
    studio = f"studio-{famille}"
    images = []
    brut = fichier(studio + ".png")
    png = image_finale(studio + "-studio")
    if brut:
        cadre = cadre_piece(brut)
        if cadre is None:
            ecarts.append(f"{brut.name} : aucun pixel de piece")
        else:
            x0, y0, x1, y1 = cadre
            with Image.open(brut) as img:
                w_, h_ = img.size
            if x0 < w_ * 0.02 or y0 < h_ * 0.02 or x1 > w_ * 0.98 or y1 > h_ * 0.98:
                ecarts.append(f"{brut.name} : piece trop pres du bord ({x0}, {y0}, {x1}, {y1})")
        # longueur de chaque pièce dans le .json du studio (vérifications indépendantes des 16/09 et 23/09 : sans elle,
        # la longueur commune des barres ne se contrôlait qu'en ajustant une caméra sur l'image ; contrôle V5)
        compo = FINAL / f"{studio}.json"
        pieces_studio = json.loads(compo.read_text(encoding="utf-8")).get("pieces", []) if compo.exists() else []
        if not pieces_studio or any(not q.get("longueur") for q in pieces_studio):
            ecarts.append(f"{studio}.json : longueur des pieces absente (recalculer : preparer_rendus.py --points-seuls)")
    if png:
        images.append(png)
        with Image.open(png) as img:
            n = marges_blanches(png, bande=round(16 * img.width / LARGEUR_REFERENCE))
        if n:
            ecarts.append(f"{png.name} : {n} pixels non blancs dans les marges")
    # bord de la pièce net sur l'image servie : pas de liseré clair en escalier (large plat, 24/09 ; V15)
    servie = FINAL / f"{studio}-studio.webp"
    if brut and servie.exists():
        lisere = lisere_bord(brut, servie)
        if lisere is not None and lisere > 20:
            ecarts.append(f"{servie.name} : bord de la piece eclairci de {lisere:.0f} niveaux (lisere ; rhabiller)")
    lum_studio = luminance_piece(brut)[0] if brut else None
    # corps seul de la barre (sans la face coupée), pour les familles dont les fiches filent hors du cadre
    lum_studio_corps = luminance_piece(brut, moitie_arriere=True)[0] if brut else None
    teinte_studio = teinte_piece(brut) if brut else None
    lum_fiches = []  # (luminance, teinte normalisée) des fiches
    debords = []  # fiches en débord (barre qui file hors du cadre, audit du 23/09)

    versions = set()  # empreintes du code de rendu (rendu_profil.py) des images de la famille
    for slug in slugs:
        p, nom = produits[slug], slug + "-caracteristiques"
        brut = fichier(slug + ".png")
        png = image_finale(nom)
        if png:
            images.append(png)
        if brut:
            with Image.open(brut) as img:
                W_IMG, H_IMG = img.size  # 1600 ou 2400 px (ADR-0012)
            K = W_IMG / LARGEUR_REFERENCE  # seuils en pixels réglés en 1600 px
            cadre = cadre_piece(brut)
            if cadre is None:
                ecarts.append(f"{slug} : aucun pixel de piece dans le rendu brut")
                cadre = (0, 0, W_IMG, H_IMG)
            x0, y0, x1, y1 = cadre
            geo = FINAL / f"{slug}.json"
            debord = geo.exists() and json.loads(geo.read_text(encoding="utf-8")).get("debord", False)
            if debord:
                # barre qui file hors du cadre (audit du 23/09) : elle sort par le haut et sous la fiche par
                # construction ; habiller.py l'efface avant la fiche (contrôle « fond de la fiche »). Restent
                # contrôlés les bords où se tient la section : gauche et bas.
                if x0 < W_IMG * 0.02 or y1 > H_IMG * 0.98:
                    ecarts.append(f"{slug} : section trop pres du bord ({x0}, {y0}, {x1}, {y1})")
            else:
                if x0 < W_IMG * 0.02 or y0 < H_IMG * 0.02 or y1 > H_IMG * 0.98:
                    ecarts.append(f"{slug} : piece trop pres du bord ({x0}, {y0}, {x1}, {y1})")
                if x1 > W_IMG * (COLONNE_FICHE - 0.01):
                    ecarts.append(f"{slug} : la piece deborde sous la fiche technique (x = {x1})")
            # poteaux de clôture : tubes creux (CLOGRIFF) ou feuillures ombrées et capuchon noir (CLOPLUS), laque noire
            # (diagnostic du 15/09)
            creux = p["valeurs"].get("serie", {}).get("valeur") in ("TC", "TR", "TUBE-ROND", "POTEAU")
            noir = part_noire(brut, creux)
            if noir > (0.35 if creux else 0.02):
                ecarts.append(f"{slug} : {noir:.0%} de la piece en noir pur (geometrie cassee ?)")
            servie = FINAL / f"{nom}.webp"  # bord de la pièce net sur l'image servie (large plat, 24/09 ; V15)
            if servie.exists():
                lisere = lisere_bord(brut, servie)
                if lisere is not None and lisere > 20:
                    ecarts.append(f"{slug} : bord de la piece eclairci de {lisere:.0f} niveaux (lisere ; rhabiller)")
            # coupe lisible : face sciée à 8 niveaux au moins de la face longue voisine (plat inox, 23/09 ; V9). Plats,
            # cornières, profils T et U ; pas les tubes, dont la coupe se lit contre la cavité sombre
            points = json.loads(geo.read_text(encoding="utf-8")).get("points", {}) if geo.exists() else {}
            serie_coupe = p["valeurs"].get("serie", {}).get("valeur")
            # section pleine : aucun noir pur dans la partie servie (bouchons de nervures des ronds à béton, 24/09 ; V11)
            if serie_coupe in ("ROND", "ROND-BETON", "CARRE", "PLAT", "L", "T", "U-ALU"):
                noirs = noir_pur_servi(brut)
                if noirs > 20 * K * K:  # 20 px en 1600 px, 45 en 2400
                    ecarts.append(f"{slug} : {noirs} px de noir pur sur la piece servie (surfaces dans le meme plan ?)")
            if (serie_coupe in ("PLAT", "L", "T", "U-ALU", "TUBE-ROND", "TC", "TR")
                    and "ame_gauche" in points and "ame_droite" in points):
                # tubes carrés et rectangulaires : la paroi pincée donne sur la cavité, on mesure la paroi d'en face
                # (V10) ; tube rond : la paroi pincée est à droite de l'anneau, le flanc la suit (V9)
                if serie_coupe in ("TC", "TR"):
                    coupe, face = contraste_paroi_opposee(brut, points["ame_gauche"], points["ame_droite"])
                else:
                    coupe, face = contraste_coupe(brut, points["ame_gauche"], points["ame_droite"])
                if coupe is None:
                    ecarts.append(f"{slug} : contraste de la coupe non mesurable")
                elif abs(face - coupe) < 8:
                    ecarts.append(f"{slug} : coupe a {abs(face - coupe):.0f} niveaux de la face longue (section peu lisible)")
            # profil U : l'aile basse se lit contre le fond du U vu au-dessus d'elle (U alu, 24/09 ; V12)
            if serie_coupe == "U-ALU" and "aile_haut_ext" in points and "aile_haut_int" in points:
                coupe, fond = contraste_aile_basse(brut, points["aile_haut_ext"], points["aile_haut_int"])
                if coupe is None:
                    ecarts.append(f"{slug} : contraste de l'aile basse non mesurable")
                elif abs(fond - coupe) < 8:
                    ecarts.append(f"{slug} : aile basse a {abs(fond - coupe):.0f} niveaux du fond du U (epaisseur illisible)")
            debords.append(debord)
            # barre en débord : seulement la partie que le site sert (à gauche du cadre de recadrer_visuels.py) ;
            # la partie cachée sous la fiche incrustée n'est vue par personne (plats, 23/09)
            servi = recadrer_visuels.CADRE[2] if debord else None
            lum = luminance_piece(brut, moitie_arriere=debord, x_max=servi)[0]
            if lum is not None:
                lum_fiches.append((lum, teinte_piece(brut)))
            if p["valeurs"].get("finition", {}).get("valeur") in FINITIONS_CLAIRES:
                _, sombre = luminance_piece(brut, moitie_arriere=True, x_max=servi)
                if sombre is not None and sombre > 0.10:  # calibré le 15/09 : 22 % et 13 % sur les tubes inox refusés, 8 % au plus ailleurs
                    ecarts.append(f"{slug} : {sombre:.0%} du corps de la piece sous 80/255 (reflet du studio sombre "
                                  f"sur une matiere claire)")
            geo = FINAL / (slug + ".json")
            sidecar = FINAL / (nom + ".controles.json")
            if geo.exists():
                infos = json.loads(geo.read_text(encoding="utf-8"))
                versions.add(infos.get("code"))
                # lignes réellement tracées par habiller.py (collées à la pièce, cotes absentes exclues) ; à défaut, les points
                traces = json.loads(sidecar.read_text(encoding="utf-8")).get("rappels") if sidecar.exists() else None
                if traces is not None:
                    points = {}
                    for i, (d_, f_) in enumerate(traces):
                        points[f"rappel_{i + 1}_debut"], points[f"rappel_{i + 1}_fin"] = d_, f_
                else:
                    points = infos["points"]
                with Image.open(brut) as img_brut:
                    alpha_brut = img_brut.convert("RGBA").split()[3]
                def opaque(pt_):
                    xi, yi = int(round(pt_[0])), int(round(pt_[1]))
                    return 0 <= xi < alpha_brut.width and 0 <= yi < alpha_brut.height and alpha_brut.getpixel((xi, yi)) >= 250

                for cle, pt_ in points.items():
                    fin_ = points.get(cle[:-len("_debut")] + "_fin") if cle.endswith("_debut") else None
                    # trait qui entre dans la pièce (début dessus, fin dehors) ; un trait entièrement posé sur le corps de
                    # la pièce (rappel de b au-dessus de l'aile du fer T) reste lisible grâce au halo (vérification du 15/09)
                    if fin_ and opaque(pt_) and not opaque(fin_):
                        ecarts.append(f"{slug} : {cle} commence sur la piece")
                serie_ = p["valeurs"].get("serie", {}).get("valeur")
                if serie_ in SANS_FOND_ENCLOS or infos.get("type") in SANS_FOND_ENCLOS:
                    part = fond_enclos(brut)
                    if part > 0.005:
                        ecarts.append(f"{slug} : fond visible a travers la piece ({part:.1%} de la piece)")
                for cle, (jour, longueur) in sorted(jours_rappel(brut, points, K).items()):
                    if jour is None:
                        ecarts.append(f"{slug} : {cle} loin de toute piece (fenetre de recherche depassee)")
                    # décollée : vide plus long que le trait, ou plus de 60 px et plus de 60 % du trait (15/09 : à « 25 px ou
                    # moitié du trait », 224 alertes sur des angles arrondis et chanfreinés corrects ; le mélange de
                    # versions du code, cause des rappels décollés des cornières, a son propre contrôle)
                    elif jour > longueur or (jour > 60 * K and jour > 0.6 * longueur):
                        ecarts.append(f"{slug} : {cle} decollee de la piece ({jour} px pour un trait de {longueur:.0f} px)")
        ctrl = fichier(nom + ".controles.json")
        if not ctrl:
            continue
        c = json.loads(ctrl.read_text(encoding="utf-8"))
        ecarts += [f"{slug} : {pb}" for pb in c["problemes"]]
        titre = titre_image(p["nom"])
        if c["titre"] != titre:
            ecarts.append(f"{slug} : titre « {c['titre']} » au lieu de « {titre} »")
        valeurs = p["valeurs"]
        fiche = {label: ecrit for label, _, _, ecrit in c["fiche"]}
        for label, lettre, cle, ecrit in c["fiche"]:
            d = valeurs.get(cle)
            if not d:
                ecarts.append(f"{slug} : « {label} {ecrit} » ecrit sans donnee sourcee")
            elif d.get("supposee"):
                ecarts.append(f"{slug} : « {label} » affiche une valeur supposee")
            elif cle == "finition":
                if ecrit != FINITIONS.get(d["valeur"], d["valeur"]):
                    ecarts.append(f"{slug} : finition « {ecrit} » ≠ donnee « {d['valeur']} »")
            elif isinstance(d["valeur"], list):  # longueurs standard (ADR-0012) : « 1 à 6 m »
                if ecrit != texte_longueurs(d["valeur"], d.get("unite", "m")):
                    ecarts.append(f"{slug} : « {label} {ecrit} » ≠ donnee {d['valeur']}")
            elif not meme_valeur(d["valeur"], ecrit):
                ecarts.append(f"{slug} : « {label} {ecrit} » ≠ donnee {d['valeur']}")
        # habillage antérieur aux contrôles d'étiquettes V6 (habiller.py) : ils n'ont jamais tourné sur cette image
        # (tubes rectangulaires alu et inox habillés le 15/09, étiquette t entre les rappels de b ; 23/09)
        if "boites" not in c:
            ecarts.append(f"{slug} : habillee avant les controles d'etiquettes V6 (rhabiller : habiller_famille.py)")
        for lettre, cle, ecrit, *centre in c["pastilles"]:
            d = valeurs.get(cle)
            if not d or d.get("supposee") or not meme_valeur(d["valeur"], ecrit):
                ecarts.append(f"{slug} : pastille {lettre} « {ecrit} » ≠ donnee {d and d['valeur']}")
            # étiquette t d'un tube posée sur une paroi claire de la pièce (tubes rectangulaires étroits, 15/09) ; sans
            # centre dans le sidecar, le contrôle ne peut pas s'appliquer : c'est un écart, pas un silence (tubes
            # rectangulaires habillés le 15/09 avant la règle, restés sans contrôle jusqu'au 23/09)
            if cle == "t" and not centre and valeurs.get("serie", {}).get("valeur") in ("TC", "TR"):
                ecarts.append(f"{slug} : centre de l'etiquette t absent du sidecar (rhabiller : habiller_famille.py)")
            place = c.get("place_t") or {}
            if cle == "t" and centre and place.get("type") == "flanc":
                # posée sur le flanc (habiller.place_t_tube) : sur la pièce par construction, claire ou sombre selon la
                # matière (aluminium, 23/09) ; elle doit laisser libre la paroi opposée, à 6 px au moins
                rang = [q[1] for q in c["pastilles"]].index("t")
                if c["boites"][rang][0] < place["x_paroi"] + 6 * c.get("echelle", 1):
                    ecarts.append(f"{slug} : etiquette t posee sur la paroi opposee du tube")
            elif cle == "t" and centre and brut and valeurs.get("serie", {}).get("valeur") in ("TC", "TR"):
                e_ = c.get("echelle", 1)  # boîte de l'étiquette t, en pixels du rendu
                part = part_claire(brut, centre[0] - 50 * e_, centre[1] - 20 * e_, centre[0] + 50 * e_, centre[1] + 20 * e_)
                if part > 0.02:
                    ecarts.append(f"{slug} : etiquette t sur une paroi de la piece ({part:.0%} de sa surface)")
        # l'image dit la meme chose que la page
        page = pages.get(slug)
        if page is None:
            ecarts.append(f"{slug} : fiche absente de lib/catalogue.ts")
            continue
        affiche = {cle for _, _, cle, _ in c["fiche"]} | {q[1] for q in c["pastilles"]}
        couvertes = set()
        serie = valeurs.get("serie", {}).get("valeur")
        for libelle, cles in {**PAGE, **PAGE_PAR_SERIE.get(serie, {})}.items():
            if libelle not in page:
                continue
            couvertes.update(cles)
            texte_sans_chiffre = (len(cles) == 1 and isinstance(valeurs.get(cles[0], {}).get("valeur"), str)
                                  and not re.search(r"\d", valeurs[cles[0]]["valeur"]))
            if cles in (["nuance"], ["norme"], ["surface"]) or texte_sans_chiffre:  # textes : égalité stricte
                if cles[0] not in affiche:
                    ecarts.append(f"{slug} : {libelle} « {page[libelle]} » sur la page, absente de l'image")
                elif valeurs[cles[0]]["valeur"] != page[libelle]:
                    ecarts.append(f"{slug} : {libelle} page « {page[libelle]} » ≠ image « {valeurs[cles[0]]['valeur']} »")
                continue
            nombres = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", str(page[libelle]))]
            attendus = []  # valeurs numériques, ou nombres contenus dans un texte (« 150 × 150 mm »)
            for k in cles:
                if k in valeurs:
                    val = valeurs[k]["valeur"]
                    attendus += ([float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", val)]
                                 if isinstance(val, str) else [val])
            if len(nombres) != len(attendus) or any(abs(n - a) > 1e-6 for n, a in zip(nombres, attendus)):
                ecarts.append(f"{slug} : {libelle} page « {page[libelle]} » ≠ image {attendus}")
        for cle in sorted(affiche & COTES_AFFICHABLES - couvertes):
            if cle in ("nuance", "norme") and str(valeurs[cle]["valeur"]) in page["_texte"]:
                continue  # écrite dans la description de la page
            ecarts.append(f"{slug} : « {cle} » sur l'image, absent de la page")
        if "Poids" in fiche and not meme_valeur(page.get("Poids"), fiche["Poids"]):
            ecarts.append(f"{slug} : poids page {page.get('Poids')} ≠ image {fiche['Poids']}")
        # longueurs de l'image = « Longueurs standard » de la page, toutes et seulement elles (ADR-0012)
        if "longueurs" in affiche and sorted(page.get("Longueurs") or []) != sorted(valeurs["longueurs"]["valeur"]):
            ecarts.append(f"{slug} : longueurs page {page.get('Longueurs')} ≠ image {valeurs['longueurs']['valeur']}")
        # poids écrit dans la description de la page (texte du site actuel) : la fiche prime (règle du propriétaire),
        # l'écart va en question en attente — note, pas écart bloquant
        m = re.search(r"[Pp]oids\s*:?\s*([\d]+(?:[.,]\d+)?)\s*kg", page.get("_texte", ""))
        if m and "Poids" in fiche and nombre(fiche["Poids"]) is not None and abs(nombre(m.group(1)) - nombre(fiche["Poids"])) > 0.005:
            print(f"   note : {slug} : poids de la description « {m.group(1)} kg » ≠ image {fiche['Poids']} (question en attente)")
        if "Finition" in fiche and fiche["Finition"] != FINITIONS.get(page.get("Finition"), page.get("Finition")):
            ecarts.append(f"{slug} : finition page {page.get('Finition')} ≠ image {fiche['Finition']}")
    if brut and lum_studio is None:
        ecarts.append(f"{famille} : luminance de la photo studio non mesurable")
    if lum_studio is not None and lum_fiches:
        # calibré le 15/09 sur 39 familles : ±26 au plus sur les familles validées, −60 à −68 sur les tôles galvanisées,
        # inox et à froid (métal lisse : la photo studio reflète le studio sombre). Comparée aux seules fiches de la
        # teinte de la photo (une seule finition ou couleur par studio : bordure Corten seule, panneaux d'un RAL).
        if teinte_studio and all(t for _, t in lum_fiches):
            def distance(t):
                return sum((u - v) ** 2 for u, v in zip(t, teinte_studio))
            proche = min(distance(t) for _, t in lum_fiches)
            retenues = [l for l, t in lum_fiches if distance(t) <= proche + 0.0004]
        else:
            retenues = [l for l, _ in lum_fiches]
        # Barres en débord (audit du 23/09) : corps de la barre seulement, des deux côtés, et sur la fiche sa partie
        # servie seulement (x_max plus haut). La silhouette entière dépend de la part de face coupée claire (carré
        # plein : −31) ; le corps mesuré jusqu'au bord de l'image, de la partie cachée de la barre (plats : −31, photo
        # studio inchangée, 60 → 59). Corps servi, avant → après l'audit : carré plein −13 → −15, plats −23 → −23.
        reference = lum_studio_corps if debords and all(debords) and lum_studio_corps is not None else lum_studio
        ecart_lum = reference - sum(retenues) / len(retenues)
        if abs(ecart_lum) > 30:
            ecarts.append(f"{famille} : photo studio {ecart_lum:+.0f} niveaux de luminance par rapport aux visuels "
                          f"caracteristiques (matiere qui change avec la vue)")
    if None in versions and famille not in EMPREINTE_ABSENTE_VERIFIEE:
        ecarts.append(f"{famille} : visuels sans empreinte du code de rendu (version inconnue) : refaire ou verifier a l'oeil")
    if len(versions) > 1:  # reprise partielle : refaire la famille, ou au moins recalculer ses points (--points-seuls)
        ecarts.append(f"{famille} : visuels issus de {len(versions)} versions du code de rendu ({', '.join(sorted(str(v) for v in versions))})")
    return ecarts, planches(famille, images) if images else []


def main():
    familles = sys.argv[1:]
    if not familles:
        raise SystemExit(__doc__)
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    pages = specs_page()
    total = 0
    for famille in familles:
        ecarts, fichiers = controler(famille, produits, pages)
        total += len(ecarts)
        n = sum(1 for p in produits.values() if p["famille"] == famille)
        print(f"== {famille} : {n} fiches + 1 photo studio | {len(ecarts)} ecart(s)")
        for e in ecarts:
            print("   -", e)
        for f in fichiers:
            print("   planche :", f)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
