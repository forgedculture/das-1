# AECX-052 MCP trust segmentation

Control statement
- Model Context Protocol (MCP) servers and the tools they expose MUST be trust-classified before use. Untrusted or unverified MCP servers MUST NOT reach high-risk tools, secrets, or R3/R4 actions. MCP tool invocations MUST be bounded by policy and logged with the invoking server identity.

Supplemental guidance
- Each MCP server should carry a trust class derived from provenance (origin, signature, review) per AEC-01 and AECX-068.
- Tool exposure should be least-privilege: an MCP server receives only the tools, data classes, and destinations its trust class permits.
- Newly added or changed MCP servers should be treated as a governed change, not silently trusted.
- Cross-server data flow (one MCP server's output feeding another server's high-risk action) should be segmented and reviewed.

Assessment objectives
- Confirm MCP servers are trust-classified before invocation.
- Confirm untrusted servers cannot reach high-risk tools, secrets, or R3/R4 actions.
- Confirm MCP invocations are bounded by policy and logged with server identity.

Assessment methods
- Examine: MCP server registry with trust classes, policy snapshot, invocation logs.
- Interview: MCP integration and policy owners.
- Test: register an untrusted MCP server and attempt a high-risk tool call; confirm denial and log.

Receipts
- MCP server registry with trust classification
- Policy evaluation logs
- Denied MCP invocation receipts
- MCP server change approval record
