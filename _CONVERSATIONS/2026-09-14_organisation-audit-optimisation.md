# 14 septembre 2026 — Organisation du dossier, audit et optimisation

Séance Claude Code sur le PC : https://claude.ai/code/session_011Va2LRc8Chevt4WRj964Em

## Demande
Rassembler le projet dans un dossier « Site Aciers Grosjean » sur le Bureau, bien organisé (photos à venir, changements fréquents).
Mettre en place un suivi par jour et par conversation, un endroit où déposer des fichiers, et une sauvegarde régulière qui garde tout à jour.
Analyser les défauts du code, corriger et optimiser. Prévoir l'ajout d'images (détails dans une prochaine séance).

## Constats
- Le projet n'existait que sur GitHub (créé dans une séance Claude web), sans copie sur le PC.
- Le site en ligne est protégé par l'authentification Vercel : invisible sans connexion au compte.
- La fiche produit restait blanche tant que le JavaScript n'avait pas fini de charger.
- Le « gel » de Chrome observé au début venait de l'outil de test (fenêtre en arrière-plan), pas du site : vérifié dans un navigateur indépendant.
- Ce PC n'a pas encore d'identifiants GitHub : il peut récupérer, pas envoyer.

## Décisions
- Dossier sur le Bureau (OneDrive), mais installation et builds hors OneDrive (`%LOCALAPPDATA%\SiteAciersGrosjean\build`).
- Journal et conversations dans le dépôt Git, pour que les séances Claude web les voient aussi. `_DEPOT` reste hors Git (dépôt public, fichiers lourds).
- Synchronisation automatique toutes les 2 heures : récupère et envoie, sans jamais créer de sauvegarde d'elle-même.
- Défilement simulé (Lenis) supprimé ; réversible via Git si l'effet manque.

## Fait
Voir `_JOURNAL/2026-09-14.md` et `_DOCS/AUDIT-2026-09-14.md`.

## Reste à faire
- [ ] Connecter le PC à GitHub : double-clic sur `_OUTILS/SAUVEGARDER.cmd`. Cela envoie aussi les corrections sur le site en ligne.
- [ ] Fournir les vraies coordonnées des 4 dépôts.
- [ ] Prochaine séance : intégration des images.
- [ ] Décider : retirer la protection Vercel pour montrer le site ? passer le dépôt GitHub en privé ? mettre en place un vrai envoi des formulaires ?
