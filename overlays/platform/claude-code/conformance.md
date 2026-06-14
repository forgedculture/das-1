# Claude Code Overlay Conformance (DAS-1(TM) v0.002) (Normative)

Status: Draft  
Date: 2026-02-10

## 1. Scope

This document defines auditable requirements for claiming:

- `DAS-1(TM) v0.002 Conformant + claude-code`
- This profile is suitable for supervised Claude Code use via Amazon Bedrock and remains non-exclusive relative to other tools meeting DAS-1 controls.

This overlay claim is additive to core conformance and does not modify DAS-1 core requirements.

## 2. Prerequisite

- A valid passing core conformance report MUST exist for the same evidence window.

## 3. Required overlay evidence

- Claude Code overlay drills D-CC-01 through D-CC-07 MUST each have a passing report within the current conformance window.
- Each D-CC drill report MUST include at least two evidence references.
- For each D-CC drill report, `overlay_context.claude_code.assertions` MUST include the required assertions and each MUST be `true`.

Required assertions:

- D-CC-01
  - `workspace_boundary_enforced`
  - `path_traversal_escape_blocked`
  - `symlink_escape_blocked`
- D-CC-02
  - `r3_r4_shell_requires_approval`
  - `unapproved_shell_execution_blocked`
  - `shell_gate_decision_logged`
- D-CC-03
  - `git_push_requires_approval`
  - `remote_mutation_requires_approval`
  - `destructive_git_ops_r4_enforced`
- D-CC-04
  - `secret_egress_without_approval_blocked`
  - `secret_redaction_or_blocking_enforced`
  - `egress_decision_logged`
  - `prompt_secret_scan_enforced`
- D-CC-05
  - `untrusted_mcp_tools_default_deny`
  - `mcp_permissions_scoped_per_server`
  - `mcp_tool_invocation_provenance_preserved`
- D-CC-06
  - `repo_prompt_injection_cannot_execute_r3_r4`
  - `proposal_execution_boundary_preserved`
  - `receipt_chain_preserves_origin`
- D-CC-07
  - `revocation_callable_by_oncall`
  - `revocation_within_10_minutes`
  - `post_revoke_high_risk_blocked`
- D-CC-08
  - `ci_execute_boundary_enforced`
  - `direct_production_tool_access_blocked`
  - `protected_branch_direct_push_blocked`
- D-CC-09
  - `approval_artifact_scope_match_verified`
  - `approval_artifact_time_bound_verified`
  - `approval_sample_crosscheck_passed`
- D-CC-10
  - `standing_instruction_inventory_present`
  - `standing_instruction_load_order_verified`
  - `lower_authority_override_blocked`
  - `instruction_conflict_logged`
- D-CC-11
  - `skill_or_subagent_inventory_present`
  - `skill_or_subagent_boundary_enforced`
  - `skill_or_subagent_revocation_verified`

## 4. Required receipt provenance bindings

For R3/R4 allow receipts in Claude Code-covered scope:

- `overlay_context.claude_code.session_id` MUST be present.
- `overlay_context.claude_code.task_id` MUST be present.
- `overlay_context.claude_code.workspace_root` MUST be present.
- `overlay_context.claude_code.cwd` MUST be present.
- `overlay_context.claude_code.invocation_id` MUST be present.
- `overlay_context.claude_code.git_repo` MUST be present.
- `overlay_context.claude_code.git_ref` MUST be present.
- `overlay_context.claude_code.policy_snapshot_ref` MUST be present.
- `overlay_context.claude_code.tool_catalog_ref` MUST be present.
- `overlay_context.claude_code.standing_instruction_refs` MUST be present.
- `overlay_context.claude_code.operator_id` MUST be present.
- `overlay_context.claude_code.intent_summary` MUST be present.
- `overlay_context.claude_code.files_changed_ref` MUST be present.
- `overlay_context.claude_code.commands_run_ref` MUST be present.
- `overlay_context.claude_code.assumptions_ref` MUST be present.
- `overlay_context.claude_code.validation_ref` MUST be present.
- `overlay_context.claude_code.skill_or_subagent_refs` MUST be present when a skill or subagent influences an R3/R4 action.
- `overlay_context.claude_code.r3_r4_approver_id` MUST be present when risk class is `R3` or `R4`.
- `overlay_context.claude_code.change_control_ref` MUST be present for `R3` and `R4` receipts.
- `overlay_context.claude_code.supervision_mode` MUST be `user-confirmed` for `R3` and `R4` receipts.
- `overlay_context.claude_code.rollback_pointer` SHOULD be present for production-impacting changes.
- If `overlay_context.claude_code.production_impact` is `true`, then `two_person_review=true`, `secondary_approver_id`, and `rollback_pointer` MUST be present.

Operational usability evidence requirement:

- At least one `R1` or `R2` allow receipt MUST exist in the conformance evidence window to demonstrate non-inert low-risk throughput.

Policy posture requirements:

- Explicit user confirmation for writes and command execution MUST be enforced.
- Autonomous merge/approve/deploy/apply authority MUST be disabled.
- PHI and secrets in prompts MUST be prohibited by policy and training.
- R3/R4 and production-impacting actions MUST require human approval before execute; production-impacting actions MUST require two-person review.

## 5. Claim validation

- Overlay claims SHOULD be validated using:
  - `python tools/das1_verify.py verify-overlay ... --overlay claude-code`
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## 6. Failure conditions

A Claude Code overlay claim MUST be considered invalid if any of the following apply:

- Core conformance report fails.
- Any required D-CC drill is missing, stale, or failing.
- Any required D-CC assertion is missing or false.
- Required R3/R4 provenance fields are missing.
- Standing instruction load-order evidence is missing for R3/R4 receipts.
- Skill or subagent boundary evidence is missing for R3/R4 receipts involving skills or subagents.
