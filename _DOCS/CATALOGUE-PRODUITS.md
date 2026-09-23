# Catalogue produits visuel — rapport de contrôle

Séance du 2026-09-23. Décision : ADR-0010. Pages : `/catalogue` (couverture et sommaire) et
`/catalogue/<univers>` (six chapitres). Code : `lib/catalogue-visuel.ts`, `components/catalogue/`
(`OngletsChapitres`, `FicheFamille`, `PlancheVariante`, `FiltreCatalogue`, `ImprimerChapitre`).
Contrôles : `tests/test_catalogue.py` (K1 à K9). Les compteurs de ce rapport viennent de
`scripts/catalogue/inventaire.py` (relevé du 2026-09-23, `_DOCS/catalogue-produits/RESUME.md`) et
du build du même jour ; aucun n'est repris d'un document antérieur.

## INVENTAIRE

| Mesure | Valeur |
|---|---|
| Nombre total de produits | 495 |
| Nombre total d'images inventoriées | 4 232 fichiers (521 dans `public/`, 1 621 dans `_DEPOT/images/`, 2 090 dans l'atelier Blender) |
| Nombre de catégories | 6 univers, 77 nœuds, dont 54 familles portant des produits |
| Nombre de produits avec image | 466 (rendu 3D aux cotes au manifeste) |
| Nombre de produits sans image | 29 |

Toutes les images du projet ont été produites dans Blender (rendus de fiche cotés, photos studio
sur fond blanc) ; les 1 093 photos de `_DEPOT/images/site-actuel/` sont des références téléchargées
du site actuel, jamais servies par le nouveau site. Aucune scène `.blend` n'est conservée : les
rendus sont pilotés par script (`scripts/rendu-3d/rendu_profil.py`).

## IMAGES

| Mesure | Valeur |
|---|---|
| Images Blender protégées (servies par le manifeste, jamais modifiées) | 514 : 466 rendus de fiche + 48 photos studio |
| Images utilisées par le catalogue | 514, toutes issues du manifeste `lib/visuels-produits.json` (contrôle K4) |
| Images orphelines | 5 photos studio dans `public/images/produits/` que rien ne sert (voir « À trancher ») |
| Images à vérifier | 2 726 : 395 essais d'atelier, 1 538 originaux `.png`/`.webp` de l'atelier, 1 093 photos du site actuel, 7 planches contact |
| Images manquantes | 0 fichier servi absent du disque ; 29 produits sans visuel (ligne « VISUEL À COMPLÉTER » de la matrice) |
| Doublons | 519 copies volontaires pour le propriétaire dans `_DEPOT/images/2-categories/` (CLAUDE.md, demande du 15/09) ; 0 fichier servi à plusieurs produits |
| Illisibles | 3 `.jpeg` de `_DEPOT/images/site-actuel/` (références, statut « À vérifier ») |

Détail par fichier : `_DOCS/catalogue-produits/inventaire-images.csv` (chemin, nom, format,
dimensions, poids, produit, catégorie, sous-catégorie, type, source, statut, note).

## PRODUITS

| Mesure | Valeur |
|---|---|
| Produits correctement associés | 495 : chaque planche porte le lien de sa fiche `/p/<slug>` et, pour 466 d'entre elles, l'image de ce produit et de lui seul (K3, K4) |
| Produits nécessitant une vérification | 0 association ambiguë ; 29 sans visuel (chimie, visserie, fixations de clôture, outillage) |
| Variantes identifiées | 495 variantes réparties en 54 familles ; 48 familles ont des caractéristiques communes affichées en tête, 46 des caractéristiques distinctives par variante |

Matrice produit ↔ visuels : `_DOCS/catalogue-produits/matrice-produits.csv` (slug, produit,
univers, catégorie, sous-catégorie, image principale, photo studio de la catégorie, autres studios
non servis, PDF, route de la fiche, route du catalogue, statut).

Référence commerciale : **absente des données**. Les 501 « SKU » relevés sur le site actuel sont
des identifiants techniques (GUID), sans référence fabricant ni EAN. Le catalogue n'affiche donc
pas de champ « Référence » plutôt qu'un identifiant de base de données.

## CATALOGUE

