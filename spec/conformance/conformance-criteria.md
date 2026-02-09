# Conformance criteria (DAS-1(TM) v0.001)

An implementation MAY claim "DAS-1(TM) v0.001 Conformant" only if:
- All AEC controls are implemented OR explicitly excepted with expiry (AEC-11).
- D1 and D2 have been executed within the last 90 days.
- Metrics M1-M4 are measurable from stored receipts.

Exception handling note
- Expired exceptions SHOULD be retained for historical evidence and audit reconstruction.
- Expired exceptions are not applicable for the current conformance period.

Overlay conformance note
- Overlay claims are additive. Implementations MAY claim core conformance without an overlay claim.
- If an overlay claim is made, overlay-specific drills and evidence requirements also apply.

Recommended evidence package
- Tool catalog export
- Approval logs + latency metrics
- Drill reports for D1 and D2 with timestamps and evidence references
- Audit completeness sample pack
- Cost attribution coverage report
- Exceptions register with expiries
- Tool-call IR annex + tabletop record
