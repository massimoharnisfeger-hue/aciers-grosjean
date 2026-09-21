"""Controles du socle d'auto-controle.

Deux familles :

1. Le carnet de lecons (`_DOCS/LECONS.md`) est bien forme, et chaque lecon cite
   un controle qui existe vraiment. Une lecon dont le controle est imaginaire
   est pire qu'une lecon absente : elle donne l'illusion d'etre protege.

2. Le lanceur (`tests/lancer.py`) tient son contrat : il sort en erreur quand un
   controle echoue, et il refuse une suite amputee. Sans ces deux controles, le
   compteur qui mesure l'apprentissage du depot ne serait garanti par rien.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
LECONS = RACINE / "_DOCS" / "LECONS.md"
LANCEUR = RACINE / "tests" / "lancer.py"

EN_TETE_LECON = re.compile(r"^### (L-\d{3}) — (.+)$", re.MULTILINE)
CHAMPS = ("Symptôme", "Cause", "Contrôle", "Date")
FORMAT_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CONTROLE_QUI_ECHOUE = """import unittest


class ControleQuiEchoue(unittest.TestCase):
    def test_echoue_volontairement(self):
        self.assertTrue(False, "echec volontaire")
"""

CONTROLE_QUI_PASSE = """import unittest


class ControleQuiPasse(unittest.TestCase):
    def test_passe(self):
        self.assertTrue(True)
