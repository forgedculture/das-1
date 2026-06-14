# AECX-065 Context and memory containment

Control statement
- Agent context, memory, retrieval, and summarization SHOULD preserve task, principal, data-class, and authority boundaries. Sensitive data, secrets, regulated data, and untrusted instructions MUST NOT cross into unauthorized sessions, memories, skills, tools, or delegated agents.

Supplemental guidance
- Containment applies to short-term context, long-term memory, retrieval indexes, task summaries, handoffs, logs, embeddings, and generated artifacts.
- Context compaction and summarization should not remove policy constraints, approvals, or open risks needed for safe execution.
- Untrusted content should retain provenance when it influences proposals or tool decisions.

Assessment objectives
- Confirm context and memory boundaries are documented and enforced.
- Confirm sensitive or untrusted content cannot leak across unauthorized scopes.
- Confirm compaction/handoff preserves active constraints and approval state.

Assessment methods
- Examine: memory policy, retrieval scope maps, handoff records, redaction rules, leakage test results.
- Interview: platform owners, workflow owners, data stewards.
- Test: attempt cross-task, cross-principal, cross-domain, and post-revoke memory access.

Receipts
- Context boundary policy
- Memory/retrieval scope map
- Leakage test evidence
- Handoff or compaction sample
