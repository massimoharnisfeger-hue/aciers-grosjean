# 16 septembre 2026 — Visuels 3D : vague 3 vérifiée, formes refaites d'après les dessins fabricants, rangement complet

Séance Claude Code sur le PC, commencée le 14/09 (suite de `2026-09-15_visuels-3d-vague2-rangement.md`) : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em
Période couverte : 15/09 vers 12 h → 16/09 à 0 h 40.

## Demandes du propriétaire (dans l'ordre)
- « Continue à 6 cœurs pour blinder » (15/09, 10 h 44) ; « le PC doit rester allumé jusqu'à 22 h » (15/09, 16 h 44).
- Faire un checkup de la mémoire, du carnet de leçons et de l'avancement.
- « Tu as tout mis dans le dossier image ? » ; puis (16/09, 0 h 20) : relire tous les .md sans mélanger les jours ; mettre **toutes** les images possédées dans `_DEPOT/images/2-categories` en créant les catégories nécessaires ; une fois tout fini, inspecter le site (tous les produits présents ? des images dans toutes les catégories ?) en le comparant au site officiel, tout publier sur https://aciers-grosjean.vercel.app et faire un rapport : ce qui manque, ce qui est en place, ce qui reste à mettre en place.
- Mettre tous les .md à jour avant la limite d'usage de la semaine.

## Constats
- Vérification indépendante de la vague 3 (15/09, 17 h 30) : formes génériques sur plusieurs familles pourtant à 0 écart aux contrôles (panneaux de clôture à maille tournée de 90°, poteaux Cloplus en tube, Clogriff en caisson, marches aux joues dressées, panneau isolé sans mousse dans les nervures). Les dessins fabricants publiés sur les fiches donnaient la bonne forme.
- Les pages de la vague 3 ne reprenaient que le nom du produit alors que les images affichaient les valeurs des descriptions et des PDF : audit valeur par valeur, 210 lignes ajoutées aux pages.
- Tôles perforées : le moiré venait de l'habillage (seuil d'ombre), pas du rendu.
- Le vert RAL 6005 était juste sur les fils fins mais terne sur les grandes faces planes des poteaux.
- Limite d'usage atteinte vers 20 h 30 (reprise à 21 h 40) : deux agents interrompus, repris sans perte.

## Décisions
- Remodéliser d'après les dessins fabricants mesurés (cotes « cotée / mesurée / supposée »), une famille à la fois (un agent), essais autocontrôlés avant tout rendu de production ; rendus déposés dans `rendu3d\reprises\a-rendre\` et rendus par un script détaché.
- La page dit ce que dit l'image : lignes sourcées ajoutées par `specs_sourcees()` du générateur ; valeurs sans source propre au produit retirées (face interne du panneau isolé, revêtement des marches O2).
- Laque verte des poteaux plus mate et plus saturée (préréglage dans `teinte()`).
- Copier dans 2-categories aussi les images rendues mais pas encore vérifiées (état dans `_ETAT.txt`).

## Fait
- En ligne (commits `17faabb`, `1209868`, `28beed7`, `c36ea48`, `51d311c`) : inox refait, tôles inox brossées et à froid, studios galva et alu, bordures, bardage imitation bois, treillis à dépassants, tôles perforées, panneaux de clôture MEDIUM 3D et PLIS 205, poteaux Cloplus 40 et Clogriff 64 : **431 fiches** avec visuel.
- `_DEPOT/images/2-categories` : 519 images (468 en ligne + rendues en cours de vérification), `_ETAT.txt`.
- Questions 36 à 40 ; carnet de leçons (formes publiées, page = image, moiré d'habillage, laque colorée, script de dépôt) ; journal du 16/09 ; avancement avec une section « REPRENDRE ICI ».

## Reprise du 16/09 (PC redémarré à 5 h 33, séance relancée vers 11 h 45)
- État d'avant la coupure vérifié puis terminé : 2 studios marches rendus avec la version du commit (`git show` via Bash, empreinte `ed72898bd5` identique aux 10 rendus de la nuit), habillage + contrôles 0 écart, vérification indépendante **CONFORME** → 9 fiches + 3 studios intégrés.
- Panneau isolé ECO et tôle profilée : code de l'agent interrompu vérifié complet, essais mesurés (mousse stable 177→179, loupe tôle 0,04 % de noirs), production de 17 rendus (11 h 54 → 12 h 35) via `rendu_reprises.ps1` relancé, contrôles 0 écart, vérification indépendante **CONFORME** (les 6 défauts du 15/09 corrigés et mesurés) → 15 fiches + 2 studios intégrés.
- **455 fiches sur 477 en ligne, vague 3 terminée** ; build OK, commit `24f71d3` poussé (déploiement Vercel). 2-categories : 519 images, `_ETAT.txt` 12 h 58.
- Audit final refait : produits (501 officiels / 495 nouveaux, 6 hors catégorie absents) + pages (0 image cassée, 0 catégorie vide). Questions 41 à 47 consignées.

## Reste à faire
- Rapport final au propriétaire (fait dans la conversation) ; réponses aux questions 27, 28, 31, 37 pour les 22 dernières fiches (caillebotis 10, rond à froid 1, fixations 5, visserie 6).
- Défauts mineurs listés dans l'avancement ; proposer l'étape vidéo maintenant que la production est stabilisée.
