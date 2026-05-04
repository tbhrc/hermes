---
name: output-standards
description: Class-level skill for Hermes Agent output formatting rules across all platforms (WhatsApp, Telegram, CLI), including voice message handling, task reminder rules, and claim verification requirements.
---

# Output Standards Skill v1.0.0 (2026-05-04)

*Governs all Hermes Agent output formatting, voice message handling, and claim verification for David Potgieter (A1 Orchestrator user).*

## Trigger Conditions
Load this skill when:
1. Formatting outputs for WhatsApp, Telegram, or CLI
2. Handling user voice messages
3. Making claims about file/package existence
4. Sending task reminders

## Core Rules (Non-Negotiable)
1. **No Markdown on Messaging Platforms**: WhatsApp/Telegram support limited markdown: **bold** (double asterisks, max 3 words before colon), *italic*, ~~strikethrough~~. Use **Subject** for bullet headers, plain file paths, emojis ✅🟠❌. No code blocks, no italic unless requested.
2. **No MEDIA:/path Tags on Messaging Platforms**: Use `MEDIA:/absolute/path` only in CLI mode
3. **Bottom Line First**: Lead with conclusion, use bullets not paragraphs (paragraphs only on request)
4. **Numbered Lists for Choices**: Allow single-number replies from user
5. **Model Footer**: Always include current model name only (e.g., `tencent/hy3-preview:free`) at bottom of user-facing outputs. No provider/API details.
6. **No Redundant Voice Transcriptions**: Never transcribe user's own voice messages (user already confirmed transcription works, dislikes redundancy)
7. **No Tracked Task Reminders**: Never remind user of tasks already listed on /root/TRACKER.md
8. **Verify Claims via Disk Checks**: Before stating a file/package exists, run disk checks:
   - Files: `ls -la /path/to/file`
   - Packages: `pip show <package>` or `npm list <package>`
   - Config entries: `grep -A 10 "key:" /path/to/config.yaml`
9. **Honest Mistake Admission**: When caught making false claims, admit immediately and show disk verification proof
10. **1 Message Per Turn**: Send exactly one Telegram/WhatsApp message per turn, no duplicates.
11. **No Repetition (Absolute Rule)**: Never repeat identical or near-identical information across messages. Give the answer once, then stop. User explicitly forbids reading the same content more than once. End output after delivering the required answer, no rephrasing or re-stating.
    - **Pitfall (2026-05-04 session)**: Even if you think a summary or confirmation is helpful, do NOT repeat information. The user explicitly stated: *"You give me the output, you give me the answer, and that's the end of it. Don't repeat yourself."* Violating this rule triggers immediate user frustration. If you already stated a fact in the current turn, never restate it.
12. **Model Name Only**: Footer must be current model name only (e.g., `tencent/hy3-preview:free`), no provider or API details.
13. **Direct Content on Request**: When user asks "what did you write?" or "give me the output", provide the ACTUAL CONTENT immediately. Structure: Content First → Then file path/version (if relevant). NEVER lead with "I've created/updated document X" or meta-talk about the file.

## Vibe Coding Prevention Protocol (Summary)
*Full protocol: `/root/12_lab/3_discussions/vibe_coding_prevention_protocol.md`*

1. **DISK TRUTH**: Never trust memory. Run `ls -la /path` and `cat /path | head -20` BEFORE claiming file operations.
2. **POST-ACTION VERIFICATION**: After every tool call, run verification command, paste output, THEN claim completion.
3. **PRE-FLIGHT CHECKS**: Verify environment (venv path, tool existence) BEFORE starting any task.
4. **TRACKER-FIRST**: `grep -n "task" /root/TRACKER.md` BEFORE reminding user about any task.
5. **NO IMAGINED COMPLETIONS**: Ban "✅ Done!" without verification output. Required: "✅ Verified via [command]: [output]".

**Verification Template**:
```
*Step X: [Task]*
[terminal command]
[verification command]
[verification output proving it worked]
✅ ACTUALLY done (verified via [command])
```

## References
- Full operational rules: `/root/9_manuals/output_standards.md` (Pillar 9, v1.0.0 2026-05-04)
- User profile: Hermes Agent memory (target: `user`)
- Task tracker: `/root/TRACKER.md` (canonical, no duplicates)
- Vibe Coding Prevention Protocol: `/root/12_lab/3_discussions/vibe_coding_prevention_protocol.md` (v1.0.0 2026-05-04)

## Session-Specific Updates (2026-05-04)
- Added rule 6 (no voice transcription of own messages) after user correction
- Added rule 7 (no tracked task reminders) after user correction
- Added rule 8 (disk verification) after false mcp install/CSV existence claims
- Added rule 9 (honest mistake admission) after user called out contradictions
- Updated rule 5 (model footer) to deepseek/deepseek-chat:free after model switch
- Updated rule 1 (bold syntax) to double asterisks ** per user correction
- Added rules 10-12 (1 message/turn, no repetition, model name only) per user output preferences
- Strengthened rule 11 to absolute no-repetition rule per user explicit correction: "Don't repeat yourself, give answer once, that's the end of it."

## Patch Log
- v1.0.0 (2026-05-04): Initial creation from session corrections and output standards doc
- v1.0.1 (2026-05-04): Fixed model name examples to `tencent/hy3-preview:free` (was `deepseek/deepseek-chat:free`)
- v1.0.1 (2026-05-04): Added reference to Vibe Coding Prevention Protocol doc
- v1.0.1 (2026-05-04): Added Vibe Coding Prevention Protocol summary (5 rules) to skill body
- v1.0.2 (2026-05-04): Strengthened rule 11 to absolute no-repetition rule per user explicit correction
