# ADR-0005 — Le dépôt vit hors de OneDrive

```text
ID: ADR-0005
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: Le dépôt Git vit dans `C:\Users\massi\Projects\aciers-grosjean`, comme les autres projets de la machine. Il n'est plus dans `OneDrive\Bureau\Site Aciers Grosjean`. Seul `_DEPOT/` (photos brutes, documents, rendus 3D en attente) reste dans OneDrive, monté dans le dépôt par une jonction NTFS : toujours sauvegardé par OneDrive, toujours ignoré par Git. La tâche planifiée « Site Aciers Grosjean - synchro GitHub » a été réinstallée depuis le nouveau dossier. `tests/test_emplacement.py` (E1, E2) refuse tout retour sous un chemin OneDrive et toute jonction cassée.
REASON: Décision H1, ouverte depuis le 14/09. OneDrive remplaçait 1 767 fichiers de `.git` par des placeholders « en ligne seulement », verrouillait les fichiers pendant la synchro (Errno 22 vu le 16/09 sur l'intégration des visuels), et rendait `npm install` interdit dans le dossier — au point que la vérification locale passait par une copie dans `%LOCALAPPDATA%`. GitHub est déjà la sauvegarde du code ; OneDrive n'apportait rien sur `.git` et y ajoutait le mode de corruption le plus classique d'un dépôt. Le 21/09, un agent a lancé `npm ci` et un build dans le dossier OneDrive malgré la règle, ce qui a mis des dizaines de milliers de fichiers en file de synchronisation : la règle écrite ne suffisait pas, il fallait que l'emplacement lui-même soit contrôlé.
IMPACT: Le dépôt a été reconstitué par `git clone` depuis GitHub puis `git fetch` du dossier OneDrive pour les deux commits locaux non poussés (c19aff9, b5467d3) — sans jamais déplacer physiquement un `.git` plein de placeholders. Les six fichiers non commités ont été copiés. `fsck` propre. `CLAUDE.md`, `tests/test_lint.py`, `scripts/inventaire/analyser.py` (seul chemin absolu du code), `project-state/CURRENT_STATE.md` et `_DOCS/CHANTIERS-RENFORCEMENT.md` mis à jour. Socle : +2 contrôles. L'ancien dossier OneDrive garde `_DEPOT/` et ses boutons `.cmd` doivent être remplacés par un renvoi vers le nouveau dossier. Un contrôle « aucun placeholder dans `.git` » a été écrit puis retiré : il n'a jamais été vu rouge (les lectures de la séance avaient hydraté les fichiers avant lui), et un contrôle jamais vu rouge ne prouve rien.
SUPERSEDES: —
VALIDATED_BY: Massimo, réponse « Déplacer vers Projects » à la question H1 posée par Claude le 2026-09-21. Exécution et contrôles écrits par Claude le même jour.
```

## Contexte

`_DOCS/CHANTIERS-RENFORCEMENT.md`, ligne H1, ouverte le 14/09 : « `.git`, `index`, `HEAD`,
`config` sont des placeholders OneDrive (`ReparsePoint` vérifié). Rien n'est cassé aujourd'hui,
mais c'est le mode de corruption classique d'un dépôt Git, et la tâche tourne toutes les 2 h sans
personne devant. » A4 (`git gc`) était bloquée par H1.

## Ce qui a été fait, dans l'ordre

1. Commit `b5467d3` dans l'ancien dossier pour partir d'un arbre propre.
2. `git clone` public dans `Projects\aciers-grosjean`, puis `git fetch` de l'ancien dossier et
   `merge --ff-only` : GitHub était deux commits en retard.
3. Copie des six fichiers non commités (formulaire, route, `.env.example`, contrôles, `package.json`
   et son lock).
4. Jonction `_DEPOT` → `OneDrive\...\_DEPOT` ; `git check-ignore` confirme qu'elle est ignorée.
5. `npm ci`, `npm run build`, registre complet dans le nouveau dossier.
6. Tâche planifiée réinstallée (`_OUTILS/installer-synchro-auto.ps1`, chemins relatifs).

## Rollback

Le dossier OneDrive n'a pas été supprimé. Réinstaller la tâche planifiée depuis
`OneDrive\Bureau\Site Aciers Grosjean\_OUTILS\`, y reporter les commits faits depuis dans
`Projects` (`git fetch` dans l'autre sens), retirer la jonction, marquer cet ADR `DEPRECATED`.
Le contrôle E1 redeviendra rouge : abaisser le socle et l'écrire dans `_DOCS/LECONS.md`.
