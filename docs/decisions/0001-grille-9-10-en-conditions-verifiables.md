# ADR-0001 — La cible « 9/10 par couche » est traduite en conditions vérifiables

```text
ID: ADR-0001
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: La cible « amener les trois couches d'architecture à 9/10 » ne s'évalue pas par une note attribuée par l'agent. Elle est traduite en seize conditions que le dépôt vérifie lui-même, consignées dans la section « GRILLE 9/10 » de _DOCS/CHANTIERS-RENFORCEMENT.md (T1 à T5 pour la couche technique, I1 à I5 pour l'information, G1 à G6 pour la gouvernance). La boucle s'arrête quand ces conditions sortent vertes, pas quand l'agent estime que c'est bien.
REASON: Un objectif auto-noté n'est pas un objectif, c'est une permission : il suffirait à l'agent de déclarer 9/10 pour terminer. C'est le mécanisme exact qui a produit « PROUVÉ : working tree propre » dans project-state/CURRENT_STATE.md au moment même où git status montrait ce fichier modifié. Une condition d'arrêt doit être une sortie de commande, pas un avis.
IMPACT: Six lignes de chantier ont été créées pour rendre la grille atteignable (C17, C18, C19, D16, D17, D18), portant le lot de 54 à 60 tâches. L'objectif de la boucle gagne une septième condition (g). Plafond assumé : 9/10 est le maximum atteignable sans décision humaine, le dixième point de la couche technique dépendant de H4 (backend des formulaires) et celui de la gouvernance de H1 (sortie de OneDrive).
SUPERSEDES: —
VALIDATED_BY: Massimo pour la cible 9/10 (demande du 21/09/2026). Traduction en seize conditions écrite par Claude le 21/09/2026 : à confirmer explicitement.
```

## Contexte

L'audit du 21/09 (`_DOCS/AUDIT-STRUCTURE-2026-09-21.md`) note les trois couches d'architecture
7, 5 et 3,5 sur 10. La demande qui suit est de les amener toutes à 9.

Le problème n'est pas la cible, il est le juge. Les notes de l'audit sont des jugements ; les
reprendre comme condition d'arrêt d'une boucle autonome revient à confier au coureur le
chronomètre. La traduction en conditions mécaniques conserve l'exigence et retire le juge.

## Conséquence pratique

Aucune itération ne peut clore la boucle en affirmant un progrès. Les seize conditions sont
listées, numérotées, et chacune renvoie à la ligne de chantier qui la porte.
