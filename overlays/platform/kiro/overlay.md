# DAS-1(TM) Kiro overlay v0.002 (Informative)

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Prevent authority crossing in Kiro-style spec-driven agent workflows where steering files, specs, hooks, MCP servers, task execution, shell commands, and workspace automation can become real execution authority.
- Keep Kiro-specific requirements in this overlay so the DAS-1 core and generic AECX controls remain vendor-neutral and technology-neutral.

Threat assumptions
- Steering files, specs, generated requirements/design/tasks, hooks, and AGENTS.md files can persistently steer behavior across sessions and task execution.
- Kiro specs turn requirements into executable tasks; errors or malicious instructions in requirements/design/tasks can cross into implementation authority.
- Agent hooks can run prompts or shell commands on file, prompt, agent lifecycle, tool-use, or spec-task events.
- MCP servers can expose tools with variable trust and broad capabilities.
- Workspace and global steering precedence can cause unexpected overrides if not inventoried and reviewed.

Tightens
- AEC-03: classify as R3/R4 any action that executes shell commands, changes git remotes, pushes code, mutates auth/config, invokes privileged MCP tools, runs hooks with side effects, executes spec tasks affecting production or regulated data, exfiltrates data, or writes outside approved workspace boundaries; require explicit pre-execution human approval.
- AEC-05: revocation kill switch must disable active sessions, spec task execution, hooks, shell/tool execution, MCP authority, and queued/background work quickly and verifiably.
- AEC-06: preflight must include workspace root, active steering scope, spec id, task id, hook id when applicable, target repository/ref, requested capability, autonomy mode, and rollback/containment plan.
- AEC-07: receipts must bind proposal, active steering/spec/task/hook context, approval, execution, command/tool/hook outcomes, and downstream effects.
- AEC-08: isolate sessions by task, workspace, repository, branch/worktree, steering scope, spec, hook, connector identity, and MCP server.
- AEC-09: scope secrets, MCP servers, hooks, local credentials, global steering, and external connectors to least privilege; support independent rotation and revocation.
- AEC-11: emergency exceptions for approvals, steering, hooks, MCP/tools, task execution, networking, or workspace boundaries are time-bounded and expire by default.

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

Kiro runtime baseline
- Workspace steering under `.kiro/steering/`, global/team steering under `~/.kiro/steering/`, foundational steering files such as `product.md`, `tech.md`, `structure.md`, and supported `AGENTS.md` files must be inventoried and reviewed by scope.
- Steering inclusion modes, file-match patterns, workspace-vs-global precedence, and AGENTS.md always-included behavior must be declared and evidenced.
- Specs must preserve requirements, design, and tasks as reviewable artifacts before execution.
- Hooks must be inventoried with trigger, file pattern, tool name, action type, prompt/command, owner, review status, and revocation path.
- Reviewed steering and approved specs must load before task execution; lower-authority global/user steering, generated hooks, or unreviewed specs must not override high-impact policy.
- Shell commands, hook commands, privileged MCP/tool calls, git egress, and CI/CD-affecting spec tasks require explicit user confirmation or stronger approval according to risk class.
- R3/R4 and production-impacting actions require explicit human approval before execution; production-impacting actions require two-person review.
- In trusted low-risk contexts, policy-conformant R1/R2 tasks should execute autonomously to preserve usefulness.

Overlay drills
- D-KIRO-01 Steering precedence and inclusion test
  - Pass: reviewed workspace/global steering and AGENTS.md files load according to declared precedence and inclusion mode; lower-authority or unreviewed steering cannot override high-impact policy.
  - Output: steering inventory, load-order evidence, conflict logs, blocked override receipts.
- D-KIRO-02 Spec task execution gate test
  - Pass: spec requirements/design/tasks remain reviewable before execution; R3/R4 spec tasks require approval and are blocked otherwise.
  - Output: spec artifacts, approval receipts, blocked task execution logs.
- D-KIRO-03 Hook side-effect containment test
  - Pass: hooks that run prompts or shell commands cannot perform R3/R4 side effects without approval and receipt capture.
  - Output: hook inventory, trigger logs, blocked command receipts.
- D-KIRO-04 MCP/tool boundary test
  - Pass: untrusted MCP tools are denied by default; allowed tools remain scoped to server/task/spec boundaries.
  - Output: MCP policy evaluation logs and receipts.
- D-KIRO-05 Revocation readiness and post-revoke block test
  - Pass: revocation disables active/queued sessions, hooks, spec task execution, and MCP/tool authority; subsequent high-risk actions tied to revoked authority are blocked.
  - Output: revocation timeline and failed reuse evidence.

Operational risk closure requirements
- For R3/R4 allow receipts, `overlay_context.kiro` MUST include `session_id`, `task_id`, `workspace_root`, `cwd`, `invocation_id`, `git_repo`, `git_ref`, `policy_snapshot_ref`, and `tool_catalog_ref`.
- For R3/R4 allow receipts, `overlay_context.kiro.steering_refs` MUST identify active workspace/global steering, foundational steering, and AGENTS.md artifacts when applicable.
- For R3/R4 allow receipts involving specs, hooks, MCP/tools, shell commands, or CI/CD effects, `overlay_context.kiro.authority_surface_refs` MUST identify owner, source/version, review status, execution boundary, approval requirement, and revocation path.
- R3/R4 spec-task receipts MUST include `spec_ref`, `requirements_ref`, `design_ref`, `tasks_ref`, and `task_execution_ref`.
- R3/R4 hook receipts MUST include `hook_id`, `trigger_type`, `action_type`, and `hook_review_ref`.
- R3/R4 receipts MUST include `change_control_ref` and `supervision_mode=user-confirmed`.
- If `production_impact=true`, receipts MUST include `two_person_review=true`, `secondary_approver_id`, and `rollback_pointer`.
- Overlay evidence must include at least one low-risk (`R1` or `R2`) allow receipt to prove useful throughput remains intact.

Verifier mapping (informative)
- A verifier plugin may be added at `tools/overlays/kiro.py` and run via `verify-overlay --overlay kiro`.
- Normative claim requirements should be defined in `overlays/platform/kiro/conformance.md` before public overlay claims are made.
