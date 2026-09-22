"""Controles de la page Protection des donnees : elle doit decrire le code.

Constat du 22/09/2026 : la page affirmait « Les formulaires de devis et de
contact n'enregistrent rien : ils composent un message dans votre propre
logiciel de messagerie [...] Tant que vous n'avez pas clique sur "envoyer"
dans votre messagerie, aucune donnee ne nous parvient. » C'etait vrai jusqu'a
l'ajout de `app/api/devis/route.ts` la veille : depuis, le formulaire de devis
poste au serveur, qui relaie par SMTP. La page est restee telle quelle.

Une page RGPD fausse n'est pas une coquille : c'est une information erronee
sur un traitement de donnees personnelles, affichee au visiteur qui la lit
precisement pour savoir ce qui lui arrive.

RG1 - Si une route serveur recoit un formulaire, la page dit que ce formulaire
      passe par le serveur.
RG2 - Tant qu'une route serveur recoit la demande de devis, la page ne peut
      pas presenter la composition dans la messagerie du visiteur comme le
      fonctionnement du formulaire de devis : c'est devenu le repli, et un
      paragraphe qui parle des deux doit dire a quelle condition il s'applique.

RG3 - Le site n'annonce pas un stockage navigateur qu'il n'utilise pas. La
      page Cookies affirmait « Certaines preferences d'affichage peuvent etre
      conservees dans le stockage local de votre navigateur — un filtre
      selectionne, un onglet ouvert » : aucun `localStorage`, `sessionStorage`
      ni `document.cookie` n'existe dans le code. Sur-declarer est moins grave
      que sous-declarer, mais une page qui annonce « voici ce qu'il utilise
      reellement » doit dire vrai dans les deux sens.

RG2 vise l'invariant, pas la tournure : ecrit d'abord comme « la promesse doit
etre qualifiee », il serait reste vert sur le texte fautif, qui la qualifiait
— mais avec une reserve devenue fausse.
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
PAGE = RACINE / "app" / "protection-des-donnees" / "page.tsx"
COOKIES = RACINE / "app" / "cookies" / "page.tsx"
SOURCES = ("app", "components", "lib")
STOCKAGES = ("localStorage", "sessionStorage", "document.cookie")
ANNONCE_STOCKAGE = "conservées dans le stockage local"
ROUTE_DEVIS = RACINE / "app" / "api" / "devis" / "route.ts"

# Ce que la page doit dire quand une route serveur existe.
RELAIS = "notre serveur"
# Le fonctionnement decrit : le message est compose chez le visiteur.
MESSAGERIE = "votre propre logiciel de messagerie"
# Le formulaire qui, lui, passe par le serveur.
DEVIS = "devis"
# La condition qui rend la composition chez le visiteur exacte pour ce
# formulaire-la : elle n'a lieu que si le relais ne repond pas.
CONDITION = "indisponible"


def le_site_stocke_dans_le_navigateur() -> list[str]:
    """Les fichiers qui ecrivent vraiment dans le navigateur, s'il y en a."""
    trouves = []
    for dossier in SOURCES:
        for fichier in (RACINE / dossier).rglob("*"):
            if fichier.suffix not in (".ts", ".tsx") or not fichier.is_file():
                continue
            texte = fichier.read_text(encoding="utf-8", errors="replace")
            if any(mot in texte for mot in STOCKAGES):
                trouves.append(str(fichier.relative_to(RACINE)))
    return sorted(trouves)


def paragraphes() -> list[str]:
    """Les textes affiches, un par litteral de chaine du gabarit."""
    return re.findall(r'"([^"]+)"', PAGE.read_text(encoding='utf-8'))


class ProtectionDesDonnees(unittest.TestCase):
    def test_rg1_le_relais_serveur_est_annonce(self):
        if not ROUTE_DEVIS.exists():
            self.skipTest("aucune route serveur ne recoit de formulaire.")
        textes = paragraphes()
        annonce = [t for t in textes if RELAIS in t]
        self.assertTrue(
            annonce,
            "`app/api/devis/route.ts` relaie la demande de devis, "
            "mais la page ne mentionne nulle part le passage par le serveur.",
        )

    def test_rg2_la_messagerie_du_visiteur_n_est_plus_donnee_pour_le_devis(self):
        if not ROUTE_DEVIS.exists():
            self.skipTest("aucune route serveur ne recoit de formulaire.")
        fautifs = [
            t[:110]
            for t in paragraphes()
            if MESSAGERIE in t and DEVIS in t.lower() and CONDITION not in t
        ]
        self.assertEqual(
            fautifs,
            [],
            "la page decrit la demande de devis comme composee dans la "
            "messagerie du visiteur, sans dire que c'est le repli : " + str(fautifs),
        )

    def test_rg3_aucun_stockage_navigateur_annonce_a_tort(self):
        if le_site_stocke_dans_le_navigateur():
            self.skipTest("le site utilise un stockage navigateur : l'annonce est fondee.")
        texte = COOKIES.read_text(encoding="utf-8")
        self.assertNotIn(
            ANNONCE_STOCKAGE,
            texte,
            "la page Cookies annonce un stockage local que le code n'utilise nulle part.",
        )

if __name__ == "__main__":
    unittest.main()
