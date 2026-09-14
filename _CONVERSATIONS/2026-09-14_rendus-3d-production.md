# 14 septembre 2026 — Production des visuels 3D (étapes 0 à 2 et test poutrelles)

Séance Claude Code sur le PC : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em

## Demande
Deux visuels Blender par fiche : photo studio (fond blanc, 1 par catégorie) et visuel caractéristiques (1 par fiche, cotes + fiche technique, modèle `_DEPOT/images/test-blender/poutrelle-ipe-200-en-acier-caracteristiques.png`).
477 fiches ; 18 produits sous emballage exclus (dire seulement si la photo du site actuel est utilisable).
Ordre imposé : étapes 0 (corriger le générateur), 1 (références visuelles), 2 (données sourcées), puis rendu test des poutrelles IPE, HEA, HEB, UPN, à montrer avant d'aller plus loin. Au premier test, demander : photo studio avec une barre ou 2-3 tailles.
Règle : aucune valeur supposée affichée ; en cas de doute, demander.

## Fait
- **Étape 0** : générateur corrigé — profils U alu (section « 20 × 20 × 20 mm »…, épaisseur 2 mm, poids recalculés 0,30/0,38/0,46/0,63 kg/m) et 28 tôles alu/inox sans « oxycoupage » (générateur + `lib/catalogue.ts`).
- **Étape 1** : 1 093 images du site actuel téléchargées (`references_telecharger.py` → `_DEPOT/images/site-actuel/`), regroupées en 137 visuels (`references_planches.py`, dHash), classées une à une (`references_classer.py` → `references.csv`, `references-groupes.csv`) ; récapitulatif par famille et réponse pour les 18 produits sous emballage : `_DOCS/rendus-3d/references-recap.md`.
- **Étape 2 (poutrelles)** : `donnees_produits.py` → `donnees/produits.json` + `donnees-produits.csv`. 45 fiches, 0 alerte. h, b, tw, tf, r (r1/r2 UPN) des tableaux VM 2013 ; poids, finition, longueurs du site actuel ; nuance et norme des descriptions (S275 IPE, S275/S355 HEB, S235/S275 UPN, rien HEA) ; recoupements automatiques cotes/poids site ↔ fournisseur.
- **Rendu test poutrelles** : `rendu_profil.py` réécrit (liste de rendus en une instance Blender, section U à ailes inclinées 8 % DIN 1026-1, matière GPP calée sur la vraie photo du dépôt [135, 66, 50], calamine pour BRUT) ; `habiller.py` réécrit (lit uniquement les données sourcées, `affichable()` masque toute valeur supposée, contrôles automatiques) ; `preparer_rendus.py` (préréglages).
  9 rendus : caractéristiques IPE/HEA/HEB/UPN 200 + studio IPE (1 barre), IPE 3 tailles, HEA, HEB, UPN. 107 à 172 s par image (32 échantillons, seuil 0,03) ; comparaison 64 échantillons : identique à l'œil, préréglage passé à 32.
  Autocontrôle : formes conformes (UPN à ailes inclinées), textes = données sourcées, aucun chevauchement, WebP 14–37 Ko. Images envoyées au propriétaire.
- `_OUTILS/site-local.ps1 -Mode verifier` : TypeScript et build de production OK (catalogue.ts modifié).
- Carnet de leçons complété (réglages validés, erreurs corrigées, temps mesurés, préréglages et contrôles créés) ; `avancement.md` créé.

## Constats à trancher (posés au propriétaire, notés dans avancement.md)
1. Studio : une barre ou trois tailles côte à côte ?
2. Générateur : « Nuance S235JR — EN 10025-2 » et « Longueur standard 6 m ou 12 m » sur les 45 fiches poutrelles ≠ site actuel (S275 IPE, S275/S355 HEB, S235/S275 UPN, rien HEA ; longueurs 1–6 m, « jusqu'à 15 m »).
3. « norme 10025 » du site → « EN 10025 » ?
4. Poids UPN : description (tableau fournisseur) ≠ fiche (+0,1 à +0,8 %) sur la même page du site actuel.
5. Clogriff 64 2M50 « VERT RAL 7016 » : vert 6005 ou gris 7016 ?
6. Cloplus 40 : légende « (ALU) » sur l'image fabricant — aluminium ou acier ?

## Réponses du propriétaire (14/09) et suite
- Décisions : studio en trois tailles ; nuances du site telles quelles, HEA sans nuance (en attente) ; « longueurs supérieures sur demande » ; poids de la fiche (écart UPN en attente) ; Clogriff 2M50 → « GRIS RAL 7016 » ; Cloplus 40 en aluminium. Nouvelle règle CLAUDE.md : site officiel, puis internet, sinon `questions-en-attente.md` et on continue.
- Fait : décisions notées au carnet ; catalogue et générateur corrigés ; `questions-en-attente.md` ; composition studio multi-tailles validée à l'essai ; contrôle automatique (`controler_rendus.py`) et intégration (`integrer_visuels.py`, galerie de la fiche produit) prêts ; build OK.
- En cours : série poutrelles (45 visuels puis 4 photos studio trois tailles), puis contrôle, vérification indépendante, intégration.

- Vague 1 (suite) : données sourcées, sections et rendus test des cornières, fers T, plats, ronds, carrés et tubes ; règle « poids non affiché au-delà de 3 % d'écart » (à confirmer par le propriétaire) ; séries enchaînées derrière les poutrelles.

## Reste à faire
- Poutrelles puis cornières, profils et tubes : habillage, contrôle, vérificateur indépendant, intégration, build, commit.
- Tôles laminées à chaud et armatures (fin de la vague 1), puis vagues 2 et 3 (avancement.md).

## Suite (mode automatique) — cornières, inox, vague 2
- Vérification indépendante des cornières : CONFORME ; lignes de rappel décollées sur les petites tailles (rendues avant un correctif) → points recalculés sans rendu, rhabillage, contrôle automatique créé ; intégration, build OK.
- Constat : « 304 (1.4301) — brossé grain 320 » sur les 43 fiches inox venait du générateur. Descriptions du site : 304 (plats, tubes, cornières), 304L (ronds pleins), 304 et 304L (tôles GR320), finition « brut ou brossé ». Pages corrigées ; questions 16 à 18 en attente.
- Vague 2 : données tôles et profilés alu/inox faites ; matières des tôles corrigées après essai ; tôles larmées, striées et perforées : références et dimensions de motif relevées (EN 10363 type T : larme ≈ 30 × 10 mm, relief 1 à 2 mm ; quintette alu d'après la photo du site), géométrie à faire.
- Reste : séries profils/tubes, tôles et armatures en cours dans Blender ; vague 2 (larmées, striées, perforées, alu, inox) ; vague 3 ; visserie.
- Tôles larmées, striées et perforées : géométrie (relief en instances, cellules percées, tuile aléatoire périodique), loupe e / E, essais conformes ; séries en file (139 puis 26 visuels).
- Pages : masse surfacique contredite retirée de 36 fiches (`integrer.py`) ; incident OneDrive sur `public/documents/` (51 PDF supprimés puis restaurés) et script corrigé.
