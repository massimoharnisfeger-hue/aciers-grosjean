# Politique de synchronisation et de publication

Ces opérations sont distinctes :

- `AUTO-SAVE` : écriture locale d'état, mémoire, rapports ou handoff dans le périmètre autorisé. Elle ne touche ni Git distant ni production.
- `AUTO-COMMIT` : interdit dans une boucle agentique par défaut. Un commit nécessite une demande humaine explicite et un diff vérifié.
- `AUTO-PUSH` : interdit pour les changements du projet. Même un commit existant ne doit pas être poussé automatiquement.
- `DEPLOY` : séparé de Git et de la CI. Aucun déploiement automatique depuis une boucle agentique.

## Déploiement Vercel vérifié

Faits vérifiés manuellement :

- le projet Vercel `Aciers Grosjean` est connecté au dépôt GitHub ;
- la branche de production est `main` ;
- le déploiement de production est actif ;
- Vercel indique : « To update your Production Deployment, push to the main branch. » ;
- le dernier déploiement de production visible correspond au commit `4afabb3` ;
- source de la vérification : `https://vercel.com/massimoharnisfeger-hues-projects/aciers-grosjean` ;
- aucune modification de la configuration Vercel n'est autorisée à ce stade.

Le flux de production est donc :

```text
PUSH main → GitHub → Vercel Production Deployment
```

Tout push sur `main` doit être traité comme une opération pouvant affecter la production. Aucun agent ne doit effectuer un push sur `main` automatiquement. Un push sur `main` exige une demande humaine explicite, une revue du diff, les preuves de tests et un human gate approuvé.

`_OUTILS/synchro.ps1` reste disponible. Le mode `auto` peut récupérer et synchroniser un dépôt propre selon ses contrôles, mais ne pousse jamais. Le mode `sauvegarder` peut préparer commit, synchronisation et push uniquement lorsqu'il est lancé volontairement par un humain après revue du diff et validation du human gate. Il ne doit pas être appelé par un agent sans cette validation.

La CI vérifie le code et les preuves ; elle ne vaut ni merge, ni release, ni deploy. Le déploiement Vercel est déclenché par le push sur `main`, mais reste une opération distincte de Git et de la CI, soumise à la validation humaine du push.
