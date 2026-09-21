# Mémoire active

**Ce fichier ne décrit plus l'état du projet.** L'état est dans
`project-state/CURRENT_STATE.md`, source unique depuis le 21/09/2026 (ligne Z5). Ici ne restent
que les références et les règles de travail. Qui fait autorité sur quoi : `_DOCS/INDEX.md`.

## Références

- Métier : `C:/Users/massi/Downloads/ERP_Aciers_Grosjean_Dossier_Reference_v1.md`.
- Gouvernance : `C:/Users/massi/Downloads/CLAUDE_CODE_PROJECT_GOVERNANCE_AND_AGENT_ARCHITECTURE_v3.md`.
- Protocole : `C:/Users/massi/Downloads/PROMPT_INTRODUCTION_ARCHITECTURE_ERP_ACIERS_GROSJEAN.md`.

Ces trois fichiers sont **hors du dépôt**, non versionnés et invisibles en session web, alors que
`.claude/rules/core.md` les érige en « référence fonctionnelle » et « référence de gouvernance ».
À verser dans le dépôt ou à retirer : ligne **C12**.

## Règles de travail

- Lire avant de modifier.
- Distinguer `FACT`, `DECISION`, `ASSUMPTION`, `UNKNOWN` et `BUSINESS_DECISION_REQUIRED`.
- Limiter chaque tâche à un périmètre explicite.
- Produire une preuve avant de déclarer `DONE`. Une preuve est une sortie de commande, pas une
  impression.
- Arrêter toute opération sensible sans human gate.
- Hiérarchie des règles : `.claude/rules/precedence.md`.
- AUTO-SAVE, AUTO-COMMIT, AUTO-PUSH et DEPLOY sont distincts ; aucun push ou deploy automatique.
- Fait vérifié : `PUSH main → GitHub → Vercel Production Deployment`. Aucun agent ne pousse `main`.
- Toute erreur constatée devient un contrôle dans `tests/`, écrit avant la correction, et une
  leçon dans `_DOCS/LECONS.md`.

## Contrat actif

- Findings canoniques et routing : `scripts/validation/engineering_quality.py`.
- Documentation : `docs/architecture/ENGINEERING_QUALITY_FINDINGS.md` et
  `docs/architecture/ENGINEERING_QUALITY_ROUTING.md`.
- Mode `REPORT-ONLY` ; fix séparé, re-review obligatoire.
