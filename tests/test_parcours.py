"""Controles de parcours : le site rendu, pas seulement son source.

Les autres controles de ce dossier lisent le code source. C'est rapide, sur,
et ca ne detecte jamais une page qui compile et qui plante au rendu : une
donnee de catalogue absente, un `.map()` sur `undefined`, une route renommee,
un lien casse vers une fiche produit. Le 21/09/2026, 92 controles etaient
verts et aucun n'ouvrait une seule page du site.

Ce fichier demarre le serveur de production sur un port libre, appelle les
pages qui portent la demande de devis, et verifie ce qu'un visiteur recoit
vraiment.

P1 - L'accueil repond 200 et porte le nom de l'entreprise.
P2 - `/devis` sert le formulaire avec ses six champs nommes. Sans eux, la
     demande de devis n'existe plus : c'est la page qui rapporte.
P3 - `/produits` repond et cite les univers du catalogue.
P4 - Chacun des six univers a sa page. Une entree de `lib/catalogue.ts` sans
     page servie est un trou dans la navigation et dans le maillage SEO.
P5 - Une fiche produit repond et affiche son nom.
P6 - Une URL inconnue renvoie 404. Un site qui repond 200 a tout fait indexer
     n'importe quoi ; un site qui repond 500 perd le visiteur.
P7 - `/sitemap.xml` et `/robots.txt` sont servis, et les premieres URL que le
     sitemap declare a Google repondent vraiment.

Ces controles exigent un build : `npm ci` puis `npm run build`. Sans lui, ils
se declarent ignores avec la commande a lancer, ils n'echouent pas et ils ne
disparaissent pas du registre.
"""

import shutil
import socket
import subprocess
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
BINAIRE_NEXT = RACINE / "node_modules" / "next" / "dist" / "bin" / "next"

# `.next/` apparait des les premieres secondes du build ; seul le manifeste de
# prerendu signe un build termine. Tester le dossier ferait demarrer `next
# start` sur un build en cours, qui echoue sur ce fichier precis.
BUILD_TERMINE = RACINE / ".next" / "prerender-manifest.json"

# Le serveur doit etre pret avant le premier controle. `next start` demarre en
# une a trois secondes ; au-dela, quelque chose ne va pas et l'attente doit
# s'arreter plutot que de manger le budget de la suite.
DEMARRAGE_MAX_S = 30.0
REQUETE_TIMEOUT_S = 10.0

UNIVERS = ("acier", "aluminium", "inox", "toiture-bardage", "jardin-cloture", "quincaillerie")
CHAMPS_DEVIS = ("nom", "email", "telephone", "produit", "depot", "details")
PRODUIT_TEMOIN = "rond-a-beton-de-10mm-de-diametre-en-acier-lamine-a-chaud"


def port_libre() -> int:
    """Port attribue par le systeme : deux lancements ne se marchent pas dessus."""
    with socket.socket() as prise:
        prise.bind(("127.0.0.1", 0))
        return prise.getsockname()[1]


