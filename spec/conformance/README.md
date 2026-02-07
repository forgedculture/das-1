# DAS-1 conformance tooling (seed)

This directory provides the smallest executable core needed to make DAS-1 claims testable.

## What you get

- Canonical schemas
  - schemas/receipt.schema.json
  - schemas/exception.schema.json
- A minimal conformance runner
  - tools/das1_verify.py

## Quickstart

- Validate example receipt packs

  python tools/das1_verify.py verify-receipts das1/examples/receipt_packs

- Validate example exception entries

  python tools/das1_verify.py verify-exceptions das1/examples/exceptions

- Validate both and write a report

  python tools/das1_verify.py verify \
    --receipts das1/examples/receipt_packs \
    --exceptions das1/examples/exceptions \
    --report conformance-report.json

## Checks implemented (v0.001)

- Schema validation (receipt + exception)
- R3/R4 allow receipts MUST include:
  - approval_id, approver_id (AEC-03)
  - preflight_id (AEC-06)
- Allow receipts SHOULD have:
  - inputs_present=true and outputs_present=true (AEC-07)
- Cost-incurring receipts require owner/cost-center attribution tags (AEC-10)
- Exceptions with `status` in `proposed|approved|active` must be unexpired; `expired` entries remain valid historical evidence (AEC-11)

## What this does not cover

Many controls require external artifacts (catalog exports, policy snapshots, drill scorecards). The runner can be extended to ingest those artifacts, but the baseline goal is to make receipts and exceptions machine-verifiable first.
