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
Brief : `_DOCS/BRIEF-RENDUS-3D.md`. Une famille à la fois : rendu test → **attendre l'accord du propriétaire** → série → planche contact → accord. Jamais de nouvelle famille sans accord.

Claude ne peut ni changer de modèle ni fermer des programmes : c'est au propriétaire de le faire. **Le lui rappeler au bon moment, sans attendre qu'il y pense :**
- **Avant de lancer une série** (plusieurs heures de rendu), lui demander de :
  1. fermer navigateurs et autres fenêtres Claude Code (15 Go de RAM, souvent presque pleine) ;
  2. brancher le PC et désactiver la mise en veille ;
  3. taper `/model` et choisir **Sonnet 5** (la surveillance n'a pas besoin de plus) ;
  4. lancer la surveillance :
     `/loop 45m Surveille la série de rendus Blender en cours (scripts/rendu-3d, dossier %LOCALAPPDATA%\SiteAciersGrosjean\rendu3d) : nombre d'images faites et restantes, durée moyenne, erreurs. Relance les rendus plantés. Contrôle chaque nouvelle image (forme, cotes lisibles sans chevauchement, textes conformes aux données sourcées) et mets de côté celles qui posent problème, avec la raison. Ne commence jamais une nouvelle famille sans mon accord. Quand la série est terminée : planche contact de la famille, envoie-la-moi, puis arrête la boucle.`
- **Quand la planche contact est validée**, avant la famille suivante : lui demander de repasser sur **Fable** (`/model`, version la plus récente) pour la modélisation et les rendus test.
- Pendant la journée, s'il doit utiliser le PC : proposer de limiter Blender à 4 cœurs (`-t 4`).

## Fin de session (obligatoire)
1. `_JOURNAL/AAAA-MM-JJ.md` : ajouter une section (ce qui a changé, pourquoi, fichiers). Créer le fichier du jour s'il n'existe pas.
2. `_CONVERSATIONS/AAAA-MM-JJ_sujet-court.md` : demande, constats, décisions, fait, reste à faire, lien de session.
3. Vérifier, puis commit en français clair et push (sur le PC : `_OUTILS/synchro.ps1 -Mode sauvegarder -Message "..."`).

Le dépôt GitHub est public : rien de confidentiel dans le code, le journal ou les conversations.
