"""Contrat et règles déterministes de la fondation Engineering Quality."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
import json
import re
from typing import Any


CONTRACT_VERSION = "1.0"
SEVERITIES = frozenset({"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"})
CATEGORIES = frozenset(
    {
        "BUG",
        "SECURITY",
        "ARCHITECTURE",
        "TYPE",
        "TEST",
        "ERROR_HANDLING",
        "PERFORMANCE",
        "SIMPLIFICATION",
        "MAINTAINABILITY",
        "DATA",
        "UX",
        "COMPLIANCE",
    }
)
CONFIDENCE_LEVELS = frozenset({"HIGH", "MEDIUM", "LOW"})
STATUSES = frozenset(
    {
        "OPEN",
        "IN_PROGRESS",
        "FIXED",
        "RE_REVIEW",
        "VERIFIED",
        "ACCEPTED_WITH_JUSTIFICATION",
        "ESCALATED",
        "WONT_FIX",
    }
)
REQUIRED_FINDING_FIELDS = (
    "id",
    "severity",
    "category",
    "title",
    "description",
    "evidence",
    "affected_files",
    "affected_lines",
    "risk",
    "suggested_remediation",
    "blocker",
    "reviewer",
    "confidence",
    "status",
    "re_review_required",
)
OPTIONAL_FINDING_FIELDS = (
    "run_id",
    "parent_finding_id",
    "baseline_ref",
    "diff_ref",
    "introduced_by",
    "requirement_refs",
    "acceptance_refs",
    "test_refs",
    "evidence_refs",
    "data_classification",
    "human_gate_required",
    "human_gate_ref",
    "owner",
    "due_phase",
    "duplicate_of",
    "contradicts",
    "tool_version",
    "source_sha",
)


def _is_non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        errors.append(f"{field} must be a list of strings")
        return
    if not value or any(not _is_non_empty_text(item) for item in value):
        errors.append(f"{field} must contain at least one non-empty string")


def validate_finding(finding: Mapping[str, Any]) -> list[str]:
    """Return contract violations; an empty list means the finding is valid."""

    if not isinstance(finding, Mapping):
        return ["finding must be an object"]

    errors: list[str] = []
    known_fields = set(REQUIRED_FINDING_FIELDS) | set(OPTIONAL_FINDING_FIELDS)
    missing = [field for field in REQUIRED_FINDING_FIELDS if field not in finding]
    errors.extend(f"missing required field: {field}" for field in missing)
    errors.extend(
        f"unsupported field: {field}" for field in sorted(set(finding) - known_fields)
    )

    for field in ("id", "title", "description", "reviewer"):
        if field in finding and not _is_non_empty_text(finding[field]):
            errors.append(f"{field} must be a non-empty string")

    if "severity" in finding and finding["severity"] not in SEVERITIES:
        errors.append("severity is not supported")
    if "category" in finding and finding["category"] not in CATEGORIES:
        errors.append("category is not supported")
    if "status" in finding and finding["status"] not in STATUSES:
        errors.append("status is not supported")

    if "evidence" in finding:
        _validate_string_list(finding["evidence"], "evidence", errors)
    if "affected_files" in finding:
        _validate_string_list(finding["affected_files"], "affected_files", errors)
    if "affected_lines" in finding:
        affected_lines = finding["affected_lines"]
        if affected_lines != "UNKNOWN":
            _validate_string_list(affected_lines, "affected_lines", errors)

    if "risk" in finding:
        risk = finding["risk"]
        if not isinstance(risk, Mapping):
            errors.append("risk must be an object")
        else:
            for field in ("impact", "blast_radius"):
                if not _is_non_empty_text(risk.get(field)):
                    errors.append(f"risk.{field} must be a non-empty string")

    if "suggested_remediation" in finding and not _is_non_empty_text(
        finding["suggested_remediation"]
    ):
        errors.append("suggested_remediation must be a non-empty string")
    for field in ("blocker", "re_review_required"):
        if field in finding and not isinstance(finding[field], bool):
            errors.append(f"{field} must be boolean")

    if "confidence" in finding:
        confidence = finding["confidence"]
        if not isinstance(confidence, Mapping):
            errors.append("confidence must be an object")
        else:
            if confidence.get("level") not in CONFIDENCE_LEVELS:
                errors.append("confidence.level is not supported")
            if not _is_non_empty_text(confidence.get("rationale")):
                errors.append("confidence.rationale must be a non-empty string")

    for field in OPTIONAL_FINDING_FIELDS:
        if field not in finding:
            continue
        value = finding[field]
        if field.endswith("_refs") or field in {"contradicts"}:
            _validate_string_list(value, field, errors)
        elif field == "human_gate_required" and not isinstance(value, bool):
            errors.append("human_gate_required must be boolean")
        elif field in {
            "run_id",
            "parent_finding_id",
            "baseline_ref",
            "diff_ref",
            "introduced_by",
            "data_classification",
            "human_gate_ref",
            "owner",
            "due_phase",
            "duplicate_of",
            "tool_version",
            "source_sha",
        } and not _is_non_empty_text(value):
            errors.append(f"{field} must be a non-empty string")

    return errors


def serialize_finding(finding: Mapping[str, Any]) -> str:
    errors = validate_finding(finding)
    if errors:
        raise ValueError("invalid finding: " + "; ".join(errors))
    return json.dumps(finding, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def finding_group_key(finding: Mapping[str, Any]) -> tuple[str, str, tuple[str, ...]]:
    """Return the stable key used as a deduplication candidate."""

    title = re.sub(r"\s+", " ", str(finding["title"]).strip().lower())
    files = tuple(sorted(str(path).replace("\\", "/") for path in finding["affected_files"]))
    return str(finding["category"]), title, files


def aggregate_findings(findings: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Group valid findings without deleting their provenance."""

    errors: list[str] = []
    groups: dict[tuple[str, str, tuple[str, ...]], list[Mapping[str, Any]]] = {}
    for finding in findings:
        finding_errors = validate_finding(finding)
        if finding_errors:
            errors.extend(f"{finding.get('id', '<unknown>')}: {error}" for error in finding_errors)
            continue
        groups.setdefault(finding_group_key(finding), []).append(finding)

    if errors:
        raise ValueError("invalid findings: " + "; ".join(errors))

    severity_order = {severity: index for index, severity in enumerate(("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"))}
    result_groups = []
    for key, members in sorted(groups.items(), key=lambda item: item[0]):
        representative = max(members, key=lambda item: severity_order[item["severity"]])
        result_groups.append(
            {
                "key": {
                    "category": key[0],
                    "title": key[1],
                    "affected_files": list(key[2]),
                },
                "representative_id": representative["id"],
                "severity": representative["severity"],
                "finding_ids": [member["id"] for member in members],
            }
        )
    return {"contract_version": CONTRACT_VERSION, "groups": result_groups}


