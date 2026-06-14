# Kiro Overlay Conformance (DAS-1(TM) v0.001) (Normative)

Status: Draft
Date: 2026-06-14

## 1. Scope

This document defines auditable requirements for claiming:

- `DAS-1(TM) v0.001 Conformant + kiro`

This overlay claim is additive to core conformance and does not modify DAS-1 core requirements.

## 2. Prerequisite

- A valid passing core conformance report MUST exist for the same evidence window.

## 3. Required overlay evidence

- Kiro overlay drills D-KIRO-01 through D-KIRO-05 MUST each have a passing report within the current conformance window.
- Each D-KIRO drill report MUST include at least two evidence references.
- For each D-KIRO drill report, `overlay_context.kiro.assertions` MUST include the required assertions and each MUST be `true`.

Required assertions:

- D-KIRO-01
  - `steering_inventory_present`
  - `steering_load_order_verified`
  - `lower_authority_steering_override_blocked`
  - `steering_conflict_logged`
- D-KIRO-02
  - `spec_artifacts_reviewable_before_execution`
  - `r3_r4_spec_task_requires_approval`
  - `unapproved_spec_task_execution_blocked`
- D-KIRO-03
  - `hook_side_effect_requires_approval`
  - `unapproved_hook_command_blocked`
  - `hook_execution_receipt_preserved`
- D-KIRO-04
  - `untrusted_mcp_tools_default_deny`
  - `mcp_tool_permissions_scoped`
  - `mcp_tool_invocation_provenance_preserved`
- D-KIRO-05
  - `revocation_callable_by_oncall`
  - `revocation_within_slo`
  - `post_revoke_high_risk_blocked`

## 4. Required receipt provenance bindings

For R3/R4 allow receipts in Kiro-covered scope:

- `overlay_context.kiro.session_id` MUST be present.
- `overlay_context.kiro.task_id` MUST be present.
- `overlay_context.kiro.workspace_root` MUST be present.
- `overlay_context.kiro.cwd` MUST be present.
- `overlay_context.kiro.invocation_id` MUST be present.
- `overlay_context.kiro.git_repo` MUST be present.
- `overlay_context.kiro.git_ref` MUST be present.
- `overlay_context.kiro.policy_snapshot_ref` MUST be present.
- `overlay_context.kiro.tool_catalog_ref` MUST be present.
- `overlay_context.kiro.steering_refs` MUST be present and MUST identify active workspace/global steering, foundational steering, and AGENTS.md artifacts when applicable.
- `overlay_context.kiro.operator_id` MUST be present.
- `overlay_context.kiro.intent_summary` MUST be present.
- `overlay_context.kiro.files_changed_ref` MUST be present.
- `overlay_context.kiro.commands_run_ref` MUST be present.
- `overlay_context.kiro.tools_invoked_ref` MUST be present when tools, MCP servers, hooks, or delegated agents are used.
- `overlay_context.kiro.assumptions_ref` MUST be present.
- `overlay_context.kiro.validation_ref` MUST be present.
- `overlay_context.kiro.r3_r4_approver_id` MUST be present when risk class is `R3` or `R4`.
- `overlay_context.kiro.change_control_ref` MUST be present for `R3` and `R4` receipts.
- `overlay_context.kiro.supervision_mode` MUST be `user-confirmed` for `R3` and `R4` receipts.
- `overlay_context.kiro.rollback_pointer` SHOULD be present for production-impacting changes.
- If `overlay_context.kiro.production_impact` is `true`, then `two_person_review=true`, `secondary_approver_id`, and `rollback_pointer` MUST be present.

Spec-task receipt bindings:

- If `overlay_context.kiro.is_spec_task` is `true`, then `spec_ref`, `requirements_ref`, `design_ref`, `tasks_ref`, and `task_execution_ref` MUST be present so that requirements, design, and tasks remain reviewable and traceable to the executed task.

Hook receipt bindings:

- If `overlay_context.kiro.is_hook` is `true`, then `hook_id`, `trigger_type`, `action_type`, and `hook_review_ref` MUST be present so that the triggering event, action class, and review status are attributable.

Authority-surface bindings:

- If `overlay_context.kiro.used_authority_surface` is `true`, then `authority_surface_refs` MUST be present and MUST identify owner, source/version, review status, execution boundary, approval requirement, and revocation path for the specs, hooks, MCP/tools, shell commands, or CI/CD effects exercised.

Operational usability evidence requirement:

- At least one `R1` or `R2` allow receipt MUST exist in the conformance evidence window to demonstrate non-inert low-risk throughput.

Policy posture requirements:

- Reviewed workspace/global steering, foundational steering, and AGENTS.md instructions MUST load by default according to declared scope, inclusion mode, and precedence.
- Specs MUST preserve requirements, design, and tasks as reviewable artifacts before execution.
- Explicit user confirmation for shell commands, hook commands, privileged MCP/tool calls, git egress, and CI/CD-affecting spec tasks MUST be enforced according to risk class.
- Autonomous merge/approve/deploy/apply authority MUST be disabled unless a separate approved policy explicitly grants it.
- PHI and secrets in steering files, specs, hooks, or tool inputs MUST be prohibited by policy and training.
- R3/R4 and production-impacting actions MUST require human approval before execute; production-impacting actions MUST require two-person review.

## 5. Claim validation

- Overlay claims SHOULD be validated using:
  - `python tools/das1_verify.py verify-overlay ... --overlay kiro`
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## 6. Failure conditions

A Kiro overlay claim MUST be considered invalid if any of the following apply:

- Core conformance report fails.
- Any required D-KIRO drill is missing, stale, or failing.
- Any required D-KIRO assertion is missing or false.
- Required R3/R4 provenance fields are missing.
- Steering load-order evidence is missing for R3/R4 receipts.
- Spec-task bindings are missing for R3/R4 spec-task receipts.
- Hook bindings are missing for R3/R4 hook receipts.
- Spec, hook, MCP/tool, shell, or CI/CD boundary evidence is missing for R3/R4 receipts involving those authority surfaces.
