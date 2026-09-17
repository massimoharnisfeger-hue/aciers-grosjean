import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validation.engineering_quality import (
    CONTRACT_VERSION,
    route_change,
    serialize_finding,
    validate_finding,
)


SAMPLE_FINDING = {
    "id": "EQ-CHECK-001",
    "severity": "LOW",
    "category": "MAINTAINABILITY",
    "title": "Validation contract smoke check",
    "description": "The internal contract accepts a complete finding.",
    "evidence": ["engineering_quality_check.py"],
    "affected_files": ["scripts/validation/engineering_quality.py"],
    "affected_lines": "UNKNOWN",
    "risk": {"impact": "None", "blast_radius": "Validation only"},
    "suggested_remediation": "NONE",
    "blocker": False,
    "reviewer": "engineering-quality-check",
    "confidence": {"level": "HIGH", "rationale": "Deterministic local fixture"},
    "status": "VERIFIED",
    "re_review_required": False,
}


def main() -> int:
    errors = validate_finding(SAMPLE_FINDING)
    if errors:
        print("ENGINEERING QUALITY CHECK: FAIL")
        print("- invalid sample: " + "; ".join(errors))
        return 1

    serialized = serialize_finding(SAMPLE_FINDING)
    route = route_change({"kind": "payment"})
    if not serialized or route["human_gate"] != "REQUIRED":
        print("ENGINEERING QUALITY CHECK: FAIL")
        print("- contract serialization or sensitive routing failed")
        return 1

    print("ENGINEERING QUALITY CHECK: PASS")
    print(f"- contract version: {CONTRACT_VERSION}")
    print("- finding validation and serialization: PASS")
    print("- payment routing requires human gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
