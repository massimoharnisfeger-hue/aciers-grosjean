"""Controles d'hygiene du depot.

Le depot GitHub est PUBLIC, et `_OUTILS/SAUVEGARDER.cmd` declenche un
`git add -A` suivi d'un push, sans revue de diff. Tout ce que `.gitignore`
laisse passer part donc en ligne au premier double-clic.

Ces controles interrogent Git lui-meme (`git check-ignore`) plutot que de lire
le texte de `.gitignore` : c'est le comportement reel qui compte, pas la
presence d'une ligne qui pourrait etre annulee plus bas par une negation.
Aucun fichier n'est cree, aucun commit n'est fait.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]

# Chemins qui ne doivent JAMAIS pouvoir etre commites sur un depot public.
A_IGNORER = (
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".vercel/project.json",
    ".claude/settings.local.json",
    "cle-privee.pem",
    "jeton.key",
    "_OUTILS/synchro.log",
)

# Contre-epreuve : ce qui doit rester versionne. Un `.gitignore` trop large est
# aussi un defaut — il fait disparaitre du code sans que personne le voie.
A_SUIVRE = (
    "CLAUDE.md",
    "next.config.mjs",
    "lib/catalogue.ts",
    "tests/lancer.py",
)


def est_ignore(chemin: str) -> bool:
    resultat = subprocess.run(
        ["git", "check-ignore", "-q", chemin],
        cwd=RACINE,
        capture_output=True,
    )
    # 0 = ignore, 1 = non ignore, 128 = erreur (pas un depot, git absent)
    if resultat.returncode not in (0, 1):
        raise RuntimeError(
            f"git check-ignore a echoue sur '{chemin}' "
            f"(code {resultat.returncode}). Le controle ne peut rien garantir."
        )
    return resultat.returncode == 0


VERIFICATEUR = RACINE / "scripts" / "hooks" / "verifier-depot.py"
HOOK = RACINE / "scripts" / "hooks" / "pre-commit"

JETON_FACTICE = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


def verifier(dossier: Path, chemins: list[str]) -> subprocess.CompletedProcess:
    """Exerce le verificateur sur des chemins, sans jamais creer de commit."""
    return subprocess.run(
        [sys.executable, str(VERIFICATEUR)],
        input="\n".join(chemins),
        cwd=dossier,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class VerificateurDeCommitTests(unittest.TestCase):
    """Le hook refuse-t-il vraiment ce qu'il annonce refuser ?

    La logique est dans un script separe precisement pour etre exercable :
    un controle qui devrait creer un commit pour se verifier ne serait jamais
    ecrit.
    """

    def test_le_verificateur_existe(self):
        self.assertTrue(
            VERIFICATEUR.exists(),
            "scripts/hooks/verifier-depot.py porte les controles de secrets et "
            "de taille du hook pre-commit.",
        )

    def test_il_refuse_un_fichier_env(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / ".env").write_text("SMTP_PASSWORD=motdepasse\n", encoding="utf-8")
            resultat = verifier(dossier, [".env"])
            self.assertEqual(
                resultat.returncode, 1, "Un .env doit etre refuse."
            )
            self.assertIn(".env", resultat.stdout + resultat.stderr)

    def test_il_accepte_un_exemple_d_environnement(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / ".env.example").write_text("SMTP_PASSWORD=\n", encoding="utf-8")
            resultat = verifier(dossier, [".env.example"])
            self.assertEqual(
                resultat.returncode,
                0,
                ".env.example documente les variables attendues sans valeur : "
                "il doit rester versionnable.",
            )

    def test_il_refuse_un_fichier_trop_gros(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            gros = dossier / "gros.bin"
            gros.write_bytes(b"0" * (6 * 1024 * 1024))
            resultat = verifier(dossier, ["gros.bin"])
            self.assertEqual(
                resultat.returncode, 1, "Un fichier de 6 Mo doit etre refuse."
            )

    def test_il_refuse_un_jeton(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "config.ts").write_text(
                f'export const jeton = "{JETON_FACTICE}";\n', encoding="utf-8"
            )
            resultat = verifier(dossier, ["config.ts"])
            self.assertEqual(
                resultat.returncode, 1, "Un jeton GitHub doit etre refuse."
            )

    def test_il_accepte_un_fichier_normal(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "page.tsx").write_text(
                "export default function Page() { return null; }\n", encoding="utf-8"
            )
            resultat = verifier(dossier, ["page.tsx"])
            self.assertEqual(
                resultat.returncode,
                0,
                f"Un fichier ordinaire doit passer. Sortie : {resultat.stdout}",
            )

    def test_la_ci_et_le_hook_partagent_les_memes_motifs(self):
        """Une source unique de motifs, sinon les deux portes divergent.

        Avant le 21/09, la CI cherchait 4 motifs en `git grep` inline et le
        hook 9 : un jeton Notion ou Google passait la CI sans etre vu.
        """
        ci = (RACINE / ".github" / "workflows" / "quality.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "verifier-depot.py",
            ci,
            "La CI doit appeler le verificateur au lieu de redefinir ses "
            "propres motifs : deux listes divergent toujours.",
        )

    def test_le_verificateur_a_un_mode_secrets_seulement(self):
        """La CI scanne tout le depot : la taille y est hors sujet.

        Sans ce mode, la CI echouerait sur des PDF deja versionnes et serait
        rouge en permanence — donc ignoree.
        """
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            gros = dossier / "gros.bin"
            gros.write_bytes(b"0" * (6 * 1024 * 1024))
            resultat = subprocess.run(
                [sys.executable, str(VERIFICATEUR), "--secrets-seulement"],
                input="gros.bin",
                cwd=dossier,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(
                resultat.returncode,
                0,
                "En mode secrets, la taille ne doit pas declencher d'echec.",
            )

    def test_le_mode_secrets_attrape_toujours_un_jeton(self):
        with tempfile.TemporaryDirectory() as temporaire:
            dossier = Path(temporaire)
            (dossier / "config.ts").write_text(
                f'const j = "{JETON_FACTICE}";\n', encoding="utf-8"
            )
            resultat = subprocess.run(
                [sys.executable, str(VERIFICATEUR), "--secrets-seulement"],
                input="config.ts",
                cwd=dossier,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(
                resultat.returncode,
                1,
                "Le mode secrets doit rester strict sur les secrets.",
            )

    def test_le_hook_appelle_le_verificateur(self):
        texte = HOOK.read_text(encoding="utf-8")
        self.assertIn(
            "verifier-depot.py",
            texte,
            "Le hook doit appeler le verificateur : un script que personne "
            "n'appelle ne protege rien.",
        )


class GitignoreTests(unittest.TestCase):
    def test_git_est_disponible(self):
        """Sans Git, les controles ci-dessous seraient verts sans rien verifier."""
        resultat = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=RACINE,
            capture_output=True,
        )
        self.assertEqual(
            resultat.returncode,
            0,
            "Ces controles interrogent Git : sans depot Git, ils ne prouvent rien.",
        )

    def test_les_fichiers_sensibles_sont_ignores(self):
        oublies = [chemin for chemin in A_IGNORER if not est_ignore(chemin)]
        self.assertEqual(
            oublies,
            [],
            f"Le depot est PUBLIC et SAUVEGARDER.cmd fait `git add -A` puis "
            f"push sans revue. Ces chemins seraient commites : {oublies}. "
            f"Une cle Vercel ou SMTP part en ligne en un double-clic.",
        )

    def test_le_code_reste_versionne(self):
        perdus = [chemin for chemin in A_SUIVRE if est_ignore(chemin)]
        self.assertEqual(
            perdus,
            [],
            f"Ces fichiers sont ignores alors qu'ils doivent etre versionnes : "
            f"{perdus}. Un .gitignore trop large fait disparaitre du code sans "
            f"que personne le voie.",
        )


if __name__ == "__main__":
    unittest.main()
