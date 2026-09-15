"""
Rendu Blender de profilés acier à partir de leurs cotes.

Usage :
  blender -b --factory-startup -P rendu_profil.py -- params.json

params.json : un objet ou une LISTE d'objets (une seule instance Blender pour toute la liste) :
  {"slug": "...", "mode": "caracteristiques" | "studio", "sortie": "dossier",
   "pieces": [{"type": "I", "h": 200, "b": 100, "tw": 5.6, "tf": 8.5, "r": 12, "longueur": 700}],
   "finition": "GPP" | "BRUT", "samples": 64, "largeur": 1600, "hauteur": 1200}
  Type "U" : "r1", "r2", "pente" (%) à la place de "r". Mode caracteristiques : une seule pièce.
  Pour compatibilité, les cotes peuvent aussi être données à la racine (une pièce).

Produit <sortie>/<slug>.png (fond transparent + ombre) et, en mode caracteristiques, <slug>.json
(coordonnées écran des points utiles aux cotes, pour l'habillage 2D).
"""

import hashlib
import json
import math
import os
import random
import sys
import time

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

MM = 0.001
PARAMS = {}
# empreinte du code de rendu, écrite dans chaque <slug>.json : controler_rendus.py signale une famille dont les
# images viennent de deux versions (reprise partielle après un correctif, vérification des cornières du 14/09)
try:
    with open(__file__, "rb") as _f:
        EMPREINTE = hashlib.sha1(_f.read()).hexdigest()[:10]
except (NameError, OSError):
    EMPREINTE = None

# Teintes (sRGB 0-255) calées sur les vraies photos du site actuel ; converties en linéaire pour Cycles.
TEINTE_GPP = PARAMS.get("teinte_gpp", (122, 52, 40))


ECHELLE = {"taille_m": 0.5}  # plus grande dimension des pièces de l'image, en mètres (échelle du brossage)


def p_mat(cle, defaut):
    """Réglage matière surchargeable depuis params.json."""
    return PARAMS.get(cle, defaut)


def lire_params():
    argv = sys.argv
    chemin = argv[argv.index("--") + 1]
    with open(chemin, encoding="utf-8-sig") as f:  # tolère le BOM ajouté par PowerShell
        return json.load(f)


