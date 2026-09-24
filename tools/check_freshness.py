#!/usr/bin/env python3
"""Report how long the example evidence has left before it ages out.

Why this exists: the conformance gate is time-gated by design. Drill passes
expire after 90 days (AEC-05) and the IR tabletop after 365 (AEC-12). That is
correct behavior, and it is what caught this repository out.

On 2026-06-10 the example drills were executed. On 2026-09-08 that evidence
crossed the 90-day line and every core and overlay job began failing. Nothing
reported it, because `conformance.yml` ran only on push and pull_request and
the last push was 2026-08-22. The gate was red for fifteen days and the
checked-in reports still said `"pass": true`.

A gate that only speaks when someone pushes is not a detector. It is a fact
that happens to be discoverable. This script makes the remaining time a
number anyone can read, and makes CI say so on a schedule while there is
still time to act, rather than at the moment the evidence is already invalid.

It never changes anything. `tools/refresh_example_dates.py` does the fixing.

Usage:
  python3 tools/check_freshness.py                 # warn at 30 days remaining
  python3 tools/check_freshness.py --warn-days 45
  python3 tools/check_freshness.py --quiet          # only print problems

Exit codes:
  0  every artifact has more than --warn-days remaining
  1  something is inside the warning window, or already expired
  2  usage or repository-layout error
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = "das1/examples"

# These mirror the verifier's defaults in tools/das1_verify.py. If they drift
# apart the warning stops meaning anything, so they are named here rather than
# spelled as bare numbers at the call sites.
DRILL_MAX_AGE_DAYS = 90      # das1_verify.py --drill-max-age-days
IR_MAX_AGE_DAYS = 365        # das1_verify.py --ir-max-age-days


def parse_iso(value):
    """Parse an RFC3339/ISO-8601 timestamp, tolerating a trailing Z."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def collect(root):
    """Every date-gated artifact, as (kind, id, path, executed_at, max_age)."""
    found = []
    for dirpath, _, files in os.walk(root):
        for filename in sorted(files):
            if not filename.endswith(".json"):
                continue
            path = os.path.join(dirpath, filename)
            try:
                with open(path, encoding="utf-8") as handle:
                    obj = json.load(handle)
            except (OSError, json.JSONDecodeError):
                # An unreadable fixture is a separate problem and the verifier
                # will say so. Freshness cannot be judged, so skip rather than
                # report a misleading age.
                continue
            if not isinstance(obj, dict):
                continue

            if "drill_id" in obj and "executed_at" in obj:
                found.append(("drill", str(obj["drill_id"]), path,
                              parse_iso(obj["executed_at"]), DRILL_MAX_AGE_DAYS))

            # IR annexes carry the annual AEC-12 tabletop. The verifier reads
            # it from tabletop.last_executed_at (das1_verify.py verify_ir_annexes),
            # so this reads the same field. A checker that looks somewhere else
            # reports "all clear" forever, which is worse than no checker.
            tabletop = obj.get("tabletop")
            if isinstance(tabletop, dict) and "last_executed_at" in tabletop:
                found.append(("ir_annex",
                              str(obj.get("annex_id") or os.path.basename(path)),
                              path, parse_iso(tabletop["last_executed_at"]),
                              IR_MAX_AGE_DAYS))
    return found


def main(argv):
    parser = argparse.ArgumentParser(
        description="Report days remaining before DAS-1 example evidence expires.")
    parser.add_argument("--warn-days", type=int, default=30,
                        help="exit non-zero when anything has fewer days left (default: 30)")
    parser.add_argument("--quiet", action="store_true",
                        help="print only artifacts inside the warning window")
    parser.add_argument("--all", action="store_true",
                        help="list every artifact rather than the most urgent few")
    parser.add_argument("--root", default=ROOT, help="evidence root (default: %s)" % ROOT)
    args = parser.parse_args(argv[1:])

    if not os.path.isdir(args.root):
        sys.stderr.write("ERROR: run from the das-1 repo root (no %s/)\n" % args.root)
        return 2

    now = datetime.now(timezone.utc)
    rows = []
    unparseable = []
    for kind, ident, path, when, max_age in collect(args.root):
        if when is None:
            unparseable.append((kind, ident, path))
            continue
        age_days = (now - when).total_seconds() / 86400.0
        rows.append((max_age - age_days, kind, ident, path, when, max_age))

    if not rows and not unparseable:
        sys.stderr.write("ERROR: no date-gated evidence found under %s/\n" % args.root)
        return 2

    rows.sort(key=lambda r: r[0])
    expired = [r for r in rows if r[0] <= 0]
    warning = [r for r in rows if 0 < r[0] <= args.warn_days]

    # Everything that matters, plus enough context to see the horizon. Printing
    # all 56 rows on every green run is the noise that hides the red one, which
    # is how the 88 dropped writes elsewhere on this machine went unread.
    if args.quiet:
        shown = expired + warning
    elif args.all:
        shown = rows
    else:
        shown = expired + warning
        if not shown:
            shown = rows[:3]

    if shown:
        print("%-9s %-12s %-10s %s" % ("REMAINING", "KIND", "ID", "EXECUTED"))
        for remaining, kind, ident, path, when, max_age in shown:
            if remaining <= 0:
                label = "EXPIRED %d" % int(abs(remaining))
            else:
                label = "%d d" % int(remaining)
            print("%-9s %-12s %-10s %s  (%d-day window)"
                  % (label, kind, ident, when.date().isoformat(), max_age))

    for kind, ident, path in unparseable:
        print("UNREADABLE DATE  %-12s %-10s %s" % (kind, ident, path))

    print("")
    print("checked %d artifact(s): %d expired, %d within %d days, %d ok"
          % (len(rows), len(expired), len(warning), args.warn_days,
             len(rows) - len(expired) - len(warning)))

    if expired or warning or unparseable:
        print("")
        print("Refresh with:  python3 tools/refresh_example_dates.py")
        print("Then regenerate the reports (they cross-check the claims) and")
        print("re-run the verifier. tools/refresh_and_verify.sh does both in order.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
