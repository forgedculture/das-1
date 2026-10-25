# Regulated overlays

Regulated overlays describe what DAS-1(TM) must produce so an assessor under a named
compliance framework can use it as evidence. They are the third layer:

- The core AECs say what any delegated-authority system must do.
- Platform overlays say how a given technology meets that.
- Domain overlays say which actions are high-risk in a field.
- Regulated overlays say what one framework's assessment needs from the controls and their
  receipts.

Each regulated overlay has a translation table in `mappings/regulated/`. The overlay
tightens; the mapping only translates.

## Status

All regulated overlays are Informative and documentation-only:

- They are not machine-verified.
- They are not part of the DAS-1 v0.002 conformance claim set.
- Using one does not establish compliance with the framework, and MUST NOT be presented as
  doing so.

Requirement citations follow the official framework text as far as it could be checked on
the date in each file. Several official documents could not be retrieved automatically, so
each mapping marks how far it was checked. Verify against the official text before relying
on a citation for an assessment or audit.

## The overlays

- `hipaa/`: HIPAA Security, Privacy and Breach Notification Rules, for covered entities and
  business associates whose agents touch ePHI.
- `soc2/`: SOC 2, against the AICPA Trust Services Criteria, for service organizations
  whose system includes agents.
- `pci/`: PCI DSS v4.0.1, for agents in, connected to, or able to affect the cardholder data
  environment.
- `fedramp-high/`: FedRAMP High, on the NIST SP 800-53 Rev 5 High baseline, for cloud
  services whose authorization boundary includes agents.

## Rules

- The core spec governs. No overlay overwrites, replaces, relaxes or renumbers any part of
  it. A regulated overlay may only:
  - tighten a core control,
  - add catalog controls, drills and namespaced receipt fields.

  Changes to the controls themselves happen in `spec/core/`, through the decision log.
- MUST and MUST NOT in a regulated overlay bind only an adopter who chooses to use that
  overlay. They create no DAS-1 conformance obligation.
- Where the framework is stricter than DAS-1, the overlay adopts the framework's figure. An
  example is log retention.
- Where DAS-1 has a control the framework lacks, the overlay keeps it and says so. Examples
  are AEC-04 approval latency and AEC-10 cost caps.
- Overlays stack. A healthcare agent under HIPAA uses all of these, and the strictest
  applicable requirement wins:
  - the core;
  - the applicable platform overlay (any under `overlays/platform/`);
  - the `healthcare` domain overlay;
  - the `hipaa` regulated overlay.
- AEC-13 and AEC-14 are v0.003 Draft controls. They are referenced as draft and are not
  claimable.
