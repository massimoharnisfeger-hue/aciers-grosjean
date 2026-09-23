#!/usr/bin/env python3
"""Inventaire des images du projet et matrice produit <-> visuels du catalogue.

Le catalogue visuel (`/catalogue`) ne montre que des visuels validés, associés
au bon produit. Ce script établit, à partir des fichiers réellement présents,
ce que le catalogue peut montrer et ce qu'il doit signaler. Lecture seule sur
les images : il ne copie, ne déplace, ne modifie et ne supprime rien.

Ce qu'il parcourt
-----------------
  1. public/**                       les images servies par le site
  2. _DEPOT/images/**                le dépôt du propriétaire (jonction OneDrive,
                                     absent des sessions web : signalé, pas une erreur)
  3. <atelier>/final/ et /essais/    les rendus Blender originaux et les brouillons
  4. public/documents/*.pdf          les fiches techniques (documents, pas des images)
  5. *.blend                         les scènes Blender, s'il en existe

Ce qu'il croise
---------------
  lib/catalogue.ts            les produits et les catégories qui existent
  lib/visuels-produits.json   le manifeste : ce que la page produit sert vraiment
  lib/site-actuel.json        les PDF rattachés à chaque produit

Types d'image : `Blender 3D — vue cotée`, `Blender 3D — photo studio`,
`Blender 3D — original atelier`, `Blender 3D — essai`, `photo produit site actuel`,
`photo situation`, `photo à intégrer`, `référence matière`, `planche contact`,
`logo`, `autre`.

Statuts : VALIDÉ (servi par le manifeste, fichier présent), ORPHELINE (sur le
disque, servi nulle part), DOUBLON (copie d'un fichier servi — les copies pour
le propriétaire dans `_DEPOT/images/2-categories/` sont volontaires, CLAUDE.md),
À VÉRIFIER (essai, brouillon, photo non intégrée, référence), MANQUANTE
(produit sans visuel : ligne de la matrice, pas de l'inventaire).

Complément de `scripts/rendu-3d/auditer_visuels.py`, qui juge chaque rendu par
produit ; ici l'unité est le fichier image, et la sortie sert le catalogue.

Usage :
    python scripts/catalogue/inventaire.py            (écrit _DOCS/catalogue-produits/)
    python scripts/catalogue/inventaire.py --resume   (console seule)
"""

import argparse
import csv
import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PUBLIC = RACINE / "public"
DEPOT_IMAGES = RACINE / "_DEPOT" / "images"
ATELIER = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "rendu3d"
MANIFESTE = RACINE / "lib" / "visuels-produits.json"
SITE_ACTUEL = RACINE / "lib" / "site-actuel.json"
CATALOGUE = RACINE / "lib" / "catalogue.ts"
SORTIE = RACINE / "_DOCS" / "catalogue-produits"

EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".avif"}
SUFFIXE_FICHE = "-caracteristiques"


