# DAS-1(TM) Government services overlay v0.002 (Informative)

Status: Informative (documentation-only). This domain overlay is NOT machine-verified and is NOT part of the DAS-1(TM) v0.002 conformance claim set. It SHOULD be read as guidance only; normative force comes from the DAS-1(TM) core and the applicable platform overlay, not from this document. It does not replace applicable public-sector law, due-process and administrative-procedure requirements, records, privacy, accessibility, or procurement policy review.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Govern delegated authority in civilian government workflows involving benefits, permits, procurement, records, casework, public communications, inspections, enforcement support, public safety support, and administrative decision systems.
- Preserve due process, accountability, public-record integrity, accessibility, and review rights when agents support public services.

Threat assumptions
- Government systems may affect rights, benefits, eligibility, enforcement, records, procurement, or public commitments.
- Records may be subject to retention, disclosure, privacy, accessibility, and audit obligations.
- AI-assisted decisions can be biased, opaque, or unappealable if receipts and human accountability are weak.
- Public communications can create reliance or official commitments.

Tightens
- AEC-03: R3/R4 includes benefits/eligibility determination, enforcement action, permit/license decision, procurement award/change, public commitment, official public communication, record deletion/mutation, or rights-affecting decision support.
- AEC-06: preflight for R3/R4 must include agency owner, statutory/policy authority, affected person/entity, public impact, appeal/review path, records retention path, and rollback/correction plan.
- AEC-07: receipts must support reconstruction across source data, policy basis, human accountability, approval, execution, notice, appeal/review, and record retention.
- AEC-08: public records, personal data, protected data, and law-enforcement/public-safety data must have explicit allowed paths.
- AEC-12: incident annex must include erroneous decision, public communication correction, records correction, data disclosure, and appeal/review reconstruction.

Adds
- AECX-030 Immutable logging
- AECX-041 Data minimization and output filtering
- AECX-063 Connector and account boundary
- AECX-066 Approval artifact integrity
- AECX-069 Standing instruction governance

Runtime baseline
- Autonomous rights-affecting decisions, enforcement actions, benefits denial/approval, permit/license decisions, procurement awards, or official public commitments are prohibited.
- Human accountability and appeal/review path must be clear for rights-affecting workflows.
- Public communications require source verification and risk-proportional approval.
- Records created or modified by agents must follow retention and audit requirements defined by the agency owner.

Overlay drills
- D-GOV-01 Rights-affecting decision gate test
  - Pass: benefits, permit, enforcement, or eligibility decisions require accountable human approval and appeal/review receipts.
  - Output: decision receipts, approval artifacts, review path evidence.
- D-GOV-02 Public record retention test
  - Pass: agent-created or modified records preserve retention, provenance, and correction evidence.
  - Output: retention mapping and record mutation receipts.
- D-GOV-03 Public communication approval test
  - Pass: official public communications require source verification and approval.
  - Output: source verification, approval, publication, and correction receipts.

Operational risk closure requirements
- R3/R4 receipts MUST include `agency_owner_id`, `authority_or_policy_ref`, `affected_person_or_entity_ref`, `human_accountable_official`, `appeal_or_review_path_ref`, `records_retention_ref`, and `correction_or_rollback_pointer`.
- Public communication receipts MUST include source verification, approval artifact, publication destination, accessibility review where applicable, and correction path.

Caveat
- Not legal, regulatory, or policy advice. Using this overlay does not establish public-sector legal or policy compliance and MUST NOT be claimed as DAS-1(TM) conformance.
