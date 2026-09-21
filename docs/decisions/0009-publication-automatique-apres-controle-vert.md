# ADR-0009 — La publication va jusqu'à Vercel, et la fusion est automatique quand le contrôle est vert

```text
ID: ADR-0009
DATE: 2026-09-22
STATUS: ACTIVE
DECISION: La chaîne de publication va jusqu'au bout sans intervention : `_OUTILS/SAUVEGARDER.cmd` commite, pousse la branche, puis `scripts/publier.ps1` crée la pull request, attend le contrôle `quality` et fusionne dans `main` — ce qui déclenche le déploiement Vercel de production. La fusion est refusée dans tous les autres cas : contrôle rouge, contrôle toujours en cours après 12 minutes, GitHub injoignable, fusion refusée par une règle du dépôt. Le mode `auto` de la tâche planifiée ne pousse toujours rien et ne fusionne jamais. L'adresse unique à regarder est https://aciers-grosjean.vercel.app.
REASON: Demande explicite du propriétaire le 22/09 : « à chaque fois qu'il y a une modification, je le voie directement via Vercel, parce que c'est la seule façon dont je vois tes modifications ». Le constat qui la motive est mesuré : la production Vercel était restée à `54d93a2` (17/09) pendant cinq jours de travail, parce que `main` est protégée et qu'aucune pull request n'avait jamais été ouverte. Pousser une branche ne change rien à ce que le propriétaire voit ; seule la fusion déplace la production. Une revue humaine qui n'a jamais lieu ne protège rien — elle laisse seulement le propriétaire regarder un site périmé en croyant voir le travail. Le vrai garde-fou est le contrôle `quality` (typecheck, lint, build, registre complet), qui lui s'exécute à chaque fois.
IMPACT: Lève l'interdiction absolue « aucun agent ne fusionne une pull request » de `docs/architecture/SYNC_POLICY.md`, remplacée par « aucune fusion sans contrôle vert ». Risque assumé : la production Vercel est la préproduction `aciers-grosjean.vercel.app`, protégée par Vercel Authentication et non indexée (`SITE_INDEXABLE` absent) ; le site réel `www.aciersgrosjean.be` est maintenu séparément par l'agence et n'est pas touché. Une régression publiée est donc visible par le propriétaire seul, et se répare par `git revert -m 1 <sha de fusion>` ou un rollback Vercel. Le jeton utilisé est celui que Git emploie déjà pour pousser (`git credential fill`) : aucun secret nouveau, rien d'écrit sur le disque, rien d'affiché. La fenêtre du bouton reste ouverte 2 à 5 minutes, le temps du contrôle.
SUPERSEDES: —
VALIDATED_BY: Massimo, demande du 2026-09-22 (« fais en sorte que la pull request soit fusionnée, et applique ça définitivement »). Première fusion — PR #1, 14 commits — faite le même jour après contrôle `quality` vert.
```

## Ce qui reste interdit

- Fusionner sans contrôle vert, ou pendant qu'il tourne.
- Pousser ou fusionner depuis le mode `auto` de la tâche planifiée (ADR-0003).
- Toucher au site réel `www.aciersgrosjean.be`.
- Activer l'indexation (`SITE_INDEXABLE`) : décision H2, toujours ouverte.

## Rollback

Retirer l'appel à `publier.ps1` dans `_OUTILS/synchro.ps1` : le bouton redevient un simple push
et donne le lien de la pull request. Retirer S5 de `tests/test_gate.py`, abaisser le socle avec
une ligne dans `_DOCS/LECONS.md`, marquer cet ADR `DEPRECATED`.
