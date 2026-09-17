# Engineering Quality Architecture

**Statut : INTERNAL FOUNDATION IMPLEMENTED — external integration deferred**
**Date : 2026-09-17**
**Nature : conception et fondation interne, aucune intégration externe**

Ce document transforme l'audit comparatif en architecture de gouvernance et
référence le socle interne implémenté en Phase 1. Il ne crée aucun nouvel
agent, skill, MCP ou dépendance externe. Il ne modifie pas le site, les données
métier, les dépendances applicatives ou le déploiement.

Les marqueurs utilisés sont :

- `EXISTING` : présent dans le dépôt et vérifié ;
- `DECIDED` : décision d'architecture prise sur la base des preuves ;
- `TARGET` : état visé, à construire dans une phase ultérieure ;
- `DEFERRED` : volontairement reporté ;
- `OPEN` / `UNRESOLVED` : impossible à fermer avec les preuves disponibles ;
- `PROPOSED` : recommandation soumise à validation humaine.

## 1. Périmètre et autorité

### EXISTING

- Le Project OS est l'autorité opérationnelle du dépôt.
- `orchestrator` route les tâches et applique les STOP.
- `requirements-architect` analyse les besoins, dépendances et critères sans
  inventer de règle métier.
- `builder` implémente un périmètre approuvé avec impact analysis et rollback.
- `tester-reviewer` vérifie tests, régressions, erreurs, périmètre et sécurité
  de base.
- `data-guardian` garde la provenance et l'intégrité des données, médias, PDF
  et fichiers générés.
- `verificateur-rendus` reste indépendant et spécialisé dans les rendus 3D.
- Les rules `.claude/rules/` placent sécurité/STOP, human gates et Project OS
  au-dessus des instructions de skills externes.
- Le dépôt contient un site Next.js existant, pas encore l'ERP métier complet.

### DECIDED

Une capacité Engineering Quality ne peut jamais :

- changer la hiérarchie des règles ;
- convertir une guidance en autorité métier ;
- bypasser un STOP ou un human gate ;
- décider seule d'une migration, d'une donnée sensible, d'un paiement,
  d'une permission ou d'une release ;
- écrire, auto-corriger, committer, pousser ou déployer sans autorisation
  distincte et preuve de re-review.

### TARGET

Une couche de revue ciblée sera ajoutée autour des agents existants, avec un
contrat de finding et un routage par risque. Le centre de décision restera
`orchestrator`.

### DEFERRED

Les agents spécialisés séparés, la baseline lint/tests, l'extraction des
skills externes et toute modification du code applicatif sont reportés. Les
modes ciblés internes, le contrat et le routing de la Phase 1 sont désormais
implémentés sans élargir les permissions.

## 2. Résolution des questions ouvertes

Les questions ci-dessous reprennent les questions exactes de l'audit. Une
question marquée `UNRESOLVED` reste une condition avant intégration ; elle
n'est pas fermée artificiellement.

### Q1

**QUESTION**
Quel SHA propre au chemin `plugins/pr-review-toolkit` Anthropic doit être
retenu pour une intégration reproductible ?

**EVIDENCE**
Le HEAD observé de `anthropics/claude-code` est
`3deb821cb71ccfaaf2ffa9935e977df314ce5cd5`. Le plugin indique `1.0.0`, mais
le dernier commit propre à son sous-chemin n'a pas été établi séparément.

**DECISION**
`UNRESOLVED`.

**JUSTIFICATION**
Un HEAD de dépôt ne prouve pas la provenance exacte d'un sous-répertoire. Il
faut un SHA de contenu, un commit de chemin vérifiable ou un snapshot hashé.

**IMPACT**
Le plugin Anthropic reste `DEFERRED`. Aucun agent ne le route, aucune skill
commune ne le référence et aucune installation n'est autorisée tant que la
provenance n'est pas reproductible.

### Q2

**QUESTION**
La parité runtime Codex/Claude Code est-elle obligatoire pour chaque revue,
ou une capacité Claude-native est-elle acceptable ?

**EVIDENCE**
Le PR Review Toolkit est Claude-native et utilise `Task`. La guidance Vercel
est textuelle et potentiellement portable. Compound annonce plusieurs hôtes,
mais cette compatibilité n'a pas été prouvée dans ce dépôt.

**DECISION**
La parité n'est pas obligatoire pour chaque outil externe. Elle est obligatoire
pour tout contrat ou composant appartenant au Project OS et annoncé comme
commun à Codex et Claude Code. Un outil Claude-only doit être explicitement
déclaré comme tel.

**JUSTIFICATION**
Cette séparation évite de transformer une compatibilité annoncée ou textuelle
en preuve de découverte runtime.

**IMPACT**
Les contrats internes seront portables. Les adaptateurs runtime déclareront
leur environnement. Les probes Codex et Claude Code resteront séparées ; un
outil non prouvé dans un environnement reste `UNKNOWN` dans cet environnement.

### Q3

**QUESTION**
Quelle licence distincte s'applique exactement au plugin Trail of Bits
`differential-review` ?

**EVIDENCE**
Le manifest du plugin ne déclare pas de licence propre. Le dépôt source
expose une licence CC BY-SA 4.0 à la racine.

**DECISION**
`UNRESOLVED`. Toute copie, vendorisation ou redistribution est interdite tant
que la licence applicable au plugin n'est pas confirmée par une revue humaine.

**JUSTIFICATION**
La licence racine ne permet pas d'inférer automatiquement la licence de
chaque sous-plugin.

**IMPACT**
Trail of Bits reste `DEFERRED`. La fonction de revue n'est pas disponible dans
le dépôt et ne peut pas être considérée comme un composant de sécurité actuel.

### Q4

**QUESTION**
Les revues cross-model sont-elles autorisées, sur quels types de données et
vers quelles destinations ?

**EVIDENCE**
Compound documente une route pouvant envoyer du contenu hors machine. Le
Project OS impose une protection des données, un egress deny-by-default et un
human gate pour les opérations sensibles.

**DECISION**
Dans le projet, cross-model et egress externe sont `DENY` par défaut. Aucun
type de donnée ni aucune destination n'est pré-approuvé. Une exception future
exige classification, destination, portée, durée, responsable et human gate
explicitement tracés.

**JUSTIFICATION**
La présence d'une option d'un outil n'est pas un consentement à transmettre
des données commerciales ou sensibles.

**IMPACT**
Les reviewers sont locaux et report-only par défaut. Une tentative d'egress
non autorisée déclenche `STOP`. Les outils externes ne peuvent pas activer eux-
mêmes une route cross-model.

### Q5

**QUESTION**
Quel framework de lint et de tests doit être choisi pour le dépôt Next.js
actuel, sans modifier le code métier ?

**EVIDENCE**
`package.json` expose `typecheck`, `build`, `dev` et `start`. Aucun fichier de
configuration ESLint, Vitest, Jest, Playwright ou Cypress n'a été établi dans
l'audit.

**DECISION**
`UNRESOLVED`. Le choix est reporté à une baseline locale dédiée, avec impact
analysis, comparaison des options et human gate si les dépendances ou la CI
sont modifiées.

**JUSTIFICATION**
Les preuves actuelles ne permettent pas de sélectionner honnêtement un
framework sans inventer une contrainte de projet.

**IMPACT**
`typecheck` et `build` restent les preuves disponibles. Aucun reviewer ne
peut les présenter comme une couverture complète. Aucune dépendance n'est
ajoutée dans cette phase.

### Q6

**QUESTION**
Quelles règles Vercel sont compatibles avec Next.js `^15.5.25` et React
`^18.3.1` ?