ALLOWED_TRANSITIONS = {
    "OPEN": {"IN_PROGRESS", "ESCALATED", "ACCEPTED_WITH_JUSTIFICATION", "WONT_FIX"},
    "IN_PROGRESS": {"FIXED", "ESCALATED", "ACCEPTED_WITH_JUSTIFICATION", "WONT_FIX"},
    "FIXED": {"RE_REVIEW", "ESCALATED"},
    "RE_REVIEW": {"VERIFIED", "OPEN", "ESCALATED"},
    "VERIFIED": set(),
    "ACCEPTED_WITH_JUSTIFICATION": set(),
    "ESCALATED": {"IN_PROGRESS", "OPEN"},
    "WONT_FIX": set(),
}


def can_transition(current: str, target: str, human_gate_valid: bool = False) -> bool:
    if current not in STATUSES or target not in STATUSES:
        return False
    if target in {"ACCEPTED_WITH_JUSTIFICATION", "WONT_FIX"} and not human_gate_valid:
        return False
    return target in ALLOWED_TRANSITIONS[current]


def transition_status(current: str, target: str, human_gate_valid: bool = False) -> str:
    if not can_transition(current, target, human_gate_valid):
        raise ValueError(f"transition not allowed: {current} -> {target}")
    return target


def finding_blocks_pass(
    finding: Mapping[str, Any],
    *,
    human_gate_valid: bool = False,
    medium_context: bool = False,
) -> bool:
    status = finding["status"]
    if status == "VERIFIED":
        return False
    if status in {"ACCEPTED_WITH_JUSTIFICATION", "WONT_FIX"}:
        return not human_gate_valid
    if status == "ESCALATED":
        return True
    if finding["re_review_required"]:
        return True
    if finding["severity"] in {"CRITICAL", "HIGH"}:
        return True
    if finding["severity"] == "MEDIUM":
        return bool(finding["blocker"] or medium_context)
    return bool(finding["blocker"])


