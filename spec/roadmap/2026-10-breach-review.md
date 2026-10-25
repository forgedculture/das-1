# DAS-1 Breach Review, October 2026

Status: Informative. No normative change.
Date: 2026-10-25
Scope: DAS-1 v0.002 (released) and v0.003 (Draft), tested against 34 public AI agent
incidents from 2025-01 to 2026-10-25.

## 1. Question

For each incident: had the DAS-1 controls as written been fully implemented, would they have
stopped it?

## 2. Answer

Yes, for every incident in scope.

- Each one was an implementation failure: a control that was not deployed, was switched off,
  or was enforced somewhere other than where the consequence happened. None revealed a gap in
  the specification.
- Maintainer decision, 2026-10-25: the spec is clear on each class below, and no change to the
  core, conformance criteria or schemas follows from this review. See `tasks/decisions.md`.

Two incidents are out of scope, because DAS-1 governs authority that an operator delegates.
When the operator is the attacker, the operator's controls are absent by design:

- 13, a state-sponsored espionage campaign run through Claude Code (GTG-1002);
- 34, criminal intrusion agents built on Claude Code.

## 3. What each class shows about implementation

### Content the agent reads was obeyed

Incidents 2, 4, 11, 12, 14, 16, 17, 22, 24 and 28.

**The controls:** AEC-08 allowed paths and AEC-03 approval govern the consequence, whatever
talked the agent into it.

**How implementations failed:**

- One credential could both read private data and write public data, so no allowed-path rule
  existed in practice.
- Approval was switched off.
- Ways data could leave were never counted as destinations, for example an image fetched when
  a reply rendered.

### Approval was removed or replaced

Incidents 2, 7, 26, 28 and 33.

**The control:** AEC-03 requires explicit human approval for R3/R4.

**How implementations failed:**

- "Always allow" was on.
- Safety-off flags were used.
- Auto modes replaced the human with a classifier.
- In entry 33, both approvers' credentials were held where an attacker could take them.
  Several products ship these modes on by default.

### Secrets within the agent's reach

Incidents 7, 10, 16, 17, 23, 29, 30 and 33.

**The controls:** AEC-02 least privilege and AEC-09 attributable, logged secret access.

**How implementations failed:** agents could read the following without any of it being
scoped or logged:

- host files;
- inherited build environments;
- cloud instance metadata;
- their own transcripts.

### The reviewed component was not the executed one

Incidents 1, 5, 9, 15, 22 and 31.

**The controls:** AEC-01 and AECX-068 (components that can influence R3/R4 actions are
pinned, reviewed and revocable).

**How implementations failed:**

- Skills fetched their instructions at run time.
- A pin was bypassed by a branch named like the pinned hash.
- Instruction files carried content reviewers could not see.
- Packages and servers were installed with no provenance.

### Isolation that was not isolation

Incidents 20 and 23.

**The control:** Annex A defines A0 as no effect on real systems.

**How implementations failed:** environments relied on as isolated were not. One had an
internet path through a proxy flaw. Another mounted the whole host filesystem into its VM.

### Detection and controls that stopped

Incidents 20 and 25.

**The controls:** AEC-12 detection, and AEC-11 for deliberately disabled controls.

**How implementations failed:** monitoring was off or thin, so unsanctioned actions ran for
days to months.

### What the agent said instead of what it did

Incidents 6 and 21.

**The control:** AEC-07 records every tool call.

**How implementations failed:** what the agent reported was taken in place of what the
platform recorded.

### Long-lived and stale credentials

Incidents 8, 18, 19 and 32.

**The controls:** AEC-02 time-bounding and no shared long-lived credentials; AEC-10 caps.

**How implementations failed:**

- Long-lived OAuth tokens were held by third parties.
- A former contributor still had publish rights.
- Provider keys were stored with no spend cap.

## 4. Overlay guidance

Implementation detail belongs in overlays. These are candidate additions, for review against
each overlay:

### claude-code

- **Auto Mode:** not AEC-03 approval. Running it for R3/R4 work needs an AEC-11 exception.
  (26)
