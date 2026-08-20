# Governance (DAS-1(TM))

## Current state, stated plainly

DAS-1 has one maintainer, Paul LaPosta. The role structure below describes how the project is intended to operate as it grows. Today, every role resolves to the maintainer, and pretending otherwise would be governance theater.

What that means for adopters:

- Decisions and their rationale are logged in spec/core/changelog.md, so the record does not depend on the maintainer's memory or availability.
- Adopters should pin a version rather than track main. The spec gives this advice to everyone; it applies double to a sole-maintainer project.
- The spec and documentation are CC BY 4.0 and the tooling is Apache 2.0, both irrevocable for published versions. If this project is abandoned or contested, any adopter can continue, fork, or rename their pinned profile without permission.
- The maintainer's interpretation of the spec is not privileged over the spec text. Where an adopter's reading of the published text and the maintainer's intent diverge, the text governs until a released revision says otherwise.

The single-maintainer state is a concentration risk, and the mitigations are the four points above, not a promise of team growth. A second maintainer will be named when a real one exists, not before.

## Goal

- Keep the core small and stable.
- Let profiles, overlays, and the control catalog evolve without rewriting core doctrine.

## Roles

- Maintainers: approve releases, own tags, resolve disputes.
- Editors: keep docs coherent, manage reviews.
- Contributors: propose changes via PR.

## Decision rule

- Consensus when possible.
- If consensus fails, maintainers decide and record rationale in spec/core/changelog.md.
- While the project has a sole maintainer, "consensus" means contributor input is read and answered in the PR record before a decision is logged.

## Version policy

- Core: slow-moving. Breaking changes are rare and explicit.
- Catalog, profiles, overlays: faster iteration allowed.

## Normative vs informative

- Core spec and conformance criteria are normative.
- Profiles, overlays, mappings, and examples are informative unless explicitly marked otherwise.

## Conflict-of-interest rule for adoptions

Where the maintainer proposes DAS-1 adoption inside an organization that employs or pays the maintainer, that proposal must disclose the authorship relationship, and conformance to DAS-1 within that organization may not be solely assessed by the maintainer. This rule exists because the first enterprise adoption was exactly this case, and the pattern will recur.
