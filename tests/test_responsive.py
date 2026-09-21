"""Controles responsive lus dans le source, issus du balayage navigateur du 21/09.

Le balayage (`scripts/qa/balayage-responsive.py`, 30 gabarits x 11 largeurs de
320 a 1280 px, Chromium) n'a trouve aucun debordement horizontal : le site est
fluide. Les defauts etaient ailleurs, et invisibles a `scrollWidth` :

R1 - Chevauchement dans la comparaison a 320 px. `grid-cols-3` a toutes les
     largeurs avec `p-5` laisse ~53 px utiles par cellule : « epaisseurs »,
     « d'expertise », « Certification » debordent sur la colonne voisine, et
     l'enveloppe `overflow-hidden` masque le tout a la mesure. Le composant doit
     porter un gabarit mobile explicite (colonnes et remplissage prefixes) et
     autoriser la coupure des mots longs.
R2 - Cibles tactiles sous 24 px : 37 a 46 par page, a TOUTES les largeurs. Ce
     sont les liens du pied de page (14 px de haut), du fil d'Ariane (13 px) et
     du plan du site. Un lien texte doit porter la classe `lien-tactile`, qui
     lui donne une boite d'au moins 24 px sans changer son rendu.
R3 - Lien interne casse : `/services/transformation` (page services) repond
     404. Tout `href` litteral vers le site doit designer une page statique,
     ou un slug connu d'une famille dynamique.

Comme `test_mobile.py`, ces controles lisent le source : verts sans serveur ni
navigateur. La preuve visuelle est dans les captures du balayage.
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
APP = RACINE / "app"
COMPOSANTS = RACINE / "components"

COMPARAISON = COMPOSANTS / "sections" / "Comparaison.tsx"
GLOBALS = APP / "globals.css"
FICHIERS_LIENS_TEXTE = (
    COMPOSANTS / "sections" / "Footer.tsx",
    COMPOSANTS / "ui" / "FilAriane.tsx",
    COMPOSANTS / "ui" / "PageHeader.tsx",
    COMPOSANTS / "ui" / "PageLegale.tsx",
    COMPOSANTS / "catalogue" / "TableauProduits.tsx",
    APP / "plan-du-site" / "page.tsx",
    APP / "nouveautes" / "page.tsx",
    APP / "depots" / "[slug]" / "page.tsx",
    APP / "services" / "[slug]" / "page.tsx",
    APP / "p" / "[slug]" / "page.tsx",
)

# Un lien a une boite suffisante s'il porte la classe tactile, un bouton, ou une
# hauteur / un remplissage vertical explicites (cartes, pastilles, icones).
BOITE_SUFFISANTE = re.compile(r"lien-tactile|btn-cta|btn-ghost|(?<![a-z-])(?:p|py|pt|pb)-[0-9.]+|(?<![a-z-])h-(?:[89]|1[0-9]|full)(?![0-9a-z-])|min-h-")

BALISE_LIEN = re.compile(r"<(?:Link|a)\b[^>]*>", re.DOTALL)
HREF_LITTERAL = re.compile(r'(?:href|h):\s*"(/[^"#?]*)"|href="(/[^"#?]*)"')


def source(chemin: Path) -> str:
    return chemin.read_text(encoding="utf-8")


def sans_prefixe(classe: str, texte: str) -> bool:
    """La classe apparait sans prefixe de point de rupture (sm:, md:, lg:...)."""
    return re.search(rf"(?<![a-z0-9:\[-]){re.escape(classe)}(?![a-z0-9-])", texte) is not None


class ComparaisonMobile(unittest.TestCase):
    """R1 : la comparaison a un gabarit mobile explicite."""

    def test_r1_colonnes_et_remplissage_prefixes(self):
        src = source(COMPARAISON)
        self.assertFalse(
            sans_prefixe("grid-cols-3", src),
            "Comparaison.tsx : `grid-cols-3` sans prefixe s'applique aussi a 320 px, "
            "ou trois colonnes de ~53 px utiles font se chevaucher les mots.",
        )
        self.assertFalse(
            sans_prefixe("p-5", src),
            "Comparaison.tsx : `p-5` (20 px) sans prefixe mange 40 px par cellule a 320 px.",
        )

    def test_r1bis_mots_longs_coupables(self):
        src = source(COMPARAISON)
        self.assertTrue(
            "break-words" in src or "hyphens-auto" in src,
            "Comparaison.tsx : sans `break-words`, « Certification » ou « d'expertise » "
            "ne peuvent pas se couper et sortent de leur cellule.",
        )


class CiblesTactiles(unittest.TestCase):
    """R2 : les liens texte des composants partages ont une boite d'au moins 24 px."""

    def test_r2_classe_definie(self):
        self.assertIn(
            ".lien-tactile",
            source(GLOBALS),
            "globals.css doit definir `.lien-tactile` (inline-flex, min-height 24 px).",
        )

    def test_r2bis_liens_texte_portent_la_classe(self):
        for fichier in FICHIERS_LIENS_TEXTE:
            src = source(fichier)
            fautifs = [
                b[:70].replace("\n", " ")
                for b in BALISE_LIEN.findall(src)
                if not BOITE_SUFFISANTE.search(b)
            ]
            self.assertEqual(
                fautifs,
                [],
                f"{fichier.relative_to(RACINE).as_posix()} : {len(fautifs)} lien(s) sans "
                f"`lien-tactile` : {fautifs[:3]}",
            )


