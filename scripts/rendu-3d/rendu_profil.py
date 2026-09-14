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

import json
import math
import os
import sys
import time

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

MM = 0.001
PARAMS = {}

# Teintes (sRGB 0-255) calées sur les vraies photos du site actuel ; converties en linéaire pour Cycles.
TEINTE_GPP = PARAMS.get("teinte_gpp", (122, 52, 40))


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


def section_u(h, b, tw, tf, r1, r2, pente=8.0, n=10):
    """Section en U à ailes inclinées (UPN, DIN 1026-1) : épaisseur d'aile tf mesurée à b/2,
    faces intérieures inclinées de `pente` %, congé r1 à la racine, arrondi r2 au bout d'aile.
    Âme à gauche, ouverture vers +x ; centrée en x."""
    k = pente / 100.0
    t_bout = tf - (b / 2) * k          # épaisseur au bout de l'aile (x = b)
    t_racine = tf + (b / 2 - tw) * k   # épaisseur contre l'âme (x = tw)
    coins = [(0, 0), (b, 0), (b, t_bout), (tw, t_racine), (tw, h - t_racine), (b, h - t_bout), (b, h), (0, h)]
    rayons = [0, 0, r2, r1, r1, r2, 0, 0]
    p = []
    for i, c in enumerate(coins):
        p += coin_arrondi(coins[i - 1], c, coins[(i + 1) % len(coins)], rayons[i], n)
    return dedoublonner([(x - b / 2, z) for x, z in p])


def section_l(h, b, t, r1, r2, n=10):
    """Cornière (EN 10056) : aile verticale de hauteur h à gauche, aile horizontale de largeur b en bas,
    épaisseur t, congé r1 à la racine intérieure, arrondi r2 au bout intérieur de chaque aile ; talon vif. Centrée en x."""
    coins = [(0, 0), (b, 0), (b, t), (t, t), (t, h), (0, h)]
    rayons = [0, 0, r2, r1, r2, 0]
    p = []
    for i, c in enumerate(coins):
        p += coin_arrondi(coins[i - 1], c, coins[(i + 1) % len(coins)], rayons[i], n)
    return dedoublonner([(x - b / 2, z) for x, z in p])


def section_t(h, b, t, r, r1, r2, n=10):
    """Fer T (EN 10055) : aile en haut (largeur b), âme en bas, même épaisseur t ; congés r à la racine,
    arrondis r1 au bout des ailes et r2 au bout de l'âme ; faces parallèles. Centrée en x, bout de l'âme en z = 0."""
    coins = [(-t / 2, 0), (t / 2, 0), (t / 2, h - t), (b / 2, h - t), (b / 2, h), (-b / 2, h), (-b / 2, h - t), (-t / 2, h - t)]
    rayons = [r2, r2, r, r1, 0, 0, r1, r]
    p = []
    for i, c in enumerate(coins):
        p += coin_arrondi(coins[i - 1], c, coins[(i + 1) % len(coins)], rayons[i], n)
    return dedoublonner(p)


def section_rectangle(h, b):
    """Plat posé sur chant (hauteur h = largeur du plat, épaisseur b) ou carré plein ; arêtes vives (chanfrein du modèle)."""
    return [(-b / 2, 0), (b / 2, 0), (b / 2, h), (-b / 2, h)]


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


def section_de(piece):
    t = piece["type"]
    if t == "TOLE":  # plaque posée à plat : section largeur × épaisseur, extrudée sur la longueur
        return section_rectangle(piece["h"], piece["b"])
    if t == "T":
        return section_t(piece["h"], piece["b"], piece["t"], piece["r"], piece["r1"], piece["r2"])
    if t in ("PLAT", "CARRE"):
        return section_rectangle(piece["h"], piece["b"])
    if t == "ROND":
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


MATIERES = {"BRUT": materiau_calamine, "GPP": materiau_gpp}


# ---------------------------------------------------------------- scène

