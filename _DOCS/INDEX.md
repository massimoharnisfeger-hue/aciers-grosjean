# Index des sources — qui fait autorité sur quoi

Un fait = une source, jamais deux. Avant d'écrire une donnée quelque part, chercher ici qui la
détient déjà. Avant de corriger une donnée à la main, regarder la colonne « Généré par » : si elle
est remplie, la correction se fait dans le générateur, jamais dans le fichier produit.

`tests/test_index.py` vérifie que tous les chemins cités dans ce tableau existent et qu'aucun
fichier n'est déclaré deux fois comme source. Cet index ne peut donc pas devenir faux en silence.

## Données du site

| Fait | Source d'autorité | Généré par | Lu par |
|---|---|---|---|
| Prix, poids, longueurs, finitions, unités, PDF par produit | `lib/site-actuel.json` | `scripts/inventaire/integrer.py` | `lib/catalogue.ts` (fusion au chargement) |
| Descriptions structurées des fiches produit | `lib/descriptions-site-actuel.json` | `scripts/inventaire/integrer.py` | `app/p/[slug]/page.tsx` |
| Fiches techniques PDF publiées | `lib/documents.json` | `scripts/inventaire/integrer.py` | `app/documentation/page.tsx` |
| Arbre du catalogue : univers, catégories, produits | `lib/catalogue.ts` | `scripts/generer-catalogue.py` | pages serveur, `lib/menu.ts` |
| Visuels 3D rattachés aux fiches et aux catégories | `lib/visuels-produits.json` | `scripts/rendu-3d/integrer_visuels.py` | `app/p/[slug]/page.tsx` |
| Redirections 301 des anciennes URL | `lib/redirections.mjs` | `scripts/generer-redirections.py` | `next.config.mjs` |
| Catalogue visuel : chapitres, familles, variantes et leurs visuels ; verrou `CATALOGUE_LOCAL` | `lib/catalogue-visuel.ts` | — (calculé à la construction depuis `lib/catalogue.ts` et le manifeste) | `app/catalogue/page.tsx`, `app/catalogue/[univers]/page.tsx`, `app/catalogue/imprimer/page.tsx` |
| Catalogue en document A4 : couverture, sommaire, chapitres, planches, dépôts | `components/catalogue/Document.tsx` | — | `app/catalogue/imprimer/page.tsx`, puis `scripts/catalogue/exporter_pdf.py` qui en fait le PDF (dossier _DEPOT/documents/catalogue, hors Git, créé à l'export) |
| Textes éditoriaux, conseils, aide | `lib/edito.ts` | — | pages serveur |
| Coordonnées, dépôts, liens d'appel | `lib/content.ts` | — | toutes les pages |

Fichiers physiques associés : les PDF vivent dans `public/documents/`, les visuels dans
`public/images/produits/`. Les originaux non optimisés restent dans `_DEPOT/`, hors Git.

## Production des visuels 3D

| Fait | Source d'autorité | Généré par | Lu par |
|---|---|---|---|
| Où en est la production, quoi reprendre | `_DOCS/rendus-3d/avancement.md` | — | la boucle 3D, à chaque itération |
| Inventaire des visuels produits et leur verdict | `_DOCS/rendus-3d/inventaire-visuels.csv` | `scripts/rendu-3d/integrer_visuels.py` | contrôles, rapports |
| Questions produit non tranchées | `_DOCS/rendus-3d/questions-en-attente.md` | — | le propriétaire |
| Réglages appris : matières, lumières, cadrages | `_DOCS/rendus-3d/lecons.md` | — | la boucle 3D — séparé du carnet global par ADR-0002 |
| Périmètre et ordre des familles | `_DOCS/BRIEF-RENDUS-3D.md` | — | la boucle 3D |
| Inventaire de chaque fichier image (site, dépôt, atelier) et matrice produit ↔ visuels | `_DOCS/catalogue-produits/RESUME.md` (détail : `_DOCS/catalogue-produits/inventaire-images.csv`, `_DOCS/catalogue-produits/matrice-produits.csv`) | `scripts/catalogue/inventaire.py` | `_DOCS/CATALOGUE-PRODUITS.md`, le catalogue visuel |
| Rapport de contrôle du catalogue visuel : structure, associations, responsive, tests, cas à trancher | `_DOCS/CATALOGUE-PRODUITS.md` | — | le propriétaire, la prochaine séance |

## Pilotage du dépôt

| Fait | Source d'autorité | Généré par | Lu par |
|---|---|---|---|
| **État du projet, toutes pistes confondues** | `project-state/CURRENT_STATE.md` | — | début de session, la boucle, `tests/test_etat.py` |
| Références externes et règles de travail | `memory/ACTIVE_CONTEXT.md` | — | début de session |
| Règles de travail et contexte projet | `CLAUDE.md` | — | chaque session Claude, automatiquement |
| Hiérarchie des règles en cas de conflit | `.claude/rules/precedence.md` | — | agents et sessions |
| Conditions d'arrêt | `.claude/rules/stop-conditions.md` | — | agents et sessions |
| Décisions tranchées | `docs/decisions/README.md` (gabarit) | — | avant toute question au propriétaire |
| Leçons du dépôt et contrôle qui les garde | `_DOCS/LECONS.md` | — | la boucle de renforcement |
| Chantiers de renforcement et grille 9/10 | `_DOCS/CHANTIERS-RENFORCEMENT.md` | — | la boucle de renforcement |
| Constat d'audit du 21/09 | `_DOCS/AUDIT-STRUCTURE-2026-09-21.md` | — | référence, non mis à jour |
| Nombre de contrôles atteint | `tests/socle.json` | `tests/lancer.py` | `tests/lancer.py`, hook et CI |
| Ce qui a changé et pourquoi, par jour | `_JOURNAL/` | — | début de session |
| Résumé par séance de travail | `_CONVERSATIONS/` | — | début de session |

## Doubles sources connues, à résorber

Ces cas violent la règle « un fait = une source ». Ils sont nommés ici pour ne pas être oubliés,
et portés par des lignes de chantier.

- ~~**État du projet** : `project-state/CURRENT_STATE.md` et `memory/ACTIVE_CONTEXT.md` décrivaient
  tous deux l'état~~ → **résorbé le 21/09 (Z5)**. `CURRENT_STATE.md` est la source unique et renvoie
  aux trois pistes ; `memory/ACTIVE_CONTEXT.md` ne garde que références et règles de travail.
  `tests/test_etat.py` interdit le retour du doublon et vérifie la fraîcheur contre `_JOURNAL/`.
- **Questions ouvertes** : `memory/OPEN_QUESTIONS.md` (12 questions ERP) et
  `_DOCS/rendus-3d/questions-en-attente.md` (40 questions produit) s'ignorent. → ligne **C9**.
- **Skills** : `.claude/skills/` et `.agents/skills/` contiennent les mêmes octets en double.
  → ligne **C16**.
