# État courant du projet

ÉTAT AU: 2026-09-21

**Source unique de l'état.** Ce fichier est le point d'entrée ; le détail de chaque chantier vit
dans son propre fichier d'avancement, listé ci-dessous. `memory/ACTIVE_CONTEXT.md` ne décrit plus
l'état : il ne contient que les références et les règles de travail.
Qui fait autorité sur quoi : `_DOCS/INDEX.md`.

## REPRENDRE ICI

| Piste | Où elle en est | Fichier d'avancement |
|---|---|---|
| Renforcement du dépôt | 16 tâches fermées sur 61, **81 contrôles, 0 échec** (départ 35), grille 9/10 à 4 conditions sur 16. Lots Z et A terminés, B en cours | `_DOCS/CHANTIERS-RENFORCEMENT.md` |
| Visuels 3D des fiches produit | 455 fiches sur 477 en ligne, 22 en attente de réponse du propriétaire, rapport final au propriétaire jamais rendu | `_DOCS/rendus-3d/avancement.md` |
| ERP | non commencé. Aucune verticale métier autorisée avant validation d'une première verticale | — |

**Prochaine action** : poursuivre le lot Z de `_DOCS/CHANTIERS-RENFORCEMENT.md`.

**En attente du propriétaire** : 8 décisions (H1 à H8, listées dans
`_DOCS/CHANTIERS-RENFORCEMENT.md`) et la confirmation de 2 ADR tranchés par l'agent
(ADR-0001, ADR-0002).

## Phase

Phase 1 — socle interne. Gouvernance Project OS et fondation Engineering Quality implémentées ;
depuis le 21/09, chantier de renforcement : transformer les règles écrites en contrôles exécutables.

Objectif : disposer d'un dépôt fiable avant de construire l'ERP. Aucune fonctionnalité métier ERP
ne commence avant validation d'une première verticale.

## Terminé

- Audit du dépôt, du dossier métier et de l'architecture V3.
- Contrat interne Engineering Quality, transitions, agrégation et routing diff-first, sans
  dépendance externe. Modes ajoutés aux agents existants, aucun nouvel agent créé.
- Audit de structure complet du dossier : `_DOCS/AUDIT-STRUCTURE-2026-09-21.md`.
- Socle d'auto-contrôle : registre `tests/lancer.py` avec invariant de non-régression, carnet de
  leçons, journal des décisions, index des sources.

## Problèmes connus

- Aucun backend, API, base de données, authentification, permission, stock, pricing ou commande.
- ~~La CI ne s'exécute sur aucun commit du chemin de production~~ → **corrigé le 21/09** (B1, B2) :
  `quality.yml` se déclenche sur `push` vers `main`, et un contrôle l'exige désormais.
- ~~`.gitignore` ne couvre pas `.env` sur un dépôt public~~ → **corrigé le 21/09** (A1), gardé par
  `tests/test_depot.py` qui interroge `git check-ignore`.
- `.git` est synchronisé par OneDrive. Décision **H1**, toujours ouverte.
- 22 redirections 301 pointent vers des pages inexistantes. Ligne **D1**.
- Les données du catalogue ont plusieurs sources et certains conflits restent ouverts.
- Doubles sources d'état et de questions ouvertes : nommées dans `_DOCS/INDEX.md`.

## Déploiement

- Flux vérifié : `PUSH main → GitHub → Vercel Production Deployment`, branche de production `main`.
- Dernier déploiement connu : commit `54d93a2`.
- Tout push sur `main` peut affecter la production et exige un human gate.
- La configuration Vercel ne doit pas être modifiée à ce stade.

## Ce qui est prouvé, ce qui ne l'est pas

### PROUVÉ le 21/09/2026

- `python tests/lancer.py` : 52 contrôles, 1 échec connu (`test_extensions.py:118-131`, ligne **B3**).
- Aucun commit automatique Git ni hook Git actif. `_OUTILS/synchro.ps1` mode `auto` ne pousse plus.
- Aucun secret dans les 69 commits de l'historique ; `_DEPOT/` n'a jamais été commité.

### UNKNOWN

- L'état temps réel de OneDrive, ses conflits, fichiers en attente et verrous.
- La protection effective de `main` dans GitHub. Décision **H2**.
- Les paramètres GitHub/Vercel non accessibles depuis le dépôt.
- La découverte runtime des skills externes sous Codex.

*Note du 21/09 : une mention déclarait ici comme établie la propreté de l'arbre de travail. Elle
était fausse à l'instant même où elle a été écrite — parmi les trois fichiers modifiés depuis le
17/09 figurait celui-ci. Un état ne se prononce plus là-dessus : c'est une donnée volatile,
mesurable en une commande, qu'aucun document ne peut garantir.
`tests/test_etat.py` refuse désormais cette affirmation.*

## Extensions externes

UI/UX Pro Max `2.13.0` et Anthropic `frontend-design` intégrés sous `.claude/skills/` et
`.agents/skills/`, parité binaire PASS. Playwright MCP `0.0.81` configuré dans `.mcp.json` pour une
QA locale isolée, sans credentials ; `browser_run_code_unsafe` exposé techniquement mais interdit
par la politique interne. Découverte runtime : PASS sous Claude Code (les deux skills apparaissent
dans les sessions), UNKNOWN sous Codex. Détail et limites : `docs/architecture/EXTENSION_DISCOVERY.md`.

## Décisions critiques

Les décisions tranchées sont versionnées dans `docs/decisions/` au gabarit de
`docs/decisions/README.md`. Une question qui a un ADR ne se repose pas (`CLAUDE.md:12`).

- Le dossier métier est la référence fonctionnelle ; l'architecture V3 la référence de gouvernance.
- Les inconnues métier ne sont jamais transformées silencieusement en règles.
- Aucune migration ni opération de production n'est autorisée à ce stade.
- Les outils externes Anthropic, Vercel, Trail of Bits et Compound restent différés.
