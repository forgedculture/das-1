# DAS-1(TM) HIPAA overlay v0.002 (Informative)

Status: Informative and documentation-only.

- This overlay is not machine-verified and is not part of the DAS-1(TM) v0.002 conformance
  claim set.
- It does not establish HIPAA compliance, and does not replace a risk analysis, privacy
  officer or legal review.
- Citation checking is recorded in `mappings/regulated/hipaa.md`.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Relationship to the healthcare domain overlay
- `overlays/domain/healthcare/` says which healthcare actions are R3/R4: chart writes,
  orders, clinical messaging and similar.
- This overlay says what HIPAA requires of the controls and evidence around any agent that
  touches ePHI, clinical or not.
- Use both where both apply.

Objective
- Make agents that create, receive, maintain or transmit ePHI assessable against the HIPAA
  Security, Privacy and Breach Notification Rules.
- Keep the agent's model provider, tools and stores inside the covered entity's or business
  associate's safeguards.

Framework basis (checked 2026-10-25)
- 45 CFR Part 160, Subparts A and C (definitions, including business associate in 160.103).
- 45 CFR Part 164, Subparts C, D and E, as currently codified.
- The 2025-01-06 Security Rule NPRM is not final. The final action is estimated for July
  2027.
- Items below marked "NPRM-ready" are recommended now, so adopters are ready if it is
  finalized as proposed. They are not current legal requirements.
- Items marked "DAS-1 tightening" go beyond what HIPAA itself requires.

Scoping
- An agent is in scope when its context, tools, memory, logs or outputs can hold ePHI.
- Every place an agent can put ePHI is an ePHI system under 164.308(a)(1)(ii)(A) risk
  analysis:
  - prompt,
  - context window,
  - retrieval index,
  - memory,
  - transcript,
  - receipt,
  - cache,
  - model-provider log.
- Business associates. An external party that creates, receives, maintains or transmits
  ePHI *on behalf of* the entity is a business associate (160.103) and needs a BAA before
  ePHI reaches it. Such parties include:
  - the model provider,
  - the hosting platform,
  - the tool broker,
  - each connector vendor.

  The conduit exception covers transmission only. It does not cover a model provider, which
  processes the content.
- Other recipients. Any other recipient needs either:
  - a permitted basis for the disclosure (164.502(a), 164.506, 164.510 or 164.512), for
    example a treatment disclosure to another provider; or
  - a limited data set under a data use agreement (164.514(e)).
- A disclosure with neither basis is impermissible, and is presumed a breach (164.402).

Tightens
- AEC-01:
  - The catalog names, for each tool and component:
    - whether it can touch ePHI;
    - the BAA that covers its vendor, where the vendor acts on the entity's behalf;
    - the security official accountable for it (164.308(a)(2)).
  - NPRM-ready: keep the catalog as part of the technology asset inventory and network map.
- AEC-02:
  - Every agent and subagent has a unique identity (164.312(a)(2)(i)).
  - Access follows authorization and/or supervision (164.308(a)(3)(ii)(A)) and information
    access management (164.308(a)(4)).
  - Agent context is scoped to the minimum necessary for the task (164.502(b), 164.514(d)).
    Retrieval MUST NOT pull records beyond the task's role-based need.
- AEC-03: R3 at minimum for:
  - any disclosure of ePHI outside the entity;
  - writes to a designated record set;
  - any use that needs an authorization under 164.508.

  Decision-support outputs used in patient care are reviewed by an accountable clinician.
  That is a DAS-1 tightening; see the healthcare domain overlay. Where Section 1557 applies,
  45 CFR 92.210, which is not part of HIPAA, separately requires reasonable efforts to
  identify and mitigate discrimination risk in such tools.
- AEC-04: when the approval budget is exceeded, the agent's R3/R4 request fails closed.
  Urgent access then goes through the documented emergency access procedure
  (164.312(a)(2)(ii)), carried out by a human outside the agent.
- AEC-05: the kill switch is part of security incident response (164.308(a)(6)(ii)), and of
  access termination and modification (164.308(a)(3)(ii)(C), 164.308(a)(4)). Its drill can
  also serve as testing of the contingency plan (164.308(a)(7)(ii)(D)).
- AEC-07:
  - Receipts give the information system activity review (164.308(a)(1)(ii)(D)) what it
    needs.
  - Receipts record each disclosure in enough detail to support an accounting of disclosures
    (164.528).
  - Receipts are kept six years. That is a DAS-1 tightening, aligned to 164.316(b)(2)(i)
    documentation retention and the six-year look-back of 164.528(a).
  - Where receipts contain ePHI, they are themselves ePHI and get 164.312 protections.
