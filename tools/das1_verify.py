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
import json
import os
import sys
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

    # AEC-10: cost attribution tags for cost-incurring tools (if cost_incurred=true).
    if receipt.get("cost_incurred") is True:
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
    # We can at least ensure expires_at is in the future at time of validation.
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
                if dt <= datetime.now(dt.tzinfo):
                    failures.append(
                        Failure(
                            kind="das1",
                            file=file,
                            message="Exception is expired (AEC-11).",
                            pointer="/expires_at",
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


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="das1", description="DAS-1 conformance helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_verify = sub.add_parser("verify", help="verify receipts and exceptions")
    p_verify.add_argument("--receipts", type=str, required=True, help="path to receipts directory")
    p_verify.add_argument("--exceptions", type=str, required=True, help="path to exceptions directory")
    p_verify.add_argument("--schemas", type=str, default="schemas", help="schemas directory")
    p_verify.add_argument("--report", type=str, default="conformance-report.json", help="output report path")

    p_r = sub.add_parser("verify-receipts", help="verify receipts")
    p_r.add_argument("path", type=str)
    p_r.add_argument("--schema", type=str, default="schemas/receipt.schema.json")
    p_r.add_argument("--report", type=str, default="receipt-report.json")

    p_e = sub.add_parser("verify-exceptions", help="verify exceptions")
    p_e.add_argument("path", type=str)
    p_e.add_argument("--schema", type=str, default="schemas/exception.schema.json")
    p_e.add_argument("--report", type=str, default="exceptions-report.json")

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

    if args.cmd == "verify":
        receipts_dir = Path(args.receipts)
        exceptions_dir = Path(args.exceptions)
        schemas_dir = Path(args.schemas)

        receipt_failures, receipt_report = verify_receipts(receipts_dir, schemas_dir / "receipt.schema.json")
        exc_failures, exc_report = verify_exceptions(exceptions_dir, schemas_dir / "exception.schema.json")

        combined = {
            "kind": "das1-conformance-seed",
            "generated_at": _utcnow_iso(),
            "receipts_path": str(receipts_dir),
            "exceptions_path": str(exceptions_dir),
            "receipts": receipt_report,
            "exceptions": exc_report,
            "pass": (len(receipt_failures) == 0 and len(exc_failures) == 0),
        }

        Path(args.report).write_text(json.dumps(combined, indent=2), encoding="utf-8")
        print(json.dumps({"pass": combined["pass"], "receipt_failures": len(receipt_failures), "exception_failures": len(exc_failures)}))
        return 1 if not combined["pass"] else 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
