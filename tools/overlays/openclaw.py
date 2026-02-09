"""OpenClaw overlay checks for DAS-1 verifier.

This plugin is intentionally runtime-specific and separate from core checks.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict, List


def _failure(file: str, message: str, pointer: str = "") -> Dict[str, str]:
    return {
        "kind": "overlay:openclaw",
        "file": file,
        "message": message,
        "pointer": pointer,
    }


REQUIRED_DRILL_ASSERTIONS = {
    "D-OC-01": [
        "proposed_action_recorded",
        "execution_blocked_without_approval",
        "sender_session_provenance_preserved"
    ],
    "D-OC-02": [
        "remote_localhost_inheritance_blocked",
        "unauth_high_risk_execution_blocked",
        "trusted_proxy_evaluation_logged"
    ],
    "D-OC-03": [
        "non_main_session_sandboxed",
        "host_filesystem_traversal_blocked",
        "unauthorized_network_egress_blocked"
    ]
}


def run_overlay_checks(context, load_json_records, parse_iso8601_aware):
    failures: List[Dict[str, str]] = []
    required_overlay_drills = ("D-OC-01", "D-OC-02", "D-OC-03")
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
                    message="OpenClaw drill executed_at must be timezone-aware ISO-8601.",
                    pointer="/executed_at",
                )
            )
            continue

        evidence_refs = obj.get("evidence_refs", [])
        if not isinstance(evidence_refs, list) or len(evidence_refs) < 2:
            failures.append(
                _failure(
                    file=file,
                    message=(
                        f"{drill_id} requires at least two evidence_refs "
                        "for claim-grade verification."
                    ),
                    pointer="/evidence_refs",
                )
            )

        overlay_context = obj.get("overlay_context")
        openclaw_ctx = overlay_context.get("openclaw") if isinstance(overlay_context, dict) else None
        assertions = openclaw_ctx.get("assertions") if isinstance(openclaw_ctx, dict) else None
        if not isinstance(assertions, dict):
            failures.append(
                _failure(
                    file=file,
                    message=f"{drill_id} requires overlay_context.openclaw.assertions object.",
                    pointer="/overlay_context/openclaw/assertions",
                )
            )
            continue

        for assertion_key in REQUIRED_DRILL_ASSERTIONS.get(drill_id, []):
            if assertions.get(assertion_key) is not True:
                failures.append(
                    _failure(
                        file=file,
                        message=(
                            f"{drill_id} assertion '{assertion_key}' must be true "
                            "for claim-grade conformance."
                        ),
                        pointer=f"/overlay_context/openclaw/assertions/{assertion_key}",
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
                    message=f"Missing required passing OpenClaw drill report for {drill_id}.",
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
    for file, obj in receipt_records:
        if not isinstance(obj, dict):
            continue
        if obj.get("risk_class") not in ("R3", "R4") or obj.get("decision") != "allow":
            continue
        inspected += 1
        overlay_context = obj.get("overlay_context")
        if not isinstance(overlay_context, dict):
            failures.append(
                _failure(
                    file=file,
                    message="R3/R4 allow receipt missing overlay_context for OpenClaw provenance checks.",
                    pointer="/overlay_context",
                )
            )
            continue
        openclaw_ctx = overlay_context.get("openclaw")
        if not isinstance(openclaw_ctx, dict):
            failures.append(
                _failure(
                    file=file,
                    message="R3/R4 allow receipt missing overlay_context.openclaw object.",
                    pointer="/overlay_context/openclaw",
                )
            )
            continue

        tagged += 1
        for key in ("channel_id", "sender_id", "session_scope_key"):
            if not openclaw_ctx.get(key):
                failures.append(
                    _failure(
                        file=file,
                        message=f"OpenClaw provenance requires {key} on R3/R4 allow receipts.",
                        pointer=f"/overlay_context/openclaw/{key}",
                    )
                )

    if inspected == 0:
        failures.append(
            _failure(
                file=str(context.receipts_path),
                message=(
                    "No R3/R4 allow receipts found; cannot verify OpenClaw provenance-binding "
                    "requirements for high-risk actions."
                ),
            )
        )

    return {
        "failures": failures,
        "details": {
            "required_overlay_drills": list(required_overlay_drills),
            "latest_overlay_pass": {k: v.isoformat() for k, v in latest_overlay_pass.items()},
            "inspected_r3_r4_allow_receipts": inspected,
            "tagged_openclaw_receipts": tagged,
        },
    }
