# AECX-069 Standing instruction governance

Control statement
- Standing instruction artifacts SHOULD have owners, scope, precedence rules, source, version or integrity evidence, review status, conflict handling, default-load evidence, and revocation path. Standing instructions that can influence R3/R4 actions MUST be reviewed, loaded predictably, and prevented from being overridden by lower-authority personalizations or untrusted content.

Supplemental guidance
- Standing instruction artifacts include persistent steering documents, rule files, memories, custom instructions, personalizations, workflow defaults, and runtime policies that shape agent behavior across requests or sessions.
- Governance should define precedence across organization, project, workflow, user, directory or object scope, skill, delegated agent, and session instructions.
- Receipts should record active standing instructions for high-risk actions and regulated-domain workflows.

Assessment objectives
- Confirm standing instruction artifacts are inventoried with owner, scope, precedence, and review status.
- Confirm default-load behavior is predictable and evidenced.
- Confirm conflicts and attempted lower-authority overrides are detected, logged, and resolved according to policy.

Assessment methods
- Examine: instruction inventory, precedence policy, review records, load logs, conflict logs.
- Interview: platform owners, workflow owners, operators.
- Test: attempt unreviewed instruction loading, precedence conflicts, unauthorized personalization overrides, and revocation.

Receipts
- Standing instruction inventory
- Precedence and conflict policy
- Default-load evidence
- Override denial or conflict-resolution logs
