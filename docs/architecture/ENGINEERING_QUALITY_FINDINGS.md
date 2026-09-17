# Engineering Quality — contrat interne des findings

## Statut

- **EXISTING** : le Project OS possède déjà des agents de revue et des règles
  de preuve.
- **DECIDED** : un seul contrat interne sérialisable est utilisé par les
  reviewers internes et les futurs adaptateurs externes.
- **TARGET** : l'agrégation et la déduplication seront exécutées par
  l'orchestrator selon ce contrat.
- **DEFERRED** : aucun adaptateur externe, auto-fix ou stockage automatisé des
  runs n'est activé dans cette phase.

La représentation technique canonique est implémentée sans dépendance externe
dans `scripts/validation/engineering_quality.py`. Ce document décrit son
contrat lisible par les agents.

## 1. Contrat canonique

Un finding est un objet JSON versionné. La version courante du contrat est
`1.0`.

### Champs obligatoires

| Champ | Valeurs/type | Rôle |
|---|---|---|
| `id` | chaîne stable | Identité du finding |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` | Gravité |
| `category` | catégorie définie ci-dessous | Nature du constat |
| `title` | chaîne courte | Résumé actionnable |
| `description` | chaîne | Constat contextualisé |
| `evidence` | liste de chaînes non vide | Preuves observées |
| `affected_files` | liste de chemins relatifs non vide | Périmètre touché |
| `affected_lines` | liste de localisations ou `UNKNOWN` | Localisation disponible |
| `risk` | objet `impact` + `blast_radius` | Conséquence potentielle |
| `suggested_remediation` | chaîne ou `NONE` | Proposition, jamais ordre d'exécution |
| `blocker` | booléen | Blocage explicite dans le contexte |
| `reviewer` | chaîne | Agent, mode ou source |
| `confidence` | objet `level` + `rationale` | Confiance dans le constat |
| `status` | statut du cycle ci-dessous | État du finding |
| `re_review_required` | booléen | Revue après correction |

### Champs complémentaires

Les champs complémentaires autorisés sont :

`run_id`, `parent_finding_id`, `baseline_ref`, `diff_ref`, `introduced_by`,
`requirement_refs`, `acceptance_refs`, `test_refs`, `evidence_refs`,
`data_classification`, `human_gate_required`, `human_gate_ref`, `owner`,
`due_phase`, `duplicate_of`, `contradicts`, `tool_version`, `source_sha`.

Ils sont facultatifs pour un finding local, mais obligatoires lorsqu'un cas
particulier le rend nécessaire : traçabilité, donnée sensible, gate, source
externe ou déduplication.

Les extensions de champ doivent rester compatibles avec la sérialisation JSON
et être documentées avant utilisation. Elles ne créent pas un second format.

## 2. Catégories et verdicts

Catégories minimales :

`BUG`, `SECURITY`, `ARCHITECTURE`, `TYPE`, `TEST`, `ERROR_HANDLING`,
`PERFORMANCE`, `SIMPLIFICATION`, `MAINTAINABILITY`, `DATA`, `UX`,
`COMPLIANCE`.

Règles de blocage :

- `CRITICAL` : toujours bloquant jusqu'à résolution, re-review et preuve.
- `HIGH` : bloquant, sauf acceptation explicite par human gate valide.
- `MEDIUM` : bloquant si `blocker` vaut `true` ou si le contexte touche une
  exigence, une régression, la sécurité, les données, la production ou le
  rollback ; sinon correction planifiée ou justification avant release.
- `LOW` et `INFO` : non bloquants par défaut, sauf `blocker` explicitement
  positionné.

Les catégories ne sont pas des niveaux de gravité. Un finding de style ne
devient pas un bug sans preuve.

## 3. Cycle de vie

```text
OPEN → IN_PROGRESS → FIXED → RE_REVIEW → VERIFIED
```

Issues alternatives :

- `OPEN → ESCALATED` quand une décision, une contradiction ou un risque exige
  une intervention supérieure ;
- `OPEN → ACCEPTED_WITH_JUSTIFICATION` uniquement avec human gate valide ;
- une re-review échouée revient à `OPEN` ou `ESCALATED` selon le risque.

Les statuts autorisés sont `OPEN`, `IN_PROGRESS`, `FIXED`, `RE_REVIEW`,
`VERIFIED`, `ACCEPTED_WITH_JUSTIFICATION`, `ESCALATED` et `WONT_FIX`. Les deux
derniers statuts de clôture exceptionnelle exigent une décision humaine
traçable.

Un reviewer ne peut pas passer lui-même un finding modifié à `VERIFIED` sans
nouvelle preuve de diff et de re-review. Un finding `FIXED` avec
`re_review_required` reste non validé.

## 4. Agrégation et déduplication

- Chaque passe reçoit un `run_id` et une référence de baseline/diff.
- Deux findings ayant même catégorie, titre normalisé et fichiers affectés
  partagent une clé de groupe ; le plus sévère devient le finding représentatif.
- `duplicate_of` conserve la relation sans perdre la source originale.
- `parent_finding_id` représente une cause ou un finding parent.
- `contradicts` conserve une contradiction ; elle déclenche `STOP` tant qu'elle
  n'est pas arbitrée.
- Les findings de sources différentes ne sont jamais fusionnés uniquement par
  similarité textuelle sans preuve de déduplication.
- La sévérité, le reviewer, la confiance, la version d'outil et le SHA source
  restent traçables après agrégation.

## 5. Report-only et sécurité

Les reviewers analysent, sérialisent, agrègent et proposent. Ils ne modifient
pas le code et ne réalisent aucune opération Git ou publication.

Un fix est une étape séparée, portée par `builder`, avec périmètre approuvé,
impact analysis, tests, rollback et re-review. Un mode spécialisé n'acquiert
aucune permission supplémentaire.

Un STOP interrompt revue, agrégation, fix, retry, délégation et parallélisme.
Le contrat de finding ne remplace pas les human gates, les règles de sécurité
ou les règles métier.

## 6. Adaptateurs futurs

Les producteurs suivants pourront utiliser le même contrat :

- reviewer interne ;
- reviewer React/Next ;
- reviewer tests ;
- reviewer sécurité ;
- reviewer externe approuvé.

Un adaptateur externe fournit sa version et son `source_sha`, mais ne devient
jamais l'autorité du Project OS.
