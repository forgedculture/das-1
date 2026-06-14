# AECX-064 Delegated agent control

Control statement
- Parent agents SHOULD delegate only within explicit task, data, tool, cost, time, and authority boundaries. Delegated agents that may affect R3/R4 actions MUST inherit or receive stricter approval, logging, revocation, and receipt requirements than the parent task.

Supplemental guidance
- Delegation should not expand authority by changing context, environment, identity, workspace, or tool availability.
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