**EVIDENCE**
La skill Vercel contient une guidance React/Next et certaines recommandations
peuvent dépendre de versions plus récentes. Aucune matrice règle par règle
n'a été établie.

**DECISION**
`UNRESOLVED` pour la compatibilité détaillée. Une règle non vérifiée contre les
versions du dépôt est informative uniquement ; elle ne peut pas bloquer ni
provoquer une correction.

**JUSTIFICATION**
La nature de guidance de la source ne prouve pas son applicabilité universelle
au dépôt actuel.

**IMPACT**
Le futur mode React/Next doit charger les règles après un contrôle de version.
Les findings doivent mentionner la règle source et le niveau de confiance.

### Q7

**QUESTION**
À partir de quel niveau un finding `MEDIUM` bloque-t-il une phase ou une
release ?

**EVIDENCE**
Le Project OS bloque déjà les risques critiques, les tests critiques, les
opérations sensibles et les human gates, sans blocage global déclaré pour
`MEDIUM`.

**DECISION**
Un `MEDIUM` ne bloque pas globalement une phase isolée. Il devient bloquant
lorsqu'il touche une exigence d'acceptation, la sécurité, les données, la
production, une régression ou un rollback non prouvé. Sinon, correction
planifiée ou acceptation documentée obligatoire avant release.

**JUSTIFICATION**
Le contexte et le blast radius comptent davantage que la sévérité seule.

**IMPACT**
L'agrégateur conserve le contexte et le blocker effectif. Le
`tester-reviewer` peut rendre `FIX`. Une acceptation concernant sécurité,
données, finances ou production exige un human gate.

### Q8

**QUESTION**
Où les rapports détaillés et artefacts de revue doivent-ils être conservés
sans gonfler la mémoire active ?

**EVIDENCE**
Le Project OS sépare état courant, mémoire active et documentation. Les
workflows audités produisent des artefacts de run mais aucun répertoire
Engineering Quality commun n'existe actuellement.

**DECISION**
`TARGET` : `docs/quality/runs/<run-id>/` contiendra les rapports détaillés et
preuves versionnables. `project-state/` ou `memory/` ne conserveront qu'un
résumé, le statut et le lien. Les artefacts temporaires browser resteront dans
un emplacement temporaire dédié.

**JUSTIFICATION**
Ce découplage limite la relecture de tout l'historique et conserve la
traçabilité.

**IMPACT**
Un run reçoit un identifiant et un scope. Les agents ne peuvent écrire que
dans l'artefact autorisé, jamais dans le code par effet secondaire. La création
de cette structure est reportée.

### Q9

**QUESTION**
Les fichiers d'extension non suivis actuellement font-ils partie du scope de
la future revue, ou leur commit doit-il être traité séparément ?

**EVIDENCE**
Le working tree contient des fichiers et changements d'extensions issus de la
phase précédente. Le Project OS exige un scope explicite et aucun commit
automatique.

**DECISION**
Les fichiers non suivis sont hors scope par défaut d'une revue applicative.
Ils doivent être snapshotés et traités dans un scope séparé avant tout commit.
Une revue ne peut les inclure que si les fichiers autorisés le déclarent.

**JUSTIFICATION**
Inclure silencieusement les fichiers non suivis fausserait le diff et la
baseline.

**IMPACT**
`DISCOVER` distingue suivis et non suivis. L'orchestrator arrête la tâche si
un fichier hors scope est touché. Les preuves de commit restent séparées.

### Q10

**QUESTION**
Qui valide les exceptions aux règles de permissions, à l'egress et aux human
gates ?

**EVIDENCE**
Le Project OS exige une validation humaine, mais le dépôt ne nomme pas une
personne ou un rôle permanent.

**DECISION**
Le validateur est l'humain explicitement désigné dans le gate de la tâche.
L'identité permanente est `UNRESOLVED` et ne sera pas inventée.

**JUSTIFICATION**
Le contrôle nécessaire est une approbation traçable, pas une auto-approbation
par un agent ou un outil.

**IMPACT**
Sans validateur identifiable, l'action reste `STOP`. Chaque exception doit
contenir action, raison, risque, fichiers, diff, tests, rollback, décision,
date et trace.

### Q11

**QUESTION**
Quel est le mécanisme de rollback accepté pour une correction automatique
locale, si une telle correction est un jour autorisée ?

**EVIDENCE**
Le Project OS exige un rollback raisonnable et interdit l'auto-push. Compound
expose `apply:local` et Anthropic documente des workflows plus larges.

**DECISION**
Politique actuelle : `NO AUTO-FIX`. Le mécanisme futur exact est `UNRESOLVED`.
La cible minimale devra isoler l'action, conserver un snapshot pré-action,
produire un diff, exécuter les tests, re-revoir puis attendre le human gate.

**JUSTIFICATION**
Il n'existe pas encore de workflow d'isolation/restauration implémenté dans
le dépôt ; déclarer le rollback opérationnel serait infondé.

**IMPACT**
Les reviewers sont report-only. `FIX` est une action distincte et autorisée
explicitement. Toute auto-correction non autorisée produit `STOP`.

### Q12

**QUESTION**
Quels critères mesurables permettront de séparer un agent spécialisé d'un
simple mode du `tester-reviewer` ?

**EVIDENCE**
Le projet ne possède pas encore de runs Engineering Quality mesurés. Les
agents existants couvrent déjà la revue, les tests, les données et la
gouvernance.

**DECISION**
`UNRESOLVED` pour un seuil numérique. Aucun nouvel agent ne sera créé avant un
pilote sur au moins trois changements représentatifs mesurant contexte, durée,
findings dupliqués, conflits, responsabilités non couvertes et blocages
manqués.

**JUSTIFICATION**
Le nombre d'agents ne constitue pas une preuve de qualité. Une séparation
nécessite une responsabilité durable, un contrat distinct et un gain mesuré.

**IMPACT**
Les responsabilités commencent comme modes ciblés autour des agents existants.
La création d'un agent exige une décision d'architecture séparée et n'est pas
autorisée par ce document.

## 2 bis. Décisions finales sur les 7 questions

Cette section est l'autorité actuelle pour les sept questions encore ouvertes.
La section 2 conserve l'analyse initiale et ses limites ; elle ne doit pas être
interprétée comme une décision plus récente que cette section.

### Q1 — QUESTION

Quel SHA propre au sous-chemin du PR Review Toolkit Anthropic doit être retenu
pour une intégration reproductible ?

**CURRENT STATUS**
Le dépôt officiel contient le plugin sous `plugins/pr-review-toolkit` et le
manifest observé indique la version `1.0.0`.

**WHAT IS KNOWN**
L'historique officiel du sous-chemin expose le commit
`f7ab5c799caf2ec8c7cd1b99d2bc2f158459ef5e` du 9 octobre 2025, qui ajoute les
17 fichiers du plugin. Le HEAD du dépôt principal observé est plus récent.

**WHAT IS UNKNOWN**
Il reste à revalider avant intégration que l'historique du sous-chemin n'a pas
évolué depuis l'observation et que le contenu exact choisi est celui attendu.

**EVIDENCE**
Source officielle :
`https://github.com/anthropics/claude-code/commits/main/plugins/pr-review-toolkit`
et commit officiel :
`https://github.com/anthropics/claude-code/commit/f7ab5c799caf2ec8c7cd1b99d2bc2f158459ef5e`.
Le manifest `.claude-plugin/plugin.json` indique `1.0.0` et le README indique
la licence MIT.

