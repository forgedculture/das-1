# AECX-061 Skill execution boundary

Control statement
- Skills SHOULD declare allowed tools, data classes, file or object scopes, network destinations, helper execution paths, and forbidden actions. Skills that can influence R3/R4 actions MUST be blocked when their execution boundary is missing, ambiguous, expired, or exceeded.

Supplemental guidance
- A skill boundary should describe what the skill may read, write, invoke, transform, emit, and retain.
- Boundary declarations should be evaluated before tool execution, not only after completion.
- Helper scripts and generated artifacts should inherit the skill boundary unless a narrower boundary is declared.

Assessment objectives
- Confirm skills declare enforceable boundaries.
- Confirm boundary violations are denied and logged.
- Confirm boundary changes require review appropriate to the highest affected risk class.

Assessment methods
- Examine: skill manifests, policy snapshots, denied action receipts, boundary change records.
- Interview: skill maintainers and policy owners.
- Test: attempt disallowed file/object, tool, data, or destination access through a skill.

Receipts
- Skill boundary manifest
- Policy evaluation logs
- Denied execution receipts
- Boundary change approval record