| Mesure | Valeur |
|---|---|
| Pages créées | 7 : `/catalogue`, `/catalogue/acier`, `/catalogue/aluminium`, `/catalogue/inox`, `/catalogue/toiture-bardage`, `/catalogue/jardin-cloture`, `/catalogue/quincaillerie` |
| Catégories (chapitres) | 6 |
| Sous-catégories (sections) | 17 nœuds intermédiaires ; les familles rangées directement sous un univers (caillebotis & marches, outillage, visserie) forment des sections sans titre |
| Fiches produits | 54 fiches famille, 495 planches de variante ; chaque planche renvoie à la fiche du site |

Structure d'un chapitre : fil d'Ariane → onglets des six chapitres → ouverture (numéro, nom,
accroche et intro déjà publiées sur le site, mosaïque de photos studio, compteurs) → index des
familles (replié sur mobile, fixe à gauche dès 1024 px) → filtre → sections → fiches famille →
planches → chapitre précédent / sommaire / chapitre suivant.

Fiche famille : photo studio (manifeste), nom, accroche du site si elle existe, nombre de
variantes, caractéristiques identiques à toutes les variantes (nuance, procédé, surface, découpe…),
finition, unité de vente, longueurs standard, fiches techniques PDF communes, lien vers la
catégorie du site. Rien n'est complété : une donnée absente n'a pas de ligne.