**DECISION**
`DECIDED WITH CONDITION` : le commit de référence proposé est
`f7ab5c799caf2ec8c7cd1b99d2bc2f158459ef5e`, à revalider et à hasher dans un
manifest avant toute intégration. Aucun `main` mouvant ni `@latest` ne sera
utilisé.

**JUSTIFICATION**
L'historique officiel fournit désormais une base de pinning exploitable. La
revalidation finale reste nécessaire parce qu'une source externe peut évoluer
entre l'audit et l'intégration.

**IMPACT**
Le Project OS garde l'autorité. L'orchestrator doit vérifier SHA, licence,
contenu et scope avant routing. Anthropic reste Claude-native tant que la
parité Codex n'est pas prouvée. Les agents internes produisent le contrat
commun ; aucun push, auto-fix ou action Git n'est importé.

### Q3 — QUESTION

Quelle licence distincte s'applique exactement au plugin Trail of Bits
`differential-review` ?

**CURRENT STATUS**
Le manifest du plugin indique la version `1.1.4` mais ne déclare pas de champ
de licence.

**WHAT IS KNOWN**
La licence officielle observée à la racine du dépôt Trail of Bits est
Creative Commons Attribution-ShareAlike 4.0 International. La documentation
du plugin expose une skill, une commande et un agent adversarial.

**WHAT IS UNKNOWN**
La licence propre au sous-plugin et les conditions exactes de copie,
vendorisation et redistribution ne sont pas établies.

**EVIDENCE**
Source officielle du plugin :
`https://github.com/trailofbits/skills/tree/main/plugins/differential-review`.
Manifest :
`https://raw.githubusercontent.com/trailofbits/skills/main/plugins/differential-review/.claude-plugin/plugin.json`.
Licence racine : `https://github.com/trailofbits/skills/blob/main/LICENSE`.

**DECISION**
`DEFERRED` — `HUMAN LEGAL REVIEW REQUIRED`. Aucune copie, modification,
vendorisation, redistribution ou intégration runtime dans le dépôt n'est
autorisée avant confirmation juridique de la licence applicable.

**JUSTIFICATION**
Il serait incorrect de déduire les droits du plugin à partir du seul manifest
ou de traiter une licence racine comme une licence propre à chaque fichier.

**IMPACT**
Trail of Bits n'est pas routable actuellement. Les règles de sécurité restent
portées par le Project OS, `tester-reviewer` et `data-guardian`. Une validation
juridique et une décision d'egress seront nécessaires avant tout usage
high-risk.

### Q5 — QUESTION

Quel framework de lint et de tests doit être choisi pour le dépôt Next.js
actuel, sans modifier le code métier ?

**CURRENT STATUS**
Le dépôt possède `typecheck` et `build` dans `package.json`, ainsi que les
tests Python du Project OS et des extensions. Il ne possède pas de script
`lint`, de framework de tests applicatifs ou de configuration ESLint/Vitest/
Jest/Playwright applicative identifiée.

**WHAT IS KNOWN**
Le lockfile résout Next.js `15.5.25`, React `18.3.1`, React DOM `18.3.1` et
TypeScript `5.9.3`. La CI exécute `npm ci --ignore-scripts`, typecheck, build,
les validations Project OS et les validations d'extensions. Les tests
applicatifs n'ont pas été détectés.

**WHAT IS UNKNOWN**
Le besoin réel de lint, unit, integration, contract et browser tests pour la
future verticale n'est pas encore arrêté. Le choix d'un outil et son impact
sur les dépendances, le temps CI et les règles métier ne sont pas mesurés.

**EVIDENCE**
`package.json`, `package-lock.json`, `tsconfig.json`, `next.config.mjs`,
`.github/workflows/quality.yml`, `tests/test_project_os.py` et
`tests/test_extensions.py`.

**DECISION**
`DECIDED WITH CONDITION` : la baseline minimale actuelle est
`npm run typecheck`, `npm run build`, les tests/validateurs Project OS et les
contrôles d'extensions. La baseline cible lint/tests est `DEFERRED` jusqu'à
une phase dédiée, sans installation dans cette phase.

**JUSTIFICATION**
Cette décision décrit honnêtement les preuves existantes sans imposer un
framework populaire sans besoin démontré. Elle permet de stabiliser le contrat
Engineering Quality avant de choisir ses outils d'exécution.

**IMPACT**
L'orchestrator ne peut pas déclarer la couverture applicative complète. Le
`tester-reviewer` doit signaler cette limite dans les runs. La CI reste la
preuve de la baseline actuelle ; toute nouvelle dépendance ou modification de
CI exige une impact analysis, un test et un human gate si nécessaire.

### Q6 — QUESTION

Quelles règles Vercel sont compatibles avec Next.js `^15.5.25` et React
`^18.3.1` ?

**CURRENT STATUS**
Les versions réellement verrouillées sont Next.js `15.5.25`, React `18.3.1`,
React DOM `18.3.1` et TypeScript `5.9.3`. Le site dispose d'un App Router,
de composants client et de `next.config.mjs` avec `reactStrictMode`, images et
redirections, mais aucun backend métier/auth/API n'a été identifié.

**WHAT IS KNOWN**
La skill officielle Vercel `react-best-practices` est une guidance version
`1.0.0`, organisée en huit catégories. La source officielle présente une
incohérence documentaire : `SKILL.md` annonce 70 règles, tandis que
`metadata.json` et `AGENTS.md` annoncent 40+ règles. `after()` est stable dans
Next.js depuis `15.1.0`. `React.cache` est une API de Server Components et
les Server Actions/Route Handlers doivent avoir des contrôles d'autorisation.

**WHAT IS UNKNOWN**
Une validation exhaustive de chaque règle contre chaque parcours futur n'est
pas encore réalisée. Les effets de règles qui supposent une dépendance ou une
API absente du dépôt ne sont pas prouvés.

**EVIDENCE**
Source Vercel :
`https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices`.
`package.json`, `package-lock.json`, `next.config.mjs`. Sources officielles
Next.js :
`https://nextjs.org/docs/app/api-reference/functions/after` et
`https://nextjs.org/docs/app/guides/authentication`. Source officielle React :
`https://react.dev/reference/react/cache`.

**DECISION**
`DECIDED WITH CONDITION` : seul le sous-ensemble contrôlé ci-dessous est
acceptable. Une règle est informative tant qu'elle n'est pas vérifiée contre
le code, les versions et le chemin d'exécution concernés. Aucun dépôt Vercel
complet et aucune règle de déploiement ne sont importés.

**JUSTIFICATION**
Le sous-ensemble évite d'appliquer à React 18 des API React 19 ou d'ajouter
implicitement des dépendances. Il préserve la valeur de la guidance sans en
faire une autorité de correction automatique.

**IMPACT**
Le futur mode React/Next est un mode de `tester-reviewer`, report-only. Les
findings indiquent la règle source, la version vérifiée, le signal observé et
la confiance. Une recommandation non applicable ne bloque pas et ne provoque
aucun fix.

#### Sous-ensemble Vercel contrôlé

