# DAS-1 Agent + Skills Refresh Spec

Status: Planning draft
Date: 2026-05-19

## 1. Goal

Refresh DAS-1 for the modern agent stack: agentic coding tools, reusable skills, tool brokers/servers, connectors, subagents, hosted automations, workflow runners, and domain-specific high-impact deployments.

The update should make DAS-1 useful for organizations moving from "prompt governance" to delegated-authority governance: who or what can act, through which tools, under which risk class, with what approval, revocation, audit, and rollback evidence.

## 2. Non-goals

- Do not replace the existing 12 AEC controls in this planning pass.
- Do not put vendor-specific or technology-specific requirements in the DAS-1 core, AEC controls, or generic catalog control intent.
- Do not make DAS-1 vendor-specific; concrete products, runtimes, protocols, file names, and settings belong in overlays or mappings.
- Do not treat prompt text alone as the governance unit when skills, tools, connectors, and execution sandboxes carry the real authority.
- Do not claim new domain conformance until domain evidence, drills, examples, and verifier checks exist.

## 3. Why DAS-1 Needs The Refresh

The risk surface has moved:

- Agents now complete tasks across files, tools, browsers, terminals, APIs, and SaaS connectors.
- Skills package reusable instructions, scripts, templates, assets, and domain workflows that can quietly become execution policy.
- Standing instruction artifacts now replace repeated prompting: steering docs, project rules, memories, personal instructions, customizations, and workflow files shape default behavior across sessions.
- Tool protocols and brokered tool servers make tool discovery and invocation portable, but also expand the number of authority-bearing endpoints.
- Coding agents can read repositories, edit files, run commands, use brokered tools, interact with repository control systems, and influence CI/CD.
- Subagents and background automations can split authority across contexts, worktrees, queues, and approval surfaces.
- High-impact domains need stronger defaults than generic enterprise automation.

## 4. External Reference Baseline

This planning draft was checked against current public documentation and should be refreshed again before normative release:

- Anthropic describes Claude Code as an agentic coding tool that can work in a terminal, edit code, run commands, and use MCP integrations.
- Anthropic describes Claude Code extension surfaces including `CLAUDE.md`, skills, subagents, hooks, commands, MCP, and settings.
- Anthropic Agent Skills package reusable capability instructions and supporting files, with automatic invocation when relevant.
- OpenAI Codex documents repo-scoped `AGENTS.md` guidance for coding agents.
- Cursor documents project rules in `.cursor/rules`, user rules, `AGENTS.md`, and legacy `.cursorrules`.
- GitHub Copilot documents repository instructions in `.github/copilot-instructions.md`, path-specific `.github/instructions/*.instructions.md`, and personal instructions.
- Gemini CLI documents hierarchical context files named `GEMINI.md`.
- Cline documents rules in `.clinerules/`; Continue documents rules in `.continue/rules`; Windsurf documents Rules, Memories, and Workflows.
- MCP defines a common tool exposure and invocation layer for model clients and servers.

These references are overlay inputs only. They must not leak concrete vendor or technology names into generic AEC control statements.

Reference URLs:
- https://docs.claude.com/en/docs/agents-and-tools/claude-code/overview
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- https://code.claude.com/docs/en/features-overview
- https://github.com/openai/codex/blob/main/docs/agents_md.md
- https://docs.cursor.com/en/context
- https://docs.github.com/en/copilot/concepts/response-customization
- https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html
- https://docs.cline.bot/customization/cline-rules
- https://docs.continue.dev/customize/rules
- https://windsurf.com/university/general-education/intro-rules-memories
- https://modelcontextprotocol.io/specification/2024-11-05/server/tools

## 5. Proposed Architecture

Keep DAS-1 layered:

- Core: retain the 12 AEC controls and keep all control intent vendor-neutral and technology-neutral.
- Glossary: add modern agent-stack terms using generic language; put concrete product names in overlays.
- Catalog controls: add optional AECX controls for new authority hazards, written generically.
- Platform overlays: encode runtime-specific hardening for concrete tools, ecosystems, file names, settings, and protocols.
- Domain overlays: encode high-impact requirements for regulated or sensitive sectors.
- Mappings: translate DAS-1 to external frameworks without changing requirements.
- Schemas/examples/verifier: make evidence machine-checkable after overlay requirements settle.

Design rule:
- Any vendor-specific or technology-specific term is prohibited in core AEC requirements and generic AECX control statements unless it is only an example clearly marked informative.
- Concrete tools, products, protocols, configuration files, settings paths, and named ecosystems are applied through overlays.

