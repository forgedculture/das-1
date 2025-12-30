# DAS-1(TM) PCI overlay v0.001 (Informative)

Prerequisite
- DAS-1(TM) v0.001 Conformant.

Tightens
- AEC-03: human gating mandatory for any action affecting payment flow integrity.
- AEC-06: preflight must declare CHD-adjacent classification and block if missing.
- AEC-07: audit trails must support reconstruction suitable for assessment.

Adds
- AECX-014 Segmentation boundary enforcement
- AECX-030 Immutable logging

Overlay drill
- D-PCI-01 Segmentation traversal test
  - Pass: disallowed traversal is blocked and logged with correlation IDs.
  - Output: test log pack and results summary.