class CompteursMobiles(unittest.TestCase):
    """R4 : un chiffre a 48 px dans une colonne de 140 px se casse en deux lignes.

    Capture du 22/09 a 320 px : « 40 ans » sur deux lignes, « 4 » seul sur la
    sienne, alors que la grille reste a deux colonnes. La taille de police
    mobile doit etre explicite et plus petite que celle du desktop.
    """

    def test_r4_taille_mobile_explicite(self):
        src = source(COMPOSANTS / "fx" / "Counters.tsx")
        self.assertFalse(
            sans_prefixe("text-5xl", src),
            "Counters.tsx : `text-5xl` sans prefixe s'applique a 320 px ou deux chiffres "
            "se partagent 280 px. Ecrire la taille mobile, puis sm:/md: pour les autres.",
        )


class FilsDAriane(unittest.TestCase):
    """R5 : un seul fil d'Ariane, celui qui emet le JSON-LD.

    Quatre gabarits — PageHeader (22 pages), PageLegale, la fiche d'un depot,
    celle d'un service — dessinaient leur fil d'Ariane a la main : meme rendu
    que `FilAriane`, mais sans le `BreadcrumbList` schema.org. Google ne voyait
    donc pas la hierarchie sur la majorite du site. Note comme dette dans
    `_DOCS/QA-RESPONSIVE.md` le 21/09, corrige le 22.

    Verifie aussi qu'aucune page ne cumule deux fils (deux BreadcrumbList sur
    une meme page se contredisent aux yeux d'un moteur).
    """

    def test_r5_aucun_fil_d_ariane_code_a_la_main(self):
        fautifs = []
        for fichier in list(APP.rglob("*.tsx")) + list(COMPOSANTS.rglob("*.tsx")):
            if fichier.name == "FilAriane.tsx":
                continue
            src = source(fichier)
            if re.search(r'<Link href="/"[^>]*>Accueil</Link>', src):
                fautifs.append(fichier.relative_to(RACINE).as_posix())
        self.assertEqual(
            fautifs, [],
            f"fil(s) d'Ariane dessines a la main, donc sans BreadcrumbList : {fautifs}",
        )

    def test_r5bis_jamais_deux_fils_sur_une_page(self):
        cumuls = []
        for fichier in APP.rglob("page.tsx"):
            src = source(fichier)
            if "FilAriane" in src and ("PageHeader" in src or "PageLegale" in src):
                cumuls.append(fichier.relative_to(RACINE).as_posix())
        self.assertEqual(cumuls, [], f"deux fils d'Ariane sur la meme page : {cumuls}")


class LiensInternes(unittest.TestCase):
    """R3 : chaque href litteral vers le site mene a une page qui existe."""

    @staticmethod
    def routes_statiques() -> set[str]:
        routes = set()
        for page in APP.rglob("page.tsx"):
            rel = page.parent.relative_to(APP).as_posix()
            if "[" in rel:
                continue
            routes.add("/" + rel if rel != "." else "/")
        return routes

    @staticmethod
    def slugs_connus() -> set[str]:
        texte = source(RACINE / "lib" / "edito.ts") + source(RACINE / "lib" / "catalogue.ts")
        return set(re.findall(r'slug: "([a-z0-9-]+)"', texte))

    @staticmethod
    def chemins_catalogue() -> set[str]:
        texte = source(RACINE / "lib" / "catalogue.ts")
        return set(re.findall(r'"(/[a-z0-9-]+(?:/[a-z0-9-]+)+)"\s*:', texte)) | set(
            re.findall(r'categorie: "(/[^"]+)"', texte)
        )

    def test_r3_chaque_href_litteral_existe(self):
        statiques = self.routes_statiques()
        slugs = self.slugs_connus()
        catalogue = self.chemins_catalogue()
        familles = {"services", "depots", "conseils", "aide", "p"}
        casses = []
        for fichier in list(APP.rglob("*.tsx")) + list(COMPOSANTS.rglob("*.tsx")):
            for m in HREF_LITTERAL.finditer(source(fichier)):
                href = (m.group(1) or m.group(2)).rstrip("/") or "/"
                if href in statiques or href in catalogue:
                    continue
                parts = href.strip("/").split("/")
                if len(parts) == 2 and parts[0] in familles and parts[1] in slugs:
                    continue
                if len(parts) == 1 and parts[0] in slugs:  # /acier, /inox... (univers)
                    continue
                casses.append(f"{fichier.relative_to(RACINE).as_posix()} -> {href}")
        self.assertEqual(casses, [], "hrefs litteraux sans page : " + str(casses[:6]))


if __name__ == "__main__":
    unittest.main()
