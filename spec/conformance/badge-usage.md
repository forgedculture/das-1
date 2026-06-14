# Badge and claim usage (DAS-1(TM) v0.001)

This is a draft policy.

Allowed claim (exact)
- "DAS-1(TM) v0.001 Conformant"
- Optional additive overlay claim:
  - "DAS-1(TM) v0.001 Conformant + <overlay>"
  - Examples:
    - "DAS-1(TM) v0.001 Conformant + codex"
    - "DAS-1(TM) v0.001 Conformant + claude-code"
    - "DAS-1(TM) v0.001 Conformant + openclaw"
    - "DAS-1(TM) v0.001 Conformant + cursor"
    - "DAS-1(TM) v0.001 Conformant + kiro"

Overlay claim rules
- Overlay claims are additive and MUST NOT imply that the overlay modifies or weakens DAS-1 core controls.
- Vendor-specific, technology-specific, and domain-specific claims MUST be made through overlays or mappings, not through altered core-control wording.
- A platform overlay claim MUST reference a passing overlay verifier report where one exists.
- A domain overlay claim MUST disclose applicable legal, regulatory, policy, or mission review status. DAS-1 domain overlays do not replace that review.
- Multiple overlays MAY be named only when evidence exists for each claimed overlay.

Required disclosure
- Last drill dates (D1, D2)
- Known exceptions with expiry
- Overlay-specific drill dates when an overlay claim is made
- Overlay-specific report reference when an overlay verifier exists
- Domain review status when a domain overlay is claimed
- Non-certification statement (self-asserted conformance, not third-party certification)

Not allowed
- Claims that imply certification by maintainers or a third party.
- Claims that imply legal, regulatory, clinical, legal-services, election, government, military, or financial compliance solely because a DAS-1 domain overlay was used.
- Claims that imply a tool, vendor, model, connector, or platform is generally safe outside the stated evidence scope.
- Claims that omit active exceptions, stale drills, or material utility-impacting controls.

Recommended claim packet links
- Core conformance report
- Overlay verifier report, if applicable
- Exceptions register
- D1/D2 drill reports
- Overlay drill reports
- Tool catalog and policy snapshot
- Incident response annex
- Scorecard with M1-M7 and utility guardrails
