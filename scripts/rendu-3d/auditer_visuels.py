"""Audit des visuels produit : catalogue x rendus Blender x site x manifeste.

Recalcule l'etat reel, sans faire confiance a aucun compteur ecrit ailleurs.
Lecture seule sur le depot et sur l'atelier : ce script ne copie, ne remplace
et ne supprime rien. Il n'ecrit que ses trois rapports.

Complement de `integrer_visuels.py`, qui integre et tient
`inventaire-visuels.csv` : cet inventaire-la ne connait que ce qui a ete
integre, donc il ne peut montrer ni produit sans rendu, ni rendu orphelin,
ni image servie sans source.

Sources croisees :
  1. lib/catalogue.ts                          les produits qui existent vraiment
  2. <atelier>/final/*-caracteristiques.webp   les rendus Blender de production
     (jamais <atelier>/essais/ : brouillons, par convention CLAUDE.md)
  3. public/images/produits/**                 les images servies par le site
  4. lib/visuels-produits.json                 le manifeste lu par la page produit
  5. <atelier>/final/*.controles.json          titre et cotes ayant servi au rendu,
                                               donc a QUI il appartient

Statuts par produit :
  CORRECT               rendu present, integre, manifeste correct, fichier lisible
  FOUND_NOT_INTEGRATED  rendu present dans l'atelier, absent du site
  INVALID               rendu present mais vide ou illisible
  AMBIGUOUS             titre du rendu different du produit, ou image sans source
  NO_RENDER             aucun rendu pour ce produit
  MISSING_FILE          le manifeste pointe un fichier absent du disque

Un produit sans image propre n'a pas d'image vide : la page sert l'illustration
SVG de sa famille (`components/art/ProductArt.tsx`). C'est la colonne `fallback`.

Usage :
    python scripts/rendu-3d/auditer_visuels.py            (rapports dans _DOCS/rendus-3d/)
    python scripts/rendu-3d/auditer_visuels.py --resume   (sortie console seule)
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
ATELIER = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SiteAciersGrosjean" / "rendu3d"
FINAL = ATELIER / "final"
ESSAIS = ATELIER / "essais"
PUBLIC = RACINE / "public"
MANIFESTE = RACINE / "lib" / "visuels-produits.json"
DOCS = RACINE / "_DOCS" / "rendus-3d"

SUFFIXE = "-caracteristiques.webp"
TAILLE_MINIMALE = 5_000  # octets : sous ce seuil, un WebP n'a pas de contenu utile


def sortie_utf8():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def normaliser(texte: str) -> str:
    """Compare deux libelles sans accents, sans casse et sans ponctuation."""
    sans = unicodedata.normalize("NFD", texte or "")
    sans = "".join(c for c in sans if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", sans.lower())


def mots(texte: str) -> list[str]:
    """Mots normalises d'un libelle, ponctuation et accents retires."""
    sans = unicodedata.normalize("NFD", texte or "")
    sans = "".join(c for c in sans if unicodedata.category(c) != "Mn")
    return [m for m in re.split(r"[^a-z0-9,.]+", sans.lower()) if m]


def le_rendu_designe_le_produit(titre: str, nom: str) -> bool:
    """Le titre du rendu designe-t-il ce produit, et lui seul ?

    Le rendu porte un titre volontairement raccourci : la matiere est deja
    dans le surtitre de l'image (« ACIER . ARMATURES BETON »). « Rond a beton
    de 10mm de diametre » est donc le bon titre pour « Rond a beton de 10mm de
    diametre en acier lamine a chaud », et « Tube rond 21,3x2mm serie legere »
    pour « Tube rond 21,3x2mm en acier brut serie legere ».

    Regle : le titre du rendu n'AJOUTE jamais d'information, il en retire. Ses
    mots doivent donc apparaitre dans le nom du produit, dans le meme ordre.
    Un mot etranger, ou une cote differente, revele un rendu qui appartient a
    un autre produit — c'est le cas qu'il faut attraper.
    """
    a, b = mots(titre), mots(nom)
    i = 0
    for mot in a:
        while i < len(b) and b[i] != mot:
            i += 1
        if i == len(b):
            return False
        i += 1
    # garde sur les cotes : tout nombre du rendu doit exister dans le produit
    chiffres_rendu = {m for m in a if any(c.isdigit() for c in m)}
    chiffres_nom = {m for m in b if any(c.isdigit() for c in m)}
    return chiffres_rendu <= chiffres_nom


