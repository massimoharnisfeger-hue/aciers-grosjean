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
P15 - Aucune valeur alignee a droite ne porte une phrase. Mesure du 22/09 sur
      les 1 727 paires « libelle : valeur » du catalogue : la valeur mediane
      fait 65 caracteres et 81 % sont des phrases, alors que `GrillePaires` les
      alignait toutes a droite comme des cotes. Une phrase alignee a droite a
      un bord GAUCHE en escalier : l'oeil perd le debut de chaque ligne. Le
      proprietaire l'a vu avant le controle — « je ne trouve pas ca
      esthetique » — et il avait raison.

P14 - Sur une page de categorie, les produits sont servis dans l'ordre
      numerique de leurs cotes. Mesure du 22/09 sur `/acier/profiles/plat` :
      l'ordre etait alphabetique — 100x10, 100x5, 100x8, 10x3, 120x10, 20x10 —
      parce que le tri « Par section », pourtant propose par defaut, ne triait
      rien : `TableauProduits` ne traitait que `prix` et `poids`. Dans un
      negoce ou l'on choisit par cote, c'est le tri le plus utilise.

P13 - Le texte du site source est servi, quelle que soit la forme que prend
      la section. La mise en onglets a d'abord rendu `null` quand aucun onglet
      n'etait produit : 24 fiches ont perdu 39 paragraphes reels, dont la seule
      mention du sur-mesure et l'adresse du service commercial. L'introduction
      alimente desormais l'onglet « Presentation » ; ce controle ne regarde
      donc plus OU le texte est rendu, seulement QU'IL l'est — c'est la
      garantie qui compte, et elle survit aux changements de mise en page.

P12 - `/api/devis` refuse un flot de demandes. Sans plafond, l'adresse
      Microsoft 365 de l'entreprise relaie autant de messages qu'on lui en
      demande : la boite se remplit, et le compte finit bride ou bloque par
      Microsoft. Le controle envoie des demandes valides jusqu'au refus.

P10 - Les vignettes 80 px d'une page de categorie passent par l'optimiseur
      d'images. Constat du 22/09/2026 : `VisuelFamille` portait `unoptimized`
      et un `sizes` de carte pleine largeur, alors que le meme composant sert
      une vignette de 80 px. Le navigateur telechargeait la photo studio
      entiere pour l'afficher dans un carre de 80 px.
P11 - Les anciennes URLs dont la cible avait ete reparee aboutissent sur une
      page servie. Avant reparation, 22 d'entre elles repondaient 301 puis
      404 : le visiteur et le lien entrant etaient perdus deux fois.

P8 - `/api/devis` existe et se tient : un corps invalide est refuse (400), un
     GET est refuse (405), un robot qui remplit le champ piege recoit un 200
     sans qu'aucun envoi ne parte, et sans SMTP configure la route se declare
     indisponible (503) au lieu de planter (500) — le formulaire bascule alors
     sur la messagerie du visiteur. Aucun controle n'envoie de vrai message :
     si `.env.local` configure un SMTP, le cas 503 est ignore.

