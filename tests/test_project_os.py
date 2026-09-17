import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "project-state/CURRENT_STATE.md",
    "project-state/BLOCKERS.md",
    "project-state/TEST_STATUS.md",
    "project-state/HANDOFF_TEMPLATE.md",
    "memory/ACTIVE_CONTEXT.md",
    "memory/OPEN_QUESTIONS.md",
    "memory/REGRESSIONS.md",
    "docs/architecture/PROJECT_OS_LOOP.md",
    "docs/decisions/README.md",
    "docs/requirements/README.md",
    "docs/acceptance/README.md",
    ".claude/agents/orchestrator.md",
    ".claude/agents/requirements-architect.md",
    ".claude/agents/builder.md",
    ".claude/agents/tester-reviewer.md",
    ".claude/agents/data-guardian.md",
    ".claude/agents/verificateur-rendus.md",
    ".claude/skills/discovery/SKILL.md",
    ".claude/skills/project-audit/SKILL.md",
    ".claude/skills/testing/SKILL.md",
    ".claude/rules/core.md",
    ".claude/rules/stop-conditions.md",
    ".claude/rules/change-policy.md",
    ".claude/rules/precedence.md",
    ".claude/rules/agent-permissions.md",
    "docs/architecture/HUMAN_GATE.md",
    "docs/architecture/SYNC_POLICY.md",
    "scripts/validation/project_os_check.py",
    ".github/workflows/quality.yml",
]


class ProjectOsTests(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
        self.assertEqual([], missing, f"Fichiers Project OS manquants : {missing}")

    def test_existing_render_agent_is_preserved(self):
        agent = (ROOT / ".claude/agents/verificateur-rendus.md").read_text(encoding="utf-8")
        self.assertIn("name: verificateur-rendus", agent)
        self.assertIn("Ne modifie rien", agent)

    def test_handoff_contract_is_complete(self):
        handoff = (ROOT / "project-state/HANDOFF_TEMPLATE.md").read_text(encoding="utf-8")
        fields = [
            "OBJECTIVE", "CURRENT STATE", "COMPLETED", "IN PROGRESS", "BLOCKED",
            "FILES TOUCHED", "DECISIONS", "UNKNOWNS", "TESTS RUN",
            "TESTS NOT RUN", "NEXT ACTION",
        ]
        for field in fields:
            self.assertIn(f"## {field}", handoff)

    def test_stop_contract_is_present(self):
        rules = (ROOT / ".claude/rules/stop-conditions.md").read_text(encoding="utf-8")
        for phrase in ["information nécessaire", "décision humaine", "test critique", "périmètre", "STOP"]:
            self.assertIn(phrase, rules)

    def test_no_business_infrastructure_was_added(self):
        forbidden = ["app/api", "prisma", "drizzle", "supabase", "database/migrations"]
        present = [path for path in forbidden if (ROOT / path).exists()]
        self.assertEqual([], present, f"Infrastructure métier interdite détectée : {present}")

    def test_generated_catalogue_contract_remains_intact(self):
        catalogue = (ROOT / "lib/catalogue.ts").read_text(encoding="utf-8")
        self.assertIn("GÉNÉRÉ", catalogue)
        self.assertTrue((ROOT / "scripts/generer-catalogue.py").is_file())

    def test_json_sources_are_valid(self):
        for path in [
            "lib/site-actuel.json",
            "lib/descriptions-site-actuel.json",
            "lib/documents.json",
            "lib/visuels-produits.json",
        ]:
            with self.subTest(path=path):
                json.loads((ROOT / path).read_text(encoding="utf-8"))

    def test_rule_precedence_is_explicit(self):
        rules = (ROOT / ".claude/rules/precedence.md").read_text(encoding="utf-8")
        order = [
            "Sécurité critique et conditions d'arrêt",
            "Human gates et décisions humaines explicites",
            "Règles du projet",
            "Règles du workflow",
            "Règles spécialisées",
            "Instructions de tâche",
        ]
        positions = [rules.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("ne peut pas annuler une règle de sécurité", rules)

    def test_sync_policy_and_script_forbid_automatic_push(self):
        policy = (ROOT / "docs/architecture/SYNC_POLICY.md").read_text(encoding="utf-8")
        script = (ROOT / "_OUTILS/synchro.ps1").read_text(encoding="utf-8")
        for operation in ["AUTO-SAVE", "AUTO-COMMIT", "AUTO-PUSH", "DEPLOY"]:
            self.assertIn(operation, policy)
        self.assertIn("if ($Mode -eq 'auto')", script)
        self.assertIn("AUTO-PUSH DESACTIVE", script)
        self.assertIn("git push", script)

    def test_ci_is_check_only(self):
        ci = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", ci)
        self.assertIn("workflow_dispatch:", ci)
        self.assertNotIn("  push:", ci)
        for forbidden in ["git push", "git commit", "vercel", "npm publish", "rm -rf", "Remove-Item"]:
            self.assertNotIn(forbidden, ci)

    def test_agent_tools_match_minimum_permissions(self):
        expected = {
            "orchestrator": {"Read", "Glob", "Grep"},
            "requirements-architect": {"Read", "Glob", "Grep"},
            "builder": {"Read", "Glob", "Grep", "Bash"},
            "tester-reviewer": {"Read", "Glob", "Grep", "Bash"},
            "data-guardian": {"Read", "Glob", "Grep", "Bash"},
            "verificateur-rendus": {"Read", "Glob", "Grep", "Bash"},
        }
        for name, tools in expected.items():
            content = (ROOT / f".claude/agents/{name}.md").read_text(encoding="utf-8")
            match = re.search(r"^tools:\s*(.+)$", content, flags=re.MULTILINE)
            self.assertIsNotNone(match, name)
            actual = {tool.strip() for tool in match.group(1).split(",")}
            self.assertEqual(tools, actual, name)

    def test_human_gate_contract_is_complete(self):
        gate = (ROOT / "docs/architecture/HUMAN_GATE.md").read_text(encoding="utf-8")
        for field in ["ACTION", "REASON", "RISK", "FILES", "DIFF", "TESTS", "ROLLBACK", "DECISION", "VALIDATED_BY", "DATE_TRACE"]:
            self.assertIn(f"`{field}`", gate)

    def test_no_business_scope_was_added_to_project_os(self):
        governance_files = [
            *[ROOT / path for path in REQUIRED_FILES if path.startswith((".claude/", "docs/architecture/", "project-state/", "memory/"))],
            ROOT / ".github/workflows/quality.yml",
        ]
        forbidden = re.compile(r"(prisma|drizzle|supabase|database/migrations|app/api|git\s+push|git\s+commit|npm\s+publish)", re.IGNORECASE)
        for path in governance_files:
            content = path.read_text(encoding="utf-8")
            self.assertFalse(forbidden.search(content), path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
