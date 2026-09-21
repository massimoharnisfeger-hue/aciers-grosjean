"""Controles du gate : rien ne part avec un controle rouge.

Deux portes doivent porter la meme commande : le hook `pre-commit` en local et
la CI. Si l'une des deux oublie le registre, elle laisse passer une regression.

Ces controles verifient les SOURCES versionnees, jamais l'etat de `.git/hooks`
du poste : ce dossier n'est pas versionne et serait vide en CI, ce qui
produirait un controle rouge chez l'un et vert chez l'autre — le defaut B3.
Le hook est exerce directement, sans jamais creer de commit.
"""

import re
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
SYNCHRO = RACINE / "_OUTILS" / "synchro.ps1"
POLITIQUE = RACINE / "docs" / "architecture" / "SYNC_POLICY.md"

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

    def test_le_bouton_de_sauvegarde_passe_par_une_branche(self):
        """S1 : `main` est protegee cote GitHub, le bouton ne peut plus la pousser.

        Le 21/09, `git push origin main` a ete refuse : « Changes must be made
        through a pull request » et « Required status check "quality" is
        expected ». Le bouton poussait `main` en dur et, en cas de refus,
        affichait « connexion GitHub a faire » : un message faux qui envoie le
        proprietaire chercher un probleme d'authentification inexistant.

        Le mode `sauvegarder` doit donc pousser une branche de travail et
        donner le lien de la pull request. Le mode `auto` ne pousse toujours
        rien (ADR-0003, `test_sync_policy_and_script_forbid_automatic_push`).
        """
        script = SYNCHRO.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn(
            "git push --quiet origin $branche",
            script,
            "synchro.ps1 pousse encore la branche courante : sur `main`, GitHub "
            "refuse le push et le bouton reste sans effet.",
        )
        self.assertIn(
            "$brancheTravail",
            script,
            "Le mode sauvegarder doit pousser une branche de travail nommee, "
            "pas la branche courante.",
        )
        self.assertIn(
            "/pull/new/",
            script,
            "Le bouton doit afficher le lien de creation de la pull request : "
            "sans lui, le travail dort sur une branche que personne n'ouvre.",
        )

    def test_aucun_parametre_powershell_n_est_ecrase_par_une_variable_locale(self):
        """S3 : PowerShell ignore la casse des variables.

        Le 21/09, `synchro.ps1` declarait le parametre `$Branche` et assignait
        plus bas `$branche = (git rev-parse --abbrev-ref HEAD)`. Ce sont la
        MEME variable : la branche courante ecrasait le parametre, et le mode
        sauvegarder poussait `main` au lieu d'une branche de travail. Le script
        tournait, journalisait, et faisait le contraire de ce qu'il annoncait.

        Aucun outil ne signale cette collision : ni l'analyseur, ni l'execution.
        Elle se voit seulement en lisant le nom deux fois, a deux casses.
        """
        declaration = re.compile(r"^\s*\[.*?\]?\$(\w+)\s*(?:=|,|\))", re.MULTILINE)
        affectation = re.compile(r"^\s*\$(\w+)\s*=", re.MULTILINE)
        for script in sorted(RACINE.glob("_OUTILS/*.ps1")) + sorted(RACINE.glob("scripts/*.ps1")):
            texte = script.read_text(encoding="utf-8", errors="replace")
            bloc = re.search(r"param\s*\((.*?)\n\)", texte, re.DOTALL)
            if not bloc:
                continue
            parametres = {n.lower() for n in declaration.findall(bloc.group(1))}
            corps = texte[bloc.end():]
            collisions = sorted({n for n in affectation.findall(corps) if n.lower() in parametres})
            self.assertEqual(
                collisions,
                [],
                f"{script.relative_to(RACINE).as_posix()} : {collisions} est a la fois "
                f"un parametre et une variable assignee. PowerShell ignore la casse : "
                f"la valeur passee par l'appelant est silencieusement ecrasee.",
            )

    def test_la_politique_decrit_le_flux_par_branche(self):
        """S2 : la politique ecrite dit ce que GitHub impose reellement."""
        politique = POLITIQUE.read_text(encoding="utf-8", errors="replace")
        for attendu in ("pull request", "quality"):
            self.assertIn(
                attendu,
                politique,
                f"SYNC_POLICY.md doit decrire le flux impose par GitHub "
                f"(branche, pull request, check « quality ») : '{attendu}' absent.",
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
