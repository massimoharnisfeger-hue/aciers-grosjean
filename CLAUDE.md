# Site Aciers Grosjean — règles pour Claude

Refonte du site d'Aciers Grosjean (négoce d'acier, Wallonie). Next.js 15 (App Router), React 18, Tailwind 3, TypeScript, 638 pages statiques.
Préproduction : https://aciers-grosjean.vercel.app (protégée par Vercel Authentication). Le site réel reste https://www.aciersgrosjean.be.
Chaque push sur `main` déclenche un déploiement Vercel (projet `aciers-grosjean`).

Répondre en français, simplement : le propriétaire du projet n'est pas développeur.

## Début de session
1. Lire `_LISEZ-MOI.md`, le dernier fichier de `_JOURNAL/` et la dernière conversation de `_CONVERSATIONS/`.
2. Récupérer les nouveautés : `git pull --ff-only` (sur le PC : `powershell -File _OUTILS/synchro.ps1`).
3. Sur le PC : regarder `_DEPOT/` (nouveaux fichiers à intégrer ?). Ce dossier n'existe pas dans les sessions web.

## Règles de code
- `lib/catalogue.ts` est **généré** par `scripts/generer-catalogue.py`. Toute modification à la main doit être reportée dans le générateur.
- Prix, poids, longueurs, finitions, descriptions et PDF sont les **données réelles du site actuel** : `scripts/inventaire/` (explorer → analyser → integrer) produit `lib/site-actuel.json`, `lib/descriptions-site-actuel.json`, `lib/documents.json` et `public/documents/`, fusionnés au chargement en bas de `lib/catalogue.ts`. Ne pas les éditer à la main : relancer `integrer.py`.
- Prix affichés HTVA (TVAC = TTC du site actuel). Le supplément de découpe n'a pas de montant connu : ne pas en inventer.
- Un composant `"use client"` n'importe jamais `lib/catalogue.ts` ni `lib/edito.ts` : tout le catalogue partirait dans le JavaScript du navigateur. Calculer les données dans la page serveur et les passer en props (exemples : `lib/menu.ts`, `lib/format.ts`).
- Le contenu doit être visible sans JavaScript : aucune animation JS qui part de `opacity: 0`. Utiliser `components/fx/Reveal.tsx` (CSS) ou les classes `.apparait` / `.flotte` de `app/globals.css`.
- Liens d'appel : `lienTel()` de `lib/content.ts`.
- Indexation Google bloquée tant que la variable Vercel `SITE_INDEXABLE` ne vaut pas `oui` (`app/layout.tsx`, `app/robots.ts`). Ne pas l'activer sans accord explicite : doublon avec aciersgrosjean.be.
- Ne jamais inventer de coordonnées, prix, certifications ou avis clients.

