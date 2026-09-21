# ADR-0006 — Les demandes de devis partent par le serveur, via le SMTP Microsoft 365 de l'entreprise

```text
ID: ADR-0006
DATE: 2026-09-21
STATUS: ACTIVE
DECISION: Le formulaire de devis envoie sa demande à `POST /api/devis` (`app/api/devis/route.ts`), qui l'expédie par le SMTP Microsoft 365 de l'entreprise (`smtp.office365.com`, port 587, STARTTLS, nodemailer) vers `DEVIS_DESTINATAIRE` ou, à défaut, `site.email`. Les identifiants vivent dans les variables d'environnement Vercel, jamais dans le dépôt (`.env.example` documente les noms). Si le service est absent (503), refusé (502) ou injoignable, le formulaire ouvre la messagerie du visiteur avec le même contenu, exactement comme avant. Un champ piège `site_web` fait répondre 200 sans envoi aux robots. Le contrat est contrôlé par P8 (`tests/test_parcours.py`) et la route est la seule admise sous `app/api` par `tests/test_project_os.py`.
REASON: Décision H4, ouverte depuis le 14/09 : « Aujourd'hui des demandes de devis peuvent se perdre sans trace. » Le formulaire construisait un `mailto:` : rien ne partait vers le site, rien n'était tracé côté entreprise, et sur un téléphone sans client mail configuré la demande disparaissait. Pour un site dont l'objet est la demande de devis, c'est le défaut le plus coûteux du dépôt. Le SMTP de l'entreprise a été choisi par le propriétaire contre Resend (exige l'accès DNS du domaine) et Formspree (tiers, quota) : aucune dépendance externe nouvelle, les mails partent d'une boîte Grosjean.
IMPACT: Sans secrets configurés, rien ne change pour le visiteur : la route répond 503 et le formulaire bascule sur la messagerie — aucune régression en production tant que H4 n'est pas déployée. Reste à faire côté entreprise : activer « SMTP AUTH » sur la boîte émettrice (désactivé par défaut sur Microsoft 365), poser SMTP_USER, SMTP_PASSWORD et DEVIS_DESTINATAIRE sur Vercel, puis envoyer une demande réelle. Aucun contrôle n'envoie de vrai message : P8d s'ignore si `.env.local` existe. Pas de limitation de débit ; à surveiller. La mention sous le formulaire ne dit plus « aucune donnée n'est stockée » mais renvoie à `/protection-des-donnees`. `tests/test_project_os.py` n'interdit plus `app/api` en bloc : une route est admise si un ADR la porte, les bases de données restent interdites. Socle : +4 contrôles (P8a-d). Dépendance ajoutée : `nodemailer` (+ types).
SUPERSEDES: —
VALIDATED_BY: Massimo, réponse « SMTP Microsoft 365 de Grosjean » à la question H4 posée par Claude le 2026-09-21. Code, contrôles et ADR écrits par Claude le même jour ; envoi réel non encore vérifié (secrets absents).
```

## Contexte

ADR-0004 laissait H4 ouverte : « Quand un service d'envoi existera, un contrôle P8 devra appeler
sa route et vérifier la réception. » P8 vérifie la route ; la réception réelle dépend des secrets.

## Ordre suivi

1. P8a-d écrits et vus rouges (404 : la route n'existait pas).
2. Route, `.env.example`, formulaire réécrit. `typecheck`, `lint`, M1-M4 verts.
3. Build dans le dépôt déplacé (ADR-0005) : P8a-d verts.
4. `test_no_business_infrastructure_was_added` rouge (« aucun ADR ne porte cette route »),
   vert avec ce fichier.

## Rollback

Supprimer `app/api/devis/` et `.env.example`, rétablir `envoyer` en `mailto:` dans
`components/sections/DevisForm.tsx` (commit `b5467d3`), retirer `nodemailer` et ses types,
retirer P8a-d et abaisser le socle avec une ligne dans `_DOCS/LECONS.md`, marquer cet ADR
`DEPRECATED`. Le garde-fou de `test_project_os.py` redeviendra vert de lui-même.
