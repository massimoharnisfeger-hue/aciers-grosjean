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


class CatalogueRegenerable(unittest.TestCase):
    """D12 : un fichier declare « genere » doit pouvoir etre regenere.

    `lib/catalogue.ts` porte 495 produits et CLAUDE.md dit : « genere par
    scripts/generer-catalogue.py, toute modification a la main doit etre
    reportee dans le generateur ». Or le 22/09 le generateur attendait son CSV
    a `/root/.claude/uploads/...` — un chemin de session web Linux, absent de
    cette machine et du depot. Le generateur ne pouvait plus tourner : le
    catalogue etait gele, et la regle de CLAUDE.md interdisait de le modifier
    a la main. Impossible d'ajouter un produit, de corriger un nom.

    Un chemin d'entree hors du depot n'est pas une source : c'est une piece
    manquante qui ne se voit qu'au moment ou l'on en a besoin.
    """

    def test_d12_l_entree_du_generateur_est_dans_le_depot(self):
        src = (RACINE / "scripts" / "generer-catalogue.py").read_text(encoding="utf-8")
        defauts = re.findall(r'^\s*"(/(?:root|home|tmp|mnt)/[^"]*)"', src, re.MULTILINE)
        self.assertEqual(
            defauts, [],
            f"generer-catalogue.py designe une entree hors du depot : {defauts}. "
            f"Le catalogue ne peut pas etre regenere, donc il ne peut plus etre corrige.",
        )


class VisuelDeFamille(unittest.TestCase):
    """D11 : une carte de famille montre la vraie photo quand il n'y en a qu'une.

    Sur `/toiture-bardage`, les trois familles — Bardage, Panneaux isoles,
    Toles profilees — affichaient le MEME dessin SVG : `lib/visuels.ts` les
    renvoyait toutes vers l'illustration « toles ». Les trois photos studio
    existaient pourtant, servies une couche plus bas.

    Regle demandee le 22/09 : si exactement UNE photo studio existe sous une
    famille, la carte la montre. Zero ou plusieurs : le dessin SVG reste, parce
    que choisir entre deux photos est une decision visuelle humaine (le cas
    HUMAN_REVIEW de l'audit).

    Le rendu passe par un composant partage : recopier le meme JSX dans les
    deux gabarits perdrait la regle dans l'un des deux (lecon L-029).
    """

    def test_d11_la_regle_du_candidat_unique(self):
        src = (RACINE / "lib" / "visuels.ts").read_text(encoding="utf-8")
        self.assertIn(
            "studioUniqueDe", src,
            "lib/visuels.ts doit exposer la regle du candidat unique.",
        )

    def test_d11bis_un_seul_composant_pour_les_deux_gabarits(self):
        composant = RACINE / "components" / "catalogue" / "VisuelFamille.tsx"
        self.assertTrue(composant.exists(), "components/catalogue/VisuelFamille.tsx manquant.")
        app = RACINE / "app"
        for gabarit in (app / "[univers]" / "page.tsx", app / "[univers]" / "[...segments]" / "page.tsx"):
            self.assertIn(
                "VisuelFamille", gabarit.read_text(encoding="utf-8"),
                f"{gabarit.name} doit utiliser le composant partage, pas recopier la regle.",
            )


class CorrespondanceRenduProduit(unittest.TestCase):
    """D10 : la regle qui dit « ce rendu appartient a ce produit ».

    Premiere version de l'audit : egalite stricte entre le titre inscrit dans
    le rendu et le nom du catalogue. Elle classait 213 produits sur 466 en
    AMBIGUOUS, soit la moitie du catalogue a reverifier a la main — alors que
    201 de ces 213 etaient de simples raccourcis voulus.

    La regle tient a une propriete du domaine : le titre d'un rendu n'AJOUTE
    jamais d'information, il en retire (la matiere est deja dans le surtitre
    de l'image). Ses mots doivent donc se retrouver dans le nom du produit,
    dans l'ordre, et toutes ses cotes doivent exister. Ces cas sont ceux qui
    ont ete verifies a la main le 22/09 sur les donnees reelles.
    """

    @staticmethod
    def regle():
        import importlib.util
        chemin = RACINE / "scripts" / "rendu-3d" / "auditer_visuels.py"
        spec = importlib.util.spec_from_file_location("auditer_visuels", chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.le_rendu_designe_le_produit

    def test_d10_un_raccourci_designe_bien_le_produit(self):
        designe = self.regle()
        for titre, nom in (
            ("Rond à béton de 10mm de diamètre", "Rond à béton de 10mm de diamètre en acier laminé à chaud"),
            ("Poutrelle HEA 100", "Poutrelle HEA 100 en acier"),
            ("Tube rond 21,3x2mm série légère", "Tube rond 21,3x2mm en acier brut série légère"),
            ("Large plat 160x10mm", "Large plat en acier laminé à chaud 160x10mm"),
            ("Plat de 20x3mm en aluminium", "Plat de 20x3mm en aluminium"),
        ):
            self.assertTrue(designe(titre, nom), f"« {titre} » devrait designer « {nom} »")

    def test_d10bis_une_cote_differente_est_un_autre_produit(self):
        designe = self.regle()
        for titre, nom in (
            ("Tube rond 21,3x2mm série légère", "Tube rond 26,9x2,5mm en acier brut série légère"),
            ("Poutrelle IPE 200", "Poutrelle HEA 100 en acier"),
            ("Plat de 30x3mm en aluminium", "Plat de 20x3mm en aluminium"),
        ):
            self.assertFalse(designe(titre, nom), f"« {titre} » ne designe PAS « {nom} »")


class StudioDeCategorie(unittest.TestCase):
    """D9 : integrer une famille ne remplace pas le studio d'une categorie voisine.

    Trois categories ont plusieurs familles de photo studio — « Caillebotis &
    marches » en a quatre (caillebotis, marche-caillebotis, marche-o2,
    plancher-o2). Le manifeste n'en tient qu'une par categorie, et
    `integrer_visuels.py` ecrasait la precedente sans condition : la derniere
    famille integree gagnait, par hasard. Le 22/09, integrer les caillebotis a
    silencieusement remplace le studio de la categorie.

    Choisir entre quatre studios est une decision humaine. Le generateur doit
    donc garder celui qui est en place et le signaler, sauf demande explicite.
    """

    def test_d9_le_studio_existant_n_est_pas_ecrase(self):
        src = (RACINE / "scripts" / "rendu-3d" / "integrer_visuels.py").read_text(encoding="utf-8")
        # L'assignation reste legitime SOUS un garde ; c'est l'assignation nue,
        # au niveau du corps de boucle (8 espaces), qui ecrase sans condition.
        nue = chr(10) + " " * 8 + 'manifeste["categories"][categorie] = image'
        self.assertNotIn(
            nue, src,
            "integrer_visuels.py ecrase le studio de la categorie sans condition : "
            "la derniere famille integree gagne, sans preuve qu'elle soit la bonne.",
        )
        self.assertIn(
            "remplacer_studio", src,
            "Le remplacement d'un studio de categorie doit etre explicite.",
        )


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