Planche de variante : rendu 3D aux cotes (`unoptimized`, 17 à 30 Ko, boîte 4/5 réservée), nom du
produit, caractéristiques distinctives (trois au plus, dans l'ordre de `lib/specs.ts`), poids,
« Voir la fiche ». Sans visuel : emplacement « Visuel à compléter », jamais le dessin SVG de famille.

Recherche : filtre par chapitre sur nom, cotes, famille et sous-catégorie, sans donnée embarquée
(attributs `data-recherche` rendus par le serveur, `lib/recherche-texte.ts` des deux côtés ;
« 40x40 » et « 40 × 40 » se lisent pareil ; chaque jeton consomme un jeton distinct, donc un tube
40 × 20 ne répond pas à « 40x40 »). Mesuré : « 40x40 » garde 20 produits sur 293 dans le chapitre
acier. Sans résultat : familles réelles du chapitre proposées, renvoi vers `/recherche` et `/devis`.
Recherche globale : `/recherche`, déjà en place.

Impression : `@media print` (en-tête, pied de page, filtre et commandes masqués ; coupure de page
avant chaque section ; planches et en-têtes de famille insécables), bouton « Imprimer ce chapitre ».

## SYSTÈME VISUEL

- Palette : 100 % charte officielle (blanc dominant, `#333642` texte, `#FFD500` en signal seul —
  onglet du chapitre courant, numéros du sommaire, anneau de focus —, `#D1D6DA` bordures, `#F4F6F7`
  fonds de planche avec la grille industrielle du site). Aucune couleur nouvelle.
- Typographie : Poppins 600/700 pour les titres (chapitre 36/60 px, section 24/36 px, famille
  24/30 px, planche 14 px), Comfortaa pour « Chapitre n », l'édition et les accroches, Questrial
  16/14/12 px pour le texte, IBM Plex Mono à chiffres tabulaires pour les valeurs techniques. Texte
  secondaire à 72 % d'encre, jamais de gris sur blanc.
- Grille : conteneur 80 rem ; planches 2 colonnes dès 320 px, 3 dès 640 px, 4 dès 1280 px ; fiche
  famille 2/5–3/5 dès 768 px ; index des familles en colonne de 14 rem dès 1024 px.
- Espacements : 12/16 px entre planches, 48/64 px entre familles, 48/64 px entre sections.
- Mouvement : aucun effet d'apparition ; seuls les changements d'état au survol et au focus
  (bordure, soulignement), 150 ms. Le contenu est intégralement visible sans JavaScript.
- Cibles : liens texte en `lien-tactile` (≥ 24 px), onglets ≥ 48 px de haut, champ de filtre
  16 px de police.

## RESPONSIVE

Balayage `scripts/qa/balayage-responsive.py` (Chromium, page déroulée jusqu'en bas) sur `/catalogue`,
`/catalogue/acier`, `/catalogue/quincaillerie`, `/catalogue/toiture-bardage` : **0 débordement
horizontal sur 44 mesures, 0 parcours en échec**. Captures relues à 320, 390, 768 et 1280 px
(couverture, ouverture de chapitre, fiche famille, planches, filtre, état vide, impression).

| Largeur | Constat |
|---|---|
| 320 px | aucun débordement ; onglets sur 2 colonnes, planches sur 2 colonnes, index des familles replié |
| 360 px | idem |
| 375 px | idem |
| 390 px | idem ; filtre vérifié (« 40x40 » → 20/293) |
| 414 px | idem |
| 768 px | fiche famille sur deux colonnes, planches sur 3 colonnes |
| 1024 px | index des familles fixe à gauche ; onglets sur une ligne |
| Desktop (1280 px) | planches sur 4 colonnes ; seule cible < 24 px : « Espace pro » dans l'en-tête du site (71 × 20 px), résidu déjà tracé le 22/09 |

Deux corrections issues du balayage : les libellés « n produits » des onglets et les étiquettes de
la mosaïque de couverture passaient sous 12 px (11 px) → 12 px ; les noms d'onglets tronqués
(« Alumini… ») → deux lignes.

Limite d'environnement rencontrée, **antérieure au catalogue** : sur le serveur local
(`next start`, Windows), l'optimiseur d'images ne répond jamais à la requête AVIF de
`studio-panneau-isole-eco.webp` à `w=640` (WebP à 640 px : 40 ms ; AVIF à 384 ou 750 px : 0,1 à
0,4 s ; AVIF à 640 px : rien après deux minutes). Un navigateur, qui accepte l'AVIF, attend donc
indéfiniment cette image aux largeurs où `sizes` choisit 640 px — dans le catalogue 390, 414, 600 et
1024 px sur `/catalogue/toiture-bardage` ; sur le site existant, `/toiture-bardage` à 390 px
présente exactement le même blocage (mesuré le 23/09, `wait_until="networkidle"`). Les autres
largeurs de la même page passent (0 débordement). Ni le fichier ni la configuration n'ont été
touchés : c'est un cas d'encodeur local, à revérifier sur la préproduction Vercel, dont l'optimiseur
est un service distinct ; si le blocage s'y reproduit, la décision serait de retirer `image/avif` de
`next.config.mjs` (choix de site, pas de catalogue).

## TESTS

| Étape | Résultat |
|---|---|
| Typecheck | `tsc --noEmit` : 0 erreur |
| Lint | `next lint` : 0 avertissement |
| Build | `next build` : vert, 646 pages (639 + 7) |
| Tests | `python tests/lancer.py` : **170 contrôles - 0 échec** (socle 160 → 170 : X1, K1 à K9), 17 s |
| Routes vérifiées | `/catalogue` et les six chapitres répondent 200 (K1, K2) ; connues de `scripts/routes.py` (K8) ; dans le sitemap ; liées depuis le méga-menu, le menu mobile, le pied de page, `/produits` et `/plan-du-site` |

Poids servis (build sain) : `/catalogue` 264 Ko brut / 48 Ko gzip ; `/catalogue/acier` (293
planches) 1 888 Ko / 106 Ko ; `/catalogue/aluminium` 530 Ko / 54 Ko ; autres chapitres 262–421 Ko /
45–51 Ko. Le chapitre acier double son HTML par la charge utile React de l'App Router : si le
propriétaire le trouve lent sur mobile, la piste est une page par sous-catégorie pour ce chapitre.

## À TRANCHER (HUMAN_REVIEW)

1. **Photos studio en concurrence** — trois catégories ont plusieurs photos studio valides et le
   manifeste n'en sert qu'une : `panneaux-rigides` (plis 205 servie, medium 3D ignorée), `poteaux`
   (Cloplus 40 servie, Clogriff 64 ignorée), `caillebotis-marches` (plancher O2 servie ; caillebotis,
   marche caillebotis, marche O2 ignorées). Le catalogue montre la photo servie. Laquelle doit
   représenter chaque famille est un choix visuel, pas une déduction.
2. **29 produits sans rendu** — colles et étanchéité (4), galvanisation à froid (7), peintures et
   primaires (6), visserie (6), fixations de clôture (5), outillage (1). Un rendu coté n'y a pas de
   sens ; des photos produit du propriétaire les compléteraient (« Visuel à compléter »).
3. **Codes articles** — Grosjean a-t-il des références internes ? Sans elles, pas de colonne
   « Référence ».
4. **Conventions de l'ADR-0010** (familles, planches, ni prix ni référence, filtre, impression) : à
   confirmer.
5. **Matière des chiffres clés de la fiche produit** — hors catalogue, constaté au passage :
   `app/p/[slug]/page.tsx` passe le nom de l'univers comme « Matière » (`u.nom`), ce qui donne
   « Jardin & clôture » ou « Quincaillerie & ferronnerie » pour une bordure ou un caillebotis. Le
   catalogue ne reprend pas cette ligne.
