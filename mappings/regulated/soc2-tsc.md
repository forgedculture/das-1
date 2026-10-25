# DAS-1(TM) to SOC 2 (Trust Services Criteria) crosswalk

Status: Informative, draft. Checked 2026-10-25.

Mappings translate DAS-1 artifacts to other frameworks. They do not change DAS-1
conformance, and this one does not establish a SOC 2 opinion. The hardening itself is in
`overlays/regulated/soc2/`.

## Framework state on 2026-10-25

- **Criteria.** The current criteria are the AICPA 2017 Trust Services Criteria (With Revised
  Points of Focus – 2022), TSP Section 100.
  - The 2022 revision changed points of focus, not criteria.
  - Points of focus are guidance, not requirements.
  - No newer TSC or exposure draft was found.
- **Description criteria.** 2018 SOC 2 Description Criteria (With Revised Implementation
  Guidance – 2022).
- **AI guidance.** AICPA TQA Section 9561, *SOC Examinations: Effect of the Service
  Organization's Use of AI on SOC 1 and SOC 2 Examinations* (2026-09-11).
  - It is nonauthoritative.
  - As summarized publicly, it adds no criteria and no report type.
  - It treats a third-party AI provider like any other subservice organization.
  - The text itself is behind an AICPA login and was not read for this file.
- **AIUC-1.** On 2026-10-19 the AICPA and AIUC announced a joint SOC 2 plus AIUC-1 agent
  certification engagement. It is in pilot, with launch expected in early 2027.

## How to read this

- SOC 2 is outcome-based. An organization writes its own control activities and maps them
  to the criteria.
- DAS-1 controls are candidate control activities. Where SOC 2 has no analog (AEC-04,
  AEC-10, the composition part of AEC-14), they sit under CC5.1 to CC5.3 as the entity's own
  activities.
- Criterion titles were checked against secondary copies of the 2017 TSC, because the AICPA
  text is login-gated. Verify against TSP Section 100 before relying on this.
- AEC-13 and AEC-14 are v0.003 Draft controls.

## Crosswalk

| DAS-1 control | Trust Services Criteria (representative) | Relationship |
|---|---|---|
| AEC-01 Tool catalog and ownership | CC1.3 structures and authorities; CC2.1 quality information; CC3.2 risk identification; CC6.1 logical access security architecture; CC9.2 vendor and business partner risk | The catalog is the inventory the system description and CC6.1 rely on. Third-party tools and model providers fall under CC9.2. |
| AEC-02 Least privilege and time bounding | CC6.1; CC6.2 registration and authorization before credentials are issued; CC6.3 role-based access, least privilege, removal | Strong overlap. Agent identities belong in the same access reviews as people. |
| AEC-03 Human gating for high-risk actions | CC5.2 technology general controls; CC5.3 policies and procedures; CC6.3; CC8.1 authorized changes; PI1.3 system processing | The R3/R4 gate is a control activity. Its approval records are the operating-effectiveness evidence. |
| AEC-04 Approval latency budget | None | DAS-1 addition; written as an entity control under CC5.1. |
| AEC-05 Revocation kill switch and drill | CC6.3 removal of access; CC7.4 incident response; CC7.5 recovery; CC4.1 separate evaluations; A1.3 recovery testing | Partial. The drill is a separate evaluation under CC4.1. |
| AEC-06 Preflight plan and declared blast radius | CC3.2; CC3.4 changes affecting internal control; CC8.1; PI1.2–PI1.3 | Partial. A per-action preflight is stricter than system-level risk assessment. |
| AEC-07 Audit trail completeness | CC7.2 monitoring for anomalies; CC7.3 evaluating events; CC4.1; CC2.1; PI1.3–PI1.5 | Strong overlap. The receipt log is the population the auditor samples. |
| AEC-08 Data class boundaries | C1.1 identifying confidential information; C1.2 disposal; CC6.1; CC6.6 external threats; CC6.7 transmission and movement; P3–P4 and P6 where Privacy is in scope | Strong overlap where Confidentiality or Privacy is in scope. |
| AEC-09 Secrets lifecycle and rotation | CC6.1; CC6.2; CC6.3; CC6.7 | Strong overlap. |
| Agent component integrity (catalog AECX-060, AECX-068) | CC6.8 unauthorized or malicious software; CC7.1 configuration and vulnerability monitoring; CC9.2 | Skills, MCP servers and fetched code are software under CC6.8. Drift in standing instructions is a CC7.1 configuration change. |
| AEC-10 Cost attribution and caps | None (A1.1 capacity only loosely) | DAS-1 addition. |
| AEC-11 Exceptions register and expiry | CC3.4; CC4.2 deficiencies evaluated and communicated; CC5.3 | Partial. An expired, unremediated exception is a deviation the auditor will report. |
| AEC-12 Tool-call incident annex and exercises | CC7.3; CC7.4; CC7.5; CC2.3 external communication; P6 breach notification where Privacy is in scope | Strong overlap. |
| AEC-13 Delegation envelope (Draft) | CC6.3; CC1.3; CC9.2 | Partial. The TSC assume privileged actions trace to an accountable person or a service account. Delegation chains are the entity's own control. |
| AEC-14 Classification and composition (Draft) | Classification: CC3.2, CC5.1; CC3.3 fraud risk for autonomous action. Composition: none | DAS-1 addition. |

## What SOC 2 needs that DAS-1 does not name

- A system description that covers agents, the tools they use, and the subservice
  organizations behind them (the Description Criteria).
- Evidence of operating effectiveness across the whole observation period (Type II), not
  only at a point in time.
- Completeness and accuracy of information produced by the entity: the auditor will test
  that the receipt log is complete before sampling from it.
- Complementary user entity controls (CUECs) stated in the report, for the customer-side
  controls the entity relies on.
- Criteria with no DAS-1 control: CC1.4 competence, CC6.4 physical access, A1.2
  environmental protection and backup, P1–P2, P5, P7 and P8.
- Disclosure of significant system incidents in the system description (Description Criteria), which covers agent incidents.

## Where DAS-1 is stricter than SOC 2

- A risk-class trigger model for approval (AEC-03). SOC 2 leaves the trigger model to the
  entity.
- A per-action preflight (AEC-06).
- Time-bounded grants (AEC-02).
- A drill cadence for revocation (AEC-05).
- Approval latency (AEC-04) and cost caps (AEC-10).
- Delegation and composition (AEC-13 and AEC-14, Draft).
