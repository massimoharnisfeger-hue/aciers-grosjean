# Avancement — visuels 3D des fiches produits

Mis à jour le 14/09/2026 vers 17 h (séance https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em).
Règles : `CLAUDE.md` (section Visuels 3D) et `_DOCS/rendus-3d/lecons.md`. Brief : `_DOCS/BRIEF-RENDUS-3D.md`.
Questions : `_DOCS/rendus-3d/questions-en-attente.md` (on ne s'arrête pas : valeur non affichée, question notée).

## Où on en est
- **Mode automatique (CLAUDE.md).** Décisions du propriétaire du 14/09 appliquées (carnet de leçons).
- **Poutrelles** : série en cours dans Blender (`serie-poutrelles.json`, 45 visuels) ; les 4 photos studio « trois tailles » (`serie-poutrelles-studio.json`) partent automatiquement ensuite. Puis : `habiller.py` sur tout, `controler_rendus.py poutrelle-ipe poutrelle-hea poutrelle-heb poutrelle-upn`, vérificateur indépendant, `integrer_visuels.py --verdict CONFORME …`, build, commit.
- **Cornières** : test conforme (pince d'épaisseur remontée à 70 % après défaut). Série `serie-cornieres.json` (15 + 2 studio) en file d'attente derrière les poutrelles.
- **Fers T, plats, larges plats, ronds, carrés, tubes** : données sourcées faites ; sections ajoutées au rendu ; essai en cours (`essais/essai-sections.json`).
- Ensuite : tôles laminées à chaud, armatures (ronds à béton, treillis) → fin de la vague 1.

## Étapes communes
- [x] 0. Générateur corrigé : profils U alu, tôles alu et inox sans oxycoupage ; nuances et longueurs des poutrelles ; nom du Clogriff 2M50 gris.
- [x] 1. Références visuelles du site actuel : `references.csv`, `references-groupes.csv`, `references-recap.md`.
- [ ] 2. Données sourcées (`donnees_produits.py`) : poutrelles, cornières, fers T, plats, pleins, tubes faits (189 fiches) ; tôles et armatures à faire.

## Familles (vague 1)
| Famille | Fiches | Données | Test | Série | Contrôle | Vérif. | Site |
|---|---|---|---|---|---|---|---|
| Poutrelles IPE, HEA, HEB, UPN | 45 | fait | fait | en cours | — | — | — |
| Cornières égales, inégales | 15 | fait | fait | en attente | — | — | — |
| Fers T | 5 | fait | en cours | — | — | — | — |
| Plats, larges plats | 40 | fait | en cours | — | — | — | — |
| Ronds lisses, carrés pleins | 16 | fait | en cours | — | — | — | — |
| Tubes carrés, rectangulaires, ronds | 68 | fait | en cours | — | — | — | — |
| Tôles laminées à chaud (+ quarto) | 37 | — | — | — | — | — | — |
| Armatures : ronds à béton, treillis | 28 | — | — | — | — | — | — |

| Autres vagues | Fiches | État |
|---|---|---|
| Vague 2 : tôles à froid, galvanisées, corten, larmées, perforées ; alu ; inox | 145 | — |
| Vague 3 : clôtures, bordures, caillebotis, tôles profilées, panneaux isolés, tasseaux | 73 | — |
| Visserie | 6 | — |

## Reprendre le rendu
Atelier hors OneDrive : `%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d\` — `final\` (production), `essais\`, `controle\` (planches), journaux `serie-*.log`.
1. `python scripts/rendu-3d/donnees_produits.py [famille…]` (données sourcées ; familles : poutrelles, cornieres, fers-t, plats, pleins, tubes)
2. `python scripts/rendu-3d/preparer_rendus.py <params.json> car <slug…>` puis `--ajouter <params.json> studio studio-<famille> <3 slugs>` (`--essai 1600` pour un test)
3. `blender -b --factory-startup -t 4 -P scripts/rendu-3d/rendu_profil.py -- <params.json>` en arrière-plan
4. `python scripts/rendu-3d/habiller.py <slug>` et `--studio studio-<famille>` (`--essai` pour les tests)
5. `python scripts/rendu-3d/controler_rendus.py <famille…>` → planches dans `controle\`
6. Vérificateur indépendant (`.claude/agents/verificateur-rendus.md`), puis `python scripts/rendu-3d/integrer_visuels.py --verdict CONFORME <famille…>`

Durée mesurée (1600 × 1200, 32 échantillons, `-t 4`, PC utilisé en parallèle) : 2 min 50 à 3 min 30 par image.
