# Politique de changement

Avant chaque groupe de modifications :

```text
IMPACT ANALYSIS
FILES AFFECTED
RISKS
TESTS
ROLLBACK
```

Par défaut :

- aucune suppression ;
- aucun déplacement ;
- aucune migration ;
- aucun push automatique ;
- aucune donnée réelle dans les tests ;
- aucun changement de prix, sécurité ou production sans validation humaine.

Les fichiers générés sont modifiés par leur générateur ou dans le cadre explicitement documenté par celui-ci.

Pour Engineering Quality, les reviewers sont `REPORT-ONLY`. Une correction
est un groupe de modifications distinct, avec périmètre approuvé, impact
analysis, tests, rollback et re-review du finding original. Un verdict ne vaut
jamais autorisation de modification, de sauvegarde ou de publication.
