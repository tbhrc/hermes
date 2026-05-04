# Repository Research Methodology (David's Method)

*Non-negotiable workflow for researching and evaluating GitHub repositories for AOS Hub tool adoption.*

## Mandatory Criteria

1. **Fork Count Threshold**: Repository MUST have **500+ forks** (minimum bar for stability/adoption)
   - Check via: `web_extract` on repo URL or `web_search` for "repo-name forks stars"
   - Verify fork count in extracted content (look for "X forks" or "forksCount" in JSON)

2. **X (Twitter) Activity Verification**: Repository MUST be actively discussed on X
   - Search: `web_search` with query `repo-name site:x.com OR site:twitter.com`
   - Look for recent posts (within 3-6 months) mentioning the repo
   - Positive signals: Tutorials, integration posts, community adoption discussions

3. **Single Discussion Document**: All findings go into ONE existing discussion file
   - Path: `/root/12_lab/3_discussions/github_tools_expansion.md`
   - NEVER create additional files — update existing doc only
   - Format: Add numbered entries with install command and verification notes

## Research Workflow

```
1. web_search: "MCP server 500 forks" or "GitHub tool 500 forks"
2. For each candidate repo:
   a. web_extract: Get repo page, verify fork count >= 500
   b. web_search: "repo-name site:x.com" to verify X activity
   c. If both pass: Add to /root/12_lab/3_discussions/github_tools_expansion.md
```

## Verified Examples (2026-05-04 Session)

- **github/github-mcp-server**: 4.1k forks, active X discussions ✅
- **wxt-dev/wxt**: 500+ forks, active X discussions ✅

## Pitfalls

- **Firecrawl Removal (2026-05-04)**: User explicitly instructed to REMOVE Firecrawl from tool list because they are self-hosting it locally on VPS. Never add tools the user is already deploying locally — check first.
- **No Duplicate Files**: User enforces single discussion document policy. Do NOT create `github_tools_v2.md` or similar — always update existing file.
- **X Verification Required**: Skipping X check invalidates the research. User explicitly requires this step.

## Install Command Preference

User prefers **non-interactive install commands** (no human intervention):
- Docker: `docker pull <image>` (non-interactive)
- npm: `npm install -g <package>` (non-interactive)
- Binary: Direct download + move to `/usr/local/bin/` (non-interactive)

Avoid: Interactive installers, `apt-get install` without `-y`, anything prompting user input.