def produits_du_catalogue() -> dict:
    """{slug: {nom, categorie, univers}} lu dans le catalogue genere."""
    texte = (RACINE / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    trouves = re.findall(
        r'"([a-z0-9-]+)": \{ slug: "[^"]+", nom: "([^"]+)", categorie: "([^"]+)", univers: "([^"]+)"',
        texte,
    )
    return {s: {"nom": n, "categorie": c, "univers": u} for s, n, c, u in trouves}


def rendus_de_l_atelier() -> dict:
    """{slug: chemin} des rendus de production. `essais/` est exclu par construction."""
    if not FINAL.is_dir():
        return {}
    return {f.name[: -len(SUFFIXE)]: f for f in FINAL.glob("*" + SUFFIXE)}


def titre_du_rendu(chemin: Path) -> str | None:
    """Titre inscrit dans le rendu, d'apres son fichier de controle voisin."""
    controle = chemin.parent / (chemin.name[: -len(".webp")] + ".controles.json")
    if not controle.is_file():
        return None
    try:
        return json.loads(controle.read_text(encoding="utf-8")).get("titre")
    except (json.JSONDecodeError, OSError):
        return None


def manifeste() -> dict:
    if not MANIFESTE.is_file():
        return {"produits": {}, "categories": {}}
    return json.loads(MANIFESTE.read_text(encoding="utf-8"))


def auditer() -> tuple[list[dict], dict]:
    catalogue = produits_du_catalogue()
    rendus = rendus_de_l_atelier()
    m = manifeste()
    inscrits = m.get("produits", {})

    lignes = []
    for slug, p in sorted(catalogue.items()):
        rendu = rendus.get(slug)
        entree = inscrits.get(slug)
        image_site = ""
        statut = ""
        action = ""
        validation = ""

        if entree:
            if (PUBLIC / entree["src"].lstrip("/")).is_file():
                image_site = entree["src"]
            else:
                statut = "MISSING_FILE"
                action = "le manifeste pointe un fichier absent : relancer integrer_visuels.py"
                validation = "HUMAN_REVIEW"

        if not statut:
            if rendu is None:
                if entree:
                    statut = "AMBIGUOUS"
                    action = "image servie sans rendu correspondant dans final/"
                    validation = "HUMAN_REVIEW"
                else:
                    statut = "NO_RENDER"
                    action = "rendu Blender a produire"
            else:
                taille = rendu.stat().st_size
                titre = titre_du_rendu(rendu)
                if taille < TAILLE_MINIMALE:
                    statut = "INVALID"
                    action = f"rendu de {taille} octets : refaire"
                    validation = "HUMAN_REVIEW"
                elif titre and not le_rendu_designe_le_produit(titre, p["nom"]):
                    statut = "AMBIGUOUS"
                    action = f"titre du rendu « {titre} » != produit « {p['nom']} »"
                    validation = "HUMAN_REVIEW"
                elif entree is None:
                    statut = "FOUND_NOT_INTEGRATED"
                    action = "integrer : python scripts/rendu-3d/integrer_visuels.py"
                else:
                    statut = "CORRECT"

        lignes.append({
            "slug": slug,
            "produit": p["nom"],
            "categorie": p["categorie"],
            "rendu_blender": rendu.name if rendu else "",
            "statut": statut,
            "image_actuelle": image_site,
            "fallback": "non" if image_site else "oui (illustration SVG de famille)",
            "action": action,
            "validation": validation,
        })

    # --- controles transverses
    slugs = set(catalogue)
    servies = {e["src"] for e in inscrits.values()} | {
        e["src"] for e in m.get("categories", {}).values()
    }
    dossier_images = PUBLIC / "images" / "produits"
    sur_disque = (
        {"/" + f.relative_to(PUBLIC).as_posix() for f in dossier_images.rglob("*.webp")}
        if dossier_images.is_dir()
        else set()
    )

    empreintes = defaultdict(list)
    for slug, entree in inscrits.items():
        empreintes[entree["src"]].append(slug)

    # Plusieurs familles de photo studio pour une meme categorie : le manifeste
    # n'en tient qu'une, les autres restent sur le disque sans etre servies.
    # Choisir laquelle montrer est une decision humaine, pas une correction.
    studios_servis = {e["src"] for e in m.get("categories", {}).values()}
    concurrences = {}
    for f in sorted(sur_disque):
        if "/studio-" not in f or f in studios_servis:
            continue
        dossier = f.rsplit("/", 1)[0]
        servi = next((s for s in studios_servis if s.rsplit("/", 1)[0] == dossier), None)
        if servi:
            concurrences.setdefault(dossier, {"servi": servi, "ignores": []})["ignores"].append(f)

    bilan = {
        "produits": len(catalogue),
        "rendus_atelier": len(rendus),
        "essais_ignores": len(list(ESSAIS.glob("*" + SUFFIXE))) if ESSAIS.is_dir() else 0,
        "manifeste": len(inscrits),
        "statuts": dict(Counter(l["statut"] for l in lignes)),
        "orphelins_atelier": sorted(set(rendus) - slugs),
        "orphelins_manifeste": sorted(set(inscrits) - slugs),
        "images_orphelines": sorted(sur_disque - servies),
        "images_manquantes": sorted(servies - sur_disque),
        "doublons": {src: s for src, s in empreintes.items() if len(s) > 1},
        "studios_en_concurrence": concurrences,
        "atelier_present": FINAL.is_dir(),
    }
    return lignes, bilan


def section_studios(bilan) -> str:
    """Les photos studio produites que le manifeste ne peut pas servir."""
    concurrences = bilan["studios_en_concurrence"]
    if not concurrences:
        return ""
    parts = [
        "### Photos studio en concurrence (decision humaine)",
        "",
        "Le manifeste ne tient qu'une photo studio par categorie. Les rendus ci-dessous "
        "existent, sont valides, et ne sont servis nulle part : lequel doit representer la "
        "categorie ne se deduit pas des donnees.",
        "",
        "| Categorie | Servie | Ignoree(s) |",
        "|---|---|---|",
    ]
    for dossier, v in sorted(concurrences.items()):
        ignores = "`, `".join(i.rsplit('/', 1)[-1] for i in v['ignores'])
        court = dossier.replace('/images/produits', '')
        servi = v['servi'].rsplit('/', 1)[-1]
        parts.append(f"| `{court}` | `{servi}` | `{ignores}` |")
    return chr(10).join(parts) + chr(10) * 2


def ecrire_rapports(lignes, bilan) -> Path:
    DOCS.mkdir(parents=True, exist_ok=True)
    aujourdhui = date.today().isoformat()

    csv_chemin = DOCS / "IMAGE-MASTER-INVENTORY.csv"
    with csv_chemin.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(lignes)

    a_rendre = [l for l in lignes if l["statut"] in ("NO_RENDER", "INVALID")]
    a_revoir = [l for l in lignes if l["validation"] == "HUMAN_REVIEW"]

    (DOCS / "IMAGE-RECONCILIATION.md").write_text(
        "# Réconciliation des visuels produit\n\n"
        f"Recalculé le {aujourdhui} par `scripts/rendu-3d/auditer_visuels.py`. "
        "Aucun compteur repris d'un document antérieur.\n\n"
        "## État réel\n\n| Mesure | Nombre |\n|---|---|\n"
        f"| Produits au catalogue | {bilan['produits']} |\n"
        f"| Rendus Blender dans `final/` | {bilan['rendus_atelier']} |\n"
        f"| Rendus dans `essais/` (jamais utilisés) | {bilan['essais_ignores']} |\n"
        f"| Entrées du manifeste | {bilan['manifeste']} |\n\n"
        "## Statuts\n\n| Statut | Produits |\n|---|---|\n"
        + "".join(f"| {s} | {n} |\n" for s, n in sorted(bilan["statuts"].items()))
        + "\n## Contrôles transverses\n\n"
        f"- Rendus sans produit au catalogue : **{len(bilan['orphelins_atelier'])}**"
        + (f" — `{'`, `'.join(bilan['orphelins_atelier'][:8])}`\n" if bilan["orphelins_atelier"] else "\n")
        + f"- Entrées de manifeste sans produit : **{len(bilan['orphelins_manifeste'])}**\n"
        f"- Images sur disque que rien ne sert : **{len(bilan['images_orphelines'])}**\n"
        f"- Images servies mais absentes du disque : **{len(bilan['images_manquantes'])}**\n"
        f"- Fichiers servis à plusieurs produits : **{len(bilan['doublons'])}**\n"
        f"- Catégories à plusieurs photos studio : **{len(bilan['studios_en_concurrence'])}**\n\n"
        + section_studios(bilan)
        + "## À valider par un humain\n\n"
        + (
            "Aucun cas.\n"
            if not a_revoir
            else "| Produit | Statut | Pourquoi |\n|---|---|---|\n"
            + "".join(f"| `{l['slug']}` | {l['statut']} | {l['action']} |\n" for l in a_revoir[:40])
        )
        + "\nDétail complet : `IMAGE-MASTER-INVENTORY.csv`.\n",
        encoding="utf-8",
    )

    (DOCS / "PRODUCTS-REQUIRING-BLENDER-RENDER.md").write_text(
        "# Produits sans rendu Blender exploitable\n\n"
        f"Recalculé le {aujourdhui}. **{len(a_rendre)} produit(s)** sur {bilan['produits']}.\n\n"
        + (
            "Aucun : chaque produit a son rendu.\n"
            if not a_rendre
            else "| Slug | Produit | Catégorie | Statut |\n|---|---|---|---|\n"
            + "".join(
                f"| `{l['slug']}` | {l['produit']} | {l['categorie']} | {l['statut']} |\n"
                for l in a_rendre
            )
        ),
        encoding="utf-8",
    )
    return csv_chemin


def main() -> int:
    sortie_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true", help="console seule, aucun rapport ecrit")
    args = ap.parse_args()

    lignes, bilan = auditer()
    if not bilan["atelier_present"]:
        print(f"ATELIER ABSENT : {FINAL}\nAucun rendu ne peut etre audite.", file=sys.stderr)

    print(f"Produits au catalogue      : {bilan['produits']}")
    print(f"Rendus Blender (final/)    : {bilan['rendus_atelier']}")
    print(f"Rendus ignores (essais/)   : {bilan['essais_ignores']}")
    print(f"Entrees du manifeste       : {bilan['manifeste']}")
    print("Statuts :")
    for s, n in sorted(bilan["statuts"].items(), key=lambda x: -x[1]):
        print(f"  {s:<22} {n}")
    print(f"Rendus sans produit        : {len(bilan['orphelins_atelier'])}")
    print(f"Manifeste sans produit     : {len(bilan['orphelins_manifeste'])}")
    print(f"Images orphelines          : {len(bilan['images_orphelines'])}")
    print(f"Images servies absentes    : {len(bilan['images_manquantes'])}")
    print(f"Fichiers partages          : {len(bilan['doublons'])}")

    if not args.resume:
        print(f"\nRapports : {ecrire_rapports(lignes, bilan).parent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