- AEC-08:
  - ePHI is the highest data class.
  - Data leaving the entity's control goes in one of four ways:
    - de-identified (164.514(b));
    - as a limited data set under a data use agreement;
    - on a permitted disclosure basis;
    - to a business associate under a BAA.
  - Safe harbor de-identification of free text is not assumed: prompts and transcripts
    routinely carry identifiers.
  - ePHI in transit is encrypted (164.312(e)(2)(ii)); at rest, encrypted where reasonable and
    appropriate (164.312(a)(2)(iv)).
  - NPRM-ready: treat encryption as required.
- AEC-09:
  - Agent credentials that reach ePHI follow 164.312(d) and password management
    (164.308(a)(5)(ii)(D)).
  - No credential in prompts, standing instructions or skills.
  - NPRM-ready: MFA for human access to agent administration.
- AEC-10: applies unchanged. HIPAA has no counterpart.
- AEC-11:
  - An addressable specification not implemented for an agent is documented under
    164.306(d)(3), as an exception with owner and expiry.
  - The NPRM would remove this route.
- AEC-12:
  - The tool-call incident annex includes the 164.402 four-factor breach risk assessment and
    the notification clocks:
    - individuals: without unreasonable delay, within 60 calendar days of discovery
      (164.404);
    - media: for more than 500 residents of a State (164.406);
    - the Secretary: at the same time as individuals for 500 or more, otherwise in a log due
      within 60 days after the calendar year ends (164.408);
    - business associate to covered entity: without unreasonable delay, within 60 days at
      most. A contract may shorten this, never extend it (164.410).
  - Discovery is the first day the breach is known, or would be known with reasonable
    diligence. An agent receipt showing an impermissible disclosure starts that clock.
- AEC-13 (v0.003 Draft):
  - A subagent or delegated tool that receives ePHI inherits the parent's minimum-necessary
    scope and no more.
  - A delegated agent hosted by another vendor acting on the entity's behalf needs that
    vendor's BAA or subcontractor agreement (164.502(e)(1)(ii), 164.504(e)(2)(ii)(D)).
- Business associate agreements for agent vendors
  - Each BAA addresses everything 164.504(e)(2) requires, including:
    - permitted uses;
    - safeguards;
    - breach reporting;
    - subcontractor flow-down;
    - support for access, amendment and accounting;
    - Privacy Rule obligations the business associate carries out;
    - books and records available to HHS;
    - return or destruction at termination.
  - For agent vendors it also prohibits training on or reusing ePHI, and states log and
    retention behavior.

Adds
- AECX-041 Data minimization and output filtering
- AECX-063 Connector and account boundary
- AECX-065 Context and memory containment
- AECX-066 Approval artifact integrity
- AECX-068 Agent supply-chain control

Overlay drills
- D-HIPAA-01 Disclosure basis coverage test
  - Pass: every destination the agent can send content to is one of:
    - covered by a BAA, for parties acting on the entity's behalf;
    - covered by a recorded permitted-disclosure basis or data use agreement;
    - blocked from receiving ePHI.
  - Output: destination inventory matched against the BAA and disclosure-basis register, and
    blocked-send receipts.
- D-HIPAA-02 Minimum necessary retrieval test
  - Pass: a task scoped to one patient or role cannot retrieve records outside that scope.
  - Output: retrieval receipts and the refused queries.
- D-HIPAA-03 ePHI store sweep
  - Pass: every store an agent writes is either protected as ePHI or holds none.
  - Output: store inventory and scan results for planted test identifiers.
- D-HIPAA-04 Breach clock tabletop
  - Pass: from a receipt showing an impermissible disclosure, the team reconstructs the
    chain, completes the four-factor assessment, and names each notification deadline.
  - Output: tabletop record with dates.

Receipt fields
- R3/R4 receipts MUST carry these fields in `overlay_context.hipaa`:
  - `ephi_present` (true or false);
  - `minimum_necessary_basis`;
  - `baa_ref_or_disclosure_basis` for every external recipient;
  - `disclosure_purpose` where the action discloses;
  - `designated_record_set_ref` for writes.

Caveat
- Not legal or compliance advice. HIPAA obligations depend on the entity's role, contracts
  and risk analysis. Using this overlay does not establish HIPAA compliance, and MUST NOT be
  claimed as DAS-1(TM) conformance.