| Statut | Règles/familles | Condition d'utilisation |
|---|---|---|
| `APPLICABLE CONDITIONALLY` | `async-cheap-condition-before-await`, `async-defer-await`, `async-parallel`, `async-api-routes`, `async-suspense-boundaries` | Seulement si un chemin asynchrone ou une data boundary existe réellement |
| `APPLICABLE CONDITIONALLY` | `bundle-barrel-imports`, `bundle-analyzable-paths`, `bundle-dynamic-imports`, `bundle-defer-third-party`, `bundle-conditional`, `bundle-preload` | Si le diff touche imports, bundle, dépendance tierce ou chargement ; aucune optimisation sans preuve |
| `APPLICABLE CONDITIONALLY` | `server-cache-react`, `server-dedup-props`, `server-hoist-static-io`, `server-no-shared-module-state`, `server-serialization`, `server-parallel-fetching`, `server-parallel-nested-fetching` | Si Server Components/data fetching sont concernés et sans changer l'architecture par déduction |
| `APPLICABLE CONDITIONALLY` | `server-after-nonblocking` | Compatible avec Next `15.5.25`, mais seulement pour un effet secondaire serveur identifié et testé |
| `SECURITY CONDITIONALLY` | `server-auth-actions` | Uniquement quand Server Actions/auth existent ; à traiter avec security routing, jamais comme simple optimisation |
| `DEPENDENCY CONDITIONALLY` | `server-cache-lru`, `client-swr-dedup` | Seulement après décision et installation séparée de la dépendance ; non applicable à l'état actuel |
| `APPLICABLE CONDITIONALLY` | familles `rerender-*`, `rendering-*` et `js-*` ne nécessitant pas d'API absente | Seulement pour un composant/client code réellement touché ; respecter React 18 et le support navigateur |
| `DEFERRED / IGNORE` | `rendering-activity`, règles liées à `useEffectEvent`, `useLatest` ou à une API React non présente | Ignorer tant que la version et l'API ne sont pas explicitement supportées par le dépôt |
| `DEFERRED / IGNORE` | toute règle nécessitant une dépendance, un runtime, une infrastructure ou un parcours absent | Ne pas installer, inventer ou simuler ce prérequis |

Cette table est un filtre de routing, pas une licence pour modifier le site.
Chaque finding doit rester une recommandation vérifiable ; l'outil ne peut
pas décider qu'une règle `CRITICAL` de performance prévaut sur la sécurité ou
les requirements.

### Q10 — QUESTION

Qui valide les exceptions aux règles de permissions, à l'egress et aux human
gates ?

**CURRENT STATUS**
Le dépôt définit les human gates et leur contenu minimal, mais aucune identité
permanente de validateur n'est documentée.

**WHAT IS KNOWN**
Les rules `.claude/rules/core.md`, `precedence.md`, `stop-conditions.md`,
`change-policy.md`, `agent-permissions.md` et `external-capabilities.md`
imposent une validation humaine pour les opérations sensibles. Les agents ne
peuvent pas s'auto-approuver.

**WHAT IS UNKNOWN**
La personne ou le rôle permanent qui doit valider toutes les exceptions n'est
pas établi dans les fichiers du projet.

**EVIDENCE**
Les rules précédentes, `project-state/CURRENT_STATE.md` et le contrat de gate
documenté dans l'architecture.

**DECISION**
`DECIDED WITH CONDITION` : chaque gate doit nommer un validateur humain
identifiable pour cette décision. Une identité permanente n'est pas nécessaire
pour figer l'architecture ; l'absence d'identité, de date ou de trace produit
`STOP`.

**JUSTIFICATION**
Cela rend l'exception traçable sans inventer une personne et sans donner à un
agent un rôle d'approbateur.

**IMPACT**
L'orchestrator bloque toute exception incomplète. Les agents, skills, rules,
tests et CI doivent transporter une référence de gate. Les décisions
sécurité, egress, données, finances, release et production restent humaines.

### Q11 — QUESTION

Quel est le mécanisme exact de rollback d'un auto-fix futur, sachant que
l'auto-fix est interdit aujourd'hui ?

**CURRENT STATUS**
L'auto-fix, l'auto-commit et l'auto-push sont interdits. Le working tree peut
contenir des changements préexistants qui ne doivent jamais être écrasés par
un `git reset --hard` global.

**WHAT IS KNOWN**
La change policy exige un rollback raisonnable. Compound expose un mode
`apply:local`, tandis que les capacités Anthropic documentent des workflows
Git plus larges ; ces modes ne sont pas activés dans le projet.

**WHAT IS UNKNOWN**
Le dépôt ne possède pas encore de protocole automatisé d'isolation,
snapshot/restauration et validation d'un auto-fix.

**EVIDENCE**
`.claude/rules/change-policy.md`, `.claude/rules/stop-conditions.md`,
`.claude/rules/external-capabilities.md`, le statut Git observé et les sources
Compound/Anthropic de l'audit.

**DECISION**
`DECIDED WITH CONDITION` : `NO AUTO-FIX` reste la règle actuelle. Si un
auto-fix est un jour proposé, le protocole cible est :

1. capturer `git status`, diff binaire, fichiers non suivis et hashes ;
2. isoler l'action dans un scope/worktree ou un patch identifié ;
3. enregistrer les fichiers ajoutés/modifiés et leurs préimages ;
4. appliquer uniquement le patch autorisé ;
5. produire diff, tests et re-review ;
6. restaurer uniquement les fichiers du manifest en cas d'échec ;
7. exécuter les contrôles Project OS et demander le human gate avant de garder
   la correction.

**JUSTIFICATION**
Ce protocole est explicable et ne détruit pas les changements étrangers. Il
ne prétend pas être déjà implémenté.

**IMPACT**
L'orchestrator peut préparer ou recommander un rollback, mais l'application
d'un rollback touchant des fichiers existants reste une action autorisée et
traçable. Rollback obligatoire si un fichier hors scope est touché, si un test
critique échoue, si la re-review échoue, si la parité est cassée ou si un
risque sécurité/production apparaît.

### Q12 — QUESTION

Quels critères mesurables permettront de séparer un agent spécialisé d'un
simple mode du `tester-reviewer` ?

**CURRENT STATUS**
Les agents existants couvrent déjà gouvernance, requirements, construction,
tests, données et 3D. Aucun run Engineering Quality mesuré n'existe encore.

**WHAT IS KNOWN**
Un nouvel agent ajoute des instructions, une maintenance, une surface d'outil
et un coût de contexte. Une responsabilité security-differential pourrait
nécessiter des permissions distinctes, mais Trail reste différé.

**WHAT IS UNKNOWN**
Le coût réel, le taux de duplication et la limite à partir de laquelle un mode
devient ambigu ne sont pas mesurés.

**EVIDENCE**
Les six agents existants, `agent-permissions.md`, le contrat de findings et
les observations de redondance de l'audit.

**DECISION**
`DECIDED WITH CONDITION` : `CREATE NEW AGENT ONLY IF ALL` les conditions
suivantes sont remplies :

1. responsabilité durable et distincte, non couverte par un agent existant ;
2. déclenchement constaté dans au moins 3 runs terminés et au moins 2 types de
   changements, sauf risque critique nécessitant immédiatement une permission
   séparée ;
3. contexte, outils, mémoire ou permissions réellement spécialisés ;
4. l'extension en mode rendrait la responsabilité ambiguë, élargirait
   dangereusement les permissions ou ne permettrait plus un output vérifiable ;
5. un pilote comparatif montre soit une baisse médiane d'au moins 20 % du
   contexte/délai, soit un gain démontré de détection dans une classe de risque
   non couverte, sans baisse de la sécurité ;
6. contrat de finding, cycle de re-review et owner distincts sont définis ;
7. Architecture Gate et human gate approuvent la création.

Sinon : `EXTEND EXISTING AGENT`.

**JUSTIFICATION**
La règle combine preuve d'usage, séparation de responsabilité, moindre
privilège et mesure de bénéfice. Elle évite de créer un agent pour un style,
une tâche unique, une préférence d'outil ou un doublon de reviewer.

**IMPACT**
Les capacités commencent comme modes. L'orchestrator mesure les trois runs,
le `tester-reviewer` porte les reviews, et aucun nouveau fichier d'agent n'est
créé dans cette phase.

