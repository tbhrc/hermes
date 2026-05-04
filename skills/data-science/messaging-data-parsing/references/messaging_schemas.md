# Messaging Database Schemas

## WhatsApp Messages Schema
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chat_id TEXT NOT NULL,
  sender_id TEXT,
  sender_name TEXT,
  timestamp TEXT NOT NULL,
  message_text TEXT,  -- Limit to 5000 chars in Python
  media_path TEXT,
  is_group BOOLEAN DEFAULT 0,
  group_subject TEXT,
  raw_json TEXT,  -- Limit to 10000 chars in Python
  created_at INTEGER DEFAULT (strftime('%s','now'))
);

CREATE INDEX idx_chat_id ON messages(chat_id);
CREATE INDEX idx_sender_id ON messages(sender_id);
CREATE INDEX idx_timestamp ON messages(timestamp);
CREATE INDEX idx_chat_timestamp ON messages(chat_id, timestamp DESC);
```

**DB Location**: `/root/2_clients/2.3_michael/whatsapp_messages.db`
**Status**: Active - 368 messages parsed from M1's .jsonl session files

## Telegram Messages Schema
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id TEXT,
  chat_id TEXT NOT NULL,
  chat_type TEXT,
  sender_id TEXT,
  sender_name TEXT,
  timestamp TEXT NOT NULL,
  message_text TEXT,  -- Limit to 5000 chars
  media_path TEXT,
  edit_date TEXT,
  reply_to_message_id TEXT,
  raw_json TEXT,  -- Limit to 10000 chars
  created_at INTEGER DEFAULT (strftime('%s','now'))
);

CREATE INDEX idx_chat_id ON messages(chat_id);
CREATE INDEX idx_message_id ON messages(message_id);
CREATE INDEX idx_timestamp ON messages(timestamp);
```

**DB Location**: `/root/2_clients/2.3_michael/telegram_messages.db`
**Status**: Schema only (no Telegram sessions found)

## Email (Outlook) Schema
```sql
CREATE TABLE emails (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email_id TEXT UNIQUE,
  thread_id TEXT,
  from_email TEXT,
  from_name TEXT,
  to_emails TEXT,  -- JSON array
  cc_emails TEXT,   -- JSON array
  subject TEXT,
  body_text TEXT,
  body_html TEXT,
  timestamp_sent TEXT,
  timestamp_received TEXT,
  has_attachments BOOLEAN DEFAULT 0,
  attachments TEXT,  -- JSON array of attachment info
  folder TEXT,
  is_read BOOLEAN DEFAULT 0,
  raw_json TEXT,  -- Limit to 10000 chars
  created_at INTEGER DEFAULT (strftime('%s','now'))
);

CREATE INDEX idx_email_id ON emails(email_id);
CREATE INDEX idx_thread_id ON emails(thread_id);
CREATE INDEX idx_from_email ON emails(from_email);
CREATE INDEX idx_timestamp_sent ON emails(timestamp_sent);
CREATE INDEX idx_folder ON emails(folder);
```

**DB Location**: `/root/2_clients/2.3_michael/email_messages.db`
**Status**: Schema only (ready for Microsoft Graph API parsing)

## Crash Prevention Settings
```sql
PRAGMA journal_mode=WAL;  -- Write-Ahead Logging
PRAGMA synchronous=NORMAL;  -- Balance safety vs performance
```

Apply these PRAGMAs immediately after connecting to any messaging DB.
