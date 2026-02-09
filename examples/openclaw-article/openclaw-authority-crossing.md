# Prompt Injection Is Not The Bug. Authority Crossing Is.

Paul LaPosta | Forge Signals | February 9, 2026

Tool calls are production changes. If an agent can read your messages, hold your keys, and execute actions, you are operating a delegated authority system whether you call it that or not.

OpenClaw is the current stress test for that reality. In early February 2026, a one-click RCE chain (CVE-2026-25253) was publicly disclosed and patched in `v2026.1.29` (released January 30, 2026). Around the same time, maintainers and researchers were still arguing about safer defaults for sandboxing and session isolation, and public reporting highlighted malicious extension risk in the skills ecosystem.[^1][^2][^3][^4][^5][^6][^11]

This is not a "dunk on OpenClaw" post. Upstream is shipping fixes. The governance point is simpler:

If your control plane cannot prove the boundary between `propose` and `execute`, your incident clock is already running.

## The Breach Class

### 1) Indirect prompt injection crosses into execution

Attackers control inbound text (email/DM/docs). The model reads it. Tool execution follows.

The fix is not "better prompting." The fix is authority design:
- classify exfiltration, mutation, impersonation, and host-adjacent actions as high risk;
- require human approval before execution;
- persist approval + origin + execution receipts.

In DAS-1 terms: AEC-03, AEC-06, AEC-07. In OpenClaw overlay terms: D-OC-01 must prove the chain blocks at authority crossing.[^7]

### 2) Reverse-proxy trust collapses localhost assumptions

"Local only" deployments often become remotely reachable through proxy topology mistakes.

OpenClaw docs explicitly call out `trustedProxies` and request provenance handling. Overlay drill D-OC-02 exists to prove remote clients cannot inherit localhost trust.[^5][^7]

### 3) Session collapse creates cross-user bleed

If multi-user traffic shares context state, one sender can poison or influence another sender's authority path.

OpenClaw's own issue discussions call out that stronger session isolation and sandbox defaults matter. DAS-1 overlay hardening requires per-peer or tighter session scope for multi-user contexts.[^3][^4][^7]

### 4) Host execution and connector overreach turn mistakes into incidents

When tools execute on host and connectors carry broad scopes, one bad completion becomes real compromise.

OpenClaw sandboxing guidance is clear: sandbox is a boundary, not a style preference. Overlay hardening adds connector segmentation, revocation drills, and bounded exceptions with expiry.[^6][^7]

## The DAS-1 Move

DAS-1 is useful here because it is not model-theater. It is control-plane discipline:
- explicit risk classes;
- approval and preflight linkage for high risk actions;
- revocation drills with receipts;
- exceptions that expire;
- measurable metrics from stored evidence.

The recent utility update matters: controls must be risk-proportional. R1/R2 should remain autonomous under policy; R3/R4 stays gated. "Safe because inert" is not conformance.[^8][^9][^10]

## What To Do In 72 Hours

1. Patch and pin
- Move to a fixed OpenClaw release line (`v2026.1.29` or newer) and record version evidence.

2. Enforce authority crossing gates
- Mark destructive/exfiltrating/impersonating actions as high risk.
- Require explicit approval + preflight for those actions.

3. Tighten topology and session boundaries
- Validate proxy trust config.
- Force isolated DM/session scope in multi-user contexts.

4. Contain execution blast radius
- Sandbox non-main/untrusted sessions.
- Keep host-elevated execution behind explicit, time-bounded emergency pathways.

5. Run drills before you publish "secure"
- D-OC-01 prompt-injection authority crossing.
- D-OC-02 reverse-proxy trust boundary.
- D-OC-03 sandbox containment.

## Ends, Means, Price

Ends: prevent silent authority crossing into harmful action.  
Means: measurable controls, receipts, and drills.  
Price: slower demos, more approvals, real operator discipline.

That price is still cheaper than incident response.

---

## Sources

[^1]: OpenClaw one-click RCE reporting and CVE context: https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html
[^2]: OSV advisory entry (`GHSA-g8p2-7wf7-98mq` / `CVE-2026-25253`): https://osv.dev/vulnerability/GHSA-g8p2-7wf7-98mq
[^3]: OpenClaw maintainers discussing safer defaults (`sandbox.mode`, `dmScope`): https://github.com/openclaw/openclaw/issues/7827
[^4]: OpenClaw release line including `v2026.1.29`: https://github.com/openclaw/openclaw/releases/tag/v2026.1.29
[^5]: OpenClaw gateway security guidance (`trustedProxies`): https://docs.openclaw.ai/gateway/security
[^6]: OpenClaw sandboxing guidance: https://docs.openclaw.ai/gateway/sandboxing
[^7]: DAS-1 OpenClaw overlay: https://github.com/forgedculture/das-1/blob/main/overlays/platform/openclaw/overlay.md
[^8]: DAS-1 core spec (risk proportionality + utility guardrails): https://github.com/forgedculture/das-1/blob/main/spec/core/das-1-core.md
[^9]: DAS-1 conformance criteria (M1-M7, additive overlays): https://github.com/forgedculture/das-1/blob/main/spec/conformance/conformance-criteria.md
[^10]: DAS-1 conformance tooling and verifier flow: https://github.com/forgedculture/das-1/blob/main/spec/conformance/README.md
[^11]: Skills ecosystem risk reporting: https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare
