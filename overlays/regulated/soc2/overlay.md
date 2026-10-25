# DAS-1(TM) SOC 2 overlay v0.002 (Informative)

Status: Informative and documentation-only.

- This overlay is not machine-verified and is not part of the DAS-1(TM) v0.002 conformance
  claim set.
- It does not establish a SOC 2 opinion, and does not replace the service auditor's
  judgement.
- Criterion checking is recorded in `mappings/regulated/soc2-tsc.md`.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Make agents inside a service organization's system examinable in a SOC 2 Type II report
  against the 2017 Trust Services Criteria.
- Turn DAS-1 receipts into evidence an auditor can sample.

Framework basis (checked 2026-10-25)
- 2017 TSC (revised points of focus, 2022).
- 2018 Description Criteria (revised implementation guidance, 2022).
- AICPA TQA Section 9561 (2026-09-11), which is nonauthoritative. As summarized publicly, it
  adds no criteria. A third-party AI provider is a subservice organization when its controls
  are needed, in combination with the entity's, to meet the service commitments.

System description and scoping
- The system description names:
  - each agent and what it does;
  - the tools and connectors it can use;
  - the model providers and tool brokers behind it.
- A model provider or hosted agent platform whose controls are needed to meet the criteria
  is a subservice organization. The description says whether it is carved out or included.
  - If carved out, the description lists the complementary subservice organization
    controls (CSOCs) the entity expects of it. The entity monitors it under CC9.2, for
    example by reviewing its SOC report.
  - If included, its controls are tested, which needs its cooperation and its own assertion.
- A provider whose controls are not needed to meet the criteria is a vendor under CC9.2.
- The report states complementary user entity controls (CUECs) for the customer side, for
  example customer-held approver identities and customer-set risk classes.

Tightens
- AEC-01:
  - The catalog is the source for the system description's component inventory (CC6.1,
    CC2.1).
  - Every third-party tool, model provider and tool broker has a CC9.2 vendor record.
- AEC-02:
  - Agent and subagent identities are registered before credentials are issued (CC6.2).
  - They are included in the periodic access reviews under CC6.3.
  - Removal is evidenced with a date.
- AEC-03:
  - The R3/R4 gate is a documented control activity (CC5.2, CC5.3).
  - For every executed R3/R4 action, the approval can be retrieved, names an authorized
    approver, and has a timestamp before execution.
  - This is what the auditor samples for operating effectiveness.
- AEC-05: the revocation drill is a separate evaluation under CC4.1, run on its stated
  cadence throughout the observation period. A missed drill is a deviation.
- AEC-06 and CC8.1: all of the following are system changes and go through change
  management with authorization and testing:
  - changes to an agent's tools,
  - changes to its model or model version,
  - changes to an MCP server or connector,
  - changes to a skill,
  - changes to a standing instruction file.
- AEC-07:
  - Receipts are retained for the full observation period and until the report is issued.
  - Their completeness is demonstrable as information produced by the entity: the receipt
    count reconciles with an independent source, such as gateway or provider-side call
    records.
- AEC-08: where Confidentiality is in scope, agent context, memory and logs are covered by
  the C1.1 and C1.2 identification and disposal controls. Where Privacy is in scope, the
  same applies under P3, P4 and P6.
- AEC-11:
  - Open exceptions are disclosed to the auditor.
  - An exception that expired without remediation, or renewed without review, is a control
    deviation.
- AEC-12: the tool-call incident annex is part of the CC7.3 to CC7.5 incident process, and
  its exercise records are retained for the period.
- AEC-13 (v0.003 Draft):
  - A delegated agent hosted by another party is a subservice organization or a vendor.
  - Each delegation record resolves to the original human principal (AEC-13). A service
    account may appear in the chain, but is never its end.
- AEC-04 and AEC-10: apply unchanged. SOC 2 has no counterpart; they are written as the
  entity's own control activities under CC5.1.
- Agent components: skills, MCP servers and code an agent fetches are software under CC6.8
  (unauthorized or malicious software). Drift in standing instructions and agent
  configuration is monitored under CC7.1.
- Fraud risk: the risk assessment (CC3.3) considers autonomous agent actions as a fraud and
  misuse vector.
- System incidents: significant agent incidents are disclosed in the system description, as
  the Description Criteria require for significant system incidents.

Adds
- AECX-030 Immutable logging
- AECX-060 Skill provenance and review
- AECX-062 Tool broker policy enforcement
- AECX-063 Connector and account boundary
- AECX-066 Approval artifact integrity
- AECX-068 Agent supply-chain control
- AECX-069 Standing instruction governance

Overlay drills
- D-SOC2-01 Population completeness
  - Pass: for a sample window, the count and identity of receipts reconcile with an
    independent record of tool calls. The differences are explained.
  - Output: reconciliation workpaper.
- D-SOC2-02 Approval-before-execution sample
  - Pass: a random sample of executed R3/R4 receipts across the period each has an
    authorized approval timestamped before execution.
  - Output: the sample, and the approval and execution pairs.
- D-SOC2-03 Agent access review
  - Pass: every agent and subagent identity appears in the CC6.3 review, with privileges
    matched to its catalog entry. Removed identities show a removal date.
  - Output: review record and the catalog diff.
- D-SOC2-04 Agent change control
  - Pass: a sample of changes to tools, models, skills and standing instructions each has
    authorization and testing evidence before it went live.
  - Output: the change sample and its tickets.

Receipt fields
- R3/R4 receipts MUST carry these fields in `overlay_context.soc2`:
  - `entity_control_ref`, the entity's own control ID;
  - `tsc_refs`;
  - `change_ref` where the action is a system change;
  - `subservice_org_ref` where a subservice organization took part.

Caveat
- Not legal, audit or compliance advice. A SOC 2 report is the service auditor's opinion
  under AICPA attestation standards. Using this overlay does not establish one, and MUST NOT
  be claimed as DAS-1(TM) conformance.
