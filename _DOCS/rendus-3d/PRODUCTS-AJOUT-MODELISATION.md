# Produits à modéliser, à corriger, à intégrer

Recalculé le 2026-09-22 par `scripts/rendu-3d/auditer_visuels.py` et par la comparaison
catalogue officiel ↔ projet. Aucun compteur repris d'un document antérieur.

## État des visuels

Compteurs remesurés le 22/09 à 11 h. Chaque libellé dit **exactement** ce qui est
compté : les précédents disaient « rendus dans `final/` » pour un sous-ensemble des
fichiers, et le dossier en contient près de quatre fois plus.

| | Nombre | Compté comment |
|---|---|---|
| Produits au catalogue du projet | 495 | clés `slug` avec `categorie` dans `lib/catalogue.ts` |
| Fiches produit servies (`*-caracteristiques.webp`) | 466 | fichiers sous `public/images/` |
| Produits sans rendu | 29 | 495 − 466 |
| Photos studio servies | 53 | `studio-*.webp` sous `public/images/` |
| Catégories pourvues au manifeste | 48 | clés de `lib/visuels-produits.json` |
| — | — | — |
| Fichiers dans l'atelier `final/` | 1 697 | dont 1 178 PNG bruts, 985 JSON, 519 WebP |
| Dont fiches produit livrables | 466 | les 466 servis y sont tous présents |
| Dont photos studio livrables | 53 | nommées `studio-<famille>-studio.webp` |
| Fichiers dans l'atelier `essais/` | 648 | dont 86 WebP |
| Dont fiches produit d'essai | 64 | **toutes** visent un produit déjà pourvu |
| Dont photos studio d'essai | 19 + 3 | 3 nommées `essai-studio-*` |

**`essais/` ne comble aucun manque** — vérifié le 22/09 : les 64 fiches d'essai visent
toutes un produit qui a déjà son rendu servi, et aucune ne vise un des 29 produits
sans rendu. La règle « ne jamais intégrer automatiquement depuis `essais/` » ne coûte
donc rien : il n'y a rien à y récupérer.

## Rendus existants non intégrés

Aucun. Les 11 qui restaient (10 caillebotis, 1 rond à béton crénelé 6 mm) ont été intégrés
le 22/09 après vérification du titre et de la taille de chaque fichier.

## Produits sans visuel — à modéliser ou à photographier

29 produits, tous des consommables sans géométrie cotée. Un rendu 3D dimensionnel n'a pas
de sens pour un tube de mastic : ils affichent l'illustration SVG de leur famille, ce qui
est le comportement voulu. La question ouverte est plutôt **une photo produit**, pas un rendu.

| Catégorie | Produits | Nature |
|---|---|---|
| `/quincaillerie/protection-chimie/galvanisation-a-froid` | 7 | aérosols et pots |
| `/quincaillerie/protection-chimie/peintures-primaires` | 6 | pots de peinture |
| `/quincaillerie/visserie` | 6 | vis, boulons |
| `/jardin-cloture/clotures/fixations` | 5 | brides, colliers |
| `/quincaillerie/protection-chimie/colles-etancheite` | 4 | cartouches |
| `/quincaillerie/outillage` | 1 | outillage |

Liste nominative : `PRODUCTS-REQUIRING-BLENDER-RENDER.md`.

## Produits à corriger — décision humaine

Trois catégories possèdent plusieurs photos studio valides ; le manifeste n'en tient qu'une.
Laquelle doit représenter la catégorie est un arbitrage visuel, pas une déduction.

| Catégorie | Servie | Non servies |
|---|---|---|
| `/quincaillerie/caillebotis-marches` | `studio-plancher-o2.webp` | `studio-caillebotis.webp`, `studio-marche-caillebotis.webp`, `studio-marche-o2.webp` |
| `/jardin-cloture/clotures/panneaux-rigides` | `studio-panneau-cloture-plis-205.webp` | `studio-panneau-cloture-medium-3d.webp` |
| `/jardin-cloture/clotures/poteaux` | `studio-poteau-cloplus-40.webp` | `studio-poteau-clogriff-64.webp` |

## Catalogue régénérable — blocage levé le 22/09

Le relevé d'URLs manquant a été retrouvé dans les téléchargements
(`AG_annexe_inventaire_URLs.csv`, 665 lignes) et déposé à
`_DOCS/catalogue-site-actuel/inventaire-urls.csv`. Aucune donnée sensible (scan de secrets
du dépôt : PASS). **`python scripts/generer-catalogue.py` tourne à nouveau sans argument.**

