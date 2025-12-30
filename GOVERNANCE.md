# Governance (DAS-1(TM))

Goal
- Keep the core small and stable.
- Let profiles, overlays, and the control catalog evolve without rewriting core doctrine.

Roles
- Maintainers: approve releases, own tags, resolve disputes.
- Editors: keep docs coherent, manage reviews.
- Contributors: propose changes via PR.

Decision rule
- Consensus when possible.
- If consensus fails, maintainers decide and record rationale in spec/core/changelog.md.

Version policy
- Core: slow-moving. Breaking changes are rare and explicit.
- Catalog, profiles, overlays: faster iteration allowed.

Normative vs informative
- Core spec and conformance criteria are normative.
- Profiles, overlays, mappings, and examples are informative unless explicitly marked otherwise.
