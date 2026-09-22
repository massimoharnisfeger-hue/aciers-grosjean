# Produits à modéliser, à corriger, à intégrer

Recalculé le 2026-09-22 par `scripts/rendu-3d/auditer_visuels.py` et par la comparaison
catalogue officiel ↔ projet. Aucun compteur repris d'un document antérieur.

## État des visuels

| | Nombre |
|---|---|
| Produits au catalogue du projet | 495 |
| Rendus Blender dans `final/` | 466 |
| Rendus intégrés et servis | 466 |
| Rendus dans `essais/` (jamais utilisés) | 64 |
| Produits sans rendu | 29 |

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