Vérification faite avant de conclure : régénérer donne un `catalogue.ts` qui ne diffère de la
version commitée que sur **quatre littéraux `prix`** (les profils U aluminium, mis à 5,00 €).
Ce n'est pas une corruption : le bas de `catalogue.ts` fusionne `lib/site-actuel.json` et
**écrase `prix`, `prixTtc`, `kg`, `unite`, `longueurs`, `finition`, `pdfs` et `specs`** pour
les 495 produits — aucun n'échappe à la fusion. Le prix affiché vient donc toujours du relevé
du site officiel, jamais du générateur. Contrôlé au navigateur sur
`/p/profil-en-u-40x40x40x2mm-en-aluminium` : la page sert 5,39 € HTVA / 6,52 € TTC, les valeurs
officielles, et non le 26,80 € inscrit dans le fichier généré.

À retenir pour une prochaine régénération : un diff sur ces quatre lignes est attendu et sans
effet. Le `prix` écrit par le générateur est une valeur morte — elle gagnerait à disparaître,
mais la retirer touche au contrat du type `Produit` et n'a pas été tenté ici.

## Produits à ajouter au catalogue — décision humaine

Deux produits existent sur le site officiel et sont absents du projet. Ils en sont absents
parce que le site officiel ne les range dans aucune catégorie (fil d'Ariane « Accueil > nom »),
et que le générateur écarte les orphelins. Vérifié en direct le 22/09.

| Produit | Prix officiel | État de la fiche officielle | Décision attendue |
|---|---|---|---|
| **Vasque Corten** | 580,80 € TTC | Complète : acier Corten, 1000 × 850 mm, rangement à bois sous le plan, cuisson par rayonnement | Sous quelle catégorie l'intégrer ? Aucune catégorie « brasero / aménagement extérieur » n'existe aujourd'hui |
| **Vasque 2** | 605,00 € TTC | **Incomplète côté officiel** : aucune description, aucune dimension, aucune matière, image de remplacement | À compléter sur le site officiel d'abord — rien à reprendre sans inventer |

Ce ne sont pas des oublis du projet : ce sont des produits mal rangés sur le site officiel.
Les corriger là-bas (leur donner une catégorie) les ferait entrer automatiquement.

## Produits écartés à juste titre

| Produit officiel | Pourquoi il n'est pas au catalogue |
|---|---|
| `COUPE TR SUP`, `COUPE PLAT 220 à 300`, `COUPE PLAT 350 à 400` | Suppléments de découpe, pas des produits. Orphelins sur le site officiel, URL `coupe-ipe-140-à-220-N` |
| `Tube acier rond diam 42,4X2,5 mm` | Page orpheline en double : le produit existe déjà sous `Tube rond 42,4x2,5mm en acier brut série légère` |

## Correction de nom assumée

`POTEAU DE CLÔTURE CLOGRIFF 64 – 2M50` : le site officiel le nomme **« VERT RAL 7016 »**.
Le RAL 7016 est un gris anthracite, et le vert de cette série est le RAL 6005. La page
officielle **se contredit elle-même** — titre « VERT RAL 7016 », en-tête « GRIS RAL 7016 »
(vérifié en direct le 22/09). Le projet retient « GRIS RAL 7016 », correction tracée dans
`scripts/generer-catalogue.py` (`NOMS_CORRIGES`).

**À corriger sur le site officiel** : un client qui cherche un poteau gris ne le trouve pas,
et un client qui commande « vert » reçoit du gris.

## HUMAN_REVIEW — où vivent les spécifications et les documents (22/09)

La section « Le produit en détail » est passée en onglets. Le propriétaire demande que
**chaque fiche garde la même structure, avec les mêmes informations qui reviennent**.

Mesuré sur les 495 fiches : spécifications **472 (95 %)**, PDF **359 (72 %)**, cotes **355**,
introduction **340 (68 %)**, longueurs **273**. Les seules données quasi universelles sont donc
les spécifications et les documents — or ils sont déjà affichés dans la colonne de droite de la
fiche, sous le calculateur.

| Option | Conséquence |
|---|---|
| **Les déplacer dans les onglets** | 95 % des fiches auraient les mêmes rubriques. La colonne de droite se limite au prix, au calculateur et aux boutons. Touche une autre partie de la fiche. |
| **Les laisser à droite** | Rien d'autre ne bouge, mais 36 fiches n'ont aucun onglet et 124 n'en ont qu'un : la structure reste variable. |
| **Les deux** | Structure uniforme, mais la même information affichée deux fois sur la page. Déconseillé. |

**Décision attendue du propriétaire.** Aucune des trois n'est déductible : c'est un arbitrage
entre uniformité et non-duplication, pas un fait à établir.
