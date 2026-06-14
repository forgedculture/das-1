# Domain overlays

Domain overlays describe how DAS-1(TM) tightens for high-impact operating contexts.

Status: Informative (documentation-only)
- All domain overlays in this directory are Informative. They are documentation-only.
- They are NOT machine-verified and are NOT part of the DAS-1(TM) v0.002 conformance claim set.
- The claimable overlay set is the platform overlays (for example: codex, claude-code, openclaw), each of which ships a verifier plugin and a conformance/claim packet. Domain overlays do not, yet.
- Why documentation-only: regulated fields (healthcare, law, finance, voting/elections, government, military) require real legal, regulatory, and policy review. Publishing machine-checkable "conformance" for them without that review would over-claim. Until a domain has been through real review and has a verifier plus evidence, it stays guidance only.

The 7 domains
- `business/`: enterprise operations, HR, procurement, customer operations, support, and internal workflows.
- `healthcare/`: healthcare administration, PHI boundaries, patient communications, chart operations, claims, and clinical-accountability boundaries.
- `law/`: legal research, drafting, matter management, e-discovery, privilege, client communications, and filings.
- `finance/`: banking, payments, trading support, ledgers, lending, insurance, treasury, compliance operations, and financial advice workflows.
- `voting-elections/`: election administration support, voter registration workflows, ballot logistics, public information, reporting support, audits, and election operations.
- `government/`: civilian public services, benefits, permits, procurement, records, public communications, enforcement support, and administrative decision systems.
- `military/`: defense administration, logistics, readiness, cyber defense support, intelligence-support workflows, mission planning support, and command-support systems.

Rule
- Domain overlays may tighten core controls and add catalog controls.
- Domain overlays must not weaken core controls.
- Domain overlays do not replace legal, regulatory, policy, or mission-specific compliance review.
- Normative force comes from the DAS-1(TM) core and the applicable platform overlay, not from a domain document.

How they layer
- A domain overlay is read on top of a system that is already DAS-1(TM) v0.002 Conformant (core) and conformant to the applicable platform overlay (for example codex, claude-code, openclaw).
- Core and the platform overlay carry the verifiable, claimable requirements. The domain overlay adds operating-context guidance (threat assumptions, tightenings, runtime baseline, drills, and suggested receipt fields) for that context.
- Using a domain overlay does not create a domain conformance claim. There is no "DAS-1(TM) v0.002 Conformant + <domain>" claim. See `spec/conformance/badge-usage.md` and `spec/conformance/conformance-criteria.md`.

Precedent
- These overlays are Informative in the same sense as `mappings/` (see `mappings/README.md`): they translate or contextualize DAS-1(TM) for another frame without becoming normative or claimable on their own.

Bar to graduate a domain to verified
A domain overlay graduates from Informative to a verifiable, claimable overlay only after all of the following exist, matching what a platform overlay already ships (see `overlays/platform/codex/` for the reference shape):
- Domain review: documented review by qualified domain legal, regulatory, clinical, or policy experts for that field, recorded as evidence.
- Verifier plugin: an `overlay.yaml` registering the overlay (requires core, applies_to, tightens, adds, drills, conformance_doc) so `tools/das1_verify.py` can check it.
- Conformance/claim packet: a normative `conformance.md` defining the exact additive claim string, required drills and assertions, and required receipt provenance bindings.
- Example evidence pack: example drill reports, receipts, and a passing verifier report (cf. `das1/examples/`).
- Claim packet: the additive claim with required disclosures, including domain review status, per `spec/conformance/badge-usage.md`.

Until all of the above exist for a domain, that domain remains Informative and MUST NOT be presented as DAS-1(TM) conformance.

Caveat
- Not legal, regulatory, clinical, or policy advice. Using a domain overlay does not establish compliance for that field and MUST NOT be claimed as DAS-1(TM) conformance.
