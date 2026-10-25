# DAS-1(TM) to PCI DSS v4.0.1 crosswalk

Status: Informative, draft. Checked 2026-10-25.

Mappings translate DAS-1 artifacts to other frameworks. They do not change DAS-1
conformance, and this one does not establish PCI DSS compliance. The hardening itself is in
`overlays/regulated/pci/`.

## Framework state on 2026-10-25

- **Current standard:** PCI DSS v4.0.1 (June 2024).
  - The requirements that were future-dated became mandatory on 2025-03-31.
  - PCI SSC ran a request for comments on v4.0.1 from 2026-06-03 to 2026-07-20. It invited
    input "to support future technology and AI innovation". No successor version has been
    published.
- **AI guidance from PCI SSC:**
  - *Integrating Artificial Intelligence in PCI Assessments* (2025-03). It is about
    assessors using AI, not about deploying agents.
  - *AI Principles: Securing the Use of AI in Payment Environments* (2025-09-11).
  - *Security Considerations for AI Systems*, an information supplement (press release
    2026-10-07). It is guidance: where it conflicts with the standard, the standard prevails.
    It is the source of the composition and detokenize rules in the AEC-14 row below.
- **Agentic payments:** no PCI SSC publication on agent-initiated payments was found.

## How to read this

- Each AEC maps to the closest PCI DSS v4.0.1 requirements. These are representative
  anchors, not an exhaustive set.
- AEC-13 and AEC-14 are v0.003 Draft controls.
- **How the citations were checked:** the official PDF could not be retrieved for this pass.
  - The requirements quoted in bold in the "PCI is stricter" section below were checked
    against a secondary copy of the text.
  - The others follow the v4.0.1 numbering as known to the author.
  - Verify every citation against the PCI SSC document library before using this for
    assessment.

## Crosswalk

| DAS-1 control | PCI DSS v4.0.1 (representative) | Relationship |
|---|---|---|
| AEC-01 Tool catalog and ownership | 12.5.1 system component inventory; 6.3.2 inventory of bespoke and custom software and third-party components; 12.8.1 third-party service provider list; 12.8.5 responsibility matrix; 12.5.2 scope confirmation | PCI wants every in-scope component inventoried. DAS-1 adds the agent's tool, skill and connector surface with an owner and revocation path for each. |
| AEC-02 Least privilege and time bounding | 7.2.1–7.2.3 access model, job-based, approved; 7.2.5 application and system accounts; 7.2.5.1 their periodic review; 8.2.2 shared accounts by exception; 8.6.1–8.6.3 system accounts | An agent identity is an application or system account. PCI has no general time-bound requirement for grants; DAS-1 adds the TTL. |
| AEC-03 Human gating for high-risk actions | 7.2.3 privileges approved by authorized personnel; 6.5.1 change management; 6.4.3 payment page script authorization; AI supplement: human approval for actions on cleartext account data | PCI gates privilege assignment and change. DAS-1 gates each R3/R4 action. |
| AEC-04 Approval latency budget | None | DAS-1 addition. |
| AEC-05 Revocation kill switch and drill | 8.2.5 access revoked on termination; 12.10.1 incident response plan; 12.10.2 plan tested annually; AI principles: "easily disabled" | PCI requires revocation and IR testing. A per-agent kill switch with a measured time-to-revoke is DAS-1's. |
| AEC-06 Preflight plan and declared blast radius | 6.5.1–6.5.2 change impact and post-change confirmation; 12.3.1 targeted risk analysis; 12.5.2 scope confirmation on significant change | Partial. PCI analyzes changes and risk. DAS-1 requires a stored per-action preflight. |
| AEC-07 Audit trail completeness | 10.2.1 logs enabled for all components and cardholder data; 10.2.1.2 administrative actions; 10.2.2 event details; 10.3.x log protection; 10.4.1 and 10.4.1.1 daily and automated review; 10.5.1 retention; 10.6.x time sync | Strong overlap. PCI fixes retention and review cadence; DAS-1 fixes per-call content and correlation. |
| AEC-08 Data class boundaries | 1.2–1.4 network security controls and CDE segmentation; 3.3.1 no SAD after authorization; 3.4.1 PAN masked on display; 3.5.1 PAN unreadable at rest; 4.2.1 strong crypto in transmission; 7.2.6 query access to cardholder data; 11.4.5 segmentation testing; 12.10.7 PAN found where not expected | Strong overlap. Account data is DAS-1's highest data class in a payment environment. |
| AEC-09 Secrets lifecycle and rotation | 8.6.2 no hard-coded passwords in scripts, configuration or source; 8.6.3 system account passwords protected and changed; 8.3.x authentication; 3.6–3.7 key management | Strong overlap. DAS-1 extends "no hard-coded secrets" to prompts, standing instructions and skills. |
| AEC-10 Cost attribution and caps | None | DAS-1 addition. |
| AEC-11 Exceptions register and expiry | 12.3.1 targeted risk analysis; compensating controls (Appendices B and C); customized approach (Appendices D and E) | Partial. PCI documents and reviews compensating controls annually. DAS-1 adds a mandatory expiry. |
| AEC-12 Tool-call incident annex and exercises | 12.10.1 IR plan; 12.10.2 annual review and test; 12.10.4 IR training; 12.10.7 unexpected PAN; 10.7.2 failure of critical security controls detected and reported | Strong overlap. DAS-1 adds the tool-call annex and chain reconstruction. |
| AEC-13 Delegation envelope (Draft) | 7.2.5 and 8.6.x per-account scoping; 12.8.x third parties; AI supplement: split roles across agents | Partial. PCI has no delegation model; each subagent identity is its own system account. |
| AEC-14 Classification and composition (Draft) | AI supplement: do not combine sensitive-data access, external communication and untrusted input in one AI system; tokenized data plus a detokenize tool counts as access to readable data | No requirement in the standard. The supplement states the composition case directly. |

## Where PCI is stricter than DAS-1

These figures are adopted as overlay tightenings:

- **Audit logs reviewed at least once daily (10.4.1), using automated mechanisms
  (10.4.1.1).**
- **Application and system account access reviewed periodically (7.2.5.1).**
- **No hard-coded passwords in scripts, configuration or bespoke code (8.6.2).**
- **Failures of critical security control systems detected, alerted and addressed promptly
  (10.7.2).**
- **System component inventory kept current (12.5.1), and scope confirmed at least every 12
  months and on significant change (12.5.2).**
- Log retention of 12 months, with 3 months immediately available (10.5.1).
- Segmentation testing: annually for merchants (11.4.5), every 6 months for service
  providers (11.4.6).
- Third-party service providers: written agreements, annual compliance monitoring, and a
  responsibility matrix (12.8.2, 12.8.4, 12.8.5).

## Where DAS-1 is stricter than PCI

- Per-action approval for R3/R4 (AEC-03), not only approval of privilege assignment.
- Time-bounded grants (AEC-02).
- A measured revocation drill per agent (AEC-05).
- Approval latency (AEC-04) and cost caps (AEC-10).
- Delegation and composition (AEC-13 and AEC-14, Draft).
