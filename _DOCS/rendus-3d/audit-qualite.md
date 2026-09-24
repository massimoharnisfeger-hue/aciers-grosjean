# Audit qualité des modèles 3D — boucle du 23/09/2026

Demande du propriétaire (23/09, après relecture du catalogue) : « parfois les dimensions, parfois
c'est beaucoup trop épais, parfois il y a des arrondis alors qu'il n'y a pas d'arrondis ». Boucle
lancée par `/loop` : AUDIT → CORRECTION → RÉAUDIT par produit, puis passage global.
Règle fondamentale : **les cotes sourcées ne changent pas** (`scripts/rendu-3d/donnees/produits.json`) ;
on corrige la fidélité visuelle (arêtes, proportions du tronçon, matière).

Règles du projet qui s'appliquent : `CLAUDE.md` (section Visuels 3D : essai → série → contrôle de
chaque image → vérification indépendante → intégration), `_DOCS/rendus-3d/lecons.md` (lu avant
chaque itération), essais dans `rendu3d/essais/`, jamais dans `final/`.

## REPRENDRE ICI

**Itération 2 (23/09, 13 h 56) — lot 1 en production** : essais B validés à la taille réelle
(carré 6, tube carré 15, rond 6 : arêtes vives, section et cotes inchangées, barre qui file ;
0 écart d'habillage). `habiller.py` efface la barre entre 0,615 W et 0,645 W (`debord` du
`<slug>.json`) ; `controler_rendus.py` ne contrôle plus le haut ni la fiche d'une barre en débord.
Lot 1 lancé en détaché : `python rendu3d/outils-seance/serie_audit.py carre-plein plat large-plat
rond-plein` (56 fiches + 4 studios, ~2 h à 6 cœurs). Suivi : `rendu3d/serie-audit.log` (lignes
`fin <famille> controles=<code>`, puis `FIN`) ; journaux par famille dans `rendu3d/audit/`.
Originaux d'avant l'audit : `rendu3d/final-avant-audit-23-09/` (retour arrière = recopier).

**Itération 3 (23/09, 14 h 45)** : carré plein rendu (7 + studio, 14 h 12), vu par le propriétaire
(planche `essais/ab-carre-plein.png`) ; 0 écart après correction du contrôle de luminance (corps de
barre, voir le carnet) ; studio gardé à 18 × / 20° après essai de 3 variantes
(`essais/ab-studio-carre-ratios.png`) ; **vérification indépendante en cours** (agent Opus, travail
dans `rendu3d/verif/carre-plein-23-09/`). Plats en production (37 + studio, ~3 min par image).

