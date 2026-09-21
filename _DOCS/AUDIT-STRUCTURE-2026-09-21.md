# Audit de structure — 21 septembre 2026

Audit du dossier complet : organisation, code Next.js, système de gouvernance, hygiène Git,
sécurité, automatisation. Trois analyses parallèles, constats vérifiés par lecture de fichier,
exécution de script ou commande Git. Rien n'a été modifié pendant l'audit.

Audit précédent : `_DOCS/AUDIT-2026-09-14.md` (poids des pages). Celui-ci porte sur le dispositif,
pas sur le rendu.

---

## 1. Verdict

Le dossier contient **deux systèmes superposés**, construits à trois jours d'intervalle.

Le premier — production des visuels 3D — **fonctionne réellement** : 455 fiches sur 477 en ligne,
un inventaire exact (506 lignes CSV = 506 images sur le disque), un carnet de leçons de 142 lignes,
un agent vérificateur qui rend de vrais verdicts, 20 commits datés, une reprise après coupure qui
marche. C'est un dispositif de production sérieux.

Le second — « Project OS / Engineering Quality », posé le 17/09 — **n'est branché sur rien**.
`CLAUDE.md` ne cite ni `.claude/rules/`, ni `memory/`, ni `project-state/`, ni `PROJECT_OS_LOOP.md`.
Il n'existe pas de `.claude/settings.json`, pas d'`@import`. Les règles qui affirment « prévaloir
sur toute formulation historique » ne sont chargées dans aucune session. Elles existent sur disque,
pas dans le contexte de l'agent.

