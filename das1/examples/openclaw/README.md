# OpenClaw overlay example artifacts

This folder contains sample evidence to exercise the `openclaw` overlay plugin.

Run:

```bash
python tools/das1_verify.py verify-overlay \
  --receipts das1/examples/openclaw/receipt_packs \
  --exceptions das1/examples/exceptions \
  --drills das1/examples/openclaw/drills \
  --overlay openclaw \
  --report openclaw-overlay-report.json
```
