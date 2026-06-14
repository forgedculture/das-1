# AECX-068 Agent supply-chain control

Control statement
- Authority-bearing agent components SHOULD have source, owner, version, integrity, review, and update evidence. Components that can influence R3/R4 actions MUST be pinned, reviewed, and revocable before use.

Supplemental guidance
- Authority-bearing components can include models, runtimes, extensions, skills, tool endpoints, execution images, standing instructions, helper scripts, templates, retrieval sources, and workflow definitions.
- Updates should be reviewed according to the highest risk class they can influence.
- Supply-chain evidence should support rollback to a known reviewed state.

Assessment objectives
- Confirm authority-bearing components are inventoried and reviewed.
- Confirm integrity and version evidence exists for components used in high-risk workflows.
- Confirm unreviewed component updates cannot silently affect R3/R4 execution.

Assessment methods
- Examine: component inventory, version pins, review logs, integrity checks, update records.
- Interview: platform owners, security owners, workflow owners.
- Test: attempt to use an unreviewed, altered, or revoked component in a high-risk workflow.

Receipts
- Component inventory
- Integrity/hash evidence
- Review and update record
- Revocation or rollback evidence
