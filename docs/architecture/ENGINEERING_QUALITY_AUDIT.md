# Engineering Quality Audit

**Statut : CONDITIONS**
**Date d'audit : 2026-09-17**
**Périmètre : audit et conception uniquement**

Ce document ne constitue pas une autorisation d'installation ou d'intégration.
Les termes `FACT`, `UNKNOWN`, `PROPOSED` et `DECISION PROPOSED` sont utilisés
pour séparer respectivement les observations vérifiées, les informations non
vérifiables, les recommandations et les décisions qui nécessitent encore une
validation humaine.

## 1. OBJECTIF

Concevoir une couche Engineering Quality qui complète le Project OS sans le
remplacer. Cette couche doit permettre une revue proportionnelle au risque,
reproductible, traçable et exploitable par Codex et Claude Code, tout en
évitant un swarm permanent, les doublons de revue et les actions implicites de
modification, commit, push ou déploiement.

Le dépôt est actuellement un site Next.js existant. `package.json` expose
`dev`, `build`, `start` et `typecheck`, mais aucun socle lint/test dédié n'a
été identifié dans la configuration actuelle. L'ERP métier, sa base de
données, son API, ses permissions et ses migrations ne sont pas encore le
périmètre de cette phase.

## 2. SOURCES AUDITÉES

### 2.1 Références internes

- `CLAUDE.md` : workflow du site, données réelles, génération du catalogue,
  synchronisation et politique de commit/push.
- `.claude/rules/core.md`, `.claude/rules/precedence.md`,
  `.claude/rules/stop-conditions.md`, `.claude/rules/change-policy.md` et
  `.claude/rules/agent-permissions.md` : gouvernance actuelle.
- `.claude/rules/external-capabilities.md` : autorité du Project OS sur les
  capacités externes et restrictions Playwright.
- `.claude/agents/orchestrator.md`, `requirements-architect.md`, `builder.md`,
  `tester-reviewer.md`, `data-guardian.md` et `verificateur-rendus.md`.
- `.claude/skills/discovery/SKILL.md`, `project-audit/SKILL.md` et
  `testing/SKILL.md`.
- `docs/architecture/EXTERNAL_CAPABILITIES.md` et
  `docs/architecture/EXTENSION_DISCOVERY.md`.
- `project-state/CURRENT_STATE.md`, `project-state/TEST_STATUS.md` et les
  tests/validateurs du Project OS et des extensions.
- `package.json`, `tsconfig.json`, `.github/workflows/quality.yml` et
  l'inventaire réel de `app/`, `components/`, `lib/` et `scripts/`.

### 2.2 Références externes officielles

- Anthropic Claude Code, plugin PR Review Toolkit :
  `https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit`
- Vercel Labs, skill React Best Practices :
  `https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices`
- Every, Compound Engineering Plugin :
  `https://github.com/EveryInc/compound-engineering-plugin`
- Trail of Bits, plugin Differential Review :
  `https://github.com/trailofbits/skills/tree/main/plugins/differential-review`

Les dépôts externes ont été consultés comme sources de référence. Aucun
script d'installation externe n'a été lancé et aucune nouvelle extension n'a
été installée dans cette phase.

## 3. VERSION / SHA

Les versions ci-dessous sont les révisions observées pendant l'audit. Une
intégration future devra refaire la vérification et enregistrer le commit
exact retenu dans un manifest. Un HEAD de dépôt n'est pas assimilé à un SHA
de sous-répertoire lorsque celui-ci n'a pas pu être établi séparément.

| Solution | Version observée | Révision pertinente observée | Licence observée | Niveau de confiance |
|---|---:|---|---|---|
| Anthropic PR Review Toolkit | `1.0.0` | HEAD du dépôt `anthropics/claude-code` : `3deb821cb71ccfaaf2ffa9935e977df314ce5cd5`; SHA propre au chemin du plugin : `UNKNOWN` | MIT dans le README du plugin | Moyenne |
| Vercel React Best Practices | `1.0.0` | `dc8367e6f91c022d83361f03c3313fa05e848ee5` | MIT | Moyenne à élevée |
| Compound Engineering | `3.26.3` | HEAD observé : `1a9f16c45e659d3bcb572b9e73c50aabccdc8b86` | MIT | Élevée pour le dépôt observé |
| Trail of Bits Differential Review | `1.1.4` | `4b1b74b181e81cbcaa8d3b68a0e4ed867165b972` | Licence propre au plugin : `UNKNOWN`; licence du dépôt : CC BY-SA 4.0 | Moyenne, avec blocage juridique à clarifier |

### Contradiction de version détectée chez Vercel

`react-best-practices/SKILL.md` annonce 70 règles dans 8 catégories, alors
que le README et le `AGENTS.md` compilé annoncent 40+ règles. Cette divergence
doit être résolue par l'artefact exact qui serait épinglé. Aucun nombre ne
doit être utilisé comme critère d'acceptation avant cette vérification.

### Limitation de provenance détectée chez Anthropic

Le HEAD du dépôt principal a été observé, mais le dernier commit propre au
sous-chemin `plugins/pr-review-toolkit` n'a pas été exposé de manière
indépendante par la source consultée. La future intégration doit donc choisir
entre un snapshot complet dont le contenu est hashé et une référence Git
reproductible après vérification humaine.

## 4. NATURE DE CHAQUE OUTIL