Chiffre qui résume le déséquilibre : **3 433 lignes** de gouvernance Markdown
(dont 1 219 pour `ENGINEERING_QUALITY_ARCHITECTURE.md` et 774 pour l'audit associé)
contre **572 lignes** de journaux et conversations réunis — la trace de ce qui a réellement été fait.
Pour un site vitrine de 40 pages, sans backend, **sans aucun test applicatif**.

La faille principale n'est donc pas un bug : c'est que le système de contrôle et le travail réel
ne se touchent pas.

---

## 2. Carte du dossier

| Zone | Poids | Suivi par Git | État |
|---|---|---|---|
| `.git` | 80 Mo | — | 1 640 objets en vrac, jamais de `gc`, **synchronisé par OneDrive** |
| `_DEPOT/` | 252 Mo, 1 691 fichiers | non (ignoré) | jamais commité — correct. `deja-integre/` **vide** |
| `public/` | 77 Mo, 572 fichiers | oui | 58 Mo de PDF (un de 19,9 Mo), 19 Mo de WebP |
| `.claude/` + `.agents/` | 6,9 Mo | oui | **6,8 Mo de skills dupliqués à l'identique** |
| `_DOCS/` | 3,7 Mo | oui | inventaires, briefs, suivi 3D — la partie vivante |
| code (`app`, `components`, `lib`, `scripts`) | — | oui | 495 produits, 77 nœuds, 638 pages annoncées |
| **Total** | **422 Mo** | 874 fichiers suivis | 69 commits, 1 branche, **0 pull request** |

Organisation d'ensemble : la convention « dossiers `_MAJUSCULE` en français pour le propriétaire,
dossiers techniques en anglais pour le code » est claire et tient. Elle est le point fort de la
structure et doit être conservée.

---

## 3. Ce qui est solide — à ne pas casser

Vérifié par script, pas sur déclaration.

1. **Intégrité des données du catalogue** : 495 produits, 77 nœuds, 6 univers, zéro catégorie
   orpheline, zéro référence produit morte, zéro lien interne cassé (52 `href` dans `app/` et
   `components/`, 48 dans `lib/edito.ts`), zéro PDF manquant, 502 WebP référencés et tous présents,
   sitemap exactement aligné. C'est rare et c'est la vraie valeur du dépôt.
2. **Qualité TypeScript** : `strict: true`, **zéro `any`, zéro `@ts-ignore`**. Les 5
   `dangerouslySetInnerHTML` ne servent qu'à du JSON-LD sérialisé, sans entrée utilisateur.
3. **Séparation client / serveur** pensée et documentée là où elle a été traitée (`lib/menu.ts`,
   `lib/format.ts`, `Reveal` et `GalerieProduit` en CSS pur, `import type` dans `TableauProduits`).
4. **Accessibilité du tableau produits** : `caption` sr-only, `scope`, `aria-live`, `aria-pressed`.
   `prefers-reduced-motion` traité (`app/globals.css:128,187,207`).
5. **Aucun secret exposé.** Historique complet des 69 commits scanné (tokens GitHub, AWS, OpenAI,
   Stripe, Slack, Notion, clés privées) : zéro. `.mcp.json` est le fichier le mieux tenu du dépôt —
   un seul serveur, version épinglée, `--headless --isolated`, origines limitées à `localhost:3000`.
   `_DEPOT` n'a jamais été commité.
6. **La règle AUTO-SAVE / AUTO-COMMIT / AUTO-PUSH / DEPLOY** (`SYNC_POLICY.md`) est la seule règle
   du système appliquée par du code et non par de la prose : `synchro.ps1:71-73` bloque réellement
   le push automatique, et `project_os_check.py` vérifie que ce blocage est là. **C'est le modèle
   à généraliser au reste du système.**
7. **La discipline PROUVÉ / UNKNOWN** (`EXTENSION_DISCOVERY.md`, `TEST_STATUS.md` : « un test non
   exécuté ne constitue pas une preuve de réussite »). Refuser de cocher ce qui n'a pas tourné est
   la meilleure habitude du dispositif.
8. **Les règles de code de `CLAUDE.md`** (catalogue généré, interdiction d'importer `lib/catalogue.ts`
   depuis un composant client, contenu visible sans JS, `SITE_INDEXABLE`, pas de `npm install` dans
   OneDrive) : spécifiques, vérifiables, avec un effet mesurable sur le produit.
9. **`.claude/agents/verificateur-rendus.md`** : le meilleur artefact du dépôt. Contrôles chiffrés,
   séparation bloquant / mineur, format de rapport court. Il a produit de vrais verdicts.

---

## 4. Failles

### CRITIQUE

**C1 — `.gitignore:7` ne protège pas les fichiers d'environnement.**
La règle est `.env*.local`. Testé avec `git check-ignore` : `.env`, `.env.production`,
`.vercel/project.json`, `.claude/settings.local.json`, `secrets.txt` seraient **commités**.
Or `_OUTILS/SAUVEGARDER.cmd` déclenche `synchro.ps1:33` qui fait `git add -A` puis push, sans revue
de diff, vers un dépôt **public**. Une clé Vercel ou SMTP créée un jour part en ligne en un
double-clic. Le scan de secrets de la CI ne rattrape rien : 4 motifs seulement, et il ne tourne
jamais (voir C2).
→ Correction : 4 lignes dans `.gitignore`. Coût nul aujourd'hui, `git filter-repo` en urgence sinon.

**C2 — La CI n'a jamais tourné sur le chemin de production.**
`.github/workflows/quality.yml:3-5` : déclencheurs `pull_request` et `workflow_dispatch` seulement.
Le dépôt a 69 commits, une seule branche, **zéro PR, zéro merge**. Le flux réel est le push direct
sur `main`, qui déclenche le déploiement Vercel — sans que `npm run typecheck` ni `next build` aient
tourné. Le contenu du workflow est pourtant bon (`quality.yml:26-30`) : c'est le déclencheur qui est
mort. Et c'est **verrouillé par le projet lui-même** : `tests/test_project_os.py:118` et
`scripts/validation/project_os_check.py:87` interdisent explicitement d'ajouter un trigger `push`.
Pendant ce temps `project-state/TEST_STATUS.md` affirme « La CI exécutera typecheck et build dans
son environnement verrouillé ».

**C3 — OneDrive synchronise `.git`.**
Vérifié sur les attributs NTFS : `.git`, `.git/index`, `.git/HEAD`, `.git/config` portent tous
`ReparsePoint` — ce sont des placeholders OneDrive. Rien n'est cassé à ce jour (0 objet en
cloud-only, aucun fichier « copie en conflit »). Mais OneDrive peut verrouiller ou déshydrater
`index`, `HEAD` ou `objects/` pendant une opération Git, et la tâche planifiée tourne toutes les
2 h sans personne devant. C'est le mode de corruption classique d'un dépôt Git en dossier
synchronisé. GitHub est déjà la sauvegarde du code : OneDrive n'apporte rien sur `.git`.

