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
        x_nervure = -v["l"] / 2 + v["base"] / 2 + 5.0 + v["pas"]
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"],
                 "profil": {"motif": "NERVURES", "pas": v["pas"], "h": v["h"], "sommet": v["sommet"], "base": v["base"]},
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
    elif serie == "PANNEAU-ISOLE":  # sandwich : âme × épaisseur e, tôle nervurée dessus ; loupe sur le chant de l'âme
        return ({"type": "TOLE", "h": v["e"], "b": v["l"], "longueur": v["L"],
                 "sandwich": {"l_utile": v["l_utile"], "pas": v["pas"], "h_nervure": v["h_nervure"], "sommet": v["sommet"],
                              "base": v["base"], "e_tole": v["e_tole"]},
                 "loupe": {"x": -v["l"] / 2 + v["pas"] / 2, "z_haut": v["e"], "z_bas": 0.0, "champ": max(6 * v["e"], 30.0), "cle": "e"}},
                v.get("finition", "BRUT"))
    elif serie in ("CAILLEBOTIS", "MARCHE-CAILLEBOTIS"):  # à plat comme une tôle ; loupe : hauteur h du plat de rive
        marche = serie == "MARCHE-CAILLEBOTIS"
        largeur, longueur = (v["L"], v["l"]) if marche else (v["l"], v["L"])  # marche : le grand côté devant
        return ({"type": "TOLE", "h": v["h"], "b": largeur, "longueur": longueur,
                 "caillebotis": {"t": v["t"], "maille_a": v["maille_a"], "maille_b": v["maille_b"], "marche": marche},
                 "loupe": {"x": -largeur * 0.3, "z_haut": v["h"], "z_bas": 0.0, "champ": max(6 * v["h"], 30.0), "cle": "h"}},
                v.get("finition", "GALVA"))
    elif serie in ("PLANCHER-O2", "MARCHE-O2"):  # tôle perforée emboutie à bords pliés ; loupe : hauteur h du bord
        marche = serie == "MARCHE-O2"
        largeur, longueur = (v["L"], v["l"]) if marche else (v["l"], v["L"])
        return ({"type": "TOLE", "h": v["h"], "b": largeur, "longueur": longueur,
                 "o2": {"t": v["t"], "trous": v["trous"], "drainage": v["drainage"], "entraxe": 25.0, "marche": marche},
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
    elif serie == "POTEAU":  # couché comme un profilé : section b × h
        q = {"modele": v["modele"], "encoche": v.get("encoche"), "pas": v.get("pas_encoches")}
        t = 2.0  # CLOGRIFF 64 : parois de 2 mm (forme du rendu)
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


def arrondir_au_pas_des_trous(pc):
    """Poteau à âme percée (CLOPLUS 40) : tronçon multiple du pas des trous, trous à `premier_trou` des deux bouts comme
    sur un poteau entier (2 000, 2 300, 2 500 mm) ; 475 et 532 mm deviennent 500."""
    pas = pc.get("poteau", {}).get("pas_trous")
    if pc["type"] == "POTEAU" and pas:
        pc["longueur"] = max(pas, round(pc["longueur"] / pas) * pas)


def teinte(p):
    """Couleur RAL des produits laqués (clôtures, tôles profilées, panneaux) : matière du rendu."""
    couleur = p["valeurs"].get("couleur", {}).get("valeur", "")
    return {"ral": couleur.replace("RAL", "").strip()} if couleur else {}


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
            pc, finition = piece(produits[slug], 500, 6.25)
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
            liste.append({**commun, **vue, **teinte(produits[slug]), "slug": slug, "mode": "caracteristiques",
                          "pieces": [pc], "finition": finition})
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
                pc["longueur"] = min(900, round(7 * max(max(q["h"], q["b"]) for q in pieces)))
                arrondir_au_pas_des_trous(pc)
        if len(finitions) > 1:
            raise SystemExit(f"Finitions differentes dans la meme photo studio : {finitions}")
        # panneaux de clôture debout : écart de 15 % de la hauteur (0,9 h les mettrait à plus d'un mètre)
        ecart = {"ecart_studio": 0.15, **SANS_TRAINEE} if pieces[0]["type"] == "PANNEAU-CLOTURE" else {}
        finition = finitions.pop()
        # tôles en métal lisse : vue plus plongeante, proche des visuels (48°) ; à 30°, elles reflétaient le studio
        # sombre, photo 60 niveaux sous les visuels (vérification du 15/09 ; essai : −68 → −15 pour l'inox)
        elevation = (46 if finition in ("INOX", "FROID", "GALVA", "ALU") else 30) if pieces[0]["type"] in ("TOLE", "TREILLIS") else 20
        liste.append({**commun, **teinte(produits[slugs[0]]), **ecart, "slug": nom, "mode": "studio", "pieces": pieces,
                      "finition": finition, "azimut": 24, "elevation": elevation})
    sortie.write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortie} : {len(liste)} rendus")


if __name__ == "__main__":
    main()
