# Delegated Authority Standard(TM) (DAS-1(TM)) v0.003

Subtitle: Tool calls are production changes.

Status: Draft. v0.003 core deltas are under review; v0.002 remains the current released version.
Date: 2026-08-20

## 1. Conformance keywords (Normative)

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, MAY are to be interpreted as described in RFC 2119.

## 2. Terms and scope (Normative)

Definitions
- Delegated authority: authority exercised by a system on behalf of a human or organization.
- Tool call: any invocation that can read data, write data, change state, spend money, or trigger workflows.
- Receipt: evidence reproducible enough to steer a decision without a personality contest.
- Revocation: a bounded action that removes authority and blocks further execution.
- Delegation: the act of one agent granting a subset of its own authority to another agent for a bounded task.
- Delegation lineage: the chain of delegation records linking an executing agent back to the original human principal.
- Autonomy level: how much latitude an agent has with a result, independent of the consequence of the action. Defined in Annex A.
- Composed effect: the combined outcome of a sequence of actions within one authorized task, which may exceed the risk class of any individual action in that sequence.

Scope
- In scope: any agent, automation, workflow, or integration that can change state, access sensitive data, trigger actions, or spend money.
- Out of scope: pure text generation without tool invocation and without access to protected data/systems.
- Applies to: production, staging with production data, and any privileged environment.

Risk classes (default; replaceable with explicit mapping)
- R1: read-only, low sensitivity, low cost, no external side effects.
- R2: sensitive reads or small writes with trivial blast radius.
- R3: privileged access or meaningful write blast radius.
- R4: high impact, irreversible, secrets/identity, production change.
- Design intent: controls MUST be risk-proportional so low-risk work remains useful while high-risk work remains bounded.
- Classification ownership, reclassification triggers, ambiguity posture, and the composition rule are normative and specified in AEC-14.
- Risk class describes the consequence of an action. It does not describe an agent's latitude with a result. That is the autonomy dimension, specified in Annex A.

## 3. Authority Engineering Controls (AEC) (Normative)

AEC-01 Tool catalog and ownership
- The organization MUST maintain a tool catalog per agent/workflow with: tool, actions, permissions, data classes, owner, revocation path, logging location.
- Receipt: catalog export plus review record and diff.

AEC-02 Least privilege and time bounding
- Delegated authority credentials MUST be least-privilege and time-bounded.
- Shared long-lived credentials MUST NOT be used.
- Receipt: policy snapshot plus TTL evidence.

AEC-03 Human gating for high risk actions
- R3 and R4 tool calls MUST require explicit human approval prior to execution.
- Approval MUST be attributable and linked to execution.
- R1 and R2 actions SHOULD execute without per-action human approval when policy conditions are satisfied.
- Receipt: approval policy plus correlated approval logs.

AEC-04 Approval latency budget
- The organization MUST define an approval latency budget and a fallback when budget is exceeded.
- Fallback behavior MUST preserve bounded utility for R1/R2 while failing safely for R3/R4.
- Receipt: SLO doc plus measured p95 approval latency.

AEC-05 Revocation kill switch and drill
- A single-action revocation mechanism MUST exist per agent/workflow.
- Revocation MUST be tested at least quarterly.
- Receipt: drill record plus time-to-revoke metrics.

AEC-06 Preflight plan and declared blast radius
- For R3/R4 tool calls, a preflight plan MUST be produced and stored prior to execution, including target, intended change, blast radius, containment/rollback plan.
- Execution MUST be blocked if preflight is missing.
- Receipt: stored preflight plus correlated execution logs.

AEC-07 Audit trail completeness
- Every tool call MUST be recorded with: tool, timestamp, inputs present, outputs present, approver (if gated), and correlation IDs tying plan, approval, execution, downstream effects.
- Retention MUST be defined.
- Receipt: log schema, sample pack, retention config.

AEC-08 Data class boundaries
- Data classes MUST be defined and mapped to allowed tools, destinations, retention, and transformations.
- R3/R4 data MUST have explicit allowed-path rules.
- Receipt: classification map plus enforcement evidence.

AEC-09 Secrets lifecycle and rotation
- Agents MUST NOT store plaintext secrets.
- Secret access MUST be attributable and logged.
- Secrets MUST be rotatable and rotated.
- Receipt: rotation logs plus access logs.

