---
name: openclaw-config
description: "Deploy, configure, and migrate OpenClaw agent systems within the AOS Hub. Master reference for managing OpenClaw multi-agent architectures, channel bindings, and client migrations."
version: 1.0.0
author: A1 (Global Orchestrator)
license: MIT
metadata:
  hermes:
    tags: [openclaw, multi-agent, configuration, migration, devops, aos]
---

# OpenClaw Config Skill

Master skill for A1 (Hermes Agent) to manage OpenClaw ecosystems on behalf of AOS Hub clients.

## Central Documentation
**Read this file FIRST before any OpenClaw operation:**
`/root/9_manuals/openclaw-complete-reference.md`

## Quick Reference (Bottom Line)

### Deploy New OpenClaw Agent
1. **Choose Method:** Method 1 (multi-agent, shared gateway) vs Method 2 (separate profiles)
2. **Create Agent:** `openclaw agents add <id>` (NO --workspace flag! Set path in config)
3. **Set Workspace Path:** In `openclaw.json`: `"agents": { "defaults": { "workspace": "/path/to/workspace" } }`
4. **Bind Channels:** `openclaw agents bind --agent <id> --bind telegram:<bot_id>`
5. **Configure:** Telegram tokens, WhatsApp, Email (Microsoft Graph)
6. **Verify:** 
   ```bash
   openclaw gateway restart
   openclaw agents list --bindings
   openclaw channels status --probe
   openclaw agent --agent <id> --message "test"
   ```

### Verification Mandate (David's Rule)
**NEVER ASSUME.** Anytime you encounter existing OpenClaw documentation:
1. Search online: `web_search(query="OpenClaw <topic> official documentation")`
2. Extract: `web_extract(urls=["https://docs.openclaw.ai/..."])`
3. Compare and correct. Update docs with version + date.
4. See `hermes-agent` skill → `references/document-verification-procedure.md`

### Configure Existing Agent
- **Edit `openclaw.json`:** Agent identity, sandbox mode, memory settings
- **Sandbox Syntax (Correct):**
  ```json
  {
    "agents": {
      "defaults": {
        "sandbox": {
          "mode": "off" | "non-main" | "all",
          "scope": "agent",
          "backend": "docker"
        }
      }
    }
  }
  ```
- **Telegram DM Policy:** Default is `pairing`. Use `allowlist` with numeric `allowFrom` for owner-only access.
- **Models:** `openclaw models auth order set --agent <id> <provider>:<model>`

### Migrate Agent (e.g., M1 - Michael's Agent)
**Special Care Required:** Michael is sensitive. Previous OpenClaw had full root access.

1. **Audit:** Check existing workspace (`2_clients/2.3_michael/`) for scripts, emails, configs
2. **Backup:** `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
3. **Reconfigure:** Set workspace path in `openclaw.json` (NOT CLI flag)
4. **Sandbox Mode:** Enable `"mode": "all"` in sandbox config to prevent root access
5. **Rebind Channels:** Keep Michael's Telegram as default, configure WhatsApp
6. **Test:** 
   ```bash
   openclaw gateway restart
   openclaw channels status --probe
   openclaw agent --agent m1 --message "migration test"
   ```
7. **Test:** `openclaw gateway restart` + real message test

### VPS Resource Planning
- **Current Specs:** 2 vCPU / 8GB RAM
- **Max Recommended:** 45 agents (Method 1) or 15 agents (Method 2)
- **RAM Budget:** ~60MB per agent + 1GB base
- **Monitor:** Keep under 6GB RAM usage; upgrade to 8GB+ at 20 agents

## AOS Governance Rules
- **Registry:** Update `0_blueprints/agent_registry.md` after every agent deployment
- **Workspace Map:** Update `workspace_map.md` if new pillar folders created
- **File Registry:** Update `7_vault/REPO/file_registry.md` for new config/files
- **Isolation:** Each agent gets dedicated workspace; root `/root/` stays clean
- **No Conversion:** Migrating M1 ≠ converting to Hermes. We reconfigure OpenClaw properly.

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| Gateway dying on SSH logout | `sudo loginctl enable-linger $USER` |
| Telegram token already in use | `ps aux \| grep openclaw` → `kill -9 <PID>` → restart |
| Email sync failing (business acct) | Use Microsoft Graph OAuth with Device Code Flow |
| Agent not receiving messages | `openclaw channels status --deep` + send real test message |

## Verification Checklist
After ANY OpenClaw operation:
- [ ] `openclaw gateway restart`
- [ ] `openclaw channels status --deep`
- [ ] Send real `openclaw agent --agent <id> --message "..."` test
- [ ] Check logs: `openclaw logs --agent <id>`
- [ ] Update `agent_registry.md`

---
**Skill Maintained By:** A1 Global Orchestrator  
**Central Doc:** `/root/9_manuals/openclaw-complete-reference.md`  
**Last Updated:** May 2026
