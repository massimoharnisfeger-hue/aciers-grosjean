#!/usr/bin/env python3
"""Retire le tableau de specifications incruste dans les rendus 3D des fiches.

Pourquoi
--------
Chaque rendu de fiche produit fait 1600 x 1200 et porte, sur ses 38 % droits,
un tableau incruste — matiere, cotes, poids, procede. Ce tableau redit la fiche
technique affichee juste a cote sur la page, et il coute a l'objet la moitie de
sa taille : les cotes portees par le dessin devenaient illisibles.

Le 22/09, le recadrage a d'abord ete fait en CSS (`object-cover` sur une boite
5/6). Mauvaise solution : elle force un agrandissement, rend la boite verticale
alors que l'objet est horizontal, et le proprietaire l'a dit sans detour —
« c'est beaucoup trop zoome et ca prend trop de place ». Une photo produit se
montre ENTIERE, posee sur un fond neutre, jamais rognee a l'affichage.

Ce script retire donc le tableau du FICHIER, une fois. La page peut alors
afficher l'objet entier (`object-contain`) dans une boite de rapport stable.

Le cadre
--------
Mesure faite sur les 466 rendus, pas sur un echantillon : l'objet ne depasse
jamais x = 0,595 et occupe verticalement de 0,073 a 0,967. Le cadre commun
retenu les contient tous avec une marge. Un cadre COMMUN, et non un cadrage au
plus juste de chaque objet : c'est ce qui donne a une serie son allure de
catalogue plutot que de collage.

Reversibilite
-------------
Le script lit toujours l'ORIGINAL depuis l'atelier, jamais le fichier deja
servi : le relancer ne degrade rien, et restaurer revient a recopier l'atelier.
Verifie le 22/09 : les 466 rendus servis ont leur original dans `final/`.

Usage :
    python scripts/rendu-3d/recadrer_visuels.py --verifier   (n'ecrit rien)
    python scripts/rendu-3d/recadrer_visuels.py
"""

import os
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SERVIS = RACINE / "public" / "images" / "produits"
ATELIER = Path(os.environ.get("LOCALAPPDATA", "")) / "SiteAciersGrosjean" / "rendu3d" / "final"

# Cadre commun, en fractions de l'image d'origine. Mesure sur les 466 rendus.
CADRE = (0.000, 0.043, 0.615, 0.987)
QUALITE = 82


def originaux() -> dict:
    return {p.name: p for p in ATELIER.glob("*-caracteristiques.webp")}


def recadrer(source: Path, destination: Path, ecrire: bool):
    """Retourne (octets avant, octets apres). N'ecrit que si `ecrire`."""
    from PIL import Image

    with Image.open(source) as image:
        largeur, hauteur = image.size
        x0, y0, x1, y1 = CADRE
        boite = (int(x0 * largeur), int(y0 * hauteur), int(x1 * largeur), int(y1 * hauteur))
        coupe = image.convert("RGB").crop(boite)
        avant = destination.stat().st_size if destination.exists() else 0
        if not ecrire:
            return avant, avant
        coupe.save(destination, "WEBP", quality=QUALITE, method=6)
    return avant, destination.stat().st_size


def main(argv: list) -> int:
    verifier = "--verifier" in argv
    if not ATELIER.exists():
        print(f"Atelier introuvable : {ATELIER}")
        print("Les originaux y sont indispensables : le script ne recadre jamais un fichier deja servi.")
        return 1

    sources = originaux()
    cibles = sorted(SERVIS.rglob("*-caracteristiques.webp"))
    sans_original = [c for c in cibles if c.name not in sources]
    if sans_original:
        print(f"{len(sans_original)} rendus servis n'ont pas d'original dans l'atelier :")
        for c in sans_original[:5]:
            print("   ", c.name)
        print("Rien n'a ete ecrit : un recadrage sans original n'est pas reversible.")
        return 1

    total_avant = total_apres = 0
    for cible in cibles:
        avant, apres = recadrer(sources[cible.name], cible, ecrire=not verifier)
        total_avant += avant
        total_apres += apres

    action = "seraient recadres" if verifier else "recadres"
    print(f"{len(cibles)} rendus {action}.")
    if not verifier:
        print(f"poids : {total_avant // 1024} Ko -> {total_apres // 1024} Ko")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
