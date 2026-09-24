# Psyche Overlay Conformance (DAS-1(TM) v0.002) (Normative)

Status: Draft
Date: 2026-09-23

## 1. Scope

This document defines auditable requirements for claiming:

- `DAS-1(TM) v0.002 Conformant + psyche`

This overlay claim is additive to core conformance and does not modify DAS-1 core requirements.

The Psyche runtime does not currently qualify for this claim. Section 8 records its assessed status against every core control as of the date above. This document is published as the mapping and the hardening target, not as a claim.

## 2. Prerequisite

- A valid passing core conformance report MUST exist for the same evidence window.

## 3. Required overlay evidence

- Psyche overlay drills D-PSY-01 through D-PSY-10 MUST each have a passing report within the current conformance window.
- Each D-PSY drill report MUST include at least two evidence references.
- For each D-PSY drill report, `overlay_context.psyche.assertions` MUST include the required assertions and each MUST be `true`.

Required assertions:

- D-PSY-01
  - `authoritative_gate_enforced`
  - `non_allow_decision_did_not_execute`
  - `gate_decision_logged`
- D-PSY-02
  - `approval_is_not_execution_grant`
  - `continuation_replays_proposal_through_authorization`
  - `recheck_decision_governs_execution`
- D-PSY-03
  - `approval_proposal_scope_match_verified`
  - `edited_proposal_packet_rejected`
  - `continuation_key_replay_blocked`
  - `denied_or_revoked_record_not_continuable`
- D-PSY-04
  - `artifact_root_declared`
  - `path_traversal_escape_blocked`
  - `symlink_escape_blocked`
  - `absolute_path_escape_blocked`
- D-PSY-05
  - `advisory_non_authoritative`
  - `advisory_disagreement_recorded`
  - `advisory_failure_recorded`
  - `authoritative_decision_unchanged`
- D-PSY-06
  - `risk_ceiling_enforced_in_execution_path`
  - `above_ceiling_request_refused`
  - `human_approval_cannot_raise_ceiling`
- D-PSY-07
  - `revocation_callable_by_operator`
  - `revoked_proposal_not_continuable`
  - `post_revocation_request_blocked`
- D-PSY-08
  - `operator_identity_resolved_at_runtime`
  - `distinct_operators_distinctly_recorded`
  - `no_build_time_constant_identity`
- D-PSY-09
  - `stored_verification_matches_recomputation`
  - `edited_packet_detected`
  - `no_partial_status_from_empty_evidence`
- D-PSY-10
  - `governed_invocation_path_inventoried`
  - `no_undeclared_authority_grant`
  - `delegation_record_present_when_delegation_exists`

## 4. Required receipt provenance bindings

For governed allow receipts in Psyche-covered scope:

- `overlay_context.psyche.trace_id` MUST be present.
- `overlay_context.psyche.receipt_key` MUST be present.
- `overlay_context.psyche.capability` MUST be present.
- `overlay_context.psyche.authorization_decision` MUST be present.
- `overlay_context.psyche.operator_id` MUST be present and MUST identify a principal resolved at runtime.
- `overlay_context.psyche.risk_ceiling` MUST be present and MUST NOT exceed the ceiling registered in the AEC-01 tool catalog entry.
- `overlay_context.psyche.autonomy_level` MUST be present and MUST match the level registered in the AEC-01 tool catalog entry.
- `overlay_context.psyche.artifact_root` MUST be present.
- `overlay_context.psyche.evidence_packet_ref` MUST be present.

For receipts produced by an approved continuation:

- `overlay_context.psyche.approval_ref` MUST be present.
- `overlay_context.psyche.proposal_ref` MUST be present.
- `overlay_context.psyche.source_trace_id` MUST be present.
- `overlay_context.psyche.source_receipt_key` MUST be present.
- `overlay_context.psyche.recheck_decision` MUST be present, and MUST be the decision returned by the continuation's own authorization pass rather than the decision recorded on the original proposal.

For receipts where a model-backed advisor ran:

- `overlay_context.psyche.advisory.status` MUST be present.
- `overlay_context.psyche.advisory.authoritative_decision` MUST be present.
- `overlay_context.psyche.advisory.advisory_decision` and `overlay_context.psyche.advisory.agreement` MUST be present when the advisor returned a decision.
- `overlay_context.psyche.advisory.authoritative` MUST NOT be `true`. An advisory path that is authoritative is not an advisory path.

