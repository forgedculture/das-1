# OpenClaw overlay example artifacts

This folder contains sample evidence to exercise the `openclaw` overlay plugin.

Run:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/openclaw/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/openclaw/drills \
  --tool-catalogs das1/examples/tool_catalogs \
  --policy-snapshots das1/examples/policy_snapshots \
  --ir-annexes das1/examples/ir_annexes \
  --overlay openclaw \
  --report openclaw-overlay-report.json
```
