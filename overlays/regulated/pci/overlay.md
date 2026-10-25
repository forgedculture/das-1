# DAS-1(TM) PCI overlay v0.002 (Informative)

Status: Informative and documentation-only.

- This overlay is not machine-verified and is not part of the DAS-1(TM) v0.002 conformance
  claim set.
- It does not establish PCI DSS compliance and does not replace a QSA, ISA or SAQ
  assessment.
- Requirement numbers follow PCI DSS v4.0.1. Their checking status is in
  `mappings/regulated/pci-dss-v4.md`.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Make agent activity in, connected to, or able to affect the cardholder data environment
  (CDE) assessable under PCI DSS v4.0.1.
- Stop agents from becoming an unscoped path to account data.

Framework basis (checked 2026-10-25)
- PCI DSS v4.0.1. The future-dated requirements have been mandatory since 2025-03-31.
- PCI SSC *AI Principles* (2025-09).
- PCI SSC *Security Considerations for AI Systems*, an information supplement (press release
  2026-10-07). It is guidance; where it conflicts with the standard, the standard prevails.
  The composition and detokenize rules below come from it.
- Items marked "DAS-1 tightening" go beyond what PCI DSS itself requires.

Scoping
- Every agent, tool broker, skill and model provider falls into one PCI scoping category:
  - CDE: stores, processes or transmits account data;
  - connected-to or security-impacting: can reach CDE systems, or can administer, configure
    or read the logs of their security controls;
  - out of scope.
- The category is recorded in the agent's AEC-01 catalog entry.
- Access to tokenized or encrypted account data, together with a tool that can detokenize or
  decrypt it, counts as access to readable account data.
- A model provider that receives account data, or whose output drives CDE-affecting
  actions, is a third-party service provider under 12.8.
- Scope is confirmed at least every 12 months and on significant change (12.5.2), and every 6
  months for service providers (12.5.2.1). Adding an agent, a tool, an MCP server or a model
  provider is a significant change.

Tightens
- AEC-01:
  - The 12.5.1 inventory includes every agent and its tools, skills, connectors and standing
    instruction files.
  - Bespoke agent code and third-party agent components are in the 6.3.2 inventory.
  - Model providers and tool brokers in scope are on the 12.8.1 list and in the 12.8.5
    responsibility matrix.
- AEC-02:
  - Each agent and subagent has its own application or system account. No shared agent
    identities (8.2.2).
  - Agent account access is reviewed at the frequency set by a targeted risk analysis
    (7.2.5.1, 12.3.1).
  - People who approve or administer CDE-reaching agents use MFA (8.4.2, 8.4.3).
- AEC-03: R3 at minimum for:
  - any action on cleartext account data;
  - changes to network security controls, segmentation or security-control configuration;
  - changes to payment pages or their scripts (6.4.3, with tamper detection under 11.6.1);
  - any action affecting payment-flow integrity.

  Auto-approve and autonomous modes MUST NOT be used for these.
- AEC-06: R3/R4 preflight declares:
  - the PCI scope category;
  - the account data classes touched;
  - the affected CDE components;
  - the change-management reference (6.5.1).

  Execution is blocked if any of these is missing.
- AEC-07:
  - Receipts are retained 12 months, with 3 months immediately available (10.5.1).
  - They are protected from modification (10.3).
  - They are time-synchronized (10.6).
  - They are reviewed daily by automated means (10.4.1, 10.4.1.1).
- AEC-07 and AEC-08:
  - Receipts, transcripts, prompts, memories and model-provider logs MUST NOT contain full
    PAN or any sensitive authentication data.
    - That is a DAS-1 tightening.
    - The PCI baseline is 3.3.1 (no SAD after authorization) and 3.5.1 (PAN unreadable
      wherever stored).
  - Account data an agent keeps in memory is subject to retention limits (3.2.1).
  - Agents cannot copy or relocate PAN over remote-access paths (3.4.2).
  - PAN found in any of these stores is handled under 12.10.7.
- AEC-08:
  - Agent egress from the CDE is limited by the 1.2–1.4 network security controls.
  - The agent's reach is included in segmentation testing (11.4.5; 11.4.6 for service
    providers).
  - Penetration testing covers the agent's application layer and tool interfaces (11.4.1 to
    11.4.3).
  - Prompt injection is treated as an attack class under 6.2.4.
- AEC-09:
  - No credential in prompts, standing instructions, skills, configuration or agent output
    (8.6.2).
  - Agent credentials live in secrets management and are changed per 8.6.3.
  - Keys follow 3.6–3.7.
- AEC-12:
  - The 12.10.1 plan covers prompt injection, out-of-scope agent actions, compromised tools
    or skills, and unauthorized AI tools.
  - It is tested annually (12.10.2).
  - Failure of an agent gate or kill switch is treated as a failure of a critical security
    control system under 10.7.2.
- AEC-04 and AEC-10: apply unchanged. PCI DSS has no counterpart.
- AEC-13 (v0.003 Draft): a subagent's CDE reach MUST NOT exceed its parent's, and each
  subagent identity is reviewed as its own system account.
- AEC-14 (v0.003 Draft):
  - Sensitive-data access, external communication and untrusted input are not combined in
    one agent context without approval at the composed class, R3 at minimum. This follows
    the PCI SSC AI supplement.
  - Detokenize-capable tool sets are classified as cleartext access.

Adds
- AECX-014 Segmentation boundary enforcement
- AECX-030 Immutable logging
- AECX-041 Data minimization and output filtering
- AECX-052 MCP trust segmentation
- AECX-063 Connector and account boundary
- AECX-065 Context and memory containment
- AECX-068 Agent supply-chain control

Overlay drills
- D-PCI-01 Segmentation traversal test
  - Pass: disallowed traversal from the agent's context into the CDE is blocked and logged
    with correlation IDs.
  - Output: test log pack and results summary.
- D-PCI-02 Account data leakage test
  - Pass: a test PAN placed in the agent's input does not appear unmasked in receipts,
    transcripts, logs, memory or provider-bound requests. Any sighting triggers the 12.10.7
    procedure.
  - Output: scan results across every store named in AEC-07, and the incident record if one
    was raised.
- D-PCI-03 Detokenize composition test
  - Pass: an agent holding tokens and a detokenize-capable tool cannot reach cleartext
    without R3 approval.
  - Output: blocked-action receipt and approval artifact.
- D-PCI-04 Agent account review
  - Pass: every agent and subagent identity appears in the 7.2.5.1 review, with privileges
    matched to its catalog entry.
  - Output: review record and the catalog diff.

Receipt fields
- R3/R4 receipts MUST carry these fields in `overlay_context.pci`:
  - `scope_category` (cde, connected, out_of_scope);
  - `account_data_class` (none, tokenized, truncated, pan, sad);
  - `cde_component_ref`;
  - `change_ref`;
  - `targeted_risk_analysis_ref` where a requirement's frequency is set by 12.3.1;
  - `tpsp_ref` when a third-party service provider took part.

Caveat
- Not legal or compliance advice.
  - PCI DSS is maintained by PCI SSC.
  - Validation requirements are set by the payment brands and acquirers.
  - Assessment is by a QSA or ISA, or by self-assessment questionnaire. Using this overlay does not establish PCI DSS compliance, and MUST NOT be claimed as
  DAS-1(TM) conformance.
