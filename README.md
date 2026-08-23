<p align="center">
  <img src="assets/brand/DAS-1_Banner_1024.png" alt="DAS-1(TM)" width="640">
</p>

<p align="center"><strong>Authority, Tempered.</strong></p>
# DAS-1(TM): Delegated Authority Standard(TM)

Tool calls are production changes.

AI is moving from content generation to execution. Agentic workflows and AI-powered automations now invoke tools: they change state, touch sensitive data, trigger workflows, and spend money at machine speed while approvals still happen at human speed.

That gap becomes your next incident.

DAS-1(TM) is a minimal, operator-grade standard for delegated authority in AI and agentic systems. It defines 12 Authority Engineering Controls (AEC-01 through AEC-12), required drills, and conformance claims backed by receipts. A v0.003 draft adds two controls (AEC-13 delegation, AEC-14 classification and composition) and a normative autonomy annex; see below.

- Core Spec: spec/core/das-1-core.md
- Conformance: spec/conformance/
- Controls Catalog: catalog/
- Profiles: profiles/
- Overlays: overlays/

Current overlay bundles:
- `openclaw`: gateway exposure, prompt-injection boundary, sandbox/session isolation, revocation readiness.
- `claude-code`: supervised coding-agent controls (propose/execute boundary, workspace containment, shell/git gating, MCP boundaries, CI execute boundary, approval integrity, revocation readiness).
- `codex`: supervised coding-agent controls (`AGENTS.md` scope, workspace containment, shell/git gating, plugin/connector boundaries, browser/computer-use actions, CI execute boundary, approval integrity, revocation readiness).
- `cursor`: supervised coding-agent controls (`.cursor/rules`, User Rules, `AGENTS.md`, workspace/index containment, terminal/tool authority, background edits, revocation readiness).
- `kiro`: supervised coding-agent controls (steering files, specs, hooks, MCP boundaries, spec task execution, revocation readiness).

Current domain overlay examples:
- `business`: enterprise operations, HR, procurement, customer operations, support, and internal workflows.
- `healthcare`: PHI boundaries, patient communications, chart operations, claims, and clinical-accountability boundaries.
- `law`: matter boundaries, privilege, citation verification, client communications, and filings.
- `finance`: payments, trades, ledger writes, financial advice, nonpublic data, and fraud/sanctions control checks.
- `voting-elections`: voter registration, ballot logistics, public information, reporting support, audits, and election operations.
- `government`: benefits, permits, procurement, records, public communications, enforcement support, and administrative decisions.
- `military`: defense administration, logistics, readiness, cyber defense support, mission planning support, and command-support systems.

## What this is for

Use DAS-1 when an AI agent, automation, or workflow can:
- Invoke tools (APIs, connectors, scripts, pipelines)
- Read sensitive data
- Write changes to systems of record
- Trigger actions with external side effects
- Incur material cost

## Core rules

- The core is closed at 12 controls. Extensions live in profiles, overlays, and the catalog.
- R3 and R4 actions require human approval before execution.
- Bypassing approval without disclosure is a conformance failure.
- If you cannot revoke it, you do not control it.
- Controls are risk-proportional: low-risk work should remain useful while high-risk work stays bounded.

## Conformance

You may claim "DAS-1(TM) v0.002 Conformant(TM)" only if:
- All 12 AEC controls are implemented, or explicitly excepted with expiry dates
- Both required drills executed within the last 90 days
- Minimum metrics M1-M7 are measurable from stored receipts

See: spec/conformance/conformance-criteria.md

Overlay claims are additive:
- Core claim: DAS-1(TM) v0.002 Conformant(TM)
- Overlay claim: DAS-1(TM) v0.002 Conformant(TM) + `<overlay>`

## v0.003 (draft, not claimable)

v0.003 came out of carrying a full enterprise agentic operating model on v0.002 and finding
three things the enterprise needed that the standard did not specify, plus one control that
was measured but never enforced. See spec/roadmap/v0.003-enterprise-load-findings.md.

- AEC-13 Delegation envelope and cascading revocation. The tool catalog governs what an agent
  may call; nothing governed what an agent may *grant*. Delegated authority must be a subset
  of the delegating agent's on every axis, revocation must cascade to every descendant within
  the AEC-05 budget, and lineage must resolve back to the human principal.
- AEC-14 Action classification and composition. Names who classifies, on what evidence, how a
  contest resolves, and what happens when individually low-risk actions compose into a
  high-risk effect. A sequence is governed at its composed class.
- Annex A Autonomy levels. A0-A5 crosswalked to R1-R4. Effective authority is the
  *intersection* of autonomy level and risk ceiling, never the maximum, and promotion along
  the autonomy axis must not raise a registered risk ceiling.
- AEC-10 tightened. A cap must be enforced in the execution path with a named owner and a
  raise path. A spend forecast is not a control.

v0.003 is additive: AEC-01 through AEC-12 are unchanged and unrenumbered, so existing v0.002
claims stay valid against v0.002. The verifier supports `--das-version v0.003` so adopters can
build evidence ahead of release, and a draft evidence pack lives in `das1/examples/v0003/`.

These findings rest on a single enterprise adoption. v0.003 stays Draft until a second
independent adoption confirms or falsifies them.

## Safety With Utility

DAS-1 is designed to protect delegated authority systems without making them inert.
- R1/R2 paths should be largely autonomous under policy.
- R3/R4 paths require explicit human gating.
- Utility guardrails (M5-M7) are part of conformance evidence.
- If emergency hardening materially reduces utility, it must be tracked as an expiring AEC-11 exception.

## Conformance Tooling Quickstart

Install tooling dependencies:

```bash
python -m pip install -r tools/requirements.txt
```

Verify core evidence:

```bash
python tools/das1_verify.py verify \
  --receipts das1/examples/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --report conformance-report.json
```

Verify core plus OpenClaw overlay:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/openclaw/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/openclaw/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --overlay openclaw \
  --report openclaw-overlay-report.json
```

Verify core plus Claude Code overlay:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/claude-code/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/claude-code/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --overlay claude-code \
  --report claude-code-overlay-report.json
```

Verify core plus Codex overlay:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/codex/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/codex/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --overlay codex \
  --report codex-overlay-report.json
```

Verify publishable claim packets:

```bash
python tools/das1_verify.py verify-claims das1/examples/claims
# optional: add --report claims-report.json for publishable evidence bundle output
```

See `/spec/conformance/README.md` for full command options and current machine checks.

## Overlay Extensions

The default verifier is runtime-agnostic and extensible:
- Overlay plugins live in `tools/overlays/`.
- Plugin contract is documented in `tools/overlays/README.md`.
- Overlay-specific evidence can be carried in namespaced `overlay_context` fields.

## Collaboration

Bring receipts.
- Run the checklist against one real agentic workflow and open an issue with artifacts and gaps.
- Propose a profile mapping (MCP, agentic UI, CI agent, ticketing agent) to the AEC controls.
- Propose an overlay manifest for regulated environments using the overlay pattern.

## Licensing

- Spec and documentation: CC BY 4.0 (see LICENSE-DOCS)
- Code and tooling: Apache 2.0 (see LICENSE and LICENSE-CODE)
- Brand assets (logos, marks, badges): all rights reserved, trademark governed (see assets/brand/LICENSE-ASSETS.txt and TRADEMARKS.md)

Status
- Released version: v0.002 (draft)
- In progress: v0.003 core deltas, verifier, and draft evidence pack; not claimable
- Date: 2026-08-20
