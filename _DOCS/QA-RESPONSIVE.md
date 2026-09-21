# QA responsive — 320 px → 1280 px

État au 21/09/2026, après trois balayages Chromium (`scripts/qa/balayage-responsive.py`).
Rien ici n'est déclaré testé sans l'avoir été : chaque case cochée correspond à une mesure réelle.

## Méthode

- **Navigateur réel** : Chromium (Playwright Python), fenêtre à la largeur indiquée, page déroulée
  jusqu'en bas, mesures en lecture seule : `scrollWidth` contre `innerWidth` avec éléments coupables,
  cibles tactiles < 24 px (WCAG 2.2, 2.5.8), textes < 12 px, erreurs console et page, réponses
  réseau ≥ 400 sur l'origine.
- **Parcours joués** à 320, 375 et 414 px : menu mobile (ouverture, CTA visible, fermeture, pas de
  débordement), recherche « tube » (48 fiches), filtre du tableau produits (`/acier/armatures-beton`),
  formulaire de devis (bouton actif une fois valide, envoi, état final).
- **Captures d'éléments** pour ce que `scrollWidth` ne voit pas : comparaison à 320/360/375/414/1280,
  fil d'Ariane, pied de page, menu ouvert, formulaire, tableau à 768.
- **Régression desktop** : 1024 et 1280 px dans chaque balayage, capture de la comparaison à 1280.
- **Contrôles source** qui gardent les corrections : `tests/test_responsive.py` (R1-R3), vus rouges
  avant correction, verts après. Leçons L-018 à L-020 dans `LECONS.md`.

Limites : pas d'appareil physique (ni Safari iOS ni Chrome Android réels), pas de test de zoom
navigateur à 200 %, pas de test clavier. Les largeurs intermédiaires sont couvertes par le
raisonnement (une seule grille mobile-first, `sm:` à 640 px) et par 11 points de mesure, dont 360,
390 et 414 hors points de rupture.

## Inventaire

35 routes (`app/**/page.tsx`), 626 URL au sitemap. Familles dynamiques et gabarit testé :

| Famille | URL | Gabarit testé |
|---|---|---|
| Accueil | `/` | Hero, Produits, Services, Publics, Étapes, Réalisations, Comparaison, Dépôts, Conseils, FAQ, CTA, Footer |
| Catalogue | `/produits`, `/[univers]` ×6, `/[univers]/[...segments]` | `/produits`, `/acier`, `/inox/profiles`, `/acier/armatures-beton`, `/acier/armatures-beton/rond-a-beton-lamine-a-chaud` (TableauProduits : cartes < 768, tableau ≥ 768) |
| Fiche produit | `/p/[slug]` ×495 | slug courant + nom le plus long (63 caractères) |
| Devis | `/devis` | formulaire complet |
| Recherche | `/recherche` | composant client |
| Services | `/services`, `/services/[slug]` ×8 | index + `decoupe` |
| Dépôts | `/depots`, `/depots/[slug]` ×4 | index + `charleroi-mont-sur-marchienne` |
| Conseils | `/conseils`, `/conseils/[slug]` ×16 | index + `acier-corten-qu-est-ce-que-c-est` (tableau) |
| Aide | `/aide/[slug]` ×4 | `livraison-retrait` (tableau) |
| Espaces | `/pro`, `/pro/demande-de-compte`, `/pro/connexion`, `/compte/*`, `/panier` | `/pro`, `/pro/demande-de-compte`, `/compte/connexion`, `/panier` |
| Éditorial | `/contact`, `/faq`, `/realisations`, `/nouveautes`, `/documentation`, `/plan-du-site`, `/entreprise*`, `/a-propos`, légales | `/contact`, `/faq`, `/realisations`, `/nouveautes`, `/documentation`, `/plan-du-site`, `/entreprise`, `/mentions-legales` |
| 404 | toute URL inconnue | `/cette-page-n-existe-pas` |

Non testés individuellement : `/pro/connexion`, `/compte/inscription`, `/compte/mot-de-passe-oublie`
(même gabarit `PageEspace` que `/compte/connexion`), `/a-propos`, `/entreprise/certifications`,
`/entreprise/engagement-esg`, les autres dépôts, les 15 autres articles, les 7 autres services,
les 493 autres fiches, les autres catégories. Ils partagent les gabarits testés ; une différence
de contenu (texte plus long, image absente) resterait possible.

Composants partagés couverts par les gabarits ci-dessus : Nav (menu mobile, méga-menu desktop),
Footer, FilAriane, PageHeader, PageLegale, PageEspace, TableauProduits, GalerieProduit, Calculateur,
Recherche, DevisForm, FormulairePro, Marquee, Comparaison, cartes produits/services/dépôts.

