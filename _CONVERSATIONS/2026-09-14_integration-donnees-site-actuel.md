# 14 septembre 2026 — Intégration des données réelles au nouveau site

Séance Claude Code sur le PC : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em

## Demande
« Je veux que tu mettes tout ça à jour sur mon site » : reporter sur https://aciers-grosjean.vercel.app le relevé du catalogue d'aciersgrosjean.be.

## Constats
- Sur le site actuel, le prix « TTC / PC » des produits à longueur variable correspond à 1 m (longueur présélectionnée, poids affiché d'un mètre).
- Les prix de la refonte étaient des estimations très éloignées : médiane × 1,6, jusqu'à × 10 d'écart.
- Poids factice « 1,0 kg » sur les tôles perforées du site actuel.
- Photos du site actuel : rendus 3D, vraies photos de dépôt, schémas cotés ; au moins une photo de banque d'images avec filigrane Adobe Stock.
- Une autre séance Claude travaille en parallèle sur les visuels 3D des fiches.

## Décisions
- Prix affichés HTVA (TTC ÷ 1,21), TVAC en regard ; données structurées Google en TVAC.
- Unité : au mètre pour les produits à longueur, sinon unité de la refonte (plaque, panneau, unité).
- Aucun montant de découpe inventé : « supplément selon le profil, sur devis ».
- Descriptions reprises en texte brut, sans HTML du site actuel ; cotes A/B/C rangées à part.
- PDF renommés et publiés ; titres explicites pour les documents mal nommés à l'origine.
- Photos du site actuel non intégrées (droits incertains, visuels confiés à la séance 3D).

## Fait
Voir `_JOURNAL/2026-09-14.md`, section « Données réelles du site actuel intégrées au nouveau site ».

## Reste à faire
- [ ] Faire confirmer par Aciers Grosjean le montant des suppléments de découpe.
- [ ] Spécifications générées par la refonte encore fausses sur certaines familles (épaisseur des profils U alu, oxycoupage sur tôles alu/inox) : à corriger avec les cotes relevées.
- [ ] Textes des pages services et conseils qui citent « 2,50 € la coupe » : à confirmer ou retirer.
