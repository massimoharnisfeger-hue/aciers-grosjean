# Inventaire des visuels — résumé

Recalculé le 2026-09-23 par `scripts/catalogue/inventaire.py`. Aucun compteur repris
d'un document antérieur. Détail : `inventaire-images.csv` (une ligne par fichier image) et
`matrice-produits.csv` (une ligne par produit du catalogue).

## Produits

| Mesure | Nombre |
|---|---|
| Produits au catalogue | 495 |
| Univers | 6 |
| Catégories portant des produits | 54 |
| Produits avec visuel validé | 466 |
| Produits sans visuel | 29 |
| Catégories sans photo studio | 6 |

## Images

| Mesure | Nombre |
|---|---|
| Fichiers image inventoriés | 4232 |
| Servis par le manifeste (fiches + studios) | 514 |
| Servis mais absents du disque | 0 |
| Orphelins dans `public/images/produits` | 5 |
| Illisibles | 3 |
| PDF publiés (`public/documents`) | 64 |
| Scènes Blender `.blend` | 0 |

### Par emplacement

| Emplacement | Fichiers |
|---|---|
| atelier | 2090 |
| depot | 1621 |
| public | 521 |

### Par type

| Type | Fichiers |
|---|---|
| Blender 3D — original atelier | 1538 |
| photo produit site actuel | 1093 |
| Blender 3D — vue cotée | 466 |
| Blender 3D — vue cotée (copie propriétaire) | 466 |
| Blender 3D — essai | 395 |
| Blender 3D — original atelier (studio) | 159 |
| Blender 3D — photo studio | 53 |
| Blender 3D — photo studio (copie propriétaire) | 53 |
| planche contact | 7 |
| logo | 2 |

### Par statut

| Statut | Fichiers |
|---|---|
| À VÉRIFIER | 2726 |
| VALIDÉ | 982 |
| DOUBLON | 519 |
| ORPHELINE | 5 |

## À signaler

- Photos studio sur le disque que rien ne sert (décision humaine, voir `_DOCS/rendus-3d/IMAGE-RECONCILIATION.md`) :
  - `public:images/produits/jardin-cloture/clotures/panneaux-rigides/studio-panneau-cloture-medium-3d.webp`
  - `public:images/produits/jardin-cloture/clotures/poteaux/studio-poteau-clogriff-64.webp`
  - `public:images/produits/quincaillerie/caillebotis-marches/studio-caillebotis.webp`
  - `public:images/produits/quincaillerie/caillebotis-marches/studio-marche-caillebotis.webp`
  - `public:images/produits/quincaillerie/caillebotis-marches/studio-marche-o2.webp`
- Catégories sans photo studio :
  - `/jardin-cloture/clotures/fixations`
  - `/quincaillerie/outillage`
  - `/quincaillerie/protection-chimie/colles-etancheite`
  - `/quincaillerie/protection-chimie/galvanisation-a-froid`
  - `/quincaillerie/protection-chimie/peintures-primaires`
  - `/quincaillerie/visserie`
