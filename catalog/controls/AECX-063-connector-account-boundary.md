# AECX-063 Connector and account boundary

Control statement
- External connectors SHOULD be scoped to explicit user, workflow, tenant, account, data-class, and action boundaries. Connectors that can access sensitive data or mutate external state MUST be least-privilege, attributable, independently revocable, and denied outside declared scope.

Supplemental guidance
- Connector authority should not silently inherit broad human account privileges.
- Shared connector credentials should be avoided; where unavoidable, compensating controls should be recorded as exceptions.
- Connector scope should be visible in tool catalogs and receipts.

Assessment objectives
- Confirm connectors are inventoried with owner, identity, scopes, data classes, and revocation path.
- Confirm connector access is least-privilege and attributable.
- Confirm out-of-scope connector actions are blocked and logged.

Assessment methods
- Examine: connector inventory, account scopes, permission grants, access logs, revocation records.
- Interview: connector owners, operators, identity administrators.
- Test: attempt out-of-scope reads, writes, exports, and post-revoke reuse.

Receipts
- Connector inventory
- Scope manifest
- Access and attribution logs
- Revocation test evidence
