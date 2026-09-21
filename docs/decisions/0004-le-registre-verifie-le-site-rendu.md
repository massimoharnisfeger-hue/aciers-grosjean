# ADR-0004 — Le registre vérifie le site rendu, pas seulement son source

```text
ID: ADR-0004
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: Le registre des contrôles (`tests/lancer.py`) contient au moins un contrôle qui démarre le site construit et vérifie ce qu'un visiteur reçoit. C'est `tests/test_parcours.py` : sept contrôles P1 à P7 sur l'accueil, `/devis` et ses six champs nommés, `/produits`, les six univers du catalogue, une fiche produit témoin, le 404 d'une URL inconnue, `robots.txt`, `sitemap.xml` et les premières URL que le sitemap déclare. Ils tournent dans l'étape « Registre des contrôles » de la CI, déjà placée après `npm run build`, sans modification du workflow. En local, sans build terminé, ils se déclarent ignorés avec la commande à lancer ; ils n'échouent pas et ne sortent pas du registre. `npm test` lance le registre.
REASON: Au 21/09/2026, 92 contrôles étaient verts et aucun n'ouvrait une page du site : tous lisaient le source. Un contrôle de source ne voit pas une page qui compile et plante au rendu, un catalogue vide, une route renommée, un sitemap qui déclare à Google des URL cassées. Le registre prouvait que le dépôt était bien rangé, pas que le site fonctionnait. Pour un site dont l'objet est la demande de devis, c'est la page `/devis` qu'il faut voir servie, pas seulement son fichier `.tsx` bien formé.
IMPACT: Socle relevé de 92 à 99 contrôles. Suite passée de 4,8 s à 10,0 s (démarrage de `next start` sur un port libre, budget de 60 s intact). Aucune dépendance ajoutée : `urllib`, `subprocess` et `socket` de la bibliothèque standard. Le marqueur de build terminé est `.next/prerender-manifest.json`, pas le dossier `.next/` qui existe dès les premières secondes du build. Non couvert : le JavaScript client, donc l'envoi du formulaire — sans objet tant que H4 n'est pas tranché, le formulaire construisant un `mailto:` et rien ne partant côté serveur (voir _DOCS/CHANTIERS-RENFORCEMENT.md, ligne H4).
SUPERSEDES: —
VALIDATED_BY: Écrit par Claude le 2026-09-21 sur la demande de Massimo « corrige tout ce que tu juges nécessaire et écris ». Sept contrôles exécutés verts en local sur build complet. Décision à confirmer explicitement par Massimo.
```

## Contexte

L'analyse du 21/09 mesurait environ 13 500 lignes de site (`app`, `components`, `lib`) pour plus
de 190 000 lignes d'appareil autour, et treize fichiers de contrôles qui vérifiaient tous la
gouvernance : `test_project_os`, `test_gate`, `test_index`, `test_decisions`, `test_depot`,
`test_socle`. Le système vérifiait qu'il était bien rangé. Rien ne vérifiait le produit.

`tests/test_mobile.py` assume ce choix dans sa docstring : « les contrôles lisent le source
plutôt que le rendu : ils restent verts sans navigateur, sans serveur et sans réseau ». Cette
propriété est précieuse et reste vraie pour tous les autres contrôles. Elle ne peut pas être la
seule : un site est ce qu'il sert, pas ce qu'il contient.

## Ce que le contrôle protège

Chaque contrôle correspond à une panne réelle et silencieuse pour les autres portes :

- P1, P3, P4, P5 : une page qui compile et plante au rendu (`typecheck` et `build` verts).
- P2 : un champ du formulaire renommé ou retiré, invisible pour `test_mobile.py` si la balise reste
  bien formée.
- P6 : un site qui répond 200 partout se fait indexer n'importe quoi ; un 500 perd le visiteur.
- P7 : un sitemap qui déclare à Google des URL que le site ne sert plus.

## Ce qu'il ne couvre pas

Le contrôle lit le HTML rendu par le serveur. Il ne voit pas ce que fait le JavaScript côté
client. L'envoi réel du formulaire de devis en fait partie et n'est pas testable tant que H4 n'est
pas tranché : aujourd'hui le formulaire ouvre la messagerie du visiteur par un `mailto:`, aucune
requête ne part vers le site, aucune trace n'existe côté entreprise. Quand un service d'envoi
existera, un contrôle P8 devra appeler sa route et vérifier la réception.

## Rollback

Supprimer `tests/test_parcours.py`, abaisser `controles_max` à 92 dans `tests/socle.json` et
écrire pourquoi dans `_DOCS/LECONS.md`, comme `tests/lancer.py` l'exige. Retirer le script `test`
de `package.json`. Marquer cet ADR `DEPRECATED`.
