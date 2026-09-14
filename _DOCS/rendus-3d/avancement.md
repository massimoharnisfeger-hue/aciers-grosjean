# Avancement — visuels 3D des fiches produits

Mis à jour le 14/09/2026 vers 17 h (séance https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em).
Règles : `CLAUDE.md` (section Visuels 3D) et `_DOCS/rendus-3d/lecons.md`. Brief : `_DOCS/BRIEF-RENDUS-3D.md`.
Questions : `_DOCS/rendus-3d/questions-en-attente.md` (on ne s'arrête pas : valeur non affichée, question notée).

## Où on en est (14/09, 18 h 15)
- **Mode automatique (CLAUDE.md).** Décisions du propriétaire du 14/09 appliquées (carnet de leçons).
- **Poutrelles** : 45 visuels + 4 studios rendus, habillés, `controler_rendus.py` = 0 écart ; **vérification indépendante en cours**. Ensuite : `integrer_visuels.py --verdict CONFORME poutrelle-ipe poutrelle-hea poutrelle-heb poutrelle-upn`, build, commit.
- **Cornières** : série en cours (`serie-cornieres.json`, 15 + 2 studio).
- **Fers T, plats, larges plats, ronds, carrés, tubes** : tests conformes ; série `serie-profils-tubes.json` (129 + 8 studio) en file derrière les cornières (~7 h).
- **Tôles laminées à chaud et quarto** : test conforme (plaque + loupe d'épaisseur) ; série `serie-toles.json` (37 + 2 studio) en file derrière les profils et tubes.
- Reste pour finir la vague 1 : armatures (ronds à béton crénelés, treillis soudés) — données et géométrie à faire.

## Étapes communes
- [x] 0. Générateur corrigé : profils U alu, tôles alu et inox sans oxycoupage ; nuances et longueurs des poutrelles ; nom du Clogriff 2M50 gris.
- [x] 1. Références visuelles du site actuel : `references.csv`, `references-groupes.csv`, `references-recap.md`.
- [ ] 2. Données sourcées (`donnees_produits.py`) : poutrelles, cornières, fers T, plats, pleins, tubes faits (189 fiches) ; tôles et armatures à faire.

## Familles (vague 1)
| Famille | Fiches | Données | Test | Série | Contrôle | Vérif. | Site |
|---|---|---|---|---|---|---|---|
| Poutrelles IPE, HEA, HEB, UPN | 45 | fait | fait | fait | 0 écart | en cours | — |
| Cornières égales, inégales | 15 | fait | fait | en cours | — | — | — |
| Fers T | 5 | fait | fait | en file | — | — | — |
| Plats, larges plats | 40 | fait | fait | en file | — | — | — |
| Ronds lisses, carrés pleins | 16 | fait | fait | en file | — | — | — |
| Tubes carrés, rectangulaires, ronds | 68 | fait | fait | en file | — | — | — |
| Tôles laminées à chaud (+ quarto) | 37 | fait | fait | en file | — | — | — |
| Armatures : ronds à béton, treillis | 28 | — | — | — | — | — | — |

| Autres vagues | Fiches | État |
|---|---|---|
| Vague 2 : tôles à froid, galvanisées, corten, larmées, perforées ; alu ; inox | 145 | — |
| Vague 3 : clôtures, bordures, caillebotis, tôles profilées, panneaux isolés, tasseaux | 73 | — |
| Visserie | 6 | — |

## Reprendre le rendu
Atelier hors OneDrive : `%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d\` — `final\` (production), `essais\`, `controle\` (planches), journaux `serie-*.log`.
1. `python scripts/rendu-3d/donnees_produits.py [famille…]` (données sourcées ; familles : poutrelles, cornieres, fers-t, plats, pleins, tubes, toles)
2. `python scripts/rendu-3d/preparer_rendus.py <params.json> car <slug…>` puis `--ajouter <params.json> studio studio-<famille> <3 slugs>` (`--essai 1600` pour un test)
3. `blender -b --factory-startup -t 4 -P scripts/rendu-3d/rendu_profil.py -- <params.json>` en arrière-plan
4. `python scripts/rendu-3d/habiller.py <slug>` et `--studio studio-<famille>` (`--essai` pour les tests)
5. `python scripts/rendu-3d/controler_rendus.py <famille…>` → planches dans `controle\`
6. Vérificateur indépendant (`.claude/agents/verificateur-rendus.md`), puis `python scripts/rendu-3d/integrer_visuels.py --verdict CONFORME <famille…>`

Durée mesurée (1600 × 1200, 32 échantillons, `-t 4`, PC utilisé en parallèle) : 2 min 50 à 3 min 30 par image.
