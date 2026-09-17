# Permissions minimales des agents

Les permissions déclarées sont des capacités, pas une autorisation générale. Chaque appel reste soumis au scope, aux STOP et aux human gates.

| Agent | Outils autorisés | Niveau | Interdictions principales |
|---|---|---|---|
| orchestrator | `Read`, `Glob`, `Grep` | lecture/orchestration | pas d'écriture, pas de Bash, pas de push/deploy |
| requirements-architect | `Read`, `Glob`, `Grep` | analyse | pas d'écriture, pas de Bash, pas de décision métier |
| builder | `Read`, `Glob`, `Grep`, `Bash` | écriture ciblée | pas de suppression, migration, push, deploy ou données réelles |
| tester-reviewer | `Read`, `Glob`, `Grep`, `Bash` | vérification | pas d'écriture projet, pas de push/deploy/destruction |
| data-guardian | `Read`, `Glob`, `Grep`, `Bash` | audit en lecture | pas de mutation de données, migration ou données réelles |
| verificateur-rendus | `Read`, `Glob`, `Grep`, `Bash` | vérification visuelle | Bash limité aux vérifications locales prévues, pas d'écriture projet, push ou deploy |

Le Bash est refusé par défaut aux agents qui n'en ont pas besoin. Pour les agents qui l'utilisent, les commandes doivent être non destructives, explicites et liées à la tâche. Une limitation technique complémentaire par sandbox ou approbation humaine reste nécessaire : le Markdown ne constitue pas à lui seul un contrôle d'accès.
