"""Controles de l'etat unique du projet.

`project-state/CURRENT_STATE.md` est la source unique de l'etat. Deux risques
le guettent : vieillir sans que personne s'en apercoive, et affirmer des choses
qu'un document ne peut pas garantir.

Fraicheur : l'etat est compare aux entrees de `_JOURNAL/`, pas au `git status`
du poste. Un controle couple a l'etat local d'une machine est rouge en
permanence chez l'un et vert chez l'autre — c'est le defaut de
`test_extensions.py:118-131` (ligne B3), a ne pas reproduire.
"""

import re
import unittest
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
ETAT = RACINE / "project-state" / "CURRENT_STATE.md"
MEMOIRE = RACINE / "memory" / "ACTIVE_CONTEXT.md"
JOURNAL = RACINE / "_JOURNAL"

DATE_ETAT = re.compile(r"^ÉTAT AU:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
NOM_JOURNAL = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")

PISTES = ("_DOCS/CHANTIERS-RENFORCEMENT.md", "_DOCS/rendus-3d/avancement.md")

# Un document ne peut pas garantir une donnee volatile : la proprete du
# working tree change a chaque frappe. Voir la note du 21/09 dans l'etat.
AFFIRMATIONS_INTERDITES = ("working tree est propre", "working tree propre")


def date_de_l_etat():
    trouve = DATE_ETAT.search(ETAT.read_text(encoding="utf-8"))
    return date.fromisoformat(trouve.group(1)) if trouve else None


def dates_des_journaux() -> list[date]:
    if not JOURNAL.exists():
        return []
    dates = []
    for fichier in JOURNAL.glob("*.md"):
        capture = NOM_JOURNAL.match(fichier.name)
        if capture:
            dates.append(date(*(int(p) for p in capture.groups())))
    return sorted(dates)


class EtatTests(unittest.TestCase):
    def test_l_etat_declare_une_date_lisible(self):
        self.assertIsNotNone(
            date_de_l_etat(),
            "project-state/CURRENT_STATE.md doit porter une ligne "
            "'ÉTAT AU: AAAA-MM-JJ'. Sans date lisible, sa fraicheur n'est pas "
            "verifiable.",
        )

    def test_l_etat_est_au_moins_aussi_frais_que_le_dernier_journal(self):
        journaux = dates_des_journaux()
        self.assertTrue(
            journaux,
            "_JOURNAL/ ne contient aucune entree datee : le controle de "
            "fraicheur n'inspecterait rien (faux vert, voir L-005).",
        )
        dernier = max(journaux)
        etat = date_de_l_etat()
        self.assertIsNotNone(etat, "Date d'etat absente.")
        self.assertGreaterEqual(
            etat,
            dernier,
            f"L'etat est date du {etat} alors que le dernier journal est du "
            f"{dernier}. Du travail a ete fait sans que l'etat suive : c'est "
            f"ainsi qu'un etat devient faux.",
        )

    def test_l_etat_renvoie_a_chaque_piste(self):
        texte = ETAT.read_text(encoding="utf-8")
        for piste in PISTES:
            self.assertIn(
                piste,
                texte,
                f"L'etat ne renvoie pas a '{piste}'. Il est le point d'entree : "
                f"une piste qu'il ignore est une piste qu'on oublie.",
            )

    def test_la_memoire_active_ne_duplique_plus_l_etat(self):
        texte = MEMOIRE.read_text(encoding="utf-8")
        for titre in ("## État", "## Tâche active", "## Audit de synchronisation"):
            self.assertNotIn(
                titre,
                texte,
                f"memory/ACTIVE_CONTEXT.md contient '{titre}' : l'etat y est "
                f"decrit une seconde fois. Un fait = une source.",
            )
        self.assertIn(
            "project-state/CURRENT_STATE.md",
            texte,
            "memory/ACTIVE_CONTEXT.md doit renvoyer a la source unique de l'etat.",
        )

    def test_l_etat_ne_se_prononce_pas_sur_le_working_tree(self):
        for fichier in (ETAT, MEMOIRE):
            texte = fichier.read_text(encoding="utf-8")
            for ligne in texte.splitlines():
                if "PROUVÉ" not in ligne:
                    continue
                for affirmation in AFFIRMATIONS_INTERDITES:
                    if affirmation in ligne:
                        self.fail(
                            f"{fichier.name} affirme « {ligne.strip()} ». La "
                            f"proprete du working tree change a chaque frappe : "
                            f"un document ne peut pas la prouver. C'est "
                            f"exactement l'affirmation qui etait fausse le "
                            f"17/09, dans le diff qui l'ecrivait."
                        )


if __name__ == "__main__":
    unittest.main()