## 6. Core Clarifications To Consider

These are candidates for later review, not approved normative edits:

- Define an agent as any system that can choose or sequence actions using tools, connectors, workflows, or code execution.
- Define a skill as an authority-bearing capability package when it includes executable instructions, helper scripts, templates, connectors, tool manifests, or operational policy.
- Define a standing instruction artifact as any persistent project, user, organization, workflow, or runtime customization that is loaded by default or selected by policy to steer agent behavior.
- Clarify that tool calls include direct and indirect invocations through execution environments, automation systems, external connectors, tool brokers, hosted workflows, and delegated agents.
- Clarify that approval must bind to the exact action scope, not merely to a broad session or vague objective.
- Clarify that revocation must cover skills, standing instruction artifacts, connectors, tool brokers, delegated agents, sessions, credentials, queues, and background jobs.

## 7. Proposed New Catalog Controls

- AECX-060 Skill provenance and review: skills have owners, versions, source, review status, allowed domains, and expiry/review cadence.
- AECX-061 Skill execution boundary: skills declare allowed tools, data classes, file paths, network destinations, helper scripts, and forbidden actions.
- AECX-062 Tool broker policy enforcement: tool brokers enforce identity, risk class, data class, approval, logging, and revocation before invocation.
- AECX-063 Connector and account boundary: external connectors are scoped to user/workflow identity, least privilege, tenant or boundary, data class, and revocation path.
- AECX-064 Subagent delegation control: parent agents can delegate only within explicit task, data, tool, budget, and time boundaries.
- AECX-065 Context and memory containment: cross-task memory, retrieval, and context compaction cannot leak secrets, regulated data, or untrusted instructions across authority boundaries.
- AECX-066 Approval artifact integrity: approvals are tamper-evident, action-scoped, time-bounded, attributable, and correlated to execution receipts.
- AECX-067 Autonomous change budget: autonomous actions have per-agent budget caps for spend, write volume, rate, blast radius, and retry loops.
- AECX-068 Agent supply-chain control: models, extensions, skills, tool endpoints, execution images, standing instructions, and helper scripts have source, integrity, review, and update evidence.
- AECX-069 Standing instruction governance: steering docs, rule files, memories, custom instructions, personalizations, and workflow customizations have owners, precedence rules, scope, review status, conflict handling, and default-load evidence.

## 8. Standing Instruction And Customization Surfaces

DAS-1 should explicitly govern the rule layer that agents follow by default. These artifacts are not "just prompts" when they persist across sessions, apply automatically, or encode operational policy.

Minimum requirements:
- Each standing instruction artifact has owner, scope, source, version/hash, review status, allowed domains, expiry/review cadence, and revocation path.
- Each tool profile declares precedence order across organization, user, project, directory/path, skill, subagent, and session instructions.
- Conflicts are resolved deterministically, logged, and reviewable.
- High-impact defaults cannot be changed by local personalizations without approval.
- Agents must load and follow the approved default rule set before relying on ad hoc repeated prompting.
- Receipts record which standing instruction artifacts were active for R3/R4 actions and regulated-domain workflows.

Generic control requirements stay above. Known tool surfaces are overlay-specific examples and must be implemented only in platform overlays:

