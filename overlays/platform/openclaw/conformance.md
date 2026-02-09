# OpenClaw Overlay Conformance (DAS-1(TM) v0.001) (Normative)

Status: Draft  
Date: 2026-02-09

## 1. Scope

This document defines auditable requirements for claiming:

- `DAS-1(TM) v0.001 Conformant + openclaw`

This overlay claim is additive to core conformance and does not modify DAS-1 core requirements.

## 2. Prerequisite

- A valid passing core conformance report MUST exist for the same evidence window.

## 3. Required overlay evidence

- OpenClaw overlay drills D-OC-01 through D-OC-07 MUST each have a passing report within the current conformance window.
- Each D-OC drill report MUST include at least two evidence references.
- For each D-OC drill report, `overlay_context.openclaw.assertions` MUST include the required assertions and each MUST be `true`.

Required assertions:

- D-OC-01
  - `proposed_action_recorded`
  - `execution_blocked_without_approval`
  - `sender_session_provenance_preserved`
- D-OC-02
  - `remote_localhost_inheritance_blocked`
  - `unauth_high_risk_execution_blocked`
  - `trusted_proxy_evaluation_logged`
- D-OC-03
  - `non_main_session_sandboxed`
  - `host_filesystem_traversal_blocked`
  - `unauthorized_network_egress_blocked`
- D-OC-04
  - `session_scope_isolation_enforced`
  - `cross_peer_context_bleed_blocked`
  - `session_scope_key_bound_in_receipts`
- D-OC-05
  - `connector_scopes_least_privilege`
  - `connector_tokens_rotatable_independently`
  - `high_risk_connector_split_enforced`
- D-OC-06
  - `r3_r4_execution_without_approval_blocked`
  - `expired_exceptions_not_honored`
  - `exception_override_disclosure_recorded`
- D-OC-07
  - `revocation_kill_switch_reachable_by_oncall`
  - `revocation_within_slo`
  - `post_revoke_actions_blocked`

## 4. Required receipt provenance bindings

For R3/R4 allow receipts in OpenClaw-covered scope:

- `overlay_context.openclaw.channel_id` MUST be present.
- `overlay_context.openclaw.sender_id` MUST be present.
- `overlay_context.openclaw.session_scope_key` MUST be present.
- `overlay_context.openclaw.gateway_instance_id` MUST be present.
- `overlay_context.openclaw.policy_snapshot_ref` MUST be present.
- `overlay_context.openclaw.tool_catalog_ref` MUST be present.

## 5. Claim validation

- Overlay claims SHOULD be validated using:
  - `python tools/das1_verify.py verify-overlay ... --overlay openclaw`
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## 6. Failure conditions

An OpenClaw overlay claim MUST be considered invalid if any of the following apply:

- Core conformance report fails.
- Any required D-OC drill is missing, stale, or failing.
- Any required D-OC assertion is missing or false.
- Required R3/R4 provenance fields are missing.
