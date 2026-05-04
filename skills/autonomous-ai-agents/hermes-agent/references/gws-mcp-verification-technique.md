# GWS MCP Setup Technique — Lessons from 2026-05-04

## Problem
Initial attempt with `gws` CLI failed due to OAuth URL bug (missing `response_type`), causing 400 Authorization Error. Switched to `taylorwilsdon/google_workspace_mcp` (MCP-based).

## Correct Venv Path Discovery

Hermes venv may NOT be `.venv/` — always discover the actual path:

```bash
# Method 1: Use which hermes to find the binary, then trace to venv
which hermes
# Output: /root/3_core_tools/hermes/engine/venv/bin/hermes
# Venv path: /root/3_core_tools/hermes/engine/venv/

# Method 2: List directory to confirm
ls -la /root/3_core_tools/hermes/engine/ | grep -E "venv|\.venv"
```

**Lesson**: Hermes venv is `/root/3_core_tools/hermes/engine/venv/` (NOT `.venv/`).

## Correct Package Installation

Do NOT use `pip install` directly — the venv may not have pip module:

```bash
# WRONG — fails with "No module named pip"
/root/3_core_tools/hermes/engine/venv/bin/pip install mcp

# CORRECT — use uv pip install with explicit python path
uv pip install --python /root/3_core_tools/hermes/engine/venv/bin/python mcp

# Verify installation
/root/3_core_tools/hermes/engine/venv/bin/python -c "import mcp; print('mcp module found:', mcp)"
```

**Lesson**: Use `uv pip install --python <venv-bin-python> <package>` for Hermes venv.

## Config.yaml Structure (Correct)

```yaml
mcp_servers:
  google_workspace:
    command: "uvx"
    args: ["workspace-mcp", "--tool-tier", "core"]
    env:
      GOOGLE_OAUTH_CLIENT_ID: "PLACEHOLDER_REPLACE_WITH_YOUR_CLIENT_ID"
      FASTMCP_SERVER_AUTH_GOOGLE_JWT_SIGNING_KEY: "<32-hex-chars>"
```

**Wrong env vars to avoid** (removed from config during fix):
- `MCP_ENABLE_OAUTH21` (typo, not valid)
- `OAUTHLIB_INSECURE_TRANSPORT` (not needed for production)
- `WORKSPACE_MCP_PORT` (not needed, uses default)
- `GOOGLE_OAUTH_REDIRECT_URI` (not needed, uses default)

**Generate JWT signing key**:
```bash
openssl rand -hex 32
```

## Verification Steps

Always verify each step before claiming completion:

```bash
# 1. Verify mcp installed
/root/3_core_tools/hermes/engine/venv/bin/python -c "import mcp"

# 2. Verify config.yaml has correct section
grep -A 10 "google_workspace:" /root/3_core_tools/hermes/data/config.yaml

# 3. Verify env vars are correct (only CLIENT_ID placeholder + JWT key)
grep -A 5 "env:" /root/3_core_tools/hermes/data/config.yaml | grep -A 5 "google_workspace"
```

## Common Mistakes (Pitfalls)

1. **Claiming mcp installed without verifying** — User will catch fake claims immediately
2. **Wrong venv path** — Assuming `.venv/` exists when it's `venv/`
3. **Using pip instead of uv** — Fails when pip module not in venv
4. **Wrong env var names** — Typos like `OAUTH21` instead of correct names
5. **Not removing stale env vars** — Keep config clean, only necessary vars

## References

- GWS MCP Repo: https://github.com/taylorwilsdon/google_workspace_mcp
- Hermes native-mcp skill: `skill_view(name='native-mcp')`
- User must create OAuth Client ID (Desktop app, PKCE) at https://console.cloud.google.com/apis/credentials
