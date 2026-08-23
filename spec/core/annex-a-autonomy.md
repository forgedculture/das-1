# Annex A: Autonomy levels (Normative)

Part of Delegated Authority Standard(TM) (DAS-1(TM)) v0.003.

## A.1 Purpose

Risk class describes the consequence of an action. It does not describe how much latitude an agent has with a result. An agent that may only draft an R3 change is in a materially different position from one that may execute it, and DAS-1 through v0.002 had no vocabulary for that difference.

Every implementation invents a ladder. Because the standard was silent, each ladder was bolted onto the R classes differently and the two axes were conflated, which destroys the comparability a standard exists to provide.

This annex defines the autonomy dimension and the rule binding it to risk class. It is normative vocabulary and a binding rule rather than an evidence obligation, so it carries no receipt of its own. Autonomy evidence surfaces through the AEC-01 tool catalog and the AEC-13 delegation record.

## A.2 Autonomy levels (default; replaceable with explicit mapping)

As with the R classes in section 2, this ladder is a default. An organization MAY substitute its own ladder, but MUST publish the crosswalk and MUST preserve the binding rules in A.3.

- A0 Sandboxed: acts only against an isolated environment with no effect on real systems or data.
- A1 Observe: MAY read and report. MUST NOT propose or execute a change.
- A2 Draft: MAY produce a proposed change as an artifact. A human MUST carry out any execution.
- A3 Recommend: MAY produce a proposed change together with a recommendation to act on it. A human MUST carry out any execution.
- A4 Execute with approval: MAY execute, and each execution MUST be preceded by an attributable human approval.
- A5 Execute under policy: MAY execute without per-action human approval where policy conditions are satisfied.

The distinction between A2 and A3 is accountability, not capability. An agent that recommends has taken a position, and the receipt MUST show that it did.

## A.3 Binding rules (Normative)

- Effective authority is the intersection of autonomy level and risk ceiling, never the maximum of them. An agent may do only what both axes permit.
- Promotion along the autonomy axis MUST NOT raise an agent's registered risk ceiling. Raising a risk ceiling is a separate decision requiring its own approval under AEC-03.
- An agent's registered autonomy level and registered risk ceiling MUST both appear in its AEC-01 tool catalog entry.
- Delegation MUST NOT grant an autonomy level above the delegating agent's own. The AEC-13 subset rule applies to both axes.
- AEC-03 is not modified by this annex. Human gating for R3/R4 is a property of the risk axis and binds regardless of autonomy level.

## A.4 Crosswalk to risk classes

The cell shows what the agent may do at that intersection.

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| A0 Sandboxed | sandbox only | sandbox only | sandbox only | sandbox only |
| A1 Observe | read, report | read, report | read, report | read, report |
| A2 Draft | draft | draft | draft | draft |
| A3 Recommend | recommend | recommend | recommend | recommend |
| A4 Execute with approval | execute, approval per policy | execute, approval per policy | execute, approval required (AEC-03) | execute, approval required (AEC-03) |
| A5 Execute under policy | execute under policy | execute under policy | execute, approval required (AEC-03) | execute, approval required (AEC-03) |

Worked example. An agent registered at A5 with an R3 ceiling does not execute R3 actions unattended. AEC-03 binds on the risk axis, so its effective authority for an R3 action is A4. Its A5 latitude is real only for the R1/R2 actions within its ceiling. Reading the two axes as a maximum would have produced unattended R3 execution from a pair of individually defensible registrations.

## A.5 Common error

The recurring implementation error is treating a promotion up the autonomy ladder as a raise in risk ceiling. An agent that has been performing well at A2/R3 gets promoted to A4, and the promotion is recorded as an increase in trust rather than as a move along one specific axis. The risk ceiling then drifts upward without a decision ever being taken about blast radius.

Promotion is a move on one axis. It is not a general increase in trust, and it MUST be recorded as such.

## A.6 Relationship to prior vocabulary

The v0.002 glossary term "autonomy mode" names the same dimension. Overlay language using "autonomy mode" remains valid and refers to this annex.
