# DAS-1(TM) to HIPAA crosswalk

Status: Informative, draft. Checked 2026-10-25.

Mappings translate DAS-1 artifacts to other frameworks. They do not change DAS-1
conformance, and this one does not establish HIPAA compliance. The hardening itself is in
`overlays/regulated/hipaa/`.

## Framework state on 2026-10-25

- **The current rule governs.** The definitions in 45 CFR Part 160 (Subparts A and C), the Security Rule (45 CFR 164 Subpart C), the Privacy Rule
  (Subpart E) and the Breach Notification Rule (Subpart D) are in force as currently
  codified.
- **The Security Rule NPRM (RIN 0945-AA22, 90 FR 898, 2025-01-06) is neither final nor
  withdrawn.**
  - The Unified Agenda lists it as a long-term action, with final action estimated for July
    2027.
  - Its proposals bind no one yet:
    - removing the addressable/required distinction;
    - mandatory MFA and encryption;
    - a technology asset inventory and network map;
    - 72-hour restoration;
    - annual compliance audits;
    - business associates verifying their safeguards.
  - They are marked "NPRM" below.
- **AI-related:**
  - The Section 1557 rule at 45 CFR 92.210 requires reasonable efforts to identify and
    mitigate discrimination risk in patient care decision support tools. Its enforcement
    status in 2026 is unconfirmed.
  - ONC's HTI-1 decision-support transparency requirements (45 CFR 170.315(b)(11)) are
    proposed for narrowing in HTI-5 (2025-12).
  - No OCR guidance specific to AI and HIPAA was found.

## How to read this

- R means required implementation specification. A means addressable: implement it, or
  document why not and what was done instead.
- Citations were checked against eCFR text dated 2026-10-20, and reviewed again on 2026-10-25.
- AEC-13 and AEC-14 are v0.003 Draft controls.

## Crosswalk

