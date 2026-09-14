# Avancement — visuels 3D des fiches produits

Mis à jour le 14/09/2026 (séance https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em).
Règles : `CLAUDE.md` (section Visuels 3D) et `_DOCS/rendus-3d/lecons.md`. Brief : `_DOCS/BRIEF-RENDUS-3D.md`.

## Où on en est
- **Poutrelles : en attente du propriétaire.** Rendu test envoyé le 14/09 ; il a demandé à le voir avant d'aller plus loin. Questions 1 à 4 ci-dessous. Le rendu en série peut précéder les réponses (l'habillage se refait en quelques secondes), l'intégration non.
- Famille suivante non bloquée, dans l'ordre du brief : cornières (vague 1).
- Questions 5 et 6 : bloquent seulement les poteaux de clôture (vague 3).

## Étapes communes
- [x] 0. Générateur corrigé : profils U alu (épaisseur 2 mm, poids recalculé), tôles alu et inox sans oxycoupage.
- [x] 1. Références visuelles du site actuel : `references.csv`, `references-groupes.csv`, `references-recap.md`.
- [ ] 2. Données sourcées : poutrelles faites (`scripts/rendu-3d/donnees/produits.json`, 45 fiches, 0 alerte) ; autres familles à ajouter dans `donnees_produits.py`.

## Familles
| Famille | Fiches | Données | Test | Validation | Série | Contrôle | Site |
|---|---|---|---|---|---|---|---|
| Poutrelles IPE, HEA, HEB, UPN | 45 | fait | fait | en attente | — | — | — |
| Cornières, fers T, plats, ronds, carrés, tubes, tôles laminées à chaud, armatures (fin de vague 1) | 208 | — | — | — | — | — | — |
| Vague 2 : tôles à froid, galvanisées, corten, larmées, perforées ; alu ; inox | 145 | — | — | — | — | — | — |
| Vague 3 : clôtures, bordures, caillebotis, tôles profilées, panneaux isolés, tasseaux | 73 | — | — | — | — | — | — |
| Visserie | 6 | — | — | — | — | — | — |

## Questions ouvertes (bloquantes)
1. Photo studio : une barre ou trois tailles côte à côte ? (Variante trois tailles : écarter davantage les barres, elles se masquent un peu.)
2. Fiches poutrelles : le générateur affiche « Nuance S235JR — EN 10025-2 » et « Longueur standard 6 m ou 12 m » sur les 45 fiches ; le site actuel dit S275 (IPE), S275/S355 (HEB), S235 ou S275 (UPN), rien (HEA), longueurs proposées 1 à 6 m, « jusqu'à 15 m suivant la section », et « 3 à 12 mètres » dans le texte UPN.
3. Site actuel, « norme 10025 » : afficher « EN 10025 » ?
4. UPN : la description donne le poids du tableau fournisseur (25,76 kg/m pour l'UPN 200), la fiche un poids plus élevé de 0,1 à 0,8 % (25,91). Les deux apparaissent sur la même page.
5. Poteau « CLOGRIFF 64 – 2M50 – VERT RAL 7016 » : vert RAL 6005 ou gris RAL 7016 ?
6. Poteaux Cloplus 40 : l'image du fabricant porte « (ALU) » : aluminium ou acier ?

## Reprendre le rendu
Dossier de travail hors OneDrive : `%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d\` (paramètres `test-poutrelles.json`, journal `test-poutrelles.log`, images `final\`).
1. `python scripts/rendu-3d/donnees_produits.py` (données sourcées)
2. `python scripts/rendu-3d/preparer_rendus.py <params.json> car <slug...>` puis `--ajouter <params.json> studio <nom> <slug...>`
3. `blender -b --factory-startup -P scripts/rendu-3d/rendu_profil.py -- <params.json>` (en arrière-plan ; `-t 4` si le PC sert en journée)
4. `python scripts/rendu-3d/habiller.py <slug>` et `python scripts/rendu-3d/habiller.py --studio <nom>`

Durée mesurée (1600 × 1200, 32 échantillons) : 1 min 50 à 2 min 50 par image. Série poutrelles (45 visuels + 4 studio) : environ 2 h.
