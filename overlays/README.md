# Overlays

Overlays are curated hardening bundles for specific environments.

Rule
- Overlays may tighten core controls and add catalog controls.
- Overlays must not weaken core controls.

Available examples
- `overlays/regulated/pci/`: PCI-oriented hardening overlay.
- `overlays/domain/`: High-impact domain overlays for business, healthcare, law, finance, voting/elections, government, and military/defense contexts.
- `overlays/platform/openclaw/`: OpenClaw runtime hardening overlay focused on exposed gateway, prompt injection, session isolation, and sandbox containment.
- `overlays/platform/claude-code/`: Claude Code runtime hardening overlay focused on workspace containment, shell/git authority gating, standing instruction governance, MCP boundaries, and revocation readiness.
- `overlays/platform/codex/`: Codex runtime hardening overlay focused on `AGENTS.md` scope, workspace containment, shell/git authority gating, plugin/connector boundaries, browser/computer-use actions, and revocation readiness.
- `overlays/platform/cursor/`: Cursor runtime hardening overlay focused on `.cursor/rules`, User Rules, `AGENTS.md`, workspace/index containment, terminal/tool authority, background edits, and revocation readiness.
- `overlays/platform/kiro/`: Kiro runtime hardening overlay focused on steering files, specs, hooks, MCP boundaries, spec task execution, and revocation readiness.
- `overlays/platform/psyche/`: Psyche local-only governed agent runtime overlay focused on the deterministic authorization gate, approval as a re-check eligibility gate rather than an execution grant, non-authoritative model advisors, artifact-root containment, and computed rather than asserted conformance status. It is the first platform overlay to register an Annex A autonomy level and risk ceiling.
