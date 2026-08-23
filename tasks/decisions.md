# DAS-1 Agent + Skills Refresh Decisions

- 2026-05-19: Create a planning spec before changing normative core language.
- 2026-05-19: Preserve the DAS-1 design rule that the core remains closed at 12 controls unless a later explicit review approves a core revision.
- 2026-05-19: Keep AEC and generic AECX control intent vendor-neutral and technology-neutral; apply concrete products, protocols, files, settings, and runtime behaviors through overlays.
- 2026-05-19: Model skills as authority-bearing artifacts when they carry executable instructions, helper code, templates, connectors, or tool access.
- 2026-05-19: Model steering docs, custom instructions, rulesets, memories, personalizations, and workflow customizations as standing instruction artifacts when they load by default or shape default agent behavior.
- 2026-05-19: Prefer governed default rulesets over repeated prompting; each platform overlay should name the exact files/settings a tool uses for default rules and prove they load before execution.
- 2026-05-19: Model coding agents as high-variance delegated-authority runtimes because repository content, command execution, repository operations, tool brokers, secrets, and CI/CD boundaries can all become authority paths.
- 2026-05-19: Cover business, healthcare, law, finance, voting/elections, government, and military through overlays or mappings rather than one generic regulated appendix.
- 2026-05-19: Keep this pass to documentation/spec planning; schema, verifier, examples, and conformance changes are future tasks.

## v0.003 (enterprise load)

- 2026-08-20: Accept the v0.003 enterprise-load backlog as a full version rather than shipping parts as v0.002 errata. Errata would retroactively invalidate AEC-10 evidence for existing v0.002 claims; a version bump does not.
- 2026-08-20: Explicitly reopen the core, overriding the 2026-05-19 decision to keep it closed at 12 controls. The reopen is bounded to the two additions justified by the enterprise-load review and does not license further core growth.
- 2026-08-20: Place the classification procedure and composition rule in a new AEC-14 rather than as a normative procedure in section 2, because every evidence obligation in DAS-1 hangs from an AEC control and this one carries a receipt.
- 2026-08-20: Ship the autonomy dimension as normative Annex A rather than a control, because it is vocabulary and a binding rule with no receipt of its own; autonomy evidence surfaces through AEC-01 and AEC-13.
- 2026-08-20: State the composition rule as an obligation to have an answer rather than a detection algorithm, to keep the core vendor-neutral. Detection mechanics belong in overlays.
- 2026-08-20: AEC-13 supersedes the authority portions of AECX-064, and AEC-10 supersedes the spend portion of AECX-067. Both catalog controls are narrowed to their remainder rather than deleted, so v0.002 implementations keep a stable reference.
- 2026-08-20: Core delegation evidence gets first-class receipt schema fields rather than riding in `overlay_context`. That field is namespaced per overlay and is the wrong home for a core control, which supersedes the 2026-06-14 note that no schema change was required.
- 2026-08-20: The findings rest on a single enterprise adoption (n=1). v0.003 stays Draft and unreleased until a second independent adoption either confirms the gaps or falsifies them per section 8 of the backlog.
- 2026-08-20: Support two versions at once in the verifier rather than migrating everything to v0.003. `--das-version` defaults to v0.002 so the five platform overlay packs and all existing claims keep passing unchanged. Forcing a migration would have broken the promise that v0.002 claims stay valid.
- 2026-08-20: Build the v0.003 evidence as a separate pack under das1/examples/v0003/ instead of mutating the v0.002 pack, so released-version evidence is untouched by draft work.
- 2026-08-20: Require negative tests for every new machine check (tools/test_v0003_checks.py) and gate them in CI. Fixtures built to pass only show the checks do not false-positive; they say nothing about whether the checks fire. This mirrors the rule that a control needs a receipt and a drill.
- 2026-08-20: Claim packets are gated by the das_version they declare, not by a verifier flag, so a v0.003 claim cannot be produced from a v0.002 evidence run.