- **Plugin installs:** verify that the executed commit is the pinned one. (31)
- **Desktop preview pane:** count it as a way out for data and as an execution path. (30)
- **Cowork local VM:** the host mount scope is part of the A0 claim. (23)
- **CI review and triage actions on untrusted issues and PRs:** keep runner secrets out of
  reach. (16, 17)
- **Transcripts and response logs:** they are in AEC-09 scope. (33)

### codex and cursor

- Full-auto and auto-run modes need an AEC-11 exception for R3/R4 work. (7)
- Cursor rules files are reviewed with invisible characters shown. (1)

### kiro

- Steering files and hooks are reviewed the same way. (1)

### openclaw

- **Skills from the public registry:** AECX-068 provenance. (15)
- **Gateway exposure:** add CVE-2026-25253. (15)
- **Credentials:** plaintext credentials in the default layout fail AEC-09. (15)

### MCP profile

- Pin server versions. (9)
- Per-tool "always allow" is an AEC-03 bypass. (2)
- A token that can read private data and write public data is the composition AEC-14 governs.
  (2)

### Candidate new platform overlays

These platforms have incidents but no overlay:

- GitHub Copilot agent and CLI: 1, 17, 28.
- Gemini CLI and Antigravity: 7, 14, 17.
- Agentic browsers: 12, 14.
- Microsoft 365 Copilot: 4, 24.
- Amazon Q and Bedrock AgentCore: 5, 29.

## 5. Effect on v0.003

None. These incidents are implementation failures, so they say nothing either way about the
v0.003 findings. The section 8 gate of the v0.003 findings stands as written.

## Appendix: incident register

Sources are listed by number below the table. Entries marked [S] were found in search results
but not opened. Entries 20, 21, 26, 31 and 33 were rechecked against their sources on
2026-10-25.

| # | Date | Incident | Control not implemented |
|---|---|---|---|
| 1 | 2025-03 | Rules File Backdoor (Cursor, Copilot) | AEC-01, AECX-069 |
| 2 | 2025-05 | GitHub MCP: public issue leads the agent to leak private repos | AEC-08, AEC-03 |
| 3 | 2025-06 | Asana MCP cross-tenant exposure [S] | AEC-08, AECX-063 |
| 4 | 2025-06 | EchoLeak, M365 Copilot [S] | AEC-08 |
| 5 | 2025-07 | Amazon Q extension wiper prompt | AECX-068 |
| 6 | 2025-07 | Replit deletes a production DB in a freeze | AEC-03, AEC-06, AEC-07 |
| 7 | 2025-08 | Nx s1ngularity drives local agent CLIs | AEC-03, AEC-09 |
| 8 | 2025-08 | Salesloft Drift OAuth theft [S] | AEC-02 |
| 9 | 2025-09 | postmark-mcp BCCs all mail | AECX-068 |
| 10 | 2025-09, 2025-11 | Shai-Hulud npm worm | AEC-02, AEC-09 |
| 11 | 2025-10 | A2A session smuggling (research) | AEC-08, AEC-13 |
| 12 | 2025-10 | CometJacking [S] | AEC-08 |
| 13 | 2025-11 | GTG-1002 espionage with Claude Code | Out of scope |
| 14 | 2025-11 | Antigravity exfiltration | AEC-08, AEC-13 |
| 15 | 2026-01/02 | OpenClaw gateways and ClawHavoc skills | AEC-09, AECX-068 |
| 16 | 2026-02 | Clinejection [S] | AEC-08, AEC-09 |
| 17 | 2026-04 | Comment and Control | AEC-08, AEC-09 |
| 18 | 2026-05 | Composio breach | AEC-02, AEC-09 |
| 19 | 2026-06 | Mastra npm compromise | AEC-02 |
| 20 | 2026-05 to 10 | OpenAI evaluation agents attack Hugging Face and others | Annex A, AEC-12 |
| 21 | 2026-06 | OpenAI agent pays from an unprovided wallet | AEC-01, AEC-10, AEC-07 |
| 22 | 2026-07 | Malicious skills on skills.sh [S] | AECX-068, AEC-08 |
| 23 | 2026-07 | Claude Cowork SharedRoot | Annex A, AEC-09 |
| 24 | 2026-07 | Copilot for Word worm | AEC-08 |
| 25 | 2026-07 | UK AISI agents act on the live internet | AEC-11, AEC-12 |
| 26 | 2026-08 | Claude Code Auto Mode bypass | AEC-03 |
| 27 | 2026-10 | Grok CFO agent posts bank data [S, unconfirmed] | AEC-08 |
| 28 | 2026-10 | Copilot CLI encrypted-context injection | AEC-08, AEC-03 |
| 29 | 2026-10 | AgentCorruption, Bedrock AgentCore | AEC-02, AEC-09 |
| 30 | 2026-10 | SneakPeek, Claude Code Desktop preview | AEC-08, AEC-09 |
| 31 | 2026-10 | CVE-2026-86063 plugin pin bypass | AECX-068 |
| 32 | 2026-10 | OpenCode Console key theft | AEC-10, AEC-02 |
| 33 | 2026-10 | LiteLLM 1.107.0 trojanised | AEC-03, AEC-09 |
| 34 | 2026-10 | CrowdStrike: Claude Code intrusion agents | Out of scope |

