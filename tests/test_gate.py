"""Controles du gate : rien ne part avec un controle rouge.

Deux portes doivent porter la meme commande : le hook `pre-commit` en local et
la CI. Si l'une des deux oublie le registre, elle laisse passer une regression.

Ces controles verifient les SOURCES versionnees, jamais l'etat de `.git/hooks`
du poste : ce dossier n'est pas versionne et serait vide en CI, ce qui
produirait un controle rouge chez l'un et vert chez l'autre — le defaut B3.
Le hook est exerce directement, sans jamais creer de commit.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
HOOK = RACINE / "scripts" / "hooks" / "pre-commit"
INSTALLEUR = RACINE / "scripts" / "installer-hooks.ps1"
CI = RACINE / ".github" / "workflows" / "quality.yml"
LANCEUR = RACINE / "tests" / "lancer.py"

CONTROLE_QUI_ECHOUE = """import unittest


class GateTemoin(unittest.TestCase):
    def test_echoue_volontairement(self):
        self.assertTrue(False, "temoin du gate")
"""


class GateTests(unittest.TestCase):
    def test_le_hook_est_versionne(self):
        self.assertTrue(
            HOOK.exists(),
            "scripts/hooks/pre-commit doit exister : .git/hooks n'est pas "
            "versionne, la source doit l'etre.",
        )

    def test_le_hook_lance_le_registre_complet(self):
        texte = HOOK.read_text(encoding="utf-8")
        self.assertIn(
            "tests/lancer.py",
            texte,
            "Le hook doit lancer le registre complet, pas un test isole : "
            "c'est le registre qui porte l'invariant de non-regression.",
        )

    def test_l_installeur_pose_le_hook(self):
        self.assertTrue(INSTALLEUR.exists(), "scripts/installer-hooks.ps1 manquant.")
        texte = INSTALLEUR.read_text(encoding="utf-8")
        self.assertIn(
            "hooks",
            texte,
            "L'installeur doit copier scripts/hooks/ vers .git/hooks.",
        )
        self.assertIn(".git", texte, "L'installeur doit viser .git/hooks.")

    def test_le_bouton_de_sauvegarde_installe_le_gate(self):
        """Un garde-fou facultatif est un garde-fou qu'on oublie d'installer.

        `.git/hooks` n'est pas versionne : sans ce branchement, le hook ne
        protege que les postes ou quelqu'un a pense a lancer l'installateur.
        Branche seulement une fois la suite verte — voir ADR-0003.
        """
        bouton = RACINE / "_OUTILS" / "SAUVEGARDER.cmd"
        texte = bouton.read_text(encoding="utf-8", errors="replace")
        self.assertIn(
            "installer-hooks.ps1",
            texte,
            "_OUTILS/SAUVEGARDER.cmd doit poser les hooks avant de sauvegarder, "
            "sinon le gate reste decoratif sur le poste du proprietaire.",
        )

    def test_la_ci_lance_le_registre(self):
        texte = CI.read_text(encoding="utf-8")
        self.assertIn(
            "tests/lancer.py",
            texte,
            "La CI doit lancer le registre : sans lui, l'invariant « le nombre "
            "de controles ne diminue jamais » n'est verifie nulle part a "
            "distance.",
        )

    def test_le_registre_refuse_un_controle_rouge(self):
        """Exerce la commande du gate, sans creer le moindre commit."""
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "test_temoin.py").write_text(
                CONTROLE_QUI_ECHOUE, encoding="utf-8"
            )
            resultat = subprocess.run(
                [sys.executable, str(LANCEUR), "--dossier", str(dossier)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(
                resultat.returncode,
                1,
                "La commande du gate doit sortir en code 1 sur un controle "
                "rouge, sinon le hook et la CI laissent tout passer.",
            )


if __name__ == "__main__":
    unittest.main()
