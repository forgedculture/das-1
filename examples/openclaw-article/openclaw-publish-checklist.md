# OpenClaw Article Publish Checklist

Date target: February 9, 2026

## Copy Readiness

- Final title selected.
- Publication date/byline set.
- Every factual claim in the article maps to `openclaw-fact-pack.md`.
- "Safe because inert" framing included (risk-proportional utility).
- No unverified screenshots or private exploit details included.

## Source Hygiene

- Advisory and release links resolve.
- OpenClaw docs links resolve (`security`, `sandboxing`).
- OpenClaw issue link resolves.
- DAS-1 overlay/core/conformance links resolve.
- Third-party reporting clearly labeled as reporting, not canonical project truth.

## Governance Framing

- Explicitly distinguish:
  - platform bug class
  - deployment misconfiguration class
  - authority-governance class
- Include D-OC-01/02/03 as concrete operational tests.
- Include R1/R2 utility posture, not only R3/R4 restrictions.
- If making a DAS-1 claim in copy, validate claim packets with:
  - `python tools/das1_verify.py verify-claims das1/examples/claims`

## Legal / Risk

- No defamatory claims against maintainers or users.
- No active exploitation instructions.
- Trademark usage follows project policy in `TRADEMARKS.md`.

## Distribution Pack

- Long-form article (`openclaw-authority-crossing.md`).
- Fact map (`openclaw-fact-pack.md`).
- One short social post:

```text
OpenClaw is a stress test for agent governance, not just model safety.
The real boundary is propose -> execute.

If you can’t prove approvals, revocation, and receipts under injection pressure,
you don’t have an assistant. You have delegated authority without controls.
```

## Final Go/No-Go

- At least one editor review completed.
- Source links checked immediately before publish.
- Publication decision logged with timestamp.
