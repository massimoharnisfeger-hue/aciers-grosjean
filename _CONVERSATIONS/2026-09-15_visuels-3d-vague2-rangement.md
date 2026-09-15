# 15 septembre 2026 — Visuels 3D : nuit de production, vague 2 en ligne, rangement 2-categories

Séance Claude Code sur le PC (suite de la séance du 14/09) : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em

## Demandes du propriétaire (dans l'ordre)
- Ranger les deux formats de chaque visuel (photo studio fond blanc, visuel avec fiche technique) dans `_DEPOT/images/2-categories`, d'abord « une fois que tu as tout fini », puis à 10 h 30 « mets déjà un maximum de photos Blender ».
- Mémoriser toutes les questions en attente pour pouvoir les compléter plus tard.
- Plus de cœurs (6, le maximum) tout de suite ; PC allumé jusqu'à 13 h ; puis, à 10 h 44, garder 6 cœurs jusqu'au bout.
- Bilan complet à 8 h ; « Go » ; relire `lecons.md`, `avancement.md` et la mémoire avant d'agir ; montrer les images, pas seulement les décrire.
- Le point sur ce qui reste ; vérifier que mémoire, leçons et avancement sont à jour.

## Constats
- La séance de la nuit a été tuée à 0 h 54 par un manque de mémoire (build Node pendant un rendu) : toute la production a été détachée de la séance (scripts PowerShell lancés par `Start-Process`).
- Vérifications indépendantes : 26 familles CONFORMES ; À CORRIGER : treillis à dépassants (donnée `depassants` jamais lue par la géométrie), tubes carrés et rectangulaires inox (dessus noir), tôles inox brossées (brossage invisible), tôles à froid (photo studio en miroir noir). Cause commune des trois derniers : métal trop lisse, l'image montre le reflet du studio sombre.
- Les contrôles automatiques ne voient ni une forme manquante ni une matière trop réfléchissante : deux contrôles de luminance créés et calibrés sur 39 familles.

## Décisions
- Copie du propriétaire : `_DEPOT/images/2-categories/<univers>/<catégorie>/fond-blanc/` et `fiche-technique/`, alimentée à chaque intégration (`integrer_visuels.py`, `CLAUDE.md`, `LISEZ-MOI.txt`) ; `visuels-3d/` supprimé.
- Build pendant les rendus uniquement avec `verifier-leger.ps1` (un worker, tas limité).
- Dépassants : fils prolongés d'une maille au fond et à droite, sans cote (question 32).
- Inox : base 0,62, rugosité 0,46, brossage de 600 stries proportionné à la pièce ; acier à froid : base 0,36, rugosité 0,50 ; photos studio des tôles en métal lisse à 46°.
- Reprises ajoutées en fin de `serie-vague3.json` (146 rendus) plutôt qu'en série séparée ; la chaîne découpe la série au moment de la lancer.

## Fait
- 3 commits poussés : `5fee5ee` (189 fiches de la vague 1 en ligne, dépassants), `25063ce` (rangement 2-categories), `85d7828` (14 familles de la vague 2, matière inox et acier à froid). 345 fiches ont un visuel sur le site ; les mêmes visuels sont dans `2-categories`.
- Questions 31 à 34 ; `alertes-produits.csv` ; journal `_JOURNAL/2026-09-15.md` ; carnet de leçons (dépassants, build allégé, métal lisse, contrôles de matière).

## Reste à faire
- Vague 2b (23 fiches) : habillage et contrôles automatiques (`post_series2.ps1`), vérification indépendante, intégration, build, push.
- Vague 3 (68 fiches + 12 studios) puis reprises (4 treillis à dépassants, 61 rendus inox / tôles à froid / studios galva et alu) : même cycle. Fin des rendus estimée vers 20 h le 15/09.
- Contrôles proposés non créés et défauts mineurs : liste dans `avancement.md`.
- Décisions du propriétaire : 34 questions, fixations (5) et visserie (6) sans 3D.
- À la toute fin : proposer l'étape vidéo.