**Itération 4 (23/09, 15 h 30)** : carré plein **VALIDÉ et intégré**. L'intégration recadre
désormais elle-même (`integrer_visuels.recadrer_sur_place`, cadre de `recadrer_visuels.CADRE`) :
plus besoin de relancer `recadrer_visuels.py` ; texte alternatif sans « fiche technique ». Registre :
174 contrôles, 0 échec, mais 61,2 s (budget 60) pendant que Blender occupe les 6 cœurs → à
remesurer à vide après la production, ne pas relever le budget. Reste ouvert (mineur, vérificateur) :
écrire la longueur `L` des pièces dans le `.json` des photos studio (après la production, pour ne
pas changer l'empreinte du code en cours de série) ; contrôles proposés : largeur de la bande claire
d'arête (refus > ~8 px à 1600 px), sol sous la barre à 0,55 W et 0,61 W (écart > 10 niveaux).

**Itération 5 (23/09, 15 h 20)** : les deux défauts de l'audit ont maintenant leur contrôle au registre,
écrit après coup (règle « Quand quelque chose casse » de `CLAUDE.md`) : `tests/test_rendus_3d.py`, V1
(chanfrein ≤ 2 % de la paroi la plus fine, plafond 0,6 mm, aucun sur une tôle, `regler_chanfrein` appelé)
et V2 (cadrage validé 6,25 ×, barre 4 × plus longue qui sort du cadre). Rouges sur la version d'avant
l'audit (commit b7b0341) et sur six régressions simulées, verts sur le code actuel ; leçons L-052 et
L-053 de `_DOCS/LECONS.md`. Plats : 21 / 38 à 15 h 19, 2 min par image, fin vers 15 h 55. Question
posée au propriétaire : le profil T **aluminium** reste-t-il dans l'audit (il a exclu le « fer en T ») ?
Sans réponse, il reste dans le lot 2 (8e famille, vers 19 h).

**Itération 6 (23/09, 16 h 10)** : plats rendus (37 + studio, fin 15 h 51), 38 images sans écart
individuel ; famille refusée à −31 de luminance studio / fiches (seuil 30). Cause : la mesure comptait la partie
de la barre cachée sous la fiche incrustée (corps des fiches 85 → 92 ; photo studio inchangée, 60 → 59).
Corrigé dans `controler_rendus.py` (`luminance_piece(x_max=…)`, partie servie à gauche de 0,615 W) après les
contrôles V3 et V4 vus rouges ; plats et carré plein : 0 écart ; leçon L-054. Larges plats (3 + studio) : fin
16 h 03, 0 écart. Planches avant / après : `essais/ab-plat.png`, `essais/ab-large-plat.png`. Vérifications
indépendantes des plats et des larges plats **en cours** (`verif/plat-23-09/`, `verif/large-plat-23-09/`).
Ronds pleins en production (9 + studio, lancés 16 h 03, fin vers 16 h 25).

**Itération 7 (23/09, 16 h 38)** : **plats et larges plats VALIDÉS et intégrés** (vérifications CONFORME) ;
registre 178 contrôles, 0 échec, 41 s. Lot 1 terminé à 16 h 29 (ronds pleins : 0 écart, vérification en cours) ;
**lot 2 lancé à 16 h 29** par le script en attente (tubes carrés en premier). Mineurs relevés par les
vérificateurs, sans correction aujourd'hui :
- longueur `L` des pièces absente des `.json` des photos studio (3e constat) → après la production : l'écrire dans
  `ecrire_json`, recalculer les `.json` des familles refaites (`--points-seuls`), puis un contrôle qui la
  refuse absente ;
- photos studio : les barres du fond sont 26 à 28 niveaux plus sombres que celle de devant (large plat 51 / 53 / 78,
  carré plein 42 / 44 / 69), déjà avant l'audit → contrôle « luminance pièce par pièce » proposé, seuil à fixer
  avec le propriétaire (HUMAN_REVIEW) ;
- étiquette t posée sur la face longue des plats : mise en page validée depuis le 15/09 (comme tw sur l'IPE) ;
  la consigne du vérificateur, trop stricte (« aucune pastille sur la pièce »), est corrigée : aucune pastille
  sur la section, sur une autre pastille ou sur le bord du cadre.

**Itération 8 (23/09, 16 h 45)** : longueur des pièces écrite dans le `.json` des photos studio
(`rendu_profil.py`, contrôle V5 vu rouge puis vert ; `controler_rendus.py` refuse un studio sans elle ; leçon
L-055). Nouvelle empreinte du code : **078be3b429** (essai `essais/studio-essai-v5`, 10 s). Le lot 2 la prend à
partir des tubes rectangulaires (un processus Blender par famille) ; les tubes carrés, lancés avant, gardent
0995ae4728. Familles rendues avant : `.json` recalculés sans rendu par `outils-seance/points_famille.py`
(sauvegarde dans `audit/json-avant-points/`) ; carré plein, plats, larges plats faits (seules l'empreinte et la
longueur des pièces du studio changent, points des cotes identiques). **À faire avant d'intégrer** les ronds
pleins et les tubes carrés : `python outils-seance/points_famille.py <famille>`, sinon le contrôle les refuse.

**Itération 9 (23/09, 17 h 00)** : **lot 1 terminé et intégré** — carré plein (7), plats (37), larges plats (3),
ronds pleins (9) et leurs 4 photos studio, tous CONFORMES à la vérification indépendante. Registre : 179 contrôles,
0 échec, **21,8 s** avec Blender en route : le dépassement de 61,2 s de l'itération 4 venait de la charge
(vérificateurs en parallèle), le budget de 60 s reste. Carnet des leçons fusionné (150 → 144 lignes). Lot 2 :
tubes carrés en rendu (5 / 37 à 16 h 44, fin vers 18 h 10) ; avant leur intégration :
`python outils-seance/points_famille.py tube-carre` (rendus avec l'ancienne empreinte).
Durée du lot 2 recalculée sur le rythme mesuré (2,6 min par image, 3 quand un vérificateur tourne) : 187 images, fin vers 0 h 30 le 24/09 ; profil T alu vers 21 h (gardé par le propriétaire, 23/09 vers 18 h).

**Itération 10 (23/09, 18 h 35)** : **tubes carrés VALIDÉS et intégrés** (36 + studio ; registre 179 / 0 / 22 s).
Tubes rectangulaires rendus (18 h 26, 0 écart, nouvelle empreinte) : sur les petits tubes, l'étiquette t passe
sous la pièce (`paroi_sous()`, règle du 15/09) — le chanfrein assombrissait le bord de la paroi et masquait à la
règle le recouvrement de la paroi opposée ; vérification indépendante **en cours**, avec ce point à juger.
Mineurs des tubes carrés : pièces du fond du studio plus sombres (3e famille, HUMAN_REVIEW déjà noté) ; étiquette
t du 15x15x2 à 3 px de la face claire (10 px avant, marge sombre du chanfrein), sans chevauchement.
Tubes ronds acier en rendu (12 images, fin vers 19 h).

**Itération 11 (23/09, 19 h 20)** : tubes rectangulaires **À CORRIGER** à la vérification (rendus bons ; étiquette t
de 17 fiches descendue sous le tube, entre les rappels de b : sur le 50x20x2, « t 2 mm » se lisait comme b). Mon
explication (chanfrein qui masquait le recouvrement) était fausse : images habillées le 15/09 avant la règle
`paroi_sous()`, contrôle muet sans centre d'étiquette. Corrigé sans rendu : `place_t_tube()` (cavité à 6 px des parois,
sinon flanc), contrôles d'habillage V6, sidecar sans centre = écart (L-056). Tubes rectangulaires et carrés rhabillés
(0 écart ; seul le tube carré 15x15x2 bouge) ; planche `essais/ab-etiquette-t-tubes.png` ; **revérification en cours**
par le même vérificateur. Tube carré à réintégrer après elle (15x15x2). Tubes ronds : vérification en cours. Cornières
égales rendues (19 h 15, 0 écart, habillées avec les nouveaux contrôles) ; inégales vers 19 h 30, vérifiées ensemble.

**Itération 12 (23/09, 19 h 45)** : tubes rectangulaires **VALIDÉS** à la revérification (étiquette t : 12 sur le flanc,
7 calées dans la cavité, 2 à la place du 15/09 ; rien d'autre n'a bougé) et intégrés ; tubes carrés réintégrés
(15x15x2) ; **tubes ronds VALIDÉS et intégrés** (aucun défaut ; le mineur du 15/09 sur la face sciée a disparu).
Registre : 180 contrôles, 0 échec. Remarque récurrente du vérificateur traitée : les contrôles V6 ne tournaient qu'à
l'habillage → le sidecar porte maintenant `boites` et `controler_rendus.py` refuse une fiche habillée avant V6.
Les 7 familles intégrées ont été rhabillées : 131 images identiques à l'octet. Tubes rectangulaires alu et inox (t sous
le tube) et tubes carrés alu (sidecar sans centre) : refaits cette nuit par le lot 2. Cornières égales et inégales
en vérification ; cornières alu en rendu.

**Itération 13 (23/09, 20 h 15)** : **cornières acier égales et inégales VALIDÉES**, rhabillées (sidecars sans `boites` :
habillées à 19 h 14 et 19 h 28, avant le contrôle de 19 h 33 ; 34 images identiques à l'octet) et intégrées ; registre
180 / 0. Cornières et plats alu rendus (0 écart) : vérification commune en cours. Profils T et U alu en rendu.
**Questions au propriétaire (HUMAN_REVIEW)** : (1) photos studio, pièces du fond 7 à 27 niveaux plus sombres que celle de
devant (déjà avant l'audit) : égaliser l'éclairage ? (2) studio des cornières inégales : 900 mm (plafond) = 6 × la
section 150x100 ; la pièce reste trapue — garder, prendre un trio plus petit (60x40, 70x50, 100x50 : 9 ×) ou relever
le plafond ?

**Itération 14 (23/09, 21 h 10)** : **alu VALIDÉS et intégrés** : cornières égales, plats, profils T et U (vérifications
CONFORME, aucun défaut bloquant) ; registre 181 contrôles, 0 échec. Tubes alu : carrés et rectangulaires rendus ; sur
le rectangulaire 60x30x3, l'étiquette t partait à 350 px (flanc alu clair pris pour la paroi) → corrigé, contrôle V7,
leçon L-057 ; le contrôle « t sur paroi claire » tient compte de la place écrite par l'habillage (`place_t`). Tubes
ronds alu en rendu ; vérification des trois familles de tubes alu ensemble ensuite.
**Questions au propriétaire, ajoutées (HUMAN_REVIEW)** : (3) cornières alu : congé intérieur r1 = t/2 (valeur usuelle
**supposée**, `profils_alu_inox()`) alors que la photo du stock (G053) montre un angle quasi vif — le passer à ~0,1 t
et refaire les 8 fiches (~25 min) ? (4) face sciée de l'aluminium rendue en « acier nu » (plus sombre que le corps :
149 contre 205), alors que les coupes alu du stock sont claires — essai d'une matière de coupe par finition ?

**Itération 15 (23/09, 21 h 25) — décisions du propriétaire** : « fais de ton mieux », puis « réponds-toi et fais en
sorte que le rendu soit le mieux possible, le plus professionnel possible » (réponse aux questions HUMAN_REVIEW 1 à 4).
Décisions prises : (1) photos studio : éclairage plus égal entre les pièces (essais : débouchage sans ombre, lumière
du dessus doublée) ; (2) studio des cornières inégales : trio 60x40x5, 70x50x6, 100x50x6 (`TRIOS_IMPOSES` de
`outils-seance/serie_audit.py`) ; (3) cornières alu : r1 = 0,1 t d'après la photo du stock G053
(`donnees_produits.py`, 8 valeurs supposées changées, rien d'autre) ; (4) face sciée claire pour l'aluminium et
l'inox (`COUPE_PAR_FINITION` de `rendu_profil.py` : 0,72 et 0,58 ; acier inchangé à 0,36). Série arrêtée
proprement après les cornières inox (21 h 24, `stop-audit.txt`, 0 écart) ; 8 essais en cours
(`essais/essais-coupe-studio.json`). Puis : refaire les 7 familles alu et les 6 inox (coupe), les 2 de ronds à
béton, et les photos studio des 9 familles acier (`serie_audit.py --studio-seul`) ; deuxième sauvegarde des images
de l'audit dans `rendu3d/final-avant-reprise-23-09-soir/`. Estimation donnée au propriétaire : rendus finis vers
2 h 30, tout vérifié et intégré vers 4 h le 24/09.

**Itération 16 (23/09, 21 h 40)** : essais jugés (`essais/decision-coupe.png`, `essais/decision-studio.png`) :
coupe claire alu (0,72) et inox (0,58) **adoptée** (section lisible, coupe de métal frais) ; cornière alu r1 = 0,1 t
**adoptée** ; éclairage studio : débouchage sans ombre sans effet mesurable (écart fond / devant 25 → 21), lumière du
dessus doublée = pièces +6 à +9 niveaux, plus proches des fiches, sans délaver → **préréglage `eclairage_studio()`
pour l'acier brut** (`preparer_rendus.py`) ; alu et inox inchangés (déjà au niveau des fiches). L'écart fond / devant
vient de l'occlusion par les pièces voisines : naturel, gardé. **Production relancée à 21 h 40** (PID 15232) :
`serie_audit.py --studio-seul` sur les 9 familles acier (trio imposé pour les cornières inégales), puis 15 familles
(inox 6, alu 7, ronds à béton 2). À faire à chaque fin : planche, vérification, intégration (studios acier : réintégrer
la famille ; alu déjà intégrés : réintégrer après vérification).

**Itération 17 (23/09, 22 h 20)** : vérification des tubes alu (rendus de 20 h 46–21 h 11, ancienne coupe) : rond
CONFORME ; carré et rectangulaire **À CORRIGER** — coins extérieurs r1 = 0,75 t (valeur usuelle reprise de l'acier
formé à froid) alors que les photos du stock G061 / G063 montrent des coins vifs. Corrigé dans les données avant que
la série n'atteigne ces familles : tubes alu r1 = 0,1 t (G061, G063), profils T alu r = 0,25 t (petit congé estimé sur
la photo), profils U confirmés ; 16 valeurs changées, rien d'autre ; contrôle V8 (rayon supposé > t/4 sur l'alu = photo
citée), leçon L-058. Photos studio acier : 9 refaites (21 h 40–22 h 04, 0 écart), vérification en cours. Série
principale : cornières inox refaites (22 h 17, coupe claire, 0 écart) ; inox plat en rendu.

**Itération 18 (23/09, 23 h 05)** : **9 photos studio acier VALIDÉES** (éclairage du soir : corps +7 à +11 niveaux,
contrôle global −2 à −16 au lieu de −10 à −24, ni délavage ni brûlure ; cornières inégales au trio 100x50 / 70x50 /
60x40, longueurs 900 mm retrouvées) et **réintégrées** ; registre 182 contrôles, 0 échec, 51,5 s (sous charge).
Suites du vérificateur : `eclairage_studio()` limité aux barres, tubes et profilés (jamais essayé sur une tôle vue à
48°) ; `points_famille.py` prend le job studio de `<famille>.studio.json` s'il existe (sinon l'ancien trio des
cornières inégales reviendrait sous la nouvelle image). Mineur noté : la pièce de devant passe de 1 à 11 niveaux
au-dessus de sa fiche. Inox : cornières, plats, ronds pleins rendus (coupe claire, 0 écart), vérification en cours ;
tubes inox en rendu.

