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
- Rangement final des visuels pour le propriétaire : les deux formats (photo studio fond blanc + visuel avec fiche technique) dans `_DEPOT/images/2-categories/`, classés par catégorie, **une fois toute la production terminée, pas avant**. Ce dossier remplacera alors `_DEPOT/images/visuels-3d/` (déplacement, pas de doublon ; mettre à jour `integrer_visuels.py`, `_DEPOT/LISEZ-MOI.txt` et la ligne de CLAUDE.md). `[fin de production, 14–15/09] (demande du propriétaire)`
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
- Tôles à relief (`relief_tole`) : éléments en instances (instanciation par sommets, deux gabarits à ±45° en damier) + un élément réel coupé par le chant avant (`bisect_plane` + `holes_fill`) où la loupe pince l'épaisseur au relief E ; épaisseur de base e pincée sur le plat voisin (`decalage_e` : 12 mm larme, 5,3 mm quintette) ; champ de loupe 6 × épaisseur totale (à 10 ×, 3 et 5 mm se distinguaient mal). Larme EN 10363 type T 30 × 10 mm au pas de 35 ; quintette : barrettes 40 × 3,5 mm écartées de 7,5, cellules de 44 mm à 45°. `[vague 2, 14/09] (autocontrôle)`
- Tôles perforées (`plaque_perforee`) : cellules percées en instances (hexagone à trou rond pour la quinconce R/T, carré pour C/U, tuile aléatoire de 250 mm tournée par quarts), cellules du bord coupées aux cotes exactes ; dessus et dessous triangulés par `mathutils.geometry.tessellate_polygon`. `[vague 2, 14/09] (essai en cours)`
- Matières vague 2 (`rendu_profil.py`) : à froid base 0,30 rugosité 0,32 ; alu base 0,78 rugosité 0,42 ; inox base 0,56 rugosité 0,30 **sans anisotropie** (sans carte UV, Cycles étire le reflet en cercles autour de z : croix sombre sur une tôle) ; variation de rugosité ±6–8 % sur les grandes tôles (`ecart_rugosite`), sinon taches de 25 cm. Galvanisé et Corten gardés du 1er essai. `[vague 2, 14/09] (autocontrôle)`
- Tôle : plaque à plat, caméra élévation 48° / azimut 10°, largeur l devant, longueur L le long du bord droit, colonne de gauche libre (cadrage 0,25–0,62) pour une loupe ronde sur le chant avant (2e rendu 700 × 700, champ 10 × e, 30 mm au moins) avec l'épaisseur e pincée dedans ; point du chant relié choisi pour que le trait ne traverse ni la pièce ni une étiquette. `[tôles, 14/09] (autocontrôle)`

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
- Loupe de tôle vide ou décalée : la caméra rapprochée (quelques cm) était sous la distance de découpe proche de Blender (10 cm par défaut). `cam.data.clip_start = 0.001` pour tout gros plan. `[tôles, 14/09]`
- 2e occurrence du conflit flèche d'épaisseur / étiquette de cote verticale (UPN 80, déjà vu sur les cornières) : l'étiquette verticale descend automatiquement à 28 % de la cote quand une flèche passe à sa hauteur (`habiller.py`), sans nouveau rendu. `[poutrelles, 14/09]`
- Photos studio : l'ombre douce touchait les bords (marges non blanches, détecté par `controler_rendus.py` sur les 4 studios poutrelles). `rendu_sur_blanc` estompe l'ombre sur 90 px et l'annule sur les 24 derniers : marges d'un blanc pur sur toutes les images. `[poutrelles, 14/09]`
- Arrêt volontaire de Blender après les visuels d'une série (pour sauter des rendus devenus inutiles) : code de sortie 255 attendu, pas une erreur. `[poutrelles, 14/09]`
- Petites pièces (rond à béton 12, plat 10x3, rond 6) : avant de la pièce et sol coupés, face avant noire. Découpe proche de la caméra (10 cm par défaut) : `clip_start = 1 mm` pour toutes les caméras. Détecté à l'œil sur un essai, **pas par les contrôles** : regarder chaque essai. `[armatures, 14/09]`
- Lignes de rappel à 4 mm fixes de la pièce : détachées sur les sections de 10 mm. Jour = min(4 mm, 0,18 × écart de cote). `[armatures, 14/09]`
- Vérification indépendante poutrelles (CONFORME) : ombre des grandes sections sous la fiche (fond 230/255) → l'ombre s'efface avant x = 0,645 W et contrôle « fond de la fiche ≥ 238 » ; poids « 8,3 » sur la page contre « 8,30 » sur l'image → deux décimales partout ; « Procédé : laminé à chaud » des pages HEA/HEB non sourcé → sourcé par la norme EN 10034 citée par la fiche fournisseur et affiché sur l'image. `[poutrelles, 14/09] (vérification indépendante)`
- Contrôle ajouté (proposé par le vérificateur) : pointes de flèche d'une cote hors de sa propre étiquette (cotes courtes). `[poutrelles, 14/09]`
- Cornières 40x40x3 et 50x50x3 : grand triangle noir, **passé inaperçu du contrôle automatique**, vu sur la planche contact. Arrondi du bout d'aile (r2 = 3 et 3,5 mm) ≥ épaisseur (3 mm) : la face du bout disparaissait et le contour se croisait. `contour_arrondi()` borne chaque arrondi à la place disponible (98 % du côté si le voisin est vif, 49 % s'il est arrondi) pour L, U et T ; contrôle « part de noir pur dans la pièce » (> 2 %, > 35 % pour les tubes) créé dès la première occurrence vu la gravité. Toujours regarder les planches, même à 0 écart. `[cornières, 14/09]`
- Fiches fournisseurs publiées sur le site : « Nuance d'acier : S235 » (IPE, HEA, HEB, tubes), en contradiction avec les descriptions (IPE S275, HEB S275/S355) : ne pas en déduire une nuance, question en attente. `[vague 1, 14/09]`
- Vérification indépendante cornières (CONFORME, 1 défaut mineur) : lignes de rappel à 27–67 px de la pièce sur les 13 cornières rendues **avant** le correctif du jour de rappel ; les 2 reprises étaient justes. Une famille mélangeait deux versions du code, invisible aux contrôles. Corrigé sans rendu : `preparer_rendus.py --points-seuls` recalcule les points (cadrage identique, vérifié point par point : seuls les débuts de rappel bougent), puis rhabillage. Après tout changement de `rendu_profil.py`, refaire ou recalculer toute la famille en cours. `[cornières, 14/09] (vérification indépendante)`
- Pages de la vague 3 : le générateur lisait « 200X105cm » comme « 200 × 105 mm » et « 150/25 x 2500mm » comme « 25 × 2500 mm » ; le site actuel y met des poids factices (1 kg, 0 kg, 2 100 kg). Règle : avant de rendre une famille, comparer nom, page et fiche fournisseur, corriger la page d'abord (`specs_vague3()` du générateur, `integrer.py`). `[vague 3, 14/09]`
- Panneaux de clôture délavés sur fond blanc : les fils de 4–5 mm sur 2,5 m font 1 à 2 px, tous leurs pixels sont semi-transparents et l'atténuation de l'ombre (alpha × 0,55 sous 250) les effaçait à moitié. Pièces à fils fins : ombre sans atténuation (`rendu_sur_blanc(..., ombre=1.0)`). `[vague 3, 15/09]`
- Tasseau imitation bois : le « 90 » du dessin fabricant est l'entraxe des tasseaux (8 par lé de 710), pas la largeur du plat ; le premier essai n'en montrait que 5. Lire une cote de dessin avec son rôle (entraxe, largeur, hauteur), pas seulement sa valeur. `[vague 3, 14/09]`
- Bordure rendue en bloc plein de 20 mm : `section_de` recevait la profondeur du pli (`b`, cadrage) comme épaisseur de tôle (`t`). Pour toute pièce en tôle pliée, `b` est l'encombrement et `t` l'épaisseur ; regarder le rendu brut d'un essai avant l'habillage. `[vague 3, 14/09]`
- Spécifications ajoutées d'office par le générateur du nouveau site, sans source (2e cas après B500A/B500B des armatures) : inox « 304 (1.4301) — brossé grain 320 » sur 43 pages, alors que les descriptions disent 304, 304L (ronds pleins), 304 **et** 304L (tôles GR320) et « brut ou brossé ». Avant chaque famille, lire nom + description et corriger la page (`specs_inox()` du générateur + lignes de `lib/catalogue.ts`) ; le contrôle « … sur la page, absente de l'image » de `controler_rendus.py` bloque l'intégration tant que page et image divergent. `[alu-inox, 14/09]`

