# Décisions

Une décision importante doit être versionnée dans un fichier séparé.

Format minimal :

```text
ID:
DATE:
STATUS: ACTIVE | SUPERSEDED | DEPRECATED | REJECTED
DECISION:
REASON:
IMPACT:
SUPERSEDES:
VALIDATED_BY:
```

Une proposition n'est pas une décision. Une question métier non tranchée reste `BUSINESS_DECISION_REQUIRED`.