**C4 — 22 redirections 301 pointent vers des pages qui n'existent pas.**
`lib/redirections.mjs`, vérifié par script contre les 28 routes statiques, les 77 nœuds du catalogue,
les 495 slugs produits et les 32 slugs éditoriaux. Destinations mortes, dont
`/toiture-bardage/panneau-tuile` (5 anciennes URL), `/conseils/rss.xml` (2), `/commande` (2),
`/acier/poutrelles/hem`, `/compte/profil`, `/compte/commandes`.
Résultat : chaîne 301 → 404, jus de lien perdu — exactement ce que le fichier dit vouloir éviter
(`lib/redirections.mjs:6-7`). C'est la raison d'être de la refonte.

**C5 — Aucune frontière d'erreur.**
`app/` n'a ni `not-found.tsx`, ni `error.tsx`, ni `loading.tsx`. Les 7 appels à `notFound()`
tombent sur la 404 par défaut de Next : « This page could not be found », en anglais, hors charte.
Sur un site qui hérite de 652 anciennes URL, la 404 est une page à trafic réel.

### IMPORTANT

**I6 — Le Project OS n'est chargé dans aucune session.** Voir §1. Tant que ce n'est pas câblé,
les 7 règles, les 6 fiches d'agent et les 159 Ko de `docs/architecture/` sont décoratifs.

**I7 — La boucle 3D autonome est instruite de pousser sur `main`.** La commande `/loop` de
`CLAUDE.md:64` fait lire `_DOCS/rendus-3d/avancement.md` en premier ; sa section « REPRENDRE ICI »
dit : « **Commit-push** dès que le build passe […] et pousser ». `SYNC_POLICY.md` interdit
AUTO-PUSH et `CLAUDE.md:75` exige un human gate. Le fichier opérationnel que la boucle lit
contredit la règle, sur le seul chemin qui déploie en production.

**I8 — Les permissions d'agents ne sont qu'un tableau Markdown.** `agent-permissions.md` accorde
`Bash` à quatre agents ; aucun `settings.json`, aucune deny-rule : `git push` et `rm` restent
techniquement disponibles. Le fichier l'admet lui-même (« le Markdown ne constitue pas à lui seul
un contrôle d'accès »). Pire, `CLAUDE.md:56` prescrit le contournement : « lancer un agent général
avec le contenu de `verificateur-rendus.md` comme consigne » — un agent général a tous les outils.
`_JOURNAL/2026-09-16.md` prouve que ce chemin a servi.
À l'inverse, `builder` est déclaré « écriture ciblée » **sans `Write` ni `Edit`** : sa seule voie
d'écriture est Bash, l'outil le moins contraignable. Le modèle de permissions est inversé.

**I9 — Deux mémoires parallèles, la gouvernée est vide.** `project-state/CURRENT_STATE.md` :
« aucun chantier d'implémentation métier ». Au même moment `_DOCS/rendus-3d/avancement.md` porte
22 fiches en attente, une quinzaine de défauts connus non corrigés, et `questions-en-attente.md`
40 questions produit ouvertes. Rien n'entre dans l'état gouverné.
Aggravant : `CURRENT_STATE.md` et `memory/ACTIVE_CONTEXT.md` écrivent « PROUVÉ : working tree
propre » alors que `git status` montre trois fichiers modifiés depuis le 17/09 — dont ces deux-là.
Le diff qui écrit la phrase la contredit.

**I10 — La synchro automatique ne fait plus rien depuis 4 jours.** `synchro.ps1:51-53` : si le
working tree est sale, la récupération est reportée. Or les fichiers sales sont des documents de
gouvernance modifiés à chaque séance — l'état sale est l'état normal. 18 des 41 lignes de
`synchro.log` disent « des modifications locales attendent une sauvegarde », dont les 5 dernières
en continu du 17/09 au 21/09. La tâche tourne (`LastTaskResult: 0`) mais dégénère en no-op.

