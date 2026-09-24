# ADR-0012 — La fiche produit est servie entière : pièce, cotes et tableau utile, en 2400 px

```text
ID: ADR-0012
DATE: 2026-09-24
STATUS: ACTIVE
DECISION: (1) Le site sert l'image de fiche ENTIÈRE, pièce et fiche technique incrustée ; plus aucun recadrage (fin du retrait du tableau décidé le 22/09, `recadrer_visuels.py`, puis fait par l'intégration le 23/09). (2) Le tableau ne garde que l'utile : les dimensions de la section (ailes, côtés, diamètre, épaisseurs), le poids, les longueurs standard du site, et le procédé, la nuance ou la finition quand le site officiel les donne. Pas les valeurs d'ingénieur des tableaux fournisseurs (section, surfaces, inerties, modules, rayons de giration, norme). (3) Les barres, profilés et tubes refaits le 24/09 (24 familles de l'ADR-0011, 223 fiches et leurs photos studio) sont rendus en 2400 × 1800 ; l'habillage garde la mise en page validée en 1600 px, agrandie 1,5 fois ; WebP qualité 90. (4) Les autres familles (poutrelles, fer T, tôles, treillis, clôtures, caillebotis, bardage) ne sont pas rendues à nouveau : leur image d'origine entière (1600 × 1200) est remise en ligne depuis l'historique, identique au rendu servi (écart moyen ≤ 1,7 niveau, compression). (5) Poids : quand le poids du site diffère de plus de 3 % du tableau fournisseur ou du poids théorique (50 fiches), il n'est pas écrit sur l'image ; question en attente.
REASON: Propriétaire, 24/09, devant l'image servie (recadrée) : « celle avec les mesures, je veux une photo entière, pas juste la moitié, et je veux que ce soit bien détaillé » ; choix B (image complète) sur trois maquettes ; « bien détaillé » = plus d'infos et plus net ; « mets les infos […] les ailes, les épaisseurs, le poids, tout ce qui serait utile ; le but, c'est pas de mettre trop d'infos non plus » ; 2400 px ; « les 24 familles » ; pour les poids contradictoires : « rien ». « Il faut, à chaque fois, que les mesures soient exactes. »
IMPACT: `scripts/rendu-3d/habiller.py` (échelle de référence 1600, ligne Longueurs, `texte_longueurs`, WebP 90), `controler_rendus.py` (tailles 1600 ou 2400, seuils en pixels à l'échelle, longueurs comparées aux données et à la page), `preparer_rendus.py` (2400 px pour les barres, `studio-famille`), `integrer_visuels.py` (plus de recadrage, textes alternatifs), `donnees_produits.py` (`longueurs_standard`, `--longueurs-seules`), `lib/visuels-produits.json` (dimensions des images), `public/images/produits/` (244 images d'origine entières), contrôles K12 et K13 réécrits (`tests/test_catalogue.py`), V14 (compositions des studios versionnées, `donnees/studios.json`). La page produit montre les mêmes informations que l'image (longueurs standard comprises) : `controler_rendus.py` le vérifie.
SUPERSEDES: — (le recadrage du 22/09 n'avait pas d'ADR : commit e2d81ee, leçon L-051)
VALIDATED_BY: Massimo, 2026-09-24, réponses citées ci-dessus (maquettes A/B/C, tableau court, 2400 px, 24 familles, poids).
```

## Rollback

Remettre le recadrage dans `copier()` de `integrer_visuels.py` (fonction `recadrer_sur_place`, commit 31c41a8),
les anciens K12 et K13, relancer `recadrer_visuels.py` sur les images servies ; marquer cet ADR `SUPERSEDED`.
