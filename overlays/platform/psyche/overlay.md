# DAS-1(TM) Psyche overlay v0.002 (Informative)

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Bind the Psyche local-first governed agent runtime to DAS-1 vocabulary, so that a runtime which computes its own conformance status does so against numbered controls rather than against locally invented identifiers.
- Prevent authority crossing in a runtime where a local model, a desktop UI, a stored approval record, or a shadow advisor could become an alternate path around the kernel-owned authorization and executor boundary.
- Make the deliberately small governed capability surface auditable as a small surface, rather than letting a narrow proof of concept be read as a broad conformance claim.

Scope note (Informative)
- Psyche is a local-only proof of concept. Its entire governed capability surface is two local operations, `echo_authorized_action` and `read_local_artifact_text`, enumerated in `kernel/psyche-kernel/src/executor.rs:32-35`. There is no network egress in the default proof path, no credential, no cost-incurring call, no secret, no delegation, and no second operator.
- This overlay therefore has two jobs. It states what the runtime genuinely evidences, and it states which controls have no subject at all in the present surface. A control with no evidence is doctrine; so is a control with no subject. Both are recorded here as unmet rather than waived.

Threat assumptions
- A local model may propose an action that must not become an effect without a recorded authorization decision.
- A desktop UI may render approval state and could be mistaken for the authority that produced it.
- A stored approval record may be replayed, edited, or paired with a proposal it does not describe.
- A shadow or advisory model path may be promoted to load-bearing by accident, or may fail in a way that silently changes the authoritative decision.
- A relative artifact path may escape its declared root by traversal, absolute path, or symlink.
- A computed conformance packet may be hand-edited after generation and still present as machine-derived.
- A governed capability surface may grow without its risk ceiling, autonomy level, or tool catalog entry being revisited.

Tightens
- AEC-01: the governed capability set MUST be closed and enumerated in the runtime, and the tool catalog entry for the runtime MUST register both a risk ceiling and an autonomy level per Annex A.3, together with owner, revocation path, and logging location for each governed capability.
- AEC-03: human approval MUST NOT be an execution grant. An approval record MAY make a stored proposal eligible for a fresh authorization re-check, and the re-check decision governs. Approval MUST be attributable to a distinguishable principal; a build-time constant operator identity does not satisfy attributability.
- AEC-05: revocation MUST remove authority from the agent, not only mark a proposal record as revoked. Post-revocation execution attempts MUST be blocked and logged.
- AEC-06: a proposal packet MUST be written for every governed request that does not execute, not only for escalated ones, and MUST carry target, intended effect, declared blast radius, and containment or rollback plan. A rollback class is a classification, not a plan.
- AEC-07: receipts MUST bind proposal, approval, continuation, and execution through correlation identifiers, and retention MUST be defined for the local receipt, proposal, approval, and evidence stores.
- AEC-08: the artifact read root MUST be declared, canonically resolved before each read, and mapped to a data class.
- AEC-11: local deviations, including any temporary widening of the capability surface or of the approval bridge, MUST be registered with owner and expiry.

Adds
- AECX-050 Workspace containment
- AECX-062 Tool broker policy enforcement
- AECX-064 Delegated agent control
- AECX-065 Context and memory containment
- AECX-066 Approval artifact integrity
- AECX-067 Autonomous change budget

