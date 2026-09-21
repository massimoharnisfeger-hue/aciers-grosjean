# Chantiers de renforcement — liste complète

Source : `_DOCS/AUDIT-STRUCTURE-2026-09-21.md` (21/09/2026).
Fichier de travail de la boucle de renforcement. Une tâche = une ligne. Une ligne se ferme sur une
**preuve exécutée**, jamais sur une impression.

États : `À FAIRE` · `EN COURS` · `FAIT` (+ date + preuve) · `BLOQUÉ` (+ raison) · `HUMAIN` (décision du propriétaire).

---

## But final

Ce dossier doit devenir la base sur laquelle sera construit un **ERP**. Le site est le banc d'essai :
ce qui n'est pas fiable ici le sera encore moins sur un logiciel de gestion.

Le but n'est donc pas « 46 corrections faites ». C'est : **le dossier attrape désormais tout seul les
46 erreurs de cet audit, et toute erreur future devient un contrôle permanent.** Un système qui
apprend, c'est un système dont le nombre de contrôles exécutables ne redescend jamais.

Ce qui apprend, c'est le dépôt — pas le modèle, qui repart de zéro à chaque session. D'où les six
mécanismes du LOT 0 : ils transforment la mémoire d'une séance en contrainte permanente.

---

## GRILLE 9/10 — la cible, traduite en conditions vérifiables

Demandé le 21/09 : amener les trois couches d'architecture à 9/10. Une note que l'agent s'attribue
lui-même n'est pas une condition d'arrêt — il lui suffirait de la décréter. Chaque point est donc
traduit ici en **condition que le dépôt vérifie tout seul**. La boucle s'arrête quand les seize
sortent vertes, pas quand quelqu'un trouve que c'est bien.

Notes de départ, audit du 21/09 : technique **7**, information **5**, gouvernance **3,5**.

### Couche technique du site — 7 → 9

| Code | Condition | Ligne qui la porte |
|---|---|---|
| T1 | Chaque JSON généré a un schéma déclaré, validé à la génération **et** au build. Zéro `as unknown as` dans le dépôt | D9 |
| T2 | Le comportement d'échec est défini : `not-found.tsx` et `error.tsx` existent, en français, et un contrôle le vérifie | D2 |
| T3 | La règle de séparation client/serveur est **exécutée** : un contrôle échoue si un fichier `"use client"` importe `lib/catalogue.ts` ou `lib/edito.ts` | D3 + **D16** |
| T4 | Tests de rendu réels : au moins un par famille de route (accueil, univers, catégorie, fiche, page légale, 404) + les 652 redirections | D15 + **D17** |
| T5 | Budget de poids JS par route déclaré et tenu automatiquement | **D18** |

### Couche information — 5 → 9

| Code | Condition | Ligne qui la porte |
|---|---|---|
| I1 | `_DOCS/INDEX.md` existe : un fait = une source déclarée, un générateur, des lecteurs | Z4 |
| I2 | Un contrôle vérifie que tout lien `.md → .md` du dépôt résout et que tout chemin cité dans l'index existe | Z4 |
| I3 | Un seul état : plus de doublon `memory/` ↔ `project-state/` ↔ `avancement.md` | Z5, C9, C10 |
| I4 | Zéro octet dupliqué : `ui-ux-pro-max` et `frontend-design` ont une seule source | C16 |
| I5 | L'état ne peut plus mentir : un contrôle échoue si le working tree a bougé et que l'état ne l'a pas suivi | Z5 |

### Couche gouvernance — 3,5 → 9

| Code | Condition | Ligne qui la porte |
|---|---|---|
| G1 | Les règles sont chargées au point d'entrée : `.claude/settings.json` existe et `CLAUDE.md` cite `precedence.md`, `CURRENT_STATE.md`, `ACTIVE_CONTEXT.md` | C1, C2 |
| G2 | Les permissions sont techniques, pas rédactionnelles : un contrôle vérifie que `agent-permissions.md` et `.claude/settings.json` disent la même chose | C1, C5 + **C17** |
| G3 | Une seule hiérarchie de précédence dans tout le dépôt | C6 |
| G4 | Zéro référence morte : aucun agent, skill ou document cité qui n'existe pas, vérifié par un contrôle permanent | C7, C8 + **C18** |
| G5 | Chaque document de `docs/architecture/` est soit cité par un contrôle, soit marqué `SUPERSEDED`. Un document que rien ne vérifie est du poids mort | C7 + **C19** |
| G6 | La boucle décrite est la boucle réelle : au moins un ADR par décision prise et un handoff rempli existent | Z3, C13 |

**Ce qui reste hors de portée de la boucle** : le 10ᵉ point de la couche technique dépend du backend
des formulaires (**H4**), et celui de la gouvernance dépend de la sortie de OneDrive (**H1**). 9/10
par couche est donc le maximum atteignable sans toi.

---

## REPRENDRE ICI

**État au 21/09/2026 — LOT Z TERMINÉ. 9 tâches fermées sur 60** (Z1 à Z8 + C10 absorbé).
8 décisions humaines en attente, 3 ADR à confirmer par le propriétaire.

**La machine qui apprend est en place.** Condition (a) de l'objectif final : atteinte.

