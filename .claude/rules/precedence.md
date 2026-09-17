# Hiérarchie des règles

Les règles s'appliquent dans cet ordre, du niveau le plus prioritaire au moins prioritaire :

1. Sécurité critique et conditions d'arrêt.
2. Human gates et décisions humaines explicites.
3. Règles du projet.
4. Règles du workflow.
5. Règles spécialisées, notamment le workflow 3D.
6. Instructions de tâche.

En cas de contradiction, la règle du niveau supérieur prévaut. Une instruction plus récente ne peut pas annuler une règle de sécurité, un STOP ou un human gate. Une règle spécialisée ne peut pas autoriser une opération interdite par les règles supérieures.

`CLAUDE.md` fournit le contexte du projet et les règles spécialisées historiques. Les règles de `.claude/rules/` gouvernent les opérations et prévalent sur toute formulation historique moins stricte. Une demande utilisateur plus restrictive s'applique également.

Le workflow 3D peut continuer localement lorsqu'une référence visuelle manque, mais cette tolérance ne permet ni intégration métier, ni commit, ni push, ni déploiement, et ne contourne jamais un STOP.
