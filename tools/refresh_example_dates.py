#!/usr/bin/env python3
"""Refresh the date-gated fields in the DAS-1 example evidence to a recent
campaign date, so the example suite keeps passing the verifier's freshness
rules (drills must be within 90 days, AEC-05 / AEC-12).

Why this exists: the example receipts/drills/claims are static fixtures. The
verifier checks drill `executed_at` against "now", so over wall-clock time the
fixtures age out of the 90-day window and the conformance gate goes red even
though nothing about the standard changed. Run this before a release (or on a
schedule) to re-date the fixtures.

It only touches freshness-sensitive fields:
  - drill files:  executed_at
  - claim files:  generated_at, attestation.attested_at,
                  disclosures.last_required_drill_pass_at.*

It deliberately does NOT touch exception `expires_at` (must stay in the future),
receipt timestamps, tool-catalog `generated_at`, or IR annex dates.

Usage:
  python3 tools/refresh_example_dates.py [YYYY-MM-DD]   # default: today (UTC) - 4 days
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

ROOT = "das1/examples"


def target_date(argv):
    if len(argv) > 1:
        # validate
        datetime.strptime(argv[1], "%Y-%m-%d")
        return argv[1]
    return (datetime.now(timezone.utc) - timedelta(days=4)).strftime("%Y-%m-%d")


def redate(value, target):
    """Replace the date part of an ISO-8601 'YYYY-MM-DDThh:mm:ssZ' string,
    preserving the time-of-day. Leaves non-matching values untouched."""
    if not isinstance(value, str) or "T" not in value:
        return value
    _, _, rest = value.partition("T")
    return f"{target}T{rest}"


def main(argv):
    target = target_date(argv)
    if not os.path.isdir(ROOT):
        sys.exit(f"ERROR: run from the das-1 repo root (no {ROOT}/)")
    changed = []
    for dirpath, _, files in os.walk(ROOT):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                obj = json.load(open(path, encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(obj, dict):
                continue
            before = json.dumps(obj, sort_keys=True)

            if "drill_id" in obj and "executed_at" in obj:
                obj["executed_at"] = redate(obj["executed_at"], target)

            if "claim_id" in obj:
                if "generated_at" in obj:
                    obj["generated_at"] = redate(obj["generated_at"], target)
                disc = obj.get("disclosures", {})
                lr = disc.get("last_required_drill_pass_at", {})
                if isinstance(lr, dict):
                    for k in list(lr):
                        lr[k] = redate(lr[k], target)
                att = obj.get("attestation", {})
                if isinstance(att, dict) and "attested_at" in att:
                    att["attested_at"] = redate(att["attested_at"], target)

            if json.dumps(obj, sort_keys=True) != before:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(obj, f, indent=2, ensure_ascii=True)
                    f.write("\n")
                changed.append(path)

    print(f"Refreshed {len(changed)} example file(s) to {target}:")
    for c in changed:
        print("  " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
