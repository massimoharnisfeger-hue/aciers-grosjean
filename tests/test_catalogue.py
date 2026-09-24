"""Controles du catalogue visuel (/catalogue) : ce que le visiteur recoit vraiment.

Le catalogue visuel presente les 495 produits par chapitre (un par univers),
chaque variante avec son rendu 3D aux cotes et un lien vers sa fiche. Sa regle
premiere : ne montrer que des visuels valides, associes au bon produit. Les
controles K1 a K7 lisent le site construit ; K8 et K9 lisent le source.

K1 - `/catalogue` repond 200 et renvoie vers les six chapitres.
K2 - Chaque chapitre repond 200 et porte le nom de son univers.
K3 - L'ensemble des fiches liees depuis les six chapitres est exactement
     l'ensemble des produits du catalogue, chaque produit une fois : rien
     d'oublie, rien d'invente, rien en double.
K4 - Toute image servie par le catalogue vient du manifeste des visuels
     (`lib/visuels-produits.json`), et la planche d'un produit porte l'image de
     CE produit. Ni dessin generique, ni image d'un autre produit, ni image
     etrangere au manifeste.
K5 - Un produit sans visuel au manifeste montre « Visuel a completer » et
     aucune image : un emplacement honnete vaut mieux qu'un remplissage.
K6 - Chaque image porte width, height et alt : la place est reservee avant le
     chargement (pas de saut de mise en page) et le lecteur d'ecran a un texte.
K7 - Aucun « undefined », « null » ou « NaN » ne fuit dans le HTML : une donnee
     absente s'omet, elle ne s'affiche pas.
K8 - `scripts/routes.py` connait `/catalogue` et ses chapitres : sans cela, le
     controle des redirections (RD1) et la deduction des routes servies (P11)
     ignoreraient ces pages.
K9 - Les composants du catalogue n'importent pas les illustrations SVG de
     famille (`components/art`) : la regle « pas d'image generique » est
     structurelle, pas seulement verifiee au rendu.

Comme `test_parcours.py`, les controles K1-K7 exigent un build ; sans lui,
ils se declarent ignores et ne disparaissent pas du registre.
"""

import json
import os
import re
import sys
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scripts.routes import produits_du_catalogue, routes_du_depot, univers_du_catalogue  # noqa: E402
from test_parcours import BINAIRE_NEXT, BUILD_TERMINE, ServeurSite  # noqa: E402

ENV_LOCAL = RACINE / ".env.local"
MANIFESTE = RACINE / "lib" / "visuels-produits.json"


def catalogue_local_actif() -> bool:
    """Le catalogue n'est construit que derrière `CATALOGUE_LOCAL=oui` (ADR-0010).

    Sans le drapeau — en CI, sur Vercel, ou sur un poste qui ne l'a pas posé —
    les pages répondent 404 par décision, pas par défaut : K1 à K7 se retirent
    alors sans disparaître du registre.
    """
    if os.environ.get("CATALOGUE_LOCAL") == "oui":
        return True
    if not ENV_LOCAL.exists():
        return False
    return re.search(r"^\s*CATALOGUE_LOCAL\s*=\s*oui\s*$", ENV_LOCAL.read_text(encoding="utf-8"), re.M) is not None
CATALOGUE = RACINE / "lib" / "catalogue.ts"
FICHIERS_CATALOGUE = (
    RACINE / "app" / "catalogue" / "page.tsx",
    RACINE / "app" / "catalogue" / "[univers]" / "page.tsx",
    RACINE / "components" / "catalogue" / "FicheFamille.tsx",
    RACINE / "components" / "catalogue" / "PlancheVariante.tsx",
    RACINE / "lib" / "catalogue-visuel.ts",
)

BALISE_IMG = re.compile(r"<img\b[^>]*>", re.DOTALL)
ATTRIBUT = re.compile(r'\b([a-zA-Z-]+)="([^"]*)"')
PLANCHE = re.compile(r"<li[^>]*\bdata-variante\b[^>]*>(.*?)</li>", re.DOTALL)
LIEN_FICHE = re.compile(r'href="/p/([^"#?]+)"')
FUITES = re.compile(r">[^<]*\b(undefined|NaN|null)\b[^<]*<")
SCRIPTS = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL)


