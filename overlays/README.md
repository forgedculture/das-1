# Overlays

Overlays are curated hardening bundles for specific environments.

Rule
- Overlays may tighten core controls and add catalog controls.
- Overlays must not weaken core controls.

Available examples
- `overlays/regulated/pci/`: PCI-oriented hardening overlay.
- `overlays/platform/openclaw/`: OpenClaw runtime hardening overlay focused on exposed gateway, prompt injection, session isolation, and sandbox containment.
- `overlays/platform/claude-code/`: Claude Code runtime hardening overlay focused on workspace containment, shell/git authority gating, MCP boundaries, and revocation readiness.
