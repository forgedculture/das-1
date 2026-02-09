#!/usr/bin/env python3
"""DAS-1 conformance helper (seed).

Goal: make DAS-1 claims less subjective and more testable.

This tool:
- Validates receipt events against the canonical DAS-1 receipt schema.
- Validates exception register entries against the canonical exceptions schema.
- Applies a small set of DAS-1 v0.001 checks that are machine-verifiable.

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

    return failures


def verify_drills(path: Path, schema_path: Path, max_age_days: int = 90) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)

    failures: List[Failure] = []
    total = 0
    now_utc = datetime.now(timezone.utc)
    required_drills = ("D1", "D2")
    latest_pass: Dict[str, datetime] = {}

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
        "total_files": total,
        "required_drills": list(required_drills),
        "max_age_days": max_age_days,
        "latest_pass": {k: v.isoformat() for k, v in latest_pass.items()},
        "failures": [f.__dict__ for f in failures],
        "pass": len(failures) == 0,
    }
    return failures, report


def verify_receipts(path: Path, schema_path: Path) -> Tuple[List[Failure], Dict[str, Any]]:
    schema = _load_json(schema_path)

    failures: List[Failure] = []
    total = 0

    for jf in _iter_json_files(path):
        total += 1
        obj = _load_json(jf)
        failures.extend(_validate_against_schema(obj, schema, str(jf), kind="schema"))
        if isinstance(obj, dict):
            failures.extend(_das1_receipt_checks(obj, str(jf)))
        else:
            failures.append(
                Failure(kind="schema", file=str(jf), message="Receipt must be a JSON object.")
            )

    report = {
        "kind": "das1-receipts",
        "generated_at": _utcnow_iso(),
        "path": str(path),
        "total_files": total,
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
    p_verify.add_argument("--schemas", type=str, default="schemas", help="schemas directory")
    p_verify.add_argument("--drill-max-age-days", type=int, default=90, help="max age for required D1/D2 passes")
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

    p_o = sub.add_parser("verify-overlay", help="verify core plus overlay plugin checks")
    p_o.add_argument("--receipts", type=str, required=True, help="path to receipts directory")
    p_o.add_argument("--exceptions", type=str, required=True, help="path to exceptions directory")
    p_o.add_argument("--drills", type=str, required=True, help="path to drills directory")
    p_o.add_argument("--schemas", type=str, default="schemas", help="schemas directory")
    p_o.add_argument("--drill-max-age-days", type=int, default=90, help="max age for required D1/D2 passes")
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

    if args.cmd in ("verify", "verify-overlay"):
        receipts_dir = Path(args.receipts)
        exceptions_dir = Path(args.exceptions)
        drills_dir = Path(args.drills)
        schemas_dir = Path(args.schemas)
        overlay_dir = Path(args.overlay_dir)
        overlays = args.overlay or []

        receipt_failures, receipt_report = verify_receipts(receipts_dir, schemas_dir / "receipt.schema.json")
        exc_failures, exc_report = verify_exceptions(exceptions_dir, schemas_dir / "exception.schema.json")
        drill_failures, drill_report = verify_drills(
            drills_dir, schemas_dir / "drill-report.schema.json", max_age_days=args.drill_max_age_days
        )
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
            "receipts_path": str(receipts_dir),
            "exceptions_path": str(exceptions_dir),
            "drills_path": str(drills_dir),
            "receipts": receipt_report,
            "exceptions": exc_report,
            "drills": drill_report,
            "overlays": overlay_reports,
            "pass": (
                len(receipt_failures) == 0
                and len(exc_failures) == 0
                and len(drill_failures) == 0
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
                    "overlay_failures": len(overlay_failures),
                }
            )
        )
        return 1 if not combined["pass"] else 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