def taille_webp(chemin: Path):
    """(largeur, hauteur) d'un WebP lue dans son en-tête (VP8, VP8L ou VP8X), sans dépendance."""
    with open(chemin, "rb") as f:
        d = f.read(30)
    if d[:4] != b"RIFF" or d[8:12] != b"WEBP":
        return None
    bloc = d[12:16]
    if bloc == b"VP8X":
        return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    if bloc == b"VP8L":
        b = int.from_bytes(d[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    if bloc == b"VP8 ":
        return int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF
    return None


def attributs(balise: str) -> dict:
    return {k: unescape(v) for k, v in ATTRIBUT.findall(balise)}


def source_image(src: str) -> str:
    """Le chemin d'origine d'une image, que Next l'ait optimisee ou non."""
    if src.startswith("/_next/image"):
        return parse_qs(urlparse(src).query).get("url", [""])[0]
    return src


class CatalogueRendu(unittest.TestCase):
    """K1-K7 : le catalogue tel qu'il est servi."""

    @classmethod
    def setUpClass(cls) -> None:
        if not BINAIRE_NEXT.exists():
            raise unittest.SkipTest("dependances absentes : lancer `npm ci`.")
        if not BUILD_TERMINE.exists():
            raise unittest.SkipTest("site non construit ou build en cours : lancer `npm run build`.")
        if not catalogue_local_actif():
            raise unittest.SkipTest("catalogue local inactif : poser CATALOGUE_LOCAL=oui dans .env.local (ADR-0010).")
        cls.manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8"))
        cls.univers = univers_du_catalogue(CATALOGUE.read_text(encoding="utf-8"))
        cls.serveur = ServeurSite()
        cls.serveur.demarrer()
        cls.chapitres = {}
        for u in cls.univers:
            statut, corps = cls.serveur.appeler("/catalogue/" + u)
            cls.chapitres[u] = (statut, corps)

    @classmethod
    def tearDownClass(cls) -> None:
        serveur = getattr(cls, "serveur", None)
        if serveur is not None:
            serveur.arreter()

    def test_k1_la_couverture_renvoie_vers_les_six_chapitres(self):
        statut, corps = self.serveur.appeler("/catalogue")
        self.assertEqual(statut, 200, "/catalogue ne repond pas 200")
        self.assertIn("Catalogue produits", corps, "la couverture ne porte pas son titre")
        absents = [u for u in self.univers if f'href="/catalogue/{u}"' not in corps]
        self.assertEqual(absents, [], "chapitres sans lien depuis la couverture : " + str(absents))

    def test_k2_chaque_chapitre_repond(self):
        casses = [u for u, (statut, _) in self.chapitres.items() if statut != 200]
        self.assertEqual(casses, [], "chapitres qui ne repondent pas 200 : " + str(casses))

    def test_k3_chaque_produit_une_fois_et_une_seule(self):
        attendus = set(produits_du_catalogue(CATALOGUE.read_text(encoding="utf-8")))
        vus = {}
        for u, (_, corps) in self.chapitres.items():
            for planche in PLANCHE.findall(corps):
                for slug in LIEN_FICHE.findall(planche):
                    vus[slug] = vus.get(slug, 0) + 1
        manquants = sorted(attendus - set(vus))
        inconnus = sorted(set(vus) - attendus)
        doubles = sorted(s for s, n in vus.items() if n > 1)
        self.assertEqual(manquants, [], f"{len(manquants)} produit(s) absents du catalogue : {manquants[:5]}")
        self.assertEqual(inconnus, [], "fiches liees qui ne sont pas des produits : " + str(inconnus[:5]))
        self.assertEqual(doubles, [], "produits presentes plusieurs fois : " + str(doubles[:5]))

    def test_k4_chaque_image_vient_du_manifeste_et_designe_son_produit(self):
        autorisees = {e["src"] for e in self.manifeste["produits"].values()} | {
            e["src"] for e in self.manifeste["categories"].values()
        }
        etrangeres = []
        mal_associees = []
        _, couverture = self.serveur.appeler("/catalogue")
        pages = [("/catalogue", couverture)] + [("/catalogue/" + u, corps) for u, (_, corps) in self.chapitres.items()]
        for chemin, corps in pages:
            for balise in BALISE_IMG.findall(corps):
                src = source_image(attributs(balise).get("src", ""))
                if src not in autorisees:
                    etrangeres.append(f"{chemin} -> {src}")
            for planche in PLANCHE.findall(corps):
                slugs = LIEN_FICHE.findall(planche)
                images = [source_image(attributs(b).get("src", "")) for b in BALISE_IMG.findall(planche)]
                if not slugs or not images:
                    continue
                attendu = self.manifeste["produits"].get(slugs[0], {}).get("src")
                if images != [attendu]:
                    mal_associees.append(f"{slugs[0]} -> {images}")
        self.assertEqual(etrangeres, [], "images hors manifeste : " + str(etrangeres[:5]))
        self.assertEqual(mal_associees, [], "planches portant l'image d'un autre produit : " + str(mal_associees[:5]))

    def test_k5_un_produit_sans_visuel_le_dit_sans_image(self):
        sans_visuel = set(produits_du_catalogue(CATALOGUE.read_text(encoding="utf-8"))) - set(
            self.manifeste["produits"]
        )
        fautives = []
        vus = set()
        for _, (_, corps) in self.chapitres.items():
            for planche in PLANCHE.findall(corps):
                slugs = LIEN_FICHE.findall(planche)
                if not slugs or slugs[0] not in sans_visuel:
                    continue
                vus.add(slugs[0])
                if BALISE_IMG.search(planche) or "Visuel à compléter" not in unescape(planche):
                    fautives.append(slugs[0])
        self.assertEqual(vus, sans_visuel, "produits sans visuel non retrouves dans les chapitres")
        self.assertEqual(fautives, [], "produits sans visuel qui montrent une image ou cachent le manque : " + str(fautives[:5]))

    def test_k6_chaque_image_a_ses_dimensions_et_un_alt(self):
        incompletes = []
        for u, (_, corps) in self.chapitres.items():
            for balise in BALISE_IMG.findall(corps):
                a = attributs(balise)
                if not (a.get("width") and a.get("height") and a.get("alt")):
                    incompletes.append(f"{u} -> {a.get('src', '?')[:80]}")
        self.assertEqual(incompletes, [], "images sans width/height/alt : " + str(incompletes[:5]))

    def test_k7_aucune_donnee_absente_ne_fuit(self):
        fuites = []
        for u, (_, corps) in self.chapitres.items():
            # La charge utile React (`self.__next_f.push`) est du JSON, ou `null`
            # est un mot legitime : seul le texte que le visiteur lit compte.
            visible = SCRIPTS.sub("", corps)
            for m in FUITES.finditer(visible):
                fuites.append(f"{u} -> {m.group(0)[:60]}")
        self.assertEqual(fuites, [], "textes « undefined/null/NaN » servis : " + str(fuites[:5]))


class CatalogueSource(unittest.TestCase):
    """K8-K9 : ce que le depot garantit sans build."""

    def test_k8_les_routes_du_depot_connaissent_le_catalogue(self):
        routes = routes_du_depot()
        self.assertIn("/catalogue", routes, "scripts/routes.py ignore /catalogue")
        manquants = [u for u in univers_du_catalogue(CATALOGUE.read_text(encoding="utf-8")) if "/catalogue/" + u not in routes]
        self.assertEqual(manquants, [], "chapitres inconnus de scripts/routes.py : " + str(manquants))

    def test_k12_l_integration_sert_l_image_entiere(self):
        """`integrer_visuels.py` sert l'image de fiche entière : la pièce et sa fiche technique (ADR-0012).

        22/09 : la fiche incrustée était retirée du fichier servi (`recadrer_visuels.py`, à la main) ; 23/09 :
        l'intégration recadrait elle-même (L-051). 24/09, le propriétaire devant l'image servie : « je veux une photo
        entière, pas juste la moitié », mesures comprises. Contrôle de structure, pas de mot (L-051) : `copier()` copie
        le fichier tel quel, sans recadrage, et l'intégration n'importe plus le recadrage."""
        source = (RACINE / "scripts" / "rendu-3d" / "integrer_visuels.py").read_text(encoding="utf-8")
        copier = source.split("def copier(", 1)[1].split("\ndef ", 1)[0] if "def copier(" in source else ""
        self.assertIn("shutil.copyfile(source, chemin)", copier, "copier() ne copie plus le visuel tel quel")
        for motif in ("recadrer_sur_place(", ".crop(", "recadrer_visuels"):
            self.assertNotIn(motif, copier, f"copier() recadre encore le visuel servi ({motif})")
        self.assertNotRegex(source, r"(?m)^import recadrer_visuels\b", "integrer_visuels.py importe encore le recadrage")

    def test_k13_chaque_visuel_servi_est_entier_et_le_manifeste_le_dit(self):
        """Toute image de fiche servie est le rendu habillé entier, pièce et fiche technique (ADR-0012) : 1600 × 1200,
        ou 2400 × 1800 pour les barres, profilés et tubes refaits le 24/09 ; le manifeste réserve exactement cette
        place. Plus aucune image recadrée (984 × 1133). Lecture de l'en-tête WebP sans Pillow : tourne aussi en CI."""
        manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8"))
        attendus = {(1600, 1200), (2400, 1800)}
        fautifs = []
        for slug, e in manifeste["produits"].items():
            chemin = RACINE / "public" / e["src"].lstrip("/")
            if not chemin.exists():
                fautifs.append(f"{slug} : fichier absent")
                continue
            taille = taille_webp(chemin)
            if taille not in attendus:
                fautifs.append(f"{slug} : fichier {taille}")
            if (e["largeur"], e["hauteur"]) != taille:
                fautifs.append(f"{slug} : manifeste {e['largeur']} x {e['hauteur']} pour un fichier {taille}")
        self.assertEqual(fautifs, [], f"{len(fautifs)} visuel(s) servi(s) non entier(s) : {fautifs[:5]}")

    def test_k10_aucun_lien_vers_le_catalogue_sans_le_verrou(self):
        """Tant que le catalogue n'est pas validé, aucune page publique n'y mène.

        Les liens vivent dans le menu (prop `catalogueLocal`), le pied de page,
        `/produits`, `/plan-du-site` et le sitemap : chacun doit lire le verrou.
        Un lien oublié enverrait le visiteur de Vercel sur une 404.
        """
        fautifs = []
        for fichier in (
            RACINE / "components" / "ui" / "Nav.tsx",
            RACINE / "components" / "sections" / "Footer.tsx",
            RACINE / "app" / "produits" / "page.tsx",
            RACINE / "app" / "plan-du-site" / "page.tsx",
            RACINE / "app" / "sitemap.ts",
        ):
            src = fichier.read_text(encoding="utf-8")
            if '"/catalogue"' in src and "catalogueActif" not in src and "catalogueLocal" not in src:
                fautifs.append(fichier.relative_to(RACINE).as_posix())
        self.assertEqual(fautifs, [], "liens vers /catalogue hors du verrou CATALOGUE_LOCAL : " + str(fautifs))

    def test_k11_chaque_page_du_catalogue_lit_le_verrou(self):
        fautifs = []
        for fichier in (
            RACINE / "app" / "catalogue" / "page.tsx",
            RACINE / "app" / "catalogue" / "[univers]" / "page.tsx",
            RACINE / "app" / "catalogue" / "imprimer" / "page.tsx",
        ):
            src = fichier.read_text(encoding="utf-8") if fichier.exists() else ""
            if "catalogueActif" not in src or "notFound" not in src:
                fautifs.append(fichier.relative_to(RACINE).as_posix())
        self.assertEqual(fautifs, [], "pages du catalogue servies sans lire le verrou : " + str(fautifs))

    def test_k9_le_catalogue_n_importe_aucune_illustration_generique(self):
        fautifs = [
            f.relative_to(RACINE).as_posix()
            for f in FICHIERS_CATALOGUE
            if f.exists() and "components/art" in f.read_text(encoding="utf-8")
        ]
        self.assertEqual(fautifs, [], "le catalogue importe une illustration SVG de famille : " + str(fautifs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