Prochaine tâche : **B5** (ESLint) — **attention, contrainte réelle** : ajouter `eslint` aux
devDependencies sans régénérer `package-lock.json` casserait le `npm ci` de la CI. Or `npm install`
est interdit dans ce dossier (OneDrive, `CLAUDE.md:25`). L'installation doit se faire dans la copie
hors OneDrive de `_OUTILS/site-local.ps1`, puis `package.json` et `package-lock.json` doivent être
rapatriés ensemble. À traiter comme une seule modification atomique.
**Lot A terminé** : A1, A2, A3, A5 fermés ; A4 reste bloqué par **H1** (sortie de OneDrive).
**B1, B2, B3 fermés.**
Grille : **I1, I2, I3, I5 vertes**. Douze conditions restantes.

**CONDITION (c) ATTEINTE** : `81 controles - 0 echecs - 4.5 s`. Départ 35, cible 75, budget 60 s.

**Le gate est vivant** : `_OUTILS/SAUVEGARDER.cmd` installe les hooks avant chaque sauvegarde.
Le hook exercé directement sort en code 0 — les commits passent et sont protégés (secrets,
taille, 81 contrôles). La CI se déclenche désormais sur `push` vers `main`.
Ordre imposé : lot **Z** → A → B → C → D → E. Dans un lot, l'ordre des lignes.
Les tâches `HUMAIN` se sautent et se listent en fin d'itération.

**Compteur de contrôles : 82 (départ 35 le 21/09), socle dans `tests/socle.json`.**
Suite complète : **5,3 s, 0 échec** pour un budget déclaré de 60 s.
Cible de l'objectif final : **≥ 75** (35 + 40). Nouvelle cible ajoutée le 21/09 : les seize
conditions de la **GRILLE 9/10** vertes (six lignes créées pour ça — C17 à C19, D16 à D18).

Dernier build vérifié : *jamais depuis l'audit*.
Working tree : 3 fichiers modifiés depuis le 17/09 non commités (`docs/architecture/SYNC_POLICY.md`,
`memory/ACTIVE_CONTEXT.md`, `project-state/CURRENT_STATE.md`) — voir E5.

---

## LOT Z — La machine qui apprend

**Se construit en premier.** Sans elle, les lots A à E sont 46 corrections ponctuelles qui se
re-dégraderont. Avec elle, chaque correction laisse derrière elle un contrôle qui empêche le retour
du défaut. C'est la seule partie du projet dont dépend la suite, ERP compris.

