#!/usr/bin/env python3
"""DAS-1 conformance helper (seed).

Goal: make DAS-1 claims less subjective and more testable.

This tool:
- Validates receipt events against the canonical DAS-1 receipt schema.
- Validates exception register entries against the canonical exceptions schema.
- Applies a small set of DAS-1 checks that are machine-verifiable.

Version gating: checks default to DAS-1 v0.002. Pass --das-version v0.003 to
additionally apply the v0.003 controls (AEC-13 delegation, AEC-14 classification
and composition, the tightened AEC-10 cap enforcement, and Annex A autonomy).
v0.002 evidence stays valid under v0.002, which is what the standard promises.

This tool does NOT fully prove conformance with all 12 controls. Some controls
require human-reviewed artifacts (catalog exports, policy docs, drill scorecards).
The intent is to provide an executable core that other tooling can build on.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker


RISK_ORDER = {"R1": 1, "R2": 2, "R3": 3, "R4": 4}
AUTONOMY_ORDER = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5}

# Autonomy levels at which the agent MUST NOT carry out execution itself
# (Annex A.2: A0 sandbox, A1 observe, A2 draft, A3 recommend).
NON_EXECUTING_AUTONOMY = ("A0", "A1", "A2", "A3")

DEFAULT_DAS_VERSION = "v0.002"
RECLASSIFICATION_TRIGGERS = ("tool", "scope", "data_class", "blast_radius")


def _version_tuple(value: str) -> Tuple[int, ...]:
    core = str(value).lstrip("vV").split("-")[0]
    parts: List[int] = []
    for chunk in core.split("."):
        try:
            parts.append(int(chunk))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _is_v0003_or_later(das_version: Optional[str]) -> bool:
    if not das_version:
        return False
    return _version_tuple(das_version) >= _version_tuple("v0.003")


def _risk_gt(a: Optional[str], b: Optional[str]) -> bool:
    """True when risk class a is strictly higher than b."""
    if a not in RISK_ORDER or b not in RISK_ORDER:
        return False
    return RISK_ORDER[a] > RISK_ORDER[b]


@dataclass
class Failure:
    kind: str
    file: str
    message: str
    pointer: str = ""


@dataclass
class OverlayContext:
    overlay_id: str
    receipts_path: Path
    exceptions_path: Path
    drills_path: Path
    schemas_path: Path
    now_utc: datetime
    max_age_days: int


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _iter_json_files(root: Path) -> Iterable[Path]:
    if root.is_file() and root.suffix.lower() == ".json":
        yield root
        return

    for p in root.rglob("*.json"):
        if p.is_file():
            yield p


def _load_json_records(path: Path) -> List[Tuple[str, Any]]:
    records: List[Tuple[str, Any]] = []
    for jf in _iter_json_files(path):
        records.append((str(jf), _load_json(jf)))
    return records


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_against_schema(instance: Any, schema: Dict[str, Any], file: str, kind: str) -> List[Failure]:
    failures: List[Failure] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(instance), key=lambda e: e.path):
        pointer = "/" + "/".join(str(x) for x in err.absolute_path)
        failures.append(
            Failure(
                kind=kind,
                file=file,
                message=err.message,
                pointer=pointer,
            )
        )
    return failures


def _das1_receipt_checks(receipt: Dict[str, Any], file: str) -> List[Failure]:
    failures: List[Failure] = []

    risk = receipt.get("risk_class")
    decision = receipt.get("decision")

    # AEC-03 / AEC-06: R3/R4 allow requires approval + preflight linkage.
    if risk in ("R3", "R4") and decision == "allow":
        for field in ("approval_id", "approver_id", "preflight_id"):
            if not receipt.get(field):
                failures.append(
                    Failure(
                        kind="das1",
                        file=file,
                        message=f"R3/R4 allow requires {field} (AEC-03/AEC-06).",
                        pointer=f"/{field}",
                    )
                )

    # AEC-07: audit trail completeness: for allow decisions, inputs/outputs should be present.
    if decision == "allow":
        if receipt.get("inputs_present") is not True:
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="Allow decision should have inputs_present=true (AEC-07).",
                    pointer="/inputs_present",
                )
            )
        if receipt.get("outputs_present") is not True:
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="Allow decision should have outputs_present=true (AEC-07).",
                    pointer="/outputs_present",
                )
            )

    # AEC-10: cost attribution tags for cost-incurring tools.
    # `cost_incurred` is optional and not part of the canonical schema; treat
    # non-zero cost estimate/actual as cost-incurring for machine checks.
    cost_estimate = receipt.get("cost_estimate")
    cost_actual = receipt.get("cost_actual")
    cost_incurred = (
        receipt.get("cost_incurred") is True
        or (isinstance(cost_estimate, (int, float)) and cost_estimate > 0)
        or (isinstance(cost_actual, (int, float)) and cost_actual > 0)
    )

    if cost_incurred:
        if not receipt.get("owner_id"):
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="cost_incurred=true requires owner_id (AEC-10).",
                    pointer="/owner_id",
                )
            )
        if not receipt.get("cost_center"):
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="cost_incurred=true requires cost_center (AEC-10).",
                    pointer="/cost_center",
                )
            )

    return failures


def _das1_receipt_checks_v0003(receipt: Dict[str, Any], file: str) -> List[Failure]:
    """AEC-13, AEC-14, the tightened AEC-10, and Annex A. Additive to the v0.002 checks."""
    failures: List[Failure] = []

    def fail(message: str, pointer: str) -> None:
        failures.append(Failure(kind="das1", file=file, message=message, pointer=pointer))

    risk = receipt.get("risk_class")
    decision = receipt.get("decision")
    execution_status = receipt.get("execution_status")

    # --- AEC-13: delegated execution must carry a reconstructable lineage ---
    delegation_id = receipt.get("delegation_id")
    parent_actor_id = receipt.get("parent_actor_id")
    delegation_depth = receipt.get("delegation_depth")
    delegated = bool(delegation_id) or bool(parent_actor_id) or (
        isinstance(delegation_depth, int) and delegation_depth > 0
    )

    if delegated:
        for field in ("delegation_id", "parent_actor_id", "root_principal_id", "granted_risk_ceiling"):
            if not receipt.get(field):
                fail(f"Delegated action requires {field} so lineage resolves to the human principal (AEC-13).", f"/{field}")
        if not isinstance(delegation_depth, int):
            fail("Delegated action requires delegation_depth (AEC-13).", "/delegation_depth")
        elif delegation_depth < 1:
            fail("Delegated action requires delegation_depth >= 1 (AEC-13).", "/delegation_depth")

        ceiling = receipt.get("granted_risk_ceiling")
        if _risk_gt(risk, ceiling):
            fail(
                f"Action classified {risk} exceeds granted_risk_ceiling {ceiling}; "
                f"delegated authority must be a subset of the delegating agent's (AEC-13).",
                "/risk_class",
            )

    # --- Annex A.3: autonomy level and risk ceiling intersect, never maximise ---
    autonomy = receipt.get("autonomy_level")
    if autonomy in NON_EXECUTING_AUTONOMY and execution_status == "executed" and risk in ("R3", "R4"):
        fail(
            f"autonomy_level {autonomy} must not record an executed {risk} action; "
            f"at this level a human carries out execution (Annex A.2/A.3).",
            "/execution_status",
        )

    # --- AEC-14: a sequence is governed at its composed class ---
    composition_group_id = receipt.get("composition_group_id")
    composed_class = receipt.get("composed_class")

    if composition_group_id and not composed_class:
        fail("Receipt in a composition group requires composed_class (AEC-14).", "/composed_class")
    if composed_class and not composition_group_id:
        fail("composed_class requires composition_group_id naming the sequence (AEC-14).", "/composition_group_id")
    if composed_class and _risk_gt(risk, composed_class):
        fail(
            f"composed_class {composed_class} is lower than the action's own class {risk}; "
            f"the composed class must be at least the highest individual class (AEC-14).",
            "/composed_class",
        )

    # This is the composition hole: individually-gated actions whose sequence
    # exceeds them must face the gate for the composed class, not their own.
    if composed_class in ("R3", "R4") and decision == "allow":
        for field in ("approval_id", "approver_id", "preflight_id"):
            if not receipt.get(field):
                fail(
                    f"Sequence governed at composed_class {composed_class} requires {field}, "
                    f"even though this action is classified {risk} (AEC-14/AEC-03/AEC-06).",
                    f"/{field}",
                )

    # --- AEC-10: caps are enforced in the execution path, not reported after ---
    if receipt.get("cap_enforcement_point") == "reporting_layer":
        fail(
            "cap_enforcement_point=reporting_layer does not satisfy AEC-10; "
            "the cap must be enforced in the execution path.",
            "/cap_enforcement_point",
        )
    if receipt.get("cap_enforced") is True:
        if receipt.get("cap_enforcement_point") != "execution_path":
            fail("cap_enforced=true requires cap_enforcement_point=execution_path (AEC-10).", "/cap_enforcement_point")
        if not receipt.get("cap_id"):
            fail("cap_enforced=true requires cap_id (AEC-10).", "/cap_id")
        if execution_status not in ("blocked", "queued"):
            fail(
                "cap_enforced=true requires execution_status blocked or queued; "
                "a cap that did not halt execution is not a breaker (AEC-10).",
                "/execution_status",
            )

    return failures


def _das1_exception_checks(exc: Dict[str, Any], file: str) -> List[Failure]:
    failures: List[Failure] = []

    # AEC-11: exceptions expire by default and must not silently renew.
    # Expired entries remain valid historical evidence, but are not applicable
    # to the current conformance window.
    status = exc.get("status")
    expires_at = exc.get("expires_at")
    if isinstance(expires_at, str):
        try:
            dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                failures.append(
                    Failure(
                        kind="das1",
                        file=file,
                        message="expires_at must include timezone (AEC-11).",
                        pointer="/expires_at",
                    )
                )
            else:
                now = datetime.now(dt.tzinfo)
                if status in ("proposed", "approved", "active") and dt <= now:
                    failures.append(
                        Failure(
                            kind="das1",
                            file=file,
                            message=(
                                "Exception is expired and not applicable to the "
                                "current period (AEC-11). Mark as expired/revoked "
                                "or renew with review."
                            ),
                            pointer="/expires_at",
                        )
                    )
                if status == "expired" and dt > now:
                    failures.append(
                        Failure(
                            kind="das1",
                            file=file,
                            message=(
                                "status=expired is inconsistent with a future "
                                "expires_at timestamp (AEC-11)."
                            ),
                            pointer="/status",
                        )
                    )
        except ValueError:
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="expires_at is not a valid ISO-8601 datetime (AEC-11).",
                    pointer="/expires_at",
                )
            )

    return failures


def _parse_iso8601_aware(value: str) -> Optional[datetime]:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return None
        return dt
    except ValueError:
        return None


def _percentile(values: List[float], p: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    rank = (len(ordered) - 1) * p
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    if high == low:
        return float(ordered[low])
    weight = rank - low
    return float(ordered[low] * (1 - weight) + ordered[high] * weight)


def _das1_drill_checks(drill: Dict[str, Any], file: str, now_utc: datetime) -> List[Failure]:
    failures: List[Failure] = []

    executed_at = drill.get("executed_at")
    if isinstance(executed_at, str):
        dt = _parse_iso8601_aware(executed_at)
        if dt is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=file,
                    message="executed_at must be a valid timezone-aware ISO-8601 datetime.",
                    pointer="/executed_at",
                )
            )
        else:
            if dt > now_utc:
                failures.append(
                    Failure(
                        kind="das1",
                        file=file,
                        message="executed_at cannot be in the future.",
                        pointer="/executed_at",
                    )
                )
    else:
        failures.append(
            Failure(
                kind="schema",
                file=file,
                message="Drill report must include executed_at as a string.",
                pointer="/executed_at",
            )
        )

    # A drill that claims a pass must show the outcome that defines the pass.
    drill_id = drill.get("drill_id")
    if drill.get("result") == "pass":
        if drill_id == "D3":
            if drill.get("cascade_complete") is not True:
                failures.append(Failure(kind="das1", file=file, message="D3 pass requires cascade_complete=true (AEC-13).", pointer="/cascade_complete"))
            if drill.get("lineage_reconstructed") is not True:
                failures.append(Failure(kind="das1", file=file, message="D3 pass requires lineage_reconstructed=true (AEC-13).", pointer="/lineage_reconstructed"))
            executed_after = drill.get("descendants_executed_after_revoke")
            if not isinstance(executed_after, int):
                failures.append(Failure(kind="das1", file=file, message="D3 pass requires descendants_executed_after_revoke (AEC-13).", pointer="/descendants_executed_after_revoke"))
            elif executed_after != 0:
                failures.append(Failure(kind="das1", file=file, message=f"D3 cannot pass with {executed_after} descendant execution(s) after revoke (AEC-13).", pointer="/descendants_executed_after_revoke"))
            if drill.get("revocation_within_budget") is not True:
                failures.append(Failure(kind="das1", file=file, message="D3 pass requires the cascade to complete within the AEC-05 revocation budget.", pointer="/revocation_within_budget"))
        elif drill_id == "D4":
            if drill.get("cap_breaker_halted_execution") is not True:
                failures.append(Failure(kind="das1", file=file, message="D4 pass requires cap_breaker_halted_execution=true (AEC-10).", pointer="/cap_breaker_halted_execution"))
            if drill.get("cap_owner_notified") is not True:
                failures.append(Failure(kind="das1", file=file, message="D4 pass requires cap_owner_notified=true; a cap has a named owner (AEC-10).", pointer="/cap_owner_notified"))
            if drill.get("cap_enforcement_point") != "execution_path":
                failures.append(Failure(kind="das1", file=file, message="D4 pass requires cap_enforcement_point=execution_path; a reporting-layer control is not a breaker (AEC-10).", pointer="/cap_enforcement_point"))

    return failures


def verify_drills(
    path: Path,
    schema_path: Path,
    max_age_days: int = 90,
    das_version: str = DEFAULT_DAS_VERSION,
) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)

    failures: List[Failure] = []
    total = 0
    now_utc = datetime.now(timezone.utc)
    required_drills = ("D1", "D2", "D3", "D4") if _is_v0003_or_later(das_version) else ("D1", "D2")
    latest_pass: Dict[str, datetime] = {}
    m8_values: List[float] = []
    m9_values: List[float] = []

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if isinstance(obj, dict):
            failures.extend(_das1_drill_checks(obj, str(jf), now_utc))
            drill_id = obj.get("drill_id")
            result = obj.get("result")
            executed_at = obj.get("executed_at")
            dt = _parse_iso8601_aware(executed_at) if isinstance(executed_at, str) else None
            if drill_id in required_drills and result == "pass" and dt is not None:
                prior = latest_pass.get(drill_id)
                if prior is None or dt > prior:
                    latest_pass[drill_id] = dt

            m8 = obj.get("m8_cap_enforcement_rate")
            if isinstance(m8, (int, float)):
                m8_values.append(float(m8))
            m9 = obj.get("m9_cascade_completion_ms_p95")
            if isinstance(m9, (int, float)):
                m9_values.append(float(m9))
        else:
            failures.append(
                Failure(kind="schema", file=str(jf), message="Drill report must be a JSON object.")
            )

    cutoff = now_utc.timestamp() - (max_age_days * 24 * 60 * 60)
    for drill_id in required_drills:
        dt = latest_pass.get(drill_id)
        if dt is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(path),
                    message=f"Missing required passing drill report for {drill_id}.",
                    pointer=f"/{drill_id}",
                )
            )
            continue
        if dt.timestamp() < cutoff:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(path),
                    message=(
                        f"{drill_id} latest pass is older than {max_age_days} days "
                        f"and not applicable to the current conformance period."
                    ),
                    pointer=f"/{drill_id}",
                )
            )

    report = {
        "kind": "das1-drills",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "das_version": das_version,
        "total_files": total,
        "required_drills": list(required_drills),
        "max_age_days": max_age_days,
        "latest_pass": {k: v.isoformat() for k, v in latest_pass.items()},
        "metrics": {
            "m8_cap_enforcement_rate": {
                "min": min(m8_values) if m8_values else None,
                "sample_size": len(m8_values),
            },
            "m9_delegation_cascade_completion_ms": {
                "p50": _percentile(m9_values, 0.50),
                "p95": _percentile(m9_values, 0.95),
                "sample_size": len(m9_values),
            },
        },
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_receipts(
    path: Path,
    schema_path: Path,
    das_version: str = DEFAULT_DAS_VERSION,
) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)
    apply_v0003 = _is_v0003_or_later(das_version)

    failures: List[Failure] = []
    total = 0
    risk_totals: Dict[str, int] = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    risk_denies: Dict[str, int] = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    risk_blocked_or_queued: Dict[str, int] = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    risk_execution_status_observed: Dict[str, int] = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    r1_r2_allow_total = 0
    r1_r2_allow_gated = 0
    r1_r2_allow_auto = 0
    r1_r2_execution_latency_values: List[float] = []
    r1_r2_execution_latency_observed = 0
    approval_wait_values: List[float] = []

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if isinstance(obj, dict):
            failures.extend(_das1_receipt_checks(obj, str(jf)))
            if apply_v0003:
                failures.extend(_das1_receipt_checks_v0003(obj, str(jf)))

            risk = obj.get("risk_class")
            decision = obj.get("decision")
            if risk in risk_totals:
                risk_totals[risk] += 1
                if decision == "deny":
                    risk_denies[risk] += 1

                execution_status = obj.get("execution_status")
                if execution_status in ("executed", "blocked", "queued", "failed", "noop"):
                    risk_execution_status_observed[risk] += 1
                    if execution_status in ("blocked", "queued"):
                        risk_blocked_or_queued[risk] += 1

            approval_wait_ms = obj.get("approval_wait_ms")
            if isinstance(approval_wait_ms, (int, float)) and approval_wait_ms >= 0:
                approval_wait_values.append(float(approval_wait_ms))

            if risk in ("R1", "R2") and decision == "allow":
                r1_r2_allow_total += 1
                approval_required = obj.get("approval_required")
                gated = (
                    approval_required is True
                    or bool(obj.get("approval_id"))
                    or bool(obj.get("approver_id"))
                )
                if gated:
                    r1_r2_allow_gated += 1
                else:
                    r1_r2_allow_auto += 1

                execution_latency_ms = obj.get("execution_latency_ms")
                if isinstance(execution_latency_ms, (int, float)) and execution_latency_ms >= 0:
                    r1_r2_execution_latency_values.append(float(execution_latency_ms))
                    r1_r2_execution_latency_observed += 1
        else:
            failures.append(
                Failure(kind="schema", file=str(jf), message="Receipt must be a JSON object.")
            )

    blocked_or_queued_rate_by_risk: Dict[str, Optional[float]] = {}
    denied_rate_by_risk: Dict[str, Optional[float]] = {}
    for risk in ("R1", "R2", "R3", "R4"):
        total_risk = risk_totals[risk]
        if total_risk == 0:
            blocked_or_queued_rate_by_risk[risk] = None
            denied_rate_by_risk[risk] = None
        else:
            if risk_execution_status_observed[risk] == 0:
                blocked_or_queued_rate_by_risk[risk] = None
            else:
                blocked_or_queued_rate_by_risk[risk] = risk_blocked_or_queued[risk] / risk_execution_status_observed[risk]
            denied_rate_by_risk[risk] = risk_denies[risk] / total_risk

            if risk_execution_status_observed[risk] < total_risk:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(path),
                        message=(
                            f"M7 measurability gap: risk class {risk} has {total_risk} receipts "
                            f"but only {risk_execution_status_observed[risk]} with execution_status."
                        ),
                        pointer=f"/metrics/m7/{risk}",
                    )
                )

    if r1_r2_allow_total > 0 and r1_r2_execution_latency_observed < r1_r2_allow_total:
        failures.append(
            Failure(
                kind="das1",
                file=str(path),
                message=(
                    "M6 measurability gap: not all R1/R2 allow receipts include execution_latency_ms."
                ),
                pointer="/metrics/m6",
            )
        )

    r1_r2_autonomous_execution_coverage = (
        (r1_r2_allow_auto / r1_r2_allow_total) if r1_r2_allow_total else None
    )

    utility_metrics = {
        "m5_r1_r2_autonomous_execution_coverage": r1_r2_autonomous_execution_coverage,
        "m6_r1_r2_execution_latency_ms": {
            "p50": _percentile(r1_r2_execution_latency_values, 0.50),
            "p95": _percentile(r1_r2_execution_latency_values, 0.95),
            "sample_size": len(r1_r2_execution_latency_values),
            "coverage": (
                (r1_r2_execution_latency_observed / r1_r2_allow_total)
                if r1_r2_allow_total
                else None
            ),
        },
        "m7_blocked_or_queued_rate_by_risk_class": blocked_or_queued_rate_by_risk,
        "supporting": {
            "r1_r2_allow_total": r1_r2_allow_total,
            "r1_r2_allow_auto": r1_r2_allow_auto,
            "r1_r2_allow_gated": r1_r2_allow_gated,
            "denied_rate_by_risk_class": denied_rate_by_risk,
            "execution_status_coverage_by_risk_class": {
                risk: (
                    (risk_execution_status_observed[risk] / risk_totals[risk])
                    if risk_totals[risk]
                    else None
                )
                for risk in ("R1", "R2", "R3", "R4")
            },
            "approval_wait_ms": {
                "p50": _percentile(approval_wait_values, 0.50),
                "p95": _percentile(approval_wait_values, 0.95),
                "sample_size": len(approval_wait_values),
            },
        },
    }

    report = {
        "kind": "das1-receipts",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "das_version": das_version,
        "total_files": total,
        "metrics": utility_metrics,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_exceptions(path: Path, schema_path: Path) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)

    failures: List[Failure] = []
    total = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if isinstance(obj, dict):
            failures.extend(_das1_exception_checks(obj, str(jf)))
        else:
            failures.append(
                Failure(kind="schema", file=str(jf), message="Exception entry must be a JSON object.")
            )

    report = {
        "kind": "das1-exceptions",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_tool_catalogs(
    path: Path,
    schema_path: Path,
    das_version: str = DEFAULT_DAS_VERSION,
) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)
    apply_v0003 = _is_v0003_or_later(das_version)
    failures: List[Failure] = []
    total = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(
                Failure(kind="schema", file=str(jf), message="Tool catalog must be a JSON object.")
            )
            continue

        generated_at = _parse_iso8601_aware(str(obj.get("generated_at", "")))
        if generated_at is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="generated_at must be a valid timezone-aware ISO-8601 datetime (AEC-01).",
                    pointer="/generated_at",
                )
            )
        elif generated_at > datetime.now(timezone.utc):
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="generated_at cannot be in the future (AEC-01).",
                    pointer="/generated_at",
                )
            )

        seen_tools = set()
        for idx, tool in enumerate(obj.get("tools", [])):
            if not isinstance(tool, dict):
                continue
            tool_name = tool.get("tool")
            if isinstance(tool_name, str):
                if tool_name in seen_tools:
                    failures.append(
                        Failure(
                            kind="das1",
                            file=str(jf),
                            message=f"Duplicate tool entry '{tool_name}' in catalog (AEC-01).",
                            pointer=f"/tools/{idx}/tool",
                        )
                    )
                seen_tools.add(tool_name)

            if apply_v0003:
                # Annex A.3: both axes must appear on the catalog entry, so a
                # promotion along one is visible as a change to that one alone.
                for field in ("risk_ceiling", "autonomy_level"):
                    if not tool.get(field):
                        failures.append(
                            Failure(
                                kind="das1",
                                file=str(jf),
                                message=f"Tool entry '{tool_name}' requires {field} (AEC-01/Annex A.3).",
                                pointer=f"/tools/{idx}/{field}",
                            )
                        )

    report = {
        "kind": "das1-tool-catalogs",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "das_version": das_version,
        "total_files": total,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_policy_snapshots(path: Path, schema_path: Path) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)
    failures: List[Failure] = []
    total = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(
                Failure(kind="schema", file=str(jf), message="Policy snapshot must be a JSON object.")
            )
            continue

        generated_at = _parse_iso8601_aware(str(obj.get("generated_at", "")))
        if generated_at is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="generated_at must be a valid timezone-aware ISO-8601 datetime (AEC-02/AEC-04).",
                    pointer="/generated_at",
                )
            )

        ttl_policy = obj.get("credential_ttl_policy", {})
        max_ttl = ttl_policy.get("max_ttl_seconds") if isinstance(ttl_policy, dict) else None
        no_shared = ttl_policy.get("no_shared_credentials") if isinstance(ttl_policy, dict) else None

        for idx, cred in enumerate(obj.get("credentials", [])):
            if not isinstance(cred, dict):
                continue
            ttl = cred.get("ttl_seconds")
            shared = cred.get("shared")

            if isinstance(max_ttl, (int, float)) and isinstance(ttl, (int, float)) and ttl > max_ttl:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message=(
                            f"Credential ttl_seconds ({ttl}) exceeds credential_ttl_policy.max_ttl_seconds "
                            f"({max_ttl}) (AEC-02)."
                        ),
                        pointer=f"/credentials/{idx}/ttl_seconds",
                    )
                )
            if no_shared is True and shared is True:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message="Shared credentials are disallowed by policy (AEC-02).",
                        pointer=f"/credentials/{idx}/shared",
                    )
                )

    report = {
        "kind": "das1-policy-snapshots",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_ir_annexes(path: Path, schema_path: Path, max_age_days: int = 365) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)
    failures: List[Failure] = []
    total = 0
    now_utc = datetime.now(timezone.utc)

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(
                Failure(kind="schema", file=str(jf), message="IR annex must be a JSON object.")
            )
            continue

        annex_generated = _parse_iso8601_aware(str(obj.get("generated_at", "")))
        if annex_generated is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="generated_at must be a valid timezone-aware ISO-8601 datetime (AEC-12).",
                    pointer="/generated_at",
                )
            )

        tabletop = obj.get("tabletop", {})
        if isinstance(tabletop, dict):
            dt = _parse_iso8601_aware(str(tabletop.get("last_executed_at", "")))
            if dt is None:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message="tabletop.last_executed_at must be a valid timezone-aware ISO-8601 datetime (AEC-12).",
                        pointer="/tabletop/last_executed_at",
                    )
                )
            else:
                if (now_utc - dt).total_seconds() > (max_age_days * 24 * 60 * 60):
                    failures.append(
                        Failure(
                            kind="das1",
                            file=str(jf),
                            message=f"IR tabletop execution is older than {max_age_days} days (AEC-12).",
                            pointer="/tabletop/last_executed_at",
                        )
                    )

    report = {
        "kind": "das1-ir-annexes",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "max_age_days": max_age_days,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def _resolve_ref(base_file: Path, ref: str) -> Path:
    ref_path = Path(ref)
    if ref_path.is_absolute():
        return ref_path
    return (base_file.parent / ref_path).resolve()


def verify_claims(path: Path, schema_path: Path, max_age_days: int = 90) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)
    failures: List[Failure] = []
    total = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(
                Failure(kind="schema", file=str(jf), message="Claim packet must be a JSON object.")
            )
            continue

        generated_at = _parse_iso8601_aware(str(obj.get("generated_at", "")))
        if generated_at is None:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="generated_at must be a valid timezone-aware ISO-8601 datetime.",
                    pointer="/generated_at",
                )
            )
            continue

        non_cert_stmt = (
            obj.get("disclosures", {}).get("non_certification_statement", "")
            if isinstance(obj.get("disclosures"), dict)
            else ""
        )
        if "not a certification" not in str(non_cert_stmt).lower():
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message='Disclosure must include a non-certification statement containing "not a certification".',
                    pointer="/disclosures/non_certification_statement",
                )
            )

        report_ref = (
            obj.get("evidence", {}).get("conformance_report_ref", "")
            if isinstance(obj.get("evidence"), dict)
            else ""
        )
        if not isinstance(report_ref, str) or not report_ref.strip():
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="Claim packet requires evidence.conformance_report_ref.",
                    pointer="/evidence/conformance_report_ref",
                )
            )
            continue

        report_path = _resolve_ref(jf, report_ref)
        if not report_path.exists():
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message=f"Referenced conformance report not found: {report_path}",
                    pointer="/evidence/conformance_report_ref",
                )
            )
            continue

        try:
            conformance_report = _load_json(report_path)
        except Exception as exc:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message=f"Unable to read referenced conformance report: {exc}",
                    pointer="/evidence/conformance_report_ref",
                )
            )
            continue

        if not isinstance(conformance_report, dict):
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="Referenced conformance report must be a JSON object.",
                    pointer="/evidence/conformance_report_ref",
                )
            )
            continue

        if conformance_report.get("pass") is not True:
            failures.append(
                Failure(
                    kind="das1",
                    file=str(jf),
                    message="Referenced conformance report is not passing.",
                    pointer="/evidence/conformance_report_ref",
                )
            )

        claim_version = str(obj.get("das_version", ""))
        claim_is_v0003 = _is_v0003_or_later(claim_version)
        required_claim_drills = ("D1", "D2", "D3", "D4") if claim_is_v0003 else ("D1", "D2")

        scope = obj.get("scope", {}) if isinstance(obj.get("scope"), dict) else {}
        core_conformant = scope.get("core_conformant")
        core_sections = ("receipts", "exceptions", "drills")
        if core_conformant is True and claim_is_v0003:
            core_sections = core_sections + ("delegation_records", "classification_registers")
        if core_conformant is True:
            for section in core_sections:
                sec = conformance_report.get(section)
                if not isinstance(sec, dict) or sec.get("pass") is not True:
                    failures.append(
                        Failure(
                            kind="das1",
                            file=str(jf),
                            message=(
                                f"Core claim requires passing {section} section in referenced conformance report."
                                + (
                                    f" ({claim_version} claims must evidence AEC-13 and AEC-14.)"
                                    if section in ("delegation_records", "classification_registers")
                                    else ""
                                )
                            ),
                            pointer="/scope/core_conformant",
                        )
                    )

        # Required disclosure: last required drill pass dates
        drill_disclosure = (
            obj.get("disclosures", {}).get("last_required_drill_pass_at", {})
            if isinstance(obj.get("disclosures"), dict)
            else {}
        )
        if not isinstance(drill_disclosure, dict):
            drill_disclosure = {}

        for drill_id in required_claim_drills:
            dt = _parse_iso8601_aware(str(drill_disclosure.get(drill_id, "")))
            if dt is None:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message=f"Disclosure for {drill_id} must be a valid timezone-aware ISO-8601 datetime.",
                        pointer=f"/disclosures/last_required_drill_pass_at/{drill_id}",
                    )
                )
                continue
            if (generated_at - dt).total_seconds() > (max_age_days * 24 * 60 * 60):
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message=f"Disclosure for {drill_id} is older than {max_age_days} days.",
                        pointer=f"/disclosures/last_required_drill_pass_at/{drill_id}",
                    )
                )

        report_drills = conformance_report.get("drills", {})
        latest_pass = report_drills.get("latest_pass", {}) if isinstance(report_drills, dict) else {}
        if isinstance(latest_pass, dict):
            for drill_id in required_claim_drills:
                claimed = _parse_iso8601_aware(str(drill_disclosure.get(drill_id, "")))
                observed = _parse_iso8601_aware(str(latest_pass.get(drill_id, "")))
                if claimed is not None and observed is not None and claimed != observed:
                    failures.append(
                        Failure(
                            kind="das1",
                            file=str(jf),
                            message=(
                                f"Disclosure for {drill_id} does not match referenced report "
                                f"latest pass ({observed.isoformat()})."
                            ),
                            pointer=f"/disclosures/last_required_drill_pass_at/{drill_id}",
                        )
                    )

        overlay_claims = scope.get("overlay_claims", [])
        if not isinstance(overlay_claims, list):
            overlay_claims = []
        report_overlays = conformance_report.get("overlays", {})
        if not isinstance(report_overlays, dict):
            report_overlays = {}

        for overlay_id in overlay_claims:
            overlay_report = report_overlays.get(overlay_id)
            if not isinstance(overlay_report, dict) or overlay_report.get("pass") is not True:
                failures.append(
                    Failure(
                        kind="das1",
                        file=str(jf),
                        message=f"Overlay claim '{overlay_id}' requires passing overlay evidence in referenced report.",
                        pointer="/scope/overlay_claims",
                    )
                )

    report = {
        "kind": "das1-claims",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "max_age_days": max_age_days,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_delegation_records(path: Path, schema_path: Path) -> Tuple[List[Failure], Dict[str, Any]]:
    """AEC-13. Checks the subset rule per record, then cascade integrity across the set."""
    schema = _load_json(schema_path)
    failures: List[Failure] = []
    total = 0
    now_utc = datetime.now(timezone.utc)
    records: Dict[str, Dict[str, Any]] = {}
    record_files: Dict[str, str] = {}

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(Failure(kind="schema", file=str(jf), message="Delegation record must be a JSON object."))
            continue

        file = str(jf)

        def fail(message: str, pointer: str) -> None:
            failures.append(Failure(kind="das1", file=file, message=message, pointer=pointer))

        delegation_id = obj.get("delegation_id")
        if isinstance(delegation_id, str):
            if delegation_id in records:
                fail(f"Duplicate delegation_id '{delegation_id}' (AEC-13).", "/delegation_id")
            records[delegation_id] = obj
            record_files[delegation_id] = file

        issued_at = _parse_iso8601_aware(str(obj.get("issued_at", "")))
        expires_at = _parse_iso8601_aware(str(obj.get("expires_at", "")))
        if issued_at is None:
            fail("issued_at must be a valid timezone-aware ISO-8601 datetime (AEC-13).", "/issued_at")
        if expires_at is None:
            fail("expires_at must be a valid timezone-aware ISO-8601 datetime; every delegation expires (AEC-13).", "/expires_at")
        if issued_at is not None and expires_at is not None and expires_at <= issued_at:
            fail("expires_at must be after issued_at (AEC-13).", "/expires_at")

        status = obj.get("status")
        if status == "active" and expires_at is not None and expires_at <= now_utc:
            fail("status=active is inconsistent with a past expires_at; the delegation has lapsed (AEC-13).", "/status")
        if status == "revoked" and not obj.get("revoked_at"):
            fail("status=revoked requires revoked_at (AEC-13).", "/revoked_at")

        depth = obj.get("delegation_depth")
        if isinstance(depth, int) and depth > 0 and not obj.get("parent_delegation_id"):
            fail("delegation_depth > 0 requires parent_delegation_id so lineage is reconstructable (AEC-13).", "/parent_delegation_id")

        if obj.get("delegating_actor_id") == obj.get("delegated_actor_id"):
            fail("delegating_actor_id and delegated_actor_id must differ (AEC-13).", "/delegated_actor_id")

        # The subset rule. Checkable from the record alone when delegating_scope is present.
        granted = obj.get("granted_scope") if isinstance(obj.get("granted_scope"), dict) else {}
        parent_scope = obj.get("delegating_scope") if isinstance(obj.get("delegating_scope"), dict) else None
        if parent_scope is not None:
            for field in ("tools", "data_classes", "actions"):
                child_vals = granted.get(field)
                parent_vals = parent_scope.get(field)
                if isinstance(child_vals, list) and isinstance(parent_vals, list):
                    extra = sorted(set(child_vals) - set(parent_vals))
                    if extra:
                        fail(
                            f"granted_scope.{field} grants {extra} not held by the delegating agent; "
                            f"delegated authority must be a subset (AEC-13).",
                            f"/granted_scope/{field}",
                        )

            granted_ceiling = obj.get("granted_risk_ceiling")
            parent_ceiling = parent_scope.get("risk_ceiling")
            if _risk_gt(granted_ceiling, parent_ceiling):
                fail(
                    f"granted_risk_ceiling {granted_ceiling} exceeds the delegating agent's {parent_ceiling} (AEC-13).",
                    "/granted_risk_ceiling",
                )

            granted_autonomy = obj.get("granted_autonomy_level")
            parent_autonomy = parent_scope.get("autonomy_level")
            if (
                granted_autonomy in AUTONOMY_ORDER
                and parent_autonomy in AUTONOMY_ORDER
                and AUTONOMY_ORDER[granted_autonomy] > AUTONOMY_ORDER[parent_autonomy]
            ):
                fail(
                    f"granted_autonomy_level {granted_autonomy} exceeds the delegating agent's "
                    f"{parent_autonomy}; the subset rule applies to both axes (AEC-13/Annex A.3).",
                    "/granted_autonomy_level",
                )

    # Cascade integrity across the whole set.
    revoked_ids = {rid for rid, rec in records.items() if rec.get("status") == "revoked"}
    orphans = 0
    for delegation_id, rec in records.items():
        parent_id = rec.get("parent_delegation_id")
        if not parent_id:
            continue
        if parent_id not in records:
            orphans += 1
            failures.append(
                Failure(
                    kind="das1",
                    file=record_files[delegation_id],
                    message=f"parent_delegation_id '{parent_id}' does not resolve to a delegation record; lineage is broken (AEC-13).",
                    pointer="/parent_delegation_id",
                )
            )
            continue

        # Walk to the root so a revocation anywhere above is caught, not just the immediate parent.
        ancestor = parent_id
        seen = {delegation_id}
        while ancestor:
            if ancestor in seen:
                failures.append(
                    Failure(
                        kind="das1",
                        file=record_files[delegation_id],
                        message=f"Delegation lineage contains a cycle at '{ancestor}' (AEC-13).",
                        pointer="/parent_delegation_id",
                    )
                )
                break
            seen.add(ancestor)
            if ancestor in revoked_ids and rec.get("status") == "active":
                failures.append(
                    Failure(
                        kind="das1",
                        file=record_files[delegation_id],
                        message=(
                            f"Delegation is still active while ancestor '{ancestor}' is revoked; "
                            f"revocation must cascade to every descendant (AEC-13)."
                        ),
                        pointer="/status",
                    )
                )
                break
            ancestor = records.get(ancestor, {}).get("parent_delegation_id")

    report = {
        "kind": "das1-delegation-records",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "total_records": len(records),
        "revoked_records": len(revoked_ids),
        "orphan_records": orphans,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_classification_registers(path: Path, schema_path: Path) -> Tuple[List[Failure], Dict[str, Any]]:
    """AEC-14. Checks the stated procedure and every composition test case."""
    schema = _load_json(schema_path)
    failures: List[Failure] = []
    total = 0
    composition_cases = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if not isinstance(obj, dict):
            failures.append(Failure(kind="schema", file=str(jf), message="Classification register must be a JSON object."))
            continue

        file = str(jf)

        def fail(message: str, pointer: str) -> None:
            failures.append(Failure(kind="das1", file=file, message=message, pointer=pointer))

        generated_at = _parse_iso8601_aware(str(obj.get("generated_at", "")))
        if generated_at is None:
            fail("generated_at must be a valid timezone-aware ISO-8601 datetime (AEC-14).", "/generated_at")

        # AEC-14: the default must be stated, and the stated default must be the higher class.
        if obj.get("ambiguity_default") != "higher_class":
            fail(
                "ambiguity_default must be higher_class; AEC-14 requires the default posture on "
                "ambiguous classification to be the higher class.",
                "/ambiguity_default",
            )

        triggers = obj.get("reclassification_triggers")
        if isinstance(triggers, list):
            missing = [t for t in RECLASSIFICATION_TRIGGERS if t not in triggers]
            if missing:
                fail(
                    f"reclassification_triggers is missing {missing}; AEC-14 requires review when the "
                    f"tool, its scope, its data class, or its blast radius changes.",
                    "/reclassification_triggers",
                )

        entries = obj.get("entries") if isinstance(obj.get("entries"), list) else []
        entry_by_id: Dict[str, Dict[str, Any]] = {}
        for idx, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("entry_id")
            if isinstance(entry_id, str):
                if entry_id in entry_by_id:
                    fail(f"Duplicate entry_id '{entry_id}' (AEC-14).", f"/entries/{idx}/entry_id")
                entry_by_id[entry_id] = entry
            reviewed_at = _parse_iso8601_aware(str(entry.get("reviewed_at", "")))
            if reviewed_at is None:
                fail(f"Entry '{entry_id}' requires a valid reviewed_at (AEC-14).", f"/entries/{idx}/reviewed_at")
            if entry.get("contested") is True and not entry.get("contest_resolution_ref"):
                fail(
                    f"Entry '{entry_id}' is marked contested and requires contest_resolution_ref (AEC-14).",
                    f"/entries/{idx}/contest_resolution_ref",
                )

        rules = obj.get("composition_rules") if isinstance(obj.get("composition_rules"), list) else []
        if not rules:
            fail(
                "Register requires at least one composition_rules entry; AEC-14 takes a composition "
                "test case as part of its receipt.",
                "/composition_rules",
            )

        for idx, rule in enumerate(rules):
            if not isinstance(rule, dict):
                continue
            composition_cases += 1
            group = rule.get("composition_group_id")
            members = rule.get("member_entry_ids") if isinstance(rule.get("member_entry_ids"), list) else []
            declared_max = rule.get("individual_max_class")
            composed = rule.get("composed_class")
            governed = rule.get("governed_at_class")

            unresolved = [m for m in members if m not in entry_by_id]
            if unresolved:
                fail(
                    f"Composition rule '{group}' references entries not in the register: {unresolved} (AEC-14).",
                    f"/composition_rules/{idx}/member_entry_ids",
                )

            observed = [entry_by_id[m].get("risk_class") for m in members if m in entry_by_id]
            observed = [r for r in observed if r in RISK_ORDER]
            if observed:
                actual_max = max(observed, key=lambda r: RISK_ORDER[r])
                if declared_max != actual_max:
                    fail(
                        f"Composition rule '{group}' declares individual_max_class {declared_max} but its "
                        f"member entries top out at {actual_max} (AEC-14).",
                        f"/composition_rules/{idx}/individual_max_class",
                    )

            if _risk_gt(declared_max, composed):
                fail(
                    f"Composition rule '{group}' has composed_class {composed} below individual_max_class "
                    f"{declared_max}; a sequence is never governed below its highest member (AEC-14).",
                    f"/composition_rules/{idx}/composed_class",
                )

            if governed != composed:
                fail(
                    f"Composition rule '{group}' is governed at {governed} but composes to {composed}; "
                    f"the sequence must be governed at the composed class (AEC-14).",
                    f"/composition_rules/{idx}/governed_at_class",
                )

    report = {
        "kind": "das1-classification-registers",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
        "composition_cases": composition_cases,
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def _load_overlay_plugin(overlay_id: str, overlay_dir: Path):
    module_name = overlay_id.replace("-", "_")
    plugin_path = overlay_dir / f"{module_name}.py"
    if not plugin_path.exists():
        raise FileNotFoundError(f"Overlay plugin not found: {plugin_path}")

    spec = importlib.util.spec_from_file_location(f"das1_overlay_{module_name}", plugin_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load overlay plugin: {plugin_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_overlay_failures(overlay_id: str, raw_failures: Any) -> List[Failure]:
    failures: List[Failure] = []
    if not isinstance(raw_failures, list):
        return [
            Failure(
                kind=f"overlay:{overlay_id}",
                file=overlay_id,
                message="Overlay plugin returned invalid failures payload (expected list).",
            )
        ]

    for item in raw_failures:
        if isinstance(item, dict):
            failures.append(
                Failure(
                    kind=str(item.get("kind") or f"overlay:{overlay_id}"),
                    file=str(item.get("file") or overlay_id),
                    message=str(item.get("message") or "Overlay check failed."),
                    pointer=str(item.get("pointer") or ""),
                )
            )
        else:
            failures.append(
                Failure(
                    kind=f"overlay:{overlay_id}",
                    file=overlay_id,
                    message=str(item),
                )
            )
    return failures


def run_overlay_checks(
    overlays: List[str],
    overlay_dir: Path,
    receipts_path: Path,
    exceptions_path: Path,
    drills_path: Path,
    schemas_path: Path,
    max_age_days: int,
) -> Tuple[List[Failure], Dict[str, Any]]:
    all_failures: List[Failure] = []
    reports: Dict[str, Any] = {}
    now_utc = datetime.now(timezone.utc)

    for overlay_id in overlays:
        context = OverlayContext(
            overlay_id=overlay_id,
            receipts_path=receipts_path,
            exceptions_path=exceptions_path,
            drills_path=drills_path,
            schemas_path=schemas_path,
            now_utc=now_utc,
            max_age_days=max_age_days,
        )

        try:
            module = _load_overlay_plugin(overlay_id, overlay_dir)
        except Exception as exc:
            failure = Failure(
                kind=f"overlay:{overlay_id}",
                file=str(overlay_dir),
                message=str(exc),
            )
            all_failures.append(failure)
            reports[overlay_id] = {"overlay_id": overlay_id, "error": str(exc), "failures": [failure.__dict__]}
            continue

        run_fn = getattr(module, "run_overlay_checks", None)
        if run_fn is None:
            failure = Failure(
                kind=f"overlay:{overlay_id}",
                file=str(overlay_dir / f"{overlay_id.replace('-', '_')}.py"),
                message="Overlay plugin must expose run_overlay_checks(context).",
            )
            all_failures.append(failure)
            reports[overlay_id] = {"overlay_id": overlay_id, "failures": [failure.__dict__]}
            continue

        try:
            result = run_fn(context, _load_json_records, _parse_iso8601_aware)
        except Exception as exc:
            failure = Failure(
                kind=f"overlay:{overlay_id}",
                file=str(overlay_dir / f"{overlay_id.replace('-', '_')}.py"),
                message=f"Overlay plugin execution failed: {exc}",
            )
            all_failures.append(failure)
            reports[overlay_id] = {"overlay_id": overlay_id, "error": str(exc), "failures": [failure.__dict__]}
            continue

        if not isinstance(result, dict):
            failure = Failure(
                kind=f"overlay:{overlay_id}",
                file=overlay_id,
                message="Overlay plugin returned invalid result (expected object).",
            )
            all_failures.append(failure)
            reports[overlay_id] = {"overlay_id": overlay_id, "failures": [failure.__dict__]}
            continue

        overlay_failures = _normalize_overlay_failures(overlay_id, result.get("failures", []))
        all_failures.extend(overlay_failures)
        reports[overlay_id] = {
            "overlay_id": overlay_id,
            "details": result.get("details", {}),
            "failures": [f.__dict__ for f in overlay_failures],
            "pass": len(overlay_failures) == 0,
        }

    return all_failures, reports


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="das1", description="DAS-1 conformance helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_verify = sub.add_parser("verify", help="verify core conformance (receipts, exceptions, drills)")
    p_verify.add_argument("--receipts", type=str, required=True, help="path to receipts directory")
    p_verify.add_argument("--exceptions", type=str, required=True, help="path to exceptions directory")
    p_verify.add_argument("--drills", type=str, required=True, help="path to drills directory")
    p_verify.add_argument("--tool-catalogs", type=str, required=True, help="path to tool catalogs directory")
    p_verify.add_argument("--policy-snapshots", type=str, required=True, help="path to policy snapshots directory")
    p_verify.add_argument("--ir-annexes", type=str, required=True, help="path to incident response annexes directory")
    p_verify.add_argument("--schemas", type=str, default="schemas", help="schemas directory")
    p_verify.add_argument("--drill-max-age-days", type=int, default=90, help="max age for required D1/D2 passes")
    p_verify.add_argument("--ir-max-age-days", type=int, default=365, help="max age for IR tabletop evidence")
    p_verify.add_argument("--das-version", type=str, default=DEFAULT_DAS_VERSION, help="DAS-1 version to check against (v0.002 default; v0.003 adds AEC-13/AEC-14/Annex A and the tightened AEC-10)")
    p_verify.add_argument("--delegation-records", type=str, default=None, help="path to delegation records directory (required at v0.003)")
    p_verify.add_argument("--classification-registers", type=str, default=None, help="path to classification registers directory (required at v0.003)")
    p_verify.add_argument("--overlay", action="append", default=[], help="overlay plugin id (repeatable)")
    p_verify.add_argument("--overlay-dir", type=str, default="tools/overlays", help="overlay plugin directory")
    p_verify.add_argument("--report", type=str, default="conformance-report.json", help="output report path")

    p_r = sub.add_parser("verify-receipts", help="verify receipts")
    p_r.add_argument("path", type=str)
    p_r.add_argument("--schema", type=str, default="schemas/receipt.schema.json")
    p_r.add_argument("--report", type=str, default="receipt-report.json")

    p_e = sub.add_parser("verify-exceptions", help="verify exceptions")
    p_e.add_argument("path", type=str)
    p_e.add_argument("--schema", type=str, default="schemas/exception.schema.json")
    p_e.add_argument("--report", type=str, default="exceptions-report.json")

    p_d = sub.add_parser("verify-drills", help="verify drill reports")
    p_d.add_argument("path", type=str)
    p_d.add_argument("--schema", type=str, default="schemas/drill-report.schema.json")
    p_d.add_argument("--max-age-days", type=int, default=90)
    p_d.add_argument("--report", type=str, default="drills-report.json")

    p_c = sub.add_parser("verify-claims", help="verify conformance claim packets")
    p_c.add_argument("path", type=str)
    p_c.add_argument("--schema", type=str, default="schemas/conformance-claim.schema.json")
    p_c.add_argument("--max-age-days", type=int, default=90)
    p_c.add_argument("--report", type=str, default="claims-report.json")

    p_tc = sub.add_parser("verify-tool-catalogs", help="verify tool catalog artifacts")
    p_tc.add_argument("path", type=str)
    p_tc.add_argument("--schema", type=str, default="schemas/tool-catalog.schema.json")
    p_tc.add_argument("--report", type=str, default="tool-catalogs-report.json")

    p_ps = sub.add_parser("verify-policy-snapshots", help="verify policy snapshot artifacts")
    p_ps.add_argument("path", type=str)
    p_ps.add_argument("--schema", type=str, default="schemas/policy-snapshot.schema.json")
    p_ps.add_argument("--report", type=str, default="policy-snapshots-report.json")

    p_ir = sub.add_parser("verify-ir-annexes", help="verify incident response annex artifacts")
    p_ir.add_argument("path", type=str)
    p_ir.add_argument("--schema", type=str, default="schemas/ir-annex.schema.json")
    p_ir.add_argument("--max-age-days", type=int, default=365)
    p_ir.add_argument("--report", type=str, default="ir-annexes-report.json")

    p_dr = sub.add_parser("verify-delegation-records", help="verify AEC-13 delegation records")
    p_dr.add_argument("path", type=str)
    p_dr.add_argument("--schema", type=str, default="schemas/delegation-record.schema.json")
    p_dr.add_argument("--report", type=str, default="delegation-records-report.json")

    p_cr = sub.add_parser("verify-classification-registers", help="verify AEC-14 classification registers")
    p_cr.add_argument("path", type=str)
    p_cr.add_argument("--schema", type=str, default="schemas/classification-register.schema.json")
    p_cr.add_argument("--report", type=str, default="classification-registers-report.json")

    p_o = sub.add_parser("verify-overlay", help="verify core plus overlay plugin checks")
    p_o.add_argument("--receipts", type=str, required=True, help="path to receipts directory")
    p_o.add_argument("--exceptions", type=str, required=True, help="path to exceptions directory")
    p_o.add_argument("--drills", type=str, required=True, help="path to drills directory")
    p_o.add_argument("--tool-catalogs", type=str, required=True, help="path to tool catalogs directory")
    p_o.add_argument("--policy-snapshots", type=str, required=True, help="path to policy snapshots directory")
    p_o.add_argument("--ir-annexes", type=str, required=True, help="path to incident response annexes directory")
    p_o.add_argument("--schemas", type=str, default="schemas", help="schemas directory")
    p_o.add_argument("--drill-max-age-days", type=int, default=90, help="max age for required D1/D2 passes")
    p_o.add_argument("--ir-max-age-days", type=int, default=365, help="max age for IR tabletop evidence")
    p_o.add_argument("--das-version", type=str, default=DEFAULT_DAS_VERSION, help="DAS-1 version to check against")
    p_o.add_argument("--delegation-records", type=str, default=None, help="path to delegation records directory (required at v0.003)")
    p_o.add_argument("--classification-registers", type=str, default=None, help="path to classification registers directory (required at v0.003)")
    p_o.add_argument("--overlay", action="append", required=True, help="overlay plugin id (repeatable)")
    p_o.add_argument("--overlay-dir", type=str, default="tools/overlays", help="overlay plugin directory")
    p_o.add_argument("--report", type=str, default="overlay-report.json", help="output report path")

    args = parser.parse_args(argv)

    if args.cmd == "verify-receipts":
        failures, report = verify_receipts(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-exceptions":
        failures, report = verify_exceptions(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-drills":
        failures, report = verify_drills(Path(args.path), Path(args.schema), max_age_days=args.max_age_days)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-claims":
        failures, report = verify_claims(Path(args.path), Path(args.schema), max_age_days=args.max_age_days)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-delegation-records":
        failures, report = verify_delegation_records(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-classification-registers":
        failures, report = verify_classification_registers(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-tool-catalogs":
        failures, report = verify_tool_catalogs(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-policy-snapshots":
        failures, report = verify_policy_snapshots(Path(args.path), Path(args.schema))
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd == "verify-ir-annexes":
        failures, report = verify_ir_annexes(Path(args.path), Path(args.schema), max_age_days=args.max_age_days)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"pass": report["pass"], "failures": len(failures)}))
        return 1 if failures else 0

    if args.cmd in ("verify", "verify-overlay"):
        receipts_dir = Path(args.receipts)
        exceptions_dir = Path(args.exceptions)
        drills_dir = Path(args.drills)
        tool_catalogs_dir = Path(args.tool_catalogs)
        policy_snapshots_dir = Path(args.policy_snapshots)
        ir_annexes_dir = Path(args.ir_annexes)
        schemas_dir = Path(args.schemas)
        overlay_dir = Path(args.overlay_dir)
        overlays = args.overlay or []
        das_version = args.das_version
        apply_v0003 = _is_v0003_or_later(das_version)

        receipt_failures, receipt_report = verify_receipts(
            receipts_dir, schemas_dir / "receipt.schema.json", das_version=das_version
        )
        exc_failures, exc_report = verify_exceptions(exceptions_dir, schemas_dir / "exception.schema.json")
        drill_failures, drill_report = verify_drills(
            drills_dir,
            schemas_dir / "drill-report.schema.json",
            max_age_days=args.drill_max_age_days,
            das_version=das_version,
        )
        tool_catalog_failures, tool_catalog_report = verify_tool_catalogs(
            tool_catalogs_dir, schemas_dir / "tool-catalog.schema.json", das_version=das_version
        )
        policy_snapshot_failures, policy_snapshot_report = verify_policy_snapshots(
            policy_snapshots_dir, schemas_dir / "policy-snapshot.schema.json"
        )
        ir_annex_failures, ir_annex_report = verify_ir_annexes(
            ir_annexes_dir, schemas_dir / "ir-annex.schema.json", max_age_days=args.ir_max_age_days
        )
        # AEC-13 and AEC-14 evidence. Only demanded at v0.003, so v0.002
        # invocations keep working unchanged.
        delegation_failures: List[Failure] = []
        delegation_report: Dict[str, Any] = {"kind": "das1-delegation-records", "skipped": True, "pass": True}
        classification_failures: List[Failure] = []
        classification_report: Dict[str, Any] = {"kind": "das1-classification-registers", "skipped": True, "pass": True}

        if args.delegation_records:
            delegation_failures, delegation_report = verify_delegation_records(
                Path(args.delegation_records), schemas_dir / "delegation-record.schema.json"
            )
        elif apply_v0003:
            delegation_failures = [
                Failure(
                    kind="das1",
                    file=str(receipts_dir),
                    message=f"{das_version} requires --delegation-records; AEC-13 takes delegation records as its receipt.",
                    pointer="/delegation_records",
                )
            ]
            delegation_report = {
                "kind": "das1-delegation-records",
                "generated_at": _utcnow_iso(),
                "failures": [f.__dict__ for f in delegation_failures],
                "pass": False,
            }

        if args.classification_registers:
            classification_failures, classification_report = verify_classification_registers(
                Path(args.classification_registers), schemas_dir / "classification-register.schema.json"
            )
        elif apply_v0003:
            classification_failures = [
                Failure(
                    kind="das1",
                    file=str(receipts_dir),
                    message=f"{das_version} requires --classification-registers; AEC-14 takes a classification register as its receipt.",
                    pointer="/classification_registers",
                )
            ]
            classification_report = {
                "kind": "das1-classification-registers",
                "generated_at": _utcnow_iso(),
                "failures": [f.__dict__ for f in classification_failures],
                "pass": False,
            }

        overlay_failures: List[Failure] = []
        overlay_reports: Dict[str, Any] = {}
        if overlays:
            overlay_failures, overlay_reports = run_overlay_checks(
                overlays=overlays,
                overlay_dir=overlay_dir,
                receipts_path=receipts_dir,
                exceptions_path=exceptions_dir,
                drills_path=drills_dir,
                schemas_path=schemas_dir,
                max_age_days=args.drill_max_age_days,
            )

        combined = {
            "kind": "das1-conformance-seed",
            "generated_at": _utcnow_iso(),
            "das_version": das_version,
            "receipts_path": str(receipts_dir),
            "exceptions_path": str(exceptions_dir),
            "drills_path": str(drills_dir),
            "tool_catalogs_path": str(tool_catalogs_dir),
            "policy_snapshots_path": str(policy_snapshots_dir),
            "ir_annexes_path": str(ir_annexes_dir),
            "receipts": receipt_report,
            "exceptions": exc_report,
            "drills": drill_report,
            "tool_catalogs": tool_catalog_report,
            "policy_snapshots": policy_snapshot_report,
            "ir_annexes": ir_annex_report,
            "delegation_records": delegation_report,
            "classification_registers": classification_report,
            "overlays": overlay_reports,
            "pass": (
                len(receipt_failures) == 0
                and len(exc_failures) == 0
                and len(drill_failures) == 0
                and len(tool_catalog_failures) == 0
                and len(policy_snapshot_failures) == 0
                and len(ir_annex_failures) == 0
                and len(delegation_failures) == 0
                and len(classification_failures) == 0
                and len(overlay_failures) == 0
            ),
        }

        Path(args.report).write_text(json.dumps(combined, indent=2), encoding="utf-8")
        print(
            json.dumps(
                {
                    "pass": combined["pass"],
                    "receipt_failures": len(receipt_failures),
                    "exception_failures": len(exc_failures),
                    "drill_failures": len(drill_failures),
                    "tool_catalog_failures": len(tool_catalog_failures),
                    "policy_snapshot_failures": len(policy_snapshot_failures),
                    "ir_annex_failures": len(ir_annex_failures),
                    "delegation_record_failures": len(delegation_failures),
                    "classification_register_failures": len(classification_failures),
                    "overlay_failures": len(overlay_failures),
                }
            )
        )
        return 1 if not combined["pass"] else 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
