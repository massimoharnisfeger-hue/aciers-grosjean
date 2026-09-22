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

    def test_la_regle_de_publication_continue_est_ecrite(self):
        """S4 : « chaque modification finie part sur GitHub et Vercel » (demande du 22/09).

        La regle ne vaut que si elle est ecrite la ou une seance la lit, et si
        le bouton sait dire ou en est le deploiement. Sans verification, « c'est
        pousse » ne prouve pas « c'est en ligne » : la branche `main` est
        protegee, et un build Vercel peut echouer apres un push reussi.
        """
        claude = (RACINE / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn(
            "Publier a chaque modification terminee",
            claude,
            "CLAUDE.md doit porter la regle de publication continue demandee le 22/09.",
        )
        chaine = SYNCHRO.read_text(encoding="utf-8", errors="replace") + (
            RACINE / "scripts" / "publier.ps1"
        ).read_text(encoding="utf-8", errors="replace")
        self.assertIn(
            "vercel.com", chaine,
            "La chaine de publication doit renvoyer vers le suivi du deploiement : "
            "pousser n'est pas publier.",
        )
        self.assertIn(
            "aciers-grosjean.vercel.app", chaine,
            "Elle doit donner l'adresse stable a regarder, pas seulement le tableau de bord.",
        )

    def test_la_chaine_de_publication_va_jusqu_a_vercel(self):
        """S5 : le bouton publie, il ne depose pas.

        Demande du proprietaire le 22/09 : « a chaque fois qu'il y a une
        modification, je le vois directement via Vercel ». Or la production
        Vercel ne bouge qu'a une fusion dans `main` : pousser une branche ne
        change rien a ce qu'il voit. La chaine doit donc aller jusqu'au bout —
        pull request, attente du check « quality », fusion — et ne fusionner
        que sur un check vert (ADR-0009).
        """
        publieur = RACINE / "scripts" / "publier.ps1"
        self.assertTrue(publieur.exists(), "scripts/publier.ps1 manquant : la chaine s'arrete au push.")
        texte = publieur.read_text(encoding="utf-8", errors="replace")
        for attendu, pourquoi in (
            ("/pulls", "creer la pull request"),
            ("check-runs", "lire l'etat du check « quality »"),
            ("/merge", "fusionner"),
            ("success", "ne fusionner que sur un check vert"),
        ):
            self.assertIn(attendu, texte, f"publier.ps1 doit {pourquoi} (« {attendu} » absent).")
        self.assertIn(
            "publier.ps1", SYNCHRO.read_text(encoding="utf-8", errors="replace"),
            "synchro.ps1 doit enchainer sur la publication apres un push reussi.",
        )

    def test_aucun_script_ne_rend_stderr_fatal(self):
        """S6 : `$ErrorActionPreference = 'Stop'` + `2>$null` sur une commande native = mort subite.

        PowerShell 5.1 emballe chaque ligne de stderr d'un executable dans une
        ErrorRecord quand la redirection est explicite ; sous 'Stop', cette
        ErrorRecord devient terminante. Verifie le 22/09 : une commande native
        qui ecrit sur stderr et sort en code 0 tue le script sous cette
        combinaison, et le passe sans elle. `publier.ps1` lisait ses
        identifiants ainsi — il serait mort sans message utile.

        La parade est de baisser la preference autour de l'appel, pas de
        supprimer la redirection au hasard.
        """
        for script in sorted(RACINE.glob("_OUTILS/*.ps1")) + sorted(RACINE.glob("scripts/**/*.ps1")):
            texte = script.read_text(encoding="utf-8", errors="replace")
            if "$ErrorActionPreference = 'Stop'" not in texte:
                continue
            fautives = [
                l.strip()[:80]
                for l in texte.splitlines()
                if "2>$null" in l and not l.strip().startswith("#")
            ]
            self.assertEqual(
                fautives, [],
                f"{script.name} declare ErrorActionPreference 'Stop' et redirige stderr "
                f"d'une commande native : le script mourra sur le premier avertissement. "
                f"Ligne(s) : {fautives[:2]}",
            )

    def test_aucun_script_n_alimente_une_commande_native_par_un_tuyau(self):
        """S7 : un tuyau PowerShell n'atteint pas l'entree standard d'un executable ici.

        Mesure du 22/09/2026, sur ce poste : `@('protocol=https','host=github.com','')
        | git credential fill` repond « refusing to work with credential missing
        protocol field » — git ne recoit rien du tout et lit EOF. La meme entree,
        passee par un fichier redirige (`cmd /c "git credential fill < f"`),
        renvoie les quatre lignes attendues. La forme tableau etait deja la
        correction d'un defaut precedent : elle reglait la mise en forme de
        l'entree, pas son acheminement.

        Consequence vecue : la branche partait, la pull request n'etait jamais
        creee, et le proprietaire regardait un site perime en croyant publier.

        La parade est d'ecrire l'entree dans un fichier temporaire sans secret et
        de la rediriger. Ce controle refuse le tuyau vers `git credential`, seul
        cas mesure ; l'etendre demanderait d'avoir mesure les autres.
        """
        for script in sorted(RACINE.glob("_OUTILS/*.ps1")) + sorted(RACINE.glob("scripts/**/*.ps1")):
            texte = script.read_text(encoding="utf-8", errors="replace")
            fautives = [
                l.strip()[:90]
                for l in texte.splitlines()
                if "| git credential" in l and not l.strip().startswith("#")
            ]
            self.assertEqual(
                fautives, [],
                f"{script.name} alimente `git credential` par un tuyau : git lit EOF et "
                f"echoue. Passer par un fichier temporaire redirige. Ligne(s) : {fautives[:2]}",
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
