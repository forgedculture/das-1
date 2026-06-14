# DAS-1 Agent + Skills Refresh Task List

Goal: update DAS-1 for the 2026 agent operating model: agentic execution, reusable skills, standing instruction artifacts, tool-broker ecosystems, coding agents, and regulated/high-impact domains, while keeping all core/AEC control language vendor-neutral and technology-neutral.

Non-goals:
- Do not rewrite the 12 core AEC controls until the refresh spec is reviewed.
- Do not add dependencies, CI changes, or verifier changes in this planning pass.
- Do not claim conformance coverage for new domains until evidence formats and drills are implemented.

## Steps

- [x] Inventory current DAS-1 core, overlays, profiles, catalog, and regulated mapping structure.
- [x] Capture constraints, assumptions, acceptance criteria, and verification plan in `tasks/context.md`.
- [x] Record initial locked decisions in `tasks/decisions.md`.
- [x] Draft the agent-and-skills refresh specification in `spec/roadmap/agent-skills-refresh-spec.md`.
- [x] Create an implementation task list covering business, healthcare, law, finance, voting/elections, government, and military domains.
- [x] Add explicit generic coverage for steering docs, customizations, personalizations, memories, rulesets, and default instruction artifacts.
- [x] Lock the architecture rule that vendor-specific and technology-specific details belong in overlays, not core AEC/AECX control intent.
- [ ] Review the refresh spec with stakeholders and confirm naming/versioning for the next DAS-1 release.
- [ ] Split accepted work into small PR-sized changes by layer: core deltas, catalog controls, platform overlays, domain overlays, schemas, examples, verifier, docs.
- [x] Update glossary for agents, skills, standing instruction artifacts, delegated agents, tool brokers, connectors, receipts, and autonomy modes using generic language.
- [x] Add or revise catalog controls for skill provenance, standing instruction governance, tool broker policy, subagent delegation, context/secret containment, identity-scoped connectors, and approval artifact integrity.
- [x] Add platform overlays that name each tool's default rule/customization files and how they must be loaded, reviewed, and overridden.
- [ ] Add platform overlays for current coding and agent runtimes beyond existing coverage. (Added OpenClaw, Claude Code, Codex, Cursor, and Kiro; decide whether more are in scope.)
- [x] Add regulated/high-impact domain overlays or mappings for business, healthcare, law, finance, voting/elections, government, and military.
- [ ] Extend evidence schemas only after overlay evidence fields are finalized. (Reviewed: current `overlay_context` schema supports namespaced overlay evidence; no schema change required for the Codex verifier slice.)
- [ ] Add example receipt packs, drill reports, tool catalogs, policy snapshots, and conformance claims for each accepted overlay. (Started: Codex receipt/drill examples and claim added; Claude Code examples updated for D-CC-10/D-CC-11.)
- [ ] Extend verifier plugins and machine checks for accepted overlays. (Started: Codex verifier added; Claude Code verifier expanded for D-CC-10/D-CC-11.)
- [x] Update README, conformance docs, checklist, and badge guidance after implementation.

## Remaining Work

- [ ] Review the refresh spec with stakeholders and confirm naming/versioning for the next DAS-1 release.
- [ ] Decide which additional platform overlays are in scope beyond OpenClaw, Claude Code, Codex, Cursor, and Kiro.
- [ ] Add verifier plugins and example evidence for accepted domain overlays, or explicitly mark them as documentation-only overlays for the current release.
- [ ] Add policy snapshot/tool catalog examples for Codex-specific evidence if stronger sample completeness is desired.
- [ ] Add conformance claims for domain overlays only after legal/regulatory/policy review expectations are finalized.
- [ ] Package changes into reviewable PRs or commits by layer.

## Verification Plan

- Planning artifact check: confirm `tasks/todo.md`, `tasks/context.md`, `tasks/decisions.md`, and `tasks/lessons.md` exist and link to the refresh spec.
- Structure check: confirm the refresh spec names goals, non-goals, assumptions, domain scope, task list, acceptance criteria, verification plan, and rollback plan.
- Repository check: run `git diff --check`.
- Future implementation checks: run existing DAS-1 verifier commands for core plus every changed overlay, then add overlay-specific proof bundles.

## Rollback Plan

- Planning-only rollback: remove `spec/roadmap/agent-skills-refresh-spec.md` and the new `tasks/` artifacts if the direction is rejected.
- Implementation rollback: keep each future layer in a separate reviewable change so core, catalog, overlays, schemas, examples, and verifier updates can be reverted independently.
