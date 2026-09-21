import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validation.extensions_check import (  # noqa: E402
    FRONTEND_FILES,
    UI_FILES,
    main as extensions_check,
)




class ExtensionTests(unittest.TestCase):
    def test_extension_validator_passes(self):
        self.assertEqual(0, extensions_check())

    def test_skill_file_sets_are_exact_and_identical(self):
        for name, expected in (
            ("ui-ux-pro-max", UI_FILES),
            ("frontend-design", FRONTEND_FILES),
        ):
            claude = ROOT / ".claude/skills" / name
            codex = ROOT / ".agents/skills" / name
            for tree in (claude, codex):
                actual = {
                    path.relative_to(tree).as_posix()
                    for path in tree.rglob("*")
                    if path.is_file()
                }
                self.assertEqual(expected, actual, str(tree))
            for relative in expected:
                self.assertEqual(
                    (claude / relative).read_bytes(),
                    (codex / relative).read_bytes(),
                    f"skill divergence: {name}/{relative}",
                )

    def test_skill_frontmatter_is_present(self):
        for relative in (
            ".claude/skills/ui-ux-pro-max/SKILL.md",
            ".claude/skills/frontend-design/SKILL.md",
        ):
            content = (ROOT / relative).read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"), relative)
            frontmatter = content.split("\n---", 1)[0]
            self.assertRegex(frontmatter, r"(?m)^name:\s*\S+")
            self.assertRegex(frontmatter, r"(?m)^description:\s*.+")

    def test_mcp_is_project_local_pinned_and_secret_free(self):
        config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["playwright"]
        args = server["args"]
        self.assertEqual("npx", server["command"])
        self.assertIn("-p", args)
        self.assertIn("@playwright/mcp@0.0.81", args)
        self.assertIn("playwright-mcp", args)
        self.assertNotIn("@latest", args)
        self.assertIn("--headless", args)
        self.assertIn("--isolated", args)
        self.assertIn("--browser", args)
        self.assertIn("chromium", args)
        self.assertIn("http://localhost:3000;http://127.0.0.1:3000", args)
        self.assertNotRegex(json.dumps(config), r"(?i)(secret|token|password|credential|api[_-]?key)")
        self.assertIn("/.playwright-mcp/", (ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_manifest_records_source_versions_and_permissions(self):
        content = (ROOT / "docs/architecture/EXTERNAL_CAPABILITIES.md").read_text(encoding="utf-8")
        for value in (
            "2.13.0", "15de38fb70bc80ae9276fa7703b48ae861a672e6",
            "34040c9c568585f6929bedeaad110ad08f079624", "0.0.81",
            "e73d72e01f162054a3d0a6b0fe8d4affffb095ee",
            "READ", "WRITE", "NETWORK", "SHELL", "GIT", "DEPLOY",
        ):
            self.assertIn(value, content)

    def test_no_tracked_file_is_deleted_in_the_working_tree(self):
        """Aucun fichier suivi ne doit avoir disparu du working tree.

        Reserve declaree (voir L-005) : ce controle lit le `git status` du
        poste. En CI, sur un checkout neuf, il n'inspecte rien et passe au vert
        par vacuite. C'est un garde LOCAL, utile avant un commit, pas une
        preuve a distance. Mesure du 21/09 : 26 chemins inspectes en local.

        L'ancienne version exigeait en plus que chaque chemin modifie figure
        dans une liste blanche ecrite le 17/09. Cette liste etait un instantane
        d'une seance : toute journee de travail normale la rendait rouge, et un
        controle rouge en permanence finit par etre ignore, y compris quand il
        a raison (defaut B3, lecon L-011).
        """
        result = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        supprimes = [
            line[3:].strip().strip('"')
            for line in result.stdout.splitlines()
            if line[:2].strip().startswith("D")
        ]
        self.assertEqual(
            supprimes,
            [],
            f"Fichiers suivis supprimes du working tree : {supprimes}. "
            f"Une suppression se decide, elle ne se constate pas.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
