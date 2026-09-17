# Conditions d'arrêt

L'agent doit écrire `STOP` et interrompre la tâche si :

- une information nécessaire manque ;
- une décision humaine est requise ;
- deux sources se contredisent ;
- le risque financier, sécurité ou production est élevé ;
- un test critique échoue ;
- le périmètre demandé est dépassé ;
- une suppression ou migration est proposée ;
- un rollback n'est pas défini ;
- des données réelles sont demandées dans une sandbox ;
- la preuve attendue ne peut pas être produite.

Format :

```text
STOP
Reason:
Impact:
Decision or information required:
Files affected:
Safe alternative:
Human validation required:
```

Une boucle ou un délai ne peut jamais contourner un `STOP`.

Dans une revue Engineering Quality, un contrat de finding invalide, une
contradiction non arbitrée, un finding bloquant non résolu, une correction
sans re-review, une régression ou une preuve de gate manquante déclenche aussi
`STOP`. Le STOP suspend la revue, l'agrégation, les retries, la délégation,
le fix et le parallélisme jusqu'à résolution ou décision humaine tracée.
