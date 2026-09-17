# Règles Engineering Quality

Cette règle est spécialisée sous la hiérarchie de `precedence.md`. Elle ne
peut pas contredire une règle de sécurité, un STOP, un human gate ou une règle
du projet.

## Contrat

- Le contrat canonique est décrit dans
  `docs/architecture/ENGINEERING_QUALITY_FINDINGS.md` et validé par
  `scripts/validation/engineering_quality.py`.
- Tous les reviewers utilisent les mêmes sévérités, catégories, statuts et
  champs de traçabilité.
- Une sortie non conforme au contrat est `FAIL` et ne peut pas être agrégée.

## REPORT-ONLY

- Les reviews sont en lecture et en rapport par défaut.
- Aucun reviewer ne modifie automatiquement le projet.
- Le fix est une étape distincte confiée à `builder` après plan approuvé.
- Aucune opération de sauvegarde, commit, publication ou déploiement ne peut
  être déduite d'un verdict de review.

## Re-review

- Toute correction d'un finding exige une re-review ciblée.
- `FIXED` n'est pas `VERIFIED`.
- Un finding bloquant ouvert, fixé sans re-review ou contradictoire empêche le
  passage de gate.
- Un agent ne peut pas auto-approuver une correction qu'il a produite.

## STOP

Un STOP interrompt la boucle, les retries, l'auto-correction, la délégation,
le parallélisme et toute automatisation spécialisée. Les causes minimales
sont : contrat invalide, contradiction, périmètre dépassé, preuve absente,
test critique échoué, régression, gate manquant ou risque sensible non arbitré.

## Agrégation

- Les runs, baselines, diffs, reviewers, versions et sources restent liés.
- Une similarité ne suffit pas à supprimer un finding.
- Une contradiction est conservée et escaladée.
- L'agrégateur ne baisse jamais la sévérité sans preuve et décision tracée.

## Permissions

Un mode hérite des permissions de son agent porteur. Son nom, sa skill ou sa
source ne lui donne aucun outil supplémentaire. Les permissions effectives
restent celles de `agent-permissions.md` et des contrôles techniques de
l'environnement.
