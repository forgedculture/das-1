# DAS-1 conformance tooling (seed)

This directory provides the smallest executable core needed to make DAS-1 claims testable.

## What you get

- Canonical schemas
  - schemas/receipt.schema.json
  - schemas/exception.schema.json
  - schemas/drill-report.schema.json
  - schemas/conformance-claim.schema.json
  - schemas/tool-catalog.schema.json
  - schemas/policy-snapshot.schema.json
  - schemas/ir-annex.schema.json
  - schemas/delegation-record.schema.json (v0.003, AEC-13)
  - schemas/classification-register.schema.json (v0.003, AEC-14)
- A minimal conformance runner
  - tools/das1_verify.py
  - tools/overlays/README.md (plugin contract for overlay-specific checks)
  - tools/test_v0003_checks.py (negative tests proving the v0.003 checks fire)

## Version selection

The runner defaults to v0.002. Pass `--das-version v0.003` to additionally apply the
v0.003 controls. v0.002 evidence keeps passing under v0.002 unchanged, which is what
the standard promises existing claimants.

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
    --tool-catalogs das1/examples/tool_catalogs \
    --policy-snapshots das1/examples/policy_snapshots \
    --ir-annexes das1/examples/ir_annexes \
    --report conformance-report.json

- Validate drill reports only

  python tools/das1_verify.py verify-drills das1/examples/drills

- Validate core + OpenClaw overlay checks

  python tools/das1_verify.py verify-overlay \
    --receipts das1/examples/openclaw/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/openclaw/drills \
    --tool-catalogs das1/examples/tool_catalogs \
    --policy-snapshots das1/examples/policy_snapshots \
    --ir-annexes das1/examples/ir_annexes \
    --overlay openclaw \
    --report openclaw-overlay-report.json

- Validate core + Claude Code overlay checks

  python tools/das1_verify.py verify-overlay \
    --receipts das1/examples/claude-code/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/claude-code/drills \
    --tool-catalogs das1/examples/tool_catalogs \
    --policy-snapshots das1/examples/policy_snapshots \
    --ir-annexes das1/examples/ir_annexes \
    --overlay claude-code \
    --report claude-code-overlay-report.json

- Validate core + Codex overlay checks

  python tools/das1_verify.py verify-overlay \
    --receipts das1/examples/codex/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/codex/drills \
    --tool-catalogs das1/examples/tool_catalogs \
    --policy-snapshots das1/examples/policy_snapshots \
    --ir-annexes das1/examples/ir_annexes \
    --overlay codex \
    --report codex-overlay-report.json

- Validate the v0.003 draft evidence pack (AEC-13, AEC-14, Annex A, tightened AEC-10)

  python tools/das1_verify.py verify \
    --das-version v0.003 \
    --receipts das1/examples/v0003/receipt_packs \
    --exceptions das1/examples/exceptions \
    --drills das1/examples/v0003/drills \
    --tool-catalogs das1/examples/v0003/tool_catalogs \
    --policy-snapshots das1/examples/policy_snapshots \
    --ir-annexes das1/examples/ir_annexes \
    --delegation-records das1/examples/v0003/delegation_records \
    --classification-registers das1/examples/v0003/classification_registers \
    --report conformance-v0003-report.json

- Validate the v0.003 artifact families individually

  python tools/das1_verify.py verify-delegation-records das1/examples/v0003/delegation_records
  python tools/das1_verify.py verify-classification-registers das1/examples/v0003/classification_registers

- Prove the v0.003 checks actually fire

  python tools/test_v0003_checks.py

- Validate conformance claim packets

  python tools/das1_verify.py verify-claims das1/examples/claims
  # optional: --report claims-report.json

- Validate core artifact families individually

  python tools/das1_verify.py verify-tool-catalogs das1/examples/tool_catalogs
  python tools/das1_verify.py verify-policy-snapshots das1/examples/policy_snapshots
  python tools/das1_verify.py verify-ir-annexes das1/examples/ir_annexes

## Checks implemented (v0.002)

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
- Claim packets can be validated against referenced conformance reports and required disclosure fields
- Tool catalogs, policy snapshots, and IR annexes are schema-validated and checked for core AEC evidence quality (AEC-01/02/04/12)

## Checks implemented (v0.003 draft, additive)

Applied only with `--das-version v0.003`.

- AEC-13 delegation records
  - The subset rule on every axis: tools, actions, data classes, risk ceiling, autonomy level
  - Every delegation has an expiry, and an active delegation has not already lapsed
  - `parent_delegation_id` resolves, lineage contains no cycles, depth is consistent
  - Cascade integrity: no delegation stays active under a revoked ancestor, checked to the root
- AEC-13 receipts
  - Delegated actions carry delegation_id, parent_actor_id, root_principal_id, granted_risk_ceiling
  - An action's own class may not exceed the risk ceiling it was granted
- AEC-14 classification registers
  - `ambiguity_default` must be `higher_class`; a stated lower default is a failure
  - All four reclassification triggers present (tool, scope, data class, blast radius)
  - At least one composition test case
  - Composition rules: members resolve, the declared individual max matches the member entries,
    the composed class is never below it, and the sequence is governed at the composed class
- AEC-14 receipts
  - A receipt in a sequence governed at R3/R4 requires approval and preflight even when the
    action's own class is R1/R2. This is the composition hole closing.
- AEC-10 receipts and D4
  - `cap_enforcement_point=reporting_layer` fails; the cap must be in the execution path
  - `cap_enforced=true` requires a cap_id and a blocked or queued execution status
- Annex A
  - A0-A3 may not record an executed R3/R4 action
  - Every tool catalog entry carries both risk_ceiling and autonomy_level
- Drills
  - D1-D4 all required within 90 days
  - D3 pass requires cascade_complete, lineage_reconstructed, zero descendant executions after
    revoke, and completion within the AEC-05 budget
  - D4 pass requires execution-path enforcement, a halted execution, and a notified cap owner
- Claims
  - A packet declaring `das_version: v0.003` requires D1-D4 disclosures and passing
    delegation_records and classification_registers sections in its referenced report

## Overlay extensions

- Core verifier is runtime-agnostic by default.
- Overlay-specific checks are loaded from `tools/overlays/<overlay_id>.py`.
- Overlay evidence can use namespaced `overlay_context` in receipt/drill artifacts without changing core control semantics.
- Platform overlays currently include `openclaw`, `claude-code`, `codex`, `cursor`, and `kiro`.
- Domain overlays under `overlays/domain/` are high-impact operating-context examples; they do not replace legal, regulatory, policy, or mission-specific compliance review.

## What this does not cover

Many controls require external artifacts (catalog exports, policy snapshots, drill scorecards). The runner can be extended to ingest those artifacts, but the baseline goal is to make receipts and exceptions machine-verifiable first.