## Vérifier avant d'envoyer
- Sur le PC, **ne jamais lancer `npm install` dans ce dossier** : il est synchronisé par OneDrive (des dizaines de milliers de fichiers, verrous pendant l'installation).
  `powershell -File _OUTILS/site-local.ps1 -Mode verifier` copie le code dans `%LOCALAPPDATA%\SiteAciersGrosjean\build`, installe, puis lance `tsc` et `next build`.
- Dans une session web : `npm ci && npm run typecheck && npm run build`.

## Images
Dépôt : `_DEPOT/images/<lot>/`, lots décrits dans `_DOCS/BESOINS-IMAGES.md`.
Intégration : WebP qualité ~80, 2400 px de large au maximum, moins de 200 Ko, nom `slug-en-minuscules.webp`, rangé dans `public/images/<lot>/`, affiché avec `next/image` et un `alt` descriptif.
Déplacer ensuite l'original dans `_DEPOT/deja-integre/<lot>/` et le noter dans le journal.

## Visuels 3D des fiches produits
Brief : `_DOCS/BRIEF-RENDUS-3D.md` (ordre des familles, périmètre de 477 fiches).
**Mode automatique**, à la demande du propriétaire (14/09/2026) : enchaîner les familles sans attendre son accord.

- **Par famille :** rendu test → autocontrôle strict (forme conforme à la famille, cotes lisibles sans chevauchement ni débordement, textes identiques aux données sourcées, fond blanc propre) → corriger jusqu'à ce que le test passe → série → contrôle de **chaque** image → **vérification indépendante** → intégration sur le site → vérification du build → commit et push → famille suivante.
- **Informer sans attendre :** envoyer au propriétaire le rendu test puis la planche contact de chaque famille. S'il répond, appliquer ses corrections avant d'aller plus loin.
- **Seul motif d'arrêt :** une donnée à afficher manque ou se contredit. Demander, ne jamais inventer.
- **Reprise :** tenir l'avancement dans `_DOCS/rendus-3d/avancement.md` ; chaque itération reprend là où la précédente s'est arrêtée. Lancer Blender en processus d'arrière-plan : les rendus continuent même si la séance est en pause.
- **Rangement et noms des images (obligatoire) :**
  - Atelier (`%LOCALAPPDATA%\SiteAciersGrosjean\rendu3d\`) : essais, comparaisons et brouillons dans `essais/`, jamais dans `final/`. `final/` ne contient que les rendus de production.
  - Sur le site, après la vérification « CONFORME » : `public/images/produits/<univers>/<catégorie>/`, calqué sur l'adresse de la catégorie (ex. `public/images/produits/acier/poutrelles/ipe/`). Dans chaque dossier : `<slug>-caracteristiques.webp` (une par fiche) et `studio-<famille>.webp` (une par catégorie). Les photos de mise en situation du propriétaire, déposées dans `_DEPOT/images/situation/<catégorie>/`, y entrent sous `situation-<famille>.webp`.
  - Inventaire : `_DOCS/rendus-3d/inventaire-visuels.csv` (slug, catégorie, fichier, type, verdict, date), mis à jour à chaque intégration.
- **Carnet de leçons (obligatoire) :** lire `_DOCS/rendus-3d/lecons.md` au début de **chaque** itération, avant de toucher au code. Le compléter après chaque famille et après chaque correction du propriétaire, en suivant les règles d'écriture en tête du fichier.
  - Un réglage validé (matière, lumière, cadrage, échantillons) devient un préréglage réutilisable dans le code : ne pas le re-régler pour la famille suivante.
  - Un défaut vu deux fois devient un contrôle automatique qui tourne sur toutes les images, sans inspection manuelle.
  - Avant de lancer une série, estimer sa durée d'après les temps réellement mesurés dans le carnet.
- **Vérification indépendante (obligatoire) :** à la fin de chaque série, **avant** l'intégration, lancer l'agent `verificateur-rendus` (`.claude/agents/`, modèle Opus) avec le nom de la famille. Pas pendant les rendus : il ne tourne qu'à ce moment-là.
  - Si l'agent n'apparaît pas dans la séance (fichier créé après son lancement), lancer un agent général avec le contenu de `.claude/agents/verificateur-rendus.md` comme consigne.
  - Verdict « À CORRIGER » : corriger chaque défaut bloquant, puis relancer la vérification sur les images refaites jusqu'au verdict « CONFORME ». Les défauts mineurs sont corrigés si c'est rapide, sinon notés dans l'avancement.
  - Défaut récurrent : l'ajouter au carnet de leçons et en faire un contrôle automatique. Envoyer au propriétaire le verdict avec la planche contact.
- **Modèle et limites d'usage :** Claude ne peut pas changer de modèle lui-même. À la limite d'usage, Claude Code (≥ 2.1.234) attend la réinitialisation et reprend seul : la production ralentit mais ne s'arrête pas. Au premier lancement, rappeler une seule fois au propriétaire :
  1. fermer navigateurs et autres fenêtres Claude Code (15 Go de RAM, souvent presque pleine) ;
  2. brancher le PC et désactiver la mise en veille ;
  3. pour éviter les attentes : activer les crédits d'usage (`/usage-credits`, avec un plafond) ; ou, au message « limite atteinte » de Fable, taper `/model` et choisir **Opus 5**, le plus puissant après Fable.
- **Commande de lancement** (boucle à rythme libre) :
  `/loop Continue la production automatique des visuels 3D selon CLAUDE.md (section Visuels 3D) : lis _DOCS/rendus-3d/lecons.md puis _DOCS/rendus-3d/avancement.md, fais l'étape suivante, mets à jour l'avancement et, si tu as appris quelque chose, le carnet de leçons. Quand les 477 fiches sont intégrées, vérifiées et poussées, arrête la boucle.`
- Pendant la journée, si le propriétaire doit utiliser le PC : limiter Blender à 4 cœurs (`-t 4`).

## Fin de session (obligatoire)
1. `_JOURNAL/AAAA-MM-JJ.md` : ajouter une section (ce qui a changé, pourquoi, fichiers). Créer le fichier du jour s'il n'existe pas.
2. `_CONVERSATIONS/AAAA-MM-JJ_sujet-court.md` : demande, constats, décisions, fait, reste à faire, lien de session.
3. Vérifier, puis commit en français clair et push (sur le PC : `_OUTILS/synchro.ps1 -Mode sauvegarder -Message "..."`).

Le dépôt GitHub est public : rien de confidentiel dans le code, le journal ou les conversations.
