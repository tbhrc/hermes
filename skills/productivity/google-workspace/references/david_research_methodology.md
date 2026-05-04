# David's Research Methodology (Condensed)

## Core Workflow for Tool Discovery

1. **GitHub Direct Search**: Go to GitHub directly, search for tool name. Look for "hot moving and active" repos (recent commits, latest release).

2. **Star/Fork Thresholds**: Prioritize repos with >500 stars or >1000 forks. High community adoption = maturity.

3. **MCP Ecosystem First**: For tool integrations, search: `web_search "MCP <tool> server"` or GitHub search `<tool> mcp`. Hermes has native-mcp skill — use it.

4. **X/Twitter Social Validation**: Use `xurl` skill to search X/Twitter for repo discussions. Check community sentiment.

5. **Full Content Verification**: Use `web_extract` (full page, up to 5000 chars) NOT `web_search` (snippets). Snippets miss critical details (e.g., Pinecone free tier).

6. **No Blind Skill Adherence**: Pre-loaded skills are references, not absolute truth. Check for newer alternatives.

## Example: Google Workspace MCP

- **David's Find**: 7 seconds to locate https://github.com/taylorwilsdon/google_workspace_mcp via GitHub direct search
- **Repo Stats**: 2.3k stars, 701 forks, 106 contributors, v1.20.3 (2026-05-01)
- **My Mistake**: Followed pre-loaded google-workspace skill (broken gws CLI v0.2.1) without checking MCP repos first
- **Correct Workflow**: Check MCP repos → validate stats → use native-mcp skill → avoid broken CLIs

## Agent Compliance

All research tasks must follow this methodology. Agents that repeat missed-MCP or web_search-snippet mistakes will have their skill references patched.

---
*Full doc: /root/9_manuals/david_research_methodology.md v1.0.0 (2026-05-04)*
