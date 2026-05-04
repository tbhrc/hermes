---
name: messaging-data-parsing
description: Class-level skill for parsing messaging platform data (WhatsApp, Telegram, Email) into SQLite databases with crash prevention, batch operations, and AI training preparation.
---

# Messaging Data Parsing Skill v1.0.0 (2026-05-04)

*Parse WhatsApp, Telegram, and Email data into SQLite databases for AI training and analysis.*

## Trigger Conditions
Load this skill when:
1. Creating databases for messaging data (WhatsApp, Telegram, Email)
2. Parsing .jsonl session files from OpenClaw agents
3. Setting up SQLite databases with crash prevention
4. Preparing messaging data for AI training

## Core Workflow

### 1. Database Creation with Crash Prevention
Always use these settings for messaging DBs:
```sql
PRAGMA journal_mode=WAL;  -- Write-Ahead Logging for crash safety
PRAGMA synchronous=NORMAL;  -- Balance safety vs performance
```

**Why WAL mode:**
- Allows concurrent reads during writes
- Better crash recovery than default rollback journal
- Critical for avoiding corruption during large inserts

### 2. Schema Design Rules
- Use `INTEGER PRIMARY KEY AUTOINCREMENT` for IDs
- Add `created_at INTEGER DEFAULT (strftime('%s','now'))` for insertion time
- **Text limits**: message_text ≤ 5000 chars, raw_json ≤ 10000 chars (prevents memory issues)
- Use BOOLEAN type for flags (is_group, is_read, has_attachments)

### 3. Required Indexes (Performance)
Every messaging table needs:
```sql
CREATE INDEX idx_chat_id ON messages(chat_id);
CREATE INDEX idx_timestamp ON messages(timestamp);
CREATE INDEX idx_chat_timestamp ON messages(chat_id, timestamp DESC);
```

For emails, also index: `email_id` (UNIQUE), `thread_id`, `from_email`, `folder`

### 4. Batch Insert Pattern (Python)
Never insert row-by-row. Use transactions:
```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
try:
    # Clear old data if replacing
    cursor.execute('DELETE FROM messages')
    
    # Batch insert
    for msg in all_messages:
        cursor.execute('''
            INSERT INTO messages (chat_id, sender_id, timestamp, message_text, ...)
            VALUES (?, ?, ?, ?, ...)
        ''', (msg['chat_id'], msg['sender_id'], ...))
    
    conn.commit()
    print(f"Inserted {len(all_messages)} messages")
except Exception as e:
    conn.rollback()
    raise
finally:
    conn.close()
```

### 5. Parsing OpenClaw .jsonl Session Files
WhatsApp messages are embedded in `type: "message"` objects with `role: "user"`:
```python
def parse_messages_from_file(filepath):
    messages = []
    with open(filepath, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            if obj.get('type') == 'message' and obj['message'].get('role') == 'user':
                # Extract metadata from text field (contains JSON block)
                text = obj['message']['content'][0]['text']
                # Parse metadata JSON from text
                # Extract chat_id, sender_id, timestamp, etc.
    return messages
```

**Finding session files:**
```bash
ls /root/.openclaw/agents/m1/sessions/ | grep -i whatsapp
```

### 6. Research Methodology (Repo Evaluation)
When adding tools/repos to discussion docs:
1. Check GitHub forks ≥ 500 (via web_extract or gh cli)
2. Verify X/Twitter activity (search: `repo-name site:x.com`)
3. Only add to docs after both checks pass
4. Update existing discussion file (never create new one for same topic)

## Pitfalls (Learned the Hard Way)

1. **Text field size**: Without limits, large raw JSON causes memory errors during insert. Always truncate: `text[:5000]`
2. **M1 (Michael) DB Isolation**: M1's messaging DBs (whatsapp_messages.db, telegram_messages.db, email_messages.db) are correctly stored in `/root/2_clients/2.3_michael/` (isolated workspace per AGENTS.md Section 2: Absolute Client Isolation). These are parsed from M1's .jsonl session files in `/root/.openclaw/agents/m1/sessions/`, not from traditional DBs in other locations.
3. **Data Attribution Rule**: When documenting parsed M1 messaging data (TRACKER.md, docs, reports), always attribute ownership to M1's isolated workspace. Never refer to M1's data as the user (David)'s data. Misattribution violates client isolation rules and causes critical user frustration.
4. **User Correction Protocol**: If the user corrects you about data ownership, isolation, or other critical mistakes: immediately stop all execution, investigate the data location/attribution, confirm findings with the user in plain text before taking any further action. Do not modify files or execute commands until confirmed.
5. **SQLite syntax**: Cannot chain multiple statements with `;` in sqlite3 command line. Use heredoc or separate calls.
6. **Session file format**: WhatsApp metadata is embedded as JSON block inside message text, not as separate fields.
7. **Crash prevention**: Always use WAL mode + transactions. Without these, large inserts can corrupt DB.
8. **CRITICAL (2026-05-04)**: David's DBs DO NOT EXIST YET. M1's existing DBs are NOT David's DBs. When TRACKER says "Create WhatsApp DB", verify WHOSE DB:
   - If David's task: Check `/root/3_core_tools/hermes/data/*.db` — if not found, task is NOT done
   - If M1's task: Check `/root/2_clients/2.3_michael/*.db` — if found, M1's part is done, David's is separate
   - NEVER mark "David's DB task" as [x] just because M1's DB exists
   - **Verification command before TRACKER update**: `ls -la /root/2_clients/2.3_michael/*.db /root/3_core_tools/hermes/data/*.db 2>&1`

## References
- Script template: `scripts/parse_whatsapp.py` (parse .jsonl to SQLite)
- Schema examples: `references/messaging_schemas.md` (WhatsApp, Telegram, Email schemas)
- Research methodology: `references/david_research_methodology.md` (500+ forks, X check)

## Session-Specific Updates (2026-05-04)
- Parsed 368 M1 session messages into M1's isolated WhatsApp DB (`/root/2_clients/2.3_michael/whatsapp_messages.db`), Telegram/Email schemas created only
- Discovered OpenClaw stores messages in .jsonl session files, parsed into isolated client DBs per AGENTS.md Section 2 (Absolute Client Isolation)
- Implemented WAL mode + batch inserts for crash prevention
- User's research methodology: 500+ forks + X activity check before adding repos to docs
- Mandatory user correction protocol: On critical corrections (data isolation/ownership), immediately stop all execution, investigate data location/attribution, confirm findings with user in plain text before taking any further action