## 2 ter. Modes ciblés : conception finale

Ces modes sont des concepts de routing et ne sont pas présents comme fichiers
dans le dépôt.

| Mode | Agent porteur | Skill/source | Déclenchement | Non-déclenchement | Output | Blocage / re-review |
|---|---|---|---|---|---|---|
| Code quality | `tester-reviewer` | `testing` + contrat interne futur | Code non trivial, duplication, complexité, responsabilité | Documentation ou média seul | Findings code/maintainability | `HIGH/CRITICAL`; re-review après fix |
| Types | `requirements-architect` + `tester-reviewer` | `testing`, guidance source si validée | TypeScript, contrats, modèles, frontières | CSS, image, texte sans contrat | Findings types/invariants | `HIGH` si contrat cassé; re-review |
| Error handling | `tester-reviewer` | `testing` + checklist errors | `fetch`, I/O, formulaire, mutation, `try/catch`, fallback | Diff sans chemin d'erreur | Scénarios et findings erreurs | `HIGH` si perte/silence; re-review |
| Tests | `tester-reviewer` | `.claude/skills/testing/SKILL.md` | Comportement ou correction observable | Documentation pure | Gaps, cas limites, logs | Gap critique bloquant; re-review |
| Simplification | `tester-reviewer` en review-only | guidance Anthropic éventuelle | Après correctness et tests, refactor | Avant validation ou sur bug non fermé | Suggestions non bloquantes | Re-review si appliquée |
| React/Next | `tester-reviewer` | Sous-ensemble Vercel contrôlé | `app/`, `components/`, `next.config.mjs`, data boundary | Data-only/backend sans UI | Findings framework/rendu | Bloque régression prouvée; re-review |
| Performance | `tester-reviewer` | Sous-ensemble Vercel + mesure | Bundle, waterfall, rendu, requête, métrique | Micro-optimisation non mesurée | Observation + mesure | Bloque si exigence/régression; re-review |
| Security | `tester-reviewer` + `data-guardian`; Trail futur | rules sécurité + Trail si approuvé | Auth, authz, secrets, données, paiement, externe | Petite UI sans frontière sensible | Findings sécurité + blast radius | `HIGH/CRITICAL` + human gate; re-review |
| Architecture | `requirements-architect` + `orchestrator` | core, precedence, change policy | Boundary, API, DB, dépendance, refactor transversal | Modification locale isolée | Écart, décision, dépendances | Gate selon impact; re-review |
| Data | `data-guardian` | rules data et Project OS | Catalogue, JSON, généré, médias, PDF, données métier | Pure UI sans donnée | Provenance, conflit, intégrité | `UNKNOWN`/business decision; re-review |

Tous les modes utilisent le contrat commun des findings. Aucun mode ne gagne
une permission supplémentaire par son nom. Les modes sécurité et data ne
peuvent pas être remplacés par une guidance de performance.

## 3. Agents existants : couverture et limites

| Agent | EXISTING : couvre déjà | TARGET : peut couvrir après extension | Ne pas lui ajouter |
|---|---|---|---|
| `orchestrator` | Scope, sélection, STOP, preuves, handoff | Classifieur de risque, routing, agrégation et arbitrage | Écriture, exécution métier, approbation de sécurité/release seul |
| `requirements-architect` | Faits, décisions, propositions, inconnues, dépendances, acceptation | Architecture review et contrats de changement | Décision métier à la place de l'humain, correction du code |
| `builder` | Implémentation approuvée, impact analysis, tests, rollback | Application d'un finding explicitement accepté | Auto-fix implicite, suppression, migration, push, deploy |
| `tester-reviewer` | Tests positifs/négatifs, erreurs, limites, scope, régression, verdict | Modes code/type/errors/tests et lecture des findings | Autorité unique de sécurité, approbation financière ou release |
| `data-guardian` | Provenance, doublons, unités, champs, médias, PDF, données supposées | Revue data/domain et impact de données | Inventer une valeur, migrer ou muter des données réelles |
| `verificateur-rendus` | Vérification indépendante des visuels 3D, mécanique et visuelle | Aucun élargissement général nécessaire | Revue TypeScript, sécurité, API ou autorisation métier |

### DECIDED : EXTEND BEFORE CREATE

Les responsabilités `code`, `types`, `errors`, `tests`, `simplification`,
`React/Next`, `performance` et `architecture` commencent comme modes ou
checklists attachés aux agents existants. Une création séparée est interdite
jusqu'au pilote défini en Q12.

La seule responsabilité qui justifie potentiellement un adaptateur distinct
plus tôt est la revue différentielle de sécurité high-risk, car elle combine
historique Git, blast radius et modèle adversarial. Elle reste néanmoins
`DEFERRED` jusqu'à la résolution de licence, egress et permissions.

## 4. Couches des capacités

| Capacité | Couche retenue | Responsable initial | Statut |
|---|---|---|---|
| Code quality | `MODE/SKILL` de revue | `tester-reviewer` sous routing de `orchestrator` | `TARGET` |
| Types/contrats | `MODE/SKILL` | `requirements-architect` + `tester-reviewer` | `TARGET` |
| Error handling | `MODE/SKILL` | `tester-reviewer` | `TARGET` |
| Tests | `WORKFLOW` + skill existante | `tester-reviewer` + CI | `EXISTING/TARGET` |
| Simplification | `MODE` post-correction | `tester-reviewer` ou revue externe ciblée | `DEFERRED` |
| React/Next/performance | `GUIDANCE/SKILL` | mode ciblé, guidance Vercel éventuelle | `DEFERRED` |
| Architecture | `WORKFLOW` + `requirements-architect` | `orchestrator` et architecte | `EXISTING/TARGET` |
| Security differential | `SKILL/AGENT` externe conditionnel | `data-guardian` + tester, outil Trail éventuel | `DEFERRED` |
| Data governance | `AGENT` existant | `data-guardian` | `EXISTING` |
| Browser QA | `MCP` existant | routing après code/tests | `EXISTING` |
| Finding aggregation | `WORKFLOW/TOOL` interne | `orchestrator` | `TARGET` |

Une guidance ne reçoit jamais le statut d'agent. Un MCP ne reçoit jamais le
statut de source d'autorité. Un plugin externe n'obtient pas les permissions
du Project OS par sa seule installation.

## 5. Contrat commun des findings

### 5.1 Champs obligatoires

Chaque reviewer, interne ou externe, doit produire un finding sérialisable
selon ce contrat `TARGET` :

