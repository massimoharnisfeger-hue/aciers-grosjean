"""
Prepare la liste de parametres Blender (rendu_profil.py) a partir des donnees sourcees.

  python scripts/rendu-3d/preparer_rendus.py <sortie.json> car <slug> [<slug> ...]
  python scripts/rendu-3d/preparer_rendus.py <sortie.json> studio <nom> <slug> [<slug> ...]
Options (avant les commandes) : --samples N  --seuil X  --ajouter (complete le fichier au lieu de l'ecraser)
  --essai LARGEUR : image reduite (hauteur = 3/4) rangee dans rendu3d/essais/, jamais dans final/
  --points-seuls : sans rendu, recalcule seulement <slug>.json (cotes) des images deja rendues dans final/

Les cotes viennent de scripts/rendu-3d/donnees/produits.json ; la finition « supposee » n'est utilisee
que pour la matiere du rendu, jamais affichee.
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
# mesuree sur la vraie photo du stock IPE GPP (site actuel, image 0003805 : mediane 130/83/78, moyenne 144/85/66),
# assombrie apres un premier essai qui sortait plus orange que la photo
TEINTE_GPP = [135, 66, 50]
# panneau de clôture debout : les lumières « contre » (derrière) et « dessus » (un peu derrière) éclairent sans ombre ;
# leurs ombres, portées devant le plan du panneau pendant que les autres la portent derrière, laissaient une traînée claire
# dans le prolongement du pied (vérification du 15/09 ; essai : alpha du sol 25 → 5 → 18 à travers la traînée, 28 → 3 → 0
# sans ces deux ombres)
SANS_TRAINEE = {"lumieres_sans_ombre": ["contre", "dessus"]}
# Longueur des pièces (ADR-0011, vues validées le 14/09 et gardées) : fiche = tronçon de 6,25 × la plus grande cote
# (RATIO_CADRE, plafond 500 mm) vu en entier ; studio = 7 × la plus grande section (plafond 900 mm). Le 23/09, une barre
# 4 × plus longue qui sortait du cadre et un studio à 18 × avaient changé la vue ; le propriétaire, le 24/09 : « je veux
# vraiment avoir l'entièreté de la pièce », « les mêmes vues ». Seule la finition change (chanfrein, coupe, rayons).
RATIO_CADRE = 6.25
BARRES = {"PLAT", "CARRE", "ROND", "ROND-BETON", "L", "T", "TC", "TR", "TUBE-ROND", "I", "U"}
RATIO_STUDIO = 7


def piece(p, longueur, ratio):
    """Pièce pour rendu_profil.py. Tronçon proportionné à la section (ratio × plus grande cote, plafonné à
    `longueur`) : une petite cornière reste lisible ; les poutrelles (cote ≥ 80 mm) gardent 500 mm."""
    v = {k: d["valeur"] for k, d in p["valeurs"].items()}
    serie = v.get("serie")
    if serie == "L":
        out = {"type": "L", "h": v["a"], "b": v["b"], "t": v["t"], "r1": v["r1"], "r2": v["r2"]}
    elif serie == "T":
        out = {"type": "T", "h": v["h"], "b": v["b"], "t": v["t"], "r": v["r"], "r1": v["r1"], "r2": v["r2"]}
    elif serie == "PLAT":  # posé sur chant : la largeur du plat est la hauteur de la section
        out = {"type": "PLAT", "h": v["b"], "b": v["t"]}
    elif serie == "ROND":
        out = {"type": "ROND", "h": v["d"], "b": v["d"]}
    elif serie == "CARRE":
        out = {"type": "CARRE", "h": v["a"], "b": v["a"]}
    elif serie in ("TC", "TR"):
        out = {"type": serie, "h": v["h"], "b": v["b"], "t": v["t"], "r1": v["r1"]}
    elif serie == "TUBE-ROND":
        out = {"type": "TUBE-ROND", "h": v["d"], "b": v["d"], "t": v["t"]}
    elif serie == "TOLE":  # plaque à plat : largeur × épaisseur, extrudée sur toute la longueur du format
        return {"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"]}, v.get("finition", "BRUT")
    elif serie == "BORDURE":  # bande pliée debout : face de hauteur h, pli en tête ; largeur = profondeur du pli + tôle
        import math
        prof = round(v["pli"] * math.sin(math.radians(v["angle"])) + v["e"], 2)
        out = {"type": "BORDURE", "h": v["h"], "b": prof, "t": v["e"], "pli": v["pli"], "angle": v["angle"]}
    elif serie == "TOLE-PROFILEE":  # tôle nervurée à plat ; loupe sur la 2e nervure (hauteur h pincée)
        # axes des nervures extrêmes à l_utile, bords coupés à mi-flanc (cotes 1000 / 1050 de la fiche) ; l'ancien modèle
        # partait d'un plat de 5 mm et coupait la dernière nervure (dissymétrique, spécification des formes du 16/09)
        marge = (v["l"] - v["l_utile"]) / 2
        x_nervure = -v["l"] / 2 + marge + v["pas"]
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"],
                 "profil": {"motif": "NERVURES", "pas": v["pas"], "h": v["h"], "sommet": v["sommet"], "base": v["base"],
                            "l_utile": v["l_utile"], "raidisseurs": v.get("raidisseurs")},
                 "loupe": {"x": x_nervure, "z_haut": v["h"], "z_bas": 0.0, "champ": max(6 * v["h"], 30.0), "cle": "h"}},
                v.get("finition", "BRUT"))
    elif serie == "TASSEAU":  # bardage à caissons ; loupe sur le 2e tasseau (hauteur d'onde h pincée)
        base = v["sommet"] + 6.0
        n = int((v["l_utile"] - base) / v["pas"]) + 1
        marge = (v["l_utile"] - (n - 1) * v["pas"] - base) / 2
        x_tasseau = -v["l_utile"] / 2 + marge + base / 2 + v["pas"]
        return ({"type": "TOLE", "h": v["e"], "b": v["l_utile"], "longueur": v["L"],
                 "profil": {"motif": "TASSEAU", "h": v["h"], "sommet": v["sommet"], "pas": v["pas"]},
                 "loupe": {"x": x_tasseau, "z_haut": v["h"], "z_bas": 0.0, "champ": max(6 * v["h"], 30.0), "cle": "h"}},
                v.get("finition", "BRUT"))
    elif serie == "PANNEAU-ISOLE":  # sandwich : mousse dans le panneau et les nervures 1 à 3, feuille d'alu dessous
        # repère u de la section : u = 0 sur l'axe de la nervure 1 ; la forme va du pied gauche de la nervure 1 au bout de
        # la lèvre (rendu_profil.panneau_isole), centrée sur son milieu u_m. Loupe : épaisseur e pincée sur la plage à
        # u = 275, champ centré à u = 300 et à la hauteur de la plage (nervure 2 pleine de mousse, petite nervure,
        # feuille d'aluminium) ; l'ancienne loupe ne montrait qu'une plaque de mousse plate
        B, S, H, lu = v["base"], v["sommet"], v["h_nervure"], v["l_utile"]
        pas_u = lu / (v["nervures"] - 1)
        u_m = (-B / 2 + (v["nervures"] - 1) * pas_u + S / 2 + (H - v["levre_h"]) / H * (B - S) / 2) / 2
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"],
                 "sandwich": {"l_utile": lu, "nervures": v["nervures"], "h_nervure": H, "sommet": S, "base": B,
                              "e_tole": v["e_tole"], "raidisseurs": v["raidisseurs"], "levre_h": v["levre_h"],
                              "e_alu": v["e_alu"]},
                 "loupe": {"x": round(pas_u - B / 2 - 21.8 - u_m, 2), "x_centre": round(pas_u - 33.3 - u_m, 2),
                           "z_centre": v["e"], "z_haut": v["e"], "z_bas": 0.0, "champ": max(6 * v["e"], 30.0), "cle": "e"}},
                v.get("finition", "BRUT"))
    elif serie == "MARCHE-CAILLEBOTIS":  # marche pressée : flasques qui pendent sous la grille, nez en cornière percée
        # (vérification indépendante du 15/09 : joues dressées au-dessus de la marche, nez percé sur la face verticale).
        # h = hauteur totale (dessus de grille -> bas des flasques) : cadrage ; barreau porteur dans `h_barreau`.
        # Loupe sur le coin avant gauche, vue de l'extérieur : flasque (trou, fente), nez ; rien n'est coté (h supposée)
        H = v["h_joue"]
        return ({"type": "TOLE", "h": H, "b": v["L"], "longueur": v["l"],
                 "caillebotis": {"marche": True, "t": v["t"], "h_barreau": v["h"], "maille_a": v["maille_a"],
                                 "maille_b": v["maille_b"], "h_entretoise": v["h_entretoise"],
                                 "joue": {"e": v["e_joue"], "chanfrein": 35.0, "d_trou": 13.0, "u_trou": 30.0,
                                          "entraxe_fente": 40.0, "recul_fente": 80.0, "v_trous": 15.0},
                                 "nez": {"largeur": 33.0, "hauteur": v["h_nez"], "e": 3.0, "r": 4.0, "d_trou": 8.0,
                                         "larg_col": 3.0, "h_col": 2.0, "pas": 42.0, "rangs": [15.0, 22.0]}},
                 "loupe": {"x": -v["L"] / 2, "z_haut": H, "z_bas": 0.0, "champ": 4.5 * H, "cle": "h",
                           "azimut": -35.0, "elevation": 24.0, "y": 0.2 * v["l"], "z_ancre": 0.0}},
                v.get("finition", "GALVA"))
    elif serie == "MARCHE-O2":  # tôle pliée : dessus percé en damier, bords avant/arrière enroulés, joues percées
        # (vérification du 15/09 : bords à angle vif, joues à deux trous). Loupe sur le coin avant gauche vu de
        # l'extérieur : nez arrondi, rouleau dans l'encoche, joue ; h supposée, rien n'est coté
        return ({"type": "TOLE", "h": v["h"], "b": v["L"], "longueur": v["l"],
                 "o2": {"marche": True, "t": v["t"], "trous": v["trous"], "drainage": v["drainage"], "entraxe": 25.0,
                        "r_nez": 5.0, "d_roule": v["d_roule"], "encoche": 12.0, "marge_bout": 37.5, "r_bout": 3.0,
                        "joue": {"d_trou": 13.0, "u_trou": 50.0, "v_trous": 15.0, "largeur_fente": 13.0,
                                 "entraxe_fente": 17.0, "ecart_fente": 142.0}},
                 "loupe": {"x": -v["L"] / 2, "z_haut": v["h"], "z_bas": 0.0, "champ": 4.5 * v["h"], "cle": "h",
                           "azimut": -35.0, "elevation": 24.0, "y": 0.2 * v["l"], "z_ancre": 0.0}},
                v.get("finition", "GALVA"))
    elif serie == "PLANCHER-O2":  # planches jointives percées, âmes pliées dos à dos, barres d'about pleines
        # loupe : hauteur h pincée sur la barre d'about avant ; trait de liaison tiré du bas du chant (hors de la pièce) ;
        # vue à 24° au lieu de 14 : les trous emboutis se lisaient comme des plots pleins (vérification du 15/09)
        return ({"type": "TOLE", "h": v["h"], "b": v["l"], "longueur": v["L"],
                 "o2": {"marche": False, "t": v["t"], "trous": v["trous"], "drainage": v["drainage"], "entraxe": 25.0,
                        "largeur_planche": v["largeur_planche"], "e_about": 3.0},
                 "loupe": {"x": -v["l"] * 0.3, "z_haut": v["h"], "z_bas": 0.0, "champ": max(6 * v["h"], 30.0), "cle": "h",
                           "elevation": 24.0, "z_ancre": 0.0}},
                v.get("finition", "GALVA"))
    elif serie in ("CAILLEBOTIS", "MARCHE-CAILLEBOTIS"):  # à plat comme une tôle ; loupe : hauteur h du plat de rive
        marche = serie == "MARCHE-CAILLEBOTIS"
        largeur, longueur = (v["L"], v["l"]) if marche else (v["l"], v["L"])  # marche : le grand côté devant
        return ({"type": "TOLE", "h": v["h"], "b": largeur, "longueur": longueur,
                 "caillebotis": {"t": v["t"], "maille_a": v["maille_a"], "maille_b": v["maille_b"], "marche": marche},
                 "loupe": {"x": -largeur * 0.3, "z_haut": v["h"], "z_bas": 0.0, "champ": max(6 * v["h"], 30.0), "cle": "h"}},
                v.get("finition", "GALVA"))
    elif serie == "PANNEAU-CLOTURE":  # panneau debout : hauteur H (m → mm), largeur l ; profondeur = V du pli + fil du sommet
        # maille verticale « type 205 » : l'ancien modèle lisait la maille tournée de 90° (vérification du 15/09)
        if not v["axe_v"] < v["axe_h"]:
            raise SystemExit(f"panneau : fils verticaux ({v['axe_v']}) moins serrés que les horizontaux ({v['axe_h']})")
        if len(v["travees"]) + 1 != v["plis"]:
            raise SystemExit(f"panneau : {v['plis']} plis mais {len(v['travees']) + 1} dans les travées {v['travees']}")
        return ({"type": "PANNEAU-CLOTURE", "h": round(v["H"] * 1000), "b": v["l"],
                 "longueur": v["prof_pli"] + (v["fil_h"] + v["fil_v"]) / 2 + v["fil_h"] / 2,
                 "cloture": {k: v[k] for k in ("fil_h", "fil_v", "axe_v", "axe_h", "h_pli", "prof_pli", "droit_pli",
                                               "travees", "abouts", "n_fils_v")}},
                v.get("finition", "LAQUE"))
    elif serie == "POTEAU" and v["modele"] == "CLOGRIFF 64":  # traverse à crochets encochés, âme double, lentille
        # (vérification indépendante du 15/09 : l'ancien modèle était un caisson rectangulaire à fenêtres)
        out = {"type": "POTEAU", "h": v["h"], "b": v["b"], "t": v["t_tole"],
               "poteau": {"modele": v["modele"], "pas": v["pas_encoches"], "premiere": v["premiere_encoche"],
                          "fente": v["fente"], "creneau": v["creneau"]}}
    elif serie == "POTEAU":  # couché comme un profilé : section b × h
        q = {"modele": v["modele"], "encoche": v.get("encoche"), "pas": v.get("pas_encoches")}
        t = 2.0
        if v.get("feuillure"):  # CLOPLUS 40 : profilé alu en H à deux tubes, lèvres et feuillures, âme percée (FTCP40PLIS205)
            t = v["paroi"]
            q.update(feuillure=v["feuillure"], tube=v["profondeur_tube"], levre=v["levre"], paroi=v["paroi"], ame=v["ame"],
                     conge=v["conge_ame"], trou=[v["trou_l"], v["trou_h"]], premier_trou=v["premier_trou"],
                     pas_trous=v["pas_trous"], capuchon=v.get("capuchon_e"))
        out = {"type": "POTEAU", "h": v["h"], "b": v["b"], "t": t, "r1": 3.0, "poteau": q}
    elif serie == "TOLE-PERFOREE":  # perforation : forme, cote et pas du code du nom (R/T, C/U) ou motif aléatoire
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"], "perforation": v["perforation"]},
                v.get("finition", "BRUT"))
    elif serie == "TOLE-RELIEF":  # tôle larmée ou striée : tôle de base + relief jusqu'à l'épaisseur totale
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"],
                 "relief": {"motif": v["motif"], "hauteur": round(v["e_total"] - v["e"], 3), "e_total": v["e_total"]}},
                v.get("finition", "BRUT"))
    elif serie == "ROND-BETON":
        out = {"type": "ROND-BETON", "h": v["d"], "b": v["d"]}
    elif serie == "TREILLIS":  # portion de 3 × 4 mailles, débord d'une demi-maille (le panneau entier : dans la fiche)
        nx, ny = 4, 5
        return ({"type": "TREILLIS", "h": 2.45 * v["d"], "b": nx * v["maille_b"], "t": v["d"], "maille_a": v["maille_a"],
                 "maille_b": v["maille_b"], "nx": nx, "ny": ny, "longueur": ny * v["maille_a"],
                 "depassants": bool(v.get("depassants"))},
                v.get("finition", "BRUT"))
    else:
        type_ = "U" if serie in ("UPN", "U-ALU") else "I"
        out = {"type": type_, "h": v["h"], "b": v["b"], "tw": v["tw"], "tf": v["tf"]}
        if type_ == "U":  # U alu filé : ailes parallèles (pente nulle)
            out.update({"r1": v["r1"], "r2": v["r2"], "pente": v.get("pente_aile", 0 if serie == "U-ALU" else 8)})
        else:
            out["r"] = v["r"]
    out["longueur"] = min(longueur, round(ratio * max(out["h"], out["b"])))
    arrondir_au_pas_des_trous(out)
    if out["type"] in ("TC", "TR", "TUBE-ROND"):  # section creuse : au moins 3 × la plus grande cote, sinon on voit
        # le fond à travers le tube (tube carré 250x250x6 à 500 mm, vérification indépendante du 15/09)
        out["longueur"] = max(out["longueur"], round(3 * max(out["h"], out["b"])))
    return out, v.get("finition", "BRUT")


def reglages_matiere(pc, finition="BRUT"):
    """Réglages de matière propres à une famille. Marches (caillebotis, O2) et plancher O2 : galvanisé moins lisse (rugosité
    0,57 au lieu de 0,34). Vérification du 15/09 : photo studio des marches O2 aux trois pièces noire, grise et blanche
    (luminance médiane 48 / 99 / 216), plancher 60 niveaux sous son visuel. Essais à 46° (800 px) : 0,34 -> 90 / 146 / 158,
    0,46 -> 109 / 151 / 160, 0,57 -> 125 / 151 / 158 ; ni la vue (56°, azimut 16) ni les lumières ne réduisaient l'écart de la
    pièce de gauche (position dans la rangée, pas la pièce : même écart dans l'ordre inverse).
    Profil U alu : coupe plus sombre (0,40 au lieu de 0,50, `COUPE_PAR_FINITION`). Vérification du 24/09 : à 0,50, l'aile
    basse sortait à 0–4 niveaux du fond du U vu au-dessus d'elle (contrôle V12) ; plus sombre pour tout l'aluminium, le
    dessus des plats 80x5 et 100x5 et celui de l'aile verticale des cornières tombaient sous 8 niveaux."""
    if pc.get("o2") or pc.get("caillebotis", {}).get("marche"):
        return {"rugosite_galva": 0.57}
    if pc.get("type") == "U" and finition == "ALU":
        return {"base_coupe": 0.40}
    return {}


def reglages_studio(pc):
    """Photo studio des marches et du plancher O2 : lumière « dessus » renforcée (45 par défaut). La pièce de gauche de la
    rangée, loin de la lumière « contre », restait plus sombre (essais 800 px, marches O2, rugosité 0,57 : dessus 45 ->
    125 / 151 / 158, 100 -> 141 / 165 / 168, 160 -> 154 / 176 / 177 ; plancher 120 -> 177 contre 166 sur son visuel,
    marches caillebotis 120 -> 122 / 132 / 128 contre 123)."""
    if pc.get("o2", {}).get("marche"):
        return {"e_dessus": 150}
    if pc.get("o2") or pc.get("caillebotis", {}).get("marche"):
        return {"e_dessus": 120}
    return {}


def eclairage_studio(finition, type_piece):
    """Photo studio des barres en acier brut (calamine) : lumière du dessus doublée (45 → 90) et débouchage sans ombre.
    Essais du 23/09 au soir (large plat, tube carré, 1600 px) : pièces plus claires de 6 à 9 niveaux, donc plus proches
    de leurs fiches (écart studio / fiches des plats −23 → −14 environ), sans délaver. L'écart entre les pièces du fond
    et celle de devant vient de l'occlusion des pièces voisines, pas de l'ombre du débouchage : il bouge à peine (25 → 23).
    Aluminium et inox : photos déjà au niveau de leurs fiches (200–207 contre 205), réglage inchangé. Barres, tubes et
    profilés seulement (`BARRES`) : jamais essayé sur une grande face horizontale (tôles vues à 48°), à essayer avant
    (vérification indépendante du 23/09)."""
    if finition == "BRUT" and type_piece in BARRES:
        return {"e_dessus": 90, "lumieres_sans_ombre": ["debouchage"]}
    return {}


def reglages_nervures(pc, mode):
    """Tôles nervurées et panneaux isolés (vérification indépendante du 15/09) : lumières ancrées au chant avant et au
    bout arrière (`lumieres_ancrees`, sinon la mousse et le chant s'assombrissaient avec la longueur : 175 → 98/255 de
    2,6 à 6,1 m) ; loupe à 64 échantillons, seuil 0,01 (intérieur de nervure noir et déchiqueté à 24 échantillons) ;
    tôle nervurée : lumière d'appoint dans la loupe, qui entre sous la nervure. Aucune autre série n'est concernée."""
    nervures = pc.get("profil", {}).get("motif") == "NERVURES"
    if not (nervures or pc.get("sandwich")):
        return {}
    r = {"lumieres_ancrees": True}
    if mode == "caracteristiques":
        r.update(samples_loupe=64, seuil_loupe=0.01)
        if nervures:
            r["e_loupe_appoint"] = 8.0
    return r


def arrondir_au_pas_des_trous(pc):
    """Poteau à âme percée (CLOPLUS 40) : tronçon multiple du pas des trous, trous à `premier_trou` des deux bouts comme
    sur un poteau entier (2 000, 2 300, 2 500 mm) ; 475 et 532 mm deviennent 500."""
    pas = pc.get("poteau", {}).get("pas_trous")
    if pc["type"] == "POTEAU" and pas:
        pc["longueur"] = max(pas, round(pc["longueur"] / pas) * pas)


def teinte(p):
    """Couleur RAL des produits laqués (clôtures, tôles profilées, panneaux) : matière du rendu. Poteaux verts RAL 6005 :
    laque plus mate et plus saturée, sinon leurs grandes faces planes reflètent le studio gris (vérification du 15/09 :
    chroma médiane Lab 11,5 Clogriff et 13,5 Cloplus contre 20,7 pour les panneaux 6005 validés ; essai Clogriff 800 px :
    chroma ×2,0, reflet 0,15, rugosité 0,6 -> 27,5 / −18,6 / 7,4, C 20,0 ; ×2,4 -> C 22,8 mais trop jaune)."""
    couleur = p["valeurs"].get("couleur", {}).get("valeur", "")
    if not couleur:
        return {}
    ral = couleur.replace("RAL", "").strip()
    if ral == "6005" and p["valeurs"].get("serie", {}).get("valeur") == "POTEAU":
        return {"ral": ral, "chroma_6005": 2.0, "speculaire_laque": 0.15, "rugosite_laque": 0.6}
    return {"ral": ral}


def main():
    args = sys.argv[1:]
    # 32 echantillons a seuil 0,03 : identique a l'oeil a 64 / 0,02 (test poutrelles), ~2 min 15 au lieu de 3 min 45
    options = {"samples": 32, "seuil": 0.03, "ajouter": False, "essai": 0, "points-seuls": False}
    while args and args[0].startswith("--"):
        cle = args.pop(0)[2:]
        options[cle] = True if cle in ("ajouter", "points-seuls") else float(args.pop(0))
    sortie, commande, reste = Path(args[0]), args[1], args[2:]
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    liste = json.loads(sortie.read_text(encoding="utf-8")) if options["ajouter"] and sortie.exists() else []
    largeur = int(options["essai"]) or 1600
    commun = {"sortie": "%LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/" + ("essais" if options["essai"] else "final"),
              "samples": int(options["samples"]), "seuil_adaptatif": options["seuil"], "exposition": -1.15,
              "largeur": largeur, "hauteur": largeur * 3 // 4, "teinte_gpp": TEINTE_GPP,
              "points_seuls": options["points-seuls"]}
    if commande == "car":
        for slug in reste:
            pc, finition = piece(produits[slug], 500, RATIO_CADRE)  # pièce entière dans le cadre (ADR-0011)
            # tôle vue de plus haut : dessus lisible et plaque plus grande dans le cadre (l'épaisseur est en loupe)
            # panneau de clôture : azimut 35 (au lieu de 20) pour lire la cassure en V des fils verticaux dans les plis
            # (essai du 15/09 : décalage du V de 3 à 5 px à l'écran)
            vue = ({"elevation": 48, "azimut": 10} if pc["type"] == "TOLE" else
                   {"elevation": 35} if pc["type"] == "TREILLIS" else
                   {"azimut": 35, **SANS_TRAINEE} if pc["type"] == "PANNEAU-CLOTURE" else {})
            # perforation au pas < 12 mm : moins de 4 px à l'écran sur une plaque entière -> rendu à 2x puis réduit
            # (moiré sur les R5 T8, vérification du 15/09)
            if pc.get("perforation", {}).get("pas", 99) < 12:
                vue["surechantillonnage"] = 2
            liste.append({**commun, **vue, **reglages_matiere(pc, finition), **reglages_nervures(pc, "caracteristiques"),
                          **teinte(produits[slug]), "slug": slug, "mode": "caracteristiques", "pieces": [pc], "finition": finition})
    elif commande == "studio":
        nom, slugs = reste[0], reste[1:]
        pieces, finitions = [], set()
        for slug in slugs:
            pc, finition = piece(produits[slug], 900, 1000)
            pieces.append(pc)
            finitions.add(finition)
        # même longueur pour toutes les pièces de la photo, proportionnée à la plus grande section (sauf tôle entière)
        for pc in pieces:
            if pc["type"] not in ("TOLE", "TREILLIS", "PANNEAU-CLOTURE"):
                pc["longueur"] = min(900, round(RATIO_STUDIO * max(max(q["h"], q["b"]) for q in pieces)))
                arrondir_au_pas_des_trous(pc)
        if len(finitions) > 1:
            raise SystemExit(f"Finitions differentes dans la meme photo studio : {finitions}")
        # panneaux de clôture debout : écart de 15 % de la hauteur (0,9 h les mettrait à plus d'un mètre)
        ecart = {"ecart_studio": 0.15, **SANS_TRAINEE} if pieces[0]["type"] == "PANNEAU-CLOTURE" else {}
        finition = finitions.pop()
        # tôles en métal lisse : vue plus plongeante, proche des visuels (48°) ; à 30°, elles reflétaient le studio
        # sombre, photo 60 niveaux sous les visuels (vérification du 15/09 ; essai : −68 → −15 pour l'inox)
        elevation = (46 if finition in ("INOX", "FROID", "GALVA", "ALU") else 30) if pieces[0]["type"] in ("TOLE", "TREILLIS") else 20
        liste.append({**commun, **teinte(produits[slugs[0]]), **ecart, **eclairage_studio(finition, pieces[0]["type"]), **reglages_matiere(pieces[0], finition),
                      **reglages_studio(pieces[0]),
                      **reglages_nervures(pieces[0], "studio"), "slug": nom, "mode": "studio", "pieces": pieces,
                      "finition": finition, "azimut": 24, "elevation": elevation})
    sortie.write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortie} : {len(liste)} rendus")


if __name__ == "__main__":
    main()
