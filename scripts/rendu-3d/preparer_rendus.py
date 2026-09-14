"""
Prepare la liste de parametres Blender (rendu_profil.py) a partir des donnees sourcees.

  python scripts/rendu-3d/preparer_rendus.py <sortie.json> car <slug> [<slug> ...]
  python scripts/rendu-3d/preparer_rendus.py <sortie.json> studio <nom> <slug> [<slug> ...]
Options (avant les commandes) : --samples N  --seuil X  --ajouter (complete le fichier au lieu de l'ecraser)

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


def piece(p, longueur):
    v = {k: d["valeur"] for k, d in p["valeurs"].items()}
    type_ = "U" if v.get("serie") == "UPN" else "I"
    out = {"type": type_, "h": v["h"], "b": v["b"], "tw": v["tw"], "tf": v["tf"], "longueur": longueur}
    if type_ == "U":
        out.update({"r1": v["r1"], "r2": v["r2"], "pente": v.get("pente_aile", 8)})
    else:
        out["r"] = v["r"]
    return out, v.get("finition", "BRUT")


def main():
    args = sys.argv[1:]
    # 32 echantillons a seuil 0,03 : identique a l'oeil a 64 / 0,02 (test poutrelles), ~2 min 15 au lieu de 3 min 45
    options = {"samples": 32, "seuil": 0.03, "ajouter": False}
    while args and args[0].startswith("--"):
        cle = args.pop(0)[2:]
        options[cle] = True if cle == "ajouter" else float(args.pop(0))
    sortie, commande, reste = Path(args[0]), args[1], args[2:]
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    liste = json.loads(sortie.read_text(encoding="utf-8")) if options["ajouter"] and sortie.exists() else []
    commun = {"sortie": "%LOCALAPPDATA%/SiteAciersGrosjean/rendu3d/final", "samples": int(options["samples"]),
              "seuil_adaptatif": options["seuil"], "exposition": -1.15, "largeur": 1600, "hauteur": 1200,
              "teinte_gpp": TEINTE_GPP}
    if commande == "car":
        for slug in reste:
            pc, finition = piece(produits[slug], 500)
            liste.append({**commun, "slug": slug, "mode": "caracteristiques", "pieces": [pc], "finition": finition})
    elif commande == "studio":
        nom, slugs = reste[0], reste[1:]
        pieces, finitions = [], set()
        for slug in slugs:
            pc, finition = piece(produits[slug], 900)
            pieces.append(pc)
            finitions.add(finition)
        if len(finitions) > 1:
            raise SystemExit(f"Finitions differentes dans la meme photo studio : {finitions}")
        liste.append({**commun, "slug": nom, "mode": "studio", "pieces": pieces, "finition": finitions.pop(),
                      "azimut": 24, "elevation": 20})
    sortie.write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortie} : {len(liste)} rendus")


if __name__ == "__main__":
    main()