Psyche runtime baseline
- The governed capability surface is closed at two local operations and MUST remain enumerated in one place. Adding a capability is a change to the registered risk ceiling question and MUST be treated as such.
- Deterministic local authorization (IC2) is the authoritative gate. Every governed request MUST pass it, and execution MUST follow only an `allow` or `allow_with_safeguards` decision.
- Any model-backed authorization advisor MUST be non-authoritative. Its disagreement with the authoritative decision MUST be recorded as disagreement, its failure MUST be recorded as failure, and neither MUST change the authoritative decision. Promotion of an advisory path to load-bearing is a separate risk-gated decision under AEC-03 and MUST NOT occur as a configuration change.
- Human approval is a re-check eligibility gate. An approved record permits the saved proposal to be replayed through authorization under a fresh trace and receipt key; it does not permit execution. A denied, revoked, missing, mismatched, or already-continued record MUST NOT be continuable.
- Human approval MUST NOT convert a refusal into an execution. The narrow bridge from escalation to `allow_with_safeguards` MUST remain bounded to reversible, below-ceiling actions whose escalation reasons are review gates rather than refusals, and the bound MUST be enforced in the authorization path rather than in the caller.
- Conformance status MUST be computed from runtime facts and MUST be recomputable from the packet's own contents, so that a verifier can check the packet rather than trust it. A status asserted in prose is not evidence.
- A status of "partial" MUST NOT be reachable from an empty evidence set. Where no evidence exists, the status is "not yet".
- Artifact reads MUST be confined to a declared root, resolved canonically, with traversal, absolute-path, and symlink escape denied before the read rather than detected after it.
- The runtime MUST NOT grant authority to any other component. If any organ, sidecar, subagent, or provider path is given authority to invoke a governed capability, that grant MUST produce a delegation record before it ships.
- Operator identity MUST be resolved at runtime and MUST be capable of distinguishing two operators. Approvals, denials, and revocations MUST carry that resolved identity.
- Low-risk governed work SHOULD execute without per-action human approval when policy conditions are satisfied, so the runtime is not safe only because it is inert.

Annex A registration (Informative for v0.002, normative under v0.003)
- Registered autonomy level: A5 Execute under policy, for actions within the registered risk ceiling. The runtime executes an authorized governed capability without per-action human approval when the authorization decision permits it.
- Registered risk ceiling: R2. The declared crosswalk from the runtime's internal risk tier is: tier 0 maps to R1, tier 1 maps to R2, tier 2 and above is refused in the authorization path and is therefore unreachable.
- Effective authority is the intersection, per Annex A.3: A5 within R1 and R2 only. Because the ceiling terminates below R3, the AEC-03 R3/R4 approval gate has no subject in this runtime. The runtime's approval machinery is triggered by ethics and policy escalation signals rather than by risk class, and is therefore an additional control, not the AEC-03 gate.
- Both values MUST appear in the AEC-01 tool catalog entry. Promotion of the autonomy level MUST NOT raise the registered risk ceiling, and raising the ceiling above R2 is a separate decision requiring its own approval.

v0.003 readiness (Informative)
- AEC-13 delegation: the runtime delegates nothing. There is no parent-child agent relationship, no subagent, and no grant of authority to any other component. The control has no subject, so it is unmet rather than satisfied, and D-PSY-10 exists to detect the day that changes.
- AEC-14 classification and composition: risk class is supplied by the calling constructor rather than assigned by a named classifier, there is no classification register, no contest procedure, and no composition rule. The approved-continuation path composes an approval record and a replayed proposal into one effect without evaluating the composed class.
- Annex A: registered above. This is the first platform overlay in this repository to register both axes.

Overlay drills
- D-PSY-01 Authoritative gate test
  - Pass: a governed request whose authorization decision is not `allow` or `allow_with_safeguards` produces a receipt with no execution and no capability effect.
  - Output: receipt chain showing decision, execution flag, and absent effect.
- D-PSY-02 Approval is not an execution grant test
  - Pass: an approved record alone executes nothing; continuation replays the stored proposal through authorization; a proposal that still refuses does not execute despite the approval.
  - Output: approval record, proposal packet, continuation receipt, and the re-check decision.
- D-PSY-03 Approval artifact integrity test
  - Pass: a mismatched approval-to-proposal pair, an edited proposal packet, a reused continuation trace or receipt key, and a denied or revoked record are each refused before authorization is re-run.
  - Output: refusal reasons and the rejected-continuation logs.
- D-PSY-04 Artifact root containment test
  - Pass: parent-directory traversal, absolute path, and symlink escape from the declared artifact root are denied before the read.
  - Output: denied-escape receipts and the resolved root declaration.
