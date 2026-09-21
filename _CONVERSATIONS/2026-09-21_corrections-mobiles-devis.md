# 21 septembre 2026 — corrections mobiles du formulaire de devis

## Demande

« Il faut que tu inspectes le site dans son intégralité pour corriger tous ces bugs », puis
« corrige tout et ensuite fais un audit pour être sûr et ensuite mets ça sur Vercel ».
Point de départ annoncé par le propriétaire : « il y a full bug surtout sur mobile ».

## Constats

**Le site n'est pas « full bug ».** Inspection des 12 gabarits couvrant les 626 URL du sitemap,
à 320, 375, 768 et 1280 px, au navigateur piloté. `scrollWidth` égale exactement la largeur
d'écran sur les 12 gabarits, à toutes les largeurs : aucun débordement horizontal. Cohérent avec
`_DOCS/AUDIT-2026-09-14.md`, qui documentait déjà la suppression de Lenis et GSAP pour le mobile.

Les deux audits existants ne listaient **aucun bug mobile ouvert** : le premier recense des
défauts déjà corrigés et des décisions en attente, le second porte sur la structure.

Les vrais défauts étaient concentrés dans le formulaire de devis :

1. Les 6 champs en 14 px — Safari iOS agrandit la page au focus sous 16 px. La classe `champStyle`
   ne déclarait aucune taille ; les 14 px venaient du `text-sm` du `<label>` parent. Invisible en
   lisant la classe du champ, visible seulement à la taille calculée au navigateur.
2. Zéro `name`, zéro `autoComplete`, zéro `inputMode` sur les 115 lignes du fichier.
3. Soumission par `mailto:` : `window.location.href = url`, aucune requête réseau.

Deux faux positifs écartés après vérification, plutôt que « corrigés » : les vignettes de
`GalerieProduit.tsx` ont `alt=""` mais un `<span className="sr-only">` porte leur libellé — balisage
correct ; et les 38 « débordements » détectés à 320 px sont le bandeau marquee, rogné volontairement
par un parent en `overflow: hidden`.

## Décisions

- **Apostrophes typographiques plutôt que désactivation de règle.** ESLint activé a révélé 48
  erreurs `react/no-unescaped-entities` sur 20 fichiers. Le garde-fou de configuration interdit de
  modifier `.eslintrc.json` pour faire taire un linter. Escaper en `&apos;` aurait dégradé la
  lisibilité du source et le problème serait revenu à chaque phrase française écrite. Remplacement
  par U+2019, la vraie apostrophe française : corrige aussi un défaut typographique réel sur des
  textes visibles par les visiteurs.
- **ESLint 8 et non 9.** Le `.eslintrc.json` du dépôt utilise l'ancien format de configuration ;
  ESLint 9 impose le format « flat config » et demanderait une migration. Compromis assumé :
  `eslint@8.57.1` est marqué non supporté par son éditeur, à réévaluer lors d'une reprise de la
  config lint.
- **Étape `Lint` explicite en CI.** `next build` saute le lint en silence quand eslint est absent :
  une dépendance que personne n'appelle ne vérifie rien.

## Fait

- 4 défauts mobiles corrigés dans `DevisForm.tsx`, avec 5 contrôles écrits **avant** la correction,
  vus rouges (4 sur 5), puis verts.
- ESLint installé, branché sur la CI, et les 2 contrôles rouges de `tests/test_lint.py` éteints.
- 48 apostrophes typographiques dans 20 fichiers.
- Leçons L-013 et L-014 inscrites au carnet avec l'ID de leur contrôle.
- Validation : `92 controles - 0 echecs`, puis TypeScript, ESLint et build de production verts
  (`site-local.ps1 -Mode verifier`, code de sortie 0).

## Reste à faire

- **`mailto:` (BLK à ouvrir)** : `DevisForm.tsx:42-45` perd la demande si le visiteur n'a pas de
  messagerie configurée. Sur le site d'une entreprise dont le métier est le devis, c'est le défaut
  le plus coûteux du lot. Remplacer par un envoi serveur exige une décision : quel service d'e-mail,
  avec quelles clés.
- **Zones cliquables** : 37 à 46 par page sous 24 px (minimum WCAG 2.2), nav et pied de page à 14 px
  de haut. Touche les 626 pages. Correction site-wide, donc décision de design.
- **Texte sous 12 px** : 1 à 27 éléments selon la page, 27 sur `/acier`.
- **`/meta.json` renvoie 404**, demandé en boucle par le navigateur.
- **Avertissement framer-motion** : un conteneur d'animation liée au défilement est en
  `position: static`, son décalage est donc mal calculé.
- **ESLint 8 non supporté** : migrer vers 9 et le format flat config.
