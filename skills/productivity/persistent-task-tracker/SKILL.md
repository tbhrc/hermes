---
name: persistent-task-tracker
description: Persistent cross-session task tracker using JSON file storage. CURRENTLY UNAVAILABLE - tasks.json deleted by user, only session-scoped todo tool remains.
---

# Persistent Task Tracker

**STATUS: UNAVAILABLE** - tasks.json deleted by user on 2026-05-03. Only session-scoped todo tool remains (no cross-session persistence).

~~Store: `/root/3_core_tools/hermes/data/tasks/tasks.json`~~ (DELETED)

## Current State
- Persistent task tracking: **DISABLED** (tasks.json deleted by user on 2026-05-03)
- Session todo tool: **ACTIVE** (resets per chat session)
- Central tasks/ folder in Pillar 3: **DELETED** (deprecated, agent-specific storage only)
- To restore: recreate tasks.json in agent workspace (e.g., A1: `/root/3_core_tools/hermes/data/tasks/tasks.json`)

## Schema
```json
{
  "schema_version": "1.0",
  "last_updated": "ISO8601",
  "tasks": [
    {
      "id": "string (unique)",
      "content": "string",
      "status": "pending|in_progress|completed|cancelled",
      "priority": "low|medium|high",
      "created_at": "ISO8601",
      "updated_at": "ISO8601",
      "tags": ["optional"]
    }
  ]
}
```

## Commands (via terminal + python/echo)

### List all tasks
```bash
cat /root/3_core_tools/hermes/data/tasks/tasks.json | python3 -m json.tool
```

### Add task
Use `patch` tool or `write_file` to append to tasks array with unique id, default status=pending, priority=medium.

### Update status
Use `patch` tool to find task by id and update status field + updated_at timestamp.

### Delete task
Use `patch` tool to remove task object from array by id.

### Filter by status
```bash
python3 -c "import json; data=json.load(open('/root/3_core_tools/hermes/data/tasks/tasks.json')); [print(t) for t in data['tasks'] if t['status']=='pending']"
```

## Workflow
1. Always update `last_updated` timestamp on any mutation.
2. Use ISO8601 format for all timestamps.
3. Generate id as `task_<incrementing_int>` or `task_<descriptive_slug>`.
4. Prefer `patch` tool over `write_file` for surgical edits.
5. After mutations, verify by reading tasks.json.

## Pitfalls
- JSON must remain valid — use `python3 -m json.tool` to validate after edits.
- Never use `sed` or `awk` on JSON — use `patch` or `write_file`.
- **Data Locality:** Task data is per-agent, stored in the agent's workspace (e.g., A1: `/root/3_core_tools/hermes/data/tasks/tasks.json`). Do not centralize task data.
- **Pillar Compliance:** Central tools live in Pillar 3 (`3_core_tools/`), agent data in their respective workspaces.
- Tasks.json path for A1 is fixed at `/root/3_core_tools/hermes/data/tasks/` — do not relocate.
