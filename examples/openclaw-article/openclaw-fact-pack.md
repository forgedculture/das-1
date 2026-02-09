# OpenClaw Article Fact Pack (Feb 9, 2026)

Use this as the editorial fact map for publication claims.

## Claim Map

1. Claim
`CVE-2026-25253` / `GHSA-g8p2-7wf7-98mq` was publicly disclosed in early Feb 2026 and is tied to one-click RCE reporting.
Evidence
- OSV advisory entry: https://osv.dev/vulnerability/GHSA-g8p2-7wf7-98mq
- Public report: https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html

2. Claim
OpenClaw published a fix line including `v2026.1.29` (January 30, 2026).
Evidence
- Release page: https://github.com/openclaw/openclaw/releases/tag/v2026.1.29

3. Claim
Maintainers/participants documented safety-default concerns around sandbox and session isolation.
Evidence
- Issue #7827: https://github.com/openclaw/openclaw/issues/7827

4. Claim
Gateway trust boundaries are configuration-sensitive (`trustedProxies`).
Evidence
- OpenClaw gateway security docs: https://docs.openclaw.ai/gateway/security

5. Claim
Tool execution containment is policy/config dependent (sandboxing behavior).
Evidence
- OpenClaw sandboxing docs: https://docs.openclaw.ai/gateway/sandboxing

6. Claim
DAS-1 OpenClaw overlay codifies drills D-OC-01/02/03 and control tightening for this breach class.
Evidence
- Overlay doc: https://github.com/forgedculture/das-1/blob/main/overlays/platform/openclaw/overlay.md

7. Claim
DAS-1 now includes utility guardrails and risk-proportional conformance metrics (`M1-M7`), not just lock-down controls.
Evidence
- Core spec: https://github.com/forgedculture/das-1/blob/main/spec/core/das-1-core.md
- Conformance criteria: https://github.com/forgedculture/das-1/blob/main/spec/conformance/conformance-criteria.md

8. Claim
Public reporting also flags extension ecosystem risk.
Evidence
- The Verge report: https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare

## Date Anchors To Use In Copy

- `January 30, 2026`: OpenClaw `v2026.1.29` release date signal.
- `February 2, 2026`: OSV advisory publication date for `GHSA-g8p2-7wf7-98mq` (`CVE-2026-25253`).
- `February 4, 2026`: OpenClaw issue #7827 opened (default safety posture discussion).
- `February 9, 2026`: article publication date.

## Editorial Guardrails

- Distinguish verified project docs/advisories from third-party reporting.
- Avoid claims that all OpenClaw deployments are vulnerable; claim that insecure deployments exist at scale and require governance.
- Frame fixes as control-plane failures (`propose -> execute` boundary), not model-intelligence failures.