def evaluate_gate(
    findings: Sequence[Mapping[str, Any]],
    *,
    tests_passed: bool,
    regression_passed: bool,
    stop_triggered: bool = False,
    human_gate_valid: bool = False,
    medium_context: bool = False,
) -> dict[str, Any]:
    reasons: list[str] = []
    if stop_triggered:
        reasons.append("STOP is active")
    if not tests_passed:
        reasons.append("tests did not pass")
    if not regression_passed:
        reasons.append("regression check did not pass")

    for finding in findings:
        finding_errors = validate_finding(finding)
        if finding_errors:
            reasons.append(f"invalid finding {finding.get('id', '<unknown>')}")
            continue
        if finding_blocks_pass(
            finding,
            human_gate_valid=human_gate_valid,
            medium_context=medium_context,
        ):
            reasons.append(f"blocking finding {finding['id']}")

    return {"status": "PASS" if not reasons else "BLOCKED", "reasons": reasons}


ROUTING_MATRIX: dict[str, dict[str, Any]] = {
    "simple_ui": {
        "required_modes": ["code-quality"],
        "optional_modes": ["react-next"],
        "agents": ["tester-reviewer"],
        "tests_required": [],
        "playwright": "CONDITIONAL",
        "human_gate": "NOT_REQUIRED",
    },
    "react_component": {
        "required_modes": ["code-quality", "react-next"],
        "optional_modes": ["performance"],
        "agents": ["tester-reviewer"],
        "tests_required": ["behavior"],
        "playwright": "CONDITIONAL",
        "human_gate": "NOT_REQUIRED",
    },
    "next_page": {
        "required_modes": ["code-quality", "react-next"],
        "optional_modes": ["performance"],
        "agents": ["tester-reviewer"],
        "tests_required": ["behavior", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "refactor": {
        "required_modes": ["code-quality", "architecture", "tests"],
        "optional_modes": ["simplification"],
        "agents": ["tester-reviewer", "requirements-architect"],
        "tests_required": ["regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "new_feature": {
        "required_modes": ["code-quality", "tests"],
        "optional_modes": ["architecture", "react-next", "performance"],
        "agents": ["tester-reviewer"],
        "tests_required": ["behavior", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "business_logic": {
        "required_modes": ["code-quality", "tests"],
        "optional_modes": ["architecture", "error-handling"],
        "agents": ["tester-reviewer"],
        "tests_required": ["edge_cases", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "data": {
        "required_modes": ["data", "tests"],
        "optional_modes": ["security-data"],
        "agents": ["data-guardian", "tester-reviewer"],
        "tests_required": ["integrity", "regression"],
        "playwright": "NOT_REQUIRED",
        "human_gate": "CONDITIONAL",
    },
    "catalogue": {
        "required_modes": ["data", "tests"],
        "optional_modes": ["security-data"],
        "agents": ["data-guardian", "tester-reviewer"],
        "tests_required": ["sources", "integrity"],
        "playwright": "NOT_REQUIRED",
        "human_gate": "CONDITIONAL",
    },
    "stock": {
        "required_modes": ["data", "tests"],
        "optional_modes": ["security-data", "architecture"],
        "agents": ["data-guardian", "tester-reviewer"],
        "tests_required": ["invariants", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "command": {
        "required_modes": ["data", "tests"],
        "optional_modes": ["security-data", "architecture"],
        "agents": ["data-guardian", "tester-reviewer"],
        "tests_required": ["invariants", "behavior"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "payment": {
        "required_modes": ["security-data", "data", "tests"],
        "optional_modes": ["architecture"],
        "agents": ["data-guardian", "tester-reviewer"],
        "tests_required": ["security", "failure_cases", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "REQUIRED",
    },
    "authentication": {
        "required_modes": ["security-data", "architecture", "tests"],
        "optional_modes": ["error-handling"],
        "agents": ["data-guardian", "requirements-architect", "tester-reviewer"],
        "tests_required": ["access_positive", "access_negative"],
        "playwright": "CONDITIONAL",
        "human_gate": "REQUIRED",
    },
    "permissions": {
        "required_modes": ["security-data", "architecture", "tests"],
        "optional_modes": ["data"],
        "agents": ["data-guardian", "requirements-architect", "tester-reviewer"],
        "tests_required": ["isolation", "access_negative"],
        "playwright": "CONDITIONAL",
        "human_gate": "REQUIRED",
    },
    "migration": {
        "required_modes": ["data", "architecture", "tests"],
        "optional_modes": ["security-data"],
        "agents": ["data-guardian", "requirements-architect", "tester-reviewer"],
        "tests_required": ["simulation", "rollback", "regression"],
        "playwright": "NOT_REQUIRED",
        "human_gate": "REQUIRED",
    },
    "dependency": {
        "required_modes": ["code-quality", "security-data"],
        "optional_modes": ["performance", "architecture"],
        "agents": ["tester-reviewer", "data-guardian"],
        "tests_required": ["typecheck", "build", "regression"],
        "playwright": "NOT_REQUIRED",
        "human_gate": "CONDITIONAL",
    },
    "configuration": {
        "required_modes": ["code-quality", "architecture"],
        "optional_modes": ["security-data"],
        "agents": ["tester-reviewer", "requirements-architect"],
        "tests_required": ["configuration"],
        "playwright": "CONDITIONAL",
        "human_gate": "CONDITIONAL",
    },
    "sensitive_change": {
        "required_modes": ["security-data", "architecture", "tests"],
        "optional_modes": ["data"],
        "agents": ["data-guardian", "requirements-architect", "tester-reviewer"],
        "tests_required": ["security", "regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "REQUIRED",
    },
    "release": {
        "required_modes": ["code-quality", "architecture", "tests"],
        "optional_modes": ["security-data", "react-next", "performance", "data"],
        "agents": ["orchestrator", "requirements-architect", "tester-reviewer"],
        "tests_required": ["regression"],
        "playwright": "CONDITIONAL",
        "human_gate": "REQUIRED",
    },
}


def classify_change(change: Mapping[str, Any]) -> str:
    if not isinstance(change, Mapping):
        raise ValueError("change must be an object")
    explicit_kind = change.get("kind") or change.get("change_type")
    if explicit_kind:
        if explicit_kind not in ROUTING_MATRIX:
            raise ValueError(f"unknown change kind: {explicit_kind}")
        return str(explicit_kind)

    files = change.get("files", [])
    if not isinstance(files, Sequence) or isinstance(files, (str, bytes)):
        raise ValueError("files must be a list when kind is not provided")
    path_text = " ".join(str(path).lower().replace("\\", "/") for path in files)
    if any(token in path_text for token in ("migration", "migrate")):
        return "migration"
    if any(token in path_text for token in ("payment", "paiement")):
        return "payment"
    if any(token in path_text for token in ("auth", "permission", "rbac")):
        return "authentication"
    if "package.json" in path_text or "package-lock.json" in path_text:
        return "dependency"
    if "catalogue" in path_text:
        return "catalogue"
    if any(path.endswith((".json", ".csv")) for path in path_text.split()):
        return "data"
    if "next.config" in path_text or ".github/" in path_text:
        return "configuration"
    if "/page." in path_text or path_text.endswith("page.tsx"):
        return "next_page"
    if "components/" in path_text:
        return "react_component"
    if "app/" in path_text:
        return "simple_ui"
    raise ValueError("unable to classify change from the provided diff")


def route_change(change: Mapping[str, Any]) -> dict[str, Any]:
    kind = classify_change(change)
    route = deepcopy(ROUTING_MATRIX[kind])
    route.update(
        {
            "contract_version": CONTRACT_VERSION,
            "kind": kind,
            "parallelism": "READ_ONLY_INDEPENDENT_ONLY",
        }
    )
    return route
