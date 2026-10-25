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

## Remaining Work (v0.002 refresh)

- [x] Confirm naming/versioning for the next DAS-1 release. Resolved 2026-08-20: v0.003, see tasks/decisions.md.
- [x] Decide the status of domain overlays for the current release. Resolved at v0.002: Informative, documentation-only.
- [ ] Decide which additional platform overlays are in scope beyond OpenClaw, Claude Code, Codex, Cursor, and Kiro.
- [ ] Add policy snapshot/tool catalog examples for Codex-specific evidence if stronger sample completeness is desired.
- [ ] Add conformance claims for domain overlays only after legal/regulatory/policy review expectations are finalized.
- [ ] Package changes into reviewable PRs or commits by layer.

## v0.003 (see spec/roadmap/v0.003-enterprise-load-findings.md)

- [x] Core normative deltas: AEC-13, AEC-14, Annex A, tightened AEC-10, M8/M9, D3/D4.
- [x] Reconcile AECX-064 and AECX-067 so delegation and budget are not stated twice at two strengths.
- [x] Schemas: delegation-record, classification-register, and additive fields on receipt/drill/tool-catalog/claim.
- [x] Verifier: `--das-version` gate, AEC-13/AEC-14/AEC-10/Annex A checks, D3/D4 outcome checks, two new artifact verifiers.
- [x] Draft evidence pack under das1/examples/v0003/ plus a v0.003 claim packet.
- [x] Negative tests proving every new check fires, gated in CI.
- [x] Conformance criteria, checklist, scorecard, badge guidance, and README updated for the two-version state.
- [ ] Re-examine the five platform overlays against AEC-13 and AEC-14. None currently declares an autonomy ladder or a delegation boundary in overlay terms.
- [ ] Decide whether domain overlays need AEC-14 classification guidance before they graduate from Informative.
- [ ] Second independent enterprise adoption to confirm or falsify the findings (section 8 of the backlog). v0.003 stays Draft until then.
- [ ] Release decision: promote v0.003 from Draft, or withdraw it as implementation defects.

## Verification Plan

- Planning artifact check: confirm `tasks/todo.md`, `tasks/context.md`, `tasks/decisions.md`, and `tasks/lessons.md` exist and link to the refresh spec.
- Structure check: confirm the refresh spec names goals, non-goals, assumptions, domain scope, task list, acceptance criteria, verification plan, and rollback plan.
- Repository check: run `git diff --check`.
- Future implementation checks: run existing DAS-1 verifier commands for core plus every changed overlay, then add overlay-specific proof bundles.

## Rollback Plan

- Planning-only rollback: remove `spec/roadmap/agent-skills-refresh-spec.md` and the new `tasks/` artifacts if the direction is rejected.
- Implementation rollback: keep each future layer in a separate reviewable change so core, catalog, overlays, schemas, examples, and verifier updates can be reverted independently.

## Breach review, October 2026 (see spec/roadmap/2026-10-breach-review.md)

- [x] Map 34 public incidents to the AEC that applies. Every in-scope incident is an implementation failure; no spec change (decision 2026-10-25).
- [ ] Review the section 4 overlay guidance against each platform overlay and the MCP profile, as part of the AEC-13/14 re-examination above.
- [ ] Decide which candidate new platform overlays are in scope (Copilot, Gemini CLI/Antigravity, agentic browsers, M365 Copilot, Amazon Q/Bedrock AgentCore).
- [ ] Crosswalks in mappings/: OWASP Agentic Top 10 (2026), IMDA agentic framework, NIST CAISI, CSA AICM v1.1. Confirm the official OWASP category names first.
- [ ] Example evidence expires about 2026-12-18 (54 days on 2026-10-25); run tools/refresh_and_verify.sh before then.

## Regulated overlays: HIPAA, SOC 2, PCI, FedRAMP High (2026-10-25)

- [x] Crosswalks in mappings/regulated/ (hipaa, soc2-tsc, pci-dss-v4, fedramp-high), each recording framework state and how far citations were checked.
- [x] Overlays in overlays/regulated/ (hipaa, soc2, pci rewritten, fedramp-high) with tightenings by AEC, drills, and namespaced receipt fields.
- [ ] Verify citations against official text the automated pass could not reach: PCI DSS v4.0.1 PDF and the PCI AI supplement, AICPA TSP Section 100 and TQA 9561, the FedRAMP High OSCAL profile.
- [ ] Watch list: HIPAA Security Rule final rule (estimated July 2027); next PCI DSS version after the 2026 RFC; FedRAMP 20x Class D pilot; NIST SP 800-53 agent overlays; AICPA/AIUC-1 joint engagement.
- [ ] Decide whether regulated overlays get example evidence and verifier plugins, or stay documentation-only.
