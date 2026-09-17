# Boucle Project OS

```text
DISCOVER → ANALYZE → PLAN → IMPLEMENT → TEST → REVIEW → SIMULATE → SECURITY CHECK → REGRESSION → DOCUMENT → UPDATE MEMORY → VERIFY → DONE / FIX / ESCALATE
```

## Règle générale

Chaque étape reçoit le contexte minimal utile, produit une sortie vérifiable et ne peut passer à l'étape suivante que si sa condition de passage est satisfaite.

## Sous-boucle Engineering Quality

Lorsqu'une tâche est routée vers la qualité du code, la sous-boucle officielle
est :

```text
REVIEW → FINDINGS → FIX → RE-REVIEW → TEST → REGRESSION → GATE → VERIFY
```

`FIX` est séparé et report-only par défaut. Un finding bloquant, un STOP, une
régression ou une re-review manquante empêche le gate. Les détails du contrat
et du routing sont dans `ENGINEERING_QUALITY_FINDINGS.md` et
`ENGINEERING_QUALITY_ROUTING.md`.

## Étapes

| Étape | Responsable initial | Sortie | Preuve | Échec |
|---|---|---|---|---|
| DISCOVER | orchestrator | périmètre et fichiers concernés | inventaire | STOP périmètre inconnu |
| ANALYZE | requirements-architect | faits, décisions, inconnues, impact | note d'analyse | STOP contradiction |
| PLAN | orchestrator + requirements-architect | plan, tests, rollback | plan approuvé | STOP plan incomplet |
| IMPLEMENT | builder | changement limité | diff | STOP hors périmètre |
| TEST | tester-reviewer | résultats ciblés | logs | FIX test échoué |
| REVIEW | tester-reviewer | verdict indépendant | rapport | FIX défaut bloquant |
| SIMULATE | tester-reviewer | scénarios dégradés | rapport sandbox | STOP simulation impossible |
| SECURITY CHECK | tester-reviewer au départ | risques et contrôles | rapport | STOP risque sécurité ou human gate requis |
| REGRESSION | tester-reviewer | régression pertinente | rapport comparatif | FIX régression |
| DOCUMENT | orchestrator + builder | documentation à jour | liens et diff | STOP incohérence |
| UPDATE MEMORY | orchestrator | état et handoff | fichiers d'état | STOP état non reprenable |
| VERIFY | orchestrator | DONE, FIX ou ESCALATE | checklist complète | ESCALATE |

## Simulation et sécurité

Ces étapes sont des emplacements contractuels au stade initial. Aucune infrastructure de simulation avancée, authentification, paiement ou donnée réelle n'est créée par ce Project OS.

`SIMULATE` et `SECURITY CHECK` restent donc documentés et déclenchables par revue manuelle, sans moteur autonome. Pour toute opération sensible, le résultat est `ESCALATE` vers un human gate plutôt qu'une autorisation implicite.

## Arrêt

Un `STOP` est terminal pour la boucle courante. Il est prioritaire sur retry, auto-correction, délégation et automatisation 3D. Il doit être documenté dans le handoff et ne peut être contourné par une répétition automatique.