| Champ | Type/valeurs | Rôle |
|---|---|---|
| `id` | identifiant stable | Déduplication et suivi |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` | Gravité technique |
| `category` | `BUG`, `RISK`, `TECHNICAL_DEBT`, `STYLE`, `OPTIMIZATION`, `SECURITY_ISSUE`, `ARCHITECTURAL_ISSUE` | Nature du constat |
| `title` | texte court | Résumé actionnable |
| `description` | texte | Constat et contexte |
| `evidence` | preuve observée | Justification vérifiable |
| `affected_files` | chemins relatifs | Scope précis |
| `affected_lines` | lignes ou `UNKNOWN` | Localisation si disponible |
| `risk` | impact + blast radius | Conséquence potentielle |
| `suggested_remediation` | texte ou `NONE` | Correction proposée, jamais automatique |
| `blocker` | booléen + raison | Passage bloqué ou non |
| `reviewer` | agent/mode/source | Provenance du constat |
| `confidence` | valeur et justification | Niveau de confiance |
| `status` | `OPEN`, `ACCEPTED`, `FIXED`, `VERIFIED`, `ESCALATED`, `WONT_FIX` | Cycle de vie |
| `re_review_required` | booléen + scope | Preuve de fermeture |

### 5.2 Champs supplémentaires nécessaires

- `run_id` et `parent_finding_id` pour relier les passes et re-revues ;
- `baseline_ref` et `diff_ref` pour savoir ce qui a été comparé ;
- `introduced_by` : nouveau, préexistant ou inconnu ;
- `requirement_refs` et `acceptance_refs` pour la traçabilité ;
- `test_refs` et `evidence_refs` pour relier les preuves ;
- `data_classification` lorsque le constat touche des données ;
- `human_gate_required` et `human_gate_ref` ;
- `owner` et `due_phase` pour le suivi ;
- `duplicate_of` et `contradicts` pour l'agrégation ;
- `tool_version` et `source_sha` lorsqu'un outil externe a produit le finding.

### 5.3 Règles de verdict

- `CRITICAL` : STOP immédiat, correction, re-review et human gate si le
  contexte touche sécurité, data, finance ou production.
- `HIGH` : passage bloqué jusqu'à correction ou acceptation humaine tracée.
- `MEDIUM` : blocker selon le contexte défini en Q7 ; sinon correction
  planifiée ou acceptation avant release.
- `LOW` : dette ou amélioration suivie, non bloquante par défaut.
- `INFO` : observation sans correction obligatoire.

Le reviewer ne peut pas passer lui-même un finding `OPEN` à `VERIFIED` après
une modification qu'il a effectuée sans relecture du diff et nouvelle preuve.

## 6. Routing matrix par risque

Les termes `obligatoire`, `optionnel` et `inutile` décrivent le routing cible,
pas des agents actuellement créés. `TR` signifie `tester-reviewer`, `RA`
`requirements-architect`, `DG` `data-guardian`, `VO` `verificateur-rendus`,
`RN` le mode React/Next, `SD` la revue security differential et `BQ` la QA
browser locale via Playwright.

| Type de changement | Reviewers obligatoires | Optionnels | Inutiles par défaut | Tests obligatoires | Playwright | Human gate |
|---|---|---|---|---|---|---|
| Simple UI | TR ciblé | RN, BQ si interaction/responsive | SD, DG, RA | typecheck/build + comportement impacté | Si interaction/visuel | Non, sauf production/sensible |
| Composant React | TR + RN si rendu/état | revue types, BQ | SD, DG | tests comportementaux si état/props | Si parcours/interaction | Selon blast radius |
| Page Next.js | TR + RN | RA si boundary data, BQ | DG si aucune donnée | typecheck/build + tests du parcours | Oui si parcours utilisateur | Selon données |
| Refactor important | RA + TR | types, errors, simplification, RN | SD si aucune frontière | tests ciblés + régression élargie | Si UI touchée | Selon blast radius |
| Nouvelle feature | RA + TR | types, errors, RN, BQ | SD si non sensible | acceptance + négatifs + régression | Si user-facing | Selon métier/data |
| Logique métier | RA + TR | types, errors, DG, SD | RN si aucun UI | unit/integration/scénarios métier | Non par défaut | Oui si décision métier |
| Données | DG + RA + TR | SD si accès sensible | RN/BQ si non UI | intégrité, cas limites, non-régression | Non | Oui pour données réelles |
| Catalogue | DG + TR | RA, BQ si affichage | SD sans frontière sensible | génération/consistance/médias/PDF | Si affichage modifié | Oui pour prix/données validées |
| Stock | RA + DG + TR + SD | types, errors, simulation | RN/BQ si backend only | scénarios métier, concurrence, rollback | Non sauf UI | Obligatoire |
| Commande | RA + DG + TR + SD | types, errors, simulation, BQ | RN si sans UI | workflow, négatifs, idempotence, régression | Si UI | Obligatoire |
| Paiement | RA + DG + TR + SD | types, errors, simulation | RN/BQ si aucune UI | intégration sandbox, erreurs, idempotence | Non par défaut | Obligatoire |
| Authentification | RA + TR + SD | types, errors, RN, BQ | DG si aucune donnée | négatifs, sessions, récupération | Si login UI local | Obligatoire |
| Permissions | RA + TR + SD | types, errors, DG | BQ si aucune UI | tests d'isolation utilisateur/entreprise | Si écran local | Obligatoire |
| Migration | RA + DG + TR + SD | errors, resilience, simulation | RN/BQ sans UI | dry-run, comparaison, rollback, reprise | Non | Obligatoire |
| Dépendance | TR | RN, SD si runtime/script, RA si architecture | DG/BQ sans data/UI | lockfile, typecheck, build, tests | Selon impact UI | Si script/secret/prod |
| Configuration | TR + SD si sécurité | RA, RN si framework | DG/BQ sans data/UI | validation config/CI et non-régression | Selon impact | Oui pour CI/prod/deploy |
| Changement sensible | RA + TR + SD + DG si données | errors, simulation | BQ si non UI | suite adaptée au blast radius | Selon impact | Obligatoire |
| Release | TR + RA + DG si data + SD | RN, BQ, VO selon contenu | Aucun reviewer applicable ne remplace le gate | preuves complètes + régression | Local seulement | Obligatoire |

### Règle de routage

Un reviewer marqué obligatoire ne peut être omis que par un STOP explicite et
une décision humaine. Un reviewer optionnel ne doit pas être lancé si son
signal de risque est absent. Un reviewer inutile ne doit pas être appelé par
défaut.

## 7. Context et tokens

### DECIDED

Le système n'utilise pas de swarm permanent. Il applique les mécanismes
suivants :

1. **Diff-first** : lire d'abord le diff, les fichiers touchés et leur contexte
   immédiat.
2. **Scoped review** : borner le reviewer à un scope de fichiers, lignes,
   requirements et risques.
3. **Lazy loading** : charger une skill, une référence ou un agent uniquement
   si le classifieur le demande.
4. **Routing** : choisir par chemin, opération, données, boundary et blast
   radius ; ne pas déduire le risque du seul nom de tâche.
5. **Shared snapshot** : les reviewers read-only parallèles lisent le même
   snapshot identifié par `run_id`.
6. **Aggregation** : normaliser une seule fois les findings dans le contrat
   commun.
7. **Deduplication** : regrouper par fichier, lignes, catégorie, preuve,
   signature sémantique et finding parent.
8. **Contradiction check** : deux conclusions incompatibles restent ouvertes et
   déclenchent `STOP` jusqu'à arbitrage.
9. **Résumé mémoire** : la mémoire active conserve statut, décisions,
   blockers, régressions et liens ; le détail reste dans l'artefact du run.

### Review complète justifiée si

- plusieurs boundaries sont touchées ;
- un changement modifie données, sécurité, permissions, finances ou release ;
- le blast radius est inconnu ou transversal ;
- le refactor supprime ou déplace des responsabilités ;
- un bug critique ou une régression est confirmé ;
- les findings précédents sont contradictoires ou non vérifiés.

Une petite UI locale ne justifie pas six reviewers ni une revue différentielle
Git complète.

## 8. Review loop finale

```text
DISCOVER
  -> ANALYZE
  -> PLAN
  -> IMPLEMENT
  -> TEST
  -> REVIEW
  -> FINDINGS
  -> FIX (action séparée)
  -> RE-REVIEW
  -> TEST
  -> REGRESSION
  -> SIMULATION si routée
  -> SECURITY GATE si routée
  -> HUMAN GATE si requis
  -> DOCUMENT
  -> UPDATE MEMORY
  -> VERIFY
  -> DONE / ESCALATE / STOP