"""


def lecons() -> list[dict]:
    """Decoupe `_DOCS/LECONS.md` en lecons, avec leurs champs."""
    if not LECONS.exists():
        return []
    texte = LECONS.read_text(encoding="utf-8")
    # Les blocs de code documentent le format attendu (L-000...) : ce sont des
    # exemples, pas des lecons. Les lire comme des donnees rend le carnet rouge
    # a cause de sa propre notice.
    texte = re.sub(r"```.*?```", "", texte, flags=re.DOTALL)
    entetes = list(EN_TETE_LECON.finditer(texte))
    resultat = []
    for numero, entete in enumerate(entetes):
        debut = entete.end()
        fin = entetes[numero + 1].start() if numero + 1 < len(entetes) else len(texte)
        corps = texte[debut:fin]
        champs = {}
        for champ in CHAMPS:
            trouve = re.search(rf"^- \*\*{champ}\*\* : (.+)$", corps, re.MULTILINE)
            champs[champ] = trouve.group(1).strip() if trouve else None
        resultat.append({"id": entete.group(1), "titre": entete.group(2), **champs})
    return resultat


def lancer_sur(dossier: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LANCEUR), "--dossier", str(dossier)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class CarnetDeLeconsTests(unittest.TestCase):
    def test_le_carnet_existe(self):
        self.assertTrue(
            LECONS.exists(),
            "_DOCS/LECONS.md est le carnet de lecons du projet : il doit exister.",
        )

    def test_chaque_lecon_a_les_champs_obligatoires(self):
        for lecon in lecons():
            for champ in CHAMPS:
                self.assertIsNotNone(
                    lecon[champ],
                    f"{lecon['id']} : champ '{champ}' manquant. "
                    f"Format attendu : '- **{champ}** : ...'",
                )
            self.assertRegex(
                lecon["Date"],
                FORMAT_DATE,
                f"{lecon['id']} : date attendue au format AAAA-MM-JJ.",
            )

    def test_les_exemples_de_format_ne_sont_pas_lus_comme_des_lecons(self):
        identifiants = [lecon["id"] for lecon in lecons()]
        self.assertNotIn(
            "L-000",
            identifiants,
            "L-000 est l'exemple de format de la notice, dans un bloc de code. "
            "Le lire comme une lecon rend le carnet rouge a cause de sa propre "
            "documentation.",
        )
        self.assertTrue(identifiants, "Le carnet doit contenir au moins une lecon.")

    def test_chaque_lecon_cite_un_controle_existant(self):
        for lecon in lecons():
            reference = (lecon["Contrôle"] or "").strip("`")
            morceaux = reference.split("::")
            self.assertEqual(
                len(morceaux),
                3,
                f"{lecon['id']} : controle attendu sous la forme "
                f"'tests/fichier.py::Classe::methode', recu '{reference}'.",
            )
            fichier, _classe, methode = morceaux
            chemin = RACINE / fichier
            self.assertTrue(
                chemin.exists(),
                f"{lecon['id']} cite {fichier}, qui n'existe pas.",
            )
            self.assertIn(
                f"def {methode}(",
                chemin.read_text(encoding="utf-8"),
                f"{lecon['id']} cite {methode}, absent de {fichier}. "
                f"Une lecon sans controle reel ne protege de rien.",
            )


class RegleDApprentissageTests(unittest.TestCase):
    """La regle qui fait apprendre le depot doit vivre la ou elle est lue.

    Ecrite dans un document que rien ne charge, elle est decorative. CLAUDE.md
    est charge automatiquement a chaque session : c'est le seul endroit ou une
    regle de travail a une chance d'etre appliquee.
    """

    def test_la_regle_d_apprentissage_est_dans_claude_md(self):
        texte = (RACINE / "CLAUDE.md").read_text(encoding="utf-8")
        for attendu in (
            "contrôle",
            "avant",
            "rouge",
            "vert",
            "_DOCS/LECONS.md",
            "tests/lancer.py",
        ):
            self.assertIn(
                attendu,
                texte,
                f"CLAUDE.md ne mentionne pas « {attendu} » : la regle "
                f"d'apprentissage (erreur -> controle ecrit avant la "
                f"correction -> lecon) n'y est pas exploitable.",
            )

    def test_le_socle_declare_un_budget(self):
        socle = json.loads((RACINE / "tests" / "socle.json").read_text(encoding="utf-8"))
        self.assertIn(
            "budget_secondes",
            socle,
            "tests/socle.json doit declarer budget_secondes : un budget "
            "implicite n'est choisi par personne.",
        )
        self.assertGreater(socle["budget_secondes"], 0)


class LanceurTests(unittest.TestCase):
    def test_le_lanceur_sort_en_erreur_si_un_controle_echoue(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "test_faux.py").write_text(CONTROLE_QUI_ECHOUE, encoding="utf-8")
            resultat = lancer_sur(dossier)
            self.assertEqual(
                resultat.returncode,
                1,
                "Un controle rouge doit faire sortir le lanceur en code 1, "
                "sinon la CI et le hook pre-commit laisseront tout passer.",
            )

    def test_le_lanceur_refuse_une_suite_trop_lente(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "test_vrai.py").write_text(CONTROLE_QUI_PASSE, encoding="utf-8")
            (dossier / "socle.json").write_text(
                '{"controles_max": 1, "date": "2026-01-01", "budget_secondes": 0}\n',
                encoding="utf-8",
            )
            resultat = lancer_sur(dossier)
            self.assertEqual(
                resultat.returncode,
                1,
                "Un budget depasse doit faire sortir le lanceur en code 1 : "
                "une suite lente finit par etre sautee.",
            )
            self.assertIn("BUDGET DEPASSE", resultat.stderr)

    def test_le_socle_conserve_ses_reglages_quand_il_est_releve(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "test_vrai.py").write_text(CONTROLE_QUI_PASSE, encoding="utf-8")
            socle = dossier / "socle.json"
            socle.write_text(
                '{"controles_max": 0, "date": "2026-01-01", "budget_secondes": 300}\n',
                encoding="utf-8",
            )
            lancer_sur(dossier)
            apres = json.loads(socle.read_text(encoding="utf-8"))
            self.assertEqual(
                apres.get("budget_secondes"),
                300,
                "Relever le socle ne doit pas effacer les autres reglages : "
                "un reglage perdu en silence revient a une valeur par defaut "
                "que personne n'a choisie.",
            )

    def test_le_lanceur_refuse_une_suite_amputee(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "test_vrai.py").write_text(CONTROLE_QUI_PASSE, encoding="utf-8")
            (dossier / "socle.json").write_text(
                '{"controles_max": 9, "date": "2026-01-01"}\n', encoding="utf-8"
            )
            resultat = lancer_sur(dossier)
            self.assertEqual(
                resultat.returncode,
                1,
                "Passer de 9 controles a 1 doit echouer : le nombre de controles "
                "ne diminue jamais.",
            )
            self.assertIn("SOCLE ROMPU", resultat.stderr)


if __name__ == "__main__":
    unittest.main()