- D-PSY-05 Advisory non-authority test
  - Pass: with the advisory model disagreeing, erroring, and unavailable in turn, the authoritative decision is unchanged in all three cases and each outcome is recorded with its status.
  - Output: advisory snapshots showing status and recorded disagreement or error alongside the unchanged authoritative decision.
- D-PSY-06 Risk ceiling test
  - Pass: a request above the registered risk ceiling is refused in the execution path, and human approval does not rescue it.
  - Output: refusal receipt, reason codes, and the failed approval attempt.
- D-PSY-07 Revocation and post-revocation block test
  - Pass: revocation is callable by the operator, the revoked proposal cannot be continued, and a fresh governed request made under revoked authority is blocked.
  - Output: revocation record, blocked continuation, and blocked post-revocation request.
- D-PSY-08 Operator attribution test
  - Pass: two distinct operators produce two distinct recorded identities on approval, denial, and revocation records, and no approval record carries a build-time constant identity.
  - Output: approval records from two principals and the identity resolution path.
- D-PSY-09 Computed status integrity test
  - Pass: the evidence packet's stored verification block equals a fresh recomputation from its own claims, and a hand-edited packet is detected.
  - Output: packet, recomputation result, and the detection of the edited copy.
- D-PSY-10 Delegation absence test
  - Pass: no component other than the governed executor can invoke a governed capability, and any path that grants such authority produces a delegation record naming grantor, grantee, granted scope, granted risk ceiling, granted autonomy level, and expiry.
  - Output: invocation-path inventory and either the absence finding or the delegation records.

Operational risk closure requirements
- For every governed allow receipt, `overlay_context.psyche` MUST include `trace_id`, `receipt_key`, `capability`, `authorization_decision`, `operator_id`, `risk_ceiling`, `autonomy_level`, `artifact_root`, and `evidence_packet_ref`.
- For every receipt produced by an approved continuation, `overlay_context.psyche` MUST additionally include `approval_ref`, `proposal_ref`, `source_trace_id`, `source_receipt_key`, and `recheck_decision`, and `recheck_decision` MUST be the decision the continuation's own authorization returned rather than the decision recorded on the original proposal.
- `overlay_context.psyche.operator_id` MUST identify a principal resolved at runtime. A constant compiled into the application does not satisfy this requirement.
- `overlay_context.psyche.advisory` MUST be present whenever a model-backed advisor ran, and MUST carry `status`, `authoritative_decision`, and, where the advisor returned a decision, `advisory_decision` and `agreement`.
- Evidence MUST include at least one `R1` or `R2` allow receipt, to show that governed low-risk work executes rather than being blocked into uselessness.
- Evidence MUST include at least one non-executing receipt, to show that the gate refuses rather than rubber-stamping.
- Retention for the local receipt, proposal, approval, and evidence stores MUST be declared in the policy snapshot.

Known unmet controls in the current runtime (Informative)
- AEC-02, AEC-04, AEC-08, AEC-09, AEC-10, AEC-11, AEC-12, AEC-13, and AEC-14 have no evidence in the present surface. Several of them also have no subject: there are no credentials, no secrets, no cost-incurring calls, and no delegation. Absence of a subject is recorded as unmet, not as satisfied, so that the day a subject appears the gap is already named.
- AEC-01, AEC-03, AEC-05, AEC-06, and AEC-07 are partially evidenced. The specific partials are enumerated in `overlays/platform/psyche/conformance.md` section 8.
- No DAS-1 minimum metric M1 through M9 is currently measured, and neither required core drill D1 nor D2 has a report in DAS-1 form.
- This overlay is therefore publishable as a mapping and as a hardening target. It is not a claim, and the runtime does not currently qualify for one.

Verifier mapping (informative)
- Overlay checks are implemented as a plugin (`tools/overlays/psyche.py`) and run via `verify-overlay --overlay psyche`.
- Normative claim requirements are defined in `overlays/platform/psyche/conformance.md`.
