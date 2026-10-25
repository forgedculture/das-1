# DAS-1(TM) to FedRAMP High crosswalk

Status: Informative, draft. Checked 2026-10-25.

Mappings translate DAS-1 artifacts to other frameworks. They do not change DAS-1
conformance, and this one does not establish a FedRAMP certification. The hardening itself
is in `overlays/regulated/fedramp-high/`.

This file adds the FedRAMP High layer on top of `mappings/nist-800-53-r5.md`, which maps
AEC-01 to AEC-12 to base 800-53 controls. It lists the control enhancements that matter most
for agents in a High system.

## Framework state on 2026-10-25

- **FedRAMP Consolidated Rules for 2026 (CR26).**
  - Certification "classes" replace impact-level labels. Rev5 Class D includes the current
    High baseline.
  - FedRAMP says classes are not strict one-for-one replacements for Low, Moderate and High.
    This file treats High as Rev5 Class D.
  - Optional adoption from 2026-07-04. Mandatory from 2027-01-01. The Class D rule for
    validated cryptographic modules also has a grace period to 2027-06-01.
  - Sources:
    - https://www.fedramp.gov/2026/agencies/use/classes/
    - https://www.fedramp.gov/notices/0004/
- **The control catalog** is NIST SP 800-53 Rev 5.2.0 (OSCAL, modified 2026-05-11). Release
  5.2.0 (2025-08-27) added SA-15(13), SA-24 and SI-2(7). None of these appears in a FedRAMP
  baseline. Source: https://www.fedramp.gov/2026/reference/controls/
- **FedRAMP 20x does not cover Class D yet.** A pilot is expected late 2026 to early 2027.
  New Rev5 certifications are accepted until 2027-06-11. Source:
  https://www.fedramp.gov/2026/timeline/
- **Changes for Class D under CR26:**
  - Collaborative Continuous Monitoring: an Ongoing Certification Report every 3 months, plus
    a quarterly review.
  - Vulnerability detection and response is rated by potential agency impact (PAIN 1 to 5).
    This replaces the old 30/90/180-day POA&M timelines.
  - Incidents are reported to FedRAMP by PAIN rating, with initial reports due in 15 minutes
    to 1 hour (section "Where FedRAMP High is stricter" below).
- **AI-specific rules:**
  - Significant change rules classify adding models to an approved AI service as *adaptive*.
  - A new third-party AI service, or training on federal data, is *transformative*.
  - FedRAMP's AI prioritization (2025-08 to 2026-04) certified several enterprise LLM
    services. No LLM service authorized at Class D was found.
- **NIST's SP 800-53 overlays for AI systems.** The project page is
  https://csrc.nist.gov/projects/cosais.
  - It plans single-agent and multi-agent overlays.
  - Only a predictive-AI outline had been published by this date.
  - Reconcile this file when the agent overlays appear.
- **OMB M-25-21** sets minimum practices for "high-impact AI", meaning AI whose output is a
  principal basis for decisions with legal, material or significant effect. They include
  human oversight, intervention and a fail-safe where practicable. They bind agencies, and
  they reach providers through contracts (M-25-22).

## How to read this

- "D" means the control is in the High (Class D) baseline but not Moderate. "C,D" means it is
  in both. "B,C,D" means it is in all classes B to D.
- Membership comes from the CR26 control pages on fedramp.gov, not from the raw OSCAL
  profile, which could not be retrieved. Re-check against the official FedRAMP High
  baseline before relying on it.
- AEC-13 and AEC-14 are v0.003 Draft controls.

## Crosswalk: High-relevant enhancements

