# Google Workspace MCP Quick Setup Reference

*Condensed setup steps from 2026-05-04 session — exact commands used to integrate taylorwilsdon/google_workspace_mcp with Hermes.*

## Prerequisites Verified
- `uv` installed at `/root/.local/bin/uv` ✓
- `mcp` Python package v1.26.0 installed in Hermes engine venv ✓
- JWT signing key generated: `openssl rand -hex 32` ✓

## Hermes Config Addition (config.yaml)
```yaml
mcp_servers:
  google_workspace:
    command: "uvx"
    args: ["workspace-mcp", "--tool-tier", "core"]
    env:
      GOOGLE_OAUTH_CLIENT_ID: "REPLACE_WITH_YOUR_CLIENT_ID"
      MCP_ENABLE_OAUTH21: "true"
      OAUTHLIB_INSECURE_TRANSPORT: "1"
      WORKSPACE_MCP_PORT: "8000"
      GOOGLE_OAUTH_REDIRECT_URI: "http://localhost:8000/oauth2callback"
      FASTMCP_SERVER_AUTH_GOOGLE_JWT_SIGNING_KEY: "bafa283417b8de7310a6e03bf0c9bc47f1d415eaf6c3d9f18f835d240e565557"
```

## User Steps (Pending)
1. Create Google Cloud OAuth Client ID (Desktop app, PKCE) at https://console.cloud.google.com/apis/credentials
2. Enable APIs: Gmail, Calendar, Drive, Docs, Sheets (links in repo)
3. Add talentbridgedubai@gmail.com as test user at https://console.cloud.google.com/auth/audience
4. Send Client ID to Hermes (format: "Client ID: xxxxxxxxxx-xxxxxxxxx.apps.googleusercontent.com")

## After Client ID Received
1. Update config.yaml with real Client ID
2. Restart Hermes gateway
3. MCP tools auto-discovered: `mcp_google_workspace_*` 
4. Auth URL generated via MCP server startup

## Repo Details (David's Research Methodology Applied)
- **Repo**: https://github.com/taylorwilsdon/google_workspace_mcp
- **Stars**: 2.3k, **Forks**: 701, **Contributors**: 106
- **Version**: v1.20.3 (2026-05-01)
- **License**: MIT, **Language**: Python 99.8%
- **PyPI**: `workspace-mcp`

## Why This Over gws CLI
- gws CLI v0.2.1: Generates invalid OAuth URLs (missing response_type) → Error 400
- google_workspace_mcp: Native OAuth 2.1, auto token refresh, 12 services, actively maintained

---
*Source: 2026-05-04 session | For full setup guide see /root/9_manuals/google_workspace_mcp_setup.md*