def vider_scene():
    for collection in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.lights,
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
        if i:
            x += p.get("ecart_studio", 0.9) * piece["h"]
        dx = x + piece["b"] / 2
        obj = extruder(section_de(piece), L, f"{p['slug']}-{i}", decalage_x=dx)
        obj.data.materials.append(mat_surface)
        obj.data.materials.append(mat_coupe)
        boite_pts += [((dx + sx * piece["b"] / 2) * MM, y * MM, z * MM)
                      for sx in (-1, 1) for y in (0, L) for z in (0, piece["h"])]
        x += piece["b"]
    centre_x = sum(q[0] for q in boite_pts) / len(boite_pts)
    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        obj.location.x -= centre_x
    boite_pts = [(q[0] - centre_x, q[1], q[2]) for q in boite_pts]

    # sol attrape-ombre
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    bpy.context.active_object.is_shadow_catcher = True

    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = p.get("focale", 50)
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
    # cote horizontale : sous la pièce, au-dessus pour le T (largeur de l'aile), aucune pour plat, rond et tube rond
    cote_b = None if typ in ("PLAT", "ROND", "TUBE-ROND") else ("haut" if typ == "T" else "bas")
    z_cote_b = h + off if cote_b == "haut" else -off
    if typ == "TOLE":  # tôle posée à plat : cotes au sol, largeur devant, longueur à gauche, épaisseur en loupe
        off = b * 0.12
        cible = Vector((0, L0 * MM * 0.5, 0))
    points_cadrage = list(boite_pts)
    if mode == "caracteristiques" and typ == "TOLE":
        points_cadrage += [((b / 2 + off * 1.6) * MM, 0, 0), ((b / 2 + off * 1.6) * MM, L0 * MM, 0),
                           (-b / 2 * MM, -off * 1.6 * MM, 0), (b / 2 * MM, -off * 1.6 * MM, 0)]
        # colonne de gauche laissée libre pour la loupe de l'épaisseur
        boite = tuple(p.get("boite", (0.25, 0.08, 0.62, 0.92)))
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
    bpy.ops.render.render(write_still=True)

    if mode == "caracteristiques" and typ == "TOLE":
        W, H = scene.render.resolution_x, scene.render.resolution_y

        def ecran(x, y, z, taille=(W, H)):
            q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
            return [round(q.x * taille[0], 2), round((1 - q.y) * taille[1], 2)]

        e, L = h, L0
        x_loupe = -b * 0.3  # point du chant avant montré dans la loupe, côté gauche où la loupe se place
        points = {
            "cote_b_gauche": ecran(-b / 2, -off, 0), "cote_b_droit": ecran(b / 2, -off, 0),
            "rappel_b_gauche_debut": ecran(-b / 2, -4, 0), "rappel_b_gauche_fin": ecran(-b / 2, -off * 1.2, 0),
            "rappel_b_droit_debut": ecran(b / 2, -4, 0), "rappel_b_droit_fin": ecran(b / 2, -off * 1.2, 0),
            # longueur le long du bord droit : le côté gauche reste libre pour la loupe
            "cote_h_bas": ecran(b / 2 + off, 0, 0), "cote_h_haut": ecran(b / 2 + off, L, 0),
            "rappel_h_bas_debut": ecran(b / 2 + 4, 0, 0), "rappel_h_bas_fin": ecran(b / 2 + off * 1.2, 0, 0),
            "rappel_h_haut_debut": ecran(b / 2 + 4, L, 0), "rappel_h_haut_fin": ecran(b / 2 + off * 1.2, L, 0),
            "loupe_ancre": ecran(x_loupe, 0, e),
            # points du chant avant candidats pour relier la loupe (le chant est le même partout)
            "loupe_ancres": [ecran(-b * k, 0, e) for k in (0.47, 0.42, 0.36, 0.3)],
        }
        # loupe : gros plan sur le chant avant, même orientation, champ de 10 épaisseurs (30 mm au moins) ;
        # la caméra passe à quelques centimètres de la pièce : découpe proche abaissée à 1 mm
        T = p.get("taille_loupe", 700)
        az_l, el_l = math.radians(20), math.radians(p.get("elevation_loupe", 14))
        dir_l = Vector((math.sin(az_l) * math.cos(el_l), -math.cos(az_l) * math.cos(el_l), math.sin(el_l)))
        cible_l = Vector((x_loupe * MM, 0, e / 2 * MM))
        cam.data.clip_start = 0.001
        cam.data.shift_x = cam.data.shift_y = 0.0
        cam.location = cible_l + dir_l * (max(10 * e, 30.0) * MM * cam.data.lens / cam.data.sensor_width)
        cam.rotation_euler = (-dir_l).to_track_quat("-Z", "Y").to_euler()
        scene.render.resolution_x = scene.render.resolution_y = T
        scene.cycles.samples = min(p.get("samples", 64), 24)
        scene.render.filepath = os.path.join(sortie, p["slug"] + "-loupe.png")
        bpy.context.view_layer.update()
        bpy.ops.render.render(write_still=True)
        points["loupe_haut"] = ecran(x_loupe, 0, e, (T, T))
        points["loupe_bas"] = ecran(x_loupe, 0, 0, (T, T))
        with open(os.path.join(sortie, p["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump({"largeur": W, "hauteur": H, "type": typ, "cote_b": "bas", "loupe": T, "points": points,
                       "duree_s": round(time.time() - t0, 1)}, f, indent=2)
    elif mode == "caracteristiques":
        W, H = scene.render.resolution_x, scene.render.resolution_y

        def ecran(x, y, z):
            q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
            return [round(q.x * W, 2), round((1 - q.y) * H, 2)]

        # épaisseur pincée : âme du I et du T (au centre), paroi gauche du U, de la cornière et des tubes carrés,
        # plat entier (sur chant), paroi droite du tube rond (seul endroit où elle est verticale, à mi-hauteur)
        tw = piece.get("tw") if typ in ("I", "U") else (b if typ == "PLAT" else piece.get("t", 0.0))
        tf = piece.get("tf", 0.0)  # seuls I et U ont une cote d'aile tf
        x_ame = {"I": 0.0, "T": 0.0, "PLAT": 0.0, "TUBE-ROND": b / 2 - tw / 2}.get(typ, -b / 2 + tw / 2)
        # mi-hauteur pour I, U et tube rond ; plus haut ailleurs, où l'étiquette de la cote verticale
        # (au milieu) cacherait la flèche sur les petites sections ; milieu de l'âme pour le T
        z_pince = {"I": h / 2, "U": h / 2, "TUBE-ROND": h / 2, "T": (h - piece.get("t", 0.0)) / 2}.get(typ, h * 0.7)
        # épaisseur d'aile relevée à b/2 (norme)
        x_aile = -b * 0.3 if typ == "I" else 0.0
        # lignes de rappel de la cote verticale : depuis le bord gauche, ou depuis le haut et le bas du cercle
        x_rappel = 0.0 if typ in ("ROND", "TUBE-ROND") else -b / 2
        sens = 1 if cote_b == "haut" else -1
        z_bord_b = h if cote_b == "haut" else 0.0
        points = {
            "cote_h_bas": ecran(-b / 2 - off, 0, 0),
            "cote_h_haut": ecran(-b / 2 - off, 0, h),
            "cote_b_gauche": ecran(-b / 2, 0, z_cote_b),
            "cote_b_droit": ecran(b / 2, 0, z_cote_b),
            "rappel_h_bas_debut": ecran(x_rappel - 4, 0, 0),
            "rappel_h_bas_fin": ecran(-b / 2 - off * 1.2, 0, 0),
            "rappel_h_haut_debut": ecran(x_rappel - 4, 0, h),
            "rappel_h_haut_fin": ecran(-b / 2 - off * 1.2, 0, h),
            "rappel_b_gauche_debut": ecran(-b / 2, 0, z_bord_b + sens * 4),
            "rappel_b_gauche_fin": ecran(-b / 2, 0, z_bord_b + sens * off * 1.2),
            "rappel_b_droit_debut": ecran(b / 2, 0, z_bord_b + sens * 4),
            "rappel_b_droit_fin": ecran(b / 2, 0, z_bord_b + sens * off * 1.2),
            "ame_gauche": ecran(x_ame - tw / 2, 0, z_pince),
            "ame_droite": ecran(x_ame + tw / 2, 0, z_pince),
            "aile_haut_ext": ecran(x_aile, 0, h),
            "aile_haut_int": ecran(x_aile, 0, h - tf),
        }
        with open(os.path.join(sortie, p["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump({"largeur": W, "hauteur": H, "type": typ, "cote_b": cote_b, "points": points,
                       "duree_s": round(time.time() - t0, 1)}, f, indent=2)
    else:  # composition de la photo studio, reprise dans le texte alternatif sur le site
        with open(os.path.join(sortie, p["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump({"largeur": scene.render.resolution_x, "hauteur": scene.render.resolution_y, "mode": "studio",
                       "pieces": [{"type": q["type"], "h": q["h"], "b": q["b"]} for q in pieces],
                       "duree_s": round(time.time() - t0, 1)}, f, indent=2)
    print(f"RENDU OK {p['slug']} ({mode}) en {time.time() - t0:.1f} s", flush=True)


def main():
    params = lire_params()
    for p in (params if isinstance(params, list) else [params]):
        rendre(p)


main()