```

### Responsabilités et preuves

| Étape | Responsable initial | Entrée | Sortie | Passage | Arrêt |
|---|---|---|---|---|---|
| `DISCOVER` | `orchestrator` | Demande, état, règles, Git | Scope, fichiers, refs, suivis/non suivis | Scope complet et non ambigu | Info manquante, fichier inattendu |
| `ANALYZE` | `orchestrator` + `RA`/`DG` | Scope et requirements | Risque, dépendances, agents/modes | Risque classifié | Contradiction, décision métier manquante |
| `PLAN` | `orchestrator` | Analyse | Plan, tests, rollback, gates | Plan approuvé | Périmètre ou preuve non défini |
| `IMPLEMENT` | `builder` | Plan approuvé | Diff local | Écriture dans scope autorisé | Scope dépassé, action interdite |
| `TEST` | `TR`/CI | Diff et acceptance | Logs, résultats, non exécutés | Tests requis passés | Test critique échoué |
| `REVIEW` | Modes routés | Snapshot + diff | Findings structurés | Findings normalisés | Permission ou preuve insuffisante |
| `FINDINGS` | Agrégateur | Findings multiples | Déduplication, blockers, contradictions | Arbitrage terminé | Contradiction non résolue |
| `FIX` | `builder` après autorisation | Finding accepté | Nouveau diff | Scope inchangé | Auto-fix non autorisé, rollback absent |
| `RE-REVIEW` | Reviewer d'origine + TR | Finding corrigé + diff | Finding `VERIFIED` ou nouveau finding | Correction prouvée | Finding bloquant encore ouvert |
| `SIMULATION` | TR + domaine | Scénarios et doubles | Résultats/failures | Scénarios requis passés | Failure non expliquée |
| `SECURITY GATE` | TR + DG + SD éventuel | Findings, tests sécurité | Verdict sécurité | Aucun blocker et preuves | Issue, egress, secret ou boundary non prouvé |
| `HUMAN GATE` | Humain désigné | Action, risque, diff, tests, rollback | Décision tracée | Approbation explicite | Refus, absence, décision incomplète |
| `REGRESSION` | TR/CI | Baseline et nouveau diff | Résultat ciblé/élargi | Aucune régression non traitée | Régression ou environnement inconnu |
| `DOCUMENT` | Orchestrator + agent concerné | Résultats | Rapport et décision | Artefact lié au run | Traçabilité manquante |
| `UPDATE MEMORY` | Orchestrator | Résumé vérifié | État, blockers, learnings | Mémoire cohérente | Conflit d'état |
| `VERIFY` | Orchestrator + reviewer indépendant | Toutes les preuves | `DONE`, `FIX`, `ESCALATE` | Definition of Done complète | Une preuve obligatoire manque |

### Automatique versus humain

**Automatisable sous contrôle :** collecte du diff, classification par chemins,
tests déterministes, typecheck/build, validation de schéma, déduplication
proposée, présence des artefacts et calcul du statut technique.

**Jamais implicite :** décision métier, acceptation d'un risque, exception de
permission, sortie d'egress, migration, paiement, modification de données
réelles, commit, push, release et deploy.

Un `DONE` est impossible si un `STOP` existe, si un finding bloquant reste
ouvert, si une re-review est due ou si une preuve obligatoire est absente.

## 9. Modèle de sécurité

### Politique par capacité

| Capacité | READ | WRITE | NETWORK | SHELL | GIT | DEPLOY |
|---|---|---|---|---|---|---|
| Guidance Vercel | `ALLOW` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| Revue Anthropic report-only | `ALLOW` scope | `DENY` sauf rapport | `DENY` | `CONDITIONAL` read-only | `ALLOW` read-only | `DENY` |
| Compound sélectionné | `CONDITIONAL` | rapport uniquement par défaut | `DENY` | `CONDITIONAL` | read-only | `DENY` |
| Trail high-risk éventuel | diff/historique borné | rapport uniquement | `DENY` par défaut | `CONDITIONAL` | read-only | `DENY` |
| Playwright existant | local QA | artefact dédié uniquement | local uniquement | selon MCP | `DENY` | `DENY` |

### Interdictions absolues

- Aucun credential réel, secret ou token dans le prompt, rapport, fixture ou
  configuration versionnée.
- Aucun accès cross-model ou réseau externe par défaut.
- Aucun filesystem hors scope et aucun écrasement silencieux.
- Aucun Git write : `commit`, `push`, création de PR ou tag par un reviewer.
- Aucun auto-fix sans action séparée, snapshot, tests, re-review et gate.
- Aucun deploy, y compris depuis une skill qui combine review et release.
- Aucune donnée métier réelle dans un test ou une simulation locale.
- Aucune compétence externe ne peut modifier `.claude/rules/`, la mémoire de
  gouvernance ou la politique de production sans scope explicite et gate.

Les permissions déclarées dans une instruction Markdown ne sont pas une
frontière technique. La sandbox, l'hôte et les approvals doivent également
limiter les outils réellement exposés.

### STOP prioritaire

Un STOP interrompt boucle, retry, auto-correction, délégation, parallélisme et
automatisation 3D. Seul le traitement de la cause, ou une décision humaine
explicite lorsque requise, peut le lever.

## 10. Décisions sur les outils audités

| Outil | Décision | Justification |
|---|---|---|
| Anthropic PR Review Toolkit | `PARTIAL / SUBSET` puis `DEFER` | Capacités de revue utiles et spécialisées, mais Claude-native, provenance de sous-chemin non établie et exemples Git incompatibles ; aucun plugin complet maintenant |
| Vercel React Best Practices | `PARTIAL / SUBSET` puis `DEFER` | Guidance React/Next unique et utile, mais dépôt complet à risque à cause de la skill deploy et compatibilité version par version non établie |
| Compound Engineering | `DEFER` avec `REJECT` du plugin complet | Agrégation et workflows intéressants, mais 35 skills, écriture, pipeline commit/push/PR et cross-model rendent l'intégration complète disproportionnée |
| Trail of Bits Differential Review | `DEFER` | Spécialiste high-risk utile, mais licence plugin inconnue, egress et permissions à valider avant toute copie ou exécution |

### KEEP / ADAPT / PARTIAL / DEFER / REJECT par usage

- **KEEP** : Project OS, agents internes, `testing`, `project-audit`,
  `discovery`, rules de sécurité et Playwright local existants.
- **ADAPT** : idées de contrat, agrégation et re-review des sources externes,
  sans importer leurs permissions ou workflows Git.
- **PARTIAL / SUBSET** : guidance Vercel et quelques rôles de revue Anthropic,
  après provenance et découverte vérifiées.
- **DEFER** : Trail high-risk et toute extraction externe jusqu'aux gates
  licence/egress/sécurité.
- **REJECT** : installation complète Compound, dépôt Vercel complet, marketplace
  Trail complète, versions mouvantes, auto-fix, auto-commit, auto-push, deploy
  et cross-model par défaut.

## 11. Architecture finale

```text
PROJECT OS AUTHORITY
        |
        v
EXISTING ORCHESTRATOR
        |
        v
RISK CLASSIFIER
  (scope / paths / operation / data / blast radius)
        |
        v
REVIEWER ROUTING
  |
  +--> requirements-architect for requirements/architecture/contracts
  +--> data-guardian for data/catalogue/generated/media/PDF provenance
  +--> tester-reviewer modes: code/types/errors/tests/regression
  +--> React/Next guidance for app/components/framework changes
  +--> Playwright local QA for user-facing interaction/responsive behavior
  +--> security differential review only for high-risk changes, if approved
        |
        v
