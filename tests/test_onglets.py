"""Controles de la section « Le produit en detail » en onglets.

La section rendait toutes les sections de description dans une grille de
cartes. Elle devient un jeu d'onglets construit a partir des donnees reelles de
chaque fiche, sur le modele d'interaction de `GalerieProduit` : des boutons
radio et des selecteurs CSS `peer`, donc AUCUN JavaScript. Le contenu reste
dans le HTML et la navigation au clavier est celle, native, d'un groupe radio.

Ce que ces controles protegent :

O1 - Le module d'onglets est pur : pas de React, pas de `use client`. Il doit
     rester testable et reutilisable hors rendu.
O2 - Aucun type de section n'est perdu. `lib/description.ts` declare sept
     `TypeSection` ; la mise en onglets doit toutes les acheminer quelque part,
     sinon du contenu du site source disparait sans bruit.
O3 - Le composant declare autant de jeux de classes CSS qu'il peut afficher
     d'onglets. Le motif `peer` de Tailwind exige des noms de classes ecrits en
     entier : un onglet au-dela du dernier jeu declare s'afficherait sans
     jamais pouvoir etre selectionne. C'est le piege de `GalerieProduit`, qui
     tronque a `CLASSES.length`.
O4 - Les specifications et les documents n'existent qu'a UN seul endroit de la
     fiche, en suivant les composants que la page rend. Premiere version, le
     22/09 : elle ne lisait que `app/p/[slug]/page.tsx`, et a laisse passer
     `ChiffresCles`, un composant appele par la page qui reaffichait matiere,
     epaisseur, ailes et poids juste sous le titre — exactement la fiche
     technique de l'onglet. Un controle qui s'arrete au fichier appelant ne
     voit pas ce que l'appele affiche. Le 22/09, le proprietaire a demande que chaque fiche porte les
     memes rubriques ; ce sont les seules donnees quasi universelles
     (specifications 472 fiches sur 495, PDF 359), donc elles passent en
     onglet. Les laisser AUSSI dans la colonne de droite afficherait deux fois
     la meme chose sur la meme page. Le controle refuse les deux emplacements
     a la fois, sans imposer lequel : c'est l'exclusivite qui compte.
O5 - Le rendu 3D dimensionnel accompagne l'onglet des cotes. 355 fiches
     portent des `cotes` (lettres A, B, C et valeurs) qui n'etaient affichees
     nulle part, alors que le rendu de la fiche porte ces memes lettres.
"""

import json
import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
MODULE = RACINE / "lib" / "onglets.ts"
COMPOSANT = RACINE / "components" / "catalogue" / "DetailProduit.tsx"
DESCRIPTION = RACINE / "lib" / "description.ts"
FICHE = RACINE / "app" / "p" / "[slug]" / "page.tsx"
DESCRIPTIONS = RACINE / "lib" / "descriptions-site-actuel.json"


def source(chemin: Path) -> str:
    return chemin.read_text(encoding="utf-8")


def sans_commentaires(texte: str) -> str:
    """Le code seul : un commentaire qui NOMME une donnee n'est pas un rendu.

    O4 a d'abord echoue sur la phrase « la colonne de droite rend deja
    `p.specs` », ecrite dans l'en-tete de `lib/onglets.ts` pour expliquer
    justement qu'il ne les rend pas.
    """
    morceaux, reste = [], texte
    while True:
        i = reste.find("/*")
        if i == -1:
            morceaux.append(reste)
            break
        morceaux.append(reste[:i])
        j = reste.find("*/", i + 2)
        if j == -1:
            break
        reste = reste[j + 2:]
    lignes = "".join(morceaux).splitlines()
    return chr(10).join(l for l in lignes if not l.strip().startswith("//"))


