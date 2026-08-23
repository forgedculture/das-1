# Change log (DAS-1(TM) core)

## v0.003 (unreleased, core deltas drafted 2026-08-20)

Source: control-by-control review while building a full enterprise agentic operating model on v0.002 (spec/roadmap/v0.003-enterprise-load-findings.md).

- Reopened the core, which had been closed at 12 controls since v0.001, to add two controls. AEC-01 through AEC-12 are neither weakened nor renumbered, so existing v0.002 conformance claims remain valid against v0.002.
- Added AEC-13 Delegation envelope and cascading revocation: the subset rule, a delegation record per delegation, cascading revocation within the AEC-05 budget, and delegation lineage reconstructable to the human principal.
- Added AEC-14 Action classification and composition: named classification ownership, reclassification triggers, the composition rule for sequences whose composed effect exceeds any individual action's class, and a stated higher-class default on ambiguity.
- Tightened AEC-10 (renamed to "Cost attribution and enforced caps") so the enforcement obligation cannot be read as satisfied by a spend forecast or a reporting-layer control. Caps now require execution-path enforcement, a named owner, and a documented raise path.
- Added Annex A, Autonomy levels: a normative A0-A5 autonomy dimension crosswalked to R1-R4, with the binding rule that effective authority is the intersection of autonomy level and risk ceiling rather than the maximum, and that promotion along the autonomy axis MUST NOT raise a registered risk ceiling.
- Added metrics M8 (cap enforcement rate) and M9 (delegation cascade completion time).
- Added drills D3 (delegation cascade) and D4 (cap breaker).
- Reconciled AECX-064 and AECX-067 with the core so delegation and budget obligations are not stated twice at two different strengths.
- Added schemas/delegation-record.schema.json (AEC-13) and schemas/classification-register.schema.json (AEC-14), and extended the receipt, drill-report, tool-catalog, and conformance-claim schemas with the fields the new controls need. All additions are optional at the schema layer, so v0.002 evidence still validates.
- Extended tools/das1_verify.py with a `--das-version` gate defaulting to v0.002. v0.003 adds the AEC-13 subset and cascade checks, the AEC-14 composition checks, the tightened AEC-10 enforcement checks, Annex A autonomy checks, D3/D4 outcome checks, and two new artifact verifiers. Claim packets are gated by their own declared das_version.
- Added das1/examples/v0003/, a draft evidence pack covering delegation lineage, a cascade revocation, a worked composition case, a cap breaker block, and D1-D4.
- Added tools/test_v0003_checks.py: 22 negative tests that mutate the passing fixtures into specific violations and assert each check fires. Wired into the conformance gate.
- Updated conformance criteria, checklist, scorecard, badge guidance, and README for the two-version state.
- Still outstanding for v0.003: platform and domain overlays have not been re-examined against AEC-13/AEC-14, and no overlay declares an autonomy ladder. No implementation may claim v0.003 conformance while the version is Draft.

## v0.002 (2026-06-14)
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