Operational usability evidence requirement:

- At least one `R1` or `R2` allow receipt MUST exist in the conformance evidence window, to demonstrate that governed low-risk work executes.
- At least one receipt with `execution_status` other than `executed` MUST exist in the conformance evidence window, to demonstrate that the gate refuses.

Policy posture requirements:

- Execution MUST follow only an `allow` or `allow_with_safeguards` authorization decision.
- A stored human approval MUST NOT execute anything by itself, and MUST NOT convert a refusal into an execution.
- A model-backed authorization advisor MUST remain non-authoritative, and its promotion to load-bearing MUST be a separately approved decision rather than a configuration change.
- The governed capability set MUST be closed and enumerated, and its registered risk ceiling and autonomy level MUST both appear in the AEC-01 tool catalog entry.
- Retention MUST be defined for the local receipt, proposal, approval, and evidence stores.

## 5. Claim validation

- Overlay claims SHOULD be validated using:
  - `python tools/das1_verify.py verify-overlay ... --overlay psyche`
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## 6. Failure conditions

A Psyche overlay claim MUST be considered invalid if any of the following apply:

- Core conformance report fails.
- Any required D-PSY drill is missing, stale, or failing.
- Any required D-PSY assertion is missing or false.
- Required governed-receipt provenance fields are missing.
- `operator_id` is a build-time constant rather than a runtime-resolved principal.
- A receipt shows execution under a decision other than `allow` or `allow_with_safeguards`.
- A continuation receipt reports the original proposal's decision as its re-check decision.
- An advisory path is recorded as authoritative.
- The receipt's declared risk ceiling or autonomy level does not match the registered tool catalog entry.

## 7. Runtime identifier crosswalk (Normative)

The Psyche runtime computes a conformance status from runtime facts using seven locally defined identifiers. Those identifiers are not DAS-1 control numbers and MUST NOT be presented as such. This section binds each one to the control or controls it actually evidences. Where an identifier spans two controls, or evidences only part of one, that is stated rather than forced into a one-to-one mapping.

Source references are to the Psyche repository at `kernel/psyche-kernel/src/`.

| Runtime identifier | Source | Controls evidenced | Strength | What it does not evidence |
|---|---|---|---|---|
| `das1_action_proposed` | `evidence.rs:421-431` | AEC-06, AEC-07 | Partial for both | The proposal packet is written only when authorization escalates (`executor.rs:293-338`), so no preflight exists for the non-escalated majority. The packet carries intent, payload, and rollback class but no declared blast radius and no containment or rollback plan (`executor.rs:145-166`). The identifier can also reach "partial" from a conversation turn existing (`evidence.rs:411-412`, `evidence.rs:423-429`), which is not a preflight artifact. On its own it evidences no complete control. |
| `das1_policy_evaluated` | `evidence.rs:433-441` | AEC-07 primarily; AEC-03 partially; AEC-14 partially (v0.003) | Substantial for AEC-07, partial otherwise | Each receipt carries the authorization decision (`executor.rs:136`), so a decision demonstrably preceded every receipt. It does not evidence a policy snapshot reference or policy version on the receipt, the AEC-08 data-class rules, or AEC-14's requirement that a named owner classify on stated evidence. |
| `das1_human_decision` | `evidence.rs:443-465` | AEC-03 partially; AECX-066 substantially | Partial for AEC-03 | The approval-to-proposal scope match, the fresh-key requirement, and the replay block are real (`executor.rs:433-447`, `executor.rs:658-679`). Attributability fails: the operator identity is a compile-time constant (`frontend/src-tauri/src/main.rs:11`, used at `:65` and `:78`). The AEC-03 trigger is absent because no R3/R4 action exists. Approval records carry no expiry, and the authorization's own `expires_at_ms` (`ic2/engine.rs:217`) is never read anywhere in the runtime. |
| `das1_executor_only` | `evidence.rs:467-477` | AEC-03 substantially; AEC-01 partially; AECX-062 substantially | Strong for the execution boundary, partial for the catalog | Execution is gated on an allow decision in one place (`executor.rs:339-343`), and the governed set is closed at two capabilities (`executor.rs:32-35`). It does not evidence the AEC-01 catalog artifact: no owner, permissions, data classes, revocation path, or logging location is recorded per capability, and neither a risk ceiling nor an autonomy level is registered. It says nothing about what the runtime may grant, which is AEC-13. |
| `das1_receipts_written` | `evidence.rs:479-492` | AEC-07 | Partial | Receipts bind tool, timestamp, decision, execution flag, and correlation keys (`executor.rs:128-141`). Retention is not defined, which AEC-07 requires. The approver is not on the receipt; it lives on a separate approval record (`executor.rs:177-195`) correlated by trace and receipt key. The identifier reports "not yet" whenever nothing executed, which conflates an idle evidence window with a missing control. |
| `das1_revocation_exists` | `evidence.rs:494-508` | AEC-05 | Weak | Revocation is a status transition on one approval record (`executor.rs:403-419`, `executor.rs:514-537`). It prevents that proposal from being continued (`executor.rs:452-458`) and nothing else; a fresh request for the same capability is unaffected, so no authority is removed. There is no single-action kill switch, no quarterly drill cadence, no time-to-revoke measurement, and no cascade. The identifier also falls back to "partial" when zero revocations exist (`evidence.rs:497-501`), making it the only one of the seven that claims partial credit from an empty evidence set. |
| `das1_evidence_mapped` | `evidence.rs:510-518` | None | None | This is a self-referential assertion that the workflow maps to a checkable packet. Its condition is that follow-up references resolve to files on disk (`evidence.rs:170-171`, `evidence.rs:512`), which measures retrieval grounding rather than DAS-1 evidence completeness. The nearest DAS-1 obligation is the conformance criteria under `spec/conformance/`, which governs the claim process and is not a control. |

