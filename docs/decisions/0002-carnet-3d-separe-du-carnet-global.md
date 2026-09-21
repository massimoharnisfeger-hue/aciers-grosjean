# ADR-0002 — Le carnet de leçons 3D reste séparé du carnet global

```text
ID: ADR-0002
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: _DOCS/rendus-3d/lecons.md n'est pas fusionné dans _DOCS/LECONS.md. Les deux carnets coexistent, avec des périmètres déclarés : le carnet 3D couvre la fabrication des images (matières, lumières, cadrages, cotes, préréglages Blender), le carnet global couvre le dépôt et sa chaîne de contrôle. Un lien explicite est posé depuis la notice de _DOCS/LECONS.md.
REASON: La ligne Z2 de _DOCS/CHANTIERS-RENFORCEMENT.md prévoyait la fusion. À l'exécution, trois faits l'ont contredite. D'abord le périmètre : les 142 lignes du carnet 3D sont des réglages de rendu, sans contrôle exécutable possible dans tests/ — les y verser aurait forcé soit des leçons sans contrôle (interdit par la règle de Z2), soit des contrôles fictifs. Ensuite l'usage : CLAUDE.md fait lire ce carnet au début de chaque itération de la boucle 3D ; le gonfler de leçons d'infrastructure alourdit une boucle qui a son propre rythme. Enfin la réversibilité : fusionner est faisable plus tard, défusionner après coup ne l'est pas.
IMPACT: La ligne Z2 est corrigée pour refléter la séparation et renvoyer à cet ADR. Le contrôle tests/test_socle.py ne vérifie que _DOCS/LECONS.md ; le carnet 3D reste sans contrôle de forme, ce qui est une dette assumée et notée. Si la production 3D reprend et produit des leçons de chaîne plutôt que de rendu, la question se rouvre — par un nouvel ADR, pas par une décision silencieuse.
SUPERSEDES: —
VALIDATED_BY: Claude, 21/09/2026, au titre d'un écart d'exécution assumé. Massimo n'a pas tranché : à confirmer ou à infirmer.
```

## Contexte

Le chantier Z2 demandait un carnet de leçons global qui « généralise `_DOCS/rendus-3d/lecons.md`,
qui y est fusionné ». La fusion n'a pas eu lieu.

L'écart est déclaré ici plutôt que corrigé en silence dans la ligne de chantier, parce qu'une
spécification discrètement réalignée sur ce qui a été fait est le premier pas vers un état qui
ment — exactement ce que l'audit du jour reproche à `CURRENT_STATE.md`.

## Ce qu'il faut surveiller

Deux carnets, c'est deux endroits où chercher. Le risque est qu'une leçon d'infrastructure
atterrisse dans le carnet 3D parce que la séance était une séance 3D. La notice de
`_DOCS/LECONS.md` nomme la frontière ; si elle est franchie deux fois, il faudra fusionner.