| Solution | Nature réelle | Ce qu'elle n'est pas | Fonction principale |
|---|---|---|---|
| Anthropic PR Review Toolkit | `PLUGIN` contenant un ensemble de six agents de revue et une commande | Pas un MCP, pas une bibliothèque métier, pas un orchestrateur autonome autorisé par le Project OS | Revue spécialisée de diff/PR : commentaires, tests, erreurs silencieuses, types, qualité et simplification |
| Vercel React Best Practices | `SKILL`, `GUIDELINES` et règles documentées/compilées | Pas un agent, pas un MCP, pas un outil de déploiement acceptable lorsqu'il est extrait seul | Guidance React/Next.js et performance |
| Compound Engineering | `PLUGIN`, ensemble de skills, workflows, scripts et sous-agents/personas | Pas une simple skill légère | Planification, exploration, revue, exécution et artefacts de workflow |
| Trail of Bits Differential Review | `PLUGIN` avec `SKILL`, `COMMAND` et agent spécialisé `adversarial-modeler` | Pas une preuve complète de sécurité et pas une frontière technique de sécurité | Revue différentielle orientée risque, historique Git, blast radius et modèle adversarial |

Aucun des quatre outils n'est un MCP. Playwright MCP est une capacité déjà
présente dans le Project OS et reste séparée de cette analyse ; il ne doit pas
être ajouté ou remplacé ici.

### Détail Anthropic

Le plugin expose six rôles : `comment-analyzer`, `pr-test-analyzer`,
`silent-failure-hunter`, `type-design-analyzer`, `code-reviewer` et
`code-simplifier`. La commande `/pr-review-toolkit:review-pr` sélectionne
les revues selon l'aspect demandé et peut les lancer en parallèle ou en
séquence. Elle utilise notamment `Bash`, `Glob`, `Grep`, `Read` et `Task`.

La documentation du plugin contient aussi un exemple de workflow avec commit
et push. Cet exemple est incompatible avec la politique interne par défaut et
ne pourrait pas être repris tel quel.

### Détail Vercel

La skill `react-best-practices` est principalement une guidance textuelle
organisée par catégories : waterfalls et asynchronisme, bundle, serveur,
client, re-renders, rendering, JavaScript et avancé. Le dépôt source contient
également des scripts de build/validation et une skill distincte de
déploiement (`vercel-deploy-claimable`). Le dépôt complet ne doit donc pas être
installé pour obtenir la seule guidance React/Next.

La guidance doit être confrontée à la version réelle du projet : Next.js
`^15.5.25` et React `^18.3.1` dans `package.json`. Une règle qui présuppose
une API plus récente ne peut pas être appliquée sans vérification.

### Détail Compound Engineering

Le plugin annonce 35 skills et une exécution sur plusieurs hôtes, dont Claude
Code et Codex. `ce-code-review` est une skill de revue qui produit des
artefacts et est report-only par défaut, mais son mode `apply:local` autorise
des corrections locales. Le plugin contient aussi une skill séparée
`ce-commit-push-pr` qui peut committer, pousser et ouvrir une PR, avec un mode
pipeline qui peut supprimer les prompts ordinaires.

Le workflow utilise beaucoup de références, de scripts et de personas. Le
mode de revue peut envoyer du contenu hors machine lorsqu'une revue
cross-model est explicitement activée. Ce comportement n'est pas compatible
avec une activation par défaut sur des données commerciales ou sensibles.

### Détail Trail of Bits

`differential-review` combine une skill, une commande et un agent adversarial.
Il inspecte le diff, l'historique et le contexte de changement, puis adapte la
profondeur à des signaux tels que l'authentification, la cryptographie, le
transfert de valeur, les appels externes ou les permissions. Il utilise
`Read`, `Write`, `Grep`, `Glob` et `Bash`.

Le manifest du plugin ne déclare pas de licence distincte. La licence
CC BY-SA 4.0 observée au niveau du dépôt impose une revue juridique avant
toute copie ou redistribution dans le projet. Les skills compagnons sont
optionnels et les dépendances applicatives ne sont pas déclarées dans le
manifest du plugin ; leur nécessité effective doit être vérifiée dans un
snapshot précis.

## 5. COMPATIBILITÉ CODEX

| Solution | Support observé | Mode possible | Limites |
|---|---|---|---|
| Anthropic PR Review Toolkit | `CONDITIONNEL` | Utilisation Claude-native ou extraction documentée de prompts | Le plugin et `Task` sont conçus pour Claude Code ; aucune preuve de découverte native par Codex n'a été établie |
| Vercel React Best Practices | `POTENTIELLEMENT PORTABLE` | Skill projet textuelle sous `.agents/skills/`, après snapshot épinglé | La découverte runtime et la compatibilité de chaque règle doivent être prouvées ; le dépôt complet ne doit pas être installé |
| Compound Engineering | `OBSERVÉ` comme support annoncé | Plugin/skills Codex natifs selon le dépôt | Forte surface, scripts/artefacts, modes d'écriture et cross-model ; support annoncé ne vaut pas validation dans ce dépôt |
| Trail of Bits Differential Review | `CONDITIONNEL` | Marketplace compatible ou adaptation contrôlée | Commandes/agents et permissions Bash/Write doivent être testés ; licence et egress restent à clarifier |

Pour qu'une capacité soit vendue comme commune à Codex et Claude Code, il faut
prouver séparément : découverte runtime, lecture de la structure, exécution
sur un diff sans écriture et interprétation du résultat. La simple présence
d'un `SKILL.md` dans le dépôt n'est pas une preuve suffisante.

## 6. COMPATIBILITÉ CLAUDE CODE