Binding requirements:

- A runtime MUST NOT present a locally defined identifier as a DAS-1 control. Where a runtime computes its own conformance view, each local identifier MUST carry the AEC number or numbers it evidences, or MUST be marked as evidencing none.
- A local identifier that evidences part of a control MUST record which part, so that the remainder is visible as a gap rather than absorbed by the mapping.
- A computed control status MUST NOT be better than "not yet" when its evidence set is empty.

Decision vocabulary crosswalk:

The core receipt schema admits two decision values, `allow` and `deny` (`schemas/receipt.schema.json:33`). The Psyche authorization vocabulary has four (`kernel/psyche-kernel/src/ic2/schema.rs:86-91`). A Psyche receipt rendered into core DAS-1 form MUST therefore use this mapping, and MUST carry the unmapped value in the overlay context so that the distinction is not lost:

| Psyche decision | Core receipt `decision` | `overlay_context.psyche.authorization_decision` |
|---|---|---|
| `allow` | `allow` | `allow` |
| `allow_with_safeguards` | `allow` | `allow_with_safeguards` |
| `escalate` | `deny` | `escalate` |
| `refuse` | `deny` | `refuse` |

The collapse of `escalate` into `deny` loses the distinction between "not now, pending a human" and "not at all", which is the distinction the whole approval path exists to express. Carrying it in `overlay_context.psyche.authorization_decision` is a workaround at overlay altitude; whether the core receipt schema should admit a third value is a question for a future core revision and is recorded in `spec/roadmap/v0.003-enterprise-load-findings.md` section 12.

## 8. Assessed control status of the Psyche runtime (Informative)

Assessed 2026-09-23 against the runtime at `/Volumes/scratch/psyche`. Statuses are stated against core v0.002 unless marked v0.003.

Partially evidenced:

- AEC-01 Tool catalog and ownership. The governed set is closed and enumerated in code (`executor.rs:32-35`). No catalog artifact, no per-capability owner, permissions, data classes, revocation path, or logging location, and no registered risk ceiling or autonomy level.
- AEC-03 Human gating for high risk actions. The propose-approve-recheck-execute chain exists and is file-backed. Approval is not attributable to a real principal (`frontend/src-tauri/src/main.rs:11`). The R3/R4 trigger has no subject because requests at risk tier 2 and above are refused in the authorization path (`ic2/engine.rs:136-141`), so the runtime has no R3/R4 actions to gate.
- AEC-05 Revocation kill switch and drill. Revocation exists as a record status only; no authority is removed, no cascade, no cadence, no time-to-revoke metric.
- AEC-06 Preflight plan and declared blast radius. Proposal packets exist for escalated requests only, and carry no declared blast radius and no containment or rollback plan.
- AEC-07 Audit trail completeness. Receipts, proposals, approvals, and evidence packets are written and correlated. Retention is undefined.

