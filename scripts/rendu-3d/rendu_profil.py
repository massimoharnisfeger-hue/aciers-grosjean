"""
Rendu Blender d'un profilé acier à partir de ses cotes.

Usage :
  blender -b --factory-startup -P rendu_profil.py -- params.json

params.json :
  {"slug": "...", "type": "I", "h": 200, "b": 100, "tw": 5.6, "tf": 8.5, "r": 12,
   "longueur": 700, "sortie": "dossier", "samples": 96, "largeur": 1600, "hauteur": 1200}

Produit <sortie>/<slug>.png (fond transparent + ombre) et <slug>.json
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


def p_mat(cle, defaut):
    """Réglage matière surchargeable depuis params.json."""
    return PARAMS.get(cle, defaut)


def lire_params():
    argv = sys.argv
    chemin = argv[argv.index("--") + 1]
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- géométrie

def arc(cx, cz, r, a0, a1, n):
    """Points d'un arc (degrés), extrémités comprises."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return pts


def section_i(h, b, tw, tf, r, n=10):
    """Section en I (IPE, HEA, HEB) : ailes parallèles, 4 congés de raccordement."""
    x = tw / 2
    p = [(-b / 2, 0), (b / 2, 0), (b / 2, tf)]
    p += arc(x + r, tf + r, r, 270, 180, n)
    p += arc(x + r, h - tf - r, r, 180, 90, n)
    p += [(b / 2, h - tf), (b / 2, h), (-b / 2, h), (-b / 2, h - tf)]
    p += arc(-x - r, h - tf - r, r, 90, 0, n)
    p += arc(-x - r, tf + r, r, 0, -90, n)
    p += [(-b / 2, tf)]
    propre = []
    for q in p:
        if not propre or (abs(q[0] - propre[-1][0]) > 1e-9 or abs(q[1] - propre[-1][1]) > 1e-9):
            propre.append(q)
    return propre


def extruder(section_mm, longueur_mm, nom):
    me = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    verts = [bm.verts.new((x * MM, 0.0, z * MM)) for x, z in section_mm]
    face = bm.faces.new(verts)
    res = bmesh.ops.extrude_face_region(bm, geom=[face])
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


# ---------------------------------------------------------------- matériaux

def noeud(nt, type_, loc, **inputs):
    n = nt.nodes.new(type_)
    n.location = loc
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def materiau_calamine():
    """Acier laminé à chaud : calamine gris bleuté, satinée, marbrée."""
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


# ---------------------------------------------------------------- scène

def vider_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


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


def main():
    p = lire_params()
    PARAMS.update(p)
    t0 = time.time()
    vider_scene()
    scene = bpy.context.scene

    h, b = p["h"], p["b"]
    L = p.get("longueur", 500)
    sec = section_i(h, b, p["tw"], p["tf"], p["r"])
    obj = extruder(sec, L, p["slug"])
    obj.data.materials.append(materiau_calamine())
    obj.data.materials.append(materiau_coupe())

    # sol attrape-ombre
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    sol = bpy.context.active_object
    sol.is_shadow_catcher = True

    # caméra : trois-quarts avant gauche, légère plongée, focale produit
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = p.get("focale", 50)
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam

    # caméra côté +X : la section apparaît à gauche, le corps file vers la droite
    az, el = math.radians(p.get("azimut", 20)), math.radians(p.get("elevation", 17))
    direction = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cible = Vector((0, L * MM * 0.35, h * MM * 0.5))
    cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()

    off = max(h, b) * 0.28  # écart des lignes de cote, en mm
    points_cadrage = [
        (x * MM, y * MM, z * MM)
        for x in (-b / 2, b / 2) for y in (0, L) for z in (0, h)
    ] + [
        ((-b / 2 - off * 1.6) * MM, 0, 0), ((-b / 2 - off * 1.6) * MM, 0, h * MM),
        (-b / 2 * MM, 0, -off * 1.6 * MM), (b / 2 * MM, 0, -off * 1.6 * MM),
    ]

    scene.render.resolution_x = p.get("largeur", 1600)
    scene.render.resolution_y = p.get("hauteur", 1200)
    scene.render.resolution_percentage = 100
    boite = tuple(p.get("boite", (0.07, 0.10, 0.62, 0.90)))
    cadrer(cam, scene, points_cadrage, boite, direction, cible)

    # éclairage studio : boîte à lumière principale, débouchage, contre-jour, dessus
    t = cible
    lumiere_zone("cle", t + Vector((-0.3, -1.2, 2.4)), t, 2.0, p.get("e_cle", 110))
    lumiere_zone("debouchage", t + Vector((1.6, -1.4, 0.7)), t, 2.0, p.get("e_debouchage", 35))
    lumiere_zone("contre", t + Vector((0.5, 1.8, 1.3)), t, 1.2, p.get("e_contre", 70))
    lumiere_zone("dessus", t + Vector((0.0, 0.3, 2.5)), t, 2.5, p.get("e_dessus", 45))
    monde_studio()

    # rendu
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = p.get("samples", 96)
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.max_bounces = 8
    scene.cycles.glossy_bounces = 4
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
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

    # points écran pour l'habillage (pixels, origine en haut à gauche)
    W, H = scene.render.resolution_x, scene.render.resolution_y

    def ecran(x, y, z):
        q = world_to_camera_view(scene, cam, Vector((x * MM, y * MM, z * MM)))
        return [round(q.x * W, 2), round((1 - q.y) * H, 2)]

    tw, tf = p["tw"], p["tf"]
    points = {
        "cote_h_bas": ecran(-b / 2 - off, 0, 0),
        "cote_h_haut": ecran(-b / 2 - off, 0, h),
        "cote_b_gauche": ecran(-b / 2, 0, -off),
        "cote_b_droit": ecran(b / 2, 0, -off),
        "rappel_h_bas_debut": ecran(-b / 2 - 4, 0, 0),
        "rappel_h_bas_fin": ecran(-b / 2 - off * 1.2, 0, 0),
        "rappel_h_haut_debut": ecran(-b / 2 - 4, 0, h),
        "rappel_h_haut_fin": ecran(-b / 2 - off * 1.2, 0, h),
        "rappel_b_gauche_debut": ecran(-b / 2, 0, -4),
        "rappel_b_gauche_fin": ecran(-b / 2, 0, -off * 1.2),
        "rappel_b_droit_debut": ecran(b / 2, 0, -4),
        "rappel_b_droit_fin": ecran(b / 2, 0, -off * 1.2),
        "ame_gauche": ecran(-tw / 2, 0, h * 0.5),
        "ame_droite": ecran(tw / 2, 0, h * 0.5),
        "aile_haut_ext": ecran(-b * 0.3, 0, h),
        "aile_haut_int": ecran(-b * 0.3, 0, h - tf),
    }
    with open(os.path.join(sortie, p["slug"] + ".json"), "w", encoding="utf-8") as f:
        json.dump({"largeur": W, "hauteur": H, "points": points,
                   "duree_s": round(time.time() - t0, 1)}, f, indent=2)
    print(f"RENDU OK {p['slug']} en {time.time() - t0:.1f} s")


main()