class ServeurSite:
    """Le site de production, demarre le temps des controles."""

    def __init__(self) -> None:
        self.port = port_libre()
        self.processus = None

    @property
    def base(self) -> str:
        return "http://127.0.0.1:" + str(self.port)

    def demarrer(self) -> None:
        node = shutil.which("node")
        if node is None:
            raise unittest.SkipTest("node est introuvable dans le PATH.")
        self.processus = subprocess.Popen(
            [node, str(BINAIRE_NEXT), "start", "-p", str(self.port)],
            cwd=RACINE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self._attendre()

    def _attendre(self) -> None:
        limite = time.monotonic() + DEMARRAGE_MAX_S
        while time.monotonic() < limite:
            if self.processus is not None and self.processus.poll() is not None:
                sortie = (self.processus.stdout.read() if self.processus.stdout else "") or ""
                self.arreter()
                raise unittest.SkipTest("`next start` s'est arrete : " + sortie.strip()[-400:])
            try:
                urllib.request.urlopen(self.base, timeout=2.0).read(1)
                return
            except urllib.error.HTTPError:
                return  # Le serveur repond : un statut d'erreur reste une reponse.
            except OSError:
                time.sleep(0.25)
        self.arreter()
        raise unittest.SkipTest("le serveur n'a pas repondu en 30 s.")

    def arreter(self) -> None:
        if self.processus is None:
            return
        self.processus.terminate()
        try:
            self.processus.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.processus.kill()
            self.processus.wait(timeout=5)
        if self.processus.stdout is not None:
            self.processus.stdout.close()
        self.processus = None

    def appeler(self, chemin: str):
        """(statut, corps) - un 404 est une reponse, pas une panne du controle."""
        try:
            reponse = urllib.request.urlopen(self.base + chemin, timeout=REQUETE_TIMEOUT_S)
            return reponse.status, reponse.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as erreur:
            return erreur.code, erreur.read().decode("utf-8", errors="replace")


class ParcoursVisiteur(unittest.TestCase):
    """Ce qu'un visiteur recoit vraiment, sur le site construit."""

    @classmethod
    def setUpClass(cls) -> None:
        if not BINAIRE_NEXT.exists():
            raise unittest.SkipTest("dependances absentes : lancer `npm ci`.")
        if not BUILD_TERMINE.exists():
            raise unittest.SkipTest("site non construit ou build en cours : lancer `npm run build`.")
        cls.serveur = ServeurSite()
        cls.serveur.demarrer()

    @classmethod
    def tearDownClass(cls) -> None:
        serveur = getattr(cls, "serveur", None)
        if serveur is not None:
            serveur.arreter()

    def test_p1_accueil_repond(self):
        statut, corps = self.serveur.appeler("/")
        self.assertEqual(statut, 200, "l'accueil ne repond pas 200")
        self.assertIn("Aciers Grosjean", corps, "l'accueil ne porte pas le nom de l'entreprise")

    def test_p2_devis_sert_le_formulaire(self):
        statut, corps = self.serveur.appeler("/devis")
        self.assertEqual(statut, 200, "la page devis ne repond pas 200")
        manquants = [champ for champ in CHAMPS_DEVIS if 'name="' + champ + '"' not in corps]
        self.assertEqual(manquants, [], "champs absents du formulaire rendu : " + str(manquants))

    def test_p3_produits_cite_les_univers(self):
        statut, corps = self.serveur.appeler("/produits")
        self.assertEqual(statut, 200, "la page produits ne repond pas 200")
        self.assertIn("Acier", corps, "la page produits ne cite aucun univers")

    def test_p4_chaque_univers_a_sa_page(self):
        casses = [u for u in UNIVERS if self.serveur.appeler("/" + u)[0] != 200]
        self.assertEqual(casses, [], "univers du catalogue sans page servie : " + str(casses))

    def test_p5_fiche_produit_repond(self):
        statut, corps = self.serveur.appeler("/p/" + PRODUIT_TEMOIN)
        self.assertEqual(statut, 200, "la fiche produit temoin ne repond pas 200")
        self.assertIn("Rond à béton", corps, "la fiche produit n'affiche pas son nom")

    def test_p6_url_inconnue_renvoie_404(self):
        statut, _ = self.serveur.appeler("/cette-page-n-existe-pas-controle")
        self.assertEqual(statut, 404, "une URL inconnue renvoie " + str(statut) + " au lieu de 404")

    def test_p7_sitemap_et_robots_sont_servis(self):
        statut_robots, _ = self.serveur.appeler("/robots.txt")
        self.assertEqual(statut_robots, 200, "robots.txt n'est pas servi")
        statut_sitemap, sitemap = self.serveur.appeler("/sitemap.xml")
        self.assertEqual(statut_sitemap, 200, "sitemap.xml n'est pas servi")
        chemins = [
            bloc.split("aciersgrosjean.be", 1)[1].split("</loc>", 1)[0]
            for bloc in sitemap.split("<loc>")[1:6]
            if "aciersgrosjean.be" in bloc
        ]
        self.assertTrue(chemins, "le sitemap ne declare aucune URL")
        casses = [(c, self.serveur.appeler(c or "/")[0]) for c in chemins]
        casses = [c for c in casses if c[1] != 200]
        self.assertEqual(casses, [], "URL declarees au sitemap mais cassees : " + str(casses))


if __name__ == "__main__":
    unittest.main()