AEC-10 Cost attribution and enforced caps
- Cost-incurring tool calls MUST emit owner and cost center tags.
- R3/R4 workflows MUST have caps/circuit breakers.
- Caps MUST be enforced in the execution path. A forecast, budget model, spend alert, or reporting-layer control MUST NOT be presented as satisfying this control.
- Every cap MUST have a named owner and a documented raise path with a response target.
- Receipt: tag coverage report plus a D4 cap breaker drill result.
- Design intent: a cap is a containment control that happens to be denominated in currency. Runaway spend is usually the first observable symptom of runaway execution.

AEC-11 Exceptions register and expiry
- Exceptions MUST be documented, owned, time-bounded, reviewed, and expire by default.
- Exceptions MUST NOT silently renew.
- Receipt: exception register plus expiry enforcement evidence.

AEC-12 Tool-call incident annex and exercises
- Incident response MUST include a tool-call annex for detection, containment via revocation, evidence capture, and decision trace reconstruction.
- At least one tabletop MUST be run annually.
- Receipt: annex plus exercise record and remediations.

AEC-13 Delegation envelope and cascading revocation
- A delegating agent MUST NOT grant authority it does not hold. Delegated authority MUST be a subset of the delegating agent's authority on every axis, including tools, data classes, risk ceiling, and autonomy level.
- Every delegation MUST produce a delegation record naming the delegating agent, the delegated agent, the granted scope, the granted risk ceiling, and an expiry.
- Revocation of an agent MUST revoke or block every live delegation descended from it, and the cascade MUST complete within the AEC-05 revocation budget.
- Delegation lineage MUST be reconstructable from receipts, so that any executed action resolves to the original human principal.
- Receipt: delegation records plus a D3 delegation cascade drill result.
- Design intent: the tool catalog governs what an agent may call. This control governs what an agent may grant. Delegation is the mechanism by which authority silently expands while every individual control still passes.

AEC-14 Action classification and composition
- The organization MUST define who classifies an action, on what evidence, and how a contested classification is resolved.
- Classification MUST be reviewed when the tool, its scope, its data class, or its blast radius changes.
- Where a sequence of actions within one authorized task produces a composed effect exceeding the highest class of any individual action in that sequence, the sequence MUST be governed at the composed class.
- The organization MUST state its default posture for ambiguous classification, and that default MUST be the higher class.
- Receipt: classification register with owner and review date, plus a composition test case showing a sequence governed at its composed class.
- Design intent: this control states an obligation to have an answer, not a detection algorithm. Prescribing detection mechanics would make the core vendor-specific; detection belongs in overlays.

## 4. Minimum metrics (Normative)

- M1 Time-to-revoke (p50, p95)
- M2 Approval latency (p50, p95)
- M3 Audit completeness rate
- M4 Cost attribution coverage
- M5 R1/R2 autonomous execution coverage rate
- M6 R1/R2 execution latency (p50, p95)
- M7 Blocked or queued action rate by risk class
- M8 Cap enforcement rate: over-cap events halted in the execution path as a proportion of over-cap events observed
- M9 Delegation cascade completion time (p50, p95)

## 5. Required drills (Normative)

D1 Tool-Call Pager Test
- Pass: chain reconstructed from receipts; correct approve/deny; revocation within budget.
- Outputs: scorecard plus receipts pack.

D2 Revocation Fire Drill
- Pass: revoke mid-execution; confirm no further tool calls; audit completeness preserved.
- Outputs: drill log plus remediations.

D3 Delegation Cascade Drill
- Pass: revoke a delegating agent mid-execution; confirm no descendant agent executes afterward; cascade completes within the AEC-05 revocation budget; delegation lineage reconstructed from receipts back to the human principal.
- Outputs: drill log plus lineage reconstruction and remediations.

D4 Cap Breaker Drill
- Pass: drive a workflow past its cap; confirm the breaker halts execution in the execution path rather than reporting the overage after the fact; confirm the named cap owner is notified.
- Outputs: drill log plus cap owner notification evidence and remediations.

## 6. Utility guardrails (Normative)

- Organizations MUST define target ranges for M5-M7 and review them at least monthly.
- If emergency hardening materially reduces R1/R2 utility, the reduction MUST be tracked as an AEC-11 exception with owner and expiry.
- Conformance evidence MUST show both protection outcomes and usefulness outcomes; "safe because inert" is not a sufficient operating posture.
- A cap with no functioning raise path is an availability failure, not a safety control, and MUST be tracked as an AEC-11 exception until the raise path is restored.

## 7. Annexes (Normative)

- Annex A, Autonomy levels (`annex-a-autonomy.md`): defines the autonomy dimension, its crosswalk to risk classes, and the binding rule that effective authority is the intersection of autonomy level and risk ceiling rather than the maximum of them.
