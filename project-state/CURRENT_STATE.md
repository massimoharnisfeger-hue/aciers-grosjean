# État courant du projet

## Phase

Phase 1 — Minimum Project OS et correction de gouvernance — vérifiée.

## Objectif courant

Construire et vérifier le socle de gouvernance permettant de travailler sur le futur ERP sans modifier encore ses fonctionnalités métier.

## Terminé

- Audit du dépôt, du dossier métier et de l'architecture V3.
- Master Plan validé.
- Dépôt propre avant construction du Project OS.

## En cours

- Aucun chantier d'implémentation métier autorisé.

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

- Audit statique et vérification Git : 17/09/2026.

## Prochaine action

- Faire valider humainement la prochaine verticale métier avant toute implémentation.

## Décisions critiques

- Le dossier métier est la référence fonctionnelle.
- L'architecture V3 est la référence de gouvernance et d'exécution.
- Les inconnues métier ne sont jamais transformées silencieusement en règles.
- Aucune migration ni opération de production n'est autorisée à ce stade.
- Les contrôles Project OS et de gouvernance passent : 13 tests structurels et contrôle de cohérence.