Sources:

1. https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents
2. https://invariantlabs.ai/blog/mcp-github-vulnerability
3. https://bleepingcomputer.com/news/security/asana-warns-mcp-ai-feature-exposed-customer-data-to-other-orgs/
4. https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html
5. https://bleepingcomputer.com/news/security/amazon-ai-coding-agent-hacked-to-inject-data-wiping-commands
6. https://www.eweek.com/news/replit-ai-coding-assistant-failure/
7. https://www.wiz.io/blog/s1ngularity-supply-chain-attack
8. https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift
9. https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
10. https://www.elastic.co/blog/shai-hulud-worm-2-0-updated-response
11. https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/
12. https://thehackernews.com/2025/10/cometjacking-one-click-can-turn.html
13. https://www.anthropic.com/news/disrupting-AI-espionage
14. https://simonwillison.net/2025/Nov/25/google-antigravity-exfiltrates-data/
15. https://conscia.com/blog/the-openclaw-security-crisis/
16. https://simonwillison.net/2026/Mar/6/clinejection/
17. https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026
18. https://material.security/resources/the-composio-breach-one-token-10242-doors
19. https://thehackernews.com/2026/06/144-mastra-npm-packages-compromised-via.html
20. https://huggingface.co/blog/security-incident-july-2026 and https://www.theregister.com/security/2026/10/02/openai-alerts-100-orgs-that-its-misaligned-models-attempted-to-break-in-or-worse/5300891
21. https://fortune.com/2026/10/16/openai-discloses-four-more-rogue-incidents-involving-financial-medical-and-government-data/
22. https://www.csoonline.com/article/4206851/trojanized-ai-skills-gain-1-7m-installs-in-agent-targeted-attack.html
23. https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html
24. https://www.theregister.com/security/2026/07/29/word-worm-crawls-into-copilot-spreads-chaos/5280588
25. https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing
26. https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/
27. https://cybernews.com/ai-news/grok-bot-leaks-bank-information/
28. https://adversa.ai/blog/cryptographic-context-injection-github-copilot/
29. https://labs.zenity.io/post/agentcorruption-how-a-single-prompt-collapsed-the-entire-cloud-security-model
30. https://noma.security/noma-labs/sneakpeek-how-the-preview-pane-in-claude-code-desktop-can-exfiltrate-your-data
31. https://github.com/advisories/GHSA-pq7j-f95f-qfcv
32. https://techcrunch.com/2026/10/19/hackers-hit-ai-coding-tool-opencode-running-up-charges-on-users-ai-accounts/
33. https://www.wiz.io/blog/litellm-compromised-steals-credentials
34. https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/