| ID | Action | Preuve | État |
|---|---|---|---|
| Z1 | **Registre des contrôles.** Créer `tests/lancer.py` : découvre et exécute tous les contrôles de `tests/`, affiche `N contrôles · M échecs · T secondes` et sort en code ≠ 0 au premier échec. Invariant inscrit en tête du fichier : **N ne diminue jamais** | `python tests/lancer.py` affiche le compte et le temps ; N ≥ nombre de contrôles existants avant la tâche | **FAIT 21/09** · `35 controles - 1 echecs - 0.3 s`, socle initialisé à 35 (`tests/socle.json`), code de sortie 1 sur échec, et invariant prouvé : socle forcé à 36 → `SOCLE ROMPU : 36 controles atteints le 2026-09-20, 35 aujourd'hui` + sortie 1 |
| Z2 | **Carnet de leçons global.** Créer `_DOCS/LECONS.md`. Le carnet 3D **n'est pas fusionné** : périmètres différents, décision tracée en **ADR-0002** (la ligne prévoyait l'inverse ; l'écart est déclaré, pas effacé). Une leçon = symptôme observé · cause réelle · **ID du contrôle qui l'attrape** · date. Une leçon sans ID de contrôle est incomplète et ne compte pas | un contrôle vérifie que chaque leçon cite un ID existant dans `tests/` ; il échoue si on ajoute une leçon sans contrôle | **FAIT 21/09** · `_DOCS/LECONS.md` + `tests/test_socle.py` (6 contrôles). Rouge d'abord (`_DOCS/LECONS.md` absent), puis vert. Registre : `41 controles - 1 echecs - 0.6 s`, socle 35 → 41. Trois leçons inscrites, L-003 née du rouge de ce chantier même. Le carnet 3D reste séparé (périmètre fabrication d'images), lien posé dans la notice |
| Z3 | **Journal des décisions.** `docs/decisions/NNNN-titre.md`, **au gabarit à 8 champs qui existait déjà dans `docs/decisions/README.md`** (aucun format concurrent créé — voir L-004). Règle inscrite dans `CLAUDE.md:12` : une question qui a un ADR ne se repose jamais | un contrôle vérifie que chaque décision citée dans l'état renvoie à un fichier existant | **FAIT 21/09** · `tests/test_decisions.py` (5 contrôles). Rouge d'abord (`docs/decisions/` vide), puis vert 5/5. Registre : `46 controles - 1 echecs - 2.5 s`, socle 41 → 46. Deux ADR écrits : ADR-0001 (grille 9/10) et ADR-0002 (carnet 3D séparé) |
| Z4 | **Index des sources — « les dossiers qui communiquent ».** Créer `_DOCS/INDEX.md` : pour chaque type de fait (prix, descriptions, visuels, redirections, documents PDF, état 3D, règles, décisions, leçons), **quel fichier fait autorité**, quel script le génère, qui le lit. Un fait = une source, jamais deux | un contrôle vérifie que tous les chemins cités dans `INDEX.md` existent, et que tout lien `.md → .md` du dépôt résout | **FAIT 21/09** · `_DOCS/INDEX.md` (23 faits, 38 chemins) + `tests/test_index.py` (6 contrôles), vert 6/6. Registre : `52 controles - 1 echecs - 1.5 s`, socle 46 → 52. **Réserve mesurée** : le contrôle des liens `.md → .md` inspecte 0 lien interne aujourd'hui (le dépôt cite entre accents graves) — c'est un garde tourné vers l'avenir, pas une preuve ; voir L-005. Les 3 doubles sources restantes sont nommées dans l'index et portées par Z5, C9, C10, C16 |
| Z5 | **État unique.** Une seule section « REPRENDRE ICI » pour tout le projet, dans `project-state/CURRENT_STATE.md`, qui renvoie aux avancements par piste (3D, renforcement, plus tard ERP). Supprime le doublon `memory/` ↔ `project-state/` (voir C9, C10) | un contrôle échoue si le working tree a bougé et que l'état date de plus de 7 jours | **FAIT 21/09** · `project-state/CURRENT_STATE.md` devient la source unique (« REPRENDRE ICI » à 3 pistes, ligne `ÉTAT AU:`), `memory/ACTIVE_CONTEXT.md` perd ses sections d'état. `tests/test_etat.py`, 5 contrôles, vert. Registre : `57 controles - 1 echecs - 1.5 s`, socle 52 → 57. **Écart de méthode assumé** : la fraîcheur se mesure contre `_JOURNAL/` (7 entrées datées), **pas** contre le `git status` du poste — un contrôle couplé à l'état local reproduirait B3. Conditions **I3** et **I5** vertes ; **C10 absorbé** |
| Z6 | **Le gate.** `python tests/lancer.py` branché en `pre-commit` (A2) **et** en CI sur `push main` (B1). Rien ne part avec un contrôle rouge | un commit avec un contrôle volontairement cassé est refusé localement | **FAIT 21/09** · `scripts/hooks/pre-commit` + `scripts/installer-hooks.ps1` + étape « Registre des controles » dans `quality.yml`. `tests/test_gate.py`, 5 contrôles, vert. Registre : `62 controles - 1 echecs - 1.6 s`, socle 57 → 62. Hook exercé directement, sans créer de commit : **sortie 1 aujourd'hui** (B3 rouge). **Branchement sur `SAUVEGARDER.cmd` volontairement différé à A2** pour ne pas livrer un bouton de sauvegarde inopérant : **ADR-0003**. Le déclencheur CI reste `pull_request` seul jusqu'à B1 |
| Z7 | **Budget de performance.** La suite complète doit tenir **sous 60 s en local**. Au-delà, un contrôle lent est isolé dans un groupe `lent` lancé seulement en CI. Une suite lente est une suite qu'on saute | `python tests/lancer.py` affiche `T < 60 s` et échoue si le budget est dépassé | **FAIT 21/09** · `budget_secondes: 60` déclaré dans `tests/socle.json`, appliqué par `tests/lancer.py`. Prouvé sur dossier témoin avec budget 0 → `BUDGET DEPASSE` + sortie 1. Un second contrôle vérifie que relever le socle n'efface pas le budget. Mesure réelle : **2,3 s pour 66 contrôles** |
| Z8 | **Règle d'apprentissage**, inscrite dans `CLAUDE.md` : toute erreur constatée — par moi, par un agent, par toi — donne lieu à un contrôle **écrit avant la correction**, dans la même itération. Un défaut vu **une** fois, plus deux. Et : aucune correction n'est déclarée faite sans que son contrôle soit passé du rouge au vert | la règle est dans `CLAUDE.md` et un contrôle vérifie sa présence | **FAIT 21/09** · section « Quand quelque chose casse » ajoutée à `CLAUDE.md`, le seul fichier chargé automatiquement à chaque session. Contrôle `test_la_regle_d_apprentissage_est_dans_claude_md`. Registre : `66 controles - 1 echecs - 2.3 s`, socle 62 → 66 |

**Méthode imposée pour les lots A à E, une fois le LOT Z en place** : pour chaque ligne, écrire
d'abord le contrôle qui reproduit le défaut et le voir **échouer**, puis corriger, puis le voir
**passer**. Le contrôle reste pour toujours. À la fin, les 46 erreurs de l'audit ne peuvent plus
revenir sans que quelque chose devienne rouge.

---

## LOT A — Sécurité et sauvegarde

Ce lot passe avant tout : il empêche une fuite irréversible sur un dépôt public.

