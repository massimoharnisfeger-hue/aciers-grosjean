import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
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
    "docs/architecture/ENGINEERING_QUALITY_FINDINGS.md",
    "docs/architecture/ENGINEERING_QUALITY_ROUTING.md",
    ".claude/rules/engineering-quality.md",
    "scripts/validation/engineering_quality.py",
]


def media_references():
    suffixes = (".webp", ".avif", ".png", ".jpg", ".jpeg", ".pdf")
    for directory in (ROOT / "app", ROOT / "components", ROOT / "lib"):
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix not in (".ts", ".tsx", ".json"):
                continue
            text = path.read_text(encoding="utf-8")
            for match in re.findall(r"[\w./-]+\.(?:webp|avif|png|jpg|jpeg|pdf)", text, re.IGNORECASE):
                yield path, match, suffixes


def resolve_media(reference):
    if reference.startswith("/"):
        return ROOT / "public" / reference.lstrip("/")
    if reference.startswith("public/"):
        return ROOT / reference
    return None


def main():
    errors = []
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    errors.extend(f"missing required file: {path}" for path in missing)

    for path in [
        "lib/site-actuel.json",
        "lib/descriptions-site-actuel.json",
        "lib/documents.json",
        "lib/visuels-produits.json",
    ]:
        try:
            json.loads((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSON {path}: {error}")

    for source, reference, _ in media_references():
        resolved = resolve_media(reference)
        if resolved is not None and not resolved.is_file():
            errors.append(f"missing media referenced by {source}: {reference}")

    generated = (ROOT / "lib/catalogue.ts").read_text(encoding="utf-8")
    if "GÉNÉRÉ" not in generated or not (ROOT / "scripts/generer-catalogue.py").is_file():
        errors.append("generated catalogue contract is incomplete")

    ci = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    for forbidden in ("  push:", "git push", "git commit", "vercel", "npm publish"):
        if forbidden in ci:
            errors.append(f"CI contains forbidden publication operation: {forbidden}")

    precedence = (ROOT / ".claude/rules/precedence.md").read_text(encoding="utf-8")
    if "Sécurité critique et conditions d'arrêt" not in precedence:
        errors.append("rule precedence contract is incomplete")
    sync = (ROOT / "_OUTILS/synchro.ps1").read_text(encoding="utf-8")
    if "AUTO-PUSH DESACTIVE" not in sync or "if ($Mode -eq 'auto')" not in sync:
        errors.append("sync script does not explicitly block automatic push")

    if errors:
        print("PROJECT OS CHECK: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("PROJECT OS CHECK: PASS")
    print("- required governance files: PASS")
    print("- JSON sources: PASS")
    print("- referenced media and PDFs: PASS")
    print("- generated catalogue contract: PASS")
    print("- engineering quality contract and routing: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
