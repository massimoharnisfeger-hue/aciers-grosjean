# 24 septembre 2026 — visuels 3D : la fiche servie entière, en 2400 px

Séance web https://claude.ai/code/session_01RAugrmPxtFyRi5jtjzPr1X, branche `claude/gracious-cannon-iql9zs`.

## Demande

« J'aimerais que tu termines le travail de la simulation des pièces 3D […]. Le visuel qu'il m'a fait
était beaucoup mieux, beaucoup plus précis, mais il m'a fait une photo que de la moitié des pièces. »
Puis : « je veux une photo comme ça, avec des dimensions, et une photo studio sans rien » ; « il faut, à
chaque fois, que les mesures soient exactes ».

## Constats

- La « moitié de pièce » venait de deux choses : la vue « D2 » du 23/09 (barre qui sortait du cadre,
  retirée le matin par l'ADR-0011) et le recadrage fait à l'intégration, qui retirait le tableau et,
  sur les fiches, rognait la pièce : le bord droit du cadre (0,62 de la largeur) passait sous la coupe
  (0,615). Contrôle V13, leçon L-063.
- Depuis le 22/09, le site servait les rendus de fiche recadrés, sans leur fiche technique ; l'image
  montrée au propriétaire (avec tableau) n'était donc pas celle du site.
- Premier essai mal compris par l'agent (« je pense que tu as pas compris ce que je veux ») : on a tout
  clarifié par maquettes avant d'agir.

## Décisions (propriétaire)

- Image avec les mesures servie **entière** sur le site (choix B sur trois maquettes) ; photo studio
  inchangée, « sans rien ».
- « Bien détaillé » = plus d'infos et plus net ; tableau **court et utile** : dimensions de la section,
  poids, longueurs standard, procédé ou matière ; pas les valeurs d'ingénieur (inerties, surfaces…).
- 2400 px ; les 24 familles ; poids contradictoires (> 3 %, 50 fiches) : **rien** (non affichés).
- Simulation sur 4 pièces validée (« Oui, c'est bon ») ; tableaux petits sur la page : « Agrandir au
  clic ».
- ADR-0012.

## Fait

Voir `_JOURNAL/2026-09-24.md` (après-midi) et `_DOCS/rendus-3d/avancement.md` (REPRENDRE ICI).
