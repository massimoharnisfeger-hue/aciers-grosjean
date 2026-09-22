#!/usr/bin/env python3
"""Regenere `lib/redirections.mjs` depuis le relevé d'URLs du site actuel.

Source : `_DOCS/catalogue-site-actuel/inventaire-urls.csv`, colonnes `Chemin`
(l'ancienne URL) et `URL_cible_recommandee` (la cible proposée par le
blueprint). Une ligne devient une redirection 301 sauf si :

  - la cible est le chemin lui-même (« conserver ») ;
  - la cible n'est pas une URL (« (retirer du catalogue public) », « -404 »).

665 lignes, 13 écartées, 652 redirections.

Pourquoi ce script existe
-------------------------
Il n'existait pas. `lib/redirections.mjs` portait pourtant l'en-tête « GÉNÉRÉ,
NE PAS ÉDITER À LA MAIN — Générateur : scripts/generer-redirections.py », et ce
générateur était un commentaire de trois lignes. Le fichier était tenu à la
main sous une étiquette qui disait le contraire.

Conséquence mesurée le 22/09/2026 : 15 des 622 destinations ne menaient nulle
part, atteintes par 22 anciennes URLs. Le blueprint proposait des pages « à
réalimenter ou fusionner » — `/acier/poutrelles/hem`, `/commande`,
`/compte/profil`… — qui n'ont jamais été construites, et ces cibles avaient été
reprises telles quelles. Le visiteur recevait un 301 puis une 404 : le lien
entrant était perdu deux fois.

Une cible morte n'est donc plus recopiée : elle est réparée ici, à la
génération, et `tests/test_redirections.py` (RD1, RD4) refuse le contraire.

Usage :
    python scripts/generer-redirections.py             (réécrit le fichier)
    python scripts/generer-redirections.py --verifier   (compare, n'écrit pas)
"""

import csv
import sys
from pathlib import Path
from urllib.parse import quote

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "scripts"))

from routes import ancetre_servi, routes_du_depot  # noqa: E402

RELEVE = RACINE / "_DOCS" / "catalogue-site-actuel" / "inventaire-urls.csv"
SORTIE = RACINE / "lib" / "redirections.mjs"

# Cibles du blueprint qui n'ont pas d'ancêtre utile : leur équivalent servi
# porte un autre nom. Chaque ligne est vérifiable — la page de droite existe
# et répond à la demande de gauche.
REPARATIONS = {
    "/commande": "/panier",                          # le tunnel s'arrête au panier
    "/compte/profil": "/compte/connexion",           # les pages de compte sont
    "/compte/commandes": "/compte/connexion",        # derrière la connexion :
    "/compte/listes": "/compte/connexion",           # sans elle il n'y a rien
    "/compte/recemment-vus": "/compte/connexion",    # à montrer
    "/conseils/rss.xml": "/conseils",                # aucun flux n'est publié
    "/documentation/toiture-bardage": "/documentation",
    "/livraison-retrait": "/aide/livraison-retrait",  # même contenu, sous /aide
}


def encoder(chemin: str) -> str:
    """La forme sous laquelle Next.js voit l'URL : percent-encodée en UTF-8.

    381 des 652 anciennes URLs contiennent des accents. Next compare le chemin
    tel qu'il arrive ; déclarer `/tôle-décapée` ne déclencherait rien.
    """
    return quote(chemin, safe="/-_.~")


def reparer(cible: str, routes: set[str]) -> tuple[str, str]:
    """La cible si elle est servie, sinon la page servie la plus proche.

    Retourne (destination, motif). Lève si rien ne peut être proposé : mieux
    vaut un générateur qui s'arrête qu'une redirection vers une 404.
    """
    if cible in routes:
        return cible, ""
    if cible in REPARATIONS:
        remplacante = REPARATIONS[cible]
        if remplacante not in routes:
            raise SystemExit(f"REPARATIONS vise une page absente : {remplacante}")
        return remplacante, "table"
    ancetre = ancetre_servi(cible, routes)
    if ancetre:
        return ancetre, "ancetre"
    raise SystemExit(
        f"Destination morte sans reparation possible : {cible}. "
        "Ajouter une entree dans REPARATIONS ou creer la page."
    )


def lire() -> list[dict]:
    if not RELEVE.exists():
        raise SystemExit(
            f"Releve introuvable : {RELEVE}\n"
            "Colonnes attendues : Chemin ; URL_cible_recommandee (separateur ';')."
        )
    with RELEVE.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def construire() -> tuple[str, list[tuple[str, str, str]]]:
    routes = routes_du_depot()
    entrees, reparees = [], []
    for ligne in lire():
        chemin = (ligne.get("Chemin") or "").strip()
        cible = (ligne.get("URL_cible_recommandee") or "").strip()
        if not chemin or not cible.startswith("/") or cible == chemin:
            continue
        destination, motif = reparer(cible, routes)
        if motif:
            reparees.append((chemin, cible, destination))
        entrees.append((encoder(chemin), destination))

    accentuees = sum(1 for s, _ in entrees if "%" in s)
    lignes = [
        "/**",
        " * Redirections 301 — GÉNÉRÉ, NE PAS ÉDITER À LA MAIN.",
        " * Générateur : scripts/generer-redirections.py",
        " *",
        " * Une entrée par ancienne URL du site (colonne Chemin du relevé) vers son URL",
        " * propre (colonne URL_cible_recommandee). Sans ces redirections, la refonte",
        " * perdrait les 2 103 backlinks et les positions acquises.",
        " *",
        f" * {accentuees} des {len(entrees)} sources contiennent des accents. Next.js compare le chemin",
        " * tel qu'il arrive, c'est-à-dire encodé en pourcent : les sources sont donc",
        " * déclarées sous leur forme encodée, pas sous leur forme lisible.",
        " *",
        f" * {len(reparees)} cibles du relevé désignaient des pages jamais construites. Le",
        " * générateur les remplace par la page servie la plus proche : un 301 vers une",
        " * 404 perd le visiteur et le lien entrant. Contrôles RD1 et RD4.",
        " */",
        "export const redirections = [",
    ]
    for source, destination in entrees:
        lignes.append('  { source: "' + source + '", destination: "' + destination + '" },')
    lignes.append("];")
    return chr(10).join(lignes) + chr(10), reparees


def main(argv: list[str]) -> int:
    contenu, reparees = construire()
    verifier = "--verifier" in argv

    if verifier:
        actuel = SORTIE.read_text(encoding="utf-8") if SORTIE.exists() else ""
        if actuel != contenu:
            print(f"{SORTIE.name} differe de ce que le generateur produit.")
            print("Relancer : python scripts/generer-redirections.py")
            return 1
        print(f"{SORTIE.name} est conforme a son generateur.")
        return 0

    SORTIE.write_text(contenu, encoding="utf-8")
    nb = contenu.count("{ source:")
    print(f"{SORTIE.relative_to(RACINE)} : {nb} redirections ecrites.")
    if reparees:
        print(f"{len(reparees)} cibles mortes reparees :")
        for chemin, cible, destination in reparees:
            print(f"   {chemin}  ->  {cible}  devient  {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
