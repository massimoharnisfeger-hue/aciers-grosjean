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

## Réglages validés
Test IPE 200 de la séance de préparation. Certaines valeurs ont pu évoluer depuis dans `rendu_profil.py` : le code fait foi.
- Caméra côté +X, azimut 20°, élévation 17°, focale 50 mm, tronçon de 500 mm : la section apparaît à gauche, le corps file vers la droite, la fiche tient dans le tiers droit. `[IPE, 14/09] (autocontrôle)`
- Calamine : metallic 0,12, rugosité 0,48–0,78, couleur de base très sombre (0,022–0,094 linéaire). Exposition AgX −1,15, look « Medium High Contrast ». `[IPE, 14/09] (autocontrôle)`
- Face sciée en acier nu (base 0,36, metallic 1, rugosité 0,32–0,46) : elle fait ressortir la forme de la section. `[IPE, 14/09] (autocontrôle)`
- Habillage : traits de cote avec halo blanc (lisibles sur l'acier foncé), pastilles jaunes, chiffres en IBM Plex Mono, mots en Questrial, ombre du sol à 55 % d'opacité. `[IPE, 14/09] (autocontrôle)`

## Erreurs rencontrées et correction
- Pièce surexposée, l'acier paraissait de l'aluminium : baisser l'exposition de la scène, pas la couleur de base. Le fond blanc et l'ombre ne bougent pas, puisqu'ils sont composés après. `[IPE, 14/09]`
- Acier trop clair même avec une base sombre : ce sont les reflets du studio blanc. Réduire le metallic de la calamine, qui est un oxyde mat. `[IPE, 14/09]`
- Cadrage de profil : la section était petite et à droite. Rapprocher la caméra de l'axe (azimut ~20°) et placer la caméra côté +X. `[IPE, 14/09]`
- Flèche invisible sur l'acier foncé : tracer d'abord un halo blanc, puis le trait. `[IPE, 14/09]`
- Ombre trop grise sur le fond blanc : multiplier l'alpha des pixels semi-transparents par 0,55. `[IPE, 14/09]`
- Téléchargement Blender : le fichier `.zip.sha256` individuel n'existe pas (404) ; utiliser la liste `blender-X.Y.Z.sha256`. `download.blender.org` refuse WebFetch : passer par `curl -A "Mozilla/5.0"`. `[préparation, 14/09]`

## Temps et ressources mesurés
- 800 × 600, 32 échantillons : 30 à 60 s. 1600 × 1200, 64 échantillons : 4 min 15 s (Ryzen 5 4500U, processeur seul). `[IPE, 14/09]`
- Pic mémoire de Blender pour une IPE : 371 Mo. La RAM du PC est souvent presque pleine à cause des navigateurs et des fenêtres Claude Code ouvertes. `[IPE, 14/09]`

## Pièges de l'environnement
- Jamais `npm install` dans OneDrive : `_OUTILS/site-local.ps1 -Mode verifier`. `[CLAUDE.md]`
- Plusieurs séances Claude travaillent dans ce dépôt : ne commiter que ses propres fichiers, jamais `git add -A`. `[préparation, 14/09]`
- Dépôt GitHub public : aucun chemin personnel (`C:\Users\…`) dans les scripts. Passer par `%LOCALAPPDATA%` ou des chemins relatifs. `[préparation, 14/09]`
- Un hook (GateGuard) exige un rappel des faits avant la première modification de chaque fichier : le prévoir, sans le contourner. `[préparation, 14/09]`

## Préréglages et contrôles automatiques créés
_(à compléter : nom, fichier, ce qu'il couvre, famille d'origine)_
