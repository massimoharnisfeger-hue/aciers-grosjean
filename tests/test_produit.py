"""Controles du systeme de fiche produit (495 fiches, un seul gabarit).

Constat du 22/09/2026 : `lib/descriptions-site-actuel.json` contenait 4 776 blocs,
TOUS de type `p`, dont 2 556 commencant par une puce litterale (« • »), et 14
fiches ou « Points forts » / « Caracteristiques » / « Services » etaient des
paragraphes. Le gabarit sait rendre `h` et `ul` ; il n'en recevait jamais. Le
« mur de texte » des fiches venait des donnees, pas du CSS : le generateur
(`scripts/inventaire/integrer.py`) ne faisait une liste que si un MEME
paragraphe contenait deux puces, et un titre que si le <p> ne contenait qu'un
<strong>. Le site source met chaque puce dans son propre <p>.

D1 - Aucun paragraphe ne commence par un marqueur de puce : c'est un item de liste.
D2 - Une fiche qui a une description longue a au moins un titre ou une liste.
D3 - Un titre reste court et ne finit pas par un point : garde contre une
     promotion trop large (un paragraphe pris pour un titre perd son sens).
D4 - Le gabarit ne dispose plus la description sur deux colonnes dont la
     premiere ne contient qu'un mot : 36 % de la largeur vide a 1280 px.
D5 - Le gabarit porte un module de chiffres cles (`data-module="chiffres-cles"`) :
     ce qui definit le produit se lit avant le prix et le calculateur.

Ces controles lisent le JSON genere et le source du gabarit : verts sans
serveur. Le rendu reel est controle par P9 dans `tests/test_parcours.py`.
"""

import json
import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DESCRIPTIONS = RACINE / "lib" / "descriptions-site-actuel.json"
GABARIT = RACINE / "app" / "p" / "[slug]" / "page.tsx"

PUCE = re.compile(r"^\s*(?:[•\-–·▪]|\d{1,2}[.)])\s+")


def descriptions() -> dict:
    return json.loads(DESCRIPTIONS.read_text(encoding="utf-8"))


class DonneesDeDescription(unittest.TestCase):
    def test_d1_aucun_paragraphe_a_puce(self):
        fautifs = [
            (slug, b["texte"][:50])
            for slug, e in descriptions().items()
            for b in e.get("blocs", [])
            if b["t"] == "p" and PUCE.match(b["texte"])
        ]
        self.assertEqual(
            fautifs[:5], [],
            f"{len(fautifs)} paragraphe(s) commencent par une puce : ce sont des items de liste "
            f"que le generateur n'a pas reconnus. Ex. : {fautifs[:3]}",
        )

    def test_d2_une_description_longue_est_structuree(self):
        longues = {s: e for s, e in descriptions().items() if len(e.get("blocs", [])) >= 3}
        plates = [s for s, e in longues.items() if not any(b["t"] in ("h", "ul") for b in e["blocs"])]
        # Mesure du 22/09 apres regeneration : 37 fiches sur 331 (11 %) sont de la vraie prose
        # (cornieres, IPE : trois paragraphes rediges, sans liste). Le seuil garde contre un
        # retour au « tout paragraphe », pas contre la prose.
        self.assertLessEqual(
            len(plates), len(longues) * 15 // 100,
            f"{len(plates)} fiche(s) sur {len(longues)} a description longue n'ont ni titre ni "
            f"liste : mur de texte. Ex. : {plates[:4]}",
        )

    def test_d3_un_titre_reste_un_titre(self):
        trop = [
            (slug, b["texte"][:60])
            for slug, e in descriptions().items()
            for b in e.get("blocs", [])
            if b["t"] == "h" and (len(b["texte"]) > 60 or b["texte"].rstrip().endswith((".", "!", "?")))
        ]
        self.assertEqual(trop, [], f"titre(s) trop longs ou ponctues comme des phrases : {trop[:3]}")


class GabaritFicheProduit(unittest.TestCase):
    def test_d4_pas_de_colonne_vide_pour_la_description(self):
        src = GABARIT.read_text(encoding="utf-8")
        self.assertNotIn(
            "lg:grid-cols-[1fr_2fr]", src,
            "app/p/[slug]/page.tsx : la description occupe deux colonnes dont la premiere "
            "ne porte que le mot « Description » — 36 % de largeur vide a 1280 px.",
        )

    def test_d5_module_chiffres_cles(self):
        src = GABARIT.read_text(encoding="utf-8")
        modules = (RACINE / "components" / "catalogue" / "FicheModules.tsx").read_text(encoding="utf-8")
        self.assertIn("<ChiffresCles", src, "Le gabarit doit afficher le module de chiffres cles en tete de fiche.")
        self.assertIn(
            'data-module="chiffres-cles"', modules,
            "Le module doit se declarer dans le HTML rendu (P9 le verifie au navigateur).",
        )


class GrillesQuiRetrecissent(unittest.TestCase):
    """D8 : un element de grille doit pouvoir devenir plus etroit que son contenu.

    A 320 px, deux fiches debordaient : « Tole striee de 2000x1000x2,5/4mm en
    aluminium » sortait de 14 px, une section « Domaines d'applications » de
    78 px. Cause commune : un enfant de grille vaut `min-width: auto`, donc il
    ne retrecit jamais sous le mot le plus long de son contenu — et les noms de
    produits sont pleins de cotes insecables. `min-w-0` leve la contrainte,
    `break-words` coupe le mot. C'est la classe de bug, pas ces deux fiches.
    """

    def test_d8_les_blocs_de_grille_peuvent_retrecir(self):
        for chemin, ancre in (
            (GABARIT, 'lg:col-start-2 lg:row-start-1'),
            (RACINE / "components" / "catalogue" / "FicheModules.tsx", "<section data-module="),
        ):
            src = chemin.read_text(encoding="utf-8")
            ligne = next((l for l in src.splitlines() if ancre in l), "")
            self.assertIn(
                "min-w-0", ligne,
                f"{chemin.name} : le bloc « {ancre} » est un enfant de grille sans `min-w-0` : "
                f"un nom de produit avec cotes le fait deborder a 320 px.",
            )
            self.assertIn("break-words", ligne, f"{chemin.name} : bloc « {ancre} » sans `break-words`.")


class DemandeDePrix(unittest.TestCase):
    """D6/D7 : la demande de prix du calculateur ne part plus par la messagerie du visiteur.

    Meme defaut que H4 (ADR-0006) : `mailto:` perd la demande sur un telephone sans
    client mail. Le calculateur envoie desormais son estimation au formulaire de
    devis (`/devis?details=...`), qui la pre-remplit et poste vers `/api/devis`.
    """

    def test_d6_le_calculateur_ne_passe_plus_par_mailto(self):
        src = (RACINE / "components" / "catalogue" / "Calculateur.tsx").read_text(encoding="utf-8")
        self.assertNotIn("mailto:", src, "Calculateur.tsx construit encore un mailto:.")
        self.assertIn('href={`/devis?', src, "Le calculateur doit renvoyer vers /devis avec son estimation.")

    def test_d7_le_formulaire_pre_remplit_depuis_l_url(self):
        src = (RACINE / "components" / "sections" / "DevisForm.tsx").read_text(encoding="utf-8")
        self.assertIn("details", src)
        self.assertRegex(src, r"location\.search|useSearchParams", "DevisForm.tsx doit lire `details` dans l'URL pour pre-remplir la demande.")

if __name__ == "__main__":
    unittest.main()
