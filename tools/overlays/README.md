# Overlay Verifier Plugins

Purpose
- Keep DAS-1 core verification runtime-agnostic while allowing overlays to add runtime-specific checks.

Plugin contract
- File name: `<overlay_id>.py` where hyphens in `overlay_id` are replaced with underscores.
- Export function:
  - `run_overlay_checks(context, load_json_records, parse_iso8601_aware) -> dict`
- `context` fields:
  - `overlay_id`, `receipts_path`, `exceptions_path`, `drills_path`, `schemas_path`, `now_utc`, `max_age_days`
- Return object:
  - `failures`: list of `{file, message, pointer?, kind?}`
  - `details`: optional object included in report output

Usage
- Core only:
  - `python tools/das1_verify.py verify --receipts ... --exceptions ... --drills ...`
- Core + overlay plugin checks:
  - `python tools/das1_verify.py verify-overlay --receipts ... --exceptions ... --drills ... --overlay openclaw`
  - `python tools/das1_verify.py verify-overlay --receipts ... --exceptions ... --drills ... --overlay claude-code`
  - `python tools/das1_verify.py verify-overlay --receipts ... --exceptions ... --drills ... --overlay codex`

Reference plugins
- `openclaw.py` for overlay id `openclaw`
- `claude_code.py` for overlay id `claude-code`
- `codex.py` for overlay id `codex`
