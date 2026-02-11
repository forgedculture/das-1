# Claude Code overlay example artifacts

This folder contains sample evidence to exercise the `claude-code` overlay plugin.

The example drill pack includes:
- D1 and D2 core required drills
- D-CC-01 through D-CC-09 overlay drills

Run:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/claude-code/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/claude-code/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --overlay claude-code \
  --report claude-code-overlay-report.json
```
