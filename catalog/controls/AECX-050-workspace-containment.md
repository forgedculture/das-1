# AECX-050 Workspace containment

Control statement
- Agent file, object, and execution access MUST be confined to a declared workspace boundary. Actions that read, write, execute, or emit outside the declared workspace MUST be denied. Workspace escape via absolute paths, path traversal, or symlink resolution MUST be blocked before execution, not detected after.

Supplemental guidance
- The workspace boundary should be declared explicitly (root path or object scope) and resolved canonically before each tool call.
- Symlinks and hardlinks should be resolved to their real path and re-checked against the boundary.
- Read scope and write scope may differ; the narrower scope governs R3/R4 actions.
- Temporary and helper paths inherit the workspace boundary unless a narrower boundary is declared.

Assessment objectives
- Confirm a workspace boundary is declared and enforced before tool execution.
- Confirm traversal, absolute-path, and symlink escape attempts are denied and logged.
- Confirm boundary changes require review appropriate to the highest affected risk class.

Assessment methods
- Examine: workspace boundary declaration, policy snapshot, denied-escape receipts.
- Interview: workspace and policy owners.
- Test: attempt access outside the workspace via parent-directory traversal, an absolute path, and a symlink pointing outside the root.

Receipts
- Workspace boundary declaration
- Policy evaluation logs
- Denied escape receipts
- Boundary change approval record