**I11 — Le catalogue entier part dans le navigateur sur `/recherche`.**
`components/catalogue/Recherche.tsx:1` (`"use client"`) importe `lib/catalogue.ts` (304 Ko), qui
importe `site-actuel.json` (224 Ko) qu'une boucle à effet de bord (`lib/catalogue.ts:711-729`) rend
non élaguable : ~528 Ko de JS brut, 43 Ko gzip, + 495 itérations de fusion côté client. Le projet
interdit lui-même cette manœuvre à deux endroits (`lib/format.ts:4-5`, `lib/menu.ts:6-8`) et
`CLAUDE.md:18` la pose en règle. `/recherche` est lié 3 fois dans la navigation.

**I12 — Les deux formulaires n'ont aucun backend et confirment un envoi non vérifié.**
`DevisForm.tsx:36-40` et `FormulairePro.tsx:43-46` : `window.location.href = mailto:…` puis
`setSent(true)` immédiatement. L'écran de confirmation s'affiche même si aucun client mail ne
s'ouvre (webmail, mobile sans app configurée). Aucun enregistrement, aucun suivi des leads.

**I13 — Le site part en `noindex` par défaut.** `SITE_INDEXABLE` non défini ⇒
`robots: {index:false}` sur tout le site **et** `Disallow: /` (`app/layout.tsx:12,46`,
`app/robots.ts:6,10`), figés au build. Volontaire aujourd'hui, mais si la variable n'est pas posée
sur Vercel avant le build de mise en production, le site est invisible et il faut redéployer.

**I14 — Trois `as unknown as` sur les trois plus gros JSON** (`app/p/[slug]/page.tsx:26,38`,
`lib/catalogue.ts:711`) : 1,1 Mo de données castées sans validation. `strict: true` ne couvre rien
là. Si un script générateur Python change de schéma, le build passe et les 495 fiches cassent au
runtime.

**I15 — Aucun test applicatif, aucun ESLint.** `tests/` ne contient que 3 scripts de gouvernance.
Pas de test de composant, pas d'E2E malgré Playwright configuré. Pas de `.eslintrc`, pas de script
`lint` : `next build` ne lint rien. Et les 652 redirections ne sont vérifiées par aucun test.
Sur les tests Python existants, la substance réelle est minoritaire : `engineering_quality.py`
(503 lignes, vraie validation) et le contrôle d'intégrité des médias de `project_os_check.py:42-80`.
Le reste est de la vérification de présence de fichiers.
`tests/test_extensions.py:118-131` lit le `git status` du poste : **rouge en permanence en local**,
toujours vert en CI. Un test qui ne détecte rien là où il tourne et casse là où il ne garde rien.

**I16 — Aucun en-tête de sécurité.** `next.config.mjs` n'a pas de fonction `headers()` : pas de CSP,
X-Frame-Options, Referrer-Policy, HSTS, X-Content-Type-Options. `poweredByHeader` non désactivé.

