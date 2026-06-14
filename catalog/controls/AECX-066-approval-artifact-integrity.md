# AECX-066 Approval artifact integrity

Control statement
- Approval artifacts SHOULD be attributable, action-scoped, time-bounded, tamper-evident, and correlated to execution receipts. R3/R4 execution MUST be blocked when approval artifacts are missing, expired, mismatched, replayed, or outside approved scope.

Supplemental guidance
- Approval should bind to the actual action, target, risk class, data class, blast radius, and execution window.
- Broad session approval should not authorize materially different high-risk actions unless the scope explicitly covers them.
- Approval artifacts should be auditable without relying on chat memory or operator recollection.

Assessment objectives
- Confirm approvals are attributable and linked to execution.
- Confirm approval scope is specific enough to detect mismatches.
- Confirm expired, replayed, or altered approvals are rejected.

Assessment methods
- Examine: approval records, execution receipts, policy snapshots, integrity logs.
- Interview: approvers, operators, auditors.
- Test: attempt execution with missing, stale, altered, replayed, and scope-mismatched approvals.

Receipts
- Approval artifact
- Approval-to-execution correlation record
- Integrity verification evidence
- Rejected approval test logs
