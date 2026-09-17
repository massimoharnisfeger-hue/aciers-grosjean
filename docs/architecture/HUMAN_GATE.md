# Contrat Human Gate

Aucune opération sensible ne commence avec un gate `PENDING`.

Chaque demande doit contenir :

- `ACTION` : opération exacte demandée ;
- `REASON` : justification ;
- `RISK` : impact et périmètre du risque ;
- `FILES` : fichiers et répertoires concernés ;
- `DIFF` : diff attendu ou constaté ;
- `TESTS` : tests exécutés et résultats ;
- `ROLLBACK` : procédure réversible ;
- `DECISION` : `APPROVED`, `REJECTED` ou `PENDING` ;
- `VALIDATED_BY` : personne ayant validé ;
- `DATE_TRACE` : date et référence de la décision.

Une validation explicite est requise pour une suppression, migration, donnée réelle, secret, opération financière, changement de sécurité, production, commit groupé, push ou déploiement. En cas de refus, d'information manquante ou de contradiction, l'agent s'arrête et n'effectue pas de retry automatique.
