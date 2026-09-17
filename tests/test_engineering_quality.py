import unittest
import sys
import inspect
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validation.engineering_quality import (
    aggregate_findings,
    can_transition,
    evaluate_gate,
    finding_blocks_pass,
    route_change,
    serialize_finding,
    transition_status,
    validate_finding,
)
import scripts.validation.engineering_quality as engineering_quality


def make_finding(**overrides):
    finding = {
        "id": "EQ-001",
        "severity": "LOW",
        "category": "MAINTAINABILITY",
        "title": "Example finding",
        "description": "A verifiable example finding.",
        "evidence": ["tests/test_engineering_quality.py"],
        "affected_files": ["src/example.ts"],
        "affected_lines": ["src/example.ts:10"],
        "risk": {"impact": "Limited", "blast_radius": "Single file"},
        "suggested_remediation": "NONE",
        "blocker": False,
        "reviewer": "tester-reviewer/code-quality",
        "confidence": {"level": "HIGH", "rationale": "Direct evidence"},
        "status": "OPEN",
        "re_review_required": False,
    }
    finding.update(overrides)
    return finding


class EngineeringQualityTests(unittest.TestCase):
    def test_complete_finding_is_valid_and_serializable(self):
        finding = make_finding()
        self.assertEqual([], validate_finding(finding))
        self.assertIn('"category":"MAINTAINABILITY"', serialize_finding(finding))

    def test_required_fields_and_enums_are_enforced(self):
        finding = make_finding()
        del finding["evidence"]
        finding["severity"] = "UNKNOWN"
        errors = validate_finding(finding)
        self.assertTrue(any("missing required field: evidence" in error for error in errors))
        self.assertIn("severity is not supported", errors)

    def test_risk_and_confidence_shapes_are_enforced(self):
        finding = make_finding(risk={"impact": "Only impact"}, confidence={"level": "HIGH"})
        errors = validate_finding(finding)
        self.assertIn("risk.blast_radius must be a non-empty string", errors)
        self.assertIn("confidence.rationale must be a non-empty string", errors)

    def test_aggregation_keeps_sources_and_selects_highest_severity(self):
        first = make_finding(id="EQ-LOW", severity="LOW")
        second = make_finding(id="EQ-HIGH", severity="HIGH")
        result = aggregate_findings([first, second])
        self.assertEqual(1, len(result["groups"]))
        self.assertEqual("EQ-HIGH", result["groups"][0]["representative_id"])
        self.assertEqual(["EQ-LOW", "EQ-HIGH"], result["groups"][0]["finding_ids"])
        self.assertIsInstance(result["groups"][0]["key"], dict)

    def test_main_review_lifecycle_is_enforced(self):
        self.assertTrue(can_transition("OPEN", "IN_PROGRESS"))
        self.assertTrue(can_transition("IN_PROGRESS", "FIXED"))
        self.assertTrue(can_transition("FIXED", "RE_REVIEW"))
        self.assertTrue(can_transition("RE_REVIEW", "VERIFIED"))
        self.assertFalse(can_transition("FIXED", "VERIFIED"))
        self.assertFalse(can_transition("OPEN", "ACCEPTED_WITH_JUSTIFICATION"))
        self.assertEqual("ACCEPTED_WITH_JUSTIFICATION", transition_status("OPEN", "ACCEPTED_WITH_JUSTIFICATION", True))

    def test_blocking_findings_prevent_pass(self):
        finding = make_finding(severity="CRITICAL")
        self.assertTrue(finding_blocks_pass(finding))
        result = evaluate_gate([finding], tests_passed=True, regression_passed=True)
        self.assertEqual("BLOCKED", result["status"])

    def test_high_finding_requires_explicit_acceptance(self):
        finding = make_finding(severity="HIGH", status="ACCEPTED_WITH_JUSTIFICATION")
        self.assertTrue(finding_blocks_pass(finding))
        self.assertFalse(finding_blocks_pass(finding, human_gate_valid=True))

    def test_fix_requires_re_review(self):
        finding = make_finding(status="FIXED", re_review_required=True)
        self.assertTrue(finding_blocks_pass(finding))
        finding["status"] = "RE_REVIEW"
        self.assertTrue(finding_blocks_pass(finding))
        finding["status"] = "VERIFIED"
        self.assertFalse(finding_blocks_pass(finding))

    def test_stop_and_failed_regression_are_terminal_for_gate(self):
        clean = make_finding(status="VERIFIED")
        stop_result = evaluate_gate([clean], tests_passed=True, regression_passed=True, stop_triggered=True)
        regression_result = evaluate_gate([clean], tests_passed=True, regression_passed=False)
        self.assertEqual("BLOCKED", stop_result["status"])
        self.assertEqual("BLOCKED", regression_result["status"])

    def test_routing_for_ui_and_sensitive_changes(self):
        ui = route_change({"kind": "react_component"})
        payment = route_change({"kind": "payment"})
        self.assertEqual(["code-quality", "react-next"], ui["required_modes"])
        self.assertEqual("REQUIRED", payment["human_gate"])
        self.assertIn("security-data", payment["required_modes"])
        self.assertIn("tests", payment["required_modes"])

    def test_routing_for_authentication_and_permissions_requires_gate(self):
        authentication = route_change({"kind": "authentication"})
        permissions = route_change({"kind": "permissions"})
        for route in (authentication, permissions):
            self.assertEqual("REQUIRED", route["human_gate"])
            self.assertIn("security-data", route["required_modes"])
            self.assertIn("architecture", route["required_modes"])
            self.assertIn("tests", route["required_modes"])

    def test_routing_for_data_and_migration(self):
        data = route_change({"kind": "data"})
        migration = route_change({"kind": "migration"})
        self.assertEqual(["data", "tests"], data["required_modes"])
        self.assertEqual("REQUIRED", migration["human_gate"])
        self.assertIn("rollback", migration["tests_required"])

    def test_routing_infers_from_diff_files(self):
        route = route_change({"files": ["app/products/page.tsx"]})
        self.assertEqual("next_page", route["kind"])
        self.assertEqual("READ_ONLY_INDEPENDENT_ONLY", route["parallelism"])

    def test_unknown_routing_does_not_get_implicit_permission(self):
        with self.assertRaises(ValueError):
            route_change({"kind": "unknown_operation"})
        with self.assertRaises(ValueError):
            route_change({"files": ["notes/random.txt"]})

    def test_quality_module_is_report_only_and_has_no_execution_hooks(self):
        source = inspect.getsource(engineering_quality)
        for forbidden in ("subprocess", "os.system", "git push", "git commit", "vercel"):
            self.assertNotIn(forbidden, source.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
