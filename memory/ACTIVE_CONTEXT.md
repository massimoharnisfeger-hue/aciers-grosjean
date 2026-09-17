# Mémoire active

## Références

- Métier : `C:/Users/massi/Downloads/ERP_Aciers_Grosjean_Dossier_Reference_v1.md`.
- Gouvernance : `C:/Users/massi/Downloads/CLAUDE_CODE_PROJECT_GOVERNANCE_AND_AGENT_ARCHITECTURE_v3.md`.
- Protocole : `C:/Users/massi/Downloads/PROMPT_INTRODUCTION_ARCHITECTURE_ERP_ACIERS_GROSJEAN.md`.

## État

Le dépôt est un site catalogue Next.js. Le backend ERP n'est pas construit. La
gouvernance Project OS et la fondation interne Engineering Quality sont
vérifiées ; aucune verticale métier ni intégration externe n'est autorisée.

## Règles de travail

- Lire avant de modifier.
- Distinguer `FACT`, `DECISION`, `ASSUMPTION`, `UNKNOWN` et `BUSINESS_DECISION_REQUIRED`.
- Limiter chaque tâche à un périmètre explicite.
- Produire une preuve avant de déclarer `DONE`.
- Arrêter toute opération sensible sans human gate.
- Hiérarchie : sécurité/STOP > human gate > projet > workflow > spécialisation > tâche.
- AUTO-SAVE, AUTO-COMMIT, AUTO-PUSH et DEPLOY sont distincts ; aucun push ou deploy automatique.
- Fait vérifié : `PUSH main → GitHub → Vercel Production Deployment`. Aucun agent ne pousse `main` automatiquement.

## Tâche active

Socle Engineering Quality interne construit et vérifié. Attendre validation
humaine avant toute intégration externe ou phase Website.

## Contrat actif

- Findings canoniques et routing : `scripts/validation/engineering_quality.py`.
- Documentation : `docs/architecture/ENGINEERING_QUALITY_FINDINGS.md` et
  `docs/architecture/ENGINEERING_QUALITY_ROUTING.md`.
- Mode `REPORT-ONLY` ; fix séparé, re-review obligatoire.
- Aucun nouvel agent, skill, MCP ou dépendance ajouté dans cette phase.
