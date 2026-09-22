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

## BLOCAGE — Catalogue gelé

**`lib/catalogue.ts` ne peut plus être régénéré.** Son générateur
(`scripts/generer-catalogue.py`) attendait son relevé d'URLs à
`/root/.claude/uploads/…`, un chemin de session web Linux. Ce fichier n'existe ni sur
cette machine, ni dans le dépôt, ni dans `_DEPOT` (cherché le 22/09).

Conséquence directe : `CLAUDE.md` interdit de modifier `lib/catalogue.ts` à la main
(« généré, toute modification doit être reportée dans le générateur »), et le générateur
ne peut pas tourner. **Aucun produit ne peut donc être ajouté, renommé ou reclassé** —
y compris la Vasque Corten ci-dessous.

Ce qui manque précisément : un CSV avec les colonnes
`Page ; Parent ; Title ; Type ; URL_cible_recommandee`. La colonne décisive est
`URL_cible_recommandee` : elle associe chaque catégorie du site officiel au chemin
correspondant du nouveau site. C'est un arbitrage éditorial, pas une donnée déductible —
les CSV survivants (`produits.csv`, `categories.csv`) portent l'arborescence **officielle**,
jamais celle du nouveau site.

Trois issues possibles, par ordre de sûreté :

1. **Retrouver le fichier original.** Il a été téléversé dans une session web
   (`AG_annexe_inventaire_URLs.csv`). S'il existe encore sur le PC ou dans les
   téléchargements, le déposer à `_DOCS/catalogue-site-actuel/inventaire-urls.csv` :
   le générateur repart immédiatement.
2. **Le reconstruire** en croisant `produits.csv` (catégorie officielle) avec le
   `categorie` de chaque produit dans `lib/catalogue.ts` (chemin du nouveau site).
   Vérifiable : régénérer doit redonner un `catalogue.ts` identique. Non tenté le 22/09 —
   se tromper corromprait silencieusement le catalogue d'un site commercial.
3. **Assumer que le catalogue est figé** et lever la règle de `CLAUDE.md`, ce qui
   autorise les corrections à la main. À éviter : la prochaine régénération, si le
   fichier réapparaît, écraserait toutes les corrections manuelles.

Garde : `tests/test_produit.py::CatalogueRegenerable::test_d12_l_entree_du_generateur_est_dans_le_depot`
refuse désormais qu'une entrée du générateur pointe hors du dépôt. Le générateur, lui,
explique ce qui manque au lieu d'échouer sur un chemin Linux.

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
