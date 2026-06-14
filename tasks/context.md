# DAS-1 Agent + Skills Refresh Context

## Current Objective

Build a specification and task list to refresh DAS-1 for the current agent ecosystem: agents now execute through standing instruction artifacts, skills, tool brokers, connectors, subagents, coding-agent shells, hosted automations, and workflow runners rather than only prompt-to-tool patterns.

## Constraints

- Follow repository instruction: plan first, persist truth in task files, and do not claim completion without proof.
- Keep this pass planning-focused and reviewable.
- Do not change the closed set of 12 core AEC controls without explicit review.
- Keep core AEC and generic AECX control language vendor-neutral and technology-neutral.
- Put concrete vendors, runtimes, protocols, file names, settings paths, and product behaviors in overlays or mappings.
- Do not add/remove dependencies, alter CI/CD, or change security policy without explicit confirmation.
- Treat healthcare, law, finance, voting/elections, government, and military as high-impact domains requiring domain-specific overlays or mappings.
- Treat steering docs, custom instructions, rulesets, memories, personalizations, and workflow customizations as governed artifacts when they load by default or define how agents act.
- Use minimal diffs and keep normative changes separate from roadmap/specification work.

## Assumptions

- "Vote" means voting/elections and election administration systems.
- "Government" covers civilian public-sector services, benefits, procurement, records, public safety support, and administrative decision systems.
- "Military" covers defense, intelligence-adjacent, mission systems, logistics, cyber operations, and command-support workflows; lethal force or targeting authority must remain explicitly out of autonomous scope unless a future reviewed profile defines an even stricter prohibited/controlled boundary.
- Business includes enterprise operations, HR, procurement, sales, support, finance operations, and operational decision workflows.
- DAS-1 should remain runtime-agnostic while adding platform overlays where concrete tools create distinct authority hazards.

## Locked Decisions

- Use `spec/roadmap/agent-skills-refresh-spec.md` as the first planning spec.
- Keep core controls closed at 12 in this pass; add new detail through glossary, catalog controls, profiles, overlays, schemas, examples, and verifier plugins.
- Keep AEC/AECX controls generic. Apply named technologies, vendors, files, settings, and tool behaviors through overlays.
- Treat skills as executable authority bundles when they include instructions, helper scripts, templates, connectors, or external tool access.
- Treat coding agents as delegated-authority systems whenever they can edit files, run commands, invoke tools, change repository state, or affect CI/CD.
- Treat standing instruction artifacts as the preferred default governance mechanism over repeated prompting, provided they are reviewed, scoped, versioned, and loaded predictably.
- Track concrete tool-specific names only inside platform overlays, not in core/AEC/AECX control intent.

## Authoritative Files

- `README.md`
- `spec/core/das-1-core.md`
- `spec/core/glossary.md`
- `spec/conformance/conformance-criteria.md`
- `catalog/index.md`
- `overlays/README.md`
- `overlays/platform/claude-code/overlay.md`
- `overlays/platform/openclaw/overlay.md`
- `overlays/regulated/pci/overlay.md`
- `tools/overlays/README.md`

## Acceptance Criteria

- A refresh spec exists and addresses agents, standing instruction artifacts, skills, tool brokers/connectors, coding agents, delegated agents, autonomy modes, receipts, drills, and conformance.
- The spec requires governance for default load, precedence, review, conflict handling, and override control in generic terms.
- Vendor-specific and technology-specific details are assigned to overlays.
- The spec explicitly covers business, healthcare, law, finance, voting/elections, government, and military.
- The task list is actionable and split by implementation layer.
- Verification and rollback plans are documented.
- No normative core or verifier behavior is changed in this planning pass.

## Verification Plan

- Inspect created files for structure and links.
- Run `git diff --check`.
- Summarize proof and residual risks before claiming the planning pass complete.

## Progress And Proof

- 2026-05-19: Added generic glossary terms for agents, autonomy mode, connectors, delegated agents, skills, standing instruction artifacts, and tool brokers.
- 2026-05-19: Added generic catalog controls AECX-060 through AECX-069 and updated the catalog index.
- 2026-05-19: Verified generic glossary/catalog layer with `git diff --check`.
- 2026-05-19: Verified no concrete vendor/tool names appear in `spec/core/glossary.md`, `catalog/index.md`, or `catalog/controls/`.
- 2026-05-19: Expanded the Claude Code platform overlay for standing instruction, skill, subagent, command, hook, and MCP configuration governance.
- 2026-05-19: Added a Codex platform overlay with `AGENTS.md`, workspace, shell/git, plugin/connector, browser/computer-use, CI/CD, approval, and revocation requirements.
- 2026-05-19: Added high-impact domain overlays for business, healthcare, law, finance, voting/elections, government, and military/defense.
- 2026-05-19: Reviewed evidence schemas; existing `overlay_context` namespacing supports the new overlay evidence fields without schema changes in this slice.
- 2026-05-19: Added `tools/overlays/codex.py` verifier plugin and expanded `tools/overlays/claude_code.py` for D-CC-10/D-CC-11 and standing-instruction evidence.
- 2026-05-19: Added Codex example R1/R3 receipt pack and D1/D2 plus D-CX-01 through D-CX-11 drill reports.
- 2026-05-19: Updated Claude Code R3 receipt example and added D-CC-10/D-CC-11 drill reports.
- 2026-05-19: Added Codex conformance claim example and updated README/conformance docs/checklist for Codex/domain overlay discoverability.
- 2026-05-19: Verified Codex overlay with `python3 tools/das1_verify.py verify-overlay --receipts das1/examples/codex/receipt_packs --exceptions das1/examples/exceptions --drills das1/examples/codex/drills --tool-catalogs das1/examples/tool_catalogs --policy-snapshots das1/examples/policy_snapshots --ir-annexes das1/examples/ir_annexes --overlay codex --report codex-overlay-report.json`.
- 2026-05-19: Verified expanded Claude Code overlay with `python3 tools/das1_verify.py verify-overlay --receipts das1/examples/claude-code/receipt_packs --exceptions das1/examples/exceptions --drills das1/examples/claude-code/drills --tool-catalogs das1/examples/tool_catalogs --policy-snapshots das1/examples/policy_snapshots --ir-annexes das1/examples/ir_annexes --overlay claude-code --drill-max-age-days 365 --report claude-code-overlay-report.json`.
- 2026-05-19: Verified conformance claims with `python3 tools/das1_verify.py verify-claims das1/examples/claims --report claims-report.json`.
- 2026-05-19: Updated badge usage, scorecard, and core changelog with additive overlay claim rules and refresh summary.
- 2026-05-19: Refreshed core example D1/D2 drill timestamps and core claim disclosure to keep seed example conformance inside the 90-day evidence window.
- 2026-05-20: Added Cursor and Kiro platform overlay drafts and updated README, overlay index, changelog, and task list.
- 2026-06-14: Included catalog controls AECX-050 through AECX-052 and registered the NIST SP 800-53 Rev. 5 crosswalk in mappings.

## Next Actions

- Review `spec/roadmap/agent-skills-refresh-spec.md`.
- Decide whether the next release should be `v0.002`, `v0.1`, or a named preview profile.
- Confirm which platform overlays are in scope after the existing platform overlays.
- Confirm whether domain artifacts should be overlays, mappings, or both.
- Decide whether domain overlays need verifier plugins in this release or remain informative documentation with future evidence packs.
