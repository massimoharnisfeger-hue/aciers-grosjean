# External capabilities manifest

Status: **PROPOSED FOR HUMAN REVIEW**

This manifest records the audited, pinned extension layer. It does not grant
permission to modify the website, test production, commit, push, or deploy.

Integration date: `2026-09-17`

## Authority and common policy

The Project OS remains authoritative. The order is:

1. critical security and STOP conditions;
2. human gates and explicit human decisions;
3. Project OS rules;
4. project and architecture rules;
5. specialized project rules;
6. external skill or MCP instructions;
7. tool preference.

CI is distinct from merge, release, push, and deploy. No extension may perform
an automatic commit, push, merge, release, or deployment. Any change outside
the extension/docs/tests/configuration scope requires a human gate.

## UI/UX Pro Max

| Field | Audited value |
| --- | --- |
| Role | Local UI/UX research and design-system guidance for the future Website phase |
| Source | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` |
| Version | `2.13.0` (`skill.json`) |
| Commit | `15de38fb70bc80ae9276fa7703b48ae861a672e6` |
| Commit date | `2026-09-15T11:29:29+02:00` |
| License | MIT; source `LICENSE` copied into both installed skill directories |
| Dependencies | Python 3 standard library for local scripts; no project package dependency |
| Installed files | `SKILL.md`, `LICENSE`, `data/`, `references/`, and runtime files in `scripts/` (`core.py`, `design_system.py`, `reasoning_contract.py`, `search.py`, `validate_data.py`) |
| Excluded | Repository CLI, stack installers, tests/fixtures, plugins, and additional MCP suggestions |
| Usage | Local design research, validation, and explicitly requested design-system generation |
| Environment | Project-local Claude Code and Codex skill directories |

The source repository contains installers that can download files, install
packages or browsers, and suggest additional integrations. Those installers
were inspected but not run. The selected skill tree uses local data and does
not itself invoke network, Git, commit, push, or deploy operations. Its
`design_system.py --persist` mode can write output; use it only with an
approved output directory and the normal Project OS change policy.

### UI/UX Pro Max permissions

| Permission | Policy |
| --- | --- |
| READ | ALLOW for its versioned local data and references |
| WRITE | CONDITIONAL; only an explicitly approved design-system output |
| NETWORK | DENY for the installed skill scripts |
| SHELL | CONDITIONAL; Python invocation only, never an installer or arbitrary command |
| GIT | DENY |
| DEPLOY | DENY |

## frontend-design

| Field | Audited value |
| --- | --- |
| Role | Anthropic guidance for distinctive, intentional frontend visual design |
| Source | `https://github.com/anthropics/skills/tree/main/skills/frontend-design` |
| Version | Repository snapshot at the pinned commit; no independent package version |
| Commit | `34040c9c568585f6929bedeaad110ad08f079624` |
| Commit date | `2026-09-10T15:44:08-04:00` |
| License | Apache-2.0; `LICENSE.txt` copied into both installed skill directories |
| Dependencies | None; no scripts, hooks, package, network, or runtime dependency |
| Installed files | `SKILL.md` and `LICENSE.txt` |
| Usage | Design guidance only, subordinate to requirements, scope, accessibility, and Project OS rules |
| Environment | Project-local Claude Code and Codex skill directories |

### frontend-design permissions

| Permission | Policy |
| --- | --- |
| READ | ALLOW for its local instructions |
| WRITE | DENY for the skill itself; any website write remains governed by the Project OS |
| NETWORK | DENY |
| SHELL | DENY |
| GIT | DENY |
| DEPLOY | DENY |

## Playwright MCP

| Field | Audited value |
| --- | --- |
| Role | Local browser navigation, interaction, accessibility and QA support |
| Source | `https://github.com/microsoft/playwright-mcp` |
| Package | `@playwright/mcp` |
| Version | `0.0.81` |
| Commit | `e73d72e01f162054a3d0a6b0fe8d4affffb095ee` (tag `v0.0.81`) |
| Commit date | `2026-09-14T14:18:22-07:00` |
| License | Apache-2.0 |
| Dependencies | Node.js `>=18`; package runtime depends on Playwright and Playwright Core `1.64.0-alpha-2026-09-14` |
| Configuration | `.mcp.json`; explicit `npx -p @playwright/mcp@0.0.81 playwright-mcp`, explicit `chromium` browser, no `@latest` |
| Tools | Core browser navigation, snapshots, tabs, input, dialogs, uploads, screenshots, console, network inspection and WebMCP; `browser_run_code_unsafe` is exposed but forbidden; vision, PDF and devtools capabilities are not enabled |
| Usage | Local page QA only; the current allowlist is `localhost:3000` and `127.0.0.1:3000` |
| Credentials | None configured; no storage state, secrets file, persistent profile, CDP endpoint, extension, or unrestricted file access |

