# AECX-051 Git egress and remote mutation control

Control statement
- Git operations that mutate remote state (push, force-push, branch or tag deletion, remote reconfiguration) are R3/R4 actions and MUST require approval and a recorded preflight. Pushes to remotes outside the declared allowlist MUST be denied.

Supplemental guidance
- Force-push and history rewrite on shared or protected branches should be treated as R4 and require human gating.
- The set of allowed remotes and branches should be declared; adding or changing a remote is itself a governed action.
- Local commits are lower risk than remote mutation; this control scopes to operations that leave the workspace or change shared state.
- Credentials used for git egress should follow AEC-09 (secrets lifecycle and rotation).

Assessment objectives
- Confirm remote-mutating git operations are gated by risk class and an allowlist.
- Confirm force-push and history rewrite on protected branches require approval.
- Confirm denied or out-of-allowlist push attempts are logged with correlation to the request.

Assessment methods
- Examine: remote allowlist, approval policy, push and preflight logs.
- Interview: repository owners and policy owners.
- Test: attempt a push to a non-allowlisted remote and a force-push to a protected branch.

Receipts
- Remote and branch allowlist
- Approval records for remote mutations
- Push preflight and execution logs
- Denied push receipts