| Solution | Support observé | Mode possible | Limites |
|---|---|---|---|
| Anthropic PR Review Toolkit | `NATIF` dans Claude Code | Plugin Claude Code en report-only contrôlé | Outils Bash/Task, exemples commit/push et six agents ; le Project OS doit rester prioritaire |
| Vercel React Best Practices | `PORTABLE` sous forme de skill/guidance | Skill projet Claude Code après validation du snapshot | Divergence du nombre de règles et compatibilité Next/React à vérifier |
| Compound Engineering | `OBSERVÉ` comme support annoncé | Plugin Claude Code complet ou extraction limitée | L'intégration complète est disproportionnée et introduit des chemins d'écriture/push/egress |
| Trail of Bits Differential Review | `NATIF/CONDITIONNEL` via plugin Claude | Revue high-risk avec Bash/Write bornés | Licence, égress et accès historique Git exigent une décision dédiée |

Même dans Claude Code, une capacité externe reste au niveau inférieur au
Project OS. La compatibilité runtime n'accorde aucune permission implicite.

## 7. CAPACITÉS

| Capacité | A Anthropic | B Vercel | C Compound | D Trail of Bits |
|---|---|---|---|---|
| Code quality | Forte, avec `code-reviewer` | Indirecte | Forte, très large | Indirecte, orientée risque |
| Types | Forte, `type-design-analyzer` | Guidance TypeScript/React partielle | Variable selon skill/persona | Indirecte |
| Tests | Forte, `pr-test-analyzer` | Guidance, pas d'exécution | Forte, workflow de tests/revue | Test gaps dans revue différentielle |
| Errors | Forte, `silent-failure-hunter` | Indirecte | Variable | Indirecte et sécurité-oriented |
| React/Next | Limitée à une revue générique | Forte et unique | Variable, selon le reviewer | Indirecte |
| Security | Partielle, erreurs silencieuses/types | Faible, guidance performance | Variable, dépend du workflow | Forte sur changements différentiels à risque |
| Performance | Partielle | Forte, cœur de la skill | Variable | Indirecte |
| Architecture | Partielle | Indirecte | Forte mais large | Blast radius/dépendances, pas gouvernance complète |
| Simplification | Forte, `code-simplifier` | Indirecte | Forte selon workflow | Non centrale |

Les capacités ne doivent pas être sommées mécaniquement. Un finding de
performance n'est pas un finding de sécurité, et une guidance n'est pas une
preuve de correction.

### Contrat de finding proposé

`PROPOSED` : toutes les revues Engineering Quality devraient produire un
format commun contenant au minimum :

- `id` stable de finding ;
- `category` : `BUG`, `RISK`, `TECHNICAL_DEBT`, `STYLE`, `OPTIMIZATION`,
  `SECURITY_ISSUE` ou `ARCHITECTURAL_ISSUE` ;
- `severity` : `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` ou `INFO` ;
- fichier et ligne, ou justification si la position est dynamique ;
- preuve observée et impact ;
- confiance ;
- statut préexistant/nouveau ;
- propriétaire ou agent responsable ;
- suggestion de correction, sans auto-application implicite ;
- nécessité d'une re-revue ;
- état : ouvert, accepté, corrigé, vérifié ou escaladé.

Ce contrat n'est pas encore créé dans le dépôt pendant cette phase d'audit.

## 8. REDONDANCES

### Matrice de couverture

| Solution | Code | Types | Tests | Errors | React | Security | Perf | Architecture |
|---|---|---|---|---|---|---|---|---|
| A Anthropic | Forte | Forte | Forte | Forte | Moyenne | Moyenne | Moyenne | Moyenne |
| B Vercel | Faible à moyenne | Moyenne | Faible | Faible | Forte | Faible | Forte | Moyenne |
| C Compound | Forte | Variable | Forte | Variable | Variable | Variable | Variable | Forte |
| D Trail of Bits | Moyenne orientée diff | Faible à moyenne | Moyenne | Moyenne | Faible | Forte | Faible | Forte sur blast radius |

### Doublons principaux

- A, C et l'actuel `tester-reviewer` couvrent tous la revue générale et les
  tests. Les lancer systématiquement ensemble produirait probablement des
  findings redondants.
- A `type-design-analyzer`, les règles de types internes et une future revue
  TypeScript couvrent le même axe. Une seule revue de type doit être routée
  pour un changement donné, avec complément ciblé si nécessaire.
- A `code-simplifier` et une future skill de simplification ont le même rôle.
  La simplification ne doit pas précéder la validation de la correction.
- B et une future revue React/Next interne couvrent performance, frontières
  Server/Client, data fetching et bundle. B est la source spécialisée ; la
  revue interne doit en faire respecter le contrat plutôt que recopier toutes
  ses règles.
- C peut agréger ou redispatcher les mêmes domaines que A et D. Son
  orchestration complète est donc susceptible de lancer plusieurs reviewers
  sur le même diff.
- D et `data-guardian` se croisent sur les changements de données, mais D
  apporte l'historique Git et le modèle adversarial ; les responsabilités sont
  complémentaires, pas interchangeables.

### Capacités uniques réellement utiles

- A : revue structurée de commentaires, tests, erreurs silencieuses, types et
  simplification dans Claude Code.
- B : guidance spécifique React/Next/performance avec classement par impact.
- C : mécanique d'agrégation, artefacts et revue multi-angle, mais au prix
  d'une grande surface opérationnelle.
- D : revue différentielle security-first, historique, blast radius et
  adversarial modeling.

### Décision d'architecture proposée

`DECISION PROPOSED` : ne pas installer les quatre solutions ensemble. Garder
le Project OS et ses agents comme autorité, puis intégrer au maximum une
capacité de guidance React/Next, une capacité de revue générale et une
capacité de revue différentielle high-risk, chacune déclenchée séparément.

