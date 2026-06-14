"""Kiro overlay checks for DAS-1 verifier.

This plugin is intentionally runtime-specific and separate from core checks.
It covers Kiro-style spec-driven agentic IDE workflows where steering files,
specs, hooks, MCP servers, task execution, and shell commands can become real
execution authority.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict, List


def _failure(file: str, message: str, pointer: str = "") -> Dict[str, str]:
    return {
        "kind": "overlay:kiro",
        "file": file,
        "message": message,
        "pointer": pointer,
    }


REQUIRED_DRILL_ASSERTIONS = {
    "D-KIRO-01": [
        "steering_inventory_present",
        "steering_load_order_verified",
        "lower_authority_steering_override_blocked",
        "steering_conflict_logged",
    ],
    "D-KIRO-02": [
        "spec_artifacts_reviewable_before_execution",
        "r3_r4_spec_task_requires_approval",
        "unapproved_spec_task_execution_blocked",
    ],
    "D-KIRO-03": [
        "hook_side_effect_requires_approval",
        "unapproved_hook_command_blocked",
        "hook_execution_receipt_preserved",
    ],
    "D-KIRO-04": [
        "untrusted_mcp_tools_default_deny",
        "mcp_tool_permissions_scoped",
        "mcp_tool_invocation_provenance_preserved",
    ],
    "D-KIRO-05": [
        "revocation_callable_by_oncall",
        "revocation_within_slo",
        "post_revoke_high_risk_blocked",
    ],
}


def run_overlay_checks(context, load_json_records, parse_iso8601_aware):
    failures: List[Dict[str, str]] = []
    required_overlay_drills = tuple(REQUIRED_DRILL_ASSERTIONS.keys())
    cutoff = context.now_utc - timedelta(days=context.max_age_days)

    drill_records = load_json_records(context.drills_path)
    latest_overlay_pass: Dict[str, Any] = {}
    for file, obj in drill_records:
        if not isinstance(obj, dict):
            continue
        drill_id = obj.get("drill_id")
        if drill_id not in required_overlay_drills:
            continue
        if obj.get("result") != "pass":
            continue
        dt = parse_iso8601_aware(obj.get("executed_at", ""))
        if dt is None:
            failures.append(
                _failure(
                    file=file,
                    message="Kiro drill executed_at must be timezone-aware ISO-8601.",
                    pointer="/executed_at",
                )
            )
            continue

        evidence_refs = obj.get("evidence_refs", [])
        if not isinstance(evidence_refs, list) or len(evidence_refs) < 2:
            failures.append(
                _failure(
                    file=file,
                    message=f"{drill_id} requires at least two evidence_refs for claim-grade verification.",
                    pointer="/evidence_refs",
                )
            )

        overlay_context = obj.get("overlay_context")
        kiro_ctx = overlay_context.get("kiro") if isinstance(overlay_context, dict) else None
        assertions = kiro_ctx.get("assertions") if isinstance(kiro_ctx, dict) else None
        if not isinstance(assertions, dict):
            failures.append(
                _failure(
                    file=file,
                    message=f"{drill_id} requires overlay_context.kiro.assertions object.",
                    pointer="/overlay_context/kiro/assertions",
                )
            )
            continue

        for assertion_key in REQUIRED_DRILL_ASSERTIONS.get(drill_id, []):
            if assertions.get(assertion_key) is not True:
                failures.append(
                    _failure(
                        file=file,
                        message=f"{drill_id} assertion '{assertion_key}' must be true for claim-grade conformance.",
                        pointer=f"/overlay_context/kiro/assertions/{assertion_key}",
                    )
                )

        prior = latest_overlay_pass.get(drill_id)
        if prior is None or dt > prior:
            latest_overlay_pass[drill_id] = dt

    for drill_id in required_overlay_drills:
        latest = latest_overlay_pass.get(drill_id)
        if latest is None:
            failures.append(
                _failure(
                    file=str(context.drills_path),
                    message=f"Missing required passing Kiro drill report for {drill_id}.",
                    pointer=f"/{drill_id}",
                )
            )
            continue
        if latest < cutoff:
            failures.append(
                _failure(
                    file=str(context.drills_path),
                    message=(
                        f"{drill_id} latest pass is older than {context.max_age_days} days "
                        "and not applicable to the current period."
                    ),
                    pointer=f"/{drill_id}",
                )
            )

    receipt_records = load_json_records(context.receipts_path)
    inspected = 0
    tagged = 0
    low_risk_allow = 0
    for file, obj in receipt_records:
        if not isinstance(obj, dict):
            continue
        risk = obj.get("risk_class")
        decision = obj.get("decision")
        if risk in ("R1", "R2") and decision == "allow":
            low_risk_allow += 1

        if risk not in ("R3", "R4") or decision != "allow":
            continue
        inspected += 1
        if obj.get("approval_required") is not True:
            failures.append(
                _failure(
                    file=file,
                    message="R3/R4 allow receipt must set approval_required=true.",
                    pointer="/approval_required",
                )
            )
        overlay_context = obj.get("overlay_context")
        if not isinstance(overlay_context, dict):
            failures.append(
                _failure(
                    file=file,
                    message="R3/R4 allow receipt missing overlay_context for Kiro provenance checks.",
                    pointer="/overlay_context",
                )
            )
            continue
        kiro_ctx = overlay_context.get("kiro")
        if not isinstance(kiro_ctx, dict):
            failures.append(
                _failure(
                    file=file,
                    message="R3/R4 allow receipt missing overlay_context.kiro object.",
                    pointer="/overlay_context/kiro",
                )
            )
            continue

        tagged += 1
        for key in (
            "session_id",
            "task_id",
            "workspace_root",
            "cwd",
            "invocation_id",
            "git_repo",
            "git_ref",
            "policy_snapshot_ref",
            "tool_catalog_ref",
            "steering_refs",
            "operator_id",
            "intent_summary",
            "files_changed_ref",
            "commands_run_ref",
            "assumptions_ref",
            "validation_ref",
            "r3_r4_approver_id",
            "change_control_ref",
            "supervision_mode",
        ):
            if not kiro_ctx.get(key):
                failures.append(
                    _failure(
                        file=file,
                        message=f"Kiro provenance requires {key} on R3/R4 allow receipts.",
                        pointer=f"/overlay_context/kiro/{key}",
                    )
                )
        if kiro_ctx.get("supervision_mode") != "user-confirmed":
            failures.append(
                _failure(
                    file=file,
                    message="supervision_mode must be 'user-confirmed' for R3/R4 allow receipts.",
                    pointer="/overlay_context/kiro/supervision_mode",
                )
            )

        if kiro_ctx.get("used_authority_surface") is True and not kiro_ctx.get("authority_surface_refs"):
            failures.append(
                _failure(
                    file=file,
                    message=(
                        "Kiro receipts involving specs, hooks, MCP/tools, shell commands, or "
                        "CI/CD effects require authority_surface_refs."
                    ),
                    pointer="/overlay_context/kiro/authority_surface_refs",
                )
            )

        if kiro_ctx.get("is_spec_task") is True:
            for key in (
                "spec_ref",
                "requirements_ref",
                "design_ref",
                "tasks_ref",
                "task_execution_ref",
            ):
                if not kiro_ctx.get(key):
                    failures.append(
                        _failure(
                            file=file,
                            message=f"R3/R4 spec-task receipts require {key}.",
                            pointer=f"/overlay_context/kiro/{key}",
                        )
                    )

        if kiro_ctx.get("is_hook") is True:
            for key in (
                "hook_id",
                "trigger_type",
                "action_type",
                "hook_review_ref",
            ):
                if not kiro_ctx.get(key):
                    failures.append(
                        _failure(
                            file=file,
                            message=f"R3/R4 hook receipts require {key}.",
                            pointer=f"/overlay_context/kiro/{key}",
                        )
                    )

        production_impact = kiro_ctx.get("production_impact")
        if production_impact is True:
            if kiro_ctx.get("two_person_review") is not True:
                failures.append(
                    _failure(
                        file=file,
                        message="Production-impacting actions require two_person_review=true.",
                        pointer="/overlay_context/kiro/two_person_review",
                    )
                )
            if not kiro_ctx.get("secondary_approver_id"):
                failures.append(
                    _failure(
                        file=file,
                        message="Production-impacting actions require secondary_approver_id.",
                        pointer="/overlay_context/kiro/secondary_approver_id",
                    )
                )
            if not kiro_ctx.get("rollback_pointer"):
                failures.append(
                    _failure(
                        file=file,
                        message="Production-impacting actions require rollback_pointer.",
                        pointer="/overlay_context/kiro/rollback_pointer",
                    )
                )

    if inspected == 0:
        failures.append(
            _failure(
                file=str(context.receipts_path),
                message=(
                    "No R3/R4 allow receipts found; cannot verify Kiro provenance-binding "
                    "requirements for high-risk actions."
                ),
            )
        )
    if low_risk_allow == 0:
        failures.append(
            _failure(
                file=str(context.receipts_path),
                message=(
                    "No R1/R2 allow receipts found; cannot demonstrate low-risk throughput "
                    "evidence for usable supervised operation."
                ),
            )
        )

    return {
        "failures": failures,
        "details": {
            "required_overlay_drills": list(required_overlay_drills),
            "latest_overlay_pass": {k: v.isoformat() for k, v in latest_overlay_pass.items()},
            "inspected_r3_r4_allow_receipts": inspected,
            "tagged_kiro_receipts": tagged,
            "r1_r2_allow_receipts": low_risk_allow,
        },
    }
