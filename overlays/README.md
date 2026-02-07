# Overlays

Overlays are curated hardening bundles for specific environments.

Rule
- Overlays may tighten core controls and add catalog controls.
- Overlays must not weaken core controls.

Available examples
- `overlays/regulated/pci/`: PCI-oriented hardening overlay.
- `overlays/platform/openclaw/`: OpenClaw runtime hardening overlay focused on exposed gateway, prompt injection, session isolation, and sandbox containment.