## 9. RISQUES

| Risque | Impact | Probabilité | Détectabilité | Mitigation proposée |
|---|---|---|---|---|
| Intégration du plugin Compound complet | Très élevé : surface d'écriture, push et contexte | Moyenne | Moyenne | Ne pas installer le plugin complet ; extraire uniquement un besoin après contrat et test |
| Skill Vercel installée depuis le dépôt entier | Élevé : inclusion d'une capacité de déploiement | Moyenne | Élevée si inventaire, faible sinon | Utiliser seulement un snapshot du sous-chemin `react-best-practices`, sans skill de déploiement |
| Push/commit déclenché par une documentation externe | Critique pour la production | Faible à moyenne | Moyenne | Règle Project OS supérieure, Git en lecture seule par défaut, human gate obligatoire |
| Auto-fix non re-revu | Élevé : régression silencieuse | Moyenne | Faible sans re-review | Report-only par défaut, correction séparée, re-review ciblée obligatoire |
| Cross-model review avec données sensibles | Critique : exfiltration potentielle | Variable | Moyenne | Egress désactivé par défaut ; classification et human gate explicites |
| Licence Trail non résolue | Élevé : risque juridique de redistribution | Moyenne | Élevée | Obtenir la licence du plugin et l'avis humain avant copie |
| Guidance incompatible avec Next/React réels | Moyen à élevé : recommandation erronée | Moyenne | Moyenne | Contrôle de version et test sur le code concerné |
| Swarm permanent | Moyen à élevé : bruit, coût, findings contradictoires | Élevée si non routé | Élevée | Classifieur de risque, lazy loading, agrégation et déduplication |
| Reviewer traité comme gate de sécurité unique | Critique | Moyenne | Faible | Project OS security gate et `data-guardian` restent obligatoires |
| Agent qui conclut DONE sur compilation seule | Élevé | Moyenne | Moyenne | Contrat de preuves requirements → code → tests → review → régression → documentation |
| Git history fetch ou shell non borné | Élevé | Moyenne | Moyenne | Bash conditionnel, commandes read-only autorisées, scope de fichiers explicite |
| Findings redondants ou contradictoires | Moyen | Élevée avec A+C+D | Élevée | Schéma commun, IDs, déduplication, arbitrage par l'orchestrator |

La probabilité est qualitative et relative au design proposé ; elle ne remplace
pas une analyse de risque opérationnelle avant chaque intégration.

### Risques propres au projet actuel

- Le projet contient des données commerciales, un catalogue généré et des
  médias/PDF/3D documentés par `CLAUDE.md`. Une revue doit distinguer le code
  et les données protégées.
- Le flux de production est `push main → GitHub → Vercel Production`, selon
  les faits documentés dans le Project OS. Tout push doit donc être traité
  comme potentiellement productif, même si une skill se présente comme une
  simple étape de revue.
- Le projet ne possède pas encore de framework de tests unitaires/E2E ou de
  configuration ESLint identifiés. Les reviewers ne peuvent pas compenser
  seuls cette absence.

## 10. AGENTS SPÉCIALISÉS RECOMMANDÉS

Les agents ci-dessous sont des propositions d'architecture, pas des fichiers à
créer maintenant. Le principe retenu est de commencer par des modes ou skills
appelés par les agents existants, puis de séparer un agent uniquement si le
volume ou le risque le justifie.

| Agent/mode proposé | Responsabilité | Entrée | Sortie | Déclenchement | Ne doit pas être déclenché | Bloquant |
|---|---|---|---|---|---|---|
| `code-quality-reviewer` | Correction, lisibilité, duplication, complexité, maintenabilité | Diff ciblé + contexte | Findings normalisés | Toute modification de code non triviale | Documentation seule ou changement de média | `CRITICAL/HIGH` |
| `type-contract-reviewer` | Contrats TypeScript, invariants, types faibles, `any` inutile | Diff TS + usages | Findings de type/contrat | Types, données, API ou domaines | CSS pur sans contrat | `HIGH` si contrat cassé |
| `error-handling-reviewer` | Erreurs réseau, états impossibles, fallbacks, erreurs silencieuses | Diff + flux d'erreur | Scénarios et findings | Fetch, mutations, formulaires, I/O | Changement sans chemin d'erreur | `HIGH` pour perte de données |
| `react-next-reviewer` | Server/Client boundaries, rendering, data fetching, bundle et performance | Diff `app/`, `components/`, `lib/` concerné | Findings et recommandations contextualisées | Page/composant/route UI | Données ou docs sans UI | `HIGH` si régression fonctionnelle |
| `test-reviewer` | Qualité et suffisance des tests | Requirements, diff, tests et résultats CI | Gaps, cas limites, verdict | Toute logique observable | Changement documentaire pur | `CRITICAL/HIGH` gap critique |
| `security-differential-reviewer` | Diff, historique, blast radius, modèle adversarial | Diff/base/ref + classification | Findings sécurité et hypothèses | Authz, données sensibles, paiements, migrations, secrets, appels externes | Petite UI sans frontière sensible | `CRITICAL/HIGH`, human gate |
| `simplification-reviewer` | Réduction de complexité après correction | Diff corrigé + findings fermés | Suggestions non bloquantes | Refactor ou fin de tranche | Avant la validation correctness | Non, sauf risque introduit |
| `architecture-reviewer` | Couplage, frontières, dépendances et cohérence Project OS | Plan + diff transversal | Décisions, écarts, risques | API, DB, domaine, refactor transversal | Petite modification locale | Human gate selon impact |

### Relation avec les agents existants

