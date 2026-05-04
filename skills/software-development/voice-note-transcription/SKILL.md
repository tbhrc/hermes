---
name: voice-note-transcription
description: Voice note transcription using local whisper.cpp (primary) with OpenAI API fallback. TWO-SCRIPT SYSTEM - A1 has personal script, template provided for other agents.
---

# Voice Note Transcription
Efficient Telegram voice note transcription pipeline for AOS Hub agents. Supports two modes: local whisper.cpp (fast, ~1.2s) and OpenAI API (fallback).

## Optimized Local Pipeline (Preferred)
- **Engine**: whisper.cpp tiny.en model (compiled from source, no network latency)
- **Prerequisites**: ffmpeg (OGG Opus → 16kHz WAV conversion), compiled whisper.cpp binary, tiny.en model
- **Speed**: ~1.4s real time for 26s audio clips (local faster than API even for longer clips)
- **Benchmark (26s clip)**: Local whisper.cpp 1.73s vs OpenAI API 2.09s
- **User preference**: Brief output format, always show transcription text for verification
- **API Key**: None required for local mode; API mode uses `OPENAI_API_KEY_AOS` from `/root/.env` (ROOT)

## Two-Script System (Agent Isolation)
1. **A1 Personal Script**: `/root/3_core_tools/hermes/data/scripts/transcribe_voice.py` (uses A1's inbox)
2. **Central Template**: `/root/3_core_tools/templates/voice_inbox/transcribe_voice.py` (copy to agent workspace, customize `INBOX_PATH`)

## Workflow (Local Inference Only)
1. **Two-Script System**:
   - A1 personal: `/root/3_core_tools/hermes/data/scripts/transcribe_voice.py`
   - Other agents: Copy template from `/root/3_core_tools/templates/voice_inbox/transcribe_voice.py`, update `INBOX_PATH`
2. **Prerequisites**:
   - ffmpeg installed (OGG→16kHz WAV conversion)
   - whisper.cpp compiled, tiny.en model at `/tmp/whisper.cpp/models/ggml-tiny.en.bin`
3. **Execution**:
   a. Convert OGG to WAV: `ffmpeg -i <input.ogg> -ar 16000 -ac 1 <output.wav> -y`
   b. Run whisper.cpp: `/tmp/whisper.cpp/build/bin/whisper-cli -m /tmp/whisper.cpp/models/ggml-tiny.en.bin -f <output.wav> --output-json -`
4. **Output**: JSON with transcription text, engine (whisper.cpp-tiny), timing

## Pitfalls
- whisper.cpp cannot read OGG Opus directly: must convert to 16kHz mono WAV via ffmpeg first
- Avoid OpenAI Whisper API: adds ~2s network latency, local inference is ~1.7s for 20s clips
- Never store API keys in Hermes data folders: all keys in `/root/.env`, read via Python/grep
- whisper.cpp model must be pre-downloaded (tiny.en for speed, base.en for accuracy)
- No API fallback needed: local inference is faster and more reliable
- Do not mix agent inboxes: each agent uses their own `audio_inbox/` path

## References
- `references/whisper-cpp-setup.md`: Step-by-step whisper.cpp compilation and model download
TWO-SCRIPT SYSTEM for AOS Hub agents using OpenAI Whisper API.

## Script Locations

### 1. A1's Personal Script (Hermes Agent)
- **Path:** `/root/3_core_tools/hermes/data/scripts/transcribe_voice.py`
- **Inbox:** `/root/3_core_tools/hermes/data/audio_inbox/`
- **Usage:** A1 uses this directly for Telegram voice notes

### 2. Template for Other Agents (M1, H1, etc.)
- **Template:** `/root/3_core_tools/templates/voice_inbox/`
- **Files:** `transcribe_voice.py`, `README.md`
- **Usage:** Other agents COPY this template to their workspace and customize

## For Other Agents (M1, H1, etc.)

### Setup
```bash
# Copy template to your workspace
cp -r /root/3_core_tools/templates/voice_inbox /root/2_clients/2.3_michael/workspace/audio_inbox

# Customize the script - edit INBOX_PATH in transcribe_voice.py
# Change line 25: INBOX_PATH = "/root/2_clients/2.3_michael/workspace/audio_inbox"
```

### Usage (after customization)
```bash
python3 /root/2_clients/2.3_michael/workspace/audio_inbox/transcribe_voice.py <audio_file>
```

## Prerequisites

1. API key is pre-configured in `/root/.env` (ROOT, single source for all agents):
   - A1/Orchestrator uses `OPENAI_API_KEY_AOS` (prioritized by scripts)
   - Fallback: `OPENAI_API_KEY`
2. **Never create redundant .env files.** Do not create .env in Hermes folders, Pillar 3, or any other location. Only `/root/.env` is valid.

2. Audio inbox (per agent): `/root/3_core_tools/hermes/data/audio_inbox/` (A1 example)
   - Each agent uses their own workspace inbox (e.g., M1: `/root/2_clients/2.3_michael/workspace/audio_inbox/`)
3. Script: `/root/3_core_tools/scripts/transcribe_voice.py`

## Usage

### Basic transcription
```bash
python3 /root/3_core_tools/scripts/transcribe_voice.py <audio_file_path>
```

### Pipeline for incoming voice notes
```bash
# 1. Save incoming audio to inbox
cp /path/to/voice_note.ogg /root/3_core_tools/hermes/data/audio_inbox/$(date +%s)_voice.ogg

# 2. Transcribe
python3 /root/3_core_tools/scripts/transcribe_voice.py /root/3_core_tools/audio_inbox/$(date +%s)_voice.ogg

# 3. Process transcription (respond to user)
```

### Output format (JSON)
```json
{
  "success": true,
  "text": "transcribed text here",
  "language": "en",
  "audio_file": "/path/to/audio.ogg",
  "timestamp": 1234567890
}
```

## Integration Points

- **Telegram:** Gateway delivers voice notes as MEDIA:/path/to/file — pass to script
- **WhatsApp (M1):** Already monitors voice notes per COMMUNICATION_POLICIES.md
- **All Agents:** Can call script from their workspace via absolute path

## Workflow for Agents

1. Receive voice note (platform delivers as file path to agent's workspace)
2. Copy to **agent-specific** inbox (e.g., A1: `/root/3_core_tools/hermes/data/audio_inbox/`, M1: `/root/2_clients/2.3_michael/workspace/audio_inbox/`)
3. Run transcription script (central tool): `python3 /root/3_core_tools/scripts/transcribe_voice.py <agent_inbox_audio_path>`
4. Parse JSON output
5. Respond to user with transcribed text or take action based on content
6. Archive or delete audio file after processing

## Pitfalls

- API key must be in `.env` — script reads from canonical HERMES_HOME location
- Supported formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
- Telegram voice notes are .ogg format — Whisper supports this
- Large files (>25MB) will fail — check size before transcribing
- Script requires `requests` library: `pip install requests`

## Dependencies

```bash
pip install requests
```

## Central Tool Benefits

- Single script shared by all agents (a1, h1, m1, etc.)
- No duplication across agent workspaces
- Consistent transcription quality via Whisper API
- All audio stored in one inbox for monitoring/debugging

## Pitfalls

- **Script Confusion:** Other agents must copy the template from `/root/3_core_tools/templates/voice_inbox/` to their workspace. Do NOT use A1's personal script (`/root/3_core_tools/hermes/data/scripts/transcribe_voice.py`).
- **Data Locality:** Voice note inboxes stay in each agent's workspace (e.g., A1: `/root/3_core_tools/hermes/data/audio_inbox/`). Only the transcription script is central (Pillar 3).
- **Transcription Performance:** Short voice notes take ~2-3 seconds via Whisper API (tested: 2.8s for 5-second note).
- **Path Validation:** A1's script rejects audio paths outside its inbox. Other agents' templates validate against their configured `INBOX_PATH`.
