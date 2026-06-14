# AECX-062 Tool broker policy enforcement

Control statement
- Tool brokers SHOULD enforce identity, risk class, data class, approval state, logging, and revocation before tool invocation. Tool brokers that expose R3/R4 capabilities MUST default to deny when policy, identity, approval, or revocation state cannot be verified.

Supplemental guidance
- A tool broker may be embedded in a runtime, deployed as a gateway, or provided as an integration boundary.
- Tool names and descriptions are not sufficient authority; enforcement should bind to stable tool identity, owner, capability, destination, and policy.
- Broker decisions should be reconstructable from receipts.

Assessment objectives
- Confirm tool broker policies are explicit and enforced before invocation.
- Confirm broker decisions are logged with enough detail to reconstruct allow, deny, and approval-required outcomes.
- Confirm revocation prevents subsequent invocation through the broker.

Assessment methods
- Examine: tool catalog, broker policy, approval bindings, revocation logs, sample receipts.
- Interview: broker administrators and workflow owners.
- Test: invoke allowed, disallowed, approval-required, and revoked tools through the broker.

Receipts
- Broker policy snapshot
- Tool catalog binding
- Policy decision logs
- Revocation enforcement evidence
