# ADR-0011 — Les visuels 3D gardent leurs vues d'origine : pièce entière, seule la finition change

```text
ID: ADR-0011
DATE: 2026-09-24
STATUS: ACTIVE
DECISION: (1) Les visuels de fiche et les photos studio gardent exactement les vues validées avant l'audit qualité du 23/09 : fiche = tronçon de 6,25 × la plus grande cote (plafond 500 mm) vu en entier, ses deux bouts dans l'image ; studio = pièces de 7 × la plus grande section (plafond 900 mm), trio de tailles d'origine. (2) La barre 4 × plus longue qui sortait du cadre (`DEBORD`) et le studio à 18 × (`RATIO_STUDIO`), introduits le 23/09 (défaut « D2 » de `_DOCS/rendus-3d/audit-qualite.md`), sont retirés, ainsi que le trio imposé des cornières inégales (`TRIOS_IMPOSES` de `serie_audit.py`). (3) L'audit ne garde que la finition : chanfrein proportionné (D1, arêtes vives), rayons de l'aluminium d'après les photos du stock, face sciée par finition et coupe du U alu (V12), nervures des ronds à béton, placement des étiquettes (V6, V7), éclairage des photos studio de l'acier brut. (4) Le contrôle V2 garde cette règle : aucune barre ne sort du cadre, le tronçon rendu est le tronçon cadré.
REASON: Propriétaire, 24/09, après avoir vu les nouveaux visuels en local : « Je veux vraiment avoir l'entièreté de la pièce et pas juste une coupe à moitié faite. Moi ce que je voulais, c'est que tu laisses exactement les mêmes vues comme il y avait, juste que tu travailles plus la finition. » Sa remarque du 23/09 (« parfois c'est beaucoup trop épais, parfois il y a des arrondis ») visait la finition ; Claude l'avait lue comme un défaut de cadrage et avait changé la vue sans essai validé par lui.
IMPACT: `scripts/rendu-3d/preparer_rendus.py` (plus de `DEBORD`, `RATIO_STUDIO` = 7), `rendu3d/outils-seance/serie_audit.py` (`TRIOS_IMPOSES` vide), `tests/test_rendus_3d.py` (V2 réécrit), leçon L-053 réécrite. `rendu_profil.py`, `habiller.py` et `controler_rendus.py` gardent la prise en charge de `longueur_cadre` / `debord` : sans débord, ils retombent sur le comportement d'avant l'audit. Toutes les familles refaites les 23 et 24/09 sont à rendre de nouveau (≈ 223 fiches et 24 photos studio). La préproduction n'a jamais reçu les vues retirées (rien n'a été publié).
SUPERSEDES: — (la vue « D2 » n'avait pas d'ADR)
VALIDATED_BY: Massimo, 2026-09-24, message cité ci-dessus.
```

## Précision (24/09, vérification indépendante des tubes carrés)

Sections creuses (tubes carrés, rectangulaires et ronds) : le tronçon fait au moins 3 × la plus grande cote, règle du
15/09 gardée avec les vues d'origine (`piece()`, `preparer_rendus.py`) : à 500 mm, on voyait le fond à travers le tube
carré 250x250x6. D'où 750 mm pour le 250x250x6 et 600 mm pour le rectangulaire 200x100x5 ; toutes les autres fiches
suivent 6,25 × la plus grande cote, plafond 500 mm.

## Rollback

Remettre `DEBORD = 4`, le bloc de débord de `main()` et `RATIO_STUDIO = 18` dans `preparer_rendus.py`,
revenir à l'ancien V2, marquer cet ADR `SUPERSEDED`.
