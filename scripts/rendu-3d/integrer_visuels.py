"""
Integre sur le site les visuels 3D d'une famille verifiee « CONFORME » (CLAUDE.md, section Visuels 3D).

  python scripts/rendu-3d/integrer_visuels.py --verdict CONFORME poutrelle-ipe [poutrelle-hea ...]

- copie rendu3d/final/<slug>-caracteristiques.webp -> public/images/produits/<categorie>/<slug>-caracteristiques.webp
  et rendu3d/final/studio-<famille>-studio.webp  -> public/images/produits/<categorie>/studio-<famille>.webp,
  avec une copie pour le proprietaire dans _DEPOT/images/2-categories/<categorie>/fond-blanc/ (studio)
  et /fiche-technique/ (caracteristiques), demande du 15/09 (CLAUDE.md) ;
- met a jour lib/visuels-produits.json, lu par la page produit : chemin, dimensions, texte alternatif ;
- met a jour _DOCS/rendus-3d/inventaire-visuels.csv (slug, categorie, fichier, type, verdict, date).
Refuse la famille si controler_rendus.py y trouve encore un ecart.
"""
import csv
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

import controler_rendus as controle

ICI = Path(__file__).resolve().parent
PROJET = ICI.parents[1]
PUBLIC = PROJET / "public"
# copie consultée par le propriétaire (hors Git, jamais d'essais) : même arborescence que le site, les deux formats
# séparés dans fond-blanc/ (photo studio) et fiche-technique/ (visuel coté)
DEPOT = PROJET / "_DEPOT" / "images" / "2-categories"
MANIFESTE = PROJET / "lib" / "visuels-produits.json"
INVENTAIRE = PROJET / "_DOCS" / "rendus-3d" / "inventaire-visuels.csv"
NOMBRES = {2: "deux", 3: "trois", 4: "quatre"}


def noms_categories():
    ts = (PROJET / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    return {m.group(1): json.loads(m.group(2))
            for m in re.finditer(r'^\s*"(/[^"]+)": \{ chemin: "[^"]+", segment: "[^"]*", nom: ("(?:[^"\\]|\\.)*")', ts, re.M)}


def copier(source, cible):
    """Copie sur le site (public/images/produits/…) et dans le dépôt du propriétaire (_DEPOT/images/2-categories/…)."""
    relatif = cible.relative_to(PUBLIC / "images" / "produits")
    copie = DEPOT / relatif.parent / ("fond-blanc" if cible.name.startswith("studio-") else "fiche-technique") / cible.name
    for chemin in (cible, copie):
        chemin.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, chemin)
    with Image.open(cible) as img:
        largeur, hauteur = img.size
    return {"src": "/" + cible.relative_to(PUBLIC).as_posix(), "largeur": largeur, "hauteur": hauteur}


def main():
    args = sys.argv[1:]
    if len(args) < 3 or args[0] != "--verdict" or args[1] != "CONFORME":
        raise SystemExit(__doc__)
    familles = args[2:]
    produits = json.loads((ICI / "donnees" / "produits.json").read_text(encoding="utf-8"))
    pages = controle.specs_page()
    categories = noms_categories()
    manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8")) if MANIFESTE.exists() else {"produits": {}, "categories": {}}
    inventaire = {}
    if INVENTAIRE.exists():
        with open(INVENTAIRE, encoding="utf-8-sig", newline="") as f:
            inventaire = {(r["slug"], r["type"]): r for r in csv.DictReader(f, delimiter=";")}
    date = datetime.date.today().isoformat()

    for famille in familles:
        ecarts, _ = controle.controler(famille, produits, pages)
        if ecarts:
            raise SystemExit(f"{famille} : {len(ecarts)} ecart(s) aux controles automatiques, integration refusee")
        slugs = sorted(s for s, p in produits.items() if p["famille"] == famille)
        cats = {produits[s]["categorie"] for s in slugs}
        if len(cats) != 1:
            raise SystemExit(f"{famille} : plusieurs categories {cats}, photo studio ambigue")
        categorie = cats.pop()
        dossier = PUBLIC / "images" / "produits" / categorie.strip("/")

        for slug in slugs:
            c = json.loads((controle.FINAL / f"{slug}-caracteristiques.controles.json").read_text(encoding="utf-8"))
            cotes = ", ".join(dict.fromkeys(f"{lettre} {valeur}" for lettre, _, valeur, *_ in c["pastilles"]))
            image = copier(controle.FINAL / f"{slug}-caracteristiques.webp", dossier / f"{slug}-caracteristiques.webp")
            image["alt"] = f"{produits[slug]['nom']} : rendu 3D aux cotes ({cotes}) et fiche technique"
            manifeste["produits"][slug] = image
            inventaire[(slug, "caracteristiques")] = {"slug": slug, "categorie": categorie, "fichier": image["src"],
                                                      "type": "caracteristiques", "verdict": "CONFORME", "date": date}

        composition = json.loads((controle.FINAL / f"studio-{famille}.json").read_text(encoding="utf-8"))
        n = len(composition["pieces"])
        nom = categories.get(categorie, famille)
        image = copier(controle.FINAL / f"studio-{famille}-studio.webp", dossier / f"studio-{famille}.webp")
        image["alt"] = (f"{nom} en acier : {NOMBRES.get(n, n)} tailles côte à côte, photo studio sur fond blanc" if n > 1
                        else f"{nom} en acier, photo studio sur fond blanc")
        manifeste["categories"][categorie] = image
        inventaire[(f"studio-{famille}", "studio")] = {"slug": f"studio-{famille}", "categorie": categorie,
                                                       "fichier": image["src"], "type": "studio", "verdict": "CONFORME",
                                                       "date": date}
        print(f"{famille} : {len(slugs)} visuels caracteristiques + 1 photo studio -> {dossier.relative_to(PROJET)}")

    manifeste = {"produits": dict(sorted(manifeste["produits"].items())),
                 "categories": dict(sorted(manifeste["categories"].items()))}
    MANIFESTE.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(INVENTAIRE, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "categorie", "fichier", "type", "verdict", "date"], delimiter=";")
        w.writeheader()
        for cle in sorted(inventaire, key=lambda k: (inventaire[k]["categorie"], k[1] != "studio", k[0])):
            w.writerow(inventaire[cle])
    print(f"{MANIFESTE.relative_to(PROJET)} : {len(manifeste['produits'])} fiches, {len(manifeste['categories'])} categories")


if __name__ == "__main__":
    main()