Not evidenced, with a subject present:

- AEC-04 Approval latency budget. No budget, no fallback, no measurement. Escalated proposals can sit indefinitely.
- AEC-08 Data class boundaries. The artifact root is enforced (`executor.rs:602-620`) but no data classes are defined and none are mapped to the read capability.
- AEC-11 Exceptions register and expiry. No register. The narrow approval bridge (`ic2/engine.rs:469-518`) is precisely the kind of deliberate deviation that AEC-11 exists to time-bound, and it is not registered.
- AEC-12 Tool-call incident annex and exercises. No annex, no tabletop.
- AEC-14 Action classification and composition (v0.003). Risk class is supplied by the calling constructor, which hardcodes tier 0 for both capabilities (`executor.rs:92`, `executor.rs:117`). No classifier is named, no register exists, no contest procedure exists, and no composition rule exists. The approved-continuation path composes an approval record with a replayed proposal into a single effect (`executor.rs:421-512`) without evaluating the composed class.

Not evidenced, with no subject in the present surface. These are recorded as unmet rather than waived, so that the gap is already named when a subject appears:

- AEC-02 Least privilege and time bounding. No credentials exist in the governed path. The only time bound in the runtime is `expires_at_ms` on the authorization (`ic2/engine.rs:217`), and nothing reads it.
- AEC-09 Secrets lifecycle and rotation. No secrets, therefore no rotation evidence. "Stores no plaintext secret" is satisfied by having none; "rotatable and rotated" has no evidence at all.
- AEC-10 Cost attribution and enforced caps. No cost-incurring tool call exists in the default proof path, no owner or cost-center tags, and no cap enforced in the execution path.
- AEC-13 Delegation envelope and cascading revocation (v0.003). The runtime delegates nothing. A repository-wide search for "delegat" across Rust, TypeScript, and Markdown sources returns no match. There is no subagent, no parent-child agent relationship, and one executor.

Annex A (v0.003):

- Not registered in the runtime. No autonomy level appears anywhere in the code. Four autonomy modes are named as a future requirement in the product specification (`docs/PSYCHE_REQUIREMENTS_SPEC.md:431-436`) and are neither implemented nor crosswalked to risk class. The registration in `overlays/platform/psyche/overlay.yaml` is this overlay's declaration, not a reading of the runtime.

Metrics and drills:

- None of M1 through M9 is currently measured.
- Neither core drill D1 nor D2 has a report in DAS-1 form. The runtime's approval lifecycle witness (`eval/reports/latest_approval_lifecycle_witness.md`) is the nearest artifact and is not a D2 equivalent: it records a revocation after a continuation has already executed, whereas D2 requires revoking mid-execution and confirming no further tool calls.

## 9. What this runtime does well, in DAS-1 terms (Informative)

Recorded because a mapping that lists only gaps is as misleading as one that lists only strengths.

- The authoritative gate is deterministic and local. It is not a model, so the decision is reproducible from inputs, which makes AEC-07's decision-trace reconstruction cheap rather than aspirational.
- Approval is a re-check eligibility gate rather than an execution grant (`docs/WORKING_PAPER_V0_1.md:68-77`, `executor.rs:421-512`). DAS-1 requires that approval precede execution; this runtime additionally requires that authorization re-run after approval and that its fresh decision govern. Human approval does not override a refusal. DAS-1 has no vocabulary for this, and it is stronger than AEC-03 requires.
- The model-backed advisor is non-authoritative by construction and its failure is recorded rather than silent (`runtime.rs:704-806`). It fails without changing the authoritative decision, and both disagreement and error are carried as explicit statuses.
- Conformance status is computed from runtime facts and is recomputable from the packet's own contents (`evidence.rs:151-161`, `evidence.rs:522-549`), so a verifier can check the packet rather than trust it. This is the posture DAS-1's conformance criteria assume and rarely get.
- The governed surface is honestly small and is documented as small. The runtime's own limitations section declines to claim what it has not proven (`docs/WORKING_PAPER_V0_1.md:124-136`).
