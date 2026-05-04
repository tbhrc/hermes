---
name: create-new-hermes-agent
description: "Deploy a new Hermes Agent instance on the AOS VPS for a new client or purpose. This skill references the central AOS documentation for detailed steps."
version: 1.0.0
author: A1 (Global Orchestrator)
license: MIT
metadata:
  hermes:
    tags: [hermes, setup, multi-agent, devops, aos]
---

# Create New Hermes Agent

This skill guides the creation of a new isolated Hermes Agent instance within the AOS Hub.

## Central Documentation
For full procedural details, **read the central documentation file first**:
`/root/9_manuals/hermes_new_agent_creation.md`

**Verification Mandate (David's Rule):**
Before using any existing documentation in AOS Hub folders:
1. Search online: `web_search(query="<topic> official documentation")`
2. Extract: `web_extract(urls=["https://docs.<site>.com/..."])`
3. Compare and correct. Update docs with version + date.
4. See `hermes-agent` skill → `references/document-verification-procedure.md`

## Quick Reference (Bottom Line)
1. **Create Data Dir**: `3_core_tools/hermes/agents/<client>/data/` or `2_clients/<folder>/workspace/`
2. **Set Path**: Ensure `HERMES_HOME` points to the new directory.
3. **Config**: Set unique gateway port, CWD, and `busy_input_mode: queue`.
4. **Register**: Update `0_blueprints/agent_registry.md` and `workspace_map.md`.
5. **Init Files**: Populate workspace with `IDENTITY.md`, `SOUL.md`, `AGENTS.md`.
6. **Start**: `hermes --profile <name> gateway start` or set `HERMES_HOME` env var.

## AOS Governance Rules
- **Root Integrity**: Do not put agent files in `/root/` directly.
- **Pillar Logic**: Use `0_blueprints/pillar_map.md` for numbering.
- **Isolation**: Each agent must have a unique port and data directory to avoid conflicts.
- **Naming Alignment**: All agent codenames must match `0_blueprints/agent_registry.md` exactly. Public codename is registry entry (e.g., a1), backend engine is Hermes. Never use "Hermes profile" as a public name.

## Verification
- `hermes gateway status`
- Check `agent_registry.md` for the new entry.
- Test message routing via the assigned platform (WhatsApp/Telegram).
