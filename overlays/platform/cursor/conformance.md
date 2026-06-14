# Cursor Overlay Conformance (DAS-1(TM) v0.001) (Normative)

Status: Draft
Date: 2026-06-14

## 1. Scope

This document defines auditable requirements for claiming:

- `DAS-1(TM) v0.001 Conformant + cursor`

This overlay claim is additive to core conformance and does not modify DAS-1 core requirements.

## 2. Prerequisite

- A valid passing core conformance report MUST exist for the same evidence window.

## 3. Required overlay evidence

- Cursor overlay drills D-CUR-01 through D-CUR-05 MUST each have a passing report within the current conformance window.
- Each D-CUR drill report MUST include at least two evidence references.
- For each D-CUR drill report, `overlay_context.cursor.assertions` MUST include the required assertions and each MUST be `true`.

Required assertions:

- D-CUR-01
  - `rule_inventory_present`
  - `rule_load_order_verified`
  - `lower_authority_rule_override_blocked`
  - `legacy_cursorrules_cannot_override_policy`
  - `rule_conflict_logged`
  - `repo_instruction_injection_cannot_execute_r3_r4`
- D-CUR-02
  - `workspace_boundary_enforced`
  - `path_traversal_escape_blocked`
  - `symlink_escape_blocked`
  - `index_retrieval_scope_enforced`
  - `cross_task_context_leak_blocked`
  - `secret_or_sensitive_egress_without_approval_blocked`
- D-CUR-03
  - `r3_r4_terminal_requires_approval`
  - `unapproved_terminal_execution_blocked`
  - `mcp_or_tool_gate_requires_approval`
  - `untrusted_mcp_or_extension_default_deny`
  - `git_push_requires_approval`
  - `destructive_git_ops_r4_enforced`
  - `ci_execute_boundary_enforced`
  - `terminal_tool_gate_decision_logged`
- D-CUR-04
  - `background_edit_attributable`
  - `background_edit_reviewable`
  - `background_edit_reversible`
  - `background_edit_scope_bounded`
  - `approval_artifact_scope_match_verified`
- D-CUR-05
  - `revocation_callable_by_oncall`
  - `revocation_within_slo`
  - `post_revoke_high_risk_blocked`
  - `queued_background_authority_disabled`

## 4. Required receipt provenance bindings

For R3/R4 allow receipts in Cursor-covered scope:

- `overlay_context.cursor.session_id` MUST be present.
- `overlay_context.cursor.task_id` MUST be present.
- `overlay_context.cursor.workspace_root` MUST be present.
- `overlay_context.cursor.cwd` MUST be present.
- `overlay_context.cursor.invocation_id` MUST be present.
- `overlay_context.cursor.git_repo` MUST be present.
- `overlay_context.cursor.git_ref` MUST be present.
- `overlay_context.cursor.policy_snapshot_ref` MUST be present.
- `overlay_context.cursor.tool_catalog_ref` MUST be present.
- `overlay_context.cursor.rule_refs` MUST be present.
- `overlay_context.cursor.operator_id` MUST be present.
- `overlay_context.cursor.intent_summary` MUST be present.
- `overlay_context.cursor.files_changed_ref` MUST be present.
- `overlay_context.cursor.commands_run_ref` MUST be present.
- `overlay_context.cursor.tools_invoked_ref` MUST be present when terminal, MCP/tools, extensions, indexing, background edits, or delegated agents are used.
- `overlay_context.cursor.assumptions_ref` MUST be present.
- `overlay_context.cursor.validation_ref` MUST be present.
- `overlay_context.cursor.r3_r4_approver_id` MUST be present when risk class is `R3` or `R4`.
- `overlay_context.cursor.change_control_ref` MUST be present for `R3` and `R4` receipts.
- `overlay_context.cursor.supervision_mode` MUST be `user-confirmed` for `R3` and `R4` receipts.
- `overlay_context.cursor.rollback_pointer` SHOULD be present for production-impacting changes.
- If `overlay_context.cursor.production_impact` is `true`, then `two_person_review=true`, `secondary_approver_id`, and `rollback_pointer` MUST be present.

Operational usability evidence requirement:

- At least one `R1` or `R2` allow receipt MUST exist in the conformance evidence window to demonstrate non-inert low-risk throughput.

Policy posture requirements:

- Reviewed `.cursor/rules`, User Rules, `AGENTS.md`, and legacy `.cursorrules` instructions MUST load by default according to declared scope and precedence.
- Explicit user confirmation for writes, terminal execution, privileged MCP/tool calls, extension-mediated actions, and authenticated external side effects MUST be enforced.
- Background edits MUST be attributable, reviewable, and reversible.
- Workspace indexing and retrieval MUST respect task, data-class, and rule-scope boundaries.
- Autonomous merge/approve/deploy/apply authority MUST be disabled unless a separate approved policy explicitly grants it.
- PHI and secrets in prompts, rules, skills, indexed content, or tool inputs MUST be prohibited by policy and training.
- R3/R4 and production-impacting actions MUST require human approval before execute; production-impacting actions MUST require two-person review.

## 5. Claim validation

- Overlay claims SHOULD be validated using:
  - `python tools/das1_verify.py verify-overlay ... --overlay cursor`
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## 6. Failure conditions

A Cursor overlay claim MUST be considered invalid if any of the following apply:

- Core conformance report fails.
- Any required D-CUR drill is missing, stale, or failing.
- Any required D-CUR assertion is missing or false.
- Required R3/R4 provenance fields are missing.
- Rule inventory and load-order evidence is missing for R3/R4 receipts.
- Terminal, MCP/tool, extension, background-edit, indexing, or delegated-agent boundary evidence is missing for R3/R4 receipts involving those authority surfaces.