| ID | Action | Preuve | État |
|---|---|---|---|
| A1 | `.gitignore` : ajouter `.env`, `.env.*`, `!.env.example`, `.vercel/`, `.claude/settings.local.json`, `*.log`, `*.pem`, `*.key` | `git check-ignore -v .env .env.production .vercel/project.json .claude/settings.local.json` renvoie une règle pour les 4 | **FAIT 21/09** · contrôle écrit d'abord et vu **rouge** sur 7 chemins (`.env`, `.env.production`, `.env.development`, `.vercel/project.json`, `.claude/settings.local.json`, `*.pem`, `*.key`), puis `.gitignore` corrigé, puis **vert**. Preuve : `.gitignore:13:.env`, `:14:.env.*`, `:16:.vercel/`, `:17:.claude/settings.local.json`. Registre : `69 controles - 1 echecs - 2.7 s`, socle 66 → 69. Contre-épreuve incluse : le code doit rester versionné. Leçon **L-007** |
| A2 | Compléter le hook `pre-commit` créé en Z6 : refuser tout fichier > 5 Mo, tout `.env`, et les motifs de secrets. **Puis brancher `scripts/installer-hooks.ps1` dans `_OUTILS/SAUVEGARDER.cmd`** — différé depuis Z6 par **ADR-0003**, à faire seulement une fois **B3** corrigé et la suite verte, sinon le bouton de sauvegarde devient inopérant | exercer le hook directement sur un `.env` bidon et un fichier > 5 Mo → sortie ≠ 0, sans créer de commit ; puis supprimer les fichiers témoins | **FAIT 21/09 (durcissement)** · `scripts/hooks/verifier-depot.py` : refuse `.env*` sauf `.env.example`, > 5 Mo, et 9 motifs de secrets. 7 contrôles écrits d'abord et vus **rouges**, puis verts 10/10. Logique extraite du hook pour être exerçable sans commit (**L-008**). Mesure sur les 874 fichiers suivis : **2 problèmes réels, 0 faux positif** — 2 PDF de 19,9 et 9,6 Mo, qui alimentent **E3**. Registre : `76 controles - 1 echecs - 4.1 s`, socle 69 → 76. **Le branchement sur `SAUVEGARDER.cmd` reste à faire : ligne A5, après B3 (ADR-0003)** |
| A3 | Élargir le scan de secrets de `.github/workflows/quality.yml:52` : ajouter Vercel, Notion (`ntn_`), Airtable (`pat[A-Za-z0-9]{14}`), OpenAI (`sk-proj-`), Google (`AIza`), Slack (`xox[baprs]-`) | le job passe sur le dépôt actuel (aucun faux positif) | **FAIT 21/09** · le `git grep` inline de `quality.yml:52` (4 motifs) est remplacé par un appel au **même** vérificateur que le hook, en mode `--secrets-seulement` (9 motifs). Une seule liste pour les deux portes — **L-009**. 3 contrôles, 2 rouges d'abord, puis verts 13/13. Étape CI simulée à l'identique sur les 874 fichiers suivis : **code 0, aucun faux positif**. Registre : `79 controles - 1 echecs - 3.0 s`, socle 76 → 79 |
| A5 | **Brancher le gate sur le bouton du propriétaire** : `_OUTILS/SAUVEGARDER.cmd` appelle `scripts/installer-hooks.ps1` avant la synchro. Différé depuis Z6 par **ADR-0003** : à faire **seulement une fois B3 corrigé et la suite verte**, sinon le bouton de sauvegarde devient inopérant | un contrôle vérifie que `SAUVEGARDER.cmd` appelle l'installateur ; `python tests/lancer.py` sort en 0 | **FAIT 21/09** · débloqué par B3. `_OUTILS/SAUVEGARDER.cmd` pose les hooks avant de sauvegarder. Condition d'ADR-0003 remplie : suite verte d'abord. Hook exercé directement, sans commit : **code 0**. Registre : `81 controles - 0 echecs - 4.5 s`, socle 80 → 81 |
| A4 | `git gc --prune=now` — **uniquement après H1** (jamais sur un `.git` synchronisé par OneDrive) | `git count-objects -vH` : objets en vrac ≈ 0, taille divisée | BLOQUÉ par H1 |

---

## LOT B — Le chemin de production

Aujourd'hui, le seul chemin qui déploie (`push main` → Vercel) est le seul qui n'est pas testé.

| ID | Action | Preuve | État |
|---|---|---|---|
| B1 | `.github/workflows/quality.yml:3-5` : ajouter `push:` / `branches: [main]` aux déclencheurs | le fichier contient bien le trigger, et B2 passe | **FAIT 21/09** · `push: branches: [main]` ajouté. Traité avec B2, modification atomique. Registre : `80 controles - 1 echecs - 2.9 s`, socle 79 → 80 |
| B2 | Lever l'interdiction qui bloque B1 : `tests/test_project_os.py:118` (`assertNotIn("  push:", ci)`) et `scripts/validation/project_os_check.py:87`. Remplacer par l'inverse : **exiger** le trigger `push` sur `main` | `python tests/test_project_os.py` et `python scripts/validation/project_os_check.py` → OK / PASS | **FAIT 21/09** · rouge d'abord (`CI does not run on the production path`), puis vert : `Ran 15 tests OK` et `PROJECT OS CHECK: PASS`. `test_ci_is_check_only` scindé en deux — un contrôle exige le déclencheur, l'autre garde l'interdiction réelle de publier + `contents: read`. Le défaut était **verrouillé par des tests verts** : leçon **L-010** |
| B3 | `tests/test_extensions.py:118-131` : le test lit le `git status` du poste, il est rouge en permanence en local et toujours vert en CI. Le restreindre aux fichiers suivis, ou le supprimer | `python tests/test_extensions.py` → OK sur ce poste, working tree sale inclus | **FAIT 21/09** · la liste blanche figée de 36 lignes (instantané du 17/09) est supprimée ; la garde contre les suppressions de fichiers suivis est conservée, avec réserve déclarée (vacante en CI). Mesure : 26 chemins inspectés en local. **La suite passe à 0 échec pour la première fois** : `80 controles - 0 echecs`. Leçon **L-011** |
| B4 | Épingler `actions/checkout@v4` et `actions/setup-node@v4` par SHA de commit (`quality.yml:15,18`), comme `EXTERNAL_CAPABILITIES.md` l'exige déjà pour les skills | le workflow référence deux SHA de 40 caractères | **FAIT 21/09** · SHA **résolus**, pas devinés : `git ls-remote --tags` → checkout `11d5960a326750d5838078e36cf38b85af677262`, setup-node `49933ea5288caeca8642d1e84afbd3f7d6820020` (tags légers, donc commits). Contrôle rouge d'abord, puis vert : `Ran 16 tests OK`. Registre : `82 controles - 0 echecs - 5.3 s`, socle 81 → 82. Leçon **L-012** |
| B5 | ESLint : `npm i -D eslint eslint-config-next`, `.eslintrc.json` (`extends: next/core-web-vitals`), script `"lint": "next lint"`, étape CI après Typecheck | `npm run lint` passe dans le build hors OneDrive | **BLOQUÉ 21/09 — STOP** · ESLint est déclaré (eslint 8.57.1 + eslint-config-next 15.5.25, alignés sur Next 15.5.25), `.eslintrc.json` créé, lock synchronisé, 5 contrôles verts. **Mais `npm run lint` n'a jamais été observé en succès** : `node_modules` de la copie hors OneDrive est cassé (`EBUSY` sur `next-swc.win32-x64-msvc.node`, fichier verrouillé par l'un des 49 processus Node actifs). **Et une étape `npm run lint` a été ajoutée en CI (`quality.yml:39`) par un autre écrivain que cette boucle** — si le lint échoue, chaque push sur `main` devient rouge. Décision humaine requise avant de continuer |
| B6 | Ajouter au workflow une étape qui vérifie les redirections et les liens internes (script de D1/D15) | l'étape échoue si une cible de redirection n'existe pas | À FAIRE |