- `orchestrator` garde le routage et l'arbitrage ; il ne devient pas un
  reviewer omniscient.
- `requirements-architect` reste responsable du besoin, du périmètre, des
  inconnues et des critères d'acceptation. Il remplit initialement le rôle
  architecture/contrat pour les changements transversaux.
- `builder` ne doit pas recevoir une capacité externe d'auto-fix ou de push.
  Toute correction suit la change policy et l'impact analysis.
- `tester-reviewer` couvre déjà tests, erreurs, régression et sécurité de
  base. Les reviewers externes sont des compléments ciblés, pas des
  remplaçants.
- `data-guardian` reste l'autorité pour provenance, unités, doublons et
  cohérence des données commerciales.
- `verificateur-rendus` reste spécialisé dans la vérification visuelle 3D et
  ne doit pas être remplacé par une revue de code générique.

### Agents à ne pas séparer immédiatement

`performance-reviewer`, `simplification-reviewer`, `architecture-reviewer`,
`type-contract-reviewer` et `error-handling-reviewer` peuvent d'abord être des
modes ciblés. Un nouvel agent ne devient justifié qu'après mesure d'un volume
de findings, d'une charge de contexte ou d'un conflit de responsabilité.

## 11. SKILLS RECOMMANDÉES

### À étudier pour une intégration future, sous conditions

- `react-best-practices` de Vercel, sous forme d'un snapshot minimal et
  read-only, sans installer le dépôt complet.
- Un sous-ensemble documenté du PR Review Toolkit d'Anthropic, de préférence
  utilisé côté Claude Code ou converti en contrat interne sans reprendre ses
  actions Git.
- Une capacité de revue différentielle Trail of Bits uniquement pour les
  changements à haut risque, après résolution de licence et d'egress.

### À ne pas créer maintenant

Aucune nouvelle skill, aucun agent spécialisé et aucune nouvelle règle ne doit
être créé dans cette phase d'audit.

### Skills internes à réutiliser

Les skills existantes `discovery`, `project-audit` et `testing` restent la
porte d'entrée pour l'audit, la découverte et la preuve. Elles ne doivent pas
être dupliquées par une copie externe sans différence explicitement documentée.

## 12. RULES RECOMMANDÉES

Les règles suivantes sont proposées pour une intégration future ; elles ne sont
pas encore écrites :

1. **Review precedence** : sécurité critique → human gate → Project OS → règles
   projet → règles spécialisées → skill externe → préférence de l'outil.
2. **Diff-only par défaut** : une revue porte sur le diff et son contexte
   nécessaire ; elle ne transforme pas une revue en audit global implicite.
3. **Report-only par défaut** : aucune écriture, auto-fix, commit, push ou
   déploiement ne découle d'un finding.
4. **Re-review obligatoire** : toute correction d'un finding bloquant doit être
   revérifiée sur le diff mis à jour.
5. **Evidence gate** : aucun verdict positif sans preuve de tests et de
   régression adaptée au risque.
6. **External egress deny-by-default** : une revue cross-model ou réseau est
   interdite sans classification, consentement et human gate.
7. **Generated/data protection** : les fichiers générés, données, médias,
   PDF et 3D restent soumis à leurs règles existantes.
8. **No security substitution** : aucune skill externe ne remplace le
   `data-guardian`, le `tester-reviewer`, la security gate ou la validation
   humaine.

## 13. MCP / OUTILS

### MCP

Aucun des quatre outils audités n'est un MCP. Aucun nouveau MCP n'est
recommandé pour cette phase. Le Playwright MCP déjà présent reste réservé à
la QA browser locale et doit être routé après les contrôles de code et de
tests, sans production ni compte réel.

### Permissions proposées

| Solution | READ | WRITE | NETWORK | SHELL | GIT | DEPLOY |
|---|---|---|---|---|---|---|
| A, report-only | `ALLOW` sur le scope | `DENY` sauf artefact approuvé | `DENY` | `CONDITIONAL` read-only | `ALLOW` read-only | `DENY` |
| B, guidance | `ALLOW` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| C, revue sélectionnée | `CONDITIONAL` | `CONDITIONAL` artefacts uniquement | `DENY` par défaut | `CONDITIONAL` | `ALLOW` read-only | `DENY` |
| D, high-risk | `ALLOW` sur diff/historique borné | `CONDITIONAL` rapport uniquement | `DENY` sauf human gate explicite | `CONDITIONAL` | `ALLOW` read-only | `DENY` |

Le `WRITE` vers un rapport n'est pas une autorisation de modifier le code.
Le `Bash` conditionnel doit être borné à des commandes non destructives et
spécifiques à la tâche. Les permissions documentaires ne sont pas une
frontière technique : les hôtes doivent aussi limiter réellement les outils
exposés.

### Capacité d'installation et maintenance

- A se distribue comme plugin Claude Code ; son installation marketplace n'est
  pas autorisée maintenant et sa portabilité Codex n'est pas prouvée.
- B possède des scripts de build/validation `pnpm`, mais ils ne sont pas
  nécessaires pour consommer un snapshot validé. `npx skills add` sur le dépôt
  complet est refusé car il peut inclure la skill de déploiement.
- C comporte des scripts et dépendances de développement, notamment autour de
  Bun, ainsi que plusieurs workflows et modes. Sa maintenance est donc lourde
  pour le besoin initial.
- D utilise des outils shell/Git pour son analyse et peut produire des
  artefacts. La maintenance et la redistribution dépendent de la licence
  effectivement applicable au plugin.

## 14. ROUTING PAR RISQUE

