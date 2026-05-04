#!/usr/bin/env python3
"""Template: Parse WhatsApp messages from OpenClaw .jsonl session files into SQLite DB.
Usage: python3 parse_whatsapp.py
"""
import json
import os
import sqlite3
from datetime import datetime

DB_PATH = '/root/2_clients/2.3_michael/whatsapp_messages.db'
SESSIONS_DIR = '/root/.openclaw/agents/m1/sessions'
MAX_MESSAGES = 1000  # Adjust as needed

def get_whatsapp_sessions():
    """Find .jsonl files that contain WhatsApp sessions."""
    sessions = []
    for f in os.listdir(SESSIONS_DIR):
        if f.endswith('.jsonl') and 'whatsapp' in f.lower():
            sessions.append(os.path.join(SESSIONS_DIR, f))
    return sessions

def parse_messages_from_file(filepath):
    """Extract messages from a .jsonl file."""
    messages = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
                if obj.get('type') == 'message' and 'message' in obj:
                    msg = obj['message']
                    if msg.get('role') == 'user':
                        content = msg.get('content', [])
                        text = ''
                        media_path = ''
                        for item in content:
                            if item.get('type') == 'text':
                                text = item.get('text', '')
                            elif item.get('type') == 'image':
                                media_path = item.get('data', '')
                        # Extract metadata from text (JSON block)
                        meta = {}
                        if text:
                            try:
                                start = text.find('```json')
                                if start != -1:
                                    end = text.find('```', start + 7)
                                    if end != -1:
                                        json_str = text[start+7:end].strip()
                                        meta = json.loads(json_str)
                            except:
                                pass
                        messages.append({
                            'chat_id': meta.get('chat_id', ''),
                            'sender_id': meta.get('sender_id', ''),
                            'sender_name': meta.get('sender', ''),
                            'timestamp': obj.get('timestamp', ''),
                            'message_text': text[:5000],  # LIMIT: prevent memory issues
                            'media_path': media_path,
                            'is_group': meta.get('is_group_chat', False),
                            'group_subject': meta.get('group_subject', ''),
                            'raw_json': json.dumps(obj)[:10000]  # LIMIT: prevent memory issues
                        })
            except json.JSONDecodeError:
                continue
    return messages

def main():
    session_files = get_whatsapp_sessions()
    print(f"Found {len(session_files)} WhatsApp session files")
    
    all_messages = []
    for sf in session_files:
        msgs = parse_messages_from_file(sf)
        all_messages.extend(msgs)
        print(f"  {sf}: {len(msgs)} messages")
    
    # Sort by timestamp (newest first) and limit
    all_messages.sort(key=lambda x: x['timestamp'], reverse=True)
    all_messages = all_messages[:MAX_MESSAGES]
    
    print(f"Total messages to insert: {len(all_messages)}")
    
    # Insert into DB using transaction (CRASH PREVENTION)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM messages')  # Clear for fresh parse
        
        for msg in all_messages:
            cursor.execute('''
                INSERT INTO messages (chat_id, sender_id, sender_name, timestamp, message_text, media_path, is_group, group_subject, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                msg['chat_id'],
                msg['sender_id'],
                msg['sender_name'],
                msg['timestamp'],
                msg['message_text'],
                msg['media_path'],
                msg['is_group'],
                msg['group_subject'],
                msg['raw_json']
            ))
        
        conn.commit()
        print(f"Successfully inserted {len(all_messages)} messages")
        
        cursor.execute('SELECT COUNT(*) FROM messages')
        count = cursor.fetchone()[0]
        print(f"Total messages in DB: {count}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
