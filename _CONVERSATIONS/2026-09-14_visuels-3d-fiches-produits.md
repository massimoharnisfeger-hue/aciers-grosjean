# 14 septembre 2026 — Visuels 3D des fiches produits

Séance Claude Code sur le PC : https://claude.ai/code/session_01Vzibs35vdEn9VgM5X9pBFg

## Demande
Mettre trois visuels par fiche produit : une photo studio sur fond blanc, une photo avec les caractéristiques du produit, une photo en situation.
Trouver la meilleure façon de les produire, idéalement gratuitement, et lister tout ce qu'il faut fournir pour y arriver.

## Constats
- 495 fiches, dont beaucoup de variantes d'un même produit : une photo studio et une mise en situation par catégorie suffisent.
- Générer 1 485 images par IA serait long, coûteux et imprécis (formes de profils, chiffres). L'abonnement ChatGPT ne donne pas accès à l'API.
- Le PC (Ryzen 5 4500U, sans carte graphique dédiée) ne permet pas de générer des images IA en local ; Blender tourne sur le processeur.
- Le dépôt Open-Higgsfield-AI n'est qu'une interface pour le service payant Muapi : il n'apporte rien ici.
- Les tableaux fournisseurs VM 2013 déjà récupérés donnent les rayons de congé et d'angle ; les noms des produits donnent motifs, RAL, hauteurs et mailles.
- Le site actuel utilise des rendus 3D et des images génériques, pas des photos du stock.

## Décisions
- Photo studio : 1 par catégorie (Blender ou IA, à trancher).
- Caractéristiques : 1 par fiche, rendu Blender aux cotes exactes + habillage automatique (cotes et fiche lues dans le catalogue).
- Mise en situation : 1 par catégorie, par IA.
- Produits de marque (24) : photos des fournisseurs, pas de 3D.
- Production par vagues, dans l'ordre où les données sont prêtes ; catalogue corrigé avant la production.

## Fait
- Blender 4.5 LTS portable installé ; test IPE 200 rendu et habillé (`_DEPOT/images/test-blender/`).
- Scripts `scripts/rendu-3d/`, générateur du classeur `scripts/generer-collecte-rendus.py`.
- Classeur de collecte `_DEPOT/rendus-3d/collecte-donnees-produits.xlsx` et brief `_DOCS/BRIEF-RENDUS-3D.md`.

## Reste à faire
- [ ] Valider le rendu IPE 200 et trancher les décisions du brief (§ 3.1).
- [ ] Faire remplir le classeur (priorité Vague 1) et prendre les photos de référence des finitions.
- [ ] Corriger le générateur du catalogue : profils U alu, découpe des tôles alu et inox, poteau « VERT RAL 7016 ».
- [ ] Ajouter au script de rendu les autres sections (UPN, cornières, T, plats, ronds, carrés, tubes, tôles) et tester un temps de rendu plus court.
- [ ] Intégrer la galerie de visuels sur les fiches produits.
