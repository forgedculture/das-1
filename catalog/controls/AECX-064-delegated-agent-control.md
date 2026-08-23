# AECX-064 Delegated agent control

Relationship to core
- As of DAS-1(TM) v0.003, AEC-13 makes the delegation envelope, the subset rule, the delegation record, cascading revocation, and lineage reconstruction mandatory in the core. AECX-064 no longer restates those obligations.
- AECX-064 remains as the extended control covering the operational remainder: the non-authority boundaries (task, cost, time), the environmental paths by which delegation can expand authority without granting it, and accountability assignment for delegated work.
- Implementations conforming to v0.002 continue to read AECX-064 as their delegation control. Implementations conforming to v0.003 or later MUST meet AEC-13 and MAY additionally adopt AECX-064.

Control statement
- Parent agents SHOULD delegate only within explicit task, cost, and time boundaries in addition to the authority boundaries required by AEC-13. Delegated agents that may affect R3/R4 actions MUST inherit or receive stricter approval, logging, revocation, and receipt requirements than the parent task.

Supplemental guidance
- Delegation should not expand authority by changing context, environment, identity, workspace, or tool availability. AEC-13 governs granted authority; this guidance covers the indirect paths that grant nothing explicitly yet widen what the delegated agent can reach.
- Delegated agents should carry parent correlation IDs so decisions and effects remain reconstructable.
- Parent agents should be accountable for delegated work unless governance assigns a different accountable owner.

Assessment objectives
- Confirm delegation boundaries are declared before delegated work begins.
- Confirm delegated agents cannot exceed parent-approved scope.
- Confirm receipts preserve parent/delegated-agent correlation.

Assessment methods
- Examine: delegation plans, task boundaries, receipts, tool policies, cost/time caps.
- Interview: workflow owners and operators.
- Test: attempt delegation that exceeds tool, data, cost, time, or authority limits.

Receipts
- Delegation plan
- Parent/delegated-agent correlation logs
- Boundary enforcement evidence
- Revocation or cancellation test
