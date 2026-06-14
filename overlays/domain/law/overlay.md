# DAS-1(TM) Legal services overlay v0.002 (Informative)

Status: Informative (documentation-only). This domain overlay is NOT machine-verified and is NOT part of the DAS-1(TM) v0.002 conformance claim set. It SHOULD be read as guidance only; normative force comes from the DAS-1(TM) core and the applicable platform overlay, not from this document. It does not replace legal professional responsibility, bar/ethics rules, privilege and confidentiality obligations, or jurisdiction-specific practice-of-law review.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Govern delegated authority in legal workflows involving research, drafting, matter management, e-discovery, privilege review, client communications, contract workflows, and filings.
- Prevent agents from silently crossing into unsupervised legal advice, privilege waiver, missed filing obligations, or unauthorized external submission.

Threat assumptions
- Matter files, client instructions, opposing-party materials, and discovery content may contain adversarial or privileged information.
- Generated legal citations, summaries, and arguments may be inaccurate or incomplete.
- Client communications and filings can create binding or deadline-sensitive effects.
- Matter-level confidentiality and conflict boundaries can be breached by shared memory, retrieval, or connectors.

Tightens
- AEC-03: R3/R4 includes filing/submission, client legal advice, settlement/contract commitment, privilege designation, waiver, matter transfer, deadline mutation, bulk discovery production, or external legal communication.
- AEC-06: preflight for R3/R4 must include matter/client scope, jurisdiction or forum when relevant, accountable lawyer, deadline impact, privilege/confidentiality assessment, and rollback/correction plan.
- AEC-07: receipts must bind matter, source materials, citation verification, approval, submission/send event, and downstream record.
- AEC-08: matter/client boundaries must apply to prompts, standing instructions, skills, retrieval, memories, connectors, logs, and delegated agents.
- AEC-11: exceptions for deadline workarounds, matter-boundary expansion, or privilege controls must be owned and expire by default.

Adds
- AECX-014 Segmentation boundary enforcement
- AECX-041 Data minimization and output filtering
- AECX-065 Context and memory containment
- AECX-066 Approval artifact integrity
- AECX-069 Standing instruction governance

Runtime baseline
- Agents may assist with drafting, research support, organization, summarization, and cite checking under supervision.
- Autonomous legal advice, client-send, filing, settlement authority, privilege waiver, or deadline mutation is prohibited.
- Citation, quotation, and authority claims require verification receipts before R3/R4 use.
- Matter-specific instructions must not be overridden by lower-authority personalizations or unrelated matter context.

Overlay drills
- D-LAW-01 Privilege boundary test
  - Pass: privileged or confidential matter content cannot cross to unauthorized matters, tools, memories, or destinations.
  - Output: denied access logs and matter-boundary receipts.
- D-LAW-02 Citation verification test
  - Pass: legal authorities used in R3/R4 work have source verification evidence.
  - Output: citation check record and approval receipt.
- D-LAW-03 Filing/client-send gate test
  - Pass: filings and client legal communications remain blocked until accountable human approval.
  - Output: draft receipt, approval artifact, send/filing receipt or blocked-send log.

Operational risk closure requirements
- R3/R4 receipts MUST include `matter_ref`, `client_or_confidentiality_boundary_ref`, `accountable_lawyer_id`, `source_material_refs`, `approval_artifact_ref`, and `correction_or_withdrawal_pointer`.
- Filing receipts MUST include forum/destination, deadline impact, final approved artifact reference, and submission confirmation.
- Privilege-affecting receipts MUST include privilege review artifact and waiver/non-waiver decision.

Caveat
- Not legal advice and not a substitute for a licensed lawyer's judgment. Using this overlay does not establish professional-responsibility or ethics compliance and MUST NOT be claimed as DAS-1(TM) conformance.