SPECIALIZED READ-ONLY REVIEWS
        |
        v
FINDING NORMALIZATION
  -> DEDUPLICATION
  -> CONTRADICTION CHECK
        |
        v
FIX AS SEPARATE AUTHORIZED ACTION
        |
        v
TARGETED RE-REVIEW
        |
        v
TESTS / SIMULATION / SECURITY GATE according to risk
        |
        v
HUMAN GATE when required
        |
        v
REGRESSION -> DOCUMENT -> UPDATE MEMORY -> VERIFY
        |
        +--> DONE
        +--> FIX
        +--> ESCALATE
        +--> STOP
```

Cette architecture est retenue parce qu'elle minimise la duplication : le
Project OS décide, les agents existants gardent leur domaine, les capacités
externes complètent seulement un axe et l'agrégateur impose un contrat commun.

## 12. Plan de construction ultérieur

Les phases futures restent `TARGET`, pas une autorisation immédiate. La
Phase 1 et le socle initial de routing/agrégation sont implémentés dans la
présente phase.

### Phase 1 — Contrat interne — IMPLEMENTED

- créer le schéma de finding et le format de run ;
- définir le mapping sévérité/catégorie/blocker ;
- définir la preuve de re-review et la règle de contradiction ;
- tests de schéma et de scope ;
- aucun outil externe.

### Phase 2 — Baseline de qualité

- choisir lint/test après résolution de Q5 ;
- mesurer typecheck/build et l'état initial ;
- ajouter seulement la CI nécessaire ;
- ne pas refactorer le métier.

### Phase 3 — Guidance React/Next

- résoudre Q6 ;
- épingler un snapshot minimal Vercel ;
- exclure le deploy skill ;
- prouver découverte Codex/Claude si exposé aux deux ;
- tester sur un changement non métier.

### Phase 4 — Revue générale

- résoudre Q1 ;
- utiliser un sous-ensemble Anthropic report-only ;
- comparer avec `tester-reviewer` ;
- mesurer doublons, coût et re-review.

### Phase 5 — Routing et agrégation — INITIAL FOUNDATION IMPLEMENTED

- le classifieur, le routing et l'agrégation minimale sont implémentés ;
- la persistance complète des runs et l'orchestration automatisée restent
  différées ;
- conserver un seul orchestrator ;
- paralléliser uniquement des reviews read-only indépendantes.

### Phase 6 — High-risk security

- résoudre Q3, Q10 et les contraintes d'egress ;
- obtenir le human gate sécurité/juridique ;
- exécuter Trail uniquement sur diff/history borné si approuvé ;
- ne pas le traiter comme security gate unique.

### Phase 7 — Mesure et séparation éventuelle

- exécuter au moins trois runs représentatifs ;
- collecter les métriques de Q12 ;
- décider si un mode devient un agent durable ;
- créer un agent uniquement après approbation séparée.

## 13. Definition of Done

### Fonctionnalité ou modification

Elle n'est terminée que si :

1. requirements et scope sont identifiés ;
2. faits, décisions, propositions et inconnues sont séparés ;
3. code modifié reste dans les fichiers autorisés ;
4. tests ciblés et négatifs sont exécutés ;
5. reviewers routés ont rendu des findings normalisés ;
6. les findings bloquants sont corrigés ou acceptés par le gate compétent ;
7. toute correction a été re-reviewée ;
8. simulation, sécurité et browser QA sont exécutées si le routing le demande ;
9. la régression est passée ;
10. documentation, mémoire, handoff et artefacts sont mis à jour ;
11. la preuve de rollback existe ;
12. `VERIFY` confirme qu'aucun STOP ni finding requis ne reste ouvert.

### Phase

Une phase est terminée seulement si ses gates, ses preuves, ses risques
acceptés et son rollback sont documentés. Le passage de phase n'est pas
déduit d'un délai, d'un build vert ou de l'absence de commentaire d'un seul
reviewer.

### Projet

Le projet ne sera terminé que lorsque requirements, code, données, tests,
sécurité, simulation, régression, documentation, preuves, validation humaine
et release contrôlée seront tous traçables et vérifiés. Cette définition ne
constitue pas une autorisation de commencer l'ERP.

## 14. Conditions résiduelles et questions non résolues

La décision d'architecture est suffisamment stable pour construire le contrat
interne, mais les conditions ci-dessous restent obligatoires avant les
intégrations externes correspondantes :

1. `Q1 CONDITION` : revalider le commit Anthropic et hasher le snapshot avant
   toute intégration.
2. `Q3 BLOCKER TRAIL` : obtenir une confirmation juridique de la licence du
   plugin Trail of Bits ; `HUMAN LEGAL REVIEW REQUIRED`.
3. `Q5 CONDITION` : choisir la baseline lint/tests dans une phase séparée.
4. `Q6 CONDITION` : valider les règles Vercel au niveau de chaque règle et de
   chaque version concernée.
5. `Q10 CONDITION` : nommer un humain identifiable dans chaque gate ; aucune
   identité permanente n'est inventée.
6. `Q11 CONDITION` : ne jamais autoriser l'auto-fix avant le protocole de
   snapshot/restauration et la re-review.
7. `Q12 CONDITION` : mesurer trois runs représentatifs avant de créer un agent.

Ces conditions ne justifient ni installation ni modification du site. Les
politiques cross-model, `MEDIUM`, stockage des runs et scope des extensions
non suivies sont décidées par défaut dans les sections précédentes ; toute
exception future doit être tracée par human gate.

## 14 bis. Architecture status

`VALIDATED WITH CONDITIONS`

Raison : aucune question critique ne remet en cause le modèle Project OS,
l'extension des agents existants, le contrat de findings, le routing par risque
ou la boucle review/fix/re-review. Les conditions externes et juridiques
restent bloquantes pour les outils concernés et empêchent de considérer leur
intégration comme validée.

## 15. État de la présente phase

- **Implémenté** : contrat findings, validation sérialisable, transitions,
  agrégation minimale, routing diff-first, modes ciblés et règles report-only.
- **Fichiers de référence** : `ENGINEERING_QUALITY_FINDINGS.md`,
  `ENGINEERING_QUALITY_ROUTING.md` et `scripts/validation/engineering_quality.py`.
- **Agents créés** : aucun ; les agents existants portent les modes définis.
- **Non intégré** : Anthropic, Vercel, Trail of Bits, Compound et tout autre
  outil externe.
- **Non modifié** : code applicatif, données métier, catalogue, médias, PDF,
  modèles 3D, dépendances et configuration de déploiement.
- **Non effectué** : installation, commit, push, deploy, migration, auto-fix
  et refactor applicatif.

### NEXT ACTION BEFORE PHASE 1

Valider humainement les sept décisions et conditions résiduelles ainsi que
cette architecture avant d'ouvrir la Phase 1 — Contrat interne.

## 16. Phase 1 — fondation interne

Cette phase peut construire le socle interne sans intégrer les outils
externes. L'implémentation autorisée est limitée à :

- `docs/architecture/ENGINEERING_QUALITY_FINDINGS.md` ;
- `docs/architecture/ENGINEERING_QUALITY_ROUTING.md` ;
- `scripts/validation/engineering_quality.py` ;
- les règles et sections de modes des agents existants ;
- les tests et contrôles Project OS associés.

Elle ne crée aucun agent, skill, MCP, dépendance, fonctionnalité métier ou
capacité d'auto-fix. L'état réalisé doit être confirmé par les tests et par un
contrôle d'intégrité Git avant de passer à la phase suivante.
