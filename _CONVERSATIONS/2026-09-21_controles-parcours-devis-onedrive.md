# 21 septembre 2026 — contrôles de parcours, envoi des devis, sortie de OneDrive

## Demande

« Analyse ça et est-ce que je m'y suis pris de la bonne manière », sur le dossier du site. Puis
« corrige tout ce que tu juges nécessaire et écris », puis « tu sais tout corriger et faire en sorte
que ça soit bien structuré et bien complémentaire sans erreur ». Deux décisions posées au
propriétaire en cours de séance : H4 (envoi des devis) → « SMTP Microsoft 365 de Grosjean » ;
H1 (OneDrive) → « Déplacer vers Projects » ; commit → oui.

## Constats

**La gouvernance était solide, la cible pas.** Environ 13 500 lignes de site pour plus de 190 000
lignes d'appareil autour ; treize fichiers de contrôles, tous sur la gouvernance, aucun n'ouvrant une
page du site. Le registre prouvait que le dépôt était bien rangé, pas que le site fonctionnait.

**Le formulaire de devis n'envoyait rien.** `mailto:` : aucune requête vers le site, aucune trace
côté entreprise. H4 était ouverte depuis le 14/09.

**Le dépôt vivait dans OneDrive.** 1 767 fichiers de `.git` en placeholders « en ligne seulement ».
H1 était ouverte depuis le 14/09.

**Correction de mon analyse initiale :** le doublon `.claude/skills` / `.agents/skills` est
voulu (Claude / Codex) et gardé par `extensions_check.py`. Pas touché.

**Erreur de séance :** `npm ci`, un build et deux `npm install` lancés dans le dossier OneDrive
avant que le `CLAUDE.md` du projet ne soit chargé, malgré sa règle. Leçon L-016.

## Décisions

- ADR-0004 : le registre vérifie le site rendu (P1-P7).
- ADR-0005 : le dépôt vit dans `C:\Users\massi\Projects\aciers-grosjean`, `_DEPOT` par jonction.
- ADR-0006 : les devis partent par `POST /api/devis` et le SMTP Microsoft 365, secours `mailto:`.
- `test_no_business_infrastructure_was_added` admet une route portée par un ADR (L-017).
- Un contrôle jamais vu rouge (placeholders `.git`) a été retiré avant commit.

## Fait

Commit `b5467d3` (contrôles de parcours, ADR-0004, `npm test`) dans l'ancien dossier. Clone dans
`Projects`, fetch des deux commits que GitHub n'avait pas, copie des six fichiers en cours, jonction
`_DEPOT`, tâche planifiée réinstallée. Route d'envoi, `.env.example`, formulaire réécrit (fetch,
secours messagerie, champ piège, mention RGPD), P8a-d rouges puis verts, `test_emplacement.py`
E1 rouge sous OneDrive puis vert, garde-fou rouge puis vert avec l'ADR-0006. Six mentions
OneDrive corrigées, dont le seul chemin absolu du code (`scripts/inventaire/analyser.py`).
Leçons L-015 à L-017. `105 controles - 0 echecs - 11.4 s` ; `typecheck`, `lint`, `build`, M1-M4
verts dans le nouveau dossier.

## Reste à faire

- Côté entreprise : activer SMTP AUTH sur la boîte émettrice, poser `SMTP_USER`, `SMTP_PASSWORD`
  et `DEVIS_DESTINATAIRE` sur Vercel, envoyer une demande réelle. Aucun envoi réel n'a été vérifié.
- Neutraliser l'ancien dossier OneDrive : retirer `node_modules/` et `.next/`, remplacer les
  trois boutons `.cmd` par un renvoi vers `Projects`. `_DEPOT` y reste.
- Push : trois commits locaux attendent un `SAUVEGARDER.cmd` humain. Rien n'a été poussé.
- Pas de limitation de débit sur `/api/devis` : à surveiller après mise en service.

## Session

Claude Code, session `d08c2e3e-6a02-4de7-a879-fa9d6afbfd21`, modèle Fable 5.1 (Opus 5 en début
de séance).


## Boucle QA responsive (suite de séance, même session)

Demande : « ULTIMATE RESPONSIVE QA LOOP — 320px Mobile → Tablet → Desktop », puis « continue
jusqu'à ce que tout soit fini ». Détail dans `_JOURNAL/2026-09-21.md` (section Nuit) et
`_DOCS/QA-RESPONSIVE.md`. Trois défauts corrigés (chevauchement 320 px, cibles < 24 px, lien
404), trois leçons (L-018 à L-020), un outil de balayage réutilisable. Un balayage a été tué par
manque de mémoire (15 Go) et relancé en deux moitiés : à retenir pour les prochains.


## Fiches produit (22/09, boucle autonome /loop)

Brief « AUTONOMOUS PRODUCT PAGE REDESIGN + QA LOOP » avec captures du site déployé (en retard de
cinq jours sur le travail local). Cause racine dans les données (générateur), pas dans le CSS ;
système réutilisable pour les 495 fiches ; détail dans `_JOURNAL/2026-09-22.md` et ADR-0008.
