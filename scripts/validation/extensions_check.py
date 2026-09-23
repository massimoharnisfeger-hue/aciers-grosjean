import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

UI_DATA_FILES = {
    "app-interface.csv",
    "catalog-summary.json",
    "charts.csv",
    "colors.csv",
    "data-provenance.json",
    "google-font-licenses.json",
    "google-fonts.csv",
    "icons.csv",
    "landing.csv",
    "motion.csv",
    "phosphor-icons-upstream.json",
    "products.csv",
    "react-performance.csv",
    "styles.csv",
    "typography.csv",
    "ui-reasoning.csv",
    "ux-guidelines.csv",
}
UI_STACKS = {
    "angular.csv", "astro.csv", "avalonia.csv", "flutter.csv", "html-tailwind.csv",
    "javafx.csv", "jetpack-compose.csv", "laravel.csv", "nextjs.csv", "nuxt-ui.csv",
    "nuxtjs.csv", "react-native.csv", "react.csv", "shadcn.csv", "svelte.csv",
    "swiftui.csv", "threejs.csv", "uno.csv", "uwp.csv", "vue.csv", "winui.csv",
    "wpf.csv",
}
UI_FILES = {
    "SKILL.md",
    "LICENSE",
    "references/pro-rules.md",
    "references/quick-reference.md",
    "scripts/core.py",
    "scripts/design_system.py",
    "scripts/reasoning_contract.py",
    "scripts/search.py",
    "scripts/validate_data.py",
    *(f"data/{name}" for name in UI_DATA_FILES),
    *(f"data/stacks/{name}" for name in UI_STACKS),
}
FRONTEND_FILES = {"SKILL.md", "LICENSE.txt"}


def read_frontmatter(path):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = content.find("\n---", 4)
    if end < 0:
        raise ValueError(f"unterminated frontmatter: {path}")
    values = {}
    for line in content[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    for key in ("name", "description"):
        if not values.get(key):
            raise ValueError(f"frontmatter missing {key}: {path}")


def fichiers_du_skill(root):
    """Les fichiers d'un skill, sans ce que Python genere en l'executant.

    `__pycache__/` et les `.pyc` apparaissent des qu'on lance le script d'un
    skill (`search.py`), dans la seule copie utilisee. Ce ne sont pas des
    fichiers du skill : Git les ignore, et les compter faisait diverger les
    deux copies sans qu'un octet du skill ait change (23/09, controle X1).
    """
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.relative_to(root).parts
        and path.suffix != ".pyc"
    }


def check_skill_tree(errors, relative_root, expected):
    root = ROOT / relative_root
    if not root.is_dir():
        errors.append(f"missing skill directory: {relative_root}")
        return
    actual = fichiers_du_skill(root)
    if actual != expected:
        errors.append(
            f"unexpected skill files in {relative_root}: "
            f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )
    try:
        read_frontmatter(root / "SKILL.md")
    except (OSError, ValueError) as error:
        errors.append(str(error))


def check_parity(errors, first, second):
    first_root = ROOT / first
    second_root = ROOT / second
    if not first_root.is_dir() or not second_root.is_dir():
        return
    first_files = fichiers_du_skill(first_root)
    second_files = fichiers_du_skill(second_root)
    if first_files != second_files:
        errors.append(f"skill file sets diverge: {first} != {second}")
        return
    for relative in sorted(first_files):
        if (first_root / relative).read_bytes() != (second_root / relative).read_bytes():
            errors.append(f"skill bytes diverge: {first}/{relative} != {second}/{relative}")


def check_mcp(errors):
    path = ROOT / ".mcp.json"
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid .mcp.json: {error}")
        return
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or set(servers) != {"playwright"}:
        errors.append(".mcp.json must contain only the playwright server")
        return
    server = servers["playwright"]
    args = server.get("args", [])
    required = {
        "--yes", "-p", "@playwright/mcp@0.0.81", "playwright-mcp",
        "--headless", "--isolated",
        "--browser", "chromium", "--allowed-origins",
    }
    if server.get("command") != "npx" or not required.issubset(args):
        errors.append("Playwright MCP command is not the audited pinned command")
    if "@latest" in " ".join(args):
        errors.append(".mcp.json uses an unpinned @latest package")
    if "http://localhost:3000;http://127.0.0.1:3000" not in args:
        errors.append("Playwright MCP origins are not restricted to the local QA origins")
    forbidden_args = {
        "--allow-unrestricted-file-access", "--cdp-endpoint", "--extension",
        "--save-session", "--secrets", "--shared-browser-context", "--storage-state",
        "--user-data-dir",
    }
    if forbidden_args.intersection(args):
        errors.append(".mcp.json enables a sensitive Playwright MCP option")
    if re.search(r"(token|secret|password|credential|api[_-]?key)", json.dumps(config), re.IGNORECASE):
        errors.append(".mcp.json contains a credential-like key")


def check_manifest(errors):
    path = ROOT / "docs/architecture/EXTERNAL_CAPABILITIES.md"
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"missing external capability manifest: {error}")
        return
    required = [
        "2.13.0", "15de38fb70bc80ae9276fa7703b48ae861a672e6", "MIT",
        "34040c9c568585f6929bedeaad110ad08f079624", "Apache-2.0",
        "0.0.81", "e73d72e01f162054a3d0a6b0fe8d4affffb095ee",
        "READ", "WRITE", "NETWORK", "SHELL", "GIT", "DEPLOY",
        "@latest", "No additional MCP server",
    ]
    for value in required:
        if value not in content:
            errors.append(f"manifest missing: {value}")


def check_artifact_policy(errors):
    try:
        content = (ROOT / ".gitignore").read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"cannot read .gitignore: {error}")
        return
    if "/.playwright-mcp/" not in content:
        errors.append("ephemeral Playwright MCP output directory is not ignored")


def main():
    errors = []
    for root in (".claude/skills/ui-ux-pro-max", ".agents/skills/ui-ux-pro-max"):
        check_skill_tree(errors, root, UI_FILES)
    for root in (".claude/skills/frontend-design", ".agents/skills/frontend-design"):
        check_skill_tree(errors, root, FRONTEND_FILES)
    check_parity(errors, ".claude/skills/ui-ux-pro-max", ".agents/skills/ui-ux-pro-max")
    check_parity(errors, ".claude/skills/frontend-design", ".agents/skills/frontend-design")
    check_mcp(errors)
    check_manifest(errors)
    check_artifact_policy(errors)
    if errors:
        print("EXTENSIONS CHECK: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("EXTENSIONS CHECK: PASS")
    print("- Claude/Codex skill trees: PASS")
    print("- frontmatter and byte parity: PASS")
    print("- pinned local-only MCP configuration: PASS")
    print("- external capability manifest: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