**Itération 19 (23/09, 23 h 35)** : inox cornières, plats, ronds pleins CONFORMES à la vérification ; mais sur les
plats inox, la coupe claire (0,58) sort à 4 niveaux de la face longue (section peu lisible en vignette ; 7 sur le plat
alu d'essai, 9 sur la cornière inox). Réglage corrigé à 23 h 25 : coupe alu 0,66, inox 0,50 ; contrôle V9 dans
`controler_rendus.py` (coupe à 8 niveaux au moins de la face longue ; plats, cornières, T, U) — refuse les 10 plats inox,
laisse passer le reste ; leçon L-059. Intégrés : cornières et ronds pleins inox (versions 0,58, à remplacer). **Reprise
programmée** (PID 22632, attend la fin de la chaîne 15232) : cornières alu et les 6 familles inox, à la coupe corrigée.
Estimation : fin des rendus vers 3 h 35, tout vérifié et intégré vers 4 h 30. Vérification des tubes inox en cours
(rendus à 0,58, seront refaits : ses constats sur les coins et les étiquettes restent utiles).

**Itération 20 (24/09, 0 h 15)** : tubes inox CONFORMES (coins arrondis justes d'après l'image publiée G071 / G072 ;
coupe 0,58 confondue avec le flanc, déjà refaite par la reprise). Profils T alu refusés par V9 : coupe à 0,66
2 niveaux plus claire que l'âme (face à 178). Réglage final de la coupe : **aluminium et inox 0,50** (0 h 11), au moins
une douzaine de niveaux sous la face la plus sombre ; contrôle étendu aux tubes (V10, paroi opposée ou anneau contre le
flanc ; leçon L-060). La série en cours rend les tubes alu à 0,50. **Reprise étendue** (PID 43976, attend la fin de
la chaîne 15232) : plats, T, U, cornières alu et les 6 familles inox. Estimation : fin des rendus vers 4 h 15, tout
vérifié et intégré vers 5 h.

**Itération 21 (24/09, 1 h 50)** : **tubes alu carrés, rectangulaires et ronds VALIDÉS et intégrés** (coins 0,12–0,31 mm,
vifs comme G061 / G063 ; coupe 0,50 à +27/+31 du dessus et −26/−27 du flanc, lisible en vignette ; étiquettes t à
la place de la règle) ; registre 184 contrôles, 0 échec. Série principale finie à 1 h 12 (ronds à béton : 0 écart,
vérification en cours) ; reprise démarrée à 1 h 12 : plats alu refaits (1 h 38, 0 écart), T et U en rendu.
Proposé par le vérificateur, non fait cette nuit : étendre V10 à la paroi haute contre le dessus et mesurer aussi en
vignette ; mesurer l'écart entre pièces d'un studio face par face (30 à 33 niveaux sur les tubes alu, constat
accepté comme ombre naturelle des voisines, sans seuil fixé).

**Itération 22 (24/09, 2 h)** : ronds à béton (rendus 0 h 55–1 h 12) CONFORMES aux points de l'audit, mais 2 défauts
repris : bouchons des nervures longitudinales dans le plan de la coupe (demi-disques noirs, 297 px sur le 12 mm ; masqués
avant par le chanfrein) et verrous en arcs symétriques au lieu d'hélices inclinées (mineur du 15/09). `nervures_barre()`
corrigé (départ 0,02 mm derrière la coupe, bouchons en matière de coupe, hélice à 55° en sens opposés) ; essai du 12 mm :
6 px de noir pur ; contrôle V11 (plus de 20 px de noir pur sur une section pleine servie) ; leçon L-061. Re-rendu des
2 familles programmé après la reprise (PID 47132). Rond à béton **laminé à froid** : question 31 ouverte (motif B500A,
finition) et **incohérence** : intégré le 22/09 alors que la question le dit « non intégré » → la version refaite ne
sera pas intégrée ; décision au propriétaire. Question 30 complétée (cornières inox laminées ou pliées ?). Profils T alu
refaits (1 h 47, 0 écart). Estimation : fin des rendus vers 4 h 20, tout vérifié et intégré vers 5 h, rapport ensuite.

**Périmètre fixé par le propriétaire (23/09, 14 h 45)** : « les tôles, bardages, clôtures et pieds de
clôtures tu as pas besoin de faire, les treillis non plus ». Hors audit : toutes les tôles (planes,
larmées, striées, perforées, profilées), bardage, panneau isolé, panneaux de clôture, poteaux,
treillis. Le chant arrondi des tôles (D1) reste donc un défaut connu, non corrigé par décision.
Puis (23/09, 15 h) : « les poutrelles ne refais pas, fer en T non plus » — poutrelles HEA, HEB, IPE,
UPN et fer T acier sortent aussi du périmètre. Profil T **aluminium** : le propriétaire, le 23/09 vers 18 h, « garde les profils en t » → il reste dans l'audit (lot 2, vers 21 h) ; le fer T acier reste exclu.
**Lot 2 en file** (script détaché PID 17428 : attend la ligne ` FIN` du lot 1 puis lance
`serie_audit.py`) : tubes acier (3), cornières égales et inégales (2), alu (7), inox (6), ronds à
béton (2) — 20 familles, 187 images, ~6 h 30 : fin estimée vers 22 h 30–23 h le 23/09.

**Demande du propriétaire (23/09, 14 h)** : « montre-moi les nouveaux modèles quand c'est fini » —
à chaque famille terminée, lui montrer dans la conversation la planche avant / après
(`outils-seance/ab_planche.py <famille> <slugs…>` : une taille petite, une moyenne, une grande,
plus la photo studio), avec une phrase de constat.

À faire pour chaque famille terminée : lire `audit/<famille>.controles.log` ; regarder la planche
contact (`rendu3d/controle/`) ; vérification indépendante (agent `verificateur-rendus`) ; puis
intégration : `PYTHONIOENCODING=utf-8 python scripts/rendu-3d/integrer_visuels.py --verdict CONFORME
<famille>` (elle recadre elle-même depuis l'itération 4 ; K13 vérifie 984 × 1133 au manifeste et sur le
disque), puis `python tests/lancer.py`.
Lots suivants proposés : tubes acier ; cornières et fers T ; alu ; inox ; poutrelles ; ronds à
béton ; tôles (D1 : chants vifs) ; treillis (bouts de fils, `fils_treillis`).

**Itération 1 (23/09, ~14 h)** : état initial fait, deux causes systémiques trouvées (D1, D2),
correctifs écrits dans `rendu_profil.py` (`largeur_chanfrein`, `regler_chanfrein`, cadrage sur
`longueur_cadre`) et `preparer_rendus.py` (`RATIO_CADRE`, `DEBORD`, `BARRES`, `RATIO_STUDIO`).
Essais A (tronçon 14 × cadré en entier) : arêtes nettes, mais section réduite à 64 % et cotes du
fer T tassées → **rejeté**. Essais B (cadrage inchangé, barre 4 × plus longue qui file hors du
cadre) : en cours, planches `rendu3d/essais/ab-debord-1.png` et `ab-debord-2.png`.
Rien n'est encore re-rendu en production ; rien de publié.

Prochaine étape : juger `ab-debord-*` (section à 100 %, barre qui file, pas de chevauchement avec
la fiche incrustée à droite, contrôles `habiller.py`) ; si bon, vérifier que `controler_rendus.py`
accepte une pièce qui sort du cadre, puis lancer la série de la première famille (carré plein),
contrôle de chaque image, vérification indépendante (`verificateur-rendus`), intégration **avec
recadrage** (`recadrer_visuels.py` : vérifier qu'il s'applique aux nouvelles images).

Durée annoncée au propriétaire (23/09) : ~375 images à refaire (barres, profilés, tubes, tôles,
studios), ~2 min par image à 6 cœurs, soit 12 à 13 h de rendu, plus contrôles et intégration :
environ une journée ; carrés, plats et ronds d'abord.

Outil de comparaison : `rendu3d/outils-seance/ab_planche.py <nom> <slug…>` (image publiée à gauche,
essai habillé et recadré comme le site à droite).

## État initial (inventaire)

- **Aucun fichier `.blend`** : les « modèles » sont procéduraux. Géométrie et matières :
  `scripts/rendu-3d/rendu_profil.py` ; paramètres par fiche : `scripts/rendu-3d/preparer_rendus.py`
  (lit `donnees/produits.json`) ; habillage 2D (cotes, fiche) : `habiller.py` ; contrôles :
  `controler_rendus.py`. Blender 4.5.13 dans `%LOCALAPPDATA%\Blender\blender-4.5.13-windows-x64`.
- **54 familles**, 495 fiches, **466 rendus de fiche + 48 photos studio** servis
  (`lib/visuels-produits.json`) ; originaux dans `rendu3d/final/`. 29 fiches sans rendu (chimie,
  visserie, fixations, outillage : hors 3D, décision du 14/09).
- **Références réelles** : `_DEPOT/images/site-actuel/<catégorie>/` (1 093 photos et dessins du site
  actuel), fiches techniques PDF (`public/documents/`), spécifications de forme de la vague 3
  (`rendu3d/outils-seance/specs/`).

## Défauts systémiques

### D1 — chanfrein fixe de 0,6 mm sur toutes les arêtes (🔴)

- **Constat** : carré 6×6 et plat 10×3 à arêtes visiblement arrondies (bande de reflet large, section
  en rectangle à coins ronds) ; chant des tôles de 1 mm en boudin dans la loupe ; arêtes extérieures
  du fer T 20×3 adoucies.
- **Cause** : `extruder()` pose un modificateur Bevel de **0,6 mm, 3 segments**, quelle que soit la
  pièce ; seules les tôles profilées et quelques formes spéciales le retirent. 0,6 mm = 10 % du côté
  d'un carré de 6, 20 % de l'épaisseur d'un plat de 3 ; sur une tôle de 1 mm, Blender le plafonne à
  0,5 mm par face : chant entièrement rond.
- **Références** : dessins et photos du site actuel — carré et plat à **arêtes vives**, tôles à chants
  vifs ; le fer T a bien des bouts arrondis (EN 10055), déjà modélisés par `r1`/`r2`.
- **Correction** : `largeur_chanfrein()` (`rendu_profil.py`) — 2 % de l'épaisseur la plus fine de la
  section, plafonné à 0,6 mm, supprimé sous 0,05 mm et sur les tôles planes. Les congés et arrondis
  normalisés (`r`, `r1`, `r2`, rayon extérieur des tubes) ne changent pas : ils existent sur le produit.

### D2 — tronçon de 6,25 × la section : une barre devient un bloc (🟠)

- **Constat** : carré 6×6 rendu sur 37,5 mm, plat 10×3 sur 62,5 mm : la pièce se lit comme un bloc
  trapu, d'où l'impression « beaucoup trop épais » ; la photo studio (7 × la plus grande section) a
  le même défaut.
- **Cause** : `preparer_rendus.py`, `piece(..., 500, 6.25)` et `7 * max(...)` du studio — cadrage
  choisi le 14/09 (autocontrôle, jamais validé par le propriétaire) pour grossir la section.
- **Références** : photos du site — barres longues et fines qui filent en perspective.
- **Correction** : la caméra cadre toujours le tronçon court de 6,25 × (`longueur_cadre`, section
  et cotes à leur taille validée), mais la barre rendue est 4 × plus longue (`DEBORD`) et file hors du
  cadre, comme sur les photos ; visée et lumières restent sur le tronçon cadré. Types concernés
  (`BARRES`) : plats, carrés, ronds, ronds à béton, cornières, fers T, tubes, poutrelles I et U ;
  poteaux, tôles et formes spéciales inchangés. Studio : pièces entières à 18 × la plus grande
  section (plafond 900 mm). Premier essai (tronçon 14 × cadré en entier) rejeté : section à 64 %.

## Statut par famille

Légende : À AUDITER · À CORRIGER · ESSAI · SÉRIE · VÉRIFICATION · VALIDÉ.

| Famille (catégorie) | Fiches | Type | Statut | Défauts constatés |
|---|---|---|---|---|
| carre-plein | 7 | CARRE | **VALIDÉ** (23/09, 15 h 30) | D1, D2 corrigés ; vérification indépendante CONFORME (bande d'arête 4–6 px contre 20–25, section carrée 0,98–0,99, cotes identiques au pixel) ; 2 mineurs corrigés (fondu d'ombre aligné sur 0,615 W ; intégration qui recadre, K12/K13) ; intégré (manifeste 984 × 1133) |
| plat (acier) | 37 | PLAT | **VALIDÉ** (23/09, 16 h 35) | D1, D2 corrigés ; vérification indépendante CONFORME (coins vifs à 0,1–1 px, reflet d'arête 1–3 px contre 6–15, rapport b/t = 1,03 × attendu par la perspective, cotes identiques au pixel) ; faux écart de luminance −31 corrigé dans le contrôle (partie servie, V3/V4) ; intégré (984 × 1133) |
| fer-t | 5 | T | À CORRIGER | D1 (arêtes extérieures), D2 |
| tole-galvanisee | 12 | TOLE | À CORRIGER | D1 (chant rond en loupe) |
| large-plat | 3 | PLAT | **VALIDÉ** (23/09, 16 h 38) | D1, D2 corrigés ; vérification CONFORME (épaisseur retrouvée 10,00–10,02 mm par ajustement de caméra, coins à 1 px au plus, bout de barre sorti du cadre servi) ; intégré |
| rond-plein (acier, inox) | 12 | ROND | acier **VALIDÉ** (23/09, 17 h 00) ; inox en lot 2 | D1, D2 corrigés ; vérification CONFORME (face sciée pleine : grand axe 322–326 px contre 290 avant sur le 6 mm, plus d'anneau ; rapport ellipse / cote constant 1,077 = perspective ; studio 392 mm mesurés pour 396) ; `.json` recalculés (longueur studio) ; intégré |
| tube-rond (acier) | 11 | TUBE-ROND | À CORRIGER | D1 (bourrelet sur la paroi de 2 mm), D2 |
| poutrelle HEB (témoin) | 11 | I | À AUDITER | 🟢 congés réels, proportions justes ; effet D1 imperceptible |
| bordures | 2 | BORDURE | À AUDITER | 🟢 arêtes vives, pli juste (vu le 23/09) |
| poteaux Cloplus 40 (témoin) | 8 | spécial | À AUDITER | 🟢 conforme au dessin (vu le 23/09) |
| treillis soudés | 17 | TREILLIS | À AUDITER | 🟡 bouts de fils arrondis (`fils_treillis` garde 0,6 mm) |
| corniere-egale / inegale (acier, alu, inox) | 28 | L | acier égale et inégale **VALIDÉES** (23/09, 20 h 15 : r1 à 0–1,3 % des tableaux, a et t retrouvés à 0,2 % et −1,7 % près, arêtes vives) et intégrées ; alu en VÉRIFICATION ; inox en lot 2 | D1, D2 |
| plat (alu, inox) | 21 | PLAT | À AUDITER | D1, D2 probables |
| profil-t / profil-u (alu) | 7 | T / U | À AUDITER | D1, D2 probables |
| tubes carrés, rectangulaires, ronds (acier, alu, inox) | 101 | TC/TR/TUBE-ROND | tubes acier **VALIDÉS** : carré (23/09, 18 h 25 ; bord de paroi 1,5–2,1 px contre 6–7, rayons = r1 ± 0,3 mm, t à −1,1/+2,4 %), rectangulaire (19 h 25, après correction de l'étiquette t : cavité ou flanc), rond (19 h 45 ; t à ±1 % contre 14–30 % trop mince avant, anneau de coupe plat) ; alu et inox en lot 2 | D1, D2 |
| poutrelles HEA, HEB, IPE, UPN | 45 | I / U | À AUDITER | — |
| tôles planes (chaud, froid, corten, quarto, alu, inox) | 69 | TOLE | À AUDITER | D1 probable |
| tôles larmées, striées, perforées | 23 | TOLE | À AUDITER | D1 probable |
| ronds à béton | 7 | ROND-BETON | À AUDITER | — |
| treillis soudés, à dépassants | 21 | TREILLIS | À AUDITER | — |
| bordures | 2 | BORDURE | À AUDITER | — |
| panneaux rigides, poteaux | 30 | spéciaux | À AUDITER | — |
| caillebotis, marches, plancher | 19 | spéciaux | À AUDITER | — |
| bardage, panneau isolé, tôle profilée | 17 | TOLE profilée | À AUDITER | — |

## Journal de la boucle

- **23/09, itération 1** : lecture du carnet 3D, du générateur et des références ; quatre rendus
  inspectés (carré 6×6, plat 10×3, fer T 20×3, tôle galva 1 mm) ; D1 et D2 établis ; correctif écrit ;
  essais A/B lancés (carré 6, plat 10×3, fer T 20×3, cornière 20×20×3, tube carré 15×15×2, tôle galva 1).