`PROPOSED` : le routage s'appuie d'abord sur les fichiers touchés, les
opérations demandées, les données traversées et le niveau d'impact. Il ne
lance pas tous les reviewers à chaque tâche.

| Scénario | Reviewers internes/externes nécessaires | Human gate |
|---|---|---|
| Petite modification UI | `tester-reviewer` ciblé ; `react-next-reviewer` si comportement/rendering ; Playwright/visuel si interaction ou responsive | Non, sauf production ou périmètre sensible |
| Nouveau composant React | Code/type + React/Next ; tests si état/comportement ; browser si parcours | Selon impact |
| Nouvelle page Next.js | Code + React/Next + tests ; architecture si frontière data ; browser/visuel si parcours utilisateur | Selon accès aux données |
| Nouvelle logique métier | `requirements-architect`, code/type/errors/tests ; `data-guardian` si données ; security si accès sensible | Oui si décision métier ou donnée sensible |
| Modification de données | `data-guardian`, tests et architecture ; security si accès/sensibilité | Oui pour migration ou données réelles |
| Authentification | Type/errors/tests/React/Next ; architecture ; Trail high-risk éventuel | Obligatoire |
| Permissions/autorisation | Architecture, types, erreurs, tests d'isolation, security differential | Obligatoire |
| Paiement | Requirements, data, tests, errors, security, architecture, simulation | Obligatoire |
| Commande | Requirements, data, tests, errors, security, architecture, simulation | Obligatoire |
| Stock | Requirements, data, tests, data-guardian, security, architecture, simulation | Obligatoire |
| Migration | Data, architecture, security differential, tests de rollback/résilience | Obligatoire ; pas de données réelles sans autorisation séparée |
| Refactor important | Architecture, code, types, tests, errors, simplification après correctness, régression | Selon blast radius |
| Changement de dépendance | Code/types, security, lockfile, build/tests ; review scripts si package lifecycle | Oui si script, secret ou production |
| Changement de configuration | Code + security ; vérifier CI, secrets, permissions et effets externes | Oui pour CI/prod/deploy |
| Bug critique | Review ciblée code/errors/tests ; security si frontière ; re-review obligatoire | Oui si données, sécurité ou production |
| Release | Preuves complètes, tests, régression, security, browser local et contrôle release | Obligatoire ; aucun agent ne déploie |

### Parallélisme

Le parallèle est autorisé uniquement pour plusieurs reviewers read-only,
indépendants, partageant le même snapshot du diff. Il est interdit lorsque :

- un résultat est nécessaire pour choisir le reviewer suivant ;
- une correction ou un mode `apply` est actif ;
- une décision humaine est attendue ;
- il existe une migration, une opération financière, un changement de
  permissions ou un risque de production ;
- deux agents pourraient écrire le même artefact ou modifier le même fichier.

L'orchestrator déduplique les findings par fichier, ligne, catégorie, preuve
et signature sémantique, puis arbitre les contradictions avec les règles du
Project OS. Une contradiction non résolue déclenche `STOP`.

## 15. WORKFLOW REVIEW → FIX → RE-REVIEW

Le cycle cible est :

`DISCOVER → ANALYZE → PLAN → IMPLEMENT → TEST → REVIEW → FINDINGS → FIX →
RE-REVIEW → SIMULATE → SECURITY CHECK → REGRESSION → DOCUMENT → UPDATE MEMORY →
VERIFY → DONE / ESCALATE`

### Règles du cycle

1. `DISCOVER` capture la branche, le diff, les fichiers, les instructions et
   les tests applicables.
2. `ANALYZE` classe le risque et identifie les domaines réellement concernés.
3. `PLAN` définit les reviewers, les preuves attendues, le scope et le
   rollback.
4. `IMPLEMENT` reste sous le contrôle du `builder` et de la change policy.
5. `TEST` exécute d'abord les validations les plus spécifiques.
6. `REVIEW` produit uniquement des findings avec preuve et confiance.
7. `FIX` est une nouvelle action autorisée, jamais un effet implicite de la
   revue. Elle réutilise le scope et l'impact analysis.
8. `RE-REVIEW` est obligatoire pour tout finding `CRITICAL/HIGH` et pour tout
   finding modifié par la correction. Le reviewer doit confirmer que le
   finding est fermé et qu'aucune régression connexe n'est introduite.
9. `SIMULATE`, `SECURITY CHECK` et `REGRESSION` deviennent bloquants selon le
   niveau de risque.
10. `DONE` est interdit sur la seule base d'un build vert ou d'une absence de
    findings d'un seul outil.

### Verdicts proposés

| Sévérité | Traitement proposé |
|---|---|
| `CRITICAL` | Bloque immédiatement ; STOP, correction et re-review ; human gate si sécurité/data/production |
| `HIGH` | Bloque le passage ; correction ou acceptation humaine explicite et tracée |
| `MEDIUM` | Correction demandée ou acceptation documentée avant release ; peut être non bloquant pour un prototype isolé |
| `LOW` | Non bloquant, suivi de dette ou correction opportuniste |
| `INFO` | Information, aucune correction obligatoire |

Un finding doit préciser s'il s'agit d'un bug, risque, dette technique, style,
optimisation, problème de sécurité ou problème architectural. Aucun finding ne
doit être promu automatiquement en bug.

### Limites des solutions auditées

- A recommande une re-run après les fixes, mais son workflow documenté ne
  remplace pas le contrat de re-review du Project OS.
- B fournit des règles, pas la boucle d'exécution ni la preuve de correction.
- C fournit une mécanique de revue/artefacts et des modes d'application, mais
  son auto-configuration et ses workflows sont trop larges pour servir de
  boucle implicite.