The official CLI reports `Version 0.0.81` and exposes the pinned options used
by `.mcp.json`. The server's origin allowlist is useful configuration but is
not a security boundary and does not constrain redirects; do not use it as a
replacement for the Project OS security gate. The MCP can launch a browser and
write screenshots or other outputs when requested, so those writes remain
conditional and must be restricted to approved temporary/artifact locations.
The official tool list also marks `browser_run_code_unsafe` as RCE-equivalent;
it is not part of the normal Project OS workflow.

The default ephemeral MCP output directory `.playwright-mcp/` is ignored by
Git. It is disposable QA output, not project source or evidence to commit.

### Playwright MCP permissions

| Permission | Policy |
| --- | --- |
| READ | CONDITIONAL; local pages and their browser-visible content only |
| WRITE | CONDITIONAL; approved QA artifacts only, never source or business files |
| NETWORK | CONDITIONAL; local origins only in this phase; redirects still require review |
| SHELL | CONDITIONAL; only the pinned `npx` server launch, not arbitrary shell commands |
| GIT | DENY |
| DEPLOY | DENY |

No additional MCP server has been installed or configured.

## Audit of installation and automation paths

- UI/UX Pro Max advertises `npx ui-ux-pro-max-cli init --ai <platform>`;
  its CLI can download a release and write project or global skill locations.
  Its repository `stack/scripts/setup.sh` can also install npm packages and
  browsers. Neither path was run; no `~/.claude`, `~/.codex`, Git, commit,
  push, or deployment operation was performed by this integration.
- The retained UI/UX runtime tree contains only local Python data/search/
  validation scripts. It has no postinstall hook and no network, Git, commit,
  push, or deployment action.
- Its upstream core `SKILL.md` contains `CLAUDE_PLUGIN_ROOT` examples for the
  plugin distribution. The project rule resolves those examples to the
  explicit Claude or Codex project tree; both installed copies remain byte-
  identical to each other and the audited source tree.
- Anthropic `frontend-design` contains only `SKILL.md` and `LICENSE.txt`; no
  scripts, hooks, dependencies, installers, or global configuration writes
  were found in the retained source.
- The Playwright package exposes the `playwright-mcp` binary and has no
  `postinstall` field. Its package metadata contains test, Docker, browser
  install, and `npm-publish` scripts, but none was run. The special
  `install-browser` path and all publish/deployment paths remain out of scope.
- `.mcp.json` uses `npx --yes -p @playwright/mcp@0.0.81 playwright-mcp`; the
  first use may download that exact package to the local npm cache. It does
  not add a project dependency or lockfile entry. Browser binaries must be
  provisioned separately by the environment owner; this phase does not run a
  browser installer.
- The CLI help lists browser channels without `chromium`, while the audited
  package source accepts `--browser chromium` and resolves it to the managed
  Chromium channel. The pinned version check and extension validator protect
  this choice; a future update must re-audit it.

## Overlap with internal capabilities

| External capability | Internal overlap | Decision |
| --- | --- | --- |
| UI/UX Pro Max | `discovery`, `project-audit`, `builder`, `tester-reviewer`, `verificateur-rendus` | Keep internal scope, stop, validation, and review authority; use UI/UX Pro Max only as a design-analysis complement |
| frontend-design | `builder`, `verificateur-rendus` | Keep internal requirements, acceptance, responsive, and review controls; use this skill only for visual-design guidance |
| Playwright MCP | `testing`, `tester-reviewer`, `verificateur-rendus` | Keep internal test/review gates; use MCP only as a local browser instrument |

External instructions cannot authorize business assumptions, production access,
database work, migration, authentication, payment, pricing, stock, orders,
Git writes, or deployment.

## Update procedure

An update is a deliberate change, never an automatic refresh:

1. inspect the official repository, license, version, commit, scripts, hooks,
   permissions, and dependencies;
2. compare the proposed tree and configuration against this manifest;
3. update both Claude and Codex copies atomically, without symlinks;
4. verify byte-for-byte parity and pinned versions;
5. run Project OS, extension, security, and regression checks;
6. obtain the required human gate before commit, push, release, or deploy.

`@latest` is prohibited in the project configuration. The final runtime
verification is recorded in `docs/architecture/EXTENSION_DISCOVERY.md`.
Repository structure, content readability, pinned Playwright version,
Playwright stdio behavior, local navigation, and local snapshot behavior were
verified. Codex and Claude Code host-level skill discovery remain `UNKNOWN`
for the documented reasons; no inference is made from file presence.
