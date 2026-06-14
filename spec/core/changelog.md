# Change log (DAS-1(TM) core)

## Unreleased
- Added a roadmap for the 2026 agent-and-skills refresh.
- Added generic glossary terms for agents, autonomy modes, connectors, delegated agents, skills, standing instruction artifacts, and tool brokers.
- Added generic AECX catalog controls AECX-050 through AECX-052 (workspace containment, git egress and remote mutation control, MCP trust segmentation) and AECX-060 through AECX-069 for skill provenance, execution boundaries, tool brokers, connectors, delegated agents, context/memory containment, approval integrity, autonomous budgets, supply chain, and standing instruction governance.
- Completed the Claude Code, Codex, Cursor, and Kiro platform overlays. Each now ships a verifier plugin, a conformance doc, an example evidence pack, and a conformance claim packet. The conformance gate verifies all five platform overlays (with OpenClaw).
- Marked the domain overlays (business, healthcare, law, finance, voting/elections, government, military/defense) as Informative (documentation-only): not machine-verified, not part of the conformance claim set, and not a substitute for domain legal, regulatory, or policy review. Added overlays/domain/README.md defining the bar to graduate a domain to verified.
- Added an informative mapping from the DAS-1(TM) core controls to NIST SP 800-53 Rev 5 (mappings/nist-800-53-r5.md).
- Added tools/refresh_example_dates.py and refreshed the example evidence dates so the suite stays within the drill-freshness window; regenerated the conformance and overlay reports.
- Updated conformance docs, checklist, scorecard, and badge guidance for additive overlay claims.

## v0.001 (2025-12-30)
- Initial draft core spec.
- Initial conformance and overlay scaffolding.