| DAS-1 control | Base 800-53 (see nist-800-53-r5.md) | High enhancements that bind agents |
|---|---|---|
| AEC-01 Tool catalog and ownership | CM-8, CM-2, PM-5 | CM-8(2) automated inventory maintenance (D); CM-8(4) accountability information (D); CM-7(5) authorized software by allow-list (C,D); SA-9 external system services (B,C,D); SA-9(2) identification of functions, ports, protocols and services (C,D) |
| AEC-02 Least privilege and time bounding | AC-6, AC-2, AC-3 | AC-2(11) usage conditions (D); AC-2(12) atypical usage monitoring and AC-2(13) disabling high-risk accounts (C,D); AC-6(1), (2), (5), (9), (10) (C,D); AC-6(3) network access to privileged commands (D); AC-6(8) privilege levels for code execution (D); IA-5(13) expiry of cached authenticators (D) |
| AEC-03 Human gating for high-risk actions | AC-3, CM-3, CM-5 | AU-10 non-repudiation (D), which binds each approval to the approver (its FedRAMP parameter lists approval among the covered actions); IA-2(1)–(2) MFA for approvers (B,C,D); AT-3 role-based training (B,C,D); CM-3(1) automated change documentation, notification and prohibition (D); CM-5(1) automated access enforcement and audit records (C,D); SC-3 security function isolation (D), which keeps the gate outside the agent's reach |
| AEC-04 Approval latency budget | none | DAS-1 addition |
| AEC-05 Revocation kill switch and drill | AC-2, IR-3 | IR-4(2) dynamic reconfiguration (D); AC-2(13) (C,D); IR-3(2) coordination with related plans (C,D) |
| AEC-06 Preflight plan and declared blast radius | CM-4, RA-3, CM-3 | CM-4(1) separate test environments (D); CM-3(2) testing, validation and documentation of changes (C,D) |
| AEC-07 Audit trail completeness | AU-2, AU-3, AU-12, AU-9 | AU-9(2) audit backup on a separate system (D); AU-9(3) cryptographic protection (D); AU-12(1) system-wide, time-correlated trail (D); AU-12(3) changes by authorized individuals (D); AU-5(1)–(2) storage capacity warning and real-time alerts on audit failure (D); AU-6(5) integrated analysis of audit records, AU-6(6) correlation with physical monitoring, AU-6(7) permitted actions (D) |
| AEC-08 Data class boundaries | RA-2, AC-4, SC-7, SC-28 | SC-7(10) prevent exfiltration (D); SC-7(20) dynamic isolation (D); SC-7(21) isolation of system components (D); AC-4(4) flow control of encrypted information (D); SC-28(1) (B,C,D); SA-9(5) processing and storage location (C,D) |
| AEC-09 Secrets lifecycle and rotation | IA-5, SC-12, SC-28 | SC-12(1) key availability (D); IA-5(8) multiple accounts (D); CMVP-validated cryptographic modules (FedRAMP rule, MUST for Class D) |
| AEC-10 Cost attribution and caps | SC-6 (in no FedRAMP baseline) | DAS-1 addition |
| AEC-11 Exceptions register and expiry | CA-5, RA-3 | CR26 vulnerability rules replace POA&M timelines. The DAS-1 exception register travels with the quarterly Ongoing Certification Report. |
| AEC-12 Tool-call incident annex and exercises | IR-8, IR-4, IR-3, IR-6 | IR-4(4) information correlation (D); IR-4(6) insider threats (D), which treats a compromised agent as an insider; IR-4(11) integrated response team (D); IR-2(1)–(2) simulated events and automated training (D); IR-5(1) automated tracking (D) |
| AEC-13 Delegation envelope (Draft) | AC-6, SA-9 | CA-3(6) data transfer authorizations, a partial analog only (D); SA-9(1)–(2) (C,D); SR-6 supplier assessments (C,D) |
| AEC-14 Classification and composition (Draft) | RA-2, RA-3 | SI-4(11) outbound communications analysis (D); SI-10 information input validation (C,D), the anchor for untrusted content; SI-4(20) privileged users (D); SI-4(22) unauthorized network services (D); SA-17 developer security architecture (D) |
| Component integrity (AEC-01, AECX-068) | SI-7, SR family | SI-7(15) code authentication (D); SR-9 tamper resistance (D); SA-4(5) system, component and service configurations (D) |

## Where FedRAMP High is stricter than DAS-1

- **Incident reports to FedRAMP** go by potential agency impact (PAIN) rating. An unrated
  incident defaults to PAIN-5.

  | | PAIN-3 to 5 | PAIN-2 | PAIN-1 |
  |---|---|---|---|
  | Initial report | 15 minutes | 1 hour | 1 hour |
  | Ongoing report | 3 hours | 6 hours | 24 hours |

  An agent tool-call incident that may affect federal data is reportable. Source:
  https://www.fedramp.gov/2026/reference/rev5/d/incident-evaluation-and-communication/
- **Validated cryptography.** CMVP-validated modules are required for Class D (Rev5, from
  2027-01-01).
- **Data location.** Processing and storage stay in U.S. locations or locations under U.S.
  jurisdiction (SA-9(5)). This includes any hosted model provider that sees federal data.
- **Significant change notice for AI services.**
  - Adaptive changes, such as adding a model to an approved AI service: notice within 10
    business days after.
  - Transformative changes, such as a new third-party AI service or training on federal
    data: notice 30 business days before, 10 business days before, and 5 after.
- **Continuous monitoring.** An Ongoing Certification Report every 3 months, plus a quarterly
  review.

## Where DAS-1 is stricter than FedRAMP High

- Per-action approval for R3/R4 (AEC-03). 800-53 leaves the trigger model to tailoring. Its closest analogs, AC-3(2) and CM-5(4) dual authorization, are in no FedRAMP baseline.
- Approval latency (AEC-04) and cost caps (AEC-10). SC-6 is in no baseline.
- A per-agent revocation drill with a measured time-to-revoke (AEC-05).
- Composition (AEC-14, Draft).