def lineaire(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


# ---------------------------------------------------------------- géométrie

def arc(cx, cz, r, a0, a1, n):
    """Points d'un arc (degrés), extrémités comprises."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return pts


def dedoublonner(p):
    propre = []
    for q in p:
        if not propre or (abs(q[0] - propre[-1][0]) > 1e-9 or abs(q[1] - propre[-1][1]) > 1e-9):
            propre.append(q)
    return propre


def section_i(h, b, tw, tf, r, n=10):
    """Section en I (IPE, HEA, HEB) : ailes parallèles, 4 congés de raccordement, centrée en x."""
    x = tw / 2
    p = [(-b / 2, 0), (b / 2, 0), (b / 2, tf)]
    p += arc(x + r, tf + r, r, 270, 180, n)
    p += arc(x + r, h - tf - r, r, 180, 90, n)
    p += [(b / 2, h - tf), (b / 2, h), (-b / 2, h), (-b / 2, h - tf)]
    p += arc(-x - r, h - tf - r, r, 90, 0, n)
    p += arc(-x - r, tf + r, r, 0, -90, n)
    p += [(-b / 2, tf)]
    return dedoublonner(p)


def coin_arrondi(p0, p1, p2, r, n=10):
    """Remplace le sommet p1 par un arc de rayon r tangent aux segments p1-p0 et p1-p2."""
    if r <= 0:
        return [p1]
    v1 = Vector((p0[0] - p1[0], p0[1] - p1[1])).normalized()
    v2 = Vector((p2[0] - p1[0], p2[1] - p1[1])).normalized()
    ang = math.acos(max(-1.0, min(1.0, v1.dot(v2))))
    if ang < 1e-3 or abs(ang - math.pi) < 1e-3:
        return [p1]
    d = r / math.tan(ang / 2)
    t1 = Vector(p1) + v1 * d
    t2 = Vector(p1) + v2 * d
    c = Vector(p1) + (v1 + v2).normalized() * (r / math.sin(ang / 2))
    a1 = math.atan2(t1.y - c.y, t1.x - c.x)
    a2 = math.atan2(t2.y - c.y, t2.x - c.x)
    da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    return [(c.x + r * math.cos(a1 + da * i / n), c.y + r * math.sin(a1 + da * i / n)) for i in range(n + 1)]


def contour_arrondi(coins, rayons, n=10):
    """Contour fermé aux sommets arrondis. Chaque arrondi est borné à la place disponible sur ses deux côtés
    (98 % du côté si le sommet voisin est vif, 49 % s'il est arrondi aussi) : sans cela, un arrondi égal à
    l'épaisseur (cornière 40x40x3, r2 = 3 mm) mangeait toute la face et cassait la géométrie."""
    p = []
    k = len(coins)
    for i, c in enumerate(coins):
        prec, suiv = coins[i - 1], coins[(i + 1) % k]
        r = rayons[i]
        if r > 0:
            v1 = Vector((prec[0] - c[0], prec[1] - c[1]))
            v2 = Vector((suiv[0] - c[0], suiv[1] - c[1]))
            ang = math.acos(max(-1.0, min(1.0, v1.normalized().dot(v2.normalized()))))
            part_prec = 0.49 if rayons[i - 1] > 0 else 0.98
            part_suiv = 0.49 if rayons[(i + 1) % k] > 0 else 0.98
            d_max = min(v1.length * part_prec, v2.length * part_suiv)
            if 1e-3 < ang < math.pi - 1e-3:
                r = min(r, d_max * math.tan(ang / 2))
        p += coin_arrondi(prec, c, suiv, r, n)
    return p


def section_u(h, b, tw, tf, r1, r2, pente=8.0, n=10):
    """Section en U à ailes inclinées (UPN, DIN 1026-1) : épaisseur d'aile tf mesurée à b/2,
    faces intérieures inclinées de `pente` %, congé r1 à la racine, arrondi r2 au bout d'aile.
    Âme à gauche, ouverture vers +x ; centrée en x."""
    k = pente / 100.0
    t_bout = tf - (b / 2) * k          # épaisseur au bout de l'aile (x = b)
    t_racine = tf + (b / 2 - tw) * k   # épaisseur contre l'âme (x = tw)
    coins = [(0, 0), (b, 0), (b, t_bout), (tw, t_racine), (tw, h - t_racine), (b, h - t_bout), (b, h), (0, h)]
    rayons = [0, 0, r2, r1, r1, r2, 0, 0]
    return dedoublonner([(x - b / 2, z) for x, z in contour_arrondi(coins, rayons, n)])


def section_l(h, b, t, r1, r2, n=10):
    """Cornière (EN 10056) : aile verticale de hauteur h à gauche, aile horizontale de largeur b en bas,
    épaisseur t, congé r1 à la racine intérieure, arrondi r2 au bout intérieur de chaque aile ; talon vif. Centrée en x."""
    coins = [(0, 0), (b, 0), (b, t), (t, t), (t, h), (0, h)]
    rayons = [0, 0, r2, r1, r2, 0]
    return dedoublonner([(x - b / 2, z) for x, z in contour_arrondi(coins, rayons, n)])


def section_t(h, b, t, r, r1, r2, n=10):
    """Fer T (EN 10055) : aile en haut (largeur b), âme en bas, même épaisseur t ; congés r à la racine,
    arrondis r1 au bout des ailes et r2 au bout de l'âme ; faces parallèles. Centrée en x, bout de l'âme en z = 0."""
    coins = [(-t / 2, 0), (t / 2, 0), (t / 2, h - t), (b / 2, h - t), (b / 2, h), (-b / 2, h), (-b / 2, h - t), (-t / 2, h - t)]
    rayons = [r2, r2, r, r1, 0, 0, r1, r]
    return dedoublonner(contour_arrondi(coins, rayons, n))


def section_rectangle(h, b):
    """Plat posé sur chant (hauteur h = largeur du plat, épaisseur b) ou carré plein ; arêtes vives (chanfrein du modèle)."""
    return [(-b / 2, 0), (b / 2, 0), (b / 2, h), (-b / 2, h)]


# ---------------------------------------------------------------- tôles pliées et profilées

def section_pliee(ligne, e):
    """Contour fermé d'une tôle d'épaisseur e dont `ligne` est la fibre moyenne (polyligne ouverte (x, z), en mm) :
    décalage de ± e/2 de part et d'autre, angles en onglet (limités à 3 e sur les plis très fermés)."""
    n = len(ligne)
    normales = []
    for i in range(n - 1):
        dx, dz = ligne[i + 1][0] - ligne[i][0], ligne[i + 1][1] - ligne[i][1]
        long_ = math.hypot(dx, dz) or 1.0
        normales.append((-dz / long_, dx / long_))
    gauche, droite = [], []
    for i, (x, z) in enumerate(ligne):
        if i == 0:
            nx, nz = normales[0]
        elif i == n - 1:
            nx, nz = normales[-1]
        else:  # bissectrice des normales des deux segments, allongée pour garder l'épaisseur dans l'angle
            ax, az = normales[i - 1]
            bx, bz = normales[i]
            sx, sz = ax + bx, az + bz
            long_ = math.hypot(sx, sz)
            if long_ < 1e-9:
                nx, nz = ax, az
            else:
                cos_demi = max(0.33, (ax * sx + az * sz) / long_)  # limite d'onglet : 3 e
                nx, nz = sx / long_ / cos_demi, sz / long_ / cos_demi
        gauche.append((x + nx * e / 2, z + nz * e / 2))
        droite.append((x - nx * e / 2, z - nz * e / 2))
    return gauche + droite[::-1]


def profil_nervures(largeur, pas, h, sommet, base, centre0, x_fin=None):
    """Fibre moyenne (x de 0 à `largeur`, z = 0 en fond) d'une tôle à nervures trapézoïdales de hauteur h (sommet et
    base en mm) centrées en centre0 + k·pas ; une nervure qui dépasse un bord est coupée. `x_fin` : fin de la tôle."""
    x_fin = largeur if x_fin is None else x_fin
    pts = [(0.0, 0.0)]
    k = 0
    while True:
        c = centre0 + k * pas
        nervure = [(c - base / 2, 0.0), (c - sommet / 2, h), (c + sommet / 2, h), (c + base / 2, 0.0)]
        if nervure[0][0] >= x_fin:
            break
        for j, (x, z) in enumerate(nervure):
            if x <= 0:
                continue
            x_prec, z_prec = nervure[j - 1] if j else (x, z)
            if x_prec < 0 < x:  # nervure coupée au bord gauche : point interpolé sur le flanc, en x = 0
                pts[-1] = (0.0, z_prec + (z - z_prec) * (0 - x_prec) / (x - x_prec))
            if x >= x_fin:  # coupe au bord droit : point interpolé sur le flanc
                if pts[-1][0] < x_fin:
                    pts.append((x_fin, z_prec + (z - z_prec) * (x_fin - x_prec) / (x - x_prec)))
                break
            pts.append((x, z))
        k += 1
    if pts[-1][0] < x_fin:
        pts.append((x_fin, 0.0))
    nets = [pts[0]]  # dédoublonnage des points confondus
    for p_ in pts[1:]:
        if abs(p_[0] - nets[-1][0]) > 1e-6 or abs(p_[1] - nets[-1][1]) > 1e-6:
            nets.append(p_)
    return nets


def tole_pliee(nom, ligne, e, longueur, decalage_x=0.0, chanfrein=False):
    """Tôle pliée extrudée le long de y : la fibre moyenne `ligne` (x, z) est centrée en x sur `decalage_x`."""
    xs = [x for x, _ in ligne]
    milieu = (min(xs) + max(xs)) / 2
    contour = section_pliee([(x - milieu, z) for x, z in ligne], e)
    obj = extruder(contour, longueur, nom, decalage_x=decalage_x)
    if not chanfrein:  # chanfrein de 0,6 mm plus large qu'une tôle de 0,5 : retiré
        obj.modifiers.remove(obj.modifiers["chanfrein"])
    return obj


def ligne_bordure(h, pli, angle, e):
    """Bordure de jardin : face verticale de hauteur h, pli rentrant de `pli` mm à `angle` degrés en tête
    (photo du site : le pli part vers l'arrière et redescend). Fibre moyenne, x = 0 sur la face avant."""
    a = math.radians(angle)
    return [(0.0, 0.0), (0.0, h), (-pli * math.sin(a), h - pli * math.cos(a))]


def ligne_tasseau(largeur, h, sommet, pas, e):
    """Bardage « tasseau » : caissons de hauteur h (sommet `sommet`, flancs presque droits) à l'entraxe `pas`
    (dessin du fabricant : 39 de sommet, 90 d'axe en axe, soit 8 tasseaux sur 710) ; marges égales aux deux bords."""
    base = sommet + 6.0
    n = int((largeur - base) / pas) + 1
    marge = (largeur - (n - 1) * pas - base) / 2
    return profil_nervures(largeur, pas, h, sommet, base, marge + base / 2)


def plaque_pleine(nom, largeur, longueur, epaisseur, decalage_x=0.0, z0=0.0):
    obj = extruder([(-largeur / 2, z0), (largeur / 2, z0), (largeur / 2, z0 + epaisseur), (-largeur / 2, z0 + epaisseur)],
                   longueur, nom, decalage_x=decalage_x)
    obj.modifiers.remove(obj.modifiers["chanfrein"])
    return obj


def panneau_isole(piece, dx, nom):
    """Panneau sandwich Eurocopre Monolamiera : âme en mousse (largeur utile × épaisseur), feuille d'aluminium plate
    dessous, tôle d'acier prélaquée dessus à nervures trapézoïdales creuses (au pas de 333, une demi-nervure à chaque
    bord ; la nervure de droite déborde en lèvre de recouvrement jusqu'à la largeur hors tout). -> (objets, matières)"""
    r = piece["sandwich"]
    e, L, l, lu = piece["h"], piece["longueur"], piece["b"], r["l_utile"]
    x0 = dx - l / 2  # bord gauche de la tôle hors tout
    mousse = plaque_pleine(f"{nom}-mousse", lu, L, e - 0.5, decalage_x=x0 + lu / 2, z0=0.5)
    feuille = plaque_pleine(f"{nom}-feuille", lu, L, 0.5, decalage_x=x0 + lu / 2, z0=0.0)
    ligne = [(x, e + z) for x, z in profil_nervures(l, r["pas"], r["h_nervure"], r["sommet"], r["base"], 0.0, x_fin=l)]
    tole = tole_pliee(f"{nom}-tole", ligne, r["e_tole"], L, decalage_x=dx)
    return [(mousse, "MOUSSE"), (feuille, "ALU-FEUILLE"), (tole, None)]


def profil_de_tole(piece):
    """Fibre moyenne (x de 0 à la largeur) d'une tôle profilée ou d'un tasseau, d'après `piece['profil']`."""
    r = piece["profil"]
    if r["motif"] == "TASSEAU":
        return ligne_tasseau(piece["b"], r["h"], r["sommet"], r["pas"], piece["h"])
    return profil_nervures(piece["b"], r["pas"], r["h"], r["sommet"], r["base"], r["base"] / 2 + 5.0)


def cercle(r, cz, n=96):
    return [(r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rectangle_arrondi(h, b, r, n=10):
    """Contour d'un rectangle à coins arrondis, centré en x, base en z = 0 ; 4 × (n + 1) points."""
    r = max(0.0, min(r, h / 2, b / 2))
    p = []
    for cx, cz, a0 in ((b / 2 - r, r, 270), (b / 2 - r, h - r, 0), (-b / 2 + r, h - r, 90), (-b / 2 + r, r, 180)):
        p += arc(cx, cz, r, a0, a0 + 90, n)
    return p


def section_tube_rect(h, b, t, r_ext, n=10):
    """Tube carré ou rectangulaire (EN 10219) : rayon extérieur r_ext, intérieur r_ext − t. (extérieur, intérieur)."""
    ext = rectangle_arrondi(h, b, r_ext, n)
    inte = [(x, z + t) for x, z in rectangle_arrondi(h - 2 * t, b - 2 * t, max(r_ext - t, 0.2), n)]
    return ext, inte


def section_tube_rond(d, t, n=96):
    return cercle(d / 2, d / 2, n), cercle(d / 2 - t, d / 2, n)


def extruder(section_mm, longueur_mm, nom, decalage_x=0.0):
    """Section pleine (liste de points) ou creuse (tuple extérieur, intérieur de même nombre de points)."""
    me = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    if isinstance(section_mm, tuple):
        ext, inte = ([bm.verts.new(((x + decalage_x) * MM, 0.0, z * MM)) for x, z in boucle] for boucle in section_mm)
        faces = [bm.faces.new((ext[i], ext[(i + 1) % len(ext)], inte[(i + 1) % len(ext)], inte[i])) for i in range(len(ext))]
    else:
        faces = [bm.faces.new([bm.verts.new(((x + decalage_x) * MM, 0.0, z * MM)) for x, z in section_mm])]
    res = bmesh.ops.extrude_face_region(bm, geom=faces)
    nouveaux = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=nouveaux, vec=(0.0, longueur_mm * MM, 0.0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # faces lisses, arêtes vives au-delà de 30° : les congés restent ronds
    for f in bm.faces:
        f.smooth = True
        f.material_index = 1 if abs(f.normal.y) > 0.99 else 0  # 1 = faces de coupe
    for e in bm.edges:
        if len(e.link_faces) == 2:
            angle = e.link_faces[0].normal.angle(e.link_faces[1].normal)
            e.smooth = angle < math.radians(30)
        else:
            e.smooth = False

    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(nom, me)
    bpy.context.collection.objects.link(obj)

    bev = obj.modifiers.new("chanfrein", "BEVEL")
    bev.width = 0.6 * MM
    bev.segments = 3
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(30)
    return obj


def courbe_tube(nom, points, rayon, rayons_points=None, resolution=4):
    """Tube le long d'une polyligne (mm) : nervure de barre crénelée. `rayons_points` module l'épaisseur."""
    cu = bpy.data.curves.new(nom, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = rayon * MM
    cu.bevel_resolution = resolution
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for i, (x, y, z) in enumerate(points):
        sp.points[i].co = (x * MM, y * MM, z * MM, 1.0)
        if rayons_points:
            sp.points[i].radius = rayons_points[i]
    obj = bpy.data.objects.new(nom, cu)
    bpy.context.collection.objects.link(obj)
    return obj


def nervures_barre(d, L, dx, nom):
    """Barre crénelée (aciers pour béton) : deux nervures longitudinales et deux rangées de nervures transverses en
    croissant, inclinées en sens opposés. Proportions usuelles (hauteur ≈ 0,065 d, pas ≈ 0,7 d, 55°) : forme seulement."""
    R, cz = d / 2, d / 2
    h_n = 0.065 * d
    objs = [courbe_tube(f"{nom}-long-{s}", [(dx + s * R, 0, cz), (dx + s * R, L, cz)], h_n * 0.8) for s in (-1, 1)]
    pas, k = 0.7 * d, 1 / math.tan(math.radians(55))
    n = 14
    for rangee, (t0, t1, sens) in enumerate(((12, 168, 1), (192, 348, -1))):
        y0 = pas / 2 + rangee * pas / 2
        while y0 + R * k < L - pas / 2:
            ts = [math.radians(t0 + (t1 - t0) * i / (n - 1)) for i in range(n)]
            pts = [(dx + R * math.cos(t), y0 + sens * R * math.sin(t) * k, cz + R * math.sin(t)) for t in ts]
            rayons = [0.25 + 0.75 * math.sin(math.pi * i / (n - 1)) for i in range(n)]  # croissant : fin aux bouts
            objs.append(courbe_tube(f"{nom}-n{rangee}-{y0:.0f}", pts, h_n, rayons))
            y0 += pas
    return objs


def fils_treillis(piece, dx, nom):
    """Portion de treillis soudé : fils longitudinaux (le long de y) posés au sol, fils transversaux soudés dessus.
    Débord d'une demi-maille autour des fils extérieurs. Fils lisses (crénelure invisible à cette échelle).
    Treillis à dépassants : fils longitudinaux prolongés d'une maille au-delà du dernier fil transversal (au fond)
    et fils transversaux d'une maille au-delà du dernier fil longitudinal (à droite) ; la longueur réelle des
    dépassants n'est pas publiée (question 32) : forme du rendu seulement, aucune cote."""
    d, ma, mb, nx, ny = piece["t"], piece["maille_a"], piece["maille_b"], piece["nx"], piece["ny"]
    dep_y, dep_x = (ma, mb) if piece.get("depassants") else (0, 0)
    Ly, Lx = ny * ma + dep_y, nx * mb
    objs = []
    for i in range(nx):
        x = dx + (i - (nx - 1) / 2) * mb
        objs.append(extruder([(xx + x, zz) for xx, zz in cercle(d / 2, d / 2, 24)], Ly, f"{nom}-long-{i}"))
    for j in range(ny):
        y = ma / 2 + j * ma
        obj = extruder(cercle(d / 2, 0, 24), Lx + dep_x, f"{nom}-trans-{j}")
        # extrudé le long de y puis tourné de 90° autour de z : fil le long de x, centré, posé sur les fils longitudinaux
        obj.rotation_euler = (0, 0, math.radians(-90))
        obj.location = ((dx - Lx / 2) * MM, y * MM, 1.45 * d * MM)
        objs.append(obj)
    return objs


# ---------------------------------------------------------------- tôles à relief (larmées, striées)

# formes du relief (mm) : larme EN 10363 type T ≈ 30 × 10 mm (catalogue ArcelorMittal A90), pas mesuré sur la vraie
# photo du site (groupe G038) ; quintette alu : 5 barrettes, proportions mesurées sur la photo du site (groupe G060).
# Forme du rendu seulement : aucune de ces cotes n'est affichée.
# `decalage_e` : distance entre le relief coupé par le chant et la pince de l'épaisseur de base, prise sur la tôle nue
# (larme : hors de sa coupe de 14 mm ; quintette : milieu du plat entre la barrette centrale et sa voisine)
MOTIFS_RELIEF = {
    "LARMES": {"longueur": 30.0, "largeur": 10.0, "barrettes": 1, "ecart": 0.0, "pas": 35.0, "grille_45": False,
               "decalage_e": 12.0},
    "QUINTETTE": {"longueur": 40.0, "largeur": 3.5, "barrettes": 5, "ecart": 7.5, "pas": 44.0, "grille_45": True,
                  "decalage_e": 5.3},
}


def champ_loupe(piece):
    """Largeur du champ de la loupe (mm) : 10 épaisseurs, 30 mm au moins ; tôle à relief : 6 épaisseurs au sommet du
    relief (essai du 14/09 : à 10, les pinces de 3 et 5 mm se distinguaient mal)."""
    relief = piece.get("relief")
    return max(6 * relief["e_total"], 30.0) if relief else max(10 * piece["h"], 30.0)


def x_relief_coupe(piece):
    """Abscisse (pièce centrée) du relief coupé par le chant avant, à droite de la pince de l'épaisseur de base."""
    return -piece["b"] * 0.3 + MOTIFS_RELIEF[piece["relief"]["motif"]]["decalage_e"]


def lentille(longueur, largeur, hauteur, dy=0.0, nu=16, nv=6):
    """Élément de relief le long de x, centré en (0, dy), base à z = 0 : contour en fuseau, dos bombé à flancs raides,
    fond plat. -> (sommets, faces) en mm ; les pointes (sommets confondus) sont fusionnées à la création du maillage."""
    verts, faces = [], []
    for i in range(nu + 1):
        u = -1 + 2 * i / nu
        demi = largeur / 2 * (1 - u * u)
        for j in range(nv + 1):
            v = -1 + 2 * j / nv
            verts.append((u * longueur / 2, dy + v * demi, hauteur * (1 - v ** 4) * (1 - u * u) ** 0.35))

    def k(i, j):
        return i * (nv + 1) + j

    faces = [(k(i, j), k(i + 1, j), k(i + 1, j + 1), k(i, j + 1)) for i in range(nu) for j in range(nv)]
    faces.append(tuple(k(i, 0) for i in range(nu, -1, -1)) + tuple(k(i, nv) for i in range(1, nu)))  # fond
    return verts, faces


def element_relief(motif, hauteur):
    """Larme seule ou groupe de barrettes parallèles (quintette), le long de x, centré à l'origine."""
    m = MOTIFS_RELIEF[motif]
    verts, faces = [], []
    for n in range(m["barrettes"]):
        v, f = lentille(m["longueur"], m["largeur"], hauteur, dy=(n - (m["barrettes"] - 1) / 2) * m["ecart"])
        faces += [tuple(i + len(verts) for i in face) for face in f]
        verts += v
    return verts, faces


def maillage(nom, verts, faces, rotation_z=0.0, position=(0.0, 0.0, 0.0), aretes_vives=False):
    """Objet maillé à partir de sommets en mm, tourné autour de z (degrés) puis placé ; pointes fusionnées, normales
    vers l'extérieur, lissé (`aretes_vives` : arêtes de plus de 30° gardées vives, pour les dalles percées)."""
    c, s = math.cos(math.radians(rotation_z)), math.sin(math.radians(rotation_z))
    me = bpy.data.meshes.new(nom)
    me.from_pydata([((x * c - y * s + position[0]) * MM, (x * s + y * c + position[1]) * MM, (z + position[2]) * MM)
                    for x, y, z in verts], [], faces)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if aretes_vives:
        aretes_par_angle(bm)
    bm.to_mesh(me)
    bm.free()
    if not aretes_vives:
        for poly in me.polygons:
            poly.use_smooth = True
    obj = bpy.data.objects.new(nom, me)
    bpy.context.collection.objects.link(obj)
    return obj


def relief_tole(piece, dx, nom):
    """Relief d'une tôle larmée ou striée posé sur la face supérieure (z = épaisseur de base) : éléments en instances
    (deux orientations à ±45°, en damier), entièrement dans la plaque, plus un élément réel coupé par le chant avant
    à `x_relief_coupe` (épaisseur totale mesurée dans la loupe). -> objets à matérialiser."""
    r = piece["relief"]
    m = MOTIFS_RELIEF[r["motif"]]
    b, L, e, hauteur = piece["b"], piece["longueur"], piece["h"], r["hauteur"]
    z0 = e - 0.02  # base légèrement enfoncée dans la tôle : pas de jour sous le relief, sommet à e + hauteur
    verts, faces = element_relief(r["motif"], hauteur + 0.02)
    rayon = max(math.hypot(x, y) for x, y, _ in verts)
    objs = []
    # éléments en instances : un gabarit par orientation, enfant d'un nuage de points (instanciation par sommets)
    pas, marge = m["pas"], rayon + 2.0
    x_coupe = dx + x_relief_coupe(piece)
    centres = {45: [], -45: []}
    n = int(max(b, L) / pas) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            if m["grille_45"]:  # grille tournée de 45° : barrettes parallèles aux axes de la grille
                u, v = (i - j) * pas / math.sqrt(2), (i + j) * pas / math.sqrt(2)
            else:
                u, v = i * pas, j * pas
            x, y = dx + u, L / 2 + v
            if not (dx - b / 2 + marge <= x <= dx + b / 2 - marge and marge <= y <= L - marge):
                continue
            if math.hypot(x - x_coupe, y) < 2 * rayon + 2:
                continue  # place du relief coupé par le chant
            centres[45 if (i + j) % 2 == 0 else -45].append((x, y, z0))
    for angle, pts in centres.items():
        if not pts:
            continue
        gabarit = maillage(f"{nom}-relief{angle}", verts, faces, rotation_z=angle)
        me = bpy.data.meshes.new(f"{nom}-points{angle}")
        me.from_pydata([(x * MM, y * MM, z * MM) for x, y, z in pts], [], [])
        nuage = bpy.data.objects.new(f"{nom}-points{angle}", me)
        bpy.context.collection.objects.link(nuage)
        nuage.instance_type = "VERTS"
        nuage.show_instancer_for_render = False
        gabarit.parent = nuage
        objs.append(gabarit)
    # relief coupé par le chant avant (y = 0) : on garde y ≥ 0 et on ferme la face coupée (matière de coupe)
    coupe = maillage(f"{nom}-relief-coupe", verts, faces, rotation_z=45, position=(x_coupe, 0.0, z0))
    bm = bmesh.new()
    bm.from_mesh(coupe.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-7,
                                 plane_co=(0, 0, 0), plane_no=(0, -1, 0), clear_outer=True)
    bords = [g for g in res["geom_cut"] if isinstance(g, bmesh.types.BMEdge)]
    if bords:
        bmesh.ops.holes_fill(bm, edges=bords, sides=0)
    for f in bm.faces:
        if all(abs(v.co.y) < 1e-6 for v in f.verts):
            f.material_index = 1
            f.smooth = False
    bm.to_mesh(coupe.data)
    bm.free()
    objs.append(coupe)
    return objs


# ---------------------------------------------------------------- tôles perforées

def dalle_percee(contour, trous, e):
    """Dalle pleine d'épaisseur e (z de 0 à e) : contour (x, y) en mm moins des trous (contours fermés), dessus et
    dessous triangulés, parois extérieures et parois des trous. -> (sommets, faces) en mm."""
    from mathutils.geometry import tessellate_polygon
    boucles = [contour] + list(trous)
    plat = [pt for boucle in boucles for pt in boucle]
    n = len(plat)
    tris = tessellate_polygon([[Vector((x, y, 0.0)) for x, y in boucle] for boucle in boucles])
    verts = [(x, y, e) for x, y in plat] + [(x, y, 0.0) for x, y in plat]
    faces = [tuple(t) for t in tris] + [tuple(i + n for i in reversed(t)) for t in tris]
    debut = 0
    for boucle in boucles:
        m = len(boucle)
        faces += [(debut + k, debut + (k + 1) % m, debut + (k + 1) % m + n, debut + k + n) for k in range(m)]
        debut += m
    return verts, faces


def cercle_xy(cx, cy, d, n):
    return [(cx + d / 2 * math.cos(2 * math.pi * k / n), cy + d / 2 * math.sin(2 * math.pi * k / n)) for k in range(n)]


def tuile_aleatoire(S, graine=7):
    """Tuile carrée périodique de S mm à trous de diamètres variables placés au hasard (tirage fixe) : distances
    mesurées sur un tore, un trou qui dépasse un bord se prolonge par une encoche sur le bord opposé, les tuiles
    jointives ne montrent donc aucune couture (essai du 14/09 : tuile fermée de 250 mm vue en damier). Ligament
    1,5 mm, un peu plus d'un tiers de vide. Le site ne donne ni diamètres ni taux de vide : forme du rendu
    seulement, d'après la vraie photo (groupe G039). -> (contour à encoches, trous intérieurs, encoches du bord y = -S/2)"""
    rnd = random.Random(graine)
    diametres, ligament, case = (3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0), 1.5, 15.0
    n = int(S // case)
    trous, vide, grille = [], 0.0, {}

    def torique(u):
        return min(abs(u), S - abs(u))

    for _ in range(60000):
        if vide >= 0.36 * S * S:
            break
        d = rnd.choice(diametres)
        x, y = rnd.uniform(-S / 2, S / 2), rnd.uniform(-S / 2, S / 2)
        if abs(x) > S / 2 - d / 2 - ligament and abs(y) > S / 2 - d / 2 - ligament:
            continue  # pas de trou sur un coin de tuile
        cx, cy = int((x + S / 2) // case) % n, int((y + S / 2) // case) % n
        voisins = [t for i in (-1, 0, 1) for j in (-1, 0, 1) for t in grille.get(((cx + i) % n, (cy + j) % n), [])]
        if all(math.hypot(torique(x - a), torique(y - b_)) >= (d + dd) / 2 + ligament for a, b_, dd in voisins):
            trous.append((x, y, d))
            grille.setdefault((cx, cy), []).append((x, y, d))
            vide += math.pi * d * d / 4
    interieurs, cercles = [], []
    for x, y, d in trous:
        if abs(x) + d / 2 < S / 2 - 1e-3 and abs(y) + d / 2 < S / 2 - 1e-3:
            interieurs.append(cercle_xy(x, y, d, 12 if d <= 5 else 18))
        else:  # trou à cheval sur un bord : lui et ses images sur les bords opposés deviennent des encoches
            cercles += [(x + i * S, y + j * S, d) for i in (-1, 0, 1) for j in (-1, 0, 1)]
    h = S / 2
    # bords parcourus dans le sens trigonométrique : (départ, direction), coordonnée le long du bord
    bords = [((-h, -h), (1, 0)), ((h, -h), (0, 1)), ((h, h), (-1, 0)), ((-h, h), (0, -1))]
    contour, encoches_bas = [], []
    for (x0, y0), (ux, uy) in bords:
        entailles = []
        for cx, cy, d in cercles:
            r = d / 2
            dist = (cy - y0) if uy == 0 else (cx - x0)  # écart du centre à la droite du bord
            if abs(dist) >= r - 1e-6:
                continue
            demi = math.sqrt(r * r - dist * dist)
            s_c = (cx - x0) * ux + (cy - y0) * uy  # position du centre le long du bord
            if s_c - demi <= 1e-6 or s_c + demi >= S - 1e-6:
                continue
            entailles.append((s_c - demi, s_c + demi, cx, cy, r))
        contour.append((x0, y0))
        for s0, s1, cx, cy, r in sorted(entailles):
            p0, p1 = (x0 + ux * s0, y0 + uy * s0), (x0 + ux * s1, y0 + uy * s1)
            t0, t1 = math.atan2(p0[1] - cy, p0[0] - cx), math.atan2(p1[1] - cy, p1[0] - cx)
            if t1 >= t0:
                t1 -= 2 * math.pi  # arc parcouru dans le sens horaire : le trou reste à droite du contour
            pas_arc = max(3, int((t0 - t1) / (2 * math.pi) * 18))
            contour += [(cx + r * math.cos(t0 + (t1 - t0) * k / pas_arc), cy + r * math.sin(t0 + (t1 - t0) * k / pas_arc))
                        for k in range(pas_arc + 1)]
            if uy == 0 and ux == 1:
                encoches_bas.append((s0 - h, s1 - h))
    return contour, interieurs, encoches_bas


def aretes_par_angle(bm):
    """Faces lisses, arêtes vives au-delà de 30° (comme `extruder`) ; faces du chant avant et arrière en matière de coupe."""
    for f in bm.faces:
        f.smooth = True
    for ar in bm.edges:
        ar.smooth = len(ar.link_faces) == 2 and ar.link_faces[0].normal.angle(ar.link_faces[1].normal, 0.0) < math.radians(30)


def plaque_perforee(piece, dx, nom):
    """Tôle perforée : cellules percées répétées (hexagones à trou rond pour la quinconce R/T, carrés à trou carré en
    rangées droites C/U, tuiles aléatoires tournées), en instances à l'intérieur de la plaque ; cellules du bord coupées
    aux dimensions exactes et réunies dans un seul maillage. Première rangée à trous entiers : chant avant plein
    (épaisseur pincée dans la loupe). -> objets à matérialiser."""
    perfo, e, b, L = piece["perforation"], piece["h"], piece["b"], piece["longueur"]
    x_min, x_max = dx - b / 2, dx + b / 2
    if perfo["forme"] == "RONDE":
        T, d = perfo["pas"], perfo["cote"]
        R = T / math.sqrt(3)  # hexagone pointe en haut : voisins à T sur la rangée et à 60°
        contour = [(R * math.cos(math.radians(90 + 60 * k)), R * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
        trous = [cercle_xy(0.0, 0.0, d, 24)]
        demi_x, demi_y, pas_x, pas_y, decale_impair, variantes = T / 2, R, T, T * math.sqrt(3) / 2, T / 2, [0]
    elif perfo["forme"] == "CARREE":
        U, c = perfo["pas"], perfo["cote"]
        contour = [(-U / 2, -U / 2), (U / 2, -U / 2), (U / 2, U / 2), (-U / 2, U / 2)]
        trous = [[(-c / 2, -c / 2), (-c / 2, c / 2), (c / 2, c / 2), (c / 2, -c / 2)]]
        demi_x, demi_y, pas_x, pas_y, decale_impair, variantes = U / 2, U / 2, U, U, 0.0, [0]
    else:  # ALEATOIRE : tuile périodique, sans rotation (les encoches des bords doivent se correspondre)
        S = 500.0
        contour, trous, encoches_bas = tuile_aleatoire(S)
        demi_x, demi_y, pas_x, pas_y, decale_impair, variantes = S / 2, S / 2, S, S, 0.0, [0]
        # chant avant entaillé par les trous : la pince de la loupe va sur le plein le plus proche de -0,3 b
        cible = dx - b * 0.3
        entailles = [(x_min + S / 2 + i * S + s0, x_min + S / 2 + i * S + s1)
                     for i in range(int(b / S) + 1) for s0, s1 in encoches_bas]
        for a0, a1 in entailles:
            if a0 - 3 <= cible <= a1 + 3:
                cible = a0 - 3 if cible - (a0 - 3) < (a1 + 3) - cible else a1 + 3
        piece["x_loupe"] = cible - dx
    verts, faces = dalle_percee(contour, trous, e)
    tirage = random.Random(3)
    interieurs, bords = {v: [] for v in variantes}, []
    for j in range(-1, int(L / pas_y) + 2):
        cy = pas_y / 2 + j * pas_y
        for i in range(-2, int(b / pas_x) + 3):
            cx = x_min + pas_x / 2 + i * pas_x + (decale_impair if j % 2 else 0.0)
            if cx + demi_x <= x_min or cx - demi_x >= x_max or cy + demi_y <= 0 or cy - demi_y >= L:
                continue
            rot = tirage.choice(variantes)
            if x_min - 1e-6 <= cx - demi_x and cx + demi_x <= x_max + 1e-6 and -1e-6 <= cy - demi_y and cy + demi_y <= L + 1e-6:
                interieurs[rot].append((cx, cy, 0.0))
            else:
                bords.append((cx, cy, rot))
    objs = []
    for rot, pts in interieurs.items():
        if not pts:
            continue
        gabarit = maillage(f"{nom}-cellule{rot}", verts, faces, rotation_z=rot, aretes_vives=True)
        me = bpy.data.meshes.new(f"{nom}-cellules{rot}")
        me.from_pydata([(x * MM, y * MM, z * MM) for x, y, z in pts], [], [])
        nuage = bpy.data.objects.new(f"{nom}-cellules{rot}", me)
        bpy.context.collection.objects.link(nuage)
        nuage.instance_type = "VERTS"
        nuage.show_instancer_for_render = False
        gabarit.parent = nuage
        objs.append(gabarit)
    # cellules du bord : coupées par les plans de la plaque (on garde l'intérieur) puis refermées
    plans = (((x_min, 0, 0), (-1, 0, 0)), ((x_max, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, -1, 0)), ((0, L, 0), (0, 1, 0)))
    bm_bord = bmesh.new()
    for cx, cy, rot in bords:
        bm = bmesh.new()
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        vs = [bm.verts.new((x * c - y * s + cx, x * s + y * c + cy, z)) for x, y, z in verts]
        for face in faces:
            bm.faces.new([vs[k] for k in face])
        for co, no in plans:
            valeurs = [(v.co.x - co[0]) * no[0] + (v.co.y - co[1]) * no[1] for v in bm.verts]
            if not valeurs or max(valeurs) <= 1e-6:
                continue  # cellule entièrement du bon côté de ce plan
            res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-6,
                                         plane_co=co, plane_no=no, clear_outer=True)
            coupe = [g for g in res["geom_cut"] if isinstance(g, bmesh.types.BMEdge) and g.is_valid]
            if coupe:
                bmesh.ops.holes_fill(bm, edges=coupe, sides=0)
        if bm.faces:
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            tmp = bpy.data.meshes.new("tmp")
            bm.to_mesh(tmp)
            bm_bord.from_mesh(tmp)
            bpy.data.meshes.remove(tmp)
        bm.free()
    for f in bm_bord.faces:  # chant avant et arrière : matière de coupe, comme les tôles pleines
        f.material_index = 1 if all(abs(v.co.y) < 1e-4 or abs(v.co.y - L) < 1e-4 for v in f.verts) else 0
    aretes_par_angle(bm_bord)
    bmesh.ops.scale(bm_bord, vec=(MM, MM, MM), verts=bm_bord.verts)
    me = bpy.data.meshes.new(f"{nom}-bord")
    bm_bord.to_mesh(me)
    bm_bord.free()
    obj = bpy.data.objects.new(f"{nom}-bord", me)
    bpy.context.collection.objects.link(obj)
    objs.append(obj)
    return objs


# ---------------------------------------------------------------- caillebotis, marches, planchers perforés

def boite(nom, x0, x1, y0, y1, z0, z1, materiau_coupe_y=True):
    """Parallélépipède plein (mm) : barreau, plat de rive, joue. Faces d'about (normales ± y) en matière de coupe,
    sauf `materiau_coupe_y=False` (pièce entière, rien n'est scié)."""
    obj = extruder([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y1 - y0, nom)
    obj.location.y = y0 * MM
    obj.modifiers["chanfrein"].width = 0.3 * MM
    if not materiau_coupe_y:
        sans_coupe(obj)
    return obj


def sans_coupe(obj):
    """Toutes les faces en matière de surface : pièce livrée entière (caillebotis, marche), pas un tronçon scié."""
    for poly in obj.data.polygons:
        poly.material_index = 0
    return obj


def plaque_percee(nom, largeur, hauteur, e, trous, repere, lisse=False, contour=None):
    """Plaque percée (dalle_percee dans son plan u-v, épaisseur w) placée par `repere` : fonction (u, v, w) -> (x, y, z)
    en mm. `trous` : contours fermés (u, v). `contour` : contour extérieur (u, v) quelconque au lieu du rectangle
    largeur × hauteur (tubes du poteau CLOPLUS 40)."""
    contour = contour or [(-largeur / 2, -hauteur / 2), (largeur / 2, -hauteur / 2), (largeur / 2, hauteur / 2), (-largeur / 2, hauteur / 2)]
    verts, faces = dalle_percee(contour, trous, e)
    me = bpy.data.meshes.new(nom)
    me.from_pydata([tuple(c * MM for c in repere(u, v, w)) for u, v, w in verts], [], faces)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    aretes_par_angle(bm)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(nom, me)
    bpy.context.collection.objects.link(obj)
    return obj


def caillebotis(piece, dx, nom):
    """Caillebotis pressé : cadre de plats de rive (h × t), barreaux porteurs h × t au pas `maille_b` le long de y
    (la portée L), barres transversales carrées tournées de 45° (5 mm, forme usuelle) au pas `maille_a`, affleurant
    le dessus. Marche d'escalier : barreaux porteurs le long de x (entre limons), nez perforé devant et joues percées
    aux deux bouts (forme du rendu). -> objets"""
    g = piece["caillebotis"]
    h, t, b, L = piece["h"], g["t"], piece["b"], piece["longueur"]
    ma, mb, marche = g["maille_a"], g["maille_b"], g.get("marche", False)
    x0, x1 = dx - b / 2, dx + b / 2
    entier = dict(materiau_coupe_y=False)  # pièce livrée entière : aucune face sciée
    objs = [boite(f"{nom}-rive-av", x0, x1, 0, t, 0, h, **entier), boite(f"{nom}-rive-ar", x0, x1, L - t, L, 0, h, **entier),
            boite(f"{nom}-rive-g", x0, x0 + t, t, L - t, 0, h, **entier), boite(f"{nom}-rive-d", x1 - t, x1, t, L - t, 0, h, **entier)]
    c = 5.0  # barre transversale carrée (forme usuelle)
    if not marche:  # porteurs le long de y, transversales le long de x
        n = int((b - 2 * t) / mb)
        for k in range(1, n + 1):
            x = x0 + k * mb
            if x < x1 - t - mb * 0.3:
                objs.append(boite(f"{nom}-porteur-{k}", x - t / 2, x + t / 2, t, L - t, 0, h, **entier))
        for k in range(1, int((L - 2 * t) / ma) + 1):
            y = k * ma
            if y < L - t - ma * 0.3:
                bar = extruder(cercle(c / 2 * math.sqrt(2), h - c / 2 * math.sqrt(2), 4), b - 2 * t, f"{nom}-trans-{k}")
                bar.rotation_euler = (0, 0, math.radians(-90))
                bar.location = (x0 * MM + t * MM, y * MM, 0)
                objs.append(sans_coupe(bar))
    else:  # porteurs le long de x (entre limons), transversales le long de y
        n = int((L - 2 * t) / mb)
        for k in range(1, n + 1):
            y = t + k * mb
            if y < L - t - mb * 0.3:
                objs.append(boite(f"{nom}-porteur-{k}", x0 + t, x1 - t, y - t / 2, y + t / 2, 0, h, **entier))
        for k in range(1, int((b - 2 * t) / ma) + 1):
            x = x0 + k * ma
            if x < x1 - t - ma * 0.3:
                objs.append(sans_coupe(extruder([(xx + x, zz) for xx, zz in cercle(c / 2 * math.sqrt(2), h - c / 2 * math.sqrt(2), 4)],
                                                L - 2 * t, f"{nom}-trans-{k}")))
                objs[-1].location.y = t * MM
        # nez antidérapant perforé (trous Ø 8 au pas de 25) devant, joues percées de 2 trous Ø 11 aux bouts
        trous = [cercle_xy(u, 0.0, 8.0, 12) for u in range(int(-b / 2 + 40), int(b / 2 - 30), 25)]
        objs.append(plaque_percee(f"{nom}-nez", b, h + 8, 2.0, trous, lambda u, v, w: (dx + u, -w, v + (h + 8) / 2 - 8)))
        for cote, x in (("g", x0 - 3.0), ("d", x1)):
            trous = [cercle_xy(-L / 2 + 40, 0.0, 11.0, 14), cercle_xy(L / 2 - 40, 0.0, 11.0, 14)]
            objs.append(plaque_percee(f"{nom}-joue-{cote}", L, h + 20, 3.0, trous, lambda u, v, w, x=x: (x + w, u + L / 2, v + (h + 20) / 2)))
    return objs


def plancher_o2(piece, dx, nom):
    """Plancher / marche de sécurité O2 (PcP) : tôle percée de trous emboutis Ø 9 au pas de 25 × 25 (collerettes en
    relief) et de trous de drainage Ø 5 entre eux, bords longs pliés vers le bas sur la hauteur h ; marche : joues
    percées aux bouts. Forme du rendu d'après la fiche fournisseur et la photo du site. -> objets"""
    o = piece["o2"]
    h, t, b, L = piece["h"], o["t"], piece["b"], piece["longueur"]
    d9, d5, pas = o["trous"], o["drainage"], o["entraxe"]
    nx, ny = int((b - 30) / pas), int((L - 30) / pas)
    u0, v0 = -(nx - 1) * pas / 2, -(ny - 1) * pas / 2
    trous, centres = [], []
    for i in range(nx):
        for j in range(ny):
            u, v = u0 + i * pas, v0 + j * pas
            trous.append(cercle_xy(u, v, d9, 16))
            centres.append((u, v))
            if i < nx - 1 and j < ny - 1:
                trous.append(cercle_xy(u + pas / 2, v + pas / 2, d5, 10))
    dessus = plaque_percee(f"{nom}-dessus", b, L, t, trous, lambda u, v, w: (dx + u, v + L / 2, h - t + w))
    objs = [dessus]
    # collerettes des trous emboutis : anneaux tronconiques en instances
    r_ext, r_int, haut = d9 / 2 + 2.0, d9 / 2, 2.5
    verts, faces, n = [], [], 16
    for k in range(n):
        a = 2 * math.pi * k / n
        verts += [(r_ext * math.cos(a), r_ext * math.sin(a), 0.0), (r_int * math.cos(a), r_int * math.sin(a), haut)]
    for k in range(n):
        k2 = (k + 1) % n
        faces.append((2 * k, 2 * k2, 2 * k2 + 1, 2 * k + 1))
    collerette = maillage(f"{nom}-collerette", verts, faces)
    me = bpy.data.meshes.new(f"{nom}-collerettes")
    me.from_pydata([((dx + u) * MM, (v + L / 2) * MM, h * MM) for u, v in centres], [], [])
    nuage = bpy.data.objects.new(f"{nom}-collerettes", me)
    bpy.context.collection.objects.link(nuage)
    nuage.instance_type = "VERTS"
    nuage.show_instancer_for_render = False
    collerette.parent = nuage
    objs.append(collerette)
    # bords pliés vers le bas devant et derrière (y = 0 et y = L), hauteur h : le chant avant, plein, porte la loupe ;
    # pièce entière, rien n'est scié
    for cote, y in (("av", 0.0), ("ar", L - t)):
        objs.append(boite(f"{nom}-bord-{cote}", dx - b / 2, dx + b / 2, y, y + t, 0, h - t, materiau_coupe_y=False))
    if o.get("marche"):  # joues percées aux deux bouts (photo du site : 2 trous), nez arrondi non modélisé
        for cote, x in (("g", dx - b / 2), ("d", dx + b / 2 - t)):
            trous = [cercle_xy(-L / 2 + 40, 0.0, 11.0, 14), cercle_xy(L / 2 - 40, 0.0, 11.0, 14)]
            objs.append(plaque_percee(f"{nom}-joue-{cote}", L, h, t, trous, lambda u, v, w, x=x: (x + w, u + L / 2, v + h / 2)))
    return objs


# ---------------------------------------------------------------- clôtures

def plan_panneau_205(H, fh, h_pli, axe_h, travees, abouts):
    """Axes z des fils horizontaux dans le plan du panneau et z0 (axe du fil bas) de chaque pli : pli en pied, plis
    séparés par `travees` entraxes de `axe_h` (de bas en haut, dessin des hauteurs des fiches FTCP40PLIS205 et
    FTCG64PLIS205), pli en tête sous les abouts. -> (z du plan, z0 des plis) ; erreur si les travées ne bouclent pas H."""
    z = fh / 2
    plis, plan = [z], [z, z + h_pli]
    z += h_pli
    for n in travees:
        for _ in range(n):
            z += axe_h
            plan.append(z)
        plis.append(z)
        z += h_pli
        plan.append(z)
    if abs(z + fh / 2 + abouts - H) > 1:  # 1530 = 2,5 + 100 + 600 + 100 + 600 + 100 + 2,5 + 25
        raise ValueError(f"travées {travees} incompatibles avec H {H}")
    return plan, plis


def panneau_cloture(piece, dx, nom):
    """Panneau rigide « type 205 » à maille verticale debout dans le plan x-z (z = 0 sous le fil inférieur) : fils
    VERTICAUX Ø fil_v à l'axe axe_v (55), fils HORIZONTAUX Ø fil_h à l'axe axe_h (200) sur toute la largeur l, soudés
    côté +y ; plis en V vers +y de h_pli (100) portant 3 fils (bas, sommet, haut), un en pied, un en tête sous les
    abouts, les autres séparés par `travees` entraxes (FTCP40PLIS205). Abouts de 25 mm en tête, bord lisse en pied.
    Vérification indépendante du 15/09 : l'ancien modèle avait la maille tournée de 90° et des plis mal placés. -> objets"""
    c = piece["cloture"]
    H, l = piece["h"], piece["b"]
    fh, fv = c["fil_h"], c["fil_v"]
    axe_v, axe_h, h_pli = c["axe_v"], c["axe_h"], c["h_pli"]
    prof, droit, abouts = c["prof_pli"], c["droit_pli"], c["abouts"]
    plan, plis = plan_panneau_205(H, fh, h_pli, axe_h, c["travees"], abouts)
    ecart = (fh + fv) / 2  # axe du fil horizontal derrière l'axe du vertical (fils tangents)
    objs = []

    def fil_h(i, zh, y):
        fil = extruder(cercle(fh / 2, zh, 20), l, f"{nom}-h{i}")
        fil.rotation_euler = (0, 0, math.radians(-90))  # y local -> x monde, x local -> -y monde
        fil.location = ((dx - l / 2) * MM, (y + ecart) * MM, 0)
        return sans_coupe(fil)  # panneau laqué après soudage : bouts des fils dans la laque, pas en acier nu

    for i, zh in enumerate(plan):
        objs.append(fil_h(i, zh, 0.0))
    for k, z0 in enumerate(plis):  # fil du sommet du V
        objs.append(fil_h(len(plan) + k, z0 + h_pli / 2, prof))
    profil = [(0.0, 0.0)]
    for z0 in plis:
        profil += [(0.0, z0 + droit), (prof, z0 + h_pli / 2), (0.0, z0 + h_pli - droit)]
    profil.append((0.0, H))  # abouts : jusqu'en tête
    n_v = c["n_fils_v"]
    x0 = dx - (n_v - 1) * axe_v / 2
    for j in range(n_v):
        x = x0 + j * axe_v
        objs.append(courbe_tube(f"{nom}-v{j}", [(x, y, zz) for y, zz in profil], fv / 2, resolution=6))
    return objs


def poteau_clogriff(piece, dx, nom):
    """Poteau CLOGRIFF 64 couché comme un profilé : tube b × h à parois t (forme), parois hautes (h) percées d'encoches
    de `encoche` mm au pas `pas` (dessin de la fiche fournisseur : 30 et 100) où s'accrochent les fils du panneau."""
    q = piece["poteau"]
    b, h, t, L = piece["b"], piece["h"], piece["t"], piece["longueur"]
    enc, pas = q["encoche"], q["pas"]
    objs = [boite(f"{nom}-bas", dx - b / 2, dx + b / 2, 0, L, 0, t), boite(f"{nom}-haut", dx - b / 2, dx + b / 2, 0, L, h - t, h)]
    trous = []
    y = pas / 2
    while y + enc / 2 < L:
        trous.append([(y - enc / 2 - L / 2, -4.0), (y + enc / 2 - L / 2, -4.0), (y + enc / 2 - L / 2, 4.0), (y - enc / 2 - L / 2, 4.0)])
        y += pas
    for cote, x in (("g", dx - b / 2), ("d", dx + b / 2 - t)):
        objs.append(plaque_percee(f"{nom}-paroi-{cote}", L, h - 2 * t, t, trous, lambda u, v, w, x=x: (x + w, u + L / 2, v + h / 2)))
    return objs


def contour_cloplus(q, b, h):
    """Section du poteau CLOPLUS 40 (dessin de section de FTCP40PLIS205, tourné de 90° : h = 76 le long de z) : deux
    tubes creux b × `tube` (40 × 13,5) en z = 0 et z = h, lèvres de `levre` (1,5) aux deux bouts de chaque tube côté
    feuillure (ouverture 76 − 2 × 15 = 46), âme centrée en x = 0 raccordée par des congés `conge` (R 3). Parois et âme
    de `paroi` / `ame` (1,8, supposées), petits rayons supposés. -> (contour extérieur, [cavité basse, cavité haute])."""
    D, lv, t, tw, rf = q["tube"], q["levre"], q["paroi"], q["ame"], q["conge"]
    xl, xt, zl = b / 2 - t, tw / 2, D + lv
    droite = [((b / 2, 0), 1.0), ((b / 2, zl), 0.6), ((xl, zl), 0.6), ((xl, D), 0.5), ((xt, D), rf),
              ((xt, h - D), rf), ((xl, h - D), 0.5), ((xl, h - zl), 0.6), ((b / 2, h - zl), 0.6), ((b / 2, h), 1.0)]
    gauche = [((-x, z), r) for (x, z), r in reversed(droite)]  # symétrique par rapport à x = 0, sens trigonométrique
    coins = [c for c, _ in droite + gauche]
    rayons = [r for _, r in droite + gauche]
    contour = dedoublonner(contour_arrondi(coins, rayons, 6))
    bas = dedoublonner(contour_arrondi([(-xl, t), (xl, t), (xl, D - t), (-xl, D - t)], [0.5] * 4, 3))
    haut = [(x, h - z) for x, z in reversed(bas)]
    return contour, [bas, haut]


def faces_bout_en_coupe(obj, L):
    """Faces d'about (tous leurs sommets en y = 0, ou tous en y = L) en matière de coupe, les autres en surface."""
    for poly in obj.data.polygons:
        ys = [obj.data.vertices[k].co.y for k in poly.vertices]
        bout = all(abs(y) < 1e-7 for y in ys) or all(abs(y - L * MM) < 1e-7 for y in ys)
        poly.material_index = 1 if bout else 0
    return obj


def poteau_cloplus(piece, dx, nom):
    """Poteau CLOPLUS 40 couché comme un profilé (FTCP40PLIS205) : profilé alu en H à deux tubes creux (tube bas en
    z 0 → 13,5, tube haut en z 62,5 → 76), lèvres et feuillures de 46 ouvertes vers ± x, âme mince dans le plan x = 0
    percée dans son axe (1er trou à `premier_trou` du bout y = 0, puis au pas `pas_trous` : cotes 50 et 100 de la fiche),
    capuchon noir en H en tête (bout y = L). Un seul objet laqué (profil d'un tenant, trous percés par un booléen) +
    capuchon. Premier essai en trois objets (tubes + plaque d'âme qui recouvrait leurs amorces) : faces d'about coplanaires,
    taches noires aux raccords âme/tubes (essai du 15/09). -> [(objet, matière)]"""
    q = piece["poteau"]
    b, h, L = piece["b"], piece["h"], piece["longueur"]
    contour, cavites = contour_cloplus(q, b, h)
    profil = plaque_percee(f"{nom}-profil", 0, 0, L, cavites, lambda u, v, w: (dx + u, w, v), contour=contour)
    # abouts retriangulés : la triangulation reliait des points colinéaires de part et d'autre de l'âme (z = 62,5), triangle
    # d'aire nulle que le booléen exact changeait en fente d'about (contrôle géométrique du 15/09)
    bm = bmesh.new()
    bm.from_mesh(profil.data)
    bouts = [f for f in bm.faces if all(abs(v.co.y) < 1e-7 for v in f.verts) or all(abs(v.co.y - L * MM) < 1e-7 for v in f.verts)]
    dans_bouts = set(bouts)
    internes = [e for e in bm.edges if len(e.link_faces) == 2 and all(f in dans_bouts for f in e.link_faces)]
    bmesh.ops.beautify_fill(bm, faces=bouts, edges=internes)
    aretes_par_angle(bm)
    bm.to_mesh(profil.data)
    bm.free()
    faces_bout_en_coupe(profil, L)
    # trous oblongs de l'âme : prismes traversant l'âme (x de −2 à 2), retirés par un booléen exact ; leurs parois
    # prennent la matière d'index 0 (laque : percés avant thermolaquage). Coupeur masqué, hors de la liste des objets.
    lt, ht = q["trou"]  # lt le long du poteau (y), ht en travers (z)
    r = ht / 2
    verts, faces, y = [], [], q["premier_trou"]
    while y + lt / 2 <= L - 1:
        oblong = arc(y + lt / 2 - r, h / 2, r, -90, 90, 8) + arc(y - lt / 2 + r, h / 2, r, 90, 270, 8)
        vs, fs = dalle_percee(oblong, [], 4.0)
        n0 = len(verts)
        verts += [((dx - 2.0 + w) * MM, u * MM, v * MM) for u, v, w in vs]
        faces += [tuple(k + n0 for k in f) for f in fs]
        y += q["pas_trous"]
    if faces:
        me = bpy.data.meshes.new(f"{nom}-percage")
        me.from_pydata(verts, [], faces)
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        aretes_par_angle(bm)
        bm.to_mesh(me)
        bm.free()
        coupeur = bpy.data.objects.new(f"{nom}-percage", me)
        bpy.context.collection.objects.link(coupeur)
        coupeur.hide_render = True
        bool_ = profil.modifiers.new("trous", "BOOLEAN")
        bool_.operation = "DIFFERENCE"
        bool_.solver = "EXACT"
        bool_.object = coupeur
    bev = profil.modifiers.new("chanfrein", "BEVEL")  # après le perçage : bords des trous chanfreinés aussi
    bev.width = 0.3 * MM
    bev.segments = 3
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(30)
    objs = [(profil, None)]
    if q.get("capuchon"):  # en tête (y = L) ; le bout y = 0 est le pied scié, section visible
        # H noir débordant de 1 autour du profil, bande centrale de 6 sur l'âme (proportions de la vue 3D de la fiche) ;
        # avec 40 × 76 : x ± 21, z −1 → 77, tubes jusqu'à z 16 et depuis z 60
        de, xw = 1.0, 3.0
        xa, zb = b / 2 + de, q["tube"] + q["levre"] + de
        coins = [(-xa, -de), (xa, -de), (xa, zb), (xw, zb), (xw, h - zb), (xa, h - zb), (xa, h + de), (-xa, h + de),
                 (-xa, h - zb), (-xw, h - zb), (-xw, zb), (-xa, zb)]
        rayons = [2, 2, 1, 1.5, 1.5, 1, 2, 2, 1, 1.5, 1.5, 1]
        cap = extruder(dedoublonner(contour_arrondi(coins, rayons, 4)), q["capuchon"], f"{nom}-capuchon", decalage_x=dx)
        cap.location.y = L * MM
        objs.append((sans_coupe(cap), "CAPUCHON"))
    return objs


def section_de(piece):
    t = piece["type"]
    if t == "POTEAU":  # CLOPLUS 40 et CLOGRIFF 64 ont leur géométrie propre : aucun poteau ne retombe sur un tube
        raise ValueError("POTEAU : poteau_cloplus (feuillure) ou poteau_clogriff (encoche)")
    if t == "TOLE" and piece.get("profil"):  # tôle profilée ou tasseau : tôle pliée, x centré, fond en z = 0
        ligne = profil_de_tole(piece)
        return [(x - piece["b"] / 2, z) for x, z in section_pliee(ligne, piece["h"])]
    if t == "TOLE":  # plaque posée à plat : section largeur × épaisseur, extrudée sur la longueur
        return section_rectangle(piece["h"], piece["b"])
    if t == "BORDURE":  # face avant en x = +b/2 (épaisseur t), pli vers l'arrière ; b = profondeur du pli + tôle
        e = piece["t"]
        ligne = ligne_bordure(piece["h"], piece["pli"], piece["angle"], e)
        return section_pliee([(x + piece["b"] / 2 - e / 2, z) for x, z in ligne], e)
    if t == "T":
        return section_t(piece["h"], piece["b"], piece["t"], piece["r"], piece["r1"], piece["r2"])
    if t in ("PLAT", "CARRE"):
        return section_rectangle(piece["h"], piece["b"])
    if t in ("ROND", "ROND-BETON"):
        return cercle(piece["h"] / 2, piece["h"] / 2)
    if t in ("TC", "TR"):
        return section_tube_rect(piece["h"], piece["b"], piece["t"], piece["r1"])
    if t == "TUBE-ROND":
        return section_tube_rond(piece["h"], piece["t"])
    if t == "L":
        return section_l(piece["h"], piece["b"], piece["t"], piece["r1"], piece["r2"])
    if piece["type"] == "U":
        return section_u(piece["h"], piece["b"], piece["tw"], piece["tf"], piece["r1"], piece["r2"], piece.get("pente", 8.0))
    return section_i(piece["h"], piece["b"], piece["tw"], piece["tf"], piece["r"])


# ---------------------------------------------------------------- matériaux

def noeud(nt, type_, loc, **inputs):
    n = nt.nodes.new(type_)
    n.location = loc
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def materiau_calamine():
    """Acier laminé à chaud brut : calamine gris bleuté, satinée, marbrée."""
    m = bpy.data.materials.new("calamine")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]

    coord = nt.nodes.new("ShaderNodeTexCoord")
    bruit = noeud(nt, "ShaderNodeTexNoise", (-900, 200), Scale=6.0, Detail=8.0, Roughness=0.6)
    nt.links.new(coord.outputs["Object"], bruit.inputs["Vector"])

    rampe = nt.nodes.new("ShaderNodeValToRGB")
    rampe.location = (-600, 300)
    rampe.color_ramp.elements[0].position = 0.30
    rampe.color_ramp.elements[0].color = (0.022, 0.025, 0.030, 1)
    rampe.color_ramp.elements[1].position = 0.80
    rampe.color_ramp.elements[1].color = (0.085, 0.088, 0.094, 1)
    nt.links.new(bruit.outputs["Fac"], rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], bsdf.inputs["Base Color"])

    rug = nt.nodes.new("ShaderNodeMapRange")
    rug.location = (-600, 0)
    rug.inputs["To Min"].default_value = 0.48
    rug.inputs["To Max"].default_value = 0.78
    nt.links.new(bruit.outputs["Fac"], rug.inputs["Value"])
    nt.links.new(rug.outputs["Result"], bsdf.inputs["Roughness"])

    grain = noeud(nt, "ShaderNodeTexNoise", (-900, -250), Scale=900.0, Detail=4.0)
    nt.links.new(coord.outputs["Object"], grain.inputs["Vector"])
    relief = noeud(nt, "ShaderNodeBump", (-400, -250), Strength=0.08, Distance=0.0005)
    nt.links.new(grain.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Metallic"].default_value = p_mat("metal_calamine", 0.12)
    bsdf.inputs["Specular IOR Level"].default_value = 0.45
    return m


def materiau_gpp():
    """GPP : grenaillé puis peinture primaire (description du site actuel). Teinte calée sur la vraie photo."""
    m = bpy.data.materials.new("gpp")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    r, g, b = (lineaire(c) for c in p_mat("teinte_gpp", TEINTE_GPP))

    coord = nt.nodes.new("ShaderNodeTexCoord")
    nuage = noeud(nt, "ShaderNodeTexNoise", (-900, 200), Scale=3.0, Detail=6.0, Roughness=0.5)
    nt.links.new(coord.outputs["Object"], nuage.inputs["Vector"])
    rampe = nt.nodes.new("ShaderNodeValToRGB")
    rampe.location = (-600, 300)
    rampe.color_ramp.elements[0].position = 0.25
    rampe.color_ramp.elements[0].color = (r * 0.88, g * 0.88, b * 0.88, 1)
    rampe.color_ramp.elements[1].position = 0.85
    rampe.color_ramp.elements[1].color = (r * 1.08, g * 1.06, b * 1.06, 1)
    nt.links.new(nuage.outputs["Fac"], rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], bsdf.inputs["Base Color"])

    # peinture mate sur surface grenaillée : grain fin
    grain = noeud(nt, "ShaderNodeTexNoise", (-900, -250), Scale=1400.0, Detail=3.0)
    nt.links.new(coord.outputs["Object"], grain.inputs["Vector"])
    relief = noeud(nt, "ShaderNodeBump", (-400, -250), Strength=0.05, Distance=0.0003)
    nt.links.new(grain.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = p_mat("rugosite_gpp", 0.62)
    bsdf.inputs["Specular IOR Level"].default_value = 0.4
    return m


def materiau_coupe():
    """Face sciée : acier nu clair, stries de scie."""
    m = bpy.data.materials.new("coupe")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.36, 0.37, 0.38, 1)
    bsdf.inputs["Metallic"].default_value = 1.0

    coord = nt.nodes.new("ShaderNodeTexCoord")
    stries = noeud(nt, "ShaderNodeTexWave", (-700, -200), Scale=260.0, Distortion=1.5, Detail=3.0)
    stries.bands_direction = "Z"
    nt.links.new(coord.outputs["Object"], stries.inputs["Vector"])
    relief = noeud(nt, "ShaderNodeBump", (-400, -200), Strength=0.12, Distance=0.0003)
    nt.links.new(stries.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], bsdf.inputs["Normal"])

    rug = nt.nodes.new("ShaderNodeMapRange")
    rug.location = (-400, 100)
    rug.inputs["To Min"].default_value = 0.32
    rug.inputs["To Max"].default_value = 0.46
    nt.links.new(stries.outputs["Fac"], rug.inputs["Value"])
    nt.links.new(rug.outputs["Result"], bsdf.inputs["Roughness"])
    return m


def materiau_metal(nom, base, rugosite, variation=0.06, metallic=1.0, cellules=0.0, stries_y=0.0, anisotropie=0.0,
                   ecart_rugosite=0.2, brossage=0.0):
    """Métal nu générique : `cellules` = échelle de fleurage (galvanisé, cellules de Voronoï par mètre),
    `stries_y` = échelle de stries le long de la barre (filage alu, brossage inox), `anisotropie` = reflet étiré
    (sans carte UV, Cycles étire le reflet en cercles autour de l'axe Z : croix sombre sur une tôle, à éviter),
    `ecart_rugosite` = variation relative de la rugosité (taches larges de 25 cm : faible sur les grandes tôles)."""
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    r, g, b = base
    if cellules:
        motif = noeud(nt, "ShaderNodeTexVoronoi", (-900, 200), Scale=cellules)
        sortie = motif.outputs["Color"]
    else:
        motif = noeud(nt, "ShaderNodeTexNoise", (-900, 200), Scale=4.0, Detail=5.0)
        sortie = motif.outputs["Fac"]
    nt.links.new(coord.outputs["Object"], motif.inputs["Vector"])
    gris = nt.nodes.new("ShaderNodeRGBToBW") if cellules else None
    if gris:
        gris.location = (-700, 200)
        nt.links.new(sortie, gris.inputs["Color"])
        sortie = gris.outputs["Val"]
    rampe = nt.nodes.new("ShaderNodeValToRGB")
    rampe.location = (-500, 300)
    rampe.color_ramp.elements[0].color = (r * (1 - variation), g * (1 - variation), b * (1 - variation), 1)
    rampe.color_ramp.elements[1].color = (r * (1 + variation), g * (1 + variation), b * (1 + variation), 1)
    nt.links.new(sortie, rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], bsdf.inputs["Base Color"])
    rug = nt.nodes.new("ShaderNodeMapRange")
    rug.location = (-500, 0)
    rug.inputs["To Min"].default_value = rugosite * (1 - ecart_rugosite)
    rug.inputs["To Max"].default_value = rugosite * (1 + ecart_rugosite)
    nt.links.new(sortie, rug.inputs["Value"])
    nt.links.new(rug.outputs["Result"], bsdf.inputs["Roughness"])
    if stries_y:  # stries fines le long de y : bruit très étiré
        etirement = noeud(nt, "ShaderNodeMapping", (-1100, -250))
        etirement.inputs["Scale"].default_value = (stries_y, stries_y * 0.004, stries_y)
        nt.links.new(coord.outputs["Object"], etirement.inputs["Vector"])
        stries = noeud(nt, "ShaderNodeTexNoise", (-900, -250), Scale=1.0, Detail=2.0)
        nt.links.new(etirement.outputs["Vector"], stries.inputs["Vector"])
        relief = noeud(nt, "ShaderNodeBump", (-400, -250), Strength=0.06, Distance=0.0002)
        nt.links.new(stries.outputs["Fac"], relief.inputs["Height"])
        nt.links.new(relief.outputs["Normal"], bsdf.inputs["Normal"])
    if brossage:
        # brossage visible : `brossage` stries sur la taille de la plus grande pièce (~3 px de large quelle que soit
        # la pièce), longues le long de y ; il module la rugosité et le relief. Les stries de 0,4 mm de `stries_y`
        # tombaient sous le pixel : tôle inox « brossée » rendue en miroir lisse (vérification du 15/09).
        f = brossage / max(ECHELLE["taille_m"], 0.05)
        etirement_b = noeud(nt, "ShaderNodeMapping", (-1100, -500))
        etirement_b.inputs["Scale"].default_value = (f, f * p_mat("etirement_brossage", 0.0015), f)
        nt.links.new(coord.outputs["Object"], etirement_b.inputs["Vector"])
        stries_b = noeud(nt, "ShaderNodeTexNoise", (-900, -500), Scale=1.0, Detail=4.0, Roughness=0.7)
        nt.links.new(etirement_b.outputs["Vector"], stries_b.inputs["Vector"])
        rug_b = noeud(nt, "ShaderNodeMapRange", (-500, -500))
        rug_b.inputs["From Min"].default_value = 0.35
        rug_b.inputs["From Max"].default_value = 0.65
        contraste = p_mat("contraste_brossage", 0.2)
        rug_b.inputs["To Min"].default_value = rugosite * (1 - contraste)
        rug_b.inputs["To Max"].default_value = rugosite * (1 + contraste)
        nt.links.new(stries_b.outputs["Fac"], rug_b.inputs["Value"])
        nt.links.new(rug_b.outputs["Result"], bsdf.inputs["Roughness"])
        relief_b = noeud(nt, "ShaderNodeBump", (-400, -500), Strength=p_mat("relief_brossage", 0.06), Distance=0.0002)
        nt.links.new(stries_b.outputs["Fac"], relief_b.inputs["Height"])
        nt.links.new(relief_b.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Metallic"].default_value = metallic
    if anisotropie:
        bsdf.inputs["Anisotropic"].default_value = anisotropie
    return m


def materiau_galva():
    """Galvanisé à chaud : zinc gris clair, fleurage (cristaux de quelques millimètres), reflets variables."""
    return materiau_metal("galva", (0.42, 0.44, 0.45), 0.34, variation=0.10, cellules=220.0)


def materiau_alu():
    """Aluminium brut de filage ou de laminage : gris très clair, reflet diffus (essai du 14/09 : à 0,30 de rugosité,
    la tôle reflétait une traînée sombre du studio), stries fines dans le sens de la barre."""
    return materiau_metal("alu", (0.78, 0.79, 0.80), 0.42, variation=0.03, stries_y=900.0, ecart_rugosite=0.08)


def materiau_inox():
    """Inox 304 satiné : gris acier clair, brossage visible dans le sens de la barre, sans anisotropie. À 0,30 de
    rugosité, les faces tournées vers le haut reflétaient le studio sombre : dessus des tubes carrés à 61/255 et tôle
    en miroir noir (vérification du 15/09)."""
    b = p_mat("base_inox", 0.62)
    return materiau_metal("inox", (b, b, b * 0.985), p_mat("rugosite_inox", 0.46), variation=0.02,
                          ecart_rugosite=0.06, brossage=p_mat("brossage_inox", 600.0))


def materiau_froid():
    """Acier laminé à froid : gris moyen lisse et satiné, sans calamine ni taches. À 0,32 de rugosité, la photo
    studio était un miroir noir, 60 niveaux sous les visuels caractéristiques (vérification du 15/09)."""
    b = p_mat("base_froid", 0.36)
    return materiau_metal("froid", (b, b * 1.03, b * 1.06), p_mat("rugosite_froid", 0.50), variation=0.02,
                          metallic=1.0, ecart_rugosite=0.06)


def materiau_corten():
    """Acier Corten patiné (aspect rouillé mis en avant par la description du site) : brun-orangé mat, taches."""
    m = bpy.data.materials.new("corten")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    taches = noeud(nt, "ShaderNodeTexNoise", (-900, 200), Scale=18.0, Detail=10.0, Roughness=0.65)
    nt.links.new(coord.outputs["Object"], taches.inputs["Vector"])
    rampe = nt.nodes.new("ShaderNodeValToRGB")
    rampe.location = (-600, 300)
    rampe.color_ramp.elements[0].position = 0.35
    rampe.color_ramp.elements[0].color = (0.16, 0.045, 0.018, 1)
    rampe.color_ramp.elements[1].position = 0.75
    rampe.color_ramp.elements[1].color = (0.36, 0.12, 0.04, 1)
    nt.links.new(taches.outputs["Fac"], rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], bsdf.inputs["Base Color"])
    grain = noeud(nt, "ShaderNodeTexNoise", (-900, -250), Scale=1100.0, Detail=4.0)
    nt.links.new(coord.outputs["Object"], grain.inputs["Vector"])
    relief = noeud(nt, "ShaderNodeBump", (-400, -250), Strength=0.15, Distance=0.0004)
    nt.links.new(grain.outputs["Fac"], relief.inputs["Height"])
    nt.links.new(relief.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.85
    return m


# teintes RAL (sRGB 0-255) des produits laqués du catalogue : nuancier usuel, seulement pour la matière du rendu
# 6005 : Lab RAL Classic 24,4 / −20,6 / 4,7 (e-paint.co.uk), pastille « RAL 6005 » de la photo du site (G083) mesurée
# (18, 66, 50) ; l'ancienne valeur (47, 69, 56) rendait les panneaux gris-vert (vérification indépendante du 15/09)
RAL = {"7016": (56, 62, 66), "9005": (14, 14, 16), "6005": (17, 66, 51)}
# renfort de saturation de la teinte de rendu, par RAL (1 = aucun) : AgX et le reflet satiné du studio grisent un vert
# sombre. Essai du 15/09 (fils de 4 mm, 1600 px, médiane des pixels opaques en Lab) : k 1,0 → 22,7 / −14,4 / 2,6
# (chroma 15) ; k 1,4 → chroma 19 ; k 1,7 → 25,0 / −20,0 / 6,5, pastille « RAL 6005 » de la photo du site 24,5 / −20,6 / 5,1.
# Gris 7016 et noir 9005 rendus justes, inchangés.
CHROMA_RAL = {"6005": 1.7}


def teinte_ral(ral):
    """Teinte de rendu (sRGB 0-255) d'un RAL : valeur du nuancier, écartée du gris de même luminance par CHROMA_RAL."""
    r, g, b = RAL.get(ral, RAL["7016"])
    k = p_mat(f"chroma_{ral}", CHROMA_RAL.get(ral, 1.0))
    if k == 1.0:
        return r, g, b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return tuple(min(255.0, max(0.0, y + k * (c - y))) for c in (r, g, b))


def materiau_laque(ral=None):
    """Acier ou aluminium thermolaqué / prélaqué polyester : couleur RAL unie, satinée, non métallique."""
    r, g, b = (lineaire(c) for c in teinte_ral(str(ral or PARAMS.get("ral", "7016"))))
    m = materiau_metal(f"laque-{ral}", (r, g, b), 0.42, variation=0.02, metallic=0.0, ecart_rugosite=0.05)
    m.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.4
    return m


def materiau_mousse():
    """Âme isolante en mousse de polyuréthane : crème mate, grain fin."""
    return materiau_metal("mousse", (0.80, 0.66, 0.36), 0.95, variation=0.05, metallic=0.0, ecart_rugosite=0.03)


def materiau_alu_feuille():
    """Feuille d'aluminium gaufrée sous le panneau : gris clair satiné."""
    return materiau_metal("alu-feuille", (0.70, 0.71, 0.72), 0.45, variation=0.04, metallic=1.0, ecart_rugosite=0.1)


def materiau_bois():
    """Bardage imitation chêne clair : veinage procédural étiré dans le sens de la longueur (bruit très allongé),
    teinte chêne clair ; les plats entre tasseaux reçoivent la matière `materiau_noir`."""
    m = bpy.data.materials.new("bois")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    etirement = noeud(nt, "ShaderNodeMapping", (-1100, 200))
    etirement.inputs["Scale"].default_value = (60.0, 1.2, 60.0)
    nt.links.new(coord.outputs["Object"], etirement.inputs["Vector"])
    veines = noeud(nt, "ShaderNodeTexNoise", (-900, 200), Scale=1.0, Detail=6.0, Roughness=0.6)
    nt.links.new(etirement.outputs["Vector"], veines.inputs["Vector"])
    rampe = nt.nodes.new("ShaderNodeValToRGB")
    rampe.location = (-600, 300)
    rampe.color_ramp.elements[0].position = 0.35
    rampe.color_ramp.elements[0].color = (lineaire(196), lineaire(150), lineaire(92), 1)
    rampe.color_ramp.elements[1].position = 0.7
    rampe.color_ramp.elements[1].color = (lineaire(232), lineaire(198), lineaire(140), 1)
    nt.links.new(veines.outputs["Fac"], rampe.inputs["Fac"])
    nt.links.new(rampe.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.5
    return m


def materiau_noir():
    """Bandes noires mates entre les tasseaux (procédé bi-couleur du fabricant)."""
    return materiau_metal("noir", (0.012, 0.012, 0.013), 0.6, variation=0.02, metallic=0.0, ecart_rugosite=0.05)


def materiau_capuchon():
    """Capuchon plastique noir du poteau CLOPLUS 40 (vue 3D de FTCP40PLIS205, photo du site G088) : noir satiné non
    métallique, un peu moins sombre que les bandes du tasseau pour garder son relief."""
    b = p_mat("base_capuchon", 0.03)
    return materiau_metal("capuchon", (b, b, b * 1.05), p_mat("rugosite_capuchon", 0.45), variation=0.02, metallic=0.0,
                          ecart_rugosite=0.05)


MATIERES = {"BRUT": materiau_calamine, "GPP": materiau_gpp, "GALVA": materiau_galva, "ALU": materiau_alu,
            "INOX": materiau_inox, "FROID": materiau_froid, "CORTEN": materiau_corten,
            "LAQUE": materiau_laque, "LAQUE-ALU": materiau_laque, "BOIS": materiau_bois,
            "MOUSSE": materiau_mousse, "ALU-FEUILLE": materiau_alu_feuille, "CAPUCHON": materiau_capuchon}


# ---------------------------------------------------------------- scène

def vider_scene():
    for collection in (bpy.data.objects, bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.lights,
                       bpy.data.cameras, bpy.data.worlds, bpy.data.images):
        for bloc in list(collection):
            collection.remove(bloc)


def lumiere_zone(nom, pos, cible, taille, energie):
    data = bpy.data.lights.new(nom, "AREA")
    data.shape = "RECTANGLE"
    data.size = taille
    data.size_y = taille * 0.7
    data.energy = energie
    obj = bpy.data.objects.new(nom, data)
    bpy.context.collection.objects.link(obj)
    obj.location = pos
    obj.rotation_euler = (Vector(cible) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    return obj


def monde_studio():
    w = bpy.data.worlds.new("studio")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    fond = nt.nodes["Background"]
    version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
    exr = os.path.join(os.path.dirname(bpy.app.binary_path), version,
                       "datafiles", "studiolights", "world", "studio.exr")
    if os.path.exists(exr):
        tex = nt.nodes.new("ShaderNodeTexEnvironment")
        tex.image = bpy.data.images.load(exr)
        nt.links.new(tex.outputs["Color"], fond.inputs["Color"])
    else:
        print("studio.exr introuvable :", exr)
    fond.inputs["Strength"].default_value = PARAMS.get("e_monde", 0.2)


def cadrer(cam, scene, points, boite, direction, cible):
    """Recule la caméra et la décale pour faire tenir `points` dans `boite` (u0, v0, u1, v1)."""
    u0, v0, u1, v1 = boite
    largeur_boite, hauteur_boite = u1 - u0, v1 - v0
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    ratio = scene.render.resolution_x / scene.render.resolution_y
    cam.data.shift_x = cam.data.shift_y = 0.0

    def etendue(d):
        cam.location = Vector(cible) + direction * d
        bpy.context.view_layer.update()
        proj = [world_to_camera_view(scene, cam, Vector(p)) for p in points]
        us = [q.x for q in proj]
        vs = [q.y for q in proj]
        return min(us), max(us), min(vs), max(vs)

    haut = 1.0
    for _ in range(4):
        bas, haut = 0.05, 60.0
        for _ in range(40):
            d = (bas + haut) / 2
            a, b, c, e = etendue(d)
            if (b - a) <= largeur_boite and (e - c) <= hauteur_boite:
                haut = d
            else:
                bas = d
        a, b, c, e = etendue(haut)
        cam.data.shift_x += ((a + b) / 2 - cu)
        cam.data.shift_y += ((c + e) / 2 - cv) / ratio
    etendue(haut)


def rendre(p):
    PARAMS.clear()
    PARAMS.update(p)
    t0 = time.time()
    vider_scene()
    scene = bpy.context.scene
    mode = p.get("mode", "caracteristiques")
    pieces = p.get("pieces") or [{k: p[k] for k in ("type", "h", "b", "tw", "tf", "r", "r1", "r2", "pente", "longueur") if k in p}]
    for piece in pieces:
        piece.setdefault("type", "I")

    finition = p.get("finition", "BRUT")
    ECHELLE["taille_m"] = max(max(q.get("longueur", p.get("longueur", 500)), q["b"], q["h"]) for q in pieces) * MM
    mat_surface = MATIERES.get(finition, materiau_calamine)()
    mat_coupe = materiau_coupe()

    # pièces côte à côte (studio) : la plus haute à gauche, extrémités alignées. La caméra, à droite, voit chaque
    # pièce par-dessus sa voisine de droite : un écart d'environ sa hauteur évite qu'elle cache la précédente.
    if len(pieces) > 1:
        pieces.sort(key=lambda q: -q["h"])
    x = 0.0
    boite_pts = []
    for i, piece in enumerate(pieces):
        L = piece.get("longueur", p.get("longueur", 500))
        if i:  # écart minimal de 12 % de la largeur (treillis : pièces larges et plates)
            x += max(p.get("ecart_studio", 0.9) * piece["h"], 0.12 * piece["b"])
        dx = x + piece["b"] / 2
        matieres_propres = {}  # objet -> matière particulière (âme de mousse, feuille d'aluminium)
        if piece["type"] == "TREILLIS":
            objs = fils_treillis(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("perforation"):  # tôle perforée : cellules percées au lieu d'une plaque pleine
            objs = plaque_perforee(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("sandwich"):  # panneau isolé : mousse, feuille d'aluminium, tôle nervurée
            objs = []
            for obj, matiere in panneau_isole(piece, dx, f"{p['slug']}-{i}"):
                objs.append(obj)
                if matiere:
                    matieres_propres[obj.name] = MATIERES[matiere]()
        elif piece.get("caillebotis"):
            objs = caillebotis(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("o2"):
            objs = plancher_o2(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("cloture"):
            objs = panneau_cloture(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("poteau", {}).get("encoche"):
            objs = poteau_clogriff(piece, dx, f"{p['slug']}-{i}")
        elif piece.get("poteau", {}).get("feuillure"):  # CLOPLUS 40 : profilé en H à feuillures, âme percée, capuchon
            objs = []
            for obj, matiere in poteau_cloplus(piece, dx, f"{p['slug']}-{i}"):
                objs.append(obj)
                if matiere:
                    matieres_propres[obj.name] = MATIERES[matiere]()
            if piece["poteau"].get("capuchon"):  # capuchon (débord de 1, épaisseur en y) dans le cadre, symétrique en x
                boite_pts += [((dx + sx * (piece["b"] / 2 + 1)) * MM, (L + piece["poteau"]["capuchon"]) * MM, z * MM)
                              for sx in (-1, 1) for z in (0, piece["h"] + 1)]
        else:
            objs = [extruder(section_de(piece), L, f"{p['slug']}-{i}", decalage_x=dx)]
            if piece["type"] == "ROND-BETON":
                objs += nervures_barre(piece["h"], L, dx, f"{p['slug']}-{i}")
            if piece.get("relief"):  # tôle larmée ou striée
                objs += relief_tole(piece, dx, f"{p['slug']}-{i}")
            if piece.get("profil"):  # tôle de 0,5 mm : pas de chanfrein (plus large que l'épaisseur)
                objs[0].modifiers.remove(objs[0].modifiers["chanfrein"])
        for obj in objs:
            obj.data.materials.append(matieres_propres.get(obj.name, mat_surface))
            if obj.type == "MESH":
                obj.data.materials.append(mat_coupe if obj.name not in matieres_propres else matieres_propres[obj.name])
        if piece.get("profil", {}).get("motif") == "TASSEAU":  # bandes noires : faces des plats, en fond de profil
            noir = materiau_noir()
            objs[0].data.materials.append(noir)
            for poly in objs[0].data.polygons:
                if poly.material_index == 0 and abs(poly.normal.z) > 0.9 and poly.center.z < 0.6 * MM:
                    poly.material_index = 2
        boite_pts += [((dx + sx * piece["b"] / 2) * MM, y * MM, z * MM)
                      for sx in (-1, 1) for y in (0, L) for z in (0, piece["h"])]
        if piece.get("depassants"):  # dépassants (fond et droite) dans le cadre, et la pièce suivante décalée d'autant
            boite_pts += [((dx + piece["b"] / 2 + piece["maille_b"]) * MM, y * MM, 0) for y in (0, L)]
            boite_pts += [((dx + sx * piece["b"] / 2) * MM, (L + piece["maille_a"]) * MM, 0) for sx in (-1, 1)]
            x += piece["maille_b"]
        x += piece["b"]
    centre_x = sum(q[0] for q in boite_pts) / len(boite_pts)
    # centre de la première pièce après recentrage : 0 pour une pièce symétrique ; −75 mm pour un treillis à dépassants
    # (points de dépassants à droite dans boite_pts), dont les points de cotes doivent suivre (vérification du 15/09)
    x0_piece = pieces[0]["b"] / 2 * MM - centre_x
    for obj in [o for o in bpy.data.objects if o.type in ("MESH", "CURVE") and o.parent is None]:
        obj.location.x -= centre_x  # les gabarits du relief suivent leur nuage de points
    boite_pts = [(q[0] - centre_x, q[1], q[2]) for q in boite_pts]

    # sol attrape-ombre
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    bpy.context.active_object.is_shadow_catcher = True

    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = p.get("focale", 50)
    # petites sections (rond de 6 mm, plat 10x3) : la caméra passe à quelques centimètres ; la découpe proche par
    # défaut (10 cm) coupait l'avant de la pièce et du sol
    cam_data.clip_start = 0.001
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam

    # caméra côté +X : la section apparaît à gauche, le corps file vers la droite
    az, el = math.radians(p.get("azimut", 20)), math.radians(p.get("elevation", 17))
    direction = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    h_max = max(q["h"] for q in pieces)
    L0 = pieces[0].get("longueur", p.get("longueur", 500))
    cible = Vector((0, L0 * MM * 0.35, h_max * MM * 0.5))
    cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()

    piece = pieces[0]
    h, b = piece["h"], piece["b"]
    typ = piece["type"]
    off = max(h, b) * 0.28  # écart des lignes de cote, en mm
    if typ == "PANNEAU-CLOTURE":  # panneau de 2,5 m : 28 % de la largeur rejetait la cote à 70 cm et vidait le bas du cadre
        off = min(h, b) * 0.12
    # cote horizontale : sous la pièce, au-dessus pour le T (largeur de l'aile), aucune pour plat, rond, tube rond
    # et bordure (l'épaisseur est pincée)
    cote_b = None if typ in ("PLAT", "ROND", "TUBE-ROND", "BORDURE") else ("haut" if typ == "T" else "bas")
    z_cote_b = h + off if cote_b == "haut" else -off
    if typ in ("TOLE", "TREILLIS"):  # pièces à plat : cotes au sol ou au niveau des fils
        off = b * 0.12
        cible = Vector((0, L0 * MM * 0.5, 0))
    points_cadrage = list(boite_pts)
    if mode == "caracteristiques" and typ == "TREILLIS":
        points_cadrage += [((-b / 2 - off * 1.6) * MM, 0, 0), ((-b / 2 - off * 1.6) * MM, L0 * MM, 0),
                           (-b / 2 * MM, -off * 1.6 * MM, 0), (b / 2 * MM, -off * 1.6 * MM, 0)]
    if mode == "caracteristiques" and typ == "TOLE":
        points_cadrage += [((b / 2 + off * 1.6) * MM, 0, 0), ((b / 2 + off * 1.6) * MM, L0 * MM, 0),
                           (-b / 2 * MM, -off * 1.6 * MM, 0), (b / 2 * MM, -off * 1.6 * MM, 0)]
        # colonne de gauche laissée libre pour la loupe de l'épaisseur
        boite = tuple(p.get("boite", (0.25, 0.08, 0.62, 0.92)))
    elif mode == "caracteristiques" and typ == "TREILLIS":
        boite = tuple(p.get("boite", (0.07, 0.10, 0.62, 0.90)))
    elif mode == "caracteristiques":
        points_cadrage += [((-b / 2 - off * 1.6) * MM, 0, 0), ((-b / 2 - off * 1.6) * MM, 0, h * MM)]
        if cote_b:
            z = (h + off * 1.6) if cote_b == "haut" else -off * 1.6
            points_cadrage += [(-b / 2 * MM, 0, z * MM), (b / 2 * MM, 0, z * MM)]
        boite = tuple(p.get("boite", (0.07, 0.10, 0.62, 0.90)))
    else:
        boite = tuple(p.get("boite", (0.12, 0.14, 0.88, 0.86)))

    scene.render.resolution_x = p.get("largeur", 1600)
    scene.render.resolution_y = p.get("hauteur", 1200)
    scene.render.resolution_percentage = 100
    cadrer(cam, scene, points_cadrage, boite, direction, cible)

    t = cible
    lumiere_zone("cle", t + Vector((-0.3, -1.2, 2.4)), t, 2.0, p.get("e_cle", 110))
    lumiere_zone("debouchage", t + Vector((1.6, -1.4, 0.7)), t, 2.0, p.get("e_debouchage", 35))
    lumiere_zone("contre", t + Vector((0.5, 1.8, 1.3)), t, 1.2, p.get("e_contre", 70))
    lumiere_zone("dessus", t + Vector((0.0, 0.3, 2.5)), t, 2.5, p.get("e_dessus", 45))
    # lumières qui éclairent sans porter d'ombre (`lumieres_sans_ombre`, panneaux de clôture) : un panneau debout reçoit
    # la lumière « contre » par derrière et les autres par devant ; leurs ombres partaient de part et d'autre de son plan
    # et laissaient une traînée claire dans le prolongement du pied (vérification indépendante du 15/09)
    for nom_lumiere in p.get("lumieres_sans_ombre", []):
        bpy.data.objects[nom_lumiere].data.use_shadow = False
    monde_studio()

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = p.get("samples", 64)
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = p.get("seuil_adaptatif", 0.02)
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.max_bounces = p.get("rebonds", 8)
    scene.cycles.glossy_bounces = min(4, p.get("rebonds", 8))
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.render.use_persistent_data = True
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = p.get("exposition", -1.3)
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"

    sortie = os.path.expandvars(p["sortie"])
    os.makedirs(sortie, exist_ok=True)
    scene.render.filepath = os.path.join(sortie, p["slug"] + ".png")
    # motif plus fin que 4 px à l'écran (tôle perforée R5 T8 vue entière : pas de 2 à 3 px) : rendu à `surechantillonnage`
    # fois la taille puis réduction, sinon moiré et plaque « en grain de papier » (vérification du 15/09). Les points
    # des cotes restent calculés dans la taille finale (resolution_x / y).
    sur = int(p.get("surechantillonnage", 1))
    scene.render.resolution_percentage = 100 * sur
    calculer_image(p)
    scene.render.resolution_percentage = 100
    if sur > 1 and not p.get("points_seuls"):
        reduire_image(scene.render.filepath, scene.render.resolution_x, scene.render.resolution_y)

    if mode == "caracteristiques" and typ == "TOLE":
        W, H = scene.render.resolution_x, scene.render.resolution_y

        def ecran(x, y, z, taille=(W, H)):
            q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
            return [round(q.x * taille[0], 2), round((1 - q.y) * taille[1], 2)]

        e, L = h, L0
        # point du chant avant montré dans la loupe, côté gauche où la loupe se place (tôle perforée aléatoire :
        # déplacé sur le plein le plus proche par plaque_perforee ; tôle profilée ou panneau : point et hauteur
        # imposés par `loupe` — sommet d'une nervure, chant de l'âme)
        lp = piece.get("loupe") or {}
        x_loupe = lp.get("x", piece.get("x_loupe", -b * 0.3))
        z_loupe_haut = lp.get("z_haut", e)
        points = {
            "cote_b_gauche": ecran(-b / 2, -off, 0), "cote_b_droit": ecran(b / 2, -off, 0),
            "rappel_b_gauche_debut": ecran(-b / 2, -4, 0), "rappel_b_gauche_fin": ecran(-b / 2, -off * 1.2, 0),
            "rappel_b_droit_debut": ecran(b / 2, -4, 0), "rappel_b_droit_fin": ecran(b / 2, -off * 1.2, 0),
            # longueur le long du bord droit : le côté gauche reste libre pour la loupe
            "cote_h_bas": ecran(b / 2 + off, 0, 0), "cote_h_haut": ecran(b / 2 + off, L, 0),
            "rappel_h_bas_debut": ecran(b / 2 + 4, 0, 0), "rappel_h_bas_fin": ecran(b / 2 + off * 1.2, 0, 0),
            "rappel_h_haut_debut": ecran(b / 2 + 4, L, 0), "rappel_h_haut_fin": ecran(b / 2 + off * 1.2, L, 0),
            "loupe_ancre": ecran(x_loupe, 0, z_loupe_haut),
            # points du chant avant candidats pour relier la loupe (le chant est le même partout, sauf si la loupe
            # vise un point précis : nervure, chant de l'âme)
            "loupe_ancres": ([ecran(x_loupe, 0, z_loupe_haut)] if lp else
                             [ecran(-b * k, 0, e) for k in (0.47, 0.42, 0.36, 0.3)]),
        }
        # loupe : gros plan sur le chant avant, même orientation, champ de 10 épaisseurs (30 mm au moins) ;
        # la caméra passe à quelques centimètres de la pièce : découpe proche abaissée à 1 mm.
        # Tôle à relief : champ sur l'épaisseur au sommet du relief, centré entre l'épaisseur de base et le relief coupé
        T = p.get("taille_loupe", 700)
        relief = piece.get("relief")
        az_l, el_l = math.radians(20), math.radians(p.get("elevation_loupe", 14))
        dir_l = Vector((math.sin(az_l) * math.cos(el_l), -math.cos(az_l) * math.cos(el_l), math.sin(el_l)))
        x_centre = (x_loupe + x_relief_coupe(piece)) / 2 if relief else x_loupe
        cible_l = Vector((x_centre * MM, 0, (relief["e_total"] if relief else z_loupe_haut) / 2 * MM))
        cam.data.clip_start = 0.001
        cam.data.shift_x = cam.data.shift_y = 0.0
        champ = lp.get("champ", champ_loupe(piece))
        cam.location = cible_l + dir_l * (champ * MM * cam.data.lens / cam.data.sensor_width)
        cam.rotation_euler = (-dir_l).to_track_quat("-Z", "Y").to_euler()
        scene.render.resolution_x = scene.render.resolution_y = T
        scene.cycles.samples = min(p.get("samples", 64), 24)
        scene.render.filepath = os.path.join(sortie, p["slug"] + "-loupe.png")
        bpy.context.view_layer.update()
        calculer_image(p)
        points["loupe_haut"] = ecran(x_loupe, 0, z_loupe_haut, (T, T))
        points["loupe_bas"] = ecran(x_loupe, 0, lp.get("z_bas", 0.0), (T, T))
        if relief:  # épaisseur totale au sommet du relief coupé par le chant
            points["loupe_relief_haut"] = ecran(x_relief_coupe(piece), 0, relief["e_total"], (T, T))
            points["loupe_relief_bas"] = ecran(x_relief_coupe(piece), 0, 0, (T, T))
        ecrire_json(p, sortie, t0, {"largeur": W, "hauteur": H, "type": typ, "cote_b": "bas", "loupe": T, "points": points,
                                    "cle_loupe": lp.get("cle", "e")})
    elif mode == "caracteristiques" and typ == "TREILLIS":
        W, H = scene.render.resolution_x, scene.render.resolution_y

        def ecran(x, y, z):
            q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
            return [round(q.x * W, 2), round((1 - q.y) * H, 2)]

        d, ma, mb, nx = piece["t"], piece["maille_a"], piece["maille_b"], piece["nx"]
        x0 = x0_piece / MM  # décalage du recentrage (dépassants), en mm
        xs = [x0 + (i - (nx - 1) / 2) * mb for i in range(nx)]
        b_gauche = x0 - b / 2
        z_t = 1.45 * d  # axe des fils transversaux
        points = {
            # maille b entre les deux premiers fils longitudinaux, au sol devant la portion
            "cote_b_gauche": ecran(xs[0], -off, 0), "cote_b_droit": ecran(xs[1], -off, 0),
            "rappel_b_gauche_debut": ecran(xs[0], -4, 0), "rappel_b_gauche_fin": ecran(xs[0], -off * 1.2, 0),
            "rappel_b_droit_debut": ecran(xs[1], -4, 0), "rappel_b_droit_fin": ecran(xs[1], -off * 1.2, 0),
            # maille a entre les deux premiers fils transversaux, à gauche
            "cote_h_bas": ecran(b_gauche - off, ma / 2, z_t), "cote_h_haut": ecran(b_gauche - off, ma * 1.5, z_t),
            "rappel_h_bas_debut": ecran(b_gauche - 4, ma / 2, z_t), "rappel_h_bas_fin": ecran(b_gauche - off * 1.2, ma / 2, z_t),
            "rappel_h_haut_debut": ecran(b_gauche - 4, ma * 1.5, z_t), "rappel_h_haut_fin": ecran(b_gauche - off * 1.2, ma * 1.5, z_t),
            # diamètre du fil pincé au bout du fil longitudinal de droite
            "ame_gauche": ecran(xs[-1] - d / 2, 0, d / 2), "ame_droite": ecran(xs[-1] + d / 2, 0, d / 2),
        }
        ecrire_json(p, sortie, t0, {"largeur": W, "hauteur": H, "type": typ, "cote_b": "bas", "points": points})
    elif mode == "caracteristiques":
        W, H = scene.render.resolution_x, scene.render.resolution_y

        def ecran(x, y, z):
            q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
            return [round(q.x * W, 2), round((1 - q.y) * H, 2)]

        # épaisseur pincée : âme du I et du T (au centre), paroi gauche du U, de la cornière et des tubes carrés,
        # plat entier (sur chant), paroi droite du tube rond (seul endroit où elle est verticale, à mi-hauteur)
        tw = piece.get("tw") if typ in ("I", "U") else (b if typ == "PLAT" else piece.get("t", 0.0))
        tf = piece.get("tf", 0.0)  # seuls I et U ont une cote d'aile tf
        x_ame = {"I": 0.0, "T": 0.0, "PLAT": 0.0, "TUBE-ROND": b / 2 - tw / 2, "BORDURE": b / 2 - tw / 2}.get(typ, -b / 2 + tw / 2)
        # mi-hauteur pour I, U et tube rond ; plus haut ailleurs, où l'étiquette de la cote verticale
        # (au milieu) cacherait la flèche sur les petites sections ; milieu de l'âme pour le T
        z_pince = {"I": h / 2, "U": h / 2, "TUBE-ROND": h / 2, "T": (h - piece.get("t", 0.0)) / 2}.get(typ, h * 0.7)
        # épaisseur d'aile relevée à b/2 (norme)
        x_aile = -b * 0.3 if typ == "I" else 0.0
        # lignes de rappel de la cote verticale : depuis le bord gauche, ou depuis le haut et le bas du cercle
        x_rappel = 0.0 if typ in ("ROND", "TUBE-ROND") else -b / 2
        sens = 1 if cote_b == "haut" else -1
        z_bord_b = h if cote_b == "haut" else 0.0
        g = min(4.0, off * 0.18)  # jour entre la pièce et la ligne de rappel (4 mm, moins sur les petites sections)
        points = {
            "cote_h_bas": ecran(-b / 2 - off, 0, 0),
            "cote_h_haut": ecran(-b / 2 - off, 0, h),
            "cote_b_gauche": ecran(-b / 2, 0, z_cote_b),
            "cote_b_droit": ecran(b / 2, 0, z_cote_b),
            "rappel_h_bas_debut": ecran(x_rappel - g, 0, 0),
            "rappel_h_bas_fin": ecran(-b / 2 - off * 1.2, 0, 0),
            "rappel_h_haut_debut": ecran(x_rappel - g, 0, h),
            "rappel_h_haut_fin": ecran(-b / 2 - off * 1.2, 0, h),
            "rappel_b_gauche_debut": ecran(-b / 2, 0, z_bord_b + sens * g),
            "rappel_b_gauche_fin": ecran(-b / 2, 0, z_bord_b + sens * off * 1.2),
            "rappel_b_droit_debut": ecran(b / 2, 0, z_bord_b + sens * g),
            "rappel_b_droit_fin": ecran(b / 2, 0, z_bord_b + sens * off * 1.2),
            "ame_gauche": ecran(x_ame - tw / 2, 0, z_pince),
            "ame_droite": ecran(x_ame + tw / 2, 0, z_pince),
            "aile_haut_ext": ecran(x_aile, 0, h),
            "aile_haut_int": ecran(x_aile, 0, h - tf),
        }
        ecrire_json(p, sortie, t0, {"largeur": W, "hauteur": H, "type": typ, "cote_b": cote_b, "points": points})
    else:  # composition de la photo studio, reprise dans le texte alternatif sur le site
        ecrire_json(p, sortie, t0, {"largeur": scene.render.resolution_x, "hauteur": scene.render.resolution_y,
                                    "mode": "studio", "pieces": [{"type": q["type"], "h": q["h"], "b": q["b"]} for q in pieces]})
    print(f"{'POINTS' if p.get('points_seuls') else 'RENDU'} OK {p['slug']} ({mode}) en {time.time() - t0:.1f} s", flush=True)


def reduire_image(chemin, largeur, hauteur):
    """Réduit le PNG rendu à `largeur` × `hauteur` par moyenne de blocs entiers de pixels (filtre boîte). `Image.scale`
    de Blender ne moyenne pas assez : le moiré des tôles perforées R5 T8 restait visible à 100 % (15/09)."""
    import numpy as np
    img = bpy.data.images.load(chemin)
    w, h = img.size
    k = w // largeur
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:hauteur * k, :largeur * k]
    a = px[..., 3:4]
    couleur = (px[..., :3] * a).reshape(hauteur, k, largeur, k, 3).mean(axis=(1, 3))  # couleur prémultipliée
    alpha = a.reshape(hauteur, k, largeur, k, 1).mean(axis=(1, 3))
    couleur = np.where(alpha > 1e-6, couleur / np.maximum(alpha, 1e-6), 0.0)
    sortie = bpy.data.images.new("reduite", largeur, hauteur, alpha=True)
    sortie.pixels.foreach_set(np.concatenate([couleur, alpha], axis=2).astype(np.float32).ravel())
    sortie.filepath_raw = chemin
    sortie.file_format = "PNG"
    sortie.save()
    bpy.data.images.remove(img)
    bpy.data.images.remove(sortie)


def calculer_image(p):
    """Rendu Cycles, sauf en mode « points_seuls » : cadrage et coordonnées des cotes recalculés sans image, pour
    rhabiller après un correctif qui ne touche pas la pièce (ex. jour des lignes de rappel). Même caméra : le
    cadrage ne dépend que de la géométrie."""
    if not p.get("points_seuls"):
        bpy.ops.render.render(write_still=True)


def ecrire_json(p, sortie, t0, donnees):
    """<slug>.json : données d'habillage + empreinte du code ; en mode points seuls, garde la durée du vrai rendu."""
    chemin = os.path.join(sortie, p["slug"] + ".json")
    duree = round(time.time() - t0, 1)
    if p.get("points_seuls") and os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            duree = json.load(f).get("duree_s", duree)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump({**donnees, "duree_s": duree, "code": EMPREINTE, "points_seuls": bool(p.get("points_seuls"))}, f, indent=2)


def main():
    params = lire_params()
    for p in (params if isinstance(params, list) else [params]):
        rendre(p)


main()
