# ADR-0003 — Le gate n'est pas branché sur le bouton SAUVEGARDER tant que la suite est rouge

```text
ID: ADR-0003
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: Le hook pre-commit (scripts/hooks/pre-commit) et son installateur (scripts/installer-hooks.ps1) sont créés et versionnés, mais _OUTILS/SAUVEGARDER.cmd n'appelle pas encore l'installateur. L'installation reste un geste explicite du propriétaire. Le branchement automatique se fera dans la ligne A2, une fois la ligne B3 corrigée et la suite verte.
REASON: Le registre compte aujourd'hui 62 contrôles dont 1 rouge : tests/test_extensions.py:118-131, couplé au git status du poste, échoue en permanence en local. Vérifié en exécutant le hook directement, sans créer de commit : il sort en code 1. Brancher l'installateur sur SAUVEGARDER.cmd maintenant rendrait le bouton de sauvegarde du propriétaire inopérant dès le prochain clic, pour un défaut connu, déjà répertorié et dont la correction est planifiée. Livrer un garde-fou qui bloque le travail légitime est le meilleur moyen qu'il soit désactivé pour de bon.
IMPACT: Le gate est réel mais volontaire : il ne protège que les postes où `powershell -File scripts/installer-hooks.ps1` a été lancé. La CI, elle, exécute le registre depuis cette itération (étape « Registre des controles » de quality.yml) — sans effet tant que son déclencheur reste `pull_request` seul, ce que corrige la ligne B1. La ligne A2 porte le branchement automatique et cite cet ADR.
SUPERSEDES: —
VALIDATED_BY: Claude, 21/09/2026. Décision d'ordonnancement, réversible en une ligne. Massimo peut l'infirmer en installant le hook tout de suite : `powershell -File scripts/installer-hooks.ps1`.
```

## Contexte

La ligne Z6 demande que rien ne parte avec un contrôle rouge. Le mécanisme est en place des deux
côtés — hook local et étape CI — mais l'activer d'office sur le seul bouton que le propriétaire
utilise reviendrait à lui retirer la possibilité de sauvegarder son travail, aujourd'hui, à cause
d'un défaut qui n'est pas le sien.

## Ordre retenu

1. Z6 : le gate existe, versionné, testé, installable.
2. B3 : correction du contrôle couplé au `git status` du poste.
3. A2 : le hook gagne les contrôles de secrets et de taille, et `SAUVEGARDER.cmd` installe
   l'ensemble automatiquement.

## Résolution — 21/09/2026, même journée

Les trois étapes ont été franchies dans l'ordre prévu. **B3** a levé le dernier contrôle rouge, la
suite est passée à `81 controles - 0 echecs - 4.5 s`, et le branchement a été fait en **A5** :
`_OUTILS/SAUVEGARDER.cmd` installe désormais les hooks avant chaque sauvegarde. Le hook, exercé
directement sans créer de commit, sort en code 0.

Le report a donc duré exactement le temps qu'il fallait. Le principe reste en vigueur pour la
suite : **on ne branche jamais un garde-fou bloquant sur le bouton du propriétaire tant que la
suite n'est pas verte.**

## Ce qu'il faut surveiller

Un garde-fou facultatif est un garde-fou qu'on oublie d'installer. Si la ligne A2 n'est pas
atteinte, ce hook restera décoratif sur tous les postes — exactement le défaut que l'audit du jour
reproche aux règles écrites en Markdown.
