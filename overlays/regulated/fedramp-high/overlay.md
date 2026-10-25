# DAS-1(TM) FedRAMP High overlay v0.002 (Informative)

Status: Informative and documentation-only.

- This overlay is not machine-verified and is not part of the DAS-1(TM) v0.002 conformance
  claim set.
- It does not establish a FedRAMP certification, and does not replace a FedRAMP-recognized
  independent assessment.
- Control membership and its checking status are recorded in
  `mappings/regulated/fedramp-high.md`.

Prerequisite
- DAS-1(TM) v0.002 Conformant.

Objective
- Make agents inside a FedRAMP High authorization boundary assessable against the NIST SP
  800-53 Rev 5 High baseline. Under the Consolidated Rules for 2026, FedRAMP Rev5 Class D
  includes the current High baseline (FedRAMP Notice 0004). FedRAMP says classes are not
  one-for-one replacements for impact levels.
- Make the agent's tools, model providers and delegated agents explicit parts of that
  boundary.

Framework basis (checked 2026-10-25)
- FedRAMP Consolidated Rules for 2026, mandatory from 2027-01-01
  (https://www.fedramp.gov/2026/timeline/). The Class D rule for validated cryptographic
  modules also has a grace period to 2027-06-01.
- FedRAMP 20x does not yet cover Class D.
- NIST's agent overlays for SP 800-53 are planned but not published. Reconcile this overlay
  when they are.

Scoping and the authorization boundary
- Every component that processes or stores federal data is inside the boundary or is an
  external service under SA-9 and SA-9(2). That includes:
  - the model provider,
  - the tool broker,
  - each MCP server or connector,
  - each delegated agent's host.
- No component sits outside both.
- A hosted model provider that processes federal data, and holds no FedRAMP certification
  adequate for the system, needs an explicit agency risk acceptance or must be brought inside
  the boundary. Which applies is recorded in `external_service_ref`. Check this against the
  CR26 rules for external services before assessment.
- Federal data an agent handles stays in U.S. locations or locations under U.S. jurisdiction
  (SA-9(5)). This includes prompts, context, memory, transcripts and provider logs.
- Changes to AI services follow FedRAMP significant change notification:
  - Adding a model to an approved AI service, without exposing federal data to a new
    service, is adaptive.
  - A new third-party AI service, or training on federal data, is transformative.
  - The AEC-01 catalog diff is the evidence for either.

Tightens
- AEC-01:
  - The catalog is maintained by automated means (CM-8(2)) with accountability information
    (CM-8(4)).
  - Uncatalogued tools and components are denied by allow-list (CM-7(5)).
  - Each component's digest is verified at load (SI-7(15)).
- AEC-02:
  - Each agent and subagent identity has usage conditions (AC-2(11)).
  - Atypical usage is monitored (AC-2(12)).
  - Agent access to privileged commands is limited (AC-6(3)), and so is its privilege for
    code execution (AC-6(8)).
  - Cached credentials expire (IA-5(13)).
- AEC-03:
  - Approvals are non-repudiable (AU-10). The FedRAMP AU-10 parameter already lists approval
    among the actions that require it. Each approval is bound to an authenticated approver.
  - Approvers use multi-factor authentication (IA-2(1), IA-2(2)) and get role-based
    training for approving agent actions (AT-3).
  - The approval function runs isolated from the agent (SC-3). The agent cannot write to the
    approval channel or hold credentials for it.
  - Automated mechanisms block changes until the designated human approvals are received
    (CM-3(1)).
- AEC-03 and OMB M-25-21:
  - M-25-21 defines high-impact AI as AI whose output "serves as a principal basis for
    decisions or actions with legal, material, binding, or significant effect on rights or
    safety".
  - An agent action meeting that definition is R4. That is a DAS-1 tightening.
  - M-25-21's minimum practices, including human oversight and a fail-safe, bind the agency.
    They reach the provider only through contract (M-25-22).
- AEC-05:
  - Revocation is implemented as dynamic reconfiguration (IR-4(2)).
  - The revocation budget MUST be shorter than the 15-minute initial report deadline below,
    so containment is in hand before the first report.
- AEC-06: R4 changes are exercised in a separate test environment first (CM-4(1)).
- AEC-07:
  - Receipts form a system-wide, time-correlated trail (AU-12(1)).
  - They are backed up to a separate system (AU-9(2)) and cryptographically protected
    (AU-9(3)).
  - Audit failure raises a real-time alert (AU-5(2)).
  - Retention follows the AU-11 value set in the system security plan and agency
    requirements.
- AEC-08:
  - Agent egress is limited to prevent exfiltration (SC-7(10)).
  - Agent execution components are isolated from each other and from security functions
    (SC-7(21)).
  - Encrypted flows are governed as flows (AC-4(4)).
- AEC-09:
  - All cryptography protecting agent credentials, receipts and federal data uses
    CMVP-validated modules (SC-13, and the FedRAMP Class D rule at
    https://www.fedramp.gov/2026/reference/rev5/d/cryptographic-module-use/).
  - Key availability is maintained (SC-12(1)).
- AEC-11: open exceptions and vulnerability items travel with the quarterly Ongoing
  Certification Report. An exception still expires by default under AEC-11.
- AEC-12:
  - The tool-call incident annex treats a compromised or misbehaving agent as an insider
    threat (IR-4(6)).
  - Initial reports go to FedRAMP within 15 minutes for PAIN-3 to 5, and within 1 hour for
    PAIN-1 and 2. An incident with no PAIN rating is treated as PAIN-5.
  - Reports also go to agency customers under their own procedures.
  - Exercises use simulated events (IR-2(1)).
- AEC-13 (v0.003 Draft):
  - A delegated agent hosted outside the boundary is an external service under SA-9.
  - Data passed between the agent and a delegated agent's system is accepted only if the
    sender holds the needed write authorization (CA-3(6)). This is a partial analog only.
- AEC-14 (v0.003 Draft):
  - Outbound communications from agent contexts are analyzed for the composed effect
    (SI-4(11)).
  - Untrusted content the agent reads is validated as input (SI-10).
- AEC-04 and AEC-10: apply unchanged. FedRAMP High has no counterpart.

Adds
- AECX-014 Segmentation boundary enforcement
- AECX-030 Immutable logging
- AECX-050 Workspace containment
- AECX-052 MCP trust segmentation
- AECX-062 Tool broker policy enforcement
- AECX-066 Approval artifact integrity
- AECX-068 Agent supply-chain control

Overlay drills
- D-FRH-01 Boundary completeness test
  - Pass: every destination reachable from an agent context is inside the boundary or listed
    as an SA-9 external service. Nothing else is reachable.
  - Output: egress inventory and blocked-destination receipts.
- D-FRH-02 Fifteen-minute incident path
  - Pass: from detection of an agent incident touching federal data, revocation completes and
    an initial report is ready within 15 minutes.
  - Output: timed drill log with revocation and report timestamps.
- D-FRH-03 Approval isolation test
  - Pass: from inside the agent context, no write, credential read or display change to the
    approval function succeeds. Approvals carry non-repudiable approver identity.
  - Output: refused-attempt receipts and a sample approval with signature evidence.
- D-FRH-04 Audit failure alert
  - Pass: stopping the receipt pipeline raises a real-time alert, and the agent halts or
    fails safe rather than running unlogged.
  - Output: alert record and the halted-execution receipt.

Receipt fields
- R3/R4 receipts MUST carry these fields in `overlay_context.fedramp_high`:
  - `boundary_component_ref`;
  - `external_service_ref` for any SA-9 service used;
  - `data_location`;
  - `approver_signature_ref`;
  - `pain_rating` for incident-linked receipts.

Caveat
- Not legal or compliance advice. FedRAMP certification is granted under FedRAMP's rules,
  through its assessment process. Using this overlay does not establish a certification, and
  MUST NOT be claimed as DAS-1(TM) conformance.
