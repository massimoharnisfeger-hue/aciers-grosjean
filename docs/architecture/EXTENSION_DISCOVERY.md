# Extension discovery protocol

## Structural checks

The repository exposes the same skills in two explicit, non-symlinked trees:

- Claude Code: `.claude/skills/`
- Codex: `.agents/skills/`

Each retained skill must contain `SKILL.md`, valid YAML frontmatter, its
versioned support files, and the same bytes in both trees. Run:

```powershell
python scripts/validation/extensions_check.py
python tests/test_extensions.py
```

These commands prove repository structure, frontmatter, parity, pinned MCP
configuration, manifest coverage, and extension-only working-tree scope. They
do not prove that an external host has loaded a skill.

## Host discovery checks

### Codex

Start a fresh Codex session from the repository root and request a read-only
discovery probe for `ui-ux-pro-max` and `frontend-design`. The response must
identify the skill name and the local path under `.agents/skills/`, without
changing files. Record the host version, date, skill paths, and result in the
Project OS test report.

### Claude Code

Start a fresh Claude Code session from the repository root and request the same
read-only discovery probe. The response must identify the skill name and the
local path under `.claude/skills/`, without changing files. Record the host
version, date, skill paths, and result in the Project OS test report.

## Final runtime verification (2026-09-17)

### Codex discovery

The fresh Codex session was launched from the repository in read-only and
ephemeral mode. The repository probe returned both project directories and
readable `SKILL.md` files:

- `ui-ux-pro-max`: files present PASS; structure/readability PASS;
  runtime discovery UNKNOWN; runtime usability UNKNOWN.
- `frontend-design`: files present PASS; structure/readability PASS;
  runtime discovery UNKNOWN; runtime usability UNKNOWN.

The session transcript shows manual inspection of both `.agents/skills/`
paths, but it does not report either skill as discovered or activated by the
Codex skill loader. File presence is therefore not treated as runtime proof.

### Claude Code discovery

Static files and structure are PASS for both skills. Runtime discovery and
runtime usability are UNKNOWN for both skills because the fresh Claude Code
probe stopped before producing a session response with:
`You've hit your weekly limit`. No runtime discovery claim is inferred from
file presence.

### Playwright MCP runtime check

- Pinned package version `0.0.81`: PASS.
- MCP stdio initialization and tool listing: PASS.
- Navigation and snapshot of an ephemeral local fixture: PASS.
- Isolated profile and no-credential configuration: PASS.
- Production access: NOT PERFORMED.
- Current host condition: the browser executable expected by the default
  pinned Playwright environment was unavailable; the protocol probe succeeded
  with an already-present Chromium executable and a temporary configuration
  outside the project. No browser installer was run.

The repository checks prove synchronized discovery trees and configuration,
but host skill-loading remains UNKNOWN until each host can return an explicit
discovery result.