---

## LOT C — Câbler la gouvernance

Le cœur du problème : 3 433 lignes de règles que rien ne charge et que rien ne vérifie.

| ID | Action | Preuve | État |
|---|---|---|---|
| C1 | Créer `.claude/settings.json` : `deny` sur `Bash(git push:*)`, `Bash(git commit:*)`, `Bash(rm:*)`, `Bash(npm install:*)`, `Bash(git reset --hard:*)` | le fichier est valide en JSON et une tentative de `git push` par un agent est refusée | À FAIRE |
| C2 | `CLAUDE.md`, section « Début de session » : ajouter la lecture de `.claude/rules/precedence.md`, `project-state/CURRENT_STATE.md` et `memory/ACTIVE_CONTEXT.md` | `CLAUDE.md` cite les trois chemins ; un test dans `project_os_check.py` le vérifie | À FAIRE |
| C3 | Supprimer `CLAUDE.md:56` (« lancer un agent général avec le contenu de `verificateur-rendus.md` ») : un agent général a tous les outils, c'est le contournement des permissions | la phrase n'existe plus ; `grep -n "agent général" CLAUDE.md` est vide | À FAIRE |
| C4 | `_DOCS/rendus-3d/avancement.md`, section « REPRENDRE ICI » : retirer l'ordre « **Commit-push** dès que le build passe […] et pousser ». Il contredit `SYNC_POLICY.md` et `CLAUDE.md:75` sur le seul chemin qui déploie | `grep -ni "push" _DOCS/rendus-3d/avancement.md` ne renvoie plus d'ordre d'exécution | À FAIRE |
| C5 | `.claude/agents/builder.md` + `agent-permissions.md` : donner `Write` et `Edit` à `builder`, restreindre son `Bash` par motif. Aujourd'hui il est « écriture ciblée » sans outil d'écriture, donc il écrit par Bash — l'outil le moins contraignable | le frontmatter contient `Write`, `Edit` ; la table est à jour | À FAIRE |
| C6 | Fusionner les 3 hiérarchies de précédence (`precedence.md` 6 niveaux, `external-capabilities.md` 7 niveaux, `ACTIVE_CONTEXT.md` formule courte) en **un seul tableau** dans `precedence.md`, que les autres citent. Y fixer le rang de `CLAUDE.md` et définir « intégration métier » | un seul fichier définit l'ordre ; les deux autres y renvoient par lien | À FAIRE |
| C7 | Archiver `docs/architecture/ENGINEERING_QUALITY_ARCHITECTURE.md` (1 219 l.) et `..._AUDIT.md` (774 l.) avec un en-tête `SUPERSEDED`. Garder `ROUTING` + `FINDINGS` + `engineering_quality.py` comme source unique. Purger des matrices les agents inexistants (`react-next-reviewer`, `security-differential-reviewer`, `SD`, `BQ`) | `grep -rn "react-next-reviewer\|security-differential-reviewer" docs/` est vide hors fichiers archivés | À FAIRE |
| C8 | `.claude/skills/discovery`, `project-audit`, `testing` : ajouter un frontmatter YAML (`name`, `description`) — sans lui le chargeur ne les voit pas — **ou** les supprimer et les retirer de la liste `REQUIRED` de `project_os_check.py` | les skills apparaissent dans la liste de la session, ou n'existent plus nulle part | À FAIRE |
| C9 | Fusionner les deux mémoires : faire de `_DOCS/rendus-3d/avancement.md` la source déclarée de l'état 3D, y renvoyer depuis `project-state/CURRENT_STATE.md`, et remonter dans `memory/OPEN_QUESTIONS.md` / `BLOCKERS.md` les 22 fiches sans visuel et les 40 questions produit | `CURRENT_STATE.md` ne dit plus « aucun chantier » pendant qu'un chantier tourne | À FAIRE |
| C10 | Retirer « PROUVÉ : working tree propre » de `CURRENT_STATE.md` et `memory/ACTIVE_CONTEXT.md`, ou le remplacer par une ligne datée et vérifiable | `git status` et la phrase disent la même chose | **FAIT 21/09, absorbé par Z5** · l'affirmation est supprimée des deux fichiers et désormais **interdite par un contrôle** (`tests/test_etat.py::EtatTests::test_l_etat_ne_se_prononce_pas_sur_le_working_tree`), pas seulement effacée. Ce contrôle a d'abord attrapé la note qui expliquait la suppression : leçon **L-006** |
| C11 | `_LISEZ-MOI.md`, section « Synchronisation automatique » : la tâche « envoie les sauvegardes déjà enregistrées » est **faux**, `synchro.ps1:72` désactive l'auto-push. Corriger — c'est le seul document écrit pour un non-développeur | la phrase décrit le comportement réel du script | À FAIRE |
| C12 | `memory/ACTIVE_CONTEXT.md` fonde le projet sur 3 fichiers de `C:/Users/massi/Downloads/`, non versionnés, invisibles en session web, que `core.md` érige en « référence fonctionnelle ». Les copier dans `_DOCS/reference/` ou retirer la dépendance | les chemins cités existent dans le dépôt, ou ne sont plus cités | À FAIRE |
| C13 | Sortir les 7 décisions structurantes empilées dans `CURRENT_STATE.md` vers `docs/decisions/` (un fichier par décision, format court : contexte, décision, conséquence, date) | `docs/decisions/` n'est plus vide ; `CURRENT_STATE.md` y renvoie | À FAIRE |
| C14 | `_OUTILS/synchro.ps1:51-53` : ne plus reporter le `fetch` quand seuls des documents de gouvernance sont modifiés (la synchro est un no-op depuis le 17/09). Et `:77` : distinguer échec d'authentification / divergence / branche protégée | `synchro.log` montre une récupération réussie avec un working tree sale | À FAIRE |
| C15 | `_DEPOT/deja-integre/` est vide depuis le début alors que `CLAUDE.md:32` impose d'y déplacer chaque original intégré. Appliquer la règle ou la supprimer | le dossier reflète la règle, ou la règle n'existe plus | À FAIRE |
| C16 | Dédupliquer `ui-ux-pro-max` et `frontend-design` (6,8 Mo identiques au bit près dans `.claude/skills/` et `.agents/skills/`, dépôt public) : un arbre source + une copie générée par script | `diff -rq` reste vide après régénération ; le dépôt perd ~3,4 Mo | À FAIRE |
| C17 | **Contrôle de cohérence des permissions** (grille **G2**) : un contrôle qui compare le tableau de `.claude/rules/agent-permissions.md`, les frontmatters de `.claude/agents/*.md` et les règles de `.claude/settings.json`, et échoue à la moindre divergence | le contrôle devient rouge si on ajoute un outil dans un frontmatter sans l'ajouter au tableau | À FAIRE |
| C18 | **Contrôle « zéro référence morte »** (grille **G4**) : un contrôle qui extrait tout nom d'agent, de skill et tout chemin de fichier cité dans `CLAUDE.md`, `.claude/rules/*.md` et `docs/architecture/*.md`, et vérifie qu'ils existent | le contrôle est rouge aujourd'hui sur `react-next-reviewer`, `security-differential-reviewer`, `SD`, `BQ` ; vert après C7 | À FAIRE |
| C19 | **Poids mort interdit** (grille **G5**) : un contrôle qui exige que chaque fichier de `docs/architecture/` soit soit cité par un contrôle de `tests/`, soit marqué `SUPERSEDED` en tête. Un document que rien ne vérifie ne gouverne rien | le contrôle nomme les fichiers orphelins ; vert quand chacun est cité ou archivé | À FAIRE |

