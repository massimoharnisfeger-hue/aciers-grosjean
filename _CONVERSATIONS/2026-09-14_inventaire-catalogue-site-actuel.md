# 14 septembre 2026 — Inventaire du catalogue du site actuel

Séance Claude Code sur le PC : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em

## Demande
Explorer tout le catalogue de www.aciersgrosjean.be (catégories, sous-catégories, pagination, recherche, fiches) et relever pour chaque produit : nom, catégorie, référence, prix, variantes, URL, images, et télécharger tous les PDF.
Compter les produits uniques, les organiser, repérer doublons et similaires, présenter une synthèse. Ne rien créer sur le nouveau site.

## Constats
- Site sous nopCommerce. Aucune référence commerciale publiée : seulement un identifiant technique (GUID) et le numéro produit.
- 501 produits, confirmés par trois voies (sitemap, listes des catégories, recherche du site).
- Les 495 produits de la refonte sont exactement les 495 produits rangés du site actuel ; les 6 autres ne sont dans aucune catégorie.
- Un doublon réel (tube 42,4 × 2,5 mm à deux prix), 5 produits invisibles dans la navigation, 2 fiches à double adresse.
- Une même fiche technique, publiée sous 9 noms, sert à toutes les tôles acier (brutes, galvanisées, larmées, corten…).
- 142 produits sans fiche technique, dont tout l'aluminium et l'inox.
- Les 26 documents « /documentation/… » sont des PDF servis sans extension : récupérés aussi.
- Incidents : exploration arrêtée une fois par manque de mémoire sur le PC (reprise depuis le cache, sans perte) ; première détection de doublons trop large (IPE/HEA confondues), remplacée par des règles strictes et un regroupement en familles.

## Décisions
- Données de travail (cache HTML) hors OneDrive : `%LOCALAPPDATA%\SiteAciersGrosjean\crawl`.
- PDF dans `_DEPOT` (hors GitHub public) ; listes et synthèse dans `_DOCS` (Git).
- Images recensées mais pas téléchargées tant que ce n'est pas décidé.

## Fait
`_DOCS/catalogue-site-actuel/SYNTHESE.md` et les fichiers associés ; outils `scripts/inventaire/`.

## Reste à faire
- [ ] Décider ensemble : produits hors catégorie, familles en fiche unique avec choix de dimension, PDF à publier et à renommer, récupération des images, prix TTC ou HTVA.
- [ ] Faire vérifier par Aciers Grosjean la fiche technique commune à toutes les tôles.