États testés : défaut, page 404, formulaire valide/invalide (bouton désactivé), menu ouvert/fermé,
recherche avec résultats, filtre actif, libellé produit le plus long. Non testés : chargement,
erreur serveur, panier rempli (le panier n'a pas de logique), grand texte système.

## Matrice

Balayage de confirmation (balayage 3) : 30 gabarits × 11 largeurs. ✅ = mesuré, sans débordement,
sans erreur console ni réseau imprévue. Les cibles < 24 px restantes sont détaillées plus bas.

| Gabarit | 320 | 360 | 375 | 390 | 414 | 600 | 768 | 820 | 834 | 1024 | 1280 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Accueil | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| /produits, /acier, /inox/profiles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Catégorie ×2 (cartes / tableau) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fiche produit ×2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Devis, Recherche | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Services ×2, Dépôts ×2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Conseils ×2, Aide | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Espaces ×4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Éditorial ×8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 404 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Parcours : menu, recherche, filtre, devis | ✅ | — | ✅ | — | ✅ | — | — | — | — | — | — |
| Comparaison (capture) | ✅ | ✅ | ✅ | — | ✅ | — | — | — | — | — | ✅ |
| Menu ouvert, formulaire (capture) | ✅ | — | — | — | — | — | — | — | — | — | — |
| Tableau produits (capture) | — | — | — | — | — | — | ✅ | — | — | — | — |

## Défauts trouvés et état

| Priorité | Défaut | Où | Cause | Correction | Contrôle |
|---|---|---|---|---|---|
| P1 | Chevauchement de texte à 320 px, invisible au `scrollWidth` (masqué par `overflow-hidden`) | Comparaison, accueil | `grid-cols-3` et `p-5` sans préfixe : ~53 px utiles par cellule | Gabarit mobile `grid-cols-[0.95fr_1.25fr_1fr]`, `p-3`, icône au-dessus du texte, `break-words hyphens-auto` ; `sm:` restaure l'existant | R1 |
| P1 | Lien cassé (404) | `/services` → `/services/transformation` | slug inventé dans la page | cible de `lib/edito.ts` : `/services/soudure` | R3 |
| P2 | 37 à 46 cibles < 24 px par page, toutes largeurs | Footer (14 px), fils d'Ariane (13 px), plan du site (152), tableau (16-20 px), dépôts, nouveautés, fiche | liens texte sans hauteur | `.lien-tactile` (inline-flex, min 24×24 px), rendu inchangé | R2 |
| P3 | Liens soulignés dans le texte courant à 13-14 px (≤ 2 par page) | espaces, légales, panier | inline dans un paragraphe | conservé : exemption WCAG 2.5.8 pour les liens en ligne | — |
| P3 | « Espace pro » 20 px de haut en desktop ≥ 1024 | Nav | `hidden lg:block` sans padding | conservé : souris uniquement | — |
| P3 | Textes 11 px : `tag-stock`, `text-[11px]` (unités, compteurs) | catalogue, fiches | choix graphique (étiquettes mono) | conservé ; à revoir si retour terrain | — |
| P3 | « En stock » sur deux lignes dans le tableau à 768 px | TableauProduits | colonne étroite | conservé | — |
| Dette | Quatre miettes « Accueil » codées à la main hors `FilAriane` (sans JSON-LD) | PageHeader, PageLegale, dépôt, service | duplication | à unifier sur `FilAriane` | — |

P0 restants : 0. P1 restants : 0. P2 restants : 0. P3 : 4, documentés ci-dessus.

## Chiffres

| | Balayage 1 (avant) | Balayage 3 (après) |
|---|---|---|
| Mesures | 330 | 330 |
| Débordements horizontaux | 0 | 0 |
| Parcours mobiles | 15/18 (sonde mal ciblée) | 18/18 |
| 404 imprévus | 1 (`/services/transformation`) | 0 |
| Cibles < 24 px, max par page, mobile/tablette | 46 (plan du site : 152) | 2 |
| Cibles < 24 px, max par page, desktop | 67 | 3 |
| Textes < 12 px, total | 268 | 268 (inchangé, P3) |

## Relancer

```
npm run build && npm run start          # port 3000
python scripts/qa/balayage-responsive.py --urls gabarits.txt --interactif
python scripts/qa/balayage-responsive.py --urls gabarits.txt --widths 320,360,375,390,414   # si la mémoire manque
python scripts/qa/balayage-responsive.py --urls gabarits.txt --widths 600,768,820,834,1024,1280 --interactif
```

`gabarits.txt` : un chemin par ligne (la liste de ce rapport est reconstituable depuis l'inventaire).
Les résultats vont dans `%LOCALAPPDATA%\SiteAciersGrosjean\qa-responsive\`.
