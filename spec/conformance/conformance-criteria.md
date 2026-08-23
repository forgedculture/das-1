# Conformance criteria (DAS-1(TM))

## v0.002 (current released version)

An implementation MAY claim "DAS-1(TM) v0.002 Conformant" only if:
- All AEC-01 through AEC-12 controls are implemented OR explicitly excepted with expiry (AEC-11).
- D1 and D2 have been executed within the last 90 days.
- Metrics M1-M7 are measurable from stored receipts.

## v0.003 (draft, not yet claimable)

v0.003 is additive. AEC-01 through AEC-12 are unchanged and unrenumbered, so a v0.002
claim stays valid against v0.002 and does not lapse when v0.003 releases.

An implementation will be able to claim "DAS-1(TM) v0.003 Conformant" only if, in addition
to everything required at v0.002:
- AEC-13 and AEC-14 are implemented OR explicitly excepted with expiry (AEC-11).
- D3 and D4 have been executed within the last 90 days, alongside D1 and D2.
- Metrics M1-M9 are measurable from stored receipts and drill reports.
- Delegation records exist for every delegation, and the AEC-13 subset rule is checkable
  from the records rather than asserted.
- A classification register exists naming the classification authority, the evidence basis,
  the contest resolution path, the reclassification triggers, and at least one composition
  test case.
- Every tool catalog entry carries both a risk ceiling and an autonomy level (Annex A.3).
- The AEC-10 cap is enforced in the execution path with a named owner and a raise path.

No implementation may claim v0.003 conformance while the version is Draft. The verifier
supports it (`--das-version v0.003`) so adopters can build and test evidence ahead of release.

Exception handling note
- Expired exceptions SHOULD be retained for historical evidence and audit reconstruction.
- Expired exceptions are not applicable for the current conformance period.

Overlay conformance note
- Overlay claims are additive. Implementations MAY claim core conformance without an overlay claim.
- If an overlay claim is made, overlay-specific drills and evidence requirements also apply.
- Vendor-specific, technology-specific, and domain-specific requirements MUST be applied through overlays or mappings, not by changing generic DAS-1 core control intent.
- Domain overlays are high-impact operating-context examples and do not replace legal, regulatory, policy, or mission-specific compliance review.

Utility and proportionality note
- Implementations SHOULD provide clear evidence that controls are risk-proportional and do not render R1/R2 workflows operationally inert.
- If emergency controls materially reduce R1/R2 autonomy or latency beyond targets, disclose this via an AEC-11 exception with expiry.

Recommended evidence package
- Tool catalog export
- Policy snapshot + approval latency budget evidence
- Drill reports for D1 and D2 with timestamps and evidence references
- Audit completeness sample pack
- Cost attribution coverage report
- Utility guardrail report (M5-M7 trends, blocked/queued rates by risk class, and declared target ranges)
- Exceptions register with expiries
- Tool-call IR annex + tabletop record
- Conformance claim packet including required disclosures and report references
- Overlay-specific receipt/drill packs and verifier report when an overlay claim is made
