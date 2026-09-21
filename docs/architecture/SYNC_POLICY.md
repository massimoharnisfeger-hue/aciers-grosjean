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
- le dernier déploiement de production connu correspond au commit `54d93a2` ;
- le déploiement précédemment documenté sur `4afabb3` est antérieur ;
- source de la vérification : `https://vercel.com/massimoharnisfeger-hues-projects/aciers-grosjean` ;
- aucune modification de la configuration Vercel n'est autorisée à ce stade.

Le flux de production est donc :

```text
PUSH branche → pull request → check « quality » vert → merge dans `main` → Vercel Production Deployment
```

Tout push sur `main` doit être traité comme une opération pouvant affecter la production. Aucun agent ne doit effectuer un push sur `main` automatiquement. Un push sur `main` exige une demande humaine explicite, une revue du diff, les preuves de tests et un human gate approuvé.

`_OUTILS/synchro.ps1` reste disponible. Le mode `auto` peut récupérer et synchroniser un dépôt propre selon ses contrôles, mais ne pousse jamais. Le mode `sauvegarder` peut préparer commit, synchronisation et push uniquement lorsqu'il est lancé volontairement par un humain après revue du diff et validation du human gate. Il ne doit pas être appelé par un agent sans cette validation.

La CI vérifie le code et les preuves ; elle ne vaut ni merge, ni release, ni deploy. Le déploiement Vercel est déclenché par le push sur `main`, mais reste une opération distincte de Git et de la CI, soumise à la validation humaine du push.

## Limites de l'audit de synchronisation (17/09/2026)

### PROUVÉ

- le repository local est correct, sur `main`, avec un working tree propre ;
- le dernier push connu correspond à `54d93a2` ;
- la CI GitHub sur `54d93a2` est en succès ;
- le déploiement Vercel sur `54d93a2` est en succès ;
- aucun commit automatique Git ni hook Git actif n'a été détecté.

### UNKNOWN

- l'état temps réel de synchronisation OneDrive, les conflits, les fichiers en attente et les verrous ;
- la protection effective de la branche `main` ;
- la fraîcheur du remote GitHub au moment exact de la dernière vérification locale ;
- les paramètres externes GitHub/Vercel non visibles depuis le dépôt.

## Branche protegee (constate le 21/09/2026)

`main` refuse le push direct : « Changes must be made through a pull request » et
« Required status check "quality" is expected ». Le flux reel est donc :

1. `_OUTILS/SAUVEGARDER.cmd` (ou `synchro.ps1 -Mode sauvegarder`) commite, puis pousse le travail
   sur une branche (`travail/AAAA-MM-JJ-HHMM` par defaut, ou celle passee par `-BrancheCible`) ;
2. le script affiche et ouvre le lien de creation de la pull request ;
3. la CI execute le check « quality » (typecheck, lint, build, registre des controles) ;
4. `scripts/publier.ps1` fusionne **si et seulement si** le check est vert — c'est ce merge qui
   declenche le deploiement Vercel de production (ADR-0009, demande du 22/09).

Une fusion sur un check rouge, ou pendant qu'il tourne, est refusee. Le mode `auto` ne pousse
toujours rien et ne fusionne jamais (ADR-0003). L'adresse a regarder est
https://aciers-grosjean.vercel.app ; le site reel www.aciersgrosjean.be n'est pas touche.
Gardes : `tests/test_gate.py::GateTests::test_le_bouton_de_sauvegarde_passe_par_une_branche`
et `::test_la_chaine_de_publication_va_jusqu_a_vercel`.