## Temps et ressources mesurés
- 800 × 600, 32 échantillons : 30 à 60 s. 1600 × 1200, 64 échantillons : 4 min 15 s en rendu isolé (Ryzen 5 4500U, processeur seul). `[IPE, 14/09]`
- 1600 × 1200, 32 échantillons, seuil 0,03, 9 rendus dans une seule instance Blender (données persistantes) : 107 à 172 s par image, le premier étant le plus long ; 64 échantillons dans la même instance : 225 s. `[poutrelles, 14/09]`
- Série réelle (`-t 4`, essais en parallèle sur 2 cœurs, PC utilisé) : 45 poutrelles en 2 h 35, soit 3 min 25 par image ; 4 studios trois tailles en 13 min. Essai 1600 px à 8 échantillons sur 2 cœurs : 2 min 10 à 3 min. `[poutrelles, 14/09]`
- Habillage PIL : 1 à 2 s par image ; WebP caractéristiques 34–37 Ko, studio 14–25 Ko. `[poutrelles, 14/09]`
- Pic mémoire de Blender pour une IPE : 371 Mo. La RAM du PC est souvent presque pleine à cause des navigateurs et des fenêtres Claude Code ouvertes. `[IPE, 14/09]`

## Pièges de l'environnement
- Jamais `npm install` dans OneDrive : `_OUTILS/site-local.ps1 -Mode verifier`. `[CLAUDE.md]`
- Plusieurs séances Claude travaillent dans ce dépôt : ne commiter que ses propres fichiers, jamais `git add -A`. `[préparation, 14/09]`
- Dépôt GitHub public : aucun chemin personnel (`C:\Users\…`) dans les scripts. Passer par `%LOCALAPPDATA%` ou des chemins relatifs. `[préparation, 14/09]`
- Mémoire du PC (15 Go, souvent 4 Go libres) : lancer `site-local.ps1 -Mode verifier` (Node, plusieurs Go) pendant une série Blender a fait tuer par le système tous les processus d'arrière-plan, Blender compris (15/09, 0 h 54, série profils arrêtée à 61/137). Pas de build pendant un rendu ; une seule chaîne d'arrière-plan pour enchaîner les séries ; à la reprise, `reste_serie.py` (scratchpad) ne relance que les rendus manquants. `[vague 1, 15/09]`
- Arrêter un script détaché en filtrant `Win32_Process` sur sa ligne de commande : la commande PowerShell de Claude contient le même texte et se tue elle-même (code 255, 15/09). Construire le motif par morceaux (`"ev" + "eil"`) et exclure les lignes qui contiennent `Get-CimInstance`. `[vague 1, 15/09]`
- Mise en veille : sur secteur, le PC du propriétaire ne se met jamais en veille (réglage Windows) ; sur batterie, après 3 min. Pour une nuit de rendu sans toucher aux réglages : demande « système requis » (`SetThreadExecutionState`, `eveil.ps1` du scratchpad ; le 15/09, jusqu'à 13 h à la demande du propriétaire, avec `rendu3d\threads.txt` = 6 cœurs retiré à la même heure). Ne protège ni de la fermeture du capot ni d'une batterie vide. `[vague 1, 15/09]`
- Un hook (GateGuard) exige un rappel des faits avant la première modification de chaque fichier : le prévoir, sans le contourner. `[préparation, 14/09]`
- JSON écrit par PowerShell `Set-Content` : BOM UTF-8 refusé par Blender (« Unexpected UTF-8 BOM ») ; `rendu_profil.py` lit en `utf-8-sig`. `[poutrelles, 14/09]`
- PowerShell 5.1 : `python -c` avec du code sur plusieurs lignes et des guillemets casse vite ; écrire un script dans le scratchpad. `[poutrelles, 14/09]`
- Script qui vide un dossier suivi par OneDrive avant de le réécrire : un fichier verrouillé l'arrête à mi-chemin (14/09 : `integrer.py`, 51 PDF de `public/documents/` supprimés, restaurés par `git checkout`). Recopier seulement les fichiers changés, supprimer les périmés à la fin en tolérant les verrous (`integrer.py` corrigé). `[vague 2, 14/09]`
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
- `controler_rendus.py` : ligne de rappel à plus de 25 px (ou plus de la moitié du trait) du pixel de pièce **le plus proche** (mesuré le long du trait, le contrôle se trompait sur les talons chanfreinés des petites sections) ; famille issue de plusieurs versions de `rendu_profil.py` (empreinte `code` écrite dans chaque `<slug>.json`). `preparer_rendus.py --points-seuls` pour rhabiller sans rendu. `[cornières, 14/09]`
