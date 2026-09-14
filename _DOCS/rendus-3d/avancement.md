# Avancement — visuels 3D des fiches produits

Mis à jour le 14/09/2026 vers 17 h (séance https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em).
Règles : `CLAUDE.md` (section Visuels 3D) et `_DOCS/rendus-3d/lecons.md`. Brief : `_DOCS/BRIEF-RENDUS-3D.md`.
Questions : `_DOCS/rendus-3d/questions-en-attente.md` (on ne s'arrête pas : valeur non affichée, question notée).

## Où on en est (14/09, soir)
- **Mode automatique (CLAUDE.md).** Décisions du propriétaire du 14/09 appliquées (carnet de leçons).
- **Poutrelles : TERMINÉES** — 45 visuels + 4 studios, CONFORME, intégrées (`public/images/produits/acier/poutrelles/`).
- **Cornières : TERMINÉES** — 15 visuels + 2 studios, CONFORME (rappels décollés corrigés par recalcul des points), intégrées (`public/images/produits/acier/profiles/`). Défaut mineur non corrigé, sans effet visible : chanfrein à peine visible sur la face coupée des 40x40x3 et 50x50x3.
- **Fers T, plats, larges plats, ronds, carrés, tubes** : série `serie-profils-tubes.json` (129 + 8 studio) en cours dans Blender (~15 images faites à 19 h ; ~3 min 30 par image).
- **Tôles laminées à chaud et quarto** : série `serie-toles.json` (37 + 2) en file derrière (surveillance en arrière-plan).
- **Armatures** : série `serie-armatures.json` (28 + 4) en file derrière les tôles. Avant intégration : retirer des pages les nuances B500B / B500A non sourcées (questions 10 et 11).
- **Vague 2** : données faites pour les tôles planes (froid, galva, Corten, alu, inox), profilés/tubes alu et inox (77), tôles larmées et striées (15), tôles perforées (8) ; pages inox corrigées (nuance sourcée) ; « Masse surfacique » contredite retirée de 36 pages (`integrer.py`). Essais conformes : matières, profilés alu/inox, tôles à relief (loupe e / E). Série `serie-vague2.json` (121 + 18 studios) en file derrière les armatures. Essai perforées en cours ; ensuite série `serie-vague2b.json` (relief + perforées).

## Étapes communes
- [x] 0. Générateur corrigé : profils U alu, tôles alu et inox sans oxycoupage ; nuances et longueurs des poutrelles ; nom du Clogriff 2M50 gris.
- [x] 1. Références visuelles du site actuel : `references.csv`, `references-groupes.csv`, `references-recap.md`.
- [ ] 2. Données sourcées (`donnees_produits.py`) : poutrelles, cornières, fers T, plats, pleins, tubes faits (189 fiches) ; tôles et armatures à faire.

## Familles (vague 1)
| Famille | Fiches | Données | Test | Série | Contrôle | Vérif. | Site |
|---|---|---|---|---|---|---|---|
| Poutrelles IPE, HEA, HEB, UPN | 45 | fait | fait | fait | 0 écart | CONFORME | intégré |
| Cornières égales, inégales | 15 | fait | fait | fait | 0 écart | CONFORME | intégré |
| Fers T | 5 | fait | fait | en cours | — | — | — |
| Plats, larges plats | 40 | fait | fait | en cours | — | — | — |
| Ronds lisses, carrés pleins | 16 | fait | fait | en cours | — | — | — |
| Tubes carrés, rectangulaires, ronds | 68 | fait | fait | en cours | — | — | — |
| Tôles laminées à chaud (+ quarto) | 37 | fait | fait | en file | — | — | — |
| Armatures : ronds à béton, treillis | 28 | fait | fait | en file | — | — | — |

| Autres vagues | Fiches | État |
|---|---|---|
| Vague 2 : tôles à froid, galvanisées, corten, alu, inox (planes) | 44 | données faites, essai matières corrigé |
| Vague 2 : profilés et tubes alu (44) et inox (33) | 77 | données faites, essai en cours |
| Vague 2 : tôles larmées (6), striées alu (9), perforées (8) | 23 | références et motifs relevés, géométrie à faire |
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
