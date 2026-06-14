# Conformance Claim Examples

These files show how to package defensible conformance claims with required disclosures.

## Validate the claim packets

```bash
python tools/das1_verify.py verify-claims das1/examples/claims
# optional: --report claims-report.json
```

## Notes

- `pass_core_claim.json` expects a passing core report at `conformance-report.json`.
- `pass_openclaw_overlay_claim.json` expects a passing overlay report at `openclaw-overlay-report.json`.
- `pass_claude_code_overlay_claim.json` expects a passing overlay report at `claude-code-overlay-report.json`.
- `pass_codex_overlay_claim.json` expects a passing overlay report at `codex-overlay-report.json`.
- Claims are self-asserted and must include a non-certification statement.
