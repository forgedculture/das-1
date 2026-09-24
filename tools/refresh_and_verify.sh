#!/usr/bin/env bash
# Refresh the date-gated example evidence and prove it verifies, in the one
# order that works.
#
# Why this is a script and not two commands in a README: refreshing the
# fixtures alone leaves the repository in a state that FAILS verification.
# The conformance claims cross-check their disclosed drill dates against the
# generated *-report.json files, so re-dating drills and claims without
# regenerating the reports makes `verify-claims` fail with sixteen
# "Disclosure for D1 does not match referenced report" errors. Observed
# 2026-09-23: before the refresh the claims passed because claims and reports
# were consistently stale; after it they disagreed.
#
# The order below is the contract:
#   1. refresh fixtures
#   2. regenerate every report (they are verifier OUTPUT, not source)
#   3. verify claims, which read those reports
#   4. report remaining runway so the next expiry is not a surprise
#
# Requires: python3 with jsonschema (python3 -m pip install -r tools/requirements.txt)

set -euo pipefail

cd "$(dirname "$0")/.."

PY="${PYTHON:-python3}"
COMMON=(
  --exceptions das1/examples/exceptions
  --tool-catalogs das1/examples/tool_catalogs
  --policy-snapshots das1/examples/policy_snapshots
  --ir-annexes das1/examples/ir_annexes
)

echo "==> 1/4 refreshing fixtures"
"$PY" tools/refresh_example_dates.py "$@"

echo "==> 2/4 regenerating reports"
"$PY" tools/das1_verify.py verify \
  --receipts das1/examples/receipt_packs \
  --drills das1/examples/drills \
  "${COMMON[@]}" \
  --report conformance-report.json

for overlay in openclaw claude-code codex cursor kiro; do
  "$PY" tools/das1_verify.py verify-overlay \
    --receipts "das1/examples/${overlay}/receipt_packs" \
    --drills "das1/examples/${overlay}/drills" \
    "${COMMON[@]}" \
    --overlay "${overlay}" \
    --report "${overlay}-overlay-report.json"
done

"$PY" tools/das1_verify.py verify \
  --das-version v0.003 \
  --receipts das1/examples/v0003/receipt_packs \
  --drills das1/examples/v0003/drills \
  --exceptions das1/examples/exceptions \
  --tool-catalogs das1/examples/v0003/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --delegation-records das1/examples/v0003/delegation_records \
  --classification-registers das1/examples/v0003/classification_registers \
  --report conformance-v0003-report.json

echo "==> 3/4 verifying claim packets against the regenerated reports"
"$PY" tools/das1_verify.py verify-claims das1/examples/claims --report claims-report.json

echo "==> 4/4 remaining runway"
"$PY" tools/check_freshness.py

echo
echo "Green. Reports regenerated; review the diff before committing."
