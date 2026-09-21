# ADR-0007 — La vérification responsive se fait au navigateur, et les cibles tactiles par une classe unique

```text
ID: ADR-0007
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: (1) La tenue du site de 320 à 1280 px se vérifie dans un Chromium réel avec `scripts/qa/balayage-responsive.py` (débordement, cibles < 24 px, textes < 12 px, console, réseau, parcours mobiles), résultats hors dépôt, rapport et matrice dans `_DOCS/QA-RESPONSIVE.md`. Un contrôle de débordement ne prouve pas la lisibilité : ce que `overflow-hidden` masque se vérifie en capture d'élément. (2) Un lien texte des composants partagés porte la classe `.lien-tactile` (`inline-flex`, `min-height` et `min-width` 24 px), qui ne change ni police ni couleur ; on ne grossit pas les textes pour atteindre 24 px. `tests/test_responsive.py` (R2) l'exige dans les fichiers listés. (3) Sont assumés, non corrigés : les liens soulignés dans le texte courant (exemption WCAG 2.5.8), le lien « Espace pro » desktop à 20 px (souris), les étiquettes à 11 px (`tag-stock`, `text-[11px]`), « En stock » sur deux lignes à 768 px. (4) Les gabarits mobiles s'écrivent mobile-first avec `sm:`/`md:` qui restaurent l'existant ; aucun `overflow-x: hidden` global.
REASON: Trois balayages de 330 mesures n'ont trouvé aucun débordement ; les vrais défauts (chevauchement masqué, cibles de 13-14 px, lien 404) n'étaient visibles qu'au navigateur, en capture ou dans le journal réseau. Sans outil rejouable, la prochaine régression repasserait inaperçue. La classe unique évite trente corrections locales divergentes et protège le design : la demande était de ne pas redessiner. Les P3 conservés relèvent du choix graphique ou d'une exemption explicite de la norme ; les corriger changerait le design sans preuve de gêne.
IMPACT: +5 contrôles (R1, R1bis, R2, R2bis, R3), socle à 110. Dépendance locale : Playwright Python avec Chromium (déjà présent sur le PC ; absent en CI, où seuls les contrôles source tournent). Le balayage complet prend ~9 min et peut manquer de mémoire sur 15 Go : le lancer par moitiés de largeurs. Dette notée : quatre miettes « Accueil » codées à la main hors `FilAriane`, à unifier.
SUPERSEDES: —
VALIDATED_BY: Massimo pour la boucle QA responsive (« continue jusqu'à ce que tout soit fini », 2026-09-21). Conventions (1)-(4) écrites par Claude le 2026-09-21 : à confirmer explicitement.
```

## Ce qui a été corrigé sous cette décision

- Comparaison à 320 px : gabarit mobile explicite, capture avant/après, desktop vérifié à 1280.
- Cibles < 24 px : de 37-46 par page à ≤ 2 en mobile et tablette, par `.lien-tactile` sur Footer,
  FilAriane, PageHeader, PageLegale, TableauProduits, plan du site, nouveautés, dépôts, services,
  fiche produit, réalisations.
- `/services/transformation` → `/services/soudure`, cible déjà associée à ce libellé dans
  `lib/edito.ts`.

## Rollback

Revert du commit ; retirer `tests/test_responsive.py` et `scripts/qa/`, abaisser le socle avec une
ligne dans `_DOCS/LECONS.md`, marquer cet ADR `DEPRECATED`. `.lien-tactile` peut rester : sans
classe appliquée, elle ne fait rien.
