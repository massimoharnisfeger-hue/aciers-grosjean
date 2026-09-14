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
                 "maille_b": v["maille_b"], "nx": nx, "ny": ny, "longueur": ny * v["maille_a"]},
                v.get("finition", "BRUT"))
    else:
        type_ = "U" if serie in ("UPN", "U-ALU") else "I"
        out = {"type": type_, "h": v["h"], "b": v["b"], "tw": v["tw"], "tf": v["tf"]}
        if type_ == "U":  # U alu filé : ailes parallèles (pente nulle)
            out.update({"r1": v["r1"], "r2": v["r2"], "pente": v.get("pente_aile", 0 if serie == "U-ALU" else 8)})
        else:
            out["r"] = v["r"]
    out["longueur"] = min(longueur, round(ratio * max(out["h"], out["b"])))
    return out, v.get("finition", "BRUT")


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
            vue = ({"elevation": 48, "azimut": 10} if pc["type"] == "TOLE" else
                   {"elevation": 35} if pc["type"] == "TREILLIS" else {})
            liste.append({**commun, **vue, "slug": slug, "mode": "caracteristiques", "pieces": [pc], "finition": finition})
    elif commande == "studio":
        nom, slugs = reste[0], reste[1:]
        pieces, finitions = [], set()
        for slug in slugs:
            pc, finition = piece(produits[slug], 900, 1000)
            pieces.append(pc)
            finitions.add(finition)
        # même longueur pour toutes les pièces de la photo, proportionnée à la plus grande section (sauf tôle entière)
        for pc in pieces:
            if pc["type"] not in ("TOLE", "TREILLIS"):
                pc["longueur"] = min(900, round(7 * max(max(q["h"], q["b"]) for q in pieces)))
        if len(finitions) > 1:
            raise SystemExit(f"Finitions differentes dans la meme photo studio : {finitions}")
        liste.append({**commun, "slug": nom, "mode": "studio", "pieces": pieces, "finition": finitions.pop(),
                      "azimut": 24, "elevation": 30 if pieces[0]["type"] in ("TOLE", "TREILLIS") else 20})
    sortie.write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortie} : {len(liste)} rendus")


if __name__ == "__main__":
    main()
