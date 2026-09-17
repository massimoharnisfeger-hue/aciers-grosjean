# 17 septembre 2026 — Engineering Quality Foundation

## Demande

Construire le socle interne Engineering Quality du Project OS sans modifier
le site ni intégrer d'outil externe.

## Constats

- Les agents et skills existants couvrent déjà la gouvernance, les
  requirements, la construction, les tests, les données et les rendus 3D.
- Le dépôt n'a pas de framework de tests applicatifs ou de lint à installer à
  ce stade.
- Le workflow Git local est protégé par les règles Project OS et reste
  report-only pour les reviews.

## Décisions

- Un contrat canonique Python version `1.0` porte les findings.
- Les spécialisations restent des modes des agents existants.
- Le routing est déterministe, diff-first et refuse un type inconnu.
- Un fix est séparé et exige une re-review ; les findings bloquants, STOP et
  régressions empêchent le gate.
- Les outils externes restent différés.

## Fait

- Documentation, règles, agents existants, validateur, tests et CI mis à jour.
- Régression complète : 35 tests Python PASS.

## Reste à faire

- Validation humaine du socle.
- Phase ultérieure de baseline lint/tests, puis éventuelle intégration externe
  sous gates dédiés.