- D produit une revue différentielle et des éléments adversariaux, mais ne
  valide pas à lui seul les requirements, le métier, la régression ou la
  release.

## 16. COÛT CONTEXTUEL

### Coûts identifiés

- A consomme du contexte par reviewer spécialisé et par lecture de diff ; six
  reviewers sur une petite modification sont disproportionnés.
- B est peu coûteuse à l'exécution car c'est surtout une guidance, mais elle
  ajoute du bruit si toutes les règles sont injectées sur un changement non
  React/Next.
- C est la plus coûteuse en orchestration, références, artefacts, scripts et
  éventuelles revues croisées.
- D coûte davantage sur l'historique, le blast radius et l'analyse adversariale,
  mais ce coût est justifié uniquement par un changement à risque élevé.

### Réduction proposée

- charger les skills et références à la demande (`lazy loading`) ;
- limiter l'analyse au diff et au contexte nécessaire (`diff-based review`) ;
- router par fichiers/opérations/risk signals ;
- agréger dans un schéma commun plutôt que recopier les rapports ;
- dédupliquer les findings par signature et preuve ;
- ne lancer les revues browser, sécurité ou architecture que si leur signal est
  présent ;
- éviter les revues cross-model et les swarms persistants ;
- stocker un résumé et les artefacts nécessaires, pas tout l'historique du
  contexte dans la mémoire active.

La consommation réelle de tokens, la durée et le coût n'ont pas été mesurés
dans ce dépôt. Ils restent `UNKNOWN` jusqu'à un pilote contrôlé.

## 17. ARCHITECTURE CIBLE

### Architecture retenue proposée

```text
PROJECT OS
    |
    v
EXISTING ORCHESTRATOR
    |
    v
RISK CLASSIFIER (scope, paths, operation, data sensitivity)
    |
    +--> requirements-architect / data-guardian when indicated
    +--> targeted code/type/error/test review modes
    +--> React/Next guidance when UI or framework code changes
    +--> browser QA only for local user-facing behavior
    +--> differential security review only for high-risk changes
    |
    v
FINDING NORMALIZATION + DEDUPLICATION + CONTRADICTION CHECK
    |
    v
EXISTING TESTER-REVIEWER + CI EVIDENCE
    |
    v
SIMULATION / SECURITY GATE / REGRESSION according to risk
    |
    v
HUMAN GATE when required
    |
    v
FIX (separate authorized action) -> TARGETED RE-REVIEW -> VERIFY
```

Cette architecture est meilleure qu'un swarm permanent car elle conserve le
centre de décision dans l'orchestrator, appelle les spécialistes à la demande
et rend les permissions et preuves explicites. Elle ne donne à aucun outil
externe le pouvoir de modifier l'autorité, les règles ou le cycle de release.

### Ce qui reste volontairement hors de la cible initiale

- orchestrateur externe Compound complet ;
- auto-fix généralisé ;
- revue cross-model par défaut ;
- agent séparé pour chaque catégorie avant mesure du besoin ;
- intégration de déploiement ou de workflow Git ;
- MCP supplémentaire.

## 18. CE QUI NE DOIT PAS ÊTRE INSTALLÉ

Tant qu'une décision humaine dédiée n'a pas été prise, ne pas installer :

- le dépôt complet `vercel-labs/agent-skills`, car il contient une capacité de
  déploiement distincte ;
- le plugin Compound Engineering complet, notamment sa skill
  `ce-commit-push-pr` ;
- la marketplace Trail of Bits complète ;
- une copie de Trail of Bits avant résolution de la licence du plugin ;
- une version `@latest`, une branche mouvante ou un snapshot sans SHA ;
- un MCP ou outil de code review supplémentaire ;
- un mode auto-fix, pipeline, commit, push, PR ou deploy fourni par une
  capacité externe ;
- une revue cross-model sans classification des données et human gate ;
- l'ancienne skill séparée `next-best-practices` si la guidance est déjà
  fournie par les documents versionnés de Next.js ;
- des agents projet qui dupliquent `tester-reviewer`, `data-guardian` ou
  `verificateur-rendus` sans preuve de besoin.

## 19. PHASE D'INTÉGRATION FUTURE

L'ordre suivant est `PROPOSED` et ne constitue pas encore une autorisation :

### Phase 0 — Acceptation de l'audit

- valider les sources, licences, versions et questions ouvertes ;
- décider si une capacité Claude-native suffit ou si une parité Codex est
  obligatoire ;
- ne modifier que le document d'audit si une conclusion est corrigée.

### Phase 1 — Contrat interne de qualité

- définir le schéma de finding ;
- définir les sévérités, catégories, états et règles de re-review ;
- définir les preuves minimales et les artefacts de run ;
- ne pas intégrer de fournisseur externe dans cette phase.

### Phase 2 — Baseline locale

- choisir séparément un lint, un framework de tests et les commandes CI ;
- mesurer l'état initial sans refactor métier ;
- vérifier la compatibilité Next.js/React/TypeScript du dépôt.

### Phase 3 — Guidance React/Next

- épingler uniquement le sous-ensemble Vercel accepté ;
- exclure toute skill de déploiement ;
- prouver la découverte et l'utilisation contrôlée dans Codex et Claude Code ;
- tester sur une tâche non métier et sans modification du site existant.

### Phase 4 — Revue générale contrôlée

- évaluer un sous-ensemble du PR Review Toolkit ;
- report-only, diff-only, sans auto-fix et sans Git write ;
- comparer ses findings à `tester-reviewer` et dédupliquer.

