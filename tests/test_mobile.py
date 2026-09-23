"""Controles mobiles du formulaire de devis.

Mesures du 21/09/2026 sur les 12 gabarits du site (320, 375, 768, 1280 px) :
la mise en page ne deborde nulle part, mais le formulaire de devis concentre
quatre defauts mobiles verifiables dans le source.

M1 - Zoom automatique iOS
    Safari iOS agrandit la page des qu'un champ recoit le focus si sa taille de
    police est inferieure a 16 px, et ne revient pas toujours en arriere. Les
    champs heritaient de `text-sm` (14 px) porte par le <label> parent. La
    classe partagee doit donc declarer une taille >= 16 px explicitement, sinon
    l'heritage la ramene a 14 px sans que rien ne le signale.

M2 - Attribut `name`
    Sans `name`, un champ n'existe pour aucun envoi natif ni aucune
    restauration de formulaire par le navigateur.

M3 - `autoComplete`
    Le remplissage automatique du nom, de l'e-mail et du telephone est le
    principal gain de confort sur mobile. Absent, chaque visiteur retape tout.

M5 - Un lien place DANS un formulaire ouvre un nouvel onglet.
    Mesure du 22/09 au navigateur, a 390 px : on remplit /devis, on touche le
    lien « protection des donnees » place sous le bouton d'envoi, on revient en
    arriere — nom, e-mail et details sont VIDES. Le formulaire n'a aucune
    reprise et le site n'ecrit rien dans le navigateur (c'est une promesse
    tenue, ecrite noir sur blanc sur la page Cookies). La parade n'est donc pas
    de stocker la saisie, mais de ne jamais quitter la page : `target="_blank"`.
    Le risque a grandi le matin meme, quand ce lien a recu `lien-tactile` pour
    atteindre 24 px de haut — plus facile a atteindre, donc plus facile a
    toucher par erreur.

M4 - Clavier adapte (`inputMode` / `type`)
    Sans indication, le telephone ouvre un clavier alphabetique. Saisir un
    numero au pouce en changeant de disposition est une cause connue
    d'abandon de formulaire.

Les controles lisent le source plutot que le rendu : ils restent verts sans
navigateur, sans serveur et sans reseau.
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
FORMULAIRE = RACINE / "components" / "sections" / "DevisForm.tsx"

# Classes Tailwind valant au moins 16 px pour la taille du texte.
TAILLES_SUFFISANTES = ("text-base", "text-lg", "text-xl", "text-[16px]", "text-[1rem]")

# Une balise de saisie complete, de `<input` jusqu'au `>` fermant.
BALISE_SAISIE = re.compile(r"<(input|select|textarea)\b[^>]*>", re.DOTALL)


def source() -> str:
    return FORMULAIRE.read_text(encoding="utf-8")


def classe_partagee() -> str:
    """Le litteral `champStyle`, applique a tous les champs du formulaire."""
    capture = re.search(r"const champStyle\s*=\s*(?:\n\s*)?\"([^\"]*)\"", source())
    return capture.group(1) if capture else ""


def balises_de_saisie() -> list[str]:
    return [m.group(0) for m in BALISE_SAISIE.finditer(source())]


class FormulaireDevisMobile(unittest.TestCase):
    """Le formulaire de devis doit etre utilisable au pouce, sur iPhone."""

    def test_m1_champs_au_moins_16px(self):
        """M1 : `champStyle` declare une taille >= 16 px, sans dependre du parent."""
        classes = classe_partagee()
        self.assertTrue(classes, "champStyle introuvable dans DevisForm.tsx")
        self.assertTrue(
            any(t in classes.split() for t in TAILLES_SUFFISANTES),
            "champStyle n'impose aucune taille >= 16 px : les champs heritent de "
            "`text-sm` (14 px) et Safari iOS zoomera au focus. "
            f"Classes actuelles : {classes!r}",
        )

    def test_m1bis_aucune_taille_inferieure_dans_champstyle(self):
        """M1bis : `champStyle` ne contient pas de classe ramenant sous 16 px."""
        classes = classe_partagee().split()
        trop_petites = [c for c in classes if c in ("text-xs", "text-sm", "text-[14px]", "text-[13px]")]
        self.assertEqual(
            trop_petites, [], f"champStyle contient une taille sous 16 px : {trop_petites}"
        )

    def test_m2_chaque_champ_a_un_name(self):
        """M2 : chaque input/select/textarea porte un attribut `name`."""
        sans_name = [b[:70] for b in balises_de_saisie() if "name=" not in b]
        self.assertEqual(
            sans_name, [], f"{len(sans_name)} champ(s) sans attribut name : {sans_name}"
        )

    def test_m3_identite_remplissable_automatiquement(self):
        """M3 : nom, e-mail et telephone declarent `autoComplete`."""
        src = source()
        manquants = [v for v in ('autoComplete="name"', 'autoComplete="email"', 'autoComplete="tel"')
                     if v not in src]
        self.assertEqual(
            manquants, [], f"autoComplete manquant : {manquants}"
        )

    def test_m4_clavier_adapte_au_type_de_champ(self):
        """M4 : le telephone ouvre un clavier numerique, l'e-mail un clavier e-mail."""
        src = source()
        manquants = []
        if 'type="tel"' not in src:
            manquants.append('type="tel" sur le champ telephone')
        if 'inputMode="tel"' not in src:
            manquants.append('inputMode="tel"')
        if 'inputMode="email"' not in src:
            manquants.append('inputMode="email"')
        self.assertEqual(manquants, [], f"Clavier mobile non adapte : {manquants}")



class LiensDansUnFormulaire(unittest.TestCase):
    """M5 : quitter un formulaire rempli le vide — un lien interne doit s'ouvrir a cote."""

    FORMULAIRES = (
        RACINE / "components" / "sections" / "DevisForm.tsx",
        RACINE / "components" / "sections" / "FormulairePro.tsx",
    )

    def test_m5_les_liens_dans_un_formulaire_ouvrent_un_nouvel_onglet(self):
        fautifs = []
        for fichier in self.FORMULAIRES:
            texte = fichier.read_text(encoding="utf-8")
            debut = texte.find("<form")
            fin = texte.find("</form>")
            if debut == -1 or fin == -1:
                continue
            dans_le_formulaire = texte[debut:fin]
            for balise in re.findall(r"<(?:Link|a)[ >][^>]*>", dans_le_formulaire, re.DOTALL):
                if "href" not in balise:
                    continue
                if "_blank" in balise or "mailto:" in balise or "tel:" in balise:
                    continue
                fautifs.append(f"{fichier.name} : {balise[:80]}")
        self.assertEqual(
            fautifs, [],
            "lien interne dans un formulaire sans `target=_blank` : le visiteur "
            "qui le suit perd tout ce qu'il a saisi. " + str(fautifs),
        )

if __name__ == "__main__":
    unittest.main()
