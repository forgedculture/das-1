# AECX-067 Autonomous change budget

Control statement
- Autonomous actions SHOULD have explicit budgets for spend, write volume, rate, retry count, blast radius, data movement, and elapsed time. Autonomous actions that exceed budget MUST stop, alert, or require approval before continuing.

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