---

## LOT D — Qualité du site, visible par le visiteur

| ID | Action | Preuve | État |
|---|---|---|---|
| D1 | Réparer les 22 redirections 301 qui pointent vers des pages inexistantes (`lib/redirections.mjs`) : `/toiture-bardage/panneau-tuile` (5 sources), `/conseils/rss.xml` (2), `/commande` (2), `/toiture-bardage/toles-profilees/feutre-anti-condensation` (2), `/acier/poutrelles/hem`, `/acier/toles/tole-electrozinguee`, `/acier/toles/tole-decapee`, `/aluminium/profiles/carre-plein`, `/documentation/toiture-bardage`, `/livraison-retrait`, `/compte/profil`, `/compte/commandes`, `/compte/listes`, `/compte/recemment-vus`, `/toiture-bardage/panneaux-isoles/ttack-toiture-plate`. Cibles ambiguës → **H3** | script de vérification : 0 cible morte sur les 652 redirections | À FAIRE |
| D2 | Créer `app/not-found.tsx` et `app/error.tsx` en charte, en français, avec recherche + liens catalogue et dépôts. Aujourd'hui les 7 `notFound()` tombent sur « This page could not be found » | les deux fichiers existent et le build les prend ; une URL inexistante rend la page en charte | À FAIRE |
| D3 | Sortir le catalogue du bundle de `/recherche` : `components/catalogue/Recherche.tsx:1` est `"use client"` et importe `lib/catalogue.ts` (304 Ko + `site-actuel.json` 224 Ko, non élaguable à cause de `lib/catalogue.ts:711-729`). Construire un index réduit côté serveur (slug, nom, chemin, prix, clé normalisée) sur le modèle de `lib/menu.ts` et le passer en props | le bundle de `/recherche` perd ~500 Ko de JS brut ; `CLAUDE.md:18` est respecté | À FAIRE |
| D4 | Brancher `DevisForm.tsx:36-40` et `FormulairePro.tsx:43-46` sur un vrai endpoint. Aujourd'hui : `mailto:` puis `setSent(true)` immédiat — la confirmation s'affiche même si rien n'est parti. Choix du service → **H4** | un envoi de test arrive réellement ; la confirmation n'apparaît qu'après réponse du serveur | À FAIRE |
| D5 | Ajouter `headers()` dans `next.config.mjs` : CSP, `X-Frame-Options`, `Referrer-Policy`, `X-Content-Type-Options`, HSTS. Et `poweredByHeader: false` | `curl -I` sur la préproduction montre les en-têtes | À FAIRE |
| D6 | Retirer `unoptimized` de `components/catalogue/GalerieProduit.tsx:44,58` — seul usage de `next/image` du projet, donc la config AVIF/WebP de `next.config.mjs:8` ne sert à rien. La vignette déclare `sizes="160px"` et télécharge le WebP 1 600 px | l'onglet réseau montre une vignette servie en ~160 px | À FAIRE |
| D7 | Contraste : `hover:text-jaune` sur fond blanc = **1,4:1** (seuil WCAG AA 4,5:1) en 12 endroits — `Nav.tsx:127,148`, `plan-du-site/page.tsx:22,49,64`, `depots/[slug]/page.tsx:155,190`, `entreprise/certifications/page.tsx:109`, `nouveautes/page.tsx:33`, `PageEspace.tsx:46`, `PageLegale.tsx:70`. Remplacer par un survol encre + soulignement. Ne pas toucher au `Footer` (fond encre, correct) | contraste mesuré ≥ 4,5:1 sur les 12 | À FAIRE |
| D8 | Ajouter `export const dynamicParams = false` à `app/services/[slug]/page.tsx` et `app/depots/[slug]/page.tsx` — les cinq autres routes dynamiques le posent déjà | les deux routes rendent un 404 statique au lieu d'une fonction serverless | À FAIRE |
| D9 | Remplacer les 3 `as unknown as` (`app/p/[slug]/page.tsx:26,38`, `lib/catalogue.ts:711`) par une validation de schéma au build : 1,1 Mo de JSON castés sans contrôle, un changement de schéma côté Python casse les 495 fiches au runtime sans que le build bronche | un JSON volontairement malformé fait échouer le build, pas le runtime | À FAIRE |
| D10 | `app/sitemap.ts:12,14` : `lastModified: new Date()` met la date de build sur les ~630 URL et dit à Google que tout a changé à chaque déploiement. Utiliser la date réelle du contenu | deux builds successifs sans changement de contenu produisent le même `lastModified` | À FAIRE |
| D11 | Ajouter `app/opengraph-image.tsx` (ou un fichier statique) et `openGraph.images` dans `app/layout.tsx:59-65` : aujourd'hui les aperçus de partage sont vides | un partage de test affiche une image | À FAIRE |
| D12 | Accessibilité clavier : lien d'évitement vers le contenu principal ; retirer `::-webkit-scrollbar{width:0}` (`app/globals.css:17`) ; ajouter `aria-controls` et la fermeture à Échap sur le méga-menu (`Nav.tsx:53-69`) | navigation au clavier complète sur l'accueil et une fiche produit | À FAIRE |
| D13 | Le composant `Faq` (6 Q/R identiques, `lib/content.ts:112-119`) est rendu sur `/`, `/faq` et les 8 pages `/aide/*` → contenu dupliqué sur 10 pages. Varier par page ou ne le garder que sur `/faq` | le même bloc n'apparaît plus sur 10 pages | À FAIRE |
| D14 | Retirer `keywords` de `app/layout.tsx:47-58` (ignoré par Google depuis 2009) | la balise n'est plus émise | À FAIRE |
| D15 | Écrire le test qui manque : vérifier les 652 redirections, les liens internes, les PDF et les WebP référencés. L'audit l'a fait par script — le figer dans `tests/` et le brancher en CI (B6) | `python tests/test_liens.py` échoue si on casse volontairement une cible | À FAIRE |
| D16 | **Contrôle de séparation client/serveur** (grille **T3**) : un contrôle qui échoue si un fichier `"use client"` importe `lib/catalogue.ts` ou `lib/edito.ts`, directement ou en chaîne. La règle existe déjà dans `CLAUDE.md:18`, `lib/format.ts:4-5` et `lib/menu.ts:6-8` — elle n'est simplement appliquée par rien | le contrôle est rouge aujourd'hui sur `components/catalogue/Recherche.tsx` ; vert après D3 | À FAIRE |
| D17 | **Tests de rendu par famille de route** (grille **T4**) : un test par famille — accueil, univers, catégorie, fiche produit, page légale, 404 — qui vérifie que la page se construit et contient ses éléments obligatoires (titre, `h1`, fil d'Ariane, metadata) | `python tests/lancer.py` compte 6 contrôles de plus ; casser un `generateMetadata` rend l'un d'eux rouge | À FAIRE |
| D18 | **Budget de poids par route** (grille **T5**) : déclarer un seuil de JS par route dans un fichier de budget, et un contrôle qui lit la sortie de build et échoue au dépassement | le contrôle est rouge aujourd'hui sur `/recherche` (~528 Ko) ; vert après D3 | À FAIRE |

---

## LOT E — Dette et propreté

| ID | Action | Preuve | État |
|---|---|---|---|
| E1 | `_DOCS/rendus-3d/donnees-produits.csv` : fichier dérivé recommité à chaque vague, 6 versions de ~700 Ko dans l'historique. L'ignorer et le régénérer, ou assumer et documenter | le fichier n'alourdit plus chaque commit | À FAIRE |
| E2 | Les commits sont signés avec l'e-mail personnel, public et permanent sur GitHub. Basculer sur l'e-mail de redirection GitHub (`…@users.noreply.github.com`) | `git config --local user.email` pointe sur l'adresse noreply | À FAIRE |
| E3 | `public/documents/ag-lattonedil-ttack-2023-manuel-technique-fr.pdf` fait 19,9 Mo (58 Mo de PDF au total). Compresser les 4 plus gros | les 4 PDF passent sous 5 Mo sans perte de lisibilité | À FAIRE |
| E4 | `_DOCS/rendus-3d/avancement.md` dit « questions 1 à 47 » à un endroit et « 40 questions » à l'autre. Trancher sur le contenu réel de `questions-en-attente.md` | les deux chiffres concordent avec le fichier | À FAIRE |
| E5 | Commiter les 3 fichiers en attente depuis le 17/09 et écrire la section de journal manquante (`CLAUDE.md:73` l'impose et elle n'existe pas). **Commit uniquement sur demande humaine** | `git status` propre après validation du propriétaire | À FAIRE |

---

## DÉCISIONS HUMAINES EN ATTENTE

Aucune ne se tranche sans le propriétaire. La boucle les saute et les rappelle en fin d'itération.

| ID | Décision | Pourquoi ça bloque |
|---|---|---|
| H1 | **FERMÉE le 21/09 (ADR-0005, `tests/test_emplacement.py`).** ~~Sortir le dossier (ou au moins `.git`) de OneDrive.** `.git`, `index`, `HEAD`, `config` sont des placeholders OneDrive (`ReparsePoint` vérifié). Rien n'est cassé aujourd'hui, mais c'est le mode de corruption classique d'un dépôt Git, et la tâche tourne toutes les 2 h sans personne devant | Débloque A4. GitHub est déjà la sauvegarde du code : OneDrive n'apporte rien sur `.git` |
| H2 | Poser `SITE_INDEXABLE=oui` sur Vercel avant la mise en production, et activer la protection de la branche `main` | Sans la variable, le site est en `noindex` + `Disallow: /`, figés au build : il faut redéployer pour corriger |
| H3 | Cibles des redirections ambiguës : créer une vraie page `/toiture-bardage/panneau-tuile` (5 anciennes URL) ou rediriger vers le parent ? Idem `/commande`, `/livraison-retrait`, les 4 pages `/compte/*` | Bloque la moitié de D1. Ne pas inventer une cible |
| H4 | **FERMÉE le 21/09 (ADR-0006, `app/api/devis/route.ts`, P8).** SMTP Microsoft 365 de l'entreprise, secrets sur Vercel, secours `mailto:`. ~~Service d'envoi des formulaires : route handler + SMTP de l'entreprise, ou service tiers (Resend, Formspree) ? Et vers quelle adresse ? | Bloque D4. Aujourd'hui des demandes de devis peuvent se perdre sans trace |
| H5 | Mesure d'audience : oui ou non ? Aucun `gtag`/`GTM`/`fbq` aujourd'hui, cohérent avec la page cookies, mais c'est un choix à assumer avant production | À trancher avant la mise en ligne, pas après |
| H6 | `_DOCS/catalogue-site-actuel/produits.csv` publie 501 prix TTC dans un CSV aspirable en un `git clone`, sur un dépôt public. Déjà publics sur aciersgrosjean.be, mais pas sous cette forme | À arbitrer avec l'entreprise, ce n'est pas un incident technique |
| H7 | Les 40 questions produit de `_DOCS/rendus-3d/questions-en-attente.md` et les 22 fiches sans visuel attendent des réponses depuis le 16/09 | Bloque la fin de la production 3D (455/477) |
| H8 | Le **rapport final au propriétaire**, promis le 16/09 à 0 h 20 (« ce qui manque / en place / à mettre en place »), n'a jamais été rendu | Le point 2 du « REPRENDRE ICI » de `avancement.md` est ouvert depuis 5 jours |

---

## HORS PÉRIMÈTRE DE CETTE BOUCLE

La production des visuels 3D (`CLAUDE.md` section Visuels 3D, `_DOCS/rendus-3d/avancement.md`) est
une piste séparée avec sa propre boucle. Ne pas la mélanger : elle rend des images, celle-ci rend
un dispositif fiable. Les deux se croisent seulement sur C4 (l'ordre de push à retirer) et H7/H8.

---

## Règle de fermeture d'une ligne

Une ligne passe à `FAIT` quand, et seulement quand :
1. la modification est appliquée ;
2. la commande de la colonne **Preuve** a été exécutée et sa sortie est conforme ;
3. la sortie est recopiée en une ligne dans la colonne État, avec la date ;
4. `powershell -File _OUTILS/site-local.ps1 -Mode verifier` passe si la ligne touche au code du site.

Sinon la ligne est `BLOQUÉ` avec la raison écrite. Une ligne n'est jamais fermée sur une impression,
un « ça devrait marcher » ou un build non lancé — c'est exactement ce qui a produit
« PROUVÉ : working tree propre » dans un fichier modifié.
