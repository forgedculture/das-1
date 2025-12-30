<p align="center">
  <img src="assets/brand/DAS-1_Banner_1024.png" alt="DAS-1(TM)" width="640">
</p>

<p align="center"><strong>Authority, Tempered.</strong></p>
# DAS-1(TM): Delegated Authority Standard(TM)

Tool calls are production changes.

AI is moving from content generation to execution. Agentic workflows and AI-powered automations now invoke tools: they change state, touch sensitive data, trigger workflows, and spend money at machine speed while approvals still happen at human speed.

That gap becomes your next incident.

DAS-1(TM) is a minimal, operator-grade standard for delegated authority in AI and agentic systems. It defines 12 Authority Engineering Controls (AEC-01 through AEC-12), required drills, and a conformance claim that is backed by receipts.

- Core Spec: spec/core/das-1-core-v0.001.md
- Conformance: spec/conformance/
- Controls Catalog: catalog/
- Profiles: profiles/
- Overlays: overlays/

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

## Conformance

You may claim "DAS-1(TM) v0.001 Conformant(TM)" only if:
- All 12 AEC controls are implemented, or explicitly excepted with expiry dates
- Both required drills executed within the last 90 days
- Minimum metrics are measurable from stored receipts

See: spec/conformance/conformance-criteria-v0.001.md

## Collaboration

Bring receipts.
- Run the checklist against one real agentic workflow and open an issue with artifacts and gaps.
- Propose a profile mapping (MCP, agentic UI, CI agent, ticketing agent) to the AEC controls.
- Propose an overlay manifest for regulated environments using the overlay pattern.

## Licensing

- Spec and documentation: CC BY 4.0 (see LICENSE-DOCS)
- Code and tooling: Apache 2.0 (see LICENSE and LICENSE-CODE)
- Brand assets (logos, marks, badges): all rights reserved, trademark governed (see assets/brand/LICENSE-ASSETS.txt and TRADEMARKS.md)

Licensing

- Spec and documentation: CC BY 4.0 (see LICENSE-DOCS)
- Code and tooling: Apache 2.0 (see LICENSE and LICENSE-CODE)
- Brand assets (logos, marks, badges): all rights reserved, trademark governed (see assets/brand/LICENSE-ASSETS.txt and TRADEMARKS.md)


Status
- Version: v0.001 (draft)
- Date: 2025-12-30