### Phase 5 — Routage Project OS

- implémenter le classifieur et l'agrégateur internes si le pilote le justifie ;
- conserver `orchestrator` comme point de décision ;
- exécuter les reviewers en parallèle uniquement lorsqu'ils sont read-only et
  indépendants.

### Phase 6 — Revue différentielle high-risk

- résoudre la licence Trail of Bits ;
- décider si les données peuvent sortir de la machine ;
- borner Bash/Write/Git ;
- lancer uniquement sur authz, paiements, migrations, données sensibles,
  secrets, appels externes et changements à fort blast radius.

### Phase 7 — Évaluation Compound ciblée

- considérer seulement ses patterns d'agrégation ou une skill strictement
  report-only ;
- ne pas installer le plugin complet sans justification de maintenance,
  permissions, egress et sécurité ;
- arrêter l'évaluation si elle duplique le système interne.

### Phase 8 — Pilote et décision

- choisir une modification documentaire/configuration non métier ;
- recueillir coûts, findings, re-review, bruit et preuves ;
- effectuer un audit indépendant ;
- décider explicitement ce qui est intégré, refusé ou différé.

Chaque phase doit avoir son impact analysis, son rollback et son human gate
lorsqu'une permission, une licence, une donnée ou une production est
concernée.

## 20. OPEN QUESTIONS

1. Quel SHA propre au chemin `plugins/pr-review-toolkit` Anthropic doit être
   retenu pour une intégration reproductible ?
2. La parité runtime Codex/Claude Code est-elle obligatoire pour chaque revue,
   ou une capacité Claude-native est-elle acceptable ?
3. Quelle licence distincte s'applique exactement au plugin Trail of Bits
   `differential-review` ?
4. Les revues cross-model sont-elles autorisées, sur quels types de données et
   vers quelles destinations ?
5. Quel framework de lint et de tests doit être choisi pour le dépôt Next.js
   actuel, sans modifier le code métier ?
6. Quelles règles Vercel sont compatibles avec Next.js `^15.5.25` et React
   `^18.3.1` ?
7. À partir de quel niveau un finding `MEDIUM` bloque-t-il une phase ou une
   release ?
8. Où les rapports détaillés et artefacts de revue doivent-ils être conservés
   sans gonfler la mémoire active ?
9. Les fichiers d'extension non suivis actuellement font-ils partie du scope
   de la future revue, ou leur commit doit-il être traité séparément ?
10. Qui valide les exceptions aux règles de permissions, à l'egress et aux
    human gates ?
11. Quel est le mécanisme de rollback accepté pour une correction automatique
    locale, si une telle correction est un jour autorisée ?
12. Quels critères mesurables permettront de séparer un agent spécialisé d'un
    simple mode du `tester-reviewer` ?

## QUESTION STATUS

La resolution detaillee de chacune des 12 questions ouvertes, avec question,
evidence, decision, justification et impact, est documentee dans
`docs/architecture/ENGINEERING_QUALITY_ARCHITECTURE.md`.

Statuts de consolidation :

1. `DECIDED WITH CONDITION` : utiliser le commit de chemin officiel
   `f7ab5c799caf2ec8c7cd1b99d2bc2f158459ef5e`, avec revalidation au moment de
   l'integration.
2. `DECIDED` : parite obligatoire pour les contrats Project OS communs, pas
   necessaire pour chaque outil externe runtime-specific.
3. `DEFERRED` : licence propre au plugin Trail of Bits non etablie ; revue
   juridique obligatoire avant toute copie ou redistribution.
4. `DECIDED` : cross-model et egress denies par defaut, exception uniquement
   par human gate et classification explicite.
5. `DECIDED WITH CONDITION` : baseline actuelle conservee ; framework cible
   reporte a une phase de baseline dediee.
6. `DECIDED WITH CONDITION` : sous-ensemble Vercel controle et applicable
   seulement apres verification de version ; le reste est conditionnel ou
   ignore.
7. `DECIDED` : un MEDIUM bloque selon contexte de risque, acceptation ou
   correction tracee sinon.
8. `DECIDED TARGET` : rapports dans `docs/quality/runs/<run-id>/`, resume dans
   l'etat projet/memoire.
9. `DECIDED` : extensions non suivies hors scope par defaut, snapshot dedie
   avant tout commit.
10. `DECIDED WITH CONDITION` : validateur humain nomme dans chaque gate ;
    absence d'identite identifiable = STOP.
11. `DECIDED WITH CONDITION` : pas d'auto-fix aujourd'hui ; protocole de
    rollback cible defini avant toute autorisation future.
12. `DECIDED WITH CONDITION` : seuil de creation defini, mesure sur trois runs
    requise avant toute creation.

## CONCLUSION D'AUDIT

### AUDIT TERMINÉ : ARCHITECTURE PROPOSÉE SOUS CONDITIONS

Les quatre sources ont été auditées à partir de leurs dépôts officiels et
leurs natures ont été séparées. Aucune intégration n'est autorisée par ce
document. Les décisions et conditions actuellement applicables sont
consolidées dans `docs/architecture/ENGINEERING_QUALITY_ARCHITECTURE.md` :
revalidation du SHA Anthropic avant intégration, revue juridique de la licence
Trail of Bits, choix futur de la baseline de qualité, sous-ensemble Vercel
contrôlé, et validation humaine de toute permission externe ou egress.

Le Project OS actuel reste l'autorité. Les agents et skills existants ne sont
pas remplacés. Le site, les données métier, l'architecture applicative, les
médias, les PDF, les modèles 3D, Git et le déploiement ne sont pas modifiés par
cet audit.
