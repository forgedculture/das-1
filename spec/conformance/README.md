# DAS-1 conformance tooling (seed)

This directory provides the smallest executable core needed to make DAS-1 claims testable.

## What you get

- Canonical schemas
  - schemas/receipt.schema.json
  - schemas/exception.schema.json
  - schemas/drill-report.schema.json
- A minimal conformance runner
  - tools/das1_verify.py
  - tools/overlays/README.md (plugin contract for overlay-specific checks)

## Quickstart

- Validate example receipt packs

  python tools/das1_verify.py verify-receipts das1/examples/receipt_packs

- Validate example exception entries

  python tools/das1_verify.py verify-exceptions das1/examples/exceptions

- Validate both and write a report

  python tools/das1_verify.py verify \
    --receipts das1/examples/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/drills \
    --report conformance-report.json

- Validate drill reports only

  python tools/das1_verify.py verify-drills das1/examples/drills

- Validate core + OpenClaw overlay checks

  python tools/das1_verify.py verify-overlay \
    --receipts das1/examples/openclaw/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/openclaw/drills \
    --overlay openclaw \
    --report openclaw-overlay-report.json

## Checks implemented (v0.001)

- Schema validation (receipt + exception + drill)
- R3/R4 allow receipts MUST include:
  - approval_id, approver_id (AEC-03)
  - preflight_id (AEC-06)
- Allow receipts SHOULD have:
  - inputs_present=true and outputs_present=true (AEC-07)
- Cost-incurring receipts require owner/cost-center attribution tags (AEC-10)
- Exceptions with `status` in `proposed|approved|active` must be unexpired; `expired` entries remain valid historical evidence (AEC-11)
- Required drills D1 and D2 must have a passing execution within the last 90 days
- Receipt reports include utility-oriented summaries for R1/R2 autonomy, execution latency, and blocked rates when optional fields are present (M5-M7 support)
- Measurability gaps for M6/M7 are surfaced as failures when relevant receipt fields are missing

## Overlay extensions

- Core verifier is runtime-agnostic by default.
- Overlay-specific checks are loaded from `tools/overlays/<overlay_id>.py`.
- Overlay evidence can use namespaced `overlay_context` in receipt/drill artifacts without changing core control semantics.

## What this does not cover

Many controls require external artifacts (catalog exports, policy snapshots, drill scorecards). The runner can be extended to ingest those artifacts, but the baseline goal is to make receipts and exceptions machine-verifiable first.