**I17 — `next/image` neutralisé.** `GalerieProduit.tsx:44,58` passe `unoptimized`, seul usage de
`Image` du projet : la configuration AVIF/WebP de `next.config.mjs:8` ne sert à rien. La vignette
déclare `sizes="160px"` et télécharge le WebP 1 600 px (jusqu'à 188 Ko). L'image LCP est servie brute.

**I18 — Contraste insuffisant au survol.** `hover:text-jaune` sur fond blanc en 12 endroits
(`Nav.tsx:127,148`, `plan-du-site/page.tsx:22,49,64`, etc.) : `#FFD500` sur `#ffffff` = **1,4:1**,
seuil WCAG AA 4,5:1. Le lien devient illisible pendant le survol. (Dans `Footer.tsx`, sur fond
encre, aucun problème.)

**I19 — 6,8 Mo de skills dupliqués dans un dépôt public.** `.claude/skills/ui-ux-pro-max` et
`.agents/skills/ui-ux-pro-max` sont identiques au bit près (48 fichiers chacun, dont un CSV de
749 Ko et un JSON de 857 Ko) ; idem `frontend-design`. Justification : parité Claude Code / Codex.
Mais `EXTERNAL_CAPABILITIES.md` les réserve à « the future Website phase », non commencée.

### MINEUR

- **`_DEPOT/deja-integre/` est vide** (0 fichier dans les 8 sous-dossiers) alors que `CLAUDE.md:32`
  impose d'y déplacer chaque original après intégration. Règle jamais appliquée : la supprimer ou
  l'appliquer.
- **`_LISEZ-MOI.md` est faux sur le point le plus sensible** : il dit que la tâche automatique
  « envoie les sauvegardes déjà enregistrées » ; `synchro.ps1:72` fait l'inverse
  (« AUTO-PUSH DESACTIVE »). C'est le seul document écrit pour un non-développeur.
- **Trois skills projet mortes** : `discovery`, `project-audit`, `testing` n'ont pas de frontmatter
  YAML — le chargeur ne les voit pas. `project_os_check.py` vérifie leur existence et rend PASS.
  Un test vert y prouve la présence d'un fichier, pas une capacité.
- **Trois matrices de routage divergentes**, dont deux citent des agents inexistants
  (`react-next-reviewer`, `security-differential-reviewer`, `SD`, `BQ` — absents de `.claude/agents/`).
- **`precedence.md` ne tranche pas** : trois hiérarchies coexistent (6 niveaux, 7 niveaux, formule
  courte), le rang de `CLAUDE.md` lui-même n'est jamais fixé, et le critère d'arbitrage
  (« formulation historique moins stricte ») est un jugement, pas un ordre applicable.
- **La tolérance 3D annule `stop-conditions.md`** sans frontière définie : « intégration métier »
  n'est défini nulle part, alors que la boucle écrit dans `public/images/` et `lib/visuels-produits.json`.
- `docs/decisions/`, `docs/requirements/`, `docs/acceptance/` : **zéro contenu**, que des README.
  7 décisions structurantes sont empilées en vrac dans `CURRENT_STATE.md`.
  `HANDOFF_TEMPLATE.md` n'a jamais été instancié.
- `memory/ACTIVE_CONTEXT.md` fonde le projet sur **trois fichiers hors dépôt** (dans `Downloads/`),
  non versionnés, invisibles en session web, que `core.md` érige en « référence fonctionnelle ».
- **`.git` n'a jamais été compacté** : 1 640 objets en vrac, 75 Mio, pack de 341 Kio. Un `git gc`
  divisera le poids.
- `app/sitemap.ts:12,14` : `lastModified: new Date()` applique la date de build aux ~630 URL et
  signale à Google que tout a changé à chaque déploiement.
- Pas d'`opengraph-image` ni d'`openGraph.images` → aperçus de partage vides.
- Pas de lien d'évitement clavier ; `::-webkit-scrollbar{width:0}` (`globals.css:17`) supprime la
  barre de défilement ; `aria-expanded` sans `aria-controls` et pas de fermeture à Échap sur le
  méga-menu (`Nav.tsx:53-69`).
- Composant `Faq` identique rendu sur `/`, `/faq` et les 8 pages `/aide/*` → contenu dupliqué.
- Deux routes dynamiques sans `dynamicParams = false` (`services/[slug]`, `depots/[slug]`) alors
  que les cinq autres le posent : fonction serverless au lieu d'un 404 statique.
- Aucune mesure d'audience (zéro `gtag`/`GTM`/`fbq`) — cohérent avec la page cookies, mais
  c'est une décision à prendre avant la mise en production d'un site commercial.
- `_DOCS/catalogue-site-actuel/produits.csv` publie 501 prix TTC dans un CSV aspirable en un
  `git clone`. Ces prix sont déjà publics sur aciersgrosjean.be — à arbitrer avec l'entreprise,
  pas un incident.
- Les commits sont signés avec l'e-mail personnel, public et permanent sur GitHub.
- `_DOCS/rendus-3d/donnees-produits.csv` : 6 versions de ~700 Ko dans l'historique, fichier dérivé
  recommité à chaque vague.
- Incohérence interne de `avancement.md` : « questions 1 à 47 » à un endroit, « 40 questions » à
  l'autre.

---

## 5. Plan de renforcement

Ordonné par rapport effet / effort. Les cinq premiers verrouillent le dispositif ; les suivants
le rendent utile.

| # | Action | Effort | Pourquoi maintenant |
|---|---|---|---|
| 1 | Boucher `.gitignore` : `.env`, `.env.*`, `!.env.example`, `.vercel/`, `.claude/settings.local.json`, `*.log` | 5 min | Évite une fuite irréversible sur dépôt public |
| 2 | Sortir `.git` de OneDrive (déplacer le dossier hors OneDrive, ou exclure `.git`) + `git gc` | 30 min | Supprime le seul risque de perte totale du dépôt |
| 3 | Ouvrir la CI sur `push: branches: [main]`, et lever l'interdiction dans `test_project_os.py:118` et `project_os_check.py:87` | 20 min | Le seul chemin qui déploie doit être le seul chemin testé |
| 4 | Réparer les 22 redirections mortes (créer la cible ou rediriger vers le parent) | 2 h | Raison d'être de la refonte ; à faire avant la mise en production |
| 5 | Ajouter `app/not-found.tsx` et `app/error.tsx` en charte | 1 h | Page d'atterrissage de tout ce que les redirections ratent |
| 6 | Câbler le Project OS : `.claude/settings.json` + lecture de `CURRENT_STATE.md` et `precedence.md` dans « Début de session » de `CLAUDE.md` | 30 min | Sans ça, toute la gouvernance reste décorative |
| 7 | Transformer les permissions en contrôle technique : deny `Bash(git push:*)`, `Bash(rm:*)`, `Bash(npm install:*)` ; donner `Write`/`Edit` à `builder` ; supprimer le contournement de `CLAUDE.md:56` | 45 min | Le Markdown n'est pas un contrôle d'accès, le fichier de règles le dit |
| 8 | Sortir le catalogue du bundle de `/recherche` : index réduit calculé côté serveur, sur le modèle de `lib/menu.ts` | 2 h | ~500 Ko de JS en moins, et respect d'une règle déjà écrite |
| 9 | Brancher les deux formulaires sur un vrai endpoint, confirmation après réponse seulement | 3 h | Aujourd'hui, des demandes de devis peuvent se perdre sans que personne le sache |
| 10 | Corriger `synchro.ps1` : ne plus reporter le fetch quand seuls des documents de gouvernance sont sales (`:51-53`) ; distinguer les causes d'échec de push (`:77`) | 30 min | La synchro est en panne silencieuse depuis le 17/09 |
| 11 | Une source par contrat : archiver `ENGINEERING_QUALITY_ARCHITECTURE.md` et `..._AUDIT.md` en `SUPERSEDED`, garder `ROUTING` + `FINDINGS` + le `.py` ; fusionner les 3 hiérarchies de précédence en un seul tableau | 1 h | 2 000 lignes qu'aucun test ne maintient, citant des agents qui n'existent pas |
| 12 | Fusionner les deux mémoires : faire de `avancement.md` la source déclarée et y renvoyer depuis `CURRENT_STATE.md`, ou remonter les 40 questions et 22 fiches en attente dans `OPEN_QUESTIONS.md` / `BLOCKERS.md` | 1 h | Un état qui dit « aucun chantier » pendant qu'un chantier tourne ne sert à personne |
| 13 | Déduplication `ui-ux-pro-max` / `frontend-design` : un arbre source + une copie générée | 30 min | −3,4 Mo dans un dépôt public |
| 14 | `headers()` dans `next.config.mjs`, ESLint installé et lancé en CI, `git gc` | 1 h | Hygiène de base avant production |
| 15 | Réparer ou supprimer `tests/test_extensions.py:118-131` (rouge en permanence en local) | 10 min | Un test toujours rouge apprend à ignorer toute la suite |

**Principe directeur pour la suite** : le seul mécanisme de gouvernance qui tient dans ce dépôt est
celui qui est appliqué par du code (`synchro.ps1` bloque réellement le push). Chaque règle nouvelle
devrait être posée sous cette forme — un contrôle exécutable — plutôt qu'en paragraphe de Markdown.
Une règle qui n'est vérifiée par rien finit par être fausse sans que personne le voie, comme
`_DEPOT/deja-integre/` ou « PROUVÉ : working tree propre ».

---

## 6. Non vérifié

- `tsc --noEmit` et `next build` n'ont pas pu être exécutés : `node_modules` est absent, et
  `CLAUDE.md:25` interdit `npm install` dans ce dossier. Les constats TypeScript sont statiques.
- La protection effective de la branche `main` et l'historique réel des exécutions de la CI côté
  GitHub : le connecteur GitHub n'a pas pu se connecter pendant l'audit.
- Le rendu visuel des pages en navigateur n'a pas été inspecté : cet audit porte sur le dispositif.
