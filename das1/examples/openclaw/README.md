# OpenClaw overlay example artifacts

This folder contains sample evidence to exercise the `openclaw` overlay plugin.

The example drill pack includes D-OC-01 through D-OC-07 for:
- prompt injection crossing control
- proxy trust boundary integrity
- sandbox containment
- session isolation
- connector scope and rotation hygiene
- approval/exception bypass prevention
- revocation readiness and latency

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
