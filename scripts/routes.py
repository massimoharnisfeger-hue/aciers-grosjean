#!/usr/bin/env python3
"""Les routes que le site sert reellement, lues dans le depot.

Une redirection dont la destination n'existe pas envoie le visiteur sur une 404
avec un code 301 : le lien est perdu deux fois. Pour le verifier sans lancer de
build, il faut savoir ce que Next.js va produire. Ce module le deduit de la
source, exactement comme `generateStaticParams` le fait a la compilation :

  - les pages statiques de `app/` (un `page.tsx` sans segment dynamique) ;
  - `/[univers]/[...segments]` : les `chemin:` de `lib/catalogue.ts` ;
  - `/p/[slug]` : les produits de `lib/catalogue.ts`. Un produit se reconnait a
    sa cle `categorie:` ; les six univers portent eux aussi un `slug:` mais
    n'ont pas de fiche produit — les compter donnait six routes fantomes ;
  - `/conseils|aide|depots|services/[slug]` : les collections de `lib/edito.ts` ;
  - `/catalogue/[univers]` : un chapitre du catalogue visuel par univers.

Partage par `scripts/generer-redirections.py` (qui s'en sert pour reparer) et
par `tests/test_redirections.py` (qui s'en sert pour controler). Une seule
definition : deux copies finiraient par diverger.
"""

import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]

# Collection de `lib/edito.ts` qui alimente chaque route dynamique.
COLLECTIONS_EDITO = {
    "conseils": "articles",
    "services": "servicesDetail",
    "depots": "depotsDetail",
    "aide": "pagesAide",
}


# Routes servies par un fichier de convention plutot que par un `page.tsx`.
FICHIERS_ROUTES = {"robots.ts": "/robots.txt", "sitemap.ts": "/sitemap.xml", "icon.svg": "/icon.svg"}


def _pages_statiques() -> set[str]:
    """Routes de `app/` sans segment dynamique, y compris la racine."""
    app = RACINE / "app"
    routes = set()
    for fichier, route in FICHIERS_ROUTES.items():
        if (app / fichier).exists():
            routes.add(route)
    for page in app.rglob("page.tsx"):
        segments = page.relative_to(app).parent.parts
        if any(s.startswith("[") or s.startswith("(") or s.startswith("@") for s in segments):
            continue
        routes.add("/" + "/".join(segments) if segments else "/")
    return routes


def _bloc(source: str, nom: str) -> str:
    """Le corps litteral de `export const <nom>... = [ ... ]`.

    Decoupe jusqu'au prochain `export const` de premier niveau : les
    collections de `lib/edito.ts` se suivent sans imbrication.
    """
    debut = re.search(rf"^export const {nom}\b[^=]*=\s*\[", source, re.M)
    if not debut:
        return ""
    reste = source[debut.end():]
    suivant = re.search(r"^export const ", reste, re.M)
    return reste[: suivant.start()] if suivant else reste


def _slugs(bloc: str) -> list[str]:
    return re.findall(r'slug:\s*"([^"]+)"', bloc)


def produits_du_catalogue(catalogue: str) -> list[str]:
    """Les slugs qui ont une fiche produit, reconnus a leur cle `categorie:`."""
    return re.findall(r'slug: "([^"]+)", nom: .*?, categorie: "', catalogue)


def univers_du_catalogue(catalogue: str) -> list[str]:
    """Les slugs des six univers, lus dans `export const univers`."""
    return re.findall(r'\{ slug: "([^"]+)", nom:', _bloc(catalogue, "univers"))


def routes_du_depot() -> set[str]:
    """Toutes les routes servies, sous leur forme lisible (sans %XX)."""
    routes = _pages_statiques()

    catalogue = (RACINE / "lib" / "catalogue.ts").read_text(encoding="utf-8")
    routes |= set(re.findall(r'chemin:\s*"(/[^"]*)"', catalogue))
    routes |= {"/p/" + s for s in produits_du_catalogue(catalogue)}

    # `/catalogue/[univers]` : un chapitre du catalogue visuel par univers
    # (app/catalogue/[univers]/page.tsx, `generateStaticParams` sur `univers`).
    if (RACINE / "app" / "catalogue" / "[univers]" / "page.tsx").exists():
        routes |= {"/catalogue/" + s for s in univers_du_catalogue(catalogue)}

    edito = (RACINE / "lib" / "edito.ts").read_text(encoding="utf-8")
    for prefixe, collection in COLLECTIONS_EDITO.items():
        routes |= {f"/{prefixe}/{s}" for s in _slugs(_bloc(edito, collection))}

    return routes


def ancetre_servi(chemin: str, routes: set[str]) -> str | None:
    """Le plus proche parent de `chemin` qui existe vraiment, sinon None.

    `/acier/toles/tole-decapee` n'existe pas ; `/acier/toles` oui. Envoyer le
    visiteur sur la categorie plutot que sur une 404 lui laisse le produit
    voisin sous les yeux. La racine n'est pas un ancetre acceptable : elle ne
    repond pas a la demande, elle l'efface.
    """
    parts = [p for p in chemin.split("/") if p]
    for n in range(len(parts) - 1, 0, -1):
        candidat = "/" + "/".join(parts[:n])
        if candidat in routes:
            return candidat
    return None


if __name__ == "__main__":
    r = routes_du_depot()
    print(f"{len(r)} routes servies")
    for prefixe in ("/", "/acier", "/conseils", "/aide", "/p/"):
        print(f"  {prefixe:<12} {sum(1 for x in r if x.startswith(prefixe))}")
