# Engineering Quality — routing par risque

## Statut

Ce routage est la matrice interne versionnée. Il est diff-first : le type
explicite de tâche est confirmé par les fichiers, le domaine et le blast
radius. Un type inconnu ne reçoit pas une permission implicite.

`scripts/validation/engineering_quality.py` contient la représentation
technique testée de cette matrice.

## Matrice

| Type | Modes obligatoires | Modes optionnels | Tests obligatoires | Playwright | Human gate |
|---|---|---|---|---|---|
| `simple_ui` | `code-quality` | `react-next` | selon comportement | `CONDITIONAL` | `NOT_REQUIRED` |
| `react_component` | `code-quality`, `react-next` | `performance` | comportement | `CONDITIONAL` | `NOT_REQUIRED` |
| `next_page` | `code-quality`, `react-next` | `performance` | comportement, régression | `CONDITIONAL` | `CONDITIONAL` |
| `refactor` | `code-quality`, `architecture`, `tests` | `simplification` | régression | `CONDITIONAL` | `CONDITIONAL` |
| `new_feature` | `code-quality`, `tests` | `architecture`, `react-next`, `performance` | comportement, régression | `CONDITIONAL` | `CONDITIONAL` |
| `business_logic` | `code-quality`, `tests` | `architecture`, `error-handling` | cas limites, régression | `CONDITIONAL` | `CONDITIONAL` |
| `data` | `data`, `tests` | `security-data` | intégrité, régression | `NOT_REQUIRED` | `CONDITIONAL` |
| `catalogue` | `data`, `tests` | `security-data` | sources, intégrité | `NOT_REQUIRED` | `CONDITIONAL` |
| `stock` | `data`, `tests` | `security-data`, `architecture` | invariants, régression | `CONDITIONAL` | `CONDITIONAL` |
| `command` | `data`, `tests` | `security-data`, `architecture` | invariants, parcours | `CONDITIONAL` | `CONDITIONAL` |
| `payment` | `security-data`, `data`, `tests` | `architecture` | sécurité, cas d'échec, régression | `CONDITIONAL` | `REQUIRED` |
| `authentication` | `security-data`, `architecture`, `tests` | `error-handling` | accès positif/négatif | `CONDITIONAL` | `REQUIRED` |
| `permissions` | `security-data`, `architecture`, `tests` | `data` | isolation, accès négatif | `CONDITIONAL` | `REQUIRED` |
| `migration` | `data`, `architecture`, `tests` | `security-data` | simulation, rollback, régression | `NOT_REQUIRED` | `REQUIRED` |
| `dependency` | `code-quality`, `security-data` | `performance`, `architecture` | typecheck, build, régression | `NOT_REQUIRED` | `CONDITIONAL` |
| `configuration` | `code-quality`, `architecture` | `security-data` | validation de configuration | `CONDITIONAL` | `CONDITIONAL` |
| `sensitive_change` | `security-data`, `architecture`, `tests` | `data` | sécurité, régression | `CONDITIONAL` | `REQUIRED` |
| `release` | `code-quality`, `architecture`, `tests` | `security-data`, `react-next`, `performance`, `data` | suite de régression | `CONDITIONAL` | `REQUIRED` |

`CONDITIONAL` signifie que l'orchestrator doit justifier la présence ou
l'absence du contrôle dans le run. Il ne signifie jamais « ignorer ».

## Agents porteurs

- `tester-reviewer` porte `code-quality`, `error-handling`, `tests`,
  `simplification`, `react-next` et `performance`.
- `requirements-architect` porte `types` et `architecture`.
- `data-guardian` porte `data` et `security-data`.
- `orchestrator` classe le risque, route et agrège ; il ne produit pas seul la
  validation métier ou sécurité.
- `builder` intervient seulement dans l'étape FIX séparée et approuvée.

## Règles d'exécution

1. `DISCOVER` capture les fichiers suivis, non suivis, les domaines et les
   changements sensibles.
2. Le routage est calculé avant le chargement des modes et skills.
3. Les analyses read-only sans chevauchement peuvent être parallèles.
4. Les fichiers partagés, données sensibles, contradictions et gates sont
   traités séquentiellement.
5. Un finding bloquant, un STOP ou un gate manquant suspend le routage.
6. Une correction relance seulement les reviewers pertinents, mais toujours
   avec re-review du finding original et contrôle de régression.
7. Toute décision non couverte par la matrice devient `ESCALATE`, pas une
   permission par défaut.

## Hors scope

Cette matrice n'active aucun outil externe, aucun auto-fix, aucune modification
du site et aucune opération de données ERP. Les intégrations externes restent
des adaptateurs futurs soumis aux mêmes contrôles.