class ModuleDOnglets(unittest.TestCase):
    def test_o1_le_module_est_pur(self):
        self.assertTrue(MODULE.exists(), "lib/onglets.ts doit exister.")
        texte = source(MODULE)
        # La directive, pas le mot : ce fichier a le droit d'expliquer en
        # commentaire qu'il n'est pas un composant client.
        premiere = next((l.strip() for l in texte.splitlines() if l.strip()), "")
        self.assertNotIn("use client", premiere, "lib/onglets.ts ne doit pas etre un composant client.")
        for interdit in ("from " + chr(34) + "react" + chr(34), "React."):
            self.assertNotIn(
                interdit, texte,
                "lib/onglets.ts doit rester pur (pas de React) : "
                "il se teste et se reutilise hors rendu.",
            )

    def test_o2_aucun_type_de_section_n_est_perdu(self):
        types = set(re.findall(r'^  [|] "([a-z]+)"', source(DESCRIPTION), re.M))
        self.assertTrue(types, "aucun TypeSection lu dans lib/description.ts")
        texte = source(MODULE)
        absents = sorted(t for t in types if chr(34) + t + chr(34) not in texte)
        self.assertEqual(
            absents, [],
            "types de section jamais achemines vers un onglet, donc contenu "
            "perdu sans bruit : " + str(absents),
        )


class ComposantDOnglets(unittest.TestCase):
    def test_o3_assez_de_jeux_de_classes_pour_tous_les_onglets(self):
        self.assertTrue(COMPOSANT.exists(), "components/catalogue/DetailProduit.tsx doit exister.")
        jeux = len(set(re.findall(r'peer/o(\d+)', source(COMPOSANT))))
        # Un onglet possible = une entree de LIBELLES dans le module.
        bloc = source(MODULE).split("const LIBELLES", 1)[1].split("};", 1)[0]
        cles = len(re.findall(r'^  [a-z"]', bloc, re.M))
        self.assertGreaterEqual(
            jeux, cles,
            f"{cles} onglets possibles pour seulement {jeux} jeux de classes CSS : "
            "les derniers s'afficheraient sans pouvoir etre selectionnes.",
        )

    def _rendu_par_la_fiche(self) -> str:
        """Le source de la fiche ET des composants qu'elle rend, sauf les onglets.

        On suit les imports `@/components/...` de la page : ce que le visiteur
        lit au-dessus des onglets ne vient pas seulement du fichier de la page.
        """
        texte = source(FICHE)
        morceaux = [texte]
        for chemin in re.findall(r'from "@/(components/[^"]+)"', texte):
            fichier = RACINE / (chemin + ".tsx")
            if not fichier.exists() or fichier == COMPOSANT:
                continue
            morceaux.append(source(fichier))
        return sans_commentaires(chr(10).join(morceaux))

    def test_o4_les_specifications_ne_sont_qu_a_un_endroit(self):
        composant = sans_commentaires(source(COMPOSANT) + source(MODULE))
        fiche = self._rendu_par_la_fiche()
        for donnee, nom in (("specs", "specifications"), ("pdfs", "documents")):
            dans_onglets = ("p." + donnee) in composant or ("produit." + donnee) in composant
            dans_colonne = ("p." + donnee) in fiche
            self.assertFalse(
                dans_onglets and dans_colonne,
                f"les {nom} sont rendus a la fois dans les onglets et dans la colonne "
                "de droite de la fiche : le visiteur lirait deux fois la meme chose.",
            )
            self.assertTrue(
                dans_onglets or dans_colonne,
                f"les {nom} ne sont rendus nulle part : la donnee existe pourtant.",
            )

    def test_o5_les_cotes_ont_leur_onglet_et_leur_visuel(self):
        avec_cotes = sum(
            1 for v in json.loads(source(DESCRIPTIONS)).values() if v.get("cotes")
        )
        self.assertGreater(avec_cotes, 300, "le jeu de donnees a change : recompter")
        self.assertIn(
            "cotes", source(MODULE),
            f"{avec_cotes} fiches portent des cotes affichees nulle part ; "
            "elles doivent alimenter un onglet.",
        )


class FicheProduit(unittest.TestCase):
    def test_o6_la_fiche_utilise_le_composant_d_onglets(self):
        texte = source(FICHE)
        self.assertIn("DetailProduit", texte, "la fiche doit rendre la section en onglets.")
        self.assertNotIn(
            "Le produit en détail", texte,
            "l'ancienne section en grille doit avoir ete remplacee, pas doublee.",
        )


if __name__ == "__main__":
    unittest.main()
