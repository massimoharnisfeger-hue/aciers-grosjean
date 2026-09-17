# État courant du projet

## Phase

Phase 1 — Engineering Quality Foundation — socle interne implémenté et testé.

## Objectif courant

Maintenir le socle de gouvernance et de qualité permettant de travailler sur le futur ERP sans modifier encore ses fonctionnalités métier ni intégrer d'outil externe.

## Terminé

- Audit du dépôt, du dossier métier et de l'architecture V3.
- Master Plan validé.
- Dépôt propre avant construction du Project OS.
- Contrat interne Engineering Quality, transitions, agrégation minimale et
  routing diff-first implémentés sans dépendance externe.
- Modes ciblés ajoutés aux agents existants : aucun nouvel agent créé.
- Workflow `REVIEW → FINDINGS → FIX → RE-REVIEW → TEST → REGRESSION → GATE`
  et règles report-only documentés et testés.

## Couche d'extensions

### Validation runtime finale (17/09/2026)

- Codex : fichiers et structure PASS pour UI/UX Pro Max et frontend-design ; decouverte runtime UNKNOWN pour les deux. La session fraiche a lu les chemins `.agents/skills/`, mais n'a explicitement active aucune de ces skills.
- Claude Code : fichiers et structure PASS pour les deux skills ; decouverte runtime UNKNOWN pour les deux. La sonde fraiche s'est arretee sur la limite hebdomadaire de l'hote avant toute reponse de session.
- Parite `.claude/skills/` / `.agents/skills/` : PASS ; contenus, versions, SHA et provenances concordants.
- Playwright MCP : PASS pour version `0.0.81`, protocole stdio, outils, navigation et snapshot d'une fixture locale avec profil isole ; condition technique : le navigateur attendu par la configuration par defaut n'etait pas present sur l'hote, et aucun installateur n'a ete execute.
- Securite : CONDITIONS ; `browser_run_code_unsafe` est expose techniquement par le MCP mais interdit par la politique interne (`EXPOSED / POLICY-DENIED`). Aucun credential, acces production, commit, push ou deploiement n'a ete utilise.

- UI/UX Pro Max `2.13.0` est intégré sous `.claude/skills/` et `.agents/skills/` depuis `15de38fb70bc80ae9276fa7703b48ae861a672e6`.
- Anthropic `frontend-design` est intégré sous les deux mêmes arbres depuis `34040c9c568585f6929bedeaad110ad08f079624`.
- Playwright MCP `0.0.81` est configuré dans `.mcp.json` pour une QA locale isolée et sans credentials.
- Parité binaire, validation des données et probe MCP local : PASS ; découverte runtime Codex et Claude Code : `UNKNOWN` pour les deux skills, avec les limitations hôte documentées dans `docs/architecture/EXTENSION_DISCOVERY.md`.
- Aucun commit, push, déploiement, migration ou fichier métier n'a été effectué dans cette phase.

## En cours

- Aucun chantier d'implémentation métier ni intégration externe autorisé.

## Bloqué

- Aucune fonctionnalité métier ERP ne doit commencer avant validation d'une première verticale.

## Problèmes connus

- Aucun backend, API, base de données, authentification, permission, stock, pricing ou commande n'existe encore.
- Les données du catalogue ont plusieurs sources et certains conflits restent ouverts.
- `_OUTILS/synchro.ps1` conserve un mode humain de sauvegarde ; son mode `auto` ne pousse plus automatiquement.

## Déploiement vérifié

- Le projet Vercel est connecté au dépôt GitHub.
- La branche de production est `main` et le déploiement de production est actif.
- Flux vérifié : `PUSH main → GitHub → Vercel Production Deployment`.
- Le dernier déploiement visible correspond au commit `4afabb3`.
- Tout push sur `main` est une opération pouvant affecter la production et exige un human gate.
- La configuration Vercel ne doit pas être modifiée à ce stade.

## Dernière validation

- Fondation Engineering Quality et régression Project OS : 17/09/2026.

## Prochaine action

- Faire valider humainement le socle Engineering Quality avant toute
  intégration externe ou sélection d'une verticale métier.

## Décisions critiques

- Le dossier métier est la référence fonctionnelle.
- L'architecture V3 est la référence de gouvernance et d'exécution.
- Les inconnues métier ne sont jamais transformées silencieusement en règles.
- Aucune migration ni opération de production n'est autorisée à ce stade.
- Les contrôles Project OS et de gouvernance passent : 14 tests structurels,
  15 tests Engineering Quality, 6 tests extensions, contrôles de cohérence et
  validation du contrat.
- Les outils externes Anthropic, Vercel, Trail of Bits et Compound restent
  différés ; le socle interne fonctionne sans eux.
