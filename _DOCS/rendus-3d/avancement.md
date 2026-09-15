# Avancement — visuels 3D des fiches produits

Mis à jour le 14/09/2026 vers 17 h (séance https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em).
Règles : `CLAUDE.md` (section Visuels 3D) et `_DOCS/rendus-3d/lecons.md`. Brief : `_DOCS/BRIEF-RENDUS-3D.md`.
Questions : `_DOCS/rendus-3d/questions-en-attente.md` (on ne s'arrête pas : valeur non affichée, question notée).

## Où on en est (14/09, soir)
- **Mode automatique (CLAUDE.md).** Décisions du propriétaire du 14/09 appliquées (carnet de leçons).
- **15/09, 11 h 20 — vague 2 vérifiée** (3 vérifications indépendantes) : **CONFORMES et intégrées** (14 familles, 96 visuels + 14 studios) : les 7 familles alu profilés/tubes, tôles galvanisées, Corten, aluminium, inox cornières, plats, ronds pleins, tubes ronds (`lib/visuels-produits.json` : 345 fiches). Build et push à faire. **À CORRIGER** : inox tubes carrés et rectangulaires (dessus noir, reflet du studio), tôles inox brossées (brossage invisible, miroir), tôles à froid (photo studio miroir noir). Matières corrigées dans `rendu_profil.py` (inox base 0,62, rugosité 0,46, `brossage` 600 stries, étirement 0,0015, contraste 0,2, relief 0,06 ; froid base 0,36, rugosité 0,50) et photo studio des tôles en métal lisse à 46° d'élévation (`preparer_rendus.py`) ; essais à 11 h 35 : dessus du tube inox 177/255 et 0 % sombre (avant 148 et 22 %), écart studio/visuel −15 inox, −19 froid, −33 galva à 42° (avant −68, −64, −60). **61 reprises ajoutées en fin de `serie-vague3.json`** (146 rendus) : d'abord inox tubes carrés (6+1), rectangulaire (1+1), tôles inox (10+1), tôles à froid (8+1), plats inox (10+1), studios tôles galvanisées et aluminium ; puis, pour la cohérence de l'inox, cornières (5+1), ronds pleins (3+1), tubes ronds (8+1). Liste : `rendu3d\reprise-matieres.json`. Suivi : `post_series2.ps1` (habille ces familles avec la vague 3). Après la série : contrôles, vérification indépendante de ces familles, réintégration. Contrôles de matière ajoutés et calibrés (`luminance_piece`). Mineurs notés, non faits : pastille t sur la paroi des tubes rectangulaires alu étroits (60x30x3 : 52 px), titres « en Aluminium » / « Profil en U en 30x30x30x2mm Aluminium » hérités du site, relief de face sciée trop marqué (plats et petits tubes), loupe des tôles de 0,8–1,5 mm (pointes presque jointives, plancher de champ à baisser), texture Corten étirée dans la loupe, titre des tôles à froid identique à celui des tôles à chaud, photos studio galva (−60) et alu (−35) plus sombres que leurs visuels (le nouveau contrôle les signale), 54 fiches dont le poids de la page n'est pas sur l'image (règle des 3 %). Question 34 (poids du tube rond inox 76,1x2).
- **15/09, 10 h 20** : les 12 familles CONFORMES (189 fiches + 12 studios : fers T, plats, larges plats, ronds, carrés, tubes carrés, rectangulaires, ronds, tôles à chaud, quarto, ronds à béton à chaud, treillis soudés) sont **intégrées** (`integrer_visuels.py`, `lib/visuels-produits.json` : 249 fiches) ; build et push à faire dès que la mémoire le permet (`verifier-leger.ps1` du scratchpad : build à 1 worker et tas Node limité, pour tourner pendant Blender). Questions 31 à 33 notées (motif du laminé à froid, longueur des dépassants, 5 poids fournisseur > 3 % du théorique). **Dépassants modélisés** (`fils_treillis` : fils prolongés d'une maille au fond et à droite, cadre et écart studio élargis d'autant, clé `depassants` passée par `preparer_rendus.py`) ; essai en cours, puis les 4 visuels + studio sont ajoutés en fin de `serie-vague3.json` (la chaîne découpe la série au moment de la lancer). Étiquette « Maille a × b » sur la fiche des treillis ; famille treillis-soude rhabillée et réintégrée. Vague 2 rendue à 10 h 17 (139/139), habillage automatique en cours ; vague 2b lancée.
- **Poutrelles : TERMINÉES** — 45 visuels + 4 studios, CONFORME, intégrées (`public/images/produits/acier/poutrelles/`).
- **Cornières : TERMINÉES** — 15 visuels + 2 studios, CONFORME (rappels décollés corrigés par recalcul des points), intégrées (`public/images/produits/acier/profiles/`). Défaut mineur non corrigé, sans effet visible : chanfrein à peine visible sur la face coupée des 40x40x3 et 50x50x3.
- **Fers T, plats, larges plats, ronds, carrés, tubes** : série `serie-profils-tubes.json` (129 + 8 studio) en cours dans Blender (~15 images faites à 19 h ; ~3 min 30 par image).
- **Tôles laminées à chaud et quarto** : série `serie-toles.json` (37 + 2) en file derrière (surveillance en arrière-plan).
- **Armatures** : série `serie-armatures.json` (28 + 4) en file derrière les tôles. Avant intégration : retirer des pages les nuances B500B / B500A non sourcées (questions 10 et 11).
- **File Blender (une seule instance à la fois, `-t 4`)** : profils et tubes (137 ; arrêtée à 61 le 15/09 à 0 h 54 par un manque de mémoire, relancée sur les 76 manquants) → tôles (39) → armatures (32) → vague 2 (139) → vague 2b relief et perforées (26) → vague 3 (80 : 68 visuels + 12 studios). Chaîne détachée de la séance (`chaine.ps1` du scratchpad, Blender lancé par `Start-Process`) ; fin écrite dans `rendu3d\chaine-terminee.txt`. Environ 3 min 30 par image : la file dure jusqu'au 16/09. **Pas de build Node pendant les rendus** (mémoire).
- **15/09, 8 h** : vérification indépendante tôles et armatures → CONFORMES : tole-laminee-a-chaud, tole-quarto, rond-a-beton-lamine-a-chaud, treillis-soude. **À CORRIGER** : treillis-soude-depassants (bloquant : dépassants non modélisés, la clé `depassants` n'est pas lue par la géométrie → 4 rendus + studio à refaire, sans cote) ; rond-a-beton-lamine-a-froid (motif de nervures du laminé à froid non sourcé → question en attente). Mineurs à faire au prochain passage : liaison de loupe à ~12 px du rappel de l (37 tôles), lettre « l » en Poppins lue « I », « Maille a × b » sans lettres (treillis), nervures transverses des ronds à béton non inclinées et `x_rappel` de ROND-BETON (au prochain rendu). Contrôles proposés : distance liaison/rappels, clé de données ignorée par la géométrie, valeur supposée visible dans le titre, `procede`/`surface` comparés à la page. Rendus : 270 / 453 à 8 h.
- **15/09, 7 h 35** : revérification ciblée → **les 8 familles profils et tubes sont CONFORMES** (129 visuels + 8 studios), prêtes à intégrer. Intégration + build + push en attente d'une fenêtre mémoire (build Node impossible avec 2 Go libres et Blender actif). Vérification indépendante tôles et armatures lancée.
- **15/09, 7 h 15** : vérification indépendante profils et tubes → 7 familles CONFORMES, tube-carre À CORRIGER (tube 250x250x6 : fond visible). Corrigé : tronçon des tubes ≥ 3 × la plus grande cote (250x250x6 et 200x100x5 refaits), rappels hauts des ronds et tubes ronds, nouveaux contrôles (fond enclos, rappel qui entre dans la pièce, empreinte absente). Les 14 familles des 3 séries de la nuit : 0 écart. Revérification ciblée en cours. Mineur non corrigé (demande un nouveau rendu) : relief de la face sciée trop marqué sur les tubes ronds 17,2x2 et 21,3x2. Tôles et armatures : vérification indépendante à lancer. Poids : 5 poids affichés dépassent 3 % du poids théorique mais respectent le tableau fournisseur, qui prime (tubes rect. 100x50x4, 120x60x4, 80x40x2 ; fer T 20x3 ; rond 6) — à signaler au propriétaire.
- **15/09, 5 h 47** : séries profils et tubes (137), tôles (39) et armatures (32) **rendues et habillées** ; vague 2 en cours. Contrôles : seuls écarts, les lignes de rappel (contrôle recalibré, vrai défaut des fers T corrigé à l'habillage) ; rhabillage des 14 familles fait à 6 h 05 (`rhabiller_nuit.ps1`), puis vérification indépendante. RAM libre 2 Go : ni build ni intégration tant que Blender tourne.
- **6 cœurs dès 2 h 07 (15/09)** : à la demande du propriétaire, relais pris tout de suite (Blender à 4 cœurs arrêté après 88 profils, 49 repris à 6 cœurs) ; `threads.txt` = 6 et PC maintenu allumé jusqu'à 13 h (`eveil.ps1`, qui retire `threads.txt` à 13 h).
- **Relais 6 cœurs (15/09, 1 h 20)** : `chaine6.ps1` (scratchpad) attend la fin du Blender des profils et tubes, arrête `chaine.ps1` et rend les séries suivantes par paquets de 12, avec 6 cœurs de 22 h à 8 h et 4 le jour (ou le nombre écrit dans `rendu3d\threads.txt`) ; journal `rendu3d\chaine6.log`. État lisible par le propriétaire, mis à jour toutes les 5 minutes par `etat.ps1` : `_DEPOT\rendus-3d\etat-production.txt`.
- **Suivi automatique, hors séance** (`post_series.ps1` du scratchpad, lancé par `Start-Process`, 15/09 matin) : à la fin de chaque série, `habiller_famille.py` habille ses familles et lance les contrôles ; résultat dans `rendu3d\post-<serie>.log`, planches dans `rendu3d\controle\`. Les alertes internes à la séance Claude sont tuées par le manque de mémoire : **pour reprendre**, lire les `post-*.log`, corriger les écarts, puis vérification indépendante, `integrer_visuels.py`, build (quand Blender est à l'arrêt ou entre deux séries), commit.
- **Vague 3** : les 12 familles validées en essai (15/09, 1 h) ; série `serie-vague3.json` (80) en file derrière la vague 2b.
- **Armatures** : nuances B500B / B500A retirées des pages (générateur + catalogue, 15/09) : l'intégration ne sera plus bloquée par le contrôle « nuance sur la page, absente de l'image ».
- **Vague 2** : données faites pour les tôles planes (froid, galva, Corten, alu, inox), profilés/tubes alu et inox (77), tôles larmées et striées (15), tôles perforées (8) ; pages inox corrigées (nuance sourcée) ; « Masse surfacique » contredite retirée de 36 pages (`integrer.py`). Essais conformes : matières, profilés alu/inox, tôles à relief (loupe e / E). Série `serie-vague2.json` (121 + 18 studios) en file derrière les armatures. Essai perforées en cours ; ensuite série `serie-vague2b.json` (relief + perforées).

## Rangement pour le propriétaire (demande du 14/09, avancée le 15/09 à 10 h 30 : « dès maintenant, un maximum »)
- Fait au fil des intégrations par `integrer_visuels.py` : `_DEPOT/images/2-categories/<univers>/<catégorie>/fond-blanc/` (photo studio) et `fiche-technique/` (visuel coté). Le 15/09 à 10 h 30, les 267 visuels déjà vérifiés y ont été déplacés (l'ancien `visuels-3d/` est supprimé) ; chaque famille vérifiée ensuite y arrive en même temps que sur le site.
- À la toute fin : proposer l'étape vidéo (CLAUDE.md), sans la lancer.

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
| Vague 3 : clôtures (30), bordures (2), caillebotis et marches (19), tôles profilées (7), panneaux isolés (8), tasseaux (2) | 68 | données faites, pages corrigées, géométrie écrite, essais en cours |
| Vague 3 : fixations de clôture | 5 | pas de plan : pas de rendu (question 27) |
| Visserie | 6 | vague 4 du brief (pas de 3D) ; à trancher (question 28) |

## Reprendre le rendu
Atelier hors OneDrive : `%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d\` — `final\` (production), `essais\`, `controle\` (planches), journaux `serie-*.log`.
1. `python scripts/rendu-3d/donnees_produits.py [famille…]` (données sourcées ; familles : poutrelles, cornieres, fers-t, plats, pleins, tubes, toles)
2. `python scripts/rendu-3d/preparer_rendus.py <params.json> car <slug…>` puis `--ajouter <params.json> studio studio-<famille> <3 slugs>` (`--essai 1600` pour un test)
3. `blender -b --factory-startup -t 4 -P scripts/rendu-3d/rendu_profil.py -- <params.json>` en arrière-plan
4. `python scripts/rendu-3d/habiller.py <slug>` et `--studio studio-<famille>` (`--essai` pour les tests)
5. `python scripts/rendu-3d/controler_rendus.py <famille…>` → planches dans `controle\`
   (4 + 5 d'un coup pour toute une série : `python scripts/rendu-3d/habiller_famille.py <famille…>`)
6. Vérificateur indépendant (`.claude/agents/verificateur-rendus.md`), puis `python scripts/rendu-3d/integrer_visuels.py --verdict CONFORME <famille…>`

Durée mesurée (1600 × 1200, 32 échantillons, `-t 4`, PC utilisé en parallèle) : 2 min 50 à 3 min 30 par image.
