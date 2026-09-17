# Extension memory

Date: `2026-09-17`

## Verified

- UI/UX Pro Max `2.13.0`, commit `15de38fb70bc80ae9276fa7703b48ae861a672e6`.
- Anthropic `frontend-design`, commit `34040c9c568585f6929bedeaad110ad08f079624`.
- Playwright MCP `0.0.81`, commit `e73d72e01f162054a3d0a6b0fe8d4affffb095ee`.
- Claude and Codex skill trees are byte-identical; `.mcp.json` is pinned to local QA origins, headless Chromium, and an isolated profile.
- No external installer, additional MCP, credential, commit, push, deploy, or business-file change was used.

## Unknown

- A fresh host probe is still required to prove runtime skill discovery in Claude Code and Codex. See `docs/architecture/EXTENSION_DISCOVERY.md`.

## Guardrails

- Project OS rules, STOP conditions, human gates, no-invention, no-production, no-Git-write, and no-deploy policies remain authoritative.
- `browser_run_code_unsafe` is forbidden in the normal workflow; browser evaluation is read-only local QA only.
