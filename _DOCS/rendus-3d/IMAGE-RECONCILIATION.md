# Réconciliation des visuels produit

Recalculé le 2026-09-22 par `scripts/rendu-3d/auditer_visuels.py`. Aucun compteur repris d'un document antérieur.

## État réel

| Mesure | Nombre |
|---|---|
| Produits au catalogue | 495 |
| Rendus Blender dans `final/` | 466 |
| Rendus dans `essais/` (jamais utilisés) | 64 |
| Entrées du manifeste | 466 |

## Statuts

| Statut | Produits |
|---|---|
| CORRECT | 466 |
| NO_RENDER | 29 |

## Contrôles transverses

- Rendus sans produit au catalogue : **0**
- Entrées de manifeste sans produit : **0**
- Images sur disque que rien ne sert : **5**
- Images servies mais absentes du disque : **0**
- Fichiers servis à plusieurs produits : **0**
- Catégories à plusieurs photos studio : **3**

### Photos studio en concurrence (decision humaine)

Le manifeste ne tient qu'une photo studio par categorie. Les rendus ci-dessous existent, sont valides, et ne sont servis nulle part : lequel doit representer la categorie ne se deduit pas des donnees.

| Categorie | Servie | Ignoree(s) |
|---|---|---|
| `/jardin-cloture/clotures/panneaux-rigides` | `studio-panneau-cloture-plis-205.webp` | `studio-panneau-cloture-medium-3d.webp` |
| `/jardin-cloture/clotures/poteaux` | `studio-poteau-cloplus-40.webp` | `studio-poteau-clogriff-64.webp` |
| `/quincaillerie/caillebotis-marches` | `studio-plancher-o2.webp` | `studio-caillebotis.webp`, `studio-marche-caillebotis.webp`, `studio-marche-o2.webp` |

## À valider par un humain

Aucun cas.

Détail complet : `IMAGE-MASTER-INVENTORY.csv`.