| Tool/ecosystem | Standing instruction/customization names to govern |
| --- | --- |
| Claude Code | `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/skills/*/SKILL.md`, `.claude/agents/*`, hooks, commands, MCP configuration, skill overrides |
| OpenAI Codex / Codex CLI | `AGENTS.md` and scoped/nested `AGENTS.md` files |
| Cursor | `.cursor/rules`, User Rules, `AGENTS.md`, legacy `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, personal instructions, editor/IDE custom instruction settings |
| Gemini CLI | `GEMINI.md` hierarchical context files and imported context files |
| Windsurf | Rules, Memories, Workflows |
| Cline | `.clinerules/` and related workspace rule files |
| Continue | `.continue/rules`, Hub rules, local rules, custom system-message configuration |
| Aider and similar CLI agents | convention/context files passed by read-only flags or project command wrappers, such as `CONVENTIONS.md` |

Future platform overlays should name the exact files/settings they govern and prove that the approved defaults load before task execution. The core and AECX catalog should refer only to the generic standing-instruction class.

## 9. Platform Overlay Backlog

Existing overlays:

- Claude Code: keep and expand for skills, hooks, subagents, MCP server trust, standing instruction files, and CI boundary evidence.
- OpenClaw: keep and expand for gateway and sandbox hardening.

Candidate new overlays:

- OpenAI Codex / Codex CLI: scoped instruction files, workspace containment, shell approval, git/PR authority, browser/computer-use authority, plugin/connector authority, and task handoff receipts.
- Cursor / IDE coding agents: editor trust, project/user rules, background edits, terminal authority, extension supply chain, and workspace indexing.
- GitHub Copilot coding agent / PR agents: issue-to-PR authority, repo permissions, branch protection, CI execution, and reviewer/merge gates.
- MCP server ecosystem: server identity, tool naming collisions, tool manifest review, broker enforcement, connector scoping, and revocation.
- Browser/computer-use agents: authenticated session scope, click/type authority, file upload/download, payment/action confirmation, and visual spoofing resistance.
- Workflow automations: scheduled/background jobs, retries, queues, idempotency, human wakeups, and post-revoke drain behavior.

## 10. Domain Coverage

### Business

Scope: enterprise operations, HR, procurement, sales, support, finance operations, internal analytics, and customer operations.

Key hazards:
- Unauthorized contract, hiring, firing, pricing, refund, procurement, customer-account, or data-export actions.
- Agent spend loops and SaaS connector overreach.
- Unreviewed skills becoming de facto operating procedures.

Required work:
- Business operations overlay or profile.
- Connector/account boundary control examples.
- Spend and procurement approval drills.
- Customer/account data export receipts.

### Healthcare

Scope: clinical operations support, revenue cycle, patient communications, insurance workflows, records workflows, and care-team administration.

Key hazards:
- PHI exposure, unsafe clinical advice, unauthorized chart modification, inappropriate patient messaging, insurance/claims errors, and emergency escalation failures.

Required work:
- Healthcare overlay with PHI data-class boundaries.
- Explicit clinical decision support boundary and human clinician accountability.
- Patient communication approval classes.
- Drills for PHI egress, chart-write gate, and emergency escalation handoff.

### Law

Scope: legal research, drafting, matter management, e-discovery, client communications, filings, privilege review, and contract workflows.

Key hazards:
- Privilege waiver, unauthorized practice of law, missed filing deadlines, hallucinated citations, client-confidential data leaks, and unsupervised legal advice.

Required work:
- Legal services overlay.
- Matter/client data segmentation.
- Citation and authority verification receipts.
- Filing and client-send approval gates.
- Privilege breach drill.

### Finance

Scope: banking, payments, trading support, accounting, lending, insurance, treasury, compliance operations, and financial advice workflows.

Key hazards:
- Unauthorized transfers/trades, market-impact actions, fraud, unsuitable advice, ledger mutation, nonpublic data leakage, and weak audit reconstruction.

Required work:
- Finance overlay beyond PCI.
- Transaction/trade approval gates.
- Ledger write receipts and reconciliation proof.
- Market/nonpublic information boundary.
- Fraud and sanctions screening connector controls.

### Voting/Elections

Scope: election administration support, voter registration workflows, ballot logistics, public information, election-night reporting support, audits, and campaign-adjacent systems when they touch election operations.

Key hazards:
- Voter suppression or misinformation, registration changes, ballot chain-of-custody failures, tabulation/reporting errors, unauthorized public communications, and partisan manipulation.

Required work:
- Voting/elections overlay.
- Prohibit autonomous voter eligibility, ballot, tabulation, certification, or official-result changes.
- Two-person approval for public election communications and operational changes.
- Chain-of-custody receipts for election artifacts.
- Drills for misinformation injection, registration-write block, reporting correction, and revocation during election operations.

### Government

Scope: civilian public services, benefits, permits, procurement, records, casework, public communications, public safety support, and administrative decision systems.

Key hazards:
- Due-process failures, biased or unappealable decisions, improper records access, unauthorized public commitments, procurement manipulation, and inaccessible public service.

Required work:
- Government services overlay.
- Public-records and retention mapping.
- Human accountability for benefits, enforcement, permit, or rights-affecting decisions.
- Appeal/review receipts.
- Public communication approval gates.

### Military

Scope: defense administration, logistics, readiness, cyber defense support, intelligence-support workflows, mission planning support, and command-support systems.

Key hazards:
- Classified data leakage, unauthorized command actions, escalation, cyber effects, targeting support misuse, supply-chain compromise, and loss of human command responsibility.

Required work:
- Military/defense overlay with strict prohibited-autonomy section.
- Classified and compartmented data boundaries.
- Two-person or command-authority approval for high-impact actions.
- No autonomous lethal force, target selection, weapons release, or strategic escalation authority.
- Drills for classified egress, command-action gate, cyber-effect containment, and revocation under degraded communications.

## 11. Evidence And Receipt Updates

Future schema work should add optional namespaced evidence for:

- `agent_context`: agent id, model/runtime, session id, autonomy mode, parent/subagent relationship, memory scope.
- `skill_context`: skill id, version, source, owner, hash, allowed tools, review status, invocation reason.
- `standing_instruction_context`: artifact ids, paths/settings, source, precedence, hash/version, scope, active/default status, conflict resolution, reviewer.
- `tool_broker_context`: broker/server id, tool manifest version, broker policy decision, identity, data class, risk class.
- `connector_context`: account, tenant, scopes, data classes, revocation path, external system.
- `approval_context`: approval artifact id, approver, scope, expiry, risk class, two-person status when required.
- `domain_context`: domain overlay id, protected data class, domain-specific human authority, prohibited action check.

## 12. Drill Backlog

- Standing instruction precedence and conflict test.
- Unauthorized personalization override test.
- Skill provenance tamper test.
- Skill helper-script boundary test.
- Tool-name collision and malicious-server test.
- Connector scope escalation test.
- Subagent delegation escape test.
- Cross-task memory leak test.
- Browser/computer-use authenticated action test.
- Background automation revocation drain test.
- Domain-specific drills listed in Section 10.

## 13. Implementation Task List

- [ ] Review this planning spec and decide release/version target.
- [ ] Update glossary with agent-stack terms, including standing instruction artifacts, steering docs, rules, memories, custom instructions, personalizations, and workflow customizations.
- [ ] Draft catalog controls AECX-060 through AECX-069.
- [ ] Add a standing-instruction governance profile that names default rule/customization files for major tools and defines precedence/override rules.
- [ ] Expand Claude Code overlay for skills, hooks, subagents, and updated MCP boundaries.
- [ ] Draft Codex/Codex CLI platform overlay.
- [ ] Draft MCP ecosystem overlay.
- [ ] Draft browser/computer-use overlay.
- [ ] Draft workflow automation overlay.
- [ ] Draft business domain overlay/profile.
- [ ] Draft healthcare domain overlay.
- [ ] Draft legal services domain overlay.
- [ ] Draft finance domain overlay.
- [ ] Draft voting/elections domain overlay.
- [ ] Draft government services domain overlay.
- [ ] Draft military/defense domain overlay.
- [ ] Update schemas for accepted `agent_context`, `skill_context`, `standing_instruction_context`, `tool_broker_context`, `connector_context`, and `domain_context` evidence.
- [ ] Add example evidence packs and claims for each accepted overlay.
- [ ] Implement or extend verifier plugins.
- [ ] Update README and conformance docs.
- [ ] Run full proof bundle and capture reports.

## 14. Acceptance Criteria

- DAS-1 can describe and verify delegated authority for agentic systems, not just direct prompt-to-tool calls.
- Skills are governed as versioned, reviewable, revocable authority packages.
- Steering docs, rule files, memories, custom instructions, personalizations, and workflow customizations are governed as standing instruction artifacts with default-load and precedence evidence.
- Tool brokers, tool servers, and external connectors are governed as authority boundaries.
- Coding agents and browser/computer-use agents have concrete overlay requirements.
- Business, healthcare, law, finance, voting/elections, government, and military each have explicit domain coverage.
- New conformance claims remain evidence-backed and machine-checkable.

## 15. Verification Plan

Planning pass:
- Confirm task artifacts exist.
- Confirm this spec covers goals, non-goals, assumptions, architecture, platform backlog, domain coverage, tasks, acceptance criteria, verification, and rollback.
- Run `git diff --check`.

Implementation pass:
- Run existing core verifier.
- Run every changed overlay verifier.
- Validate new schema examples.
- Produce conformance reports for sample claims.
- Add residual-risk notes for domains where DAS-1 maps to external law/policy but does not replace legal compliance review.

## 16. Rollback Plan

- Planning rollback: remove this roadmap spec and task artifacts.
- Normative rollback: keep future core/glossary/catalog/overlay/schema/verifier updates in separate changes so each layer can be reverted independently.
- Domain rollback: keep each domain overlay independent so disagreement about one sector does not block unrelated sectors.
