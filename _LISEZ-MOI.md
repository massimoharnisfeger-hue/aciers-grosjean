# Site Aciers Grosjean — mode d'emploi du dossier

Ce dossier contient **tout** le site : le code, l'historique des modifications et l'espace où tu déposes tes fichiers.
Il est sauvegardé deux fois : par **OneDrive** (tout le dossier) et par **GitHub** (le code, le journal et les conversations).

- Site en ligne (préproduction) : https://aciers-grosjean.vercel.app — visible seulement connecté à ton compte Vercel
- Code : https://github.com/massimoharnisfeger-hue/aciers-grosjean — dépôt **public**
- Chaque envoi sur GitHub redéploie le site sur Vercel (environ 1 minute).

## Où mettre quoi

| Dossier | Pour quoi | Sauvegardé par |
|---|---|---|
| `_DEPOT/images/` | Tes photos à intégrer, rangées par lot (voir `_DOCS/BESOINS-IMAGES.md`) ; `test-blender/` : essais de rendus 3D | OneDrive |
| `_DEPOT/documents/` | Briefs, PDF, textes, tarifs, infos du client ; `pdf-site-actuel/` : les 64 PDF d'origine du site actuel | OneDrive |
| `_DEPOT/rendus-3d/` | Classeur de collecte des données pour les visuels 3D | OneDrive |
| `_DEPOT/deja-integre/` | Claude y range ce qui a été intégré au site | OneDrive |
| `_JOURNAL/` | Une fiche par jour : ce qui a changé sur le site et pourquoi | GitHub + OneDrive |
| `_CONVERSATIONS/` | Un résumé par séance de travail avec Claude : demande, décisions, reste à faire | GitHub + OneDrive |
| `_DOCS/` | Audits, besoins en images, brief des rendus 3D | GitHub + OneDrive |
| `_DOCS/catalogue-site-actuel/` | Inventaire complet d'aciersgrosjean.be : `SYNTHESE.md` à lire d'abord, listes Excel (produits, catégories, familles, doublons, PDF, images) | GitHub + OneDrive |
| `_OUTILS/` | Les boutons à double-cliquer (ci-dessous) | GitHub + OneDrive |
| `app`, `components`, `lib`, `scripts` | Le code du site : ne pas modifier à la main | GitHub + OneDrive |
| `public/documents/` | Les fiches techniques PDF publiées sur le site, renommées proprement | GitHub + OneDrive |

`_DEPOT` n'est volontairement **pas** envoyé sur GitHub : le dépôt est public et les photos brutes sont lourdes.
Une fois intégrées, les images optimisées vont dans `public/images/` et partent avec le site.

## Les boutons (`_OUTILS`)

- **LANCER-LE-SITE.cmd** : ouvre le site sur ton PC (http://localhost:3000). La première fois, compte 1 à 2 minutes.
- **SAUVEGARDER.cmd** : enregistre toutes les modifications et les envoie sur GitHub, ce qui met à jour le site en ligne.
- **METTRE-A-JOUR.cmd** : récupère les modifications faites ailleurs (par exemple une séance Claude sur le web).
- `synchro.log` : l'historique des synchronisations, ligne par ligne.

## Synchronisation automatique

La tâche Windows « Site Aciers Grosjean - synchro GitHub » tourne toutes les 2 heures.
Elle récupère les nouveautés de GitHub et envoie les sauvegardes déjà enregistrées.
Elle ne crée jamais de sauvegarde d'elle-même et ne touche pas à un travail en cours.

## Travailler avec Claude

Ouvre Claude Code dans ce dossier, ou dis-lui « travaille sur le site Aciers Grosjean du Bureau ».
Le fichier `CLAUDE.md` lui donne les règles : lire le dernier journal, noter chaque changement, vérifier, sauvegarder.

## À faire une seule fois

Connecter ce PC à GitHub : double-clique sur `_OUTILS/SAUVEGARDER.cmd`, une fenêtre de connexion GitHub s'ouvre, connecte-toi.
C'est retenu ensuite, et la synchronisation automatique pourra envoyer elle aussi.
