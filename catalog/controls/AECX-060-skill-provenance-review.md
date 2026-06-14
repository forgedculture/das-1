# AECX-060 Skill provenance and review

Control statement
- Reusable agent skills SHOULD have owners, source records, version identifiers, integrity evidence, allowed domains, review status, and review cadence. Skills that can influence R3/R4 actions MUST be reviewed before use and MUST have a revocation path.

Supplemental guidance
- Treat skills as authority-bearing artifacts when they carry operational instructions, helper code, templates, data access patterns, tool declarations, or decision procedures.
- Review should cover both human-readable instructions and executable/supporting files.
- High-impact environments should pin skill versions and prevent unreviewed automatic updates.

Assessment objectives
- Confirm skills are inventoried with owner, source, version, and allowed scope.
- Confirm reviewed skills can be distinguished from draft or untrusted skills.
- Confirm skill revocation prevents future invocation.

Assessment methods
- Examine: skill inventory, review records, version history, integrity checks, revocation procedure.
- Interview: skill owners, operators, approvers.
- Test: attempt to invoke an unreviewed or revoked skill and confirm denial or quarantine.

Receipts
- Skill inventory
- Review record
- Integrity/hash evidence
- Revocation test result
