# 23 septembre 2026 — catalogue produits visuel

## Demande

Brief complet « MISSION — CRÉER UN CATALOGUE PRODUITS PROFESSIONNEL À PARTIR DES VISUELS
EXISTANTS » : inventorier toutes les images du projet, les associer aux bons produits, construire un
catalogue visuel (couverture, sommaire, catégories, fiches, variantes, recherche, responsive de 320 px
au bureau), ne modifier aucun visuel, n'en inventer aucun, n'afficher aucune donnée non vérifiée,
réutiliser les routes du site, documenter dans `_DOCS/CATALOGUE-PRODUITS.md`. Puis : « utilise ton
skill /ui-ux-pro-max ou /frontend-design ».

## Constats

- Le dépôt de travail est `C:\Users\massi\Projects\aciers-grosjean` (ADR-0005), pas le dossier
  OneDrive donné dans le message.
- 495 produits en 54 familles ; 466 rendus 3D aux cotes et 48 photos studio validés et servis ;
  29 produits sans rendu (un rendu coté n'y a pas de sens : chimie, visserie, fixations, outillage).
- Aucune référence commerciale exploitable : 501 SKU = GUID.
- Les caractéristiques se partagent naturellement en communes (famille) et distinctives (variante).
- Le site a déjà `/produits` (hub en tableaux) et `/recherche` (index serveur) : le catalogue les
  complète, il ne les remplace pas.

## Décisions

- ADR-0010 : familles comme unité, planches par variante, images du manifeste uniquement, ni prix ni
  référence, filtre sans données embarquées, rendus `unoptimized`, `prefetch={false}`, impression.
- Photos studio en concurrence : le catalogue montre celle que le manifeste sert ; l'arbitrage reste
  humain (inchangé).
- Le `_DEPOT` et l'atelier sont inventoriés en lecture seule ; rien n'y est déplacé.

## Fait

Voir `_JOURNAL/2026-09-23.md`. Pages `/catalogue` et `/catalogue/<univers>`, cinq composants,
quatre modules `lib/`, script d'inventaire et ses sorties, ADR-0010, rapport, contrôles K1-K9 et X1,
leçons L-049 et L-050, raccords (routes, sitemap, menus, pied de page, `/produits`, plan du site).
Typecheck 0, lint 0, build vert, **170 contrôles - 0 échec**.

## Reste à faire

- Arbitrages humains listés dans `_DOCS/CATALOGUE-PRODUITS.md` (photos studio en concurrence,
  produits sans rendu, codes articles, conventions de l'ADR-0010).
- Si le chapitre acier (1,9 Mo brut, 106 Ko gzip) paraît lent sur mobile : une page par
  sous-catégorie pour ce chapitre.
- Publication : commit local ; la chaîne `SAUVEGARDER.cmd` → PR → fusion (ADR-0009) dépend des
  identifiants Git du poste, que la séance ne peut pas actionner elle-même.

## Session

Claude Code, session `e20392c4-1181-4dfa-9625-d3e51cd6589f`, modèle Fable 5.1 (Opus 5.5 en début de
séance).
