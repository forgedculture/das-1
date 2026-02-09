# Conformance criteria (DAS-1(TM) v0.001)

An implementation MAY claim "DAS-1(TM) v0.001 Conformant" only if:
- All AEC controls are implemented OR explicitly excepted with expiry (AEC-11).
- D1 and D2 have been executed within the last 90 days.
- Metrics M1-M7 are measurable from stored receipts.

Exception handling note
- Expired exceptions SHOULD be retained for historical evidence and audit reconstruction.
- Expired exceptions are not applicable for the current conformance period.

Overlay conformance note
- Overlay claims are additive. Implementations MAY claim core conformance without an overlay claim.
- If an overlay claim is made, overlay-specific drills and evidence requirements also apply.

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