| DAS-1 control | HIPAA (representative) | Relationship |
|---|---|---|
| AEC-01 Tool catalog and ownership | 164.308(a)(2) assigned security responsibility; 164.308(a)(1)(ii)(A) risk analysis (R); 164.310(d)(2)(iii) accountability (A); NPRM: technology asset inventory | HIPAA requires a responsible official and a risk analysis covering every system holding ePHI. DAS-1 makes the agent's tool surface an inventoried, owned item. |
| AEC-02 Least privilege and time bounding | 164.308(a)(3)(ii)(A)–(C) authorization and supervision, clearance, termination (A); 164.308(a)(4)(ii)(B)–(C) access authorization, establishment and modification (A); 164.312(a)(2)(i) unique user identification (R); 164.312(a)(2)(iii) automatic logoff (A); 164.312(d) person or entity authentication; 164.502(b) and 164.514(d) minimum necessary | Strong overlap. An agent needs its own identity (unique user ID), and minimum necessary governs what it may see. |
| AEC-03 Human gating for high-risk actions | Partial: 164.308(a)(4) access authorization; 164.508 authorizations for uses and disclosures; 45 CFR 92.210 Section 1557 discrimination-risk mitigation (not HIPAA) | HIPAA has no per-action approval. DAS-1's R3/R4 gate supplies it. |
| AEC-04 Approval latency budget | None (nearest: 164.312(a)(2)(ii) emergency access procedure (R)) | DAS-1 addition. The emergency access procedure is the fallback when approval cannot be reached. |
| AEC-05 Revocation kill switch and drill | 164.308(a)(3)(ii)(C) termination procedures (A); 164.308(a)(6)(ii) response and reporting (R); 164.308(a)(7)(ii)(C) emergency mode operation (R); 164.308(a)(7)(ii)(D) testing and revision (A) | Partial. HIPAA requires termination and contingency procedures; a tested per-agent kill switch is DAS-1's. |
| AEC-06 Preflight plan and declared blast radius | 164.308(a)(1)(ii)(A)–(B) risk analysis and risk management (R); 164.308(a)(8) evaluation; 164.306(e) maintenance | Partial. HIPAA analyzes risk at system level; DAS-1 requires it per R3/R4 action. |
| AEC-07 Audit trail completeness | 164.312(b) audit controls; 164.308(a)(1)(ii)(D) information system activity review (R); 164.308(a)(5)(ii)(C) log-in monitoring (A); 164.312(c)(1)–(2) integrity and authentication of ePHI; 164.528 accounting of disclosures; 164.316(b)(2)(i) six-year retention of required documentation | Strong overlap. HIPAA does not set an audit-log retention period. Six years applies to required documentation, and whether that covers log data is a judgement for the entity. |
| AEC-08 Data class boundaries | 164.502(b) and 164.514(d) minimum necessary; 164.514(a)–(c) de-identification; 164.312(a)(2)(iv) encryption and decryption (A); 164.312(e)(1)–(2) transmission security, integrity, encryption (A); 164.502(e) and 164.504(e) disclosures to business associates | Strong overlap. ePHI is DAS-1's highest data class in this context, and minimum necessary applies to what an agent ingests. |
| AEC-09 Secrets lifecycle and rotation | 164.308(a)(5)(ii)(D) password management (A); 164.312(d) authentication; 164.312(a)(2)(iv) encryption | Partial. HIPAA does not specify key or credential lifecycle; DAS-1 does. |
| AEC-10 Cost attribution and caps | None | DAS-1 addition. |
| AEC-11 Exceptions register and expiry | 164.306(d)(3) documenting addressable decisions; 164.316(b) documentation | Partial. HIPAA documents addressable decisions; DAS-1 adds an expiry. The NPRM would remove the addressable route. |
| AEC-12 Tool-call incident annex and exercises | 164.308(a)(6) security incident procedures (R); 164.308(a)(7)(ii)(D) testing (A); 164.400–414 breach notification; 164.530(f) mitigation | Strong overlap. DAS-1 adds the tool-call annex; HIPAA adds the breach risk assessment and notification clocks. |
| AEC-13 Delegation envelope (Draft) | 164.308(b)(1) and 164.314(a) business associate contracts; 164.502(e)(1)(ii) subcontractor assurances; 164.504(e)(2)(ii)(D) flow-down to subcontractors; 160.103 subcontractor as business associate | Analogy at contract level. HIPAA flows restrictions down a chain of organizations; DAS-1 flows them down a chain of agents. |
| AEC-14 Classification and composition (Draft) | None (weak: 164.308(a)(1)(ii)(A), 164.514(d)) | DAS-1 addition. |

## Where HIPAA is stricter than DAS-1

- **Business associate agreements.** A vendor or platform that creates, receives, maintains
  or transmits ePHI for the entity is a business associate (160.103). A BAA is required
  before ePHI reaches it.
  - This includes a model provider or agent platform.
  - The conduit exception covers transmission only, not storage or processing.
- **Breach clocks.**
  - Individuals are notified without unreasonable delay, and no later than 60 calendar days
    from discovery (164.404).
  - The media are notified for breaches affecting more than 500 residents of a State
    (164.406).
  - The Secretary is notified (164.408).
  - A business associate notifies the covered entity within 60 days (164.410), or sooner
    under its contract.
- **Breach presumption.** An impermissible use or disclosure is presumed a breach unless a
  documented four-factor risk assessment shows a low probability of compromise (164.402).
- **Documentation retention.** Six years from creation or last effective date
  (164.316(b)(2)(i)).

## Where DAS-1 is stricter than HIPAA

- Per-action approval for R3/R4 (AEC-03).
- A per-action preflight (AEC-06).
- Time-bounded grants (AEC-02).
- A measured revocation drill (AEC-05).
- Approval latency (AEC-04) and cost caps (AEC-10).
- Composition (AEC-14, Draft).
