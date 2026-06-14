# DAS-1(TM) Business operations overlay v0.002 (Informative)

Status: Informative (documentation-only). This domain overlay is NOT machine-verified and is NOT part of the DAS-1(TM) v0.002 conformance claim set. It SHOULD be read as guidance only; normative force comes from the DAS-1(TM) core and the applicable platform overlay, not from this document. It does not replace corporate legal, contractual, employment, financial, privacy, or sector-specific regulatory review.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Govern delegated authority in enterprise operations where agents can affect customers, employees, vendors, contracts, procurement, pricing, refunds, support cases, records, analytics, and internal workflows.
- Preserve useful R1/R2 automation while bounding actions that create financial, contractual, employment, customer, or reputational impact.

Threat assumptions
- Agents may inherit broad SaaS connector access from human accounts.
- Standing instructions and skills can become unofficial operating procedures.
- Low-dollar or low-volume actions can become material through loops, retries, batching, or background automation.
- Customer, employee, vendor, and operational records may include sensitive or regulated data.

Tightens
- AEC-01: tool catalogs must map enterprise tools to business owner, cost center, data class, system of record, and revocation path.
- AEC-03: R3/R4 includes contract issuance or amendment, employment action, price change, refund above threshold, procurement commitment, vendor onboarding, customer account mutation, bulk export, or external communication that binds the organization.
- AEC-06: preflight for R3/R4 must include business owner, affected records/accounts, financial exposure, customer/employee/vendor impact, and rollback plan.
- AEC-07: receipts must correlate request, standing instructions, skill/tool path, approval, execution, and downstream system-of-record mutation.
- AEC-10: spend-incurring and revenue-impacting actions must include cost center, owner, threshold, and cap evidence.
- AEC-11: emergency exceptions for approval bypass, connector expansion, or bulk action must expire by default.

Adds
- AECX-060 Skill provenance and review
- AECX-063 Connector and account boundary
- AECX-066 Approval artifact integrity
- AECX-067 Autonomous change budget
- AECX-069 Standing instruction governance

Runtime baseline
- Business workflows must define thresholds for autonomous, approval-required, and prohibited actions.
- Autonomous contract, hiring, firing, compensation, pricing, procurement, customer-account, and bulk-export actions are prohibited unless explicitly approved by policy and evidenced in receipts.
- External customer, vendor, employee, or public communications that create commitments require risk-proportional review.
- Standing instructions and skills used as operating procedures require owner, review status, version/source, precedence, and revocation evidence.

Overlay drills
- D-BIZ-01 Spend and procurement threshold test
  - Pass: over-threshold spend or procurement commitments require approval and are blocked otherwise.
  - Output: policy thresholds, approval receipts, denied action logs.
- D-BIZ-02 Customer/account mutation test
  - Pass: material customer/account mutations require approval, attribution, rollback pointer, and system-of-record receipts.
  - Output: mutation receipts and rollback evidence.
- D-BIZ-03 Standing operating instruction override test
  - Pass: lower-authority personalizations or unreviewed skills cannot override approved operating rules.
  - Output: instruction inventory, conflict logs, blocked override receipts.

Operational risk closure requirements
- R3/R4 receipts MUST include `business_owner_id`, `system_of_record_ref`, `affected_party_type`, `financial_exposure`, `approval_artifact_ref`, and `rollback_pointer`.
- Spend or revenue-impacting receipts MUST include `cost_center`, `threshold_ref`, and `cap_evaluation_ref`.
- Bulk action receipts MUST include batch size, sampling/approval evidence, and rollback or remediation plan.

Caveat
- Not legal, regulatory, or policy advice. Using this overlay does not establish business legal, contractual, employment, or regulatory compliance and MUST NOT be claimed as DAS-1(TM) conformance.
