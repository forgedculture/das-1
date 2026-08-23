# AECX-067 Autonomous change budget

Relationship to core
- As of DAS-1(TM) v0.003, AEC-10 requires that spend caps on R3/R4 workflows be enforced in the execution path, carry a named owner and a documented raise path, and be exercised by drill D4.
- AECX-067 remains the extended control for the budget dimensions the core does not denominate in currency: write volume, rate, retry count, blast radius, data movement, and elapsed time.
- Where a budget in this control governs an R3/R4 workflow, the AEC-10 enforcement obligation applies to it: a forecast or reporting-layer control does not satisfy it.

Control statement
- Autonomous actions SHOULD have explicit budgets for write volume, rate, retry count, blast radius, data movement, and elapsed time, in addition to the spend caps required by AEC-10. Autonomous actions that exceed budget MUST stop, alert, or require approval before continuing.

Supplemental guidance
- Budgets should be risk-proportional and tied to owner, workflow, environment, and data class.
- Retry loops and background automations should be included because they can amplify otherwise small actions.
- Budget exhaustion should fail safely for high-risk work while preserving bounded low-risk utility where policy allows.

Assessment objectives
- Confirm autonomous budgets are defined and enforced.
- Confirm budget decisions are logged and attributable.
- Confirm over-budget actions stop, alert, queue, or require approval as designed.

Assessment methods
- Examine: budget policies, workflow configuration, cost/rate logs, alert records.
- Interview: workflow owners and operations staff.
- Test: exceed spend, rate, retry, write-volume, and time budgets.

Receipts
- Budget policy
- Budget utilization logs
- Over-budget block or approval receipts
- Alert or queue evidence
