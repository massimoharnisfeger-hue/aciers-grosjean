# Politique de synchronisation et de publication

Ces opérations sont distinctes :

- `AUTO-SAVE` : écriture locale d'état, mémoire, rapports ou handoff dans le périmètre autorisé. Elle ne touche ni Git distant ni production.
- `AUTO-COMMIT` : interdit dans une boucle agentique par défaut. Un commit nécessite une demande humaine explicite et un diff vérifié.
- `AUTO-PUSH` : interdit pour les changements du projet. Même un commit existant ne doit pas être poussé automatiquement.
- `DEPLOY` : séparé de Git et de la CI. Aucun déploiement automatique depuis une boucle agentique.

`_OUTILS/synchro.ps1` reste disponible. Le mode `auto` peut récupérer et synchroniser un dépôt propre selon ses contrôles, mais ne pousse jamais. Le mode `sauvegarder` peut préparer commit, synchronisation et push uniquement lorsqu'il est lancé volontairement par un humain après revue du diff et validation du human gate. Il ne doit pas être appelé par un agent sans cette validation.

La CI vérifie le code et les preuves ; elle ne vaut ni merge, ni release, ni deploy. Un éventuel déploiement externe après un push humain reste soumis à la politique de production et à la validation humaine.
