"""Controles de l'outillage de qualite JavaScript/TypeScript.

`next build` ne lint rien : sans ESLint declare et lance, aucune regle de
qualite JS/TS n'est appliquee sur 40 pages et 32 composants.

Ces controles verifient la DECLARATION (dependance, script, configuration,
synchronisation du lock, etape CI). Ils ne lancent pas ESLint : `npm install`
est interdit dans ce dossier synchronise par OneDrive (CLAUDE.md), et un
controle qui ne peut pas s'executer partout ne doit pas pretendre le faire.
L'execution reelle appartient a `_OUTILS/site-local.ps1` et a la CI.
"""

import json
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
PAQUET = RACINE / "package.json"
LOCK = RACINE / "package-lock.json"
CI = RACINE / ".github" / "workflows" / "quality.yml"

CONFIGURATIONS = ("eslint.config.mjs", "eslint.config.js", ".eslintrc.json")


def paquet() -> dict:
    return json.loads(PAQUET.read_text(encoding="utf-8"))


class LintTests(unittest.TestCase):
    def test_eslint_est_declare_en_dependance_de_developpement(self):
        dev = paquet().get("devDependencies", {})
        for attendu in ("eslint", "eslint-config-next"):
            self.assertIn(
                attendu,
                dev,
                f"{attendu} absent des devDependencies : rien ne lint le code.",
            )

    def test_un_script_lint_existe(self):
        scripts = paquet().get("scripts", {})
        self.assertIn(
            "lint",
            scripts,
            "package.json doit exposer un script `lint` : une dependance "
            "installee que personne n'appelle ne verifie rien.",
        )

    def test_une_configuration_eslint_existe(self):
        presentes = [nom for nom in CONFIGURATIONS if (RACINE / nom).is_file()]
        self.assertTrue(
            presentes,
            f"Aucune configuration ESLint parmi {CONFIGURATIONS}. "
            f"ESLint sans configuration n'applique aucune regle.",
        )

    def test_le_lock_est_synchronise_avec_le_paquet(self):
        """Un lock desynchronise fait echouer `npm ci` en CI.

        C'est le piege de ce chantier : ajouter une dependance a package.json
        sans regenerer package-lock.json casse la CI au premier push, alors que
        tout parait correct en local.
        """
        dev = paquet().get("devDependencies", {})
        lock = LOCK.read_text(encoding="utf-8")
        for dependance in dev:
            self.assertIn(
                f'"node_modules/{dependance}"',
                lock,
                f"{dependance} est dans package.json mais absent de "
                f"package-lock.json : `npm ci` echouera en CI.",
            )

    def test_la_ci_lance_le_lint(self):
        texte = CI.read_text(encoding="utf-8")
        self.assertIn(
            "run lint",
            texte,
            "La CI doit lancer le lint : declare mais jamais execute, il ne "
            "garde rien.",
        )


if __name__ == "__main__":
    unittest.main()