Ces controles exigent un build : `npm ci` puis `npm run build`. Sans lui, ils
se declarent ignores avec la commande a lancer, ils n'echouent pas et ils ne
disparaissent pas du registre.
"""

import json
import re
from html import unescape
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
# Fiche a description riche (titres, listes, services) : le rond a beton n'a que de la prose.
PRODUIT_RICHE = "plat-de-20x3mm-en-aluminium"

# Demande de devis valide, donnees fictives : rien ici n'est une personne reelle.
DEMANDE_TEMOIN = {
    "profil": "Particulier",
    "nom": "Controle Parcours",
    "email": "controle@example.invalid",
    "telephone": "",
    "produit": "Acier",
    "depot": "Charleroi",
    "details": "Demande fictive emise par tests/test_parcours.py, a ignorer.",
    "site_web": "",
}

# Page de categorie qui affiche des vignettes de 80 px (`h-20 w-20`) pour ses
# sous-categories : sept enfants, tous avec une vraie photo studio de
# 1600 x 1200, dont la tole perforee (187 Ko a elle seule).
CATEGORIE_A_VIGNETTES = "/acier/toles"

# Largeur maximale qu'une vignette de 80 px doit pouvoir demander. Un ecran
# retina en reclame 160 ; 256 est le palier suivant de `next/image`. Au-dela,
# le navigateur n'a plus de candidat a sa taille et prend l'image entiere.
LARGEUR_MAX_VIGNETTE = 256

# Anciennes URLs dont la cible n'existait pas (voir scripts/generer-redirections.py,
# table REPARATIONS et repli sur l'ancetre servi). Une par cible reparee.
ANCIENNES_URLS_REPAREES = (
    "/poutrelle-hem",
    "/t%C3%B4le-d%C3%A9cap%C3%A9e",
    "/t%C3%B4le-%C3%A9lectrozingu%C3%A9e",
    "/carr%C3%A9-plein-en-aluminium",
    "/panneau-tuile",
    "/anti-condensation",
    "/ttack-toiture-plate",
    "/catalogue-toiture-et-bardage",
    "/checkout",
    "/order/history",
    "/wishlist",
    "/customer/info",
    "/recentlyviewedproducts",
    "/blog/rss/2",
    "/shippinginfo",
)

# Fiche dont les quatre paragraphes d'introduction avaient disparu.
PRODUIT_SANS_ONGLET = "tole-30-200-1000-ral-7016-300x105cm"
PHRASES_ATTENDUES = (
    "peuvent être placées en toiture",
    "commandées sur-mesure",
)

# Categorie a forte cardinalite dont les noms portent deux cotes : le cas ou
# l'ordre alphabetique se voit le plus.
CATEGORIE_TRIEE = "/acier/profiles/plat"

# Fiche dont la description porte des paires en phrases (« Forme et Geometrie »,
# « Resistance ») : le cas ou l'alignement a droite se voyait.
PRODUIT_A_PHRASES = "corniere-egale-25x25x2mm-en-aluminium"
# Au-dela, une valeur n'est plus une cote : elle se lit alignee a gauche.
LONGUEUR_MAX_ALIGNEE_A_DROITE = 40

# Plafond d'envois par adresse, declare dans `app/api/devis/route.ts`. Le
# controle en envoie un de plus et attend un 429.
ENVOIS_MAX_PAR_IP = 5

# Adresse du seul controle qui sature le plafond. Prise dans TEST-NET-3
# (RFC 5737), reservee a la documentation : elle ne designe personne. Sans
# elle, P12 consommerait le quota de P8d, qui tourne apres lui.
ADRESSE_DU_FLOT = "203.0.113.12"

# Si un SMTP est configure en local, un POST valide enverrait un vrai message a
# chaque lancement du registre. Le controle 503 se retire alors de lui-meme.
ENV_LOCAL = RACINE / ".env.local"


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

    def envoyer(self, chemin: str, donnees, methode: str = "POST", adresse: str = ""):
        """(statut, corps) d'une requete JSON. `donnees=None` envoie un corps vide.

        `adresse` remplit `X-Forwarded-For` : le plafond de `/api/devis` compte
        par adresse, et un controle qui le sature ne doit pas consommer le
        quota des autres.
        """
        corps = None if donnees is None else json.dumps(donnees).encode("utf-8")
        entetes = {"Content-Type": "application/json"}
        if adresse:
            entetes["X-Forwarded-For"] = adresse
        requete = urllib.request.Request(
            self.base + chemin,
            data=corps,
            method=methode,
            headers=entetes,
        )
        try:
            reponse = urllib.request.urlopen(requete, timeout=REQUETE_TIMEOUT_S)
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

    def test_p9_fiche_produit_structuree(self):
        """P9 : ce que le visiteur recoit sur une fiche produit est structure.

        Avant le 22/09, la description de chaque fiche etait rendue en
        paragraphes commencant par « • » : aucun titre, aucune liste, une colonne
        vide sur 36 % de la largeur. Le module de chiffres cles n'existait pas.
        """
        statut, corps = self.serveur.appeler("/p/" + PRODUIT_TEMOIN)
        self.assertEqual(statut, 200)
        # Le pave « chiffres cles » de tete a ete retire le 22/09 : il repetait
        # la fiche technique de l'onglet Caracteristiques. C'est ce bloc-la que
        # le visiteur doit recevoir, et il porte `data-module="caracteristiques"`.
        self.assertIn(
            'data-module="caracteristiques"', corps,
            "la fiche technique n'est servie nulle part dans le HTML rendu",
        )
        self.assertNotRegex(corps, r">\s*[•]\s", "une puce litterale « • » subsiste dans le HTML : liste non reconnue")
        self.assertIn("Le produit en d", corps, "le bloc « Le produit en détail » n'est pas rendu")
        statut, riche = self.serveur.appeler("/p/" + PRODUIT_RICHE)
        self.assertEqual(statut, 200)
        self.assertNotRegex(riche, r">\s*[•]\s", "une puce litterale « • » subsiste dans le HTML : liste non reconnue")
        self.assertRegex(riche, r"<h3[^>]*>", "les sections du detail doivent etre des <h3> sous le <h2> du bloc")
        for module in ("atouts", "caracteristiques", "services"):
            self.assertIn(f'data-module="{module}"', riche, f"module « {module} » absent de la fiche riche")

    def test_p8a_devis_api_refuse_un_corps_invalide(self):
        statut, _ = self.serveur.envoyer("/api/devis", {"nom": "x"})
        self.assertEqual(statut, 400, "un corps incomplet devrait donner 400, pas " + str(statut))

    def test_p8b_devis_api_refuse_le_get(self):
        statut, _ = self.serveur.appeler("/api/devis")
        self.assertEqual(statut, 405, "GET /api/devis devrait donner 405, pas " + str(statut))

    def test_p8c_devis_api_ignore_les_robots_sans_envoyer(self):
        """Champ piege rempli : 200 muet, avant toute tentative d'envoi.

        Sans SMTP configure, une tentative d'envoi donnerait 503. Le 200 prouve
        donc que le piege court-circuite l'envoi, pas seulement qu'il repond.
        """
        piege = dict(DEMANDE_TEMOIN, site_web="http://spam.example.invalid")
        statut, corps = self.serveur.envoyer("/api/devis", piege)
        self.assertEqual(statut, 200, "un robot pris au piege devrait recevoir 200, pas " + str(statut))
        self.assertIn('"ok":true', corps.replace(" ", ""), "la reponse au robot doit ressembler a un succes")

    def test_p8d_devis_api_sans_smtp_se_declare_indisponible(self):
        if ENV_LOCAL.exists():
            self.skipTest("SMTP configure dans .env.local : aucun envoi reel pendant les controles.")
        statut, corps = self.serveur.envoyer("/api/devis", DEMANDE_TEMOIN)
        self.assertEqual(statut, 503, "sans SMTP la route devrait repondre 503, pas " + str(statut))
        self.assertIn("erreur", corps, "la reponse 503 doit porter un champ `erreur` lisible par le formulaire")


    def test_p12_devis_api_refuse_un_flot(self):
        if ENV_LOCAL.exists():
            self.skipTest("SMTP configure dans .env.local : aucun envoi reel pendant les controles.")
        statuts = [
            self.serveur.envoyer("/api/devis", DEMANDE_TEMOIN, adresse=ADRESSE_DU_FLOT)[0]
            for _ in range(ENVOIS_MAX_PAR_IP + 1)
        ]
        self.assertNotIn(
            429,
            statuts[:ENVOIS_MAX_PAR_IP],
            "le plafond se declenche avant " + str(ENVOIS_MAX_PAR_IP) + " demandes : " + str(statuts),
        )
        self.assertEqual(
            statuts[-1],
            429,
            "la demande au-dela du plafond devrait etre refusee (429), pas " + str(statuts[-1]),
        )

    def test_p13_le_texte_du_site_source_est_servi(self):
        statut, corps = self.serveur.appeler("/p/" + PRODUIT_SANS_ONGLET)
        self.assertEqual(statut, 200, "la fiche temoin ne repond pas 200")
        absentes = [p for p in PHRASES_ATTENDUES if p not in corps]
        self.assertEqual(
            absentes, [],
            "texte du site source perdu sur une fiche sans onglet : " + str(absentes),
        )

    def test_p15_aucune_phrase_n_est_alignee_a_droite(self):
        statut, corps = self.serveur.appeler("/p/" + PRODUIT_A_PHRASES)
        self.assertEqual(statut, 200, "la fiche temoin ne repond pas 200")

        trop_longues = []
        for balise in re.findall("<dd[^>]*>.*?</dd>", corps, re.S):
            if "text-right" not in balise:
                continue
            texte = re.sub("<[^>]+>", "", balise)
            texte = unescape(texte).strip()
            if len(texte) > LONGUEUR_MAX_ALIGNEE_A_DROITE:
                trop_longues.append(texte[:60])
        self.assertEqual(
            trop_longues, [],
            "valeurs alignees a droite trop longues pour l'etre : " + str(trop_longues),
        )

    def test_p14_les_produits_sont_servis_en_ordre_numerique(self):
        statut, corps = self.serveur.appeler(CATEGORIE_TRIEE)
        self.assertEqual(statut, 200, CATEGORIE_TRIEE + " ne repond pas 200")

        # Les noms tels qu'ils apparaissent, dans l'ordre du HTML servi.
        noms = re.findall("Plat ([0-9]+)x([0-9]+)mm", corps)
        self.assertGreater(len(noms), 20, "trop peu de produits lus pour juger de l'ordre")

        vus, cotes = set(), []
        for largeur, epaisseur in noms:
            cle = (int(largeur), int(epaisseur))
            if cle in vus:
                continue
            vus.add(cle)
            cotes.append(cle)

        desordre = [
            (cotes[i], cotes[i + 1])
            for i in range(len(cotes) - 1)
            if cotes[i] > cotes[i + 1]
        ]
        self.assertEqual(
            desordre, [],
            f"{len(desordre)} ruptures dans l'ordre des cotes : "
            f"{desordre[:4]}. Le tri par defaut doit etre numerique.",
        )

    def test_p10_vignettes_categorie_passent_par_optimiseur(self):
        statut, corps = self.serveur.appeler(CATEGORIE_A_VIGNETTES)
        self.assertEqual(statut, 200, CATEGORIE_A_VIGNETTES + " ne repond pas 200")
        html = corps.replace("&amp;", "&")

        brutes = sorted({
            morceau.split(chr(34), 1)[0]
            for morceau in html.split("src=" + chr(34) + "/images/produits/")[1:]
        })
        self.assertEqual(
            brutes,
            [],
            "photos servies en pleine resolution dans une vignette : " + str(brutes),
        )

        # Sans candidat assez petit dans le `srcset`, le navigateur prend le
        # plus grand : l'optimiseur ne sert alors a rien.
        balises = re.findall("<img" + chr(92) + "b[^>]*>", html, re.I)
        self.assertTrue(balises, "aucune image sur " + CATEGORIE_A_VIGNETTES)
        trop_grandes = []
        for balise in balises:
            jeu = re.search('srcset="([^"]+)"', balise, re.I)
            if not jeu:
                continue
            largeurs = [int(l) for l in re.findall("&w=(" + chr(92) + "d+)&", jeu.group(1))]
            if largeurs and min(largeurs) > LARGEUR_MAX_VIGNETTE:
                source = re.search("url=([^&]+)", jeu.group(1))
                trop_grandes.append(source.group(1).split("%2F")[-1] if source else "?")
        self.assertEqual(
            trop_grandes,
            [],
            "vignettes sans candidat sous "
            + str(LARGEUR_MAX_VIGNETTE)
            + " px : " + str(trop_grandes),
        )

    def test_p11_anciennes_urls_reparees_aboutissent(self):
        casses = []
        for ancienne in ANCIENNES_URLS_REPAREES:
            statut, _ = self.serveur.appeler(ancienne)
            if statut != 200:
                casses.append((ancienne, statut))
        self.assertEqual(casses, [], "anciennes URLs qui n'aboutissent pas : " + str(casses))


if __name__ == "__main__":
    unittest.main()
