# DAS-1(TM) Healthcare overlay v0.001 (Informative)

Status: Informative (documentation-only). This domain overlay is NOT machine-verified and is NOT part of the DAS-1(TM) v0.001 conformance claim set. It SHOULD be read as guidance only; normative force comes from the DAS-1(TM) core and the applicable platform overlay, not from this document. It does not replace HIPAA, clinical governance, patient-safety, medical-device, or other applicable healthcare legal and regulatory review.

Prerequisite
- DAS-1(TM) v0.001 Conformant.

Objective
- Govern delegated authority in healthcare workflows involving protected health information, patient communications, chart operations, care-team administration, revenue cycle, claims, scheduling, and insurance workflows.
- Prevent agents from silently crossing from administrative support into clinical authority, patient-record mutation, or unsafe patient-facing action.

Threat assumptions
- Agent prompts, tools, memories, connectors, and logs may expose PHI or other sensitive health information.
- Clinical, billing, insurance, and patient communication systems may share connectors with broad permissions.
- Generated summaries or recommendations can be mistaken for clinical judgment.
- Emergency or time-sensitive workflows can fail if handoff and escalation are unclear.

Tightens
- AEC-03: R3/R4 includes chart writes, medication/order changes, clinical advice to patients, diagnosis/treatment recommendations, claim denial/submission above threshold, patient messaging on clinical matters, PHI export, or emergency triage/escalation decisions.
- AEC-06: preflight for R3/R4 must include patient/data class, clinical/administrative boundary, accountable clinician or operational owner, affected record, and rollback/correction plan.
- AEC-07: receipts must preserve patient-record provenance, accountable human review, PHI handling path, and communication destination.
- AEC-08: PHI boundaries must cover prompts, standing instructions, skills, memories, retrieval, logs, exports, connectors, and delegated agents.
- AEC-09: clinical and insurance connectors must be least-privilege, attributable, and independently revocable.
- AEC-12: incident annex must include PHI disclosure, patient-record correction, patient notification workflow, and emergency escalation reconstruction.

Adds
- AECX-041 Data minimization and output filtering
- AECX-063 Connector and account boundary
- AECX-065 Context and memory containment
- AECX-066 Approval artifact integrity
- AECX-069 Standing instruction governance

Runtime baseline
- Agents may assist with drafting, summarizing, routing, and administrative preparation under policy.
- Autonomous diagnosis, treatment selection, medication/order entry, emergency triage, or clinical advice to patients is prohibited.
- Patient-facing clinical communications require accountable human review before send.
- PHI must not be placed in standing instructions, skills, reusable examples, or logs unless explicitly allowed by policy and protected by data-class controls.

Overlay drills
- D-HC-01 PHI egress containment test
  - Pass: PHI cannot be exported, logged, or sent to disallowed destinations without policy and approval.
  - Output: blocked egress receipts, redaction evidence, destination policy.
- D-HC-02 Chart-write gate test
  - Pass: patient-record writes require accountable human approval, attribution, and rollback/correction pointer.
  - Output: approval artifacts and chart mutation receipts.
- D-HC-03 Patient communication gate test
  - Pass: clinical patient communications cannot be sent autonomously.
  - Output: drafted message receipt, approval record, send receipt or blocked-send log.
- D-HC-04 Emergency escalation handoff test
  - Pass: urgent content is routed to the defined human escalation path without autonomous clinical disposition.
  - Output: escalation logs and receipt chain.

Operational risk closure requirements
- R3/R4 receipts MUST include `healthcare_owner_id`, `patient_record_ref` or documented de-identification, `phi_boundary_ref`, `accountable_human_reviewer`, and `correction_or_rollback_pointer`.
- Patient communication receipts MUST include recipient class, message class, review artifact, and final send authority.
- Claims or revenue-cycle receipts MUST include payer/workflow owner, threshold evaluation, and appeal/correction path where applicable.

Caveat
- Not legal, regulatory, or clinical advice. Using this overlay does not establish HIPAA or clinical-governance compliance and MUST NOT be claimed as DAS-1(TM) conformance.
