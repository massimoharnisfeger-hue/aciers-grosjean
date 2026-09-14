# Carnet de leçons — visuels 3D

Mémoire de travail du projet. **À lire au début de chaque itération, à compléter après chaque famille et après chaque correction du propriétaire.**

Règles d'écriture :
- Une leçon = une ligne, concrète et vérifiable (valeur, fichier, commande). Pas de généralités.
- Indiquer la source : `[famille, date]` et `(validé propriétaire)` ou `(autocontrôle)`.
- Une leçon contredite par un résultat plus récent est **remplacée**, pas empilée.
- Tout réglage validé devient un préréglage dans le code ; toute erreur qui s'est produite deux fois devient un contrôle automatique. Noter ici le nom du préréglage ou du contrôle.
- Toutes les 3 familles : relire, fusionner les doublons, supprimer ce qui est devenu faux. Rester sous ~150 lignes.

---

## Préférences du propriétaire
- Réponses en français simple : il n'est pas développeur. `[préparation, 14/09]`
- Production **automatique** : enchaîner les familles, informer avec les rendus test et les planches contact, ne s'arrêter que si une donnée manque. `[14/09] (validé propriétaire)`
- Photo studio : 1 par catégorie. Visuel caractéristiques : 1 par fiche. Mises en situation : faites par lui avec l'IA, hors périmètre. `[14/09] (validé propriétaire)`
- Ne jamais afficher une valeur inventée ou supposée. `[14/09] (validé propriétaire)`
- Photo studio : fond blanc pur, pièce seule, sans cote, ombre douce, 1600 × 1200. Visuel caractéristiques : modèle `_DEPOT/images/test-blender/poutrelle-ipe-200-en-acier-caracteristiques.png`. `[14/09] (validé propriétaire)`
- Finition : `lib/site-actuel.json` d'abord, puis la description, puis une vraie photo ; sinon la finition la plus courante, marquée « supposée » et jamais affichée. `[14/09] (validé propriétaire)`
- 18 produits sous emballage (DL Chemicals, Zinga, primaires, Flex) : pas de 3D, seulement dire si la photo du site actuel est utilisable (fait : `references-recap.md`). `[14/09] (validé propriétaire)`
- Photo studio : **trois tailles côte à côte** quand la famille a plusieurs tailles ; une seule pièce pour les familles sans gamme (tôles, produits uniques). `[poutrelles, 14/09] (validé propriétaire)`
- Nuance affichée = celle du site actuel telle quelle (S275 IPE, S275/S355 HEB, S235 ou S275 UPN) ; aucune nuance quand le site n'en donne pas (HEA → questions en attente). « EN 10025-2 » seulement si une source le mentionne. `[poutrelles, 14/09] (validé propriétaire)`
- Longueurs affichées = celles du site actuel (1 à 6 m) + « longueurs supérieures sur demande » sans chiffre (les textes disent « jusqu'à 15 m » et « 3 à 12 m » : écart en attente). `[poutrelles, 14/09] (validé propriétaire)`
- Deux poids sur une même page du site actuel : afficher celui de la **fiche**, l'image doit dire la même chose que la page ; noter l'écart en attente. `[poutrelles, 14/09] (validé propriétaire)`
- Poids de la fiche à plus de 3 % du tableau fournisseur publié (ou du poids théorique) : sources contradictoires, **poids non affiché** sur l'image et question en attente (plats 80x10/80x8 +23 %, 23 tubes +3 à 8 %). Seuil appliqué dans `poids_et_controle()` (`donnees_produits.py`). `[vague 1, 14/09] (autocontrôle, à confirmer par le propriétaire)`
- Clogriff 64 2M50 « VERT RAL 7016 » : c'est un **gris anthracite RAL 7016** (pastille de la photo du site ; le vert de la série est le RAL 6005) → nom corrigé en « GRIS RAL 7016 ». `[clôture, 14/09] (validé propriétaire)`
- Poteaux Cloplus 40 : **aluminium** (fiche fabricant `GAG - FT-CP40-Plis205.pdf` : « poteau en aluminium », « alliage d'aluminium à très haute limite élastique »). `[clôture, 14/09] (validé propriétaire)`

## Réglages validés
Test IPE 200 de la séance de préparation. Certaines valeurs ont pu évoluer depuis dans `rendu_profil.py` : le code fait foi.
- Caméra côté +X, azimut 20°, élévation 17°, focale 50 mm, tronçon de 500 mm : la section apparaît à gauche, le corps file vers la droite, la fiche tient dans le tiers droit. `[IPE, 14/09] (autocontrôle)`
- Calamine : metallic 0,12, rugosité 0,48–0,78, couleur de base très sombre (0,022–0,094 linéaire). Exposition AgX −1,15, look « Medium High Contrast ». `[IPE, 14/09] (autocontrôle)`
- Face sciée en acier nu (base 0,36, metallic 1, rugosité 0,32–0,46) : elle fait ressortir la forme de la section. `[IPE, 14/09] (autocontrôle)`
- Habillage : traits de cote avec halo blanc (lisibles sur l'acier foncé), pastilles jaunes, chiffres en IBM Plex Mono, mots en Questrial, ombre du sol à 55 % d'opacité. `[IPE, 14/09] (autocontrôle)`
- GPP (grenaillé, primaire) : base sRGB [135, 66, 50] mesurée sur la vraie photo du stock IPE (groupe G010 de `references-groupes.csv`), rugosité 0,62, bosselage fin. Préréglage `TEINTE_GPP` (`preparer_rendus.py`), matière `materiau_gpp` (`rendu_profil.py`). `[poutrelles, 14/09] (autocontrôle)`
- UPN : ailes à pente intérieure 8 % (DIN 1026-1, citée par la fiche VM 2013), tf mesuré à b/2, congés r1 en racine et r2 en bout d'aile : `section_u()`. `[poutrelles, 14/09] (autocontrôle)`
- Cadrage studio : tronçon 900 mm, azimut 24°, élévation 20°, boîte (0,12 ; 0,14 ; 0,88 ; 0,86). Caractéristiques : 500 mm, boîte (0,07 ; 0,10 ; 0,62 ; 0,90). `[poutrelles, 14/09] (autocontrôle)`
- 32 échantillons, seuil adaptatif 0,03, débruitage OIDN = 64 échantillons à seuil 0,02 à l'œil (écart moyen 0,4/255 sur la pièce, recadrage à 100 %) : préréglage par défaut de `preparer_rendus.py`. `[poutrelles, 14/09] (autocontrôle)`
- Studio multi-tailles : la plus haute à gauche, extrémités alignées, écart = 0,9 × hauteur de la voisine de droite (`ecart_studio`) : plus aucune pièce masquée. `[poutrelles, 14/09] (autocontrôle)`
- Tronçon proportionné à la section : visuel caractéristiques 6,25 × plus grande cote (plafond 500 mm), studio 7 × plus grande cote de la plus grosse pièce (plafond 900 mm) ; les poutrelles gardent 500 et 900 mm. `[cornières, 14/09] (autocontrôle)`
- Titre de la fiche : nom sans « en acier / Acier LAC / laminé à chaud » (`titre_image`), sur deux lignes si besoin ; surtitre avec les noms du catalogue (« PROFILÉS » accentué, `surtitre_image`). `[cornières, 14/09] (autocontrôle)`
- Sections creuses (tubes) : anneau de quadrilatères entre contour extérieur et intérieur de même nombre de points, puis extrusion (`extruder`). Plat posé sur chant : cote verticale = largeur, pince = épaisseur. `[vague 1, 14/09] (autocontrôle)`

## Erreurs rencontrées et correction
- Pièce surexposée, l'acier paraissait de l'aluminium : baisser l'exposition de la scène, pas la couleur de base. Le fond blanc et l'ombre ne bougent pas, puisqu'ils sont composés après. `[IPE, 14/09]`
- Acier trop clair même avec une base sombre : ce sont les reflets du studio blanc. Réduire le metallic de la calamine, qui est un oxyde mat. `[IPE, 14/09]`
- Cadrage de profil : la section était petite et à droite. Rapprocher la caméra de l'axe (azimut ~20°) et placer la caméra côté +X. `[IPE, 14/09]`
- Flèche invisible sur l'acier foncé : tracer d'abord un halo blanc, puis le trait. `[IPE, 14/09]`
- Ombre trop grise sur le fond blanc : multiplier l'alpha des pixels semi-transparents par 0,55. `[IPE, 14/09]`
- Téléchargement Blender : le fichier `.zip.sha256` individuel n'existe pas (404) ; utiliser la liste `blender-X.Y.Z.sha256`. `download.blender.org` refuse WebFetch : passer par `curl -A "Mozilla/5.0"`. `[préparation, 14/09]`
- Visuel IPE 200 de la préparation : poids calculé (22,40) et nuance S235JR lus dans `lib/catalogue.ts`, non sourcés ; calamine alors que le site vend l'IPE en GPP. L'habillage lit uniquement `scripts/rendu-3d/donnees/produits.json`. `[poutrelles, 14/09]`
- Première teinte GPP trop orange à côté de la photo du dépôt : assombrir la base (réglage ci-dessus). `[poutrelles, 14/09]`
- Tableaux VM 2013 : un tableau statique en bas de PDF écrasait la bonne ligne (IPE h = 64,6). Garder la première occurrence, filtre 0,85–1,15 × h nominal ; ce sont les alertes de recoupement qui l'ont révélé. `[poutrelles, 14/09]`
- Nuance : seule la première était lue dans « S275/S355 » ; `nuance_et_norme()` les collecte toutes. `[poutrelles, 14/09]`
- Studio « 3 tailles » : barres décalées en profondeur qui se masquent en partie ; écarter davantage si cette variante est retenue. `[poutrelles, 14/09] (autocontrôle)`
- Données contradictoires dans le site actuel lui-même : poids UPN de la description (tableau fournisseur) ≠ poids de la fiche (+0,1 à +0,8 %). Toujours comparer description et fiche avant d'afficher. `[poutrelles, 14/09]`
- Petites cornières : la flèche d'épaisseur, à mi-hauteur, touchait l'étiquette de la cote verticale (même hauteur). Pince remontée à 70 % de la hauteur pour toutes les sections sauf I, U et tube rond ; contrôle automatique « flèche sous l'étiquette » créé. `[cornières, 14/09]`
- Tableaux fournisseurs avec colonnes vides (fers T) : `tableau_vm2013(..., sauter_vides=True)`. Nom « 17,2(18)x2mm » : la désignation courante entre parenthèses casse les motifs de cotes. `[vague 1, 14/09]`
- Fiches fournisseurs publiées sur le site : « Nuance d'acier : S235 » (IPE, HEA, HEB, tubes), en contradiction avec les descriptions (IPE S275, HEB S275/S355) : ne pas en déduire une nuance, question en attente. `[vague 1, 14/09]`

## Temps et ressources mesurés
- 800 × 600, 32 échantillons : 30 à 60 s. 1600 × 1200, 64 échantillons : 4 min 15 s en rendu isolé (Ryzen 5 4500U, processeur seul). `[IPE, 14/09]`
- 1600 × 1200, 32 échantillons, seuil 0,03, 9 rendus dans une seule instance Blender (données persistantes) : 107 à 172 s par image, le premier étant le plus long ; 64 échantillons dans la même instance : 225 s. `[poutrelles, 14/09]`
- Habillage PIL : 1 à 2 s par image ; WebP caractéristiques 34–37 Ko, studio 14–25 Ko. `[poutrelles, 14/09]`
- Pic mémoire de Blender pour une IPE : 371 Mo. La RAM du PC est souvent presque pleine à cause des navigateurs et des fenêtres Claude Code ouvertes. `[IPE, 14/09]`

## Pièges de l'environnement
- Jamais `npm install` dans OneDrive : `_OUTILS/site-local.ps1 -Mode verifier`. `[CLAUDE.md]`
- Plusieurs séances Claude travaillent dans ce dépôt : ne commiter que ses propres fichiers, jamais `git add -A`. `[préparation, 14/09]`
- Dépôt GitHub public : aucun chemin personnel (`C:\Users\…`) dans les scripts. Passer par `%LOCALAPPDATA%` ou des chemins relatifs. `[préparation, 14/09]`
- Un hook (GateGuard) exige un rappel des faits avant la première modification de chaque fichier : le prévoir, sans le contourner. `[préparation, 14/09]`
- JSON écrit par PowerShell `Set-Content` : BOM UTF-8 refusé par Blender (« Unexpected UTF-8 BOM ») ; `rendu_profil.py` lit en `utf-8-sig`. `[poutrelles, 14/09]`
- PowerShell 5.1 : `python -c` avec du code sur plusieurs lignes et des guillemets casse vite ; écrire un script dans le scratchpad. `[poutrelles, 14/09]`
- 3 « images » du site actuel sont des PDF nommés `.jpeg` : `references_planches.py` les ignore et les liste. `[références, 14/09]`

## Préréglages et contrôles automatiques créés
- `TEINTE_GPP` et échantillons 32 / seuil 0,03 par défaut : `preparer_rendus.py`. `[poutrelles, 14/09]`
- `affichable()` (`habiller.py`) : aucune valeur absente ou « supposée » n'est écrite sur l'image. `[poutrelles, 14/09]`
- Contrôles d'habillage (`habiller.py`, ligne `CONTROLES :`) : étiquette hors cadre, étiquette sur la fiche, étiquettes qui se chevauchent, titre trop long. `[poutrelles, 14/09]`
- Alertes de données (`donnees_produits.py`) : cotes A/B/C/D du site ≠ fournisseur, poids site ≠ fournisseur de plus de 3 %, hauteur du nom ≠ hauteur fournisseur (sauf HEA). `[poutrelles, 14/09]`
- `preparer_rendus.py` refuse une photo studio qui mélange deux finitions. `[poutrelles, 14/09]`
- `controler_rendus.py <famille…>` : fichiers, 1600 × 1200, WebP < 200 Ko, pièce dans le cadre et à gauche de la fiche, marges blanches du studio, textes de l'image = données sourcées non supposées = fiche du site, planches contact (`rendu3d/controle/`). `integrer_visuels.py` refuse une famille qui a encore un écart. `[poutrelles, 14/09]`
- Contrôles `habiller.py` ajoutés : « flèche sous l'étiquette », « fiche technique trop haute ». `[cornières, 14/09]`
- `poids_et_controle()` : poids non affiché au-delà de 3 % d'écart avec le fournisseur ou le théorique. `[vague 1, 14/09]`
