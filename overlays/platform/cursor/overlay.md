# DAS-1(TM) Cursor overlay v0.002 (Informative)

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Prevent authority crossing in Cursor-style coding-agent workflows where reusable rules, repository instructions, editor context, terminal actions, MCP/tool calls, extension state, git operations, and background edits can become real execution authority.
- Keep Cursor-specific requirements in this overlay so the DAS-1 core and generic AECX controls remain vendor-neutral and technology-neutral.

Threat assumptions
- Repository content, docs, issues, PR text, chat context, and generated files may contain adversarial instructions.
- Project rules in `.cursor/rules`, User Rules, `AGENTS.md`, and legacy `.cursorrules` can persistently steer behavior across sessions or path scopes.
- Rule activation and file-glob scoping can accidentally include or omit authority-shaping instructions.
- Editor context, background edits, terminal commands, MCP/tool calls, extensions, and git operations can mutate local or remote systems quickly.
- Workspace indexing and retrieval can leak sensitive data across tasks or rule scopes if not bounded.

Tightens
- AEC-03: classify as R3/R4 any action that executes terminal commands, changes git remotes, pushes code, mutates auth/config, invokes privileged MCP/tools/extensions, exfiltrates indexed data, affects CI/CD, or writes outside approved workspace boundaries; require explicit pre-execution human approval.
- AEC-05: revocation kill switch must disable active sessions, terminal/tool execution, MCP authority, extension-derived authority, background edits, and queued work quickly and verifiably.
- AEC-06: preflight must include workspace root, active rule set, file/path scope, target repository/ref, requested capability, autonomy mode, and rollback/containment plan.
- AEC-07: receipts must bind proposal, active rules/instructions, approval, execution, terminal/tool/editor outcomes, and downstream effects.
- AEC-08: isolate sessions by task, workspace, repository, branch/worktree, rule scope, connector identity, and indexed context.
- AEC-09: scope secrets, MCP servers, extensions, local credentials, indexed content, and external connectors to least privilege; support independent rotation and revocation.
- AEC-11: emergency exceptions for approvals, indexing, rules, terminal, MCP/tools, extensions, networking, or workspace boundaries are time-bounded and expire by default.

Adds
- AECX-060 Skill provenance and review
- AECX-061 Skill execution boundary
- AECX-062 Tool broker policy enforcement
- AECX-063 Connector and account boundary
- AECX-064 Delegated agent control
- AECX-065 Context and memory containment
- AECX-066 Approval artifact integrity
- AECX-067 Autonomous change budget
- AECX-068 Agent supply-chain control
- AECX-069 Standing instruction governance

Cursor runtime baseline
- `.cursor/rules`, User Rules, `AGENTS.md`, and legacy `.cursorrules` must be inventoried and reviewed by scope.
- Rule activation mode, path/file globs, user-vs-project precedence, and legacy rule behavior must be declared and evidenced.
- Reviewed project rules must load before task execution for their declared scope; unreviewed or lower-authority personalizations must not override high-impact policy.
- Writes outside the declared workspace root are prohibited unless explicitly approved as R4.
- Writes, terminal execution, privileged MCP/tool calls, extension-mediated actions, git egress, and CI/CD-affecting actions require explicit user confirmation or stronger approval according to risk class.
- Background edits must be attributable, reviewable, and reversible.
- Workspace indexing/retrieval must respect task, data-class, and rule-scope boundaries.
- R3/R4 and production-impacting actions require explicit human approval before execution; production-impacting actions require two-person review.
- In trusted low-risk contexts, policy-conformant R1/R2 actions should execute autonomously to preserve usefulness.

Overlay drills
- D-CUR-01 Rule precedence and scope test
  - Pass: reviewed project/user rules load according to declared precedence and path/file scope; lower-authority personalizations and legacy rules cannot override high-impact policy.
  - Output: rule inventory, load-order evidence, conflict logs, blocked override receipts.
- D-CUR-02 Workspace/index containment test
  - Pass: workspace writes and indexed/retrieved context remain inside approved workspace, task, repository, and data-class boundaries.
  - Output: containment receipts, denied retrieval logs, index scope evidence.
- D-CUR-03 Terminal and tool gate test
  - Pass: R3/R4 terminal, MCP/tool, extension-mediated, and git actions remain proposed-only until approval.
  - Output: proposal/approval/blocked receipt chain.
- D-CUR-04 Background edit accountability test
  - Pass: background edits are attributable, reviewable, reversible, and cannot cross approved path or branch/worktree scope.
  - Output: edit receipt log, changed-files record, rollback evidence.
- D-CUR-05 Revocation readiness and post-revoke block test
  - Pass: revocation disables active/queued authority and subsequent high-risk actions tied to revoked authority are blocked.
  - Output: revocation timeline and failed reuse evidence.

Operational risk closure requirements
- For R3/R4 allow receipts, `overlay_context.cursor` MUST include `session_id`, `task_id`, `workspace_root`, `cwd`, `invocation_id`, `git_repo`, `git_ref`, `policy_snapshot_ref`, and `tool_catalog_ref`.
- For R3/R4 allow receipts, `overlay_context.cursor.rule_refs` MUST identify active `.cursor/rules`, User Rules, `AGENTS.md`, and legacy `.cursorrules` artifacts when applicable.
- For R3/R4 allow receipts involving terminal, MCP/tools, extensions, background edits, indexing, or CI/CD effects, `overlay_context.cursor.authority_surface_refs` MUST identify owner, source/version, review status, execution boundary, approval requirement, and revocation path.
- R3/R4 receipts MUST include `change_control_ref` and `supervision_mode=user-confirmed`.
- If `production_impact=true`, receipts MUST include `two_person_review=true`, `secondary_approver_id`, and `rollback_pointer`.
- Overlay evidence must include at least one low-risk (`R1` or `R2`) allow receipt to prove useful throughput remains intact.

Verifier mapping (informative)
- A verifier plugin may be added at `tools/overlays/cursor.py` and run via `verify-overlay --overlay cursor`.
- Normative claim requirements should be defined in `overlays/platform/cursor/conformance.md` before public overlay claims are made.