def sortie_utf8():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def charger_auditeur():
    """`produits_du_catalogue` de auditer_visuels.py : une seule lecture du catalogue."""
    chemin = RACINE / "scripts" / "rendu-3d" / "auditer_visuels.py"
    spec = importlib.util.spec_from_file_location("auditer_visuels", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def noeuds_du_catalogue() -> dict:
    """{chemin: {nom, univers, enfants, produits}} lus dans le catalogue généré."""
    texte = CATALOGUE.read_text(encoding="utf-8")
    trouves = {}
    motif = re.compile(
        r'"(/[^"]+)": \{ chemin: "[^"]+", segment: "[^"]*", nom: "((?:[^"\\]|\\.)*)", h1: "(?:[^"\\]|\\.)*", '
        r'univers: "([^"]+)", accroche: "(?:[^"\\]|\\.)*", titreSeo: "(?:[^"\\]|\\.)*", '
        r'enfants: \[([^\]]*)\], produits: \[([^\]]*)\]'
    )
    for m in motif.finditer(texte):
        trouves[m.group(1)] = {
            "nom": m.group(2),
            "univers": m.group(3),
            "enfants": re.findall(r'"([^"]+)"', m.group(4)),
            "produits": re.findall(r'"([^"]+)"', m.group(5)),
        }
    return trouves


def dimensions(chemin: Path):
    """(largeur, hauteur) d'une image raster, ou ('vectoriel', '') pour un SVG."""
    if chemin.suffix.lower() == ".svg":
        return "vectoriel", ""
    try:
        from PIL import Image

        with Image.open(chemin) as img:
            return img.size
    except Exception:  # fichier illisible : c'est une information, pas une panne
        return "illisible", ""


def relatif(chemin: Path, base: Path) -> str:
    try:
        return chemin.relative_to(base).as_posix()
    except ValueError:
        return chemin.as_posix()


def type_et_source(chemin: Path, base: str, rel: str) -> tuple[str, str]:
    """Le type d'image et sa source, déduits du nom et de l'emplacement."""
    nom = chemin.name.lower()
    if base == "public":
        if nom.endswith(SUFFIXE_FICHE + chemin.suffix.lower()):
            return "Blender 3D — vue cotée", "public/images/produits"
        if nom.startswith("studio-"):
            return "Blender 3D — photo studio", "public/images/produits"
        if nom.startswith("situation-"):
            return "photo situation", "public/images/produits"
        if nom.startswith("logo"):
            return "logo", "public"
        return "autre", "public"
    if base == "atelier":
        if rel.startswith("essais/"):
            return "Blender 3D — essai", "atelier/essais"
        if nom.startswith("studio-"):
            return "Blender 3D — original atelier (studio)", "atelier/final"
        return "Blender 3D — original atelier", "atelier/final"
    # _DEPOT/images
    premier = rel.split("/", 1)[0]
    if premier == "2-categories":
        if "/fiche-technique/" in rel:
            return "Blender 3D — vue cotée (copie propriétaire)", "_DEPOT/images/2-categories"
        if "/fond-blanc/" in rel:
            return "Blender 3D — photo studio (copie propriétaire)", "_DEPOT/images/2-categories"
        return "photo à intégrer", "_DEPOT/images/2-categories"
    if premier == "site-actuel":
        if "_planches" in rel:
            return "planche contact", "_DEPOT/images/site-actuel"
        return "photo produit site actuel", "_DEPOT/images/site-actuel"
    if premier == "situation":
        return "photo situation", "_DEPOT/images/situation"
    if premier == "references-matieres":
        return "référence matière", "_DEPOT/images/references-matieres"
    if premier == "test-blender":
        return "Blender 3D — essai", "_DEPOT/images/test-blender"
    return "photo à intégrer", f"_DEPOT/images/{premier}"


def produit_et_categorie(chemin: Path, base: str, rel: str, produits: dict, noeuds: dict):
    """Le produit (slug) et la catégorie (chemin) qu'un fichier désigne, si son nom le dit."""
    racine_nom = chemin.name[: -len(chemin.suffix)]
    if racine_nom.endswith(SUFFIXE_FICHE):
        slug = racine_nom[: -len(SUFFIXE_FICHE)]
        if slug in produits:
            return slug, produits[slug]["categorie"]
        return slug, ""
    if base == "public" and rel.startswith("images/produits/"):
        dossier = "/" + rel[len("images/produits/"):].rsplit("/", 1)[0]
        return "", dossier if dossier in noeuds else ""
    if base == "depot" and rel.startswith("2-categories/"):
        parties = rel.split("/")
        # 2-categories/<univers>/<catégorie...>/fond-blanc|fiche-technique/<fichier>
        if len(parties) >= 4:
            dossier = "/" + "/".join(parties[1:-2])
            return "", dossier if dossier in noeuds else ""
    return "", ""


def sous_categorie(categorie: str, noeuds: dict) -> str:
    """Le nœud intermédiaire (sous-catégorie) d'une catégorie feuille, s'il existe."""
    parties = [p for p in categorie.split("/") if p]
    if len(parties) >= 3:
        parent = "/" + "/".join(parties[:-1])
        return noeuds.get(parent, {}).get("nom", "")
    return ""


def inventorier() -> tuple[list[dict], list[dict], dict]:
    auditeur = charger_auditeur()
    produits = auditeur.produits_du_catalogue()
    noeuds = noeuds_du_catalogue()
    manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    site = json.loads(SITE_ACTUEL.read_text(encoding="utf-8"))

    servis = {e["src"] for e in manifeste["produits"].values()} | {
        e["src"] for e in manifeste["categories"].values()
    }
    servis_par_fichier = defaultdict(list)
    for slug, e in manifeste["produits"].items():
        servis_par_fichier[e["src"]].append(slug)

    lignes = []

    def ajouter(chemin: Path, base: str, rel: str):
        typ, source = type_et_source(chemin, base, rel)
        slug, categorie = produit_et_categorie(chemin, base, rel, produits, noeuds)
        larg, haut = dimensions(chemin)
        src_site = "/" + rel if base == "public" else ""
        note = ""
        if base == "public":
            if src_site in servis:
                statut = "VALIDÉ"
                if len(servis_par_fichier.get(src_site, [])) > 1:
                    statut = "DOUBLON"
                    note = "servi à plusieurs produits : " + ", ".join(servis_par_fichier[src_site])
            elif rel.startswith("images/produits/"):
                statut = "ORPHELINE"
                note = "sur le disque, servi nulle part (photo studio en concurrence : décision humaine)"
            else:
                statut = "VALIDÉ" if typ == "logo" else "À VÉRIFIER"
        elif base == "atelier":
            if typ.startswith("Blender 3D — essai"):
                statut = "À VÉRIFIER"
                note = "brouillon d'atelier, jamais servi (convention CLAUDE.md)"
            else:
                copie_servie = categorie and (
                    "/images/produits" + categorie + "/" + chemin.name
                ) in servis
                statut = "VALIDÉ" if copie_servie else "À VÉRIFIER"
                note = "original de production, copie servie" if copie_servie else "original sans copie servie (png source, studio non retenu ou produit inconnu)"
        else:  # dépôt
            if "copie propriétaire" in typ:
                statut = "DOUBLON"
                note = "copie volontaire pour le propriétaire (CLAUDE.md, demande du 15/09)"
            elif typ in ("photo produit site actuel", "planche contact"):
                statut = "À VÉRIFIER"
                note = "référence téléchargée du site actuel, non validée pour le nouveau site"
            elif typ == "photo situation":
                statut = "À VÉRIFIER"
                note = "mise en situation : à valider avant intégration"
            else:
                statut = "À VÉRIFIER"
                note = "déposé, pas encore intégré"
        lignes.append({
            "chemin": f"{base}:{rel}",
            "nom": chemin.name,
            "format": chemin.suffix.lower().lstrip("."),
            "largeur": larg,
            "hauteur": haut,
            "octets": chemin.stat().st_size,
            "produit": slug,
            "categorie": categorie,
            "sous_categorie": sous_categorie(categorie, noeuds) if categorie else "",
            "type": typ,
            "source": source,
            "statut": statut,
            "note": note,
        })

    for f in sorted(PUBLIC.rglob("*")):
        if f.is_file() and f.suffix.lower() in EXTENSIONS:
            ajouter(f, "public", relatif(f, PUBLIC))

    depot_present = DEPOT_IMAGES.is_dir()
    if depot_present:
        for f in sorted(DEPOT_IMAGES.rglob("*")):
            if f.is_file() and f.suffix.lower() in EXTENSIONS:
                ajouter(f, "depot", relatif(f, DEPOT_IMAGES))

    atelier_present = (ATELIER / "final").is_dir()
    if atelier_present:
        for dossier in ("final", "essais"):
            for f in sorted((ATELIER / dossier).rglob("*")):
                if f.is_file() and f.suffix.lower() in EXTENSIONS:
                    ajouter(f, "atelier", relatif(f, ATELIER))

    blends = [relatif(f, RACINE) for f in RACINE.rglob("*.blend") if "node_modules" not in f.parts]
    if atelier_present:
        blends += [relatif(f, ATELIER) for f in ATELIER.rglob("*.blend")]
    pdfs = sorted(f.name for f in (PUBLIC / "documents").glob("*.pdf")) if (PUBLIC / "documents").is_dir() else []

    # --- matrice produit <-> visuels
    studios_par_categorie = defaultdict(list)
    for l in lignes:
        if l["chemin"].startswith("public:images/produits/") and l["type"] == "Blender 3D — photo studio":
            studios_par_categorie[l["categorie"]].append("/" + l["chemin"].split(":", 1)[1])

    matrice = []
    for slug, p in sorted(produits.items()):
        fiche = manifeste["produits"].get(slug, {}).get("src", "")
        studio = manifeste["categories"].get(p["categorie"], {}).get("src", "")
        autres = [s for s in studios_par_categorie.get(p["categorie"], []) if s != studio]
        docs = [d["fichier"] for d in site.get(slug, {}).get("pdfs", [])]
        fiche_ok = bool(fiche) and (PUBLIC / fiche.lstrip("/")).is_file()
        matrice.append({
            "slug": slug,
            "produit": p["nom"],
            "univers": p["univers"],
            "categorie": p["categorie"],
            "sous_categorie": sous_categorie(p["categorie"], noeuds),
            "image_principale": fiche if fiche_ok else "",
            "photo_studio_categorie": studio,
            "autres_studios_non_servis": " | ".join(autres),
            "pdfs": " | ".join(docs),
            "route_fiche": f"/p/{slug}",
            "route_catalogue": f"/catalogue/{p['univers']}#{p['categorie'].strip('/').replace('/', '-')}",
            "statut": "VALIDÉ" if fiche_ok else "VISUEL À COMPLÉTER",
        })

    bilan = {
        "date": date.today().isoformat(),
        "produits": len(produits),
        "categories_feuilles": sum(1 for n in noeuds.values() if n["produits"]),
        "univers": len({p["univers"] for p in produits.values()}),
        "produits_avec_image": sum(1 for m in matrice if m["statut"] == "VALIDÉ"),
        "produits_sans_image": sum(1 for m in matrice if m["statut"] != "VALIDÉ"),
        "images_total": len(lignes),
        "images_par_base": dict(Counter(l["chemin"].split(":", 1)[0] for l in lignes)),
        "images_par_type": dict(Counter(l["type"] for l in lignes)),
        "images_par_statut": dict(Counter(l["statut"] for l in lignes)),
        "images_servies_manifeste": len(servis),
        "images_orphelines_public": [l["chemin"] for l in lignes if l["statut"] == "ORPHELINE"],
        "images_servies_absentes": sorted(s for s in servis if not (PUBLIC / s.lstrip("/")).is_file()),
        "images_illisibles": [l["chemin"] for l in lignes if l["largeur"] == "illisible"],
        "categories_sans_studio": sorted(
            c for c, n in noeuds.items() if n["produits"] and c not in manifeste["categories"]
        ),
        "pdfs_publies": len(pdfs),
        "fichiers_blend": blends,
        "depot_present": depot_present,
        "atelier_present": atelier_present,
        "manifeste_produits": len(manifeste["produits"]),
        "manifeste_categories": len(manifeste["categories"]),
    }
    return lignes, matrice, bilan


def ecrire(lignes, matrice, bilan) -> Path:
    SORTIE.mkdir(parents=True, exist_ok=True)
    for nom, contenu in (("inventaire-images.csv", lignes), ("matrice-produits.csv", matrice)):
        with (SORTIE / nom).open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(contenu[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(contenu)

    def tableau(compteur: dict) -> str:
        return "".join(f"| {k} | {v} |\n" for k, v in sorted(compteur.items(), key=lambda x: -x[1]))

    (SORTIE / "RESUME.md").write_text(
        "# Inventaire des visuels — résumé\n\n"
        f"Recalculé le {bilan['date']} par `scripts/catalogue/inventaire.py`. Aucun compteur repris\n"
        "d'un document antérieur. Détail : `inventaire-images.csv` (une ligne par fichier image) et\n"
        "`matrice-produits.csv` (une ligne par produit du catalogue).\n\n"
        "## Produits\n\n| Mesure | Nombre |\n|---|---|\n"
        f"| Produits au catalogue | {bilan['produits']} |\n"
        f"| Univers | {bilan['univers']} |\n"
        f"| Catégories portant des produits | {bilan['categories_feuilles']} |\n"
        f"| Produits avec visuel validé | {bilan['produits_avec_image']} |\n"
        f"| Produits sans visuel | {bilan['produits_sans_image']} |\n"
        f"| Catégories sans photo studio | {len(bilan['categories_sans_studio'])} |\n\n"
        "## Images\n\n| Mesure | Nombre |\n|---|---|\n"
        f"| Fichiers image inventoriés | {bilan['images_total']} |\n"
        f"| Servis par le manifeste (fiches + studios) | {bilan['images_servies_manifeste']} |\n"
        f"| Servis mais absents du disque | {len(bilan['images_servies_absentes'])} |\n"
        f"| Orphelins dans `public/images/produits` | {len(bilan['images_orphelines_public'])} |\n"
        f"| Illisibles | {len(bilan['images_illisibles'])} |\n"
        f"| PDF publiés (`public/documents`) | {bilan['pdfs_publies']} |\n"
        f"| Scènes Blender `.blend` | {len(bilan['fichiers_blend'])} |\n\n"
        "### Par emplacement\n\n| Emplacement | Fichiers |\n|---|---|\n"
        + tableau(bilan["images_par_base"])
        + "\n### Par type\n\n| Type | Fichiers |\n|---|---|\n"
        + tableau(bilan["images_par_type"])
        + "\n### Par statut\n\n| Statut | Fichiers |\n|---|---|\n"
        + tableau(bilan["images_par_statut"])
        + "\n## À signaler\n\n"
        + (
            "- Photos studio sur le disque que rien ne sert (décision humaine, voir "
            "`_DOCS/rendus-3d/IMAGE-RECONCILIATION.md`) :\n"
            + "".join(f"  - `{c}`\n" for c in bilan["images_orphelines_public"])
            if bilan["images_orphelines_public"]
            else "- Aucune image orpheline dans `public/images/produits`.\n"
        )
        + (
            "- Catégories sans photo studio :\n"
            + "".join(f"  - `{c}`\n" for c in bilan["categories_sans_studio"])
            if bilan["categories_sans_studio"]
            else ""
        )
        + ("" if bilan["depot_present"] else "- `_DEPOT/images` absent : dépôt du propriétaire non inventorié (session sans jonction).\n")
        + ("" if bilan["atelier_present"] else "- Atelier Blender absent : originaux et essais non inventoriés.\n"),
        encoding="utf-8",
    )
    return SORTIE


def main() -> int:
    sortie_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true", help="console seule, aucun fichier écrit")
    args = ap.parse_args()

    lignes, matrice, bilan = inventorier()
    print(f"Produits                 : {bilan['produits']} ({bilan['produits_avec_image']} avec visuel, {bilan['produits_sans_image']} sans)")
    print(f"Catégories feuilles      : {bilan['categories_feuilles']} ({len(bilan['categories_sans_studio'])} sans photo studio)")
    print(f"Images inventoriées      : {bilan['images_total']}  {bilan['images_par_base']}")
    print("Par statut               :", bilan["images_par_statut"])
    print(f"Servies par le manifeste : {bilan['images_servies_manifeste']} (absentes du disque : {len(bilan['images_servies_absentes'])})")
    print(f"Orphelines (public)      : {len(bilan['images_orphelines_public'])}")
    print(f"PDF publiés              : {bilan['pdfs_publies']}   Scènes .blend : {len(bilan['fichiers_blend'])}")
    if not bilan["depot_present"]:
        print("_DEPOT/images absent : dépôt non inventorié", file=sys.stderr)
    if not bilan["atelier_present"]:
        print("Atelier Blender absent : originaux non inventoriés", file=sys.stderr)
    if not args.resume:
        print(f"\nÉcrit dans : {ecrire(lignes, matrice, bilan)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
