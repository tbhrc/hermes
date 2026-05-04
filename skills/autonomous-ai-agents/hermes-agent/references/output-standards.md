# Output Standards v1.0.0 (2026-05-04)

*Operational Rules for A1 Global Orchestrator (Hermes Agent) Messaging Platform Outputs*
*Location: /root/9_manuals/ (Pillar 9 — Canonical Storage for Operational SOPs)*

## Mandatory WhatsApp/Telegram Formatting
1. **No Markdown**: Platforms do not render markdown — use plain text only
2. **Bold Subjects**: Use *single asterisk* Unicode bold (max 3 words before colon), e.g., *Task Update*:
3. **File Paths**: Plain absolute paths only (e.g., /root/file.txt), no formatting
4. **Emojis**: Strategic use only: ✅ Completed/Success, 🟠 In Progress/Pending, ❌ Error/Blocked
5. **Numbered Lists**: For user selectable options, allow single-number replies
6. **Bottom Line First**: Concise, assertive tone — no fluff, no repetitive content
7. **Model Footer**: Dynamic current model name only (pull from `config.yaml` `model.default`) at bottom of every output, no provider/API details
8. **No MEDIA:/path Tags**: Native attachments use MEDIA:/absolute/path only on messaging platforms, never include tags in text
9. **No Repetition**: Never repeat confirmed information or restate points in the same session

## Platform-Specific Rules
- **WhatsApp/Telegram**: Unicode *bold* for subjects, no markdown, plain paths, emojis as above
- **CLI**: Plain text only, no markdown, no MEDIA:/path tags, absolute file paths

## Verification & Storage
- This document is the canonical source of truth for output standards, not volatile memory or skill files
- Always check this doc first before formatting outputs
- Update version + date on every change (e.g., v1.0.1, 2026-05-04)

## Related Docs
- /root/3_core_tools/hermes/data/START_HERE.md (A1 onboarding)
- /root/RULES.md (AOS Hub operating policy)
- /root/12_lab/3_discussions/ (unfinalized discussion docs)

---
*Version: v1.0.0 | Date: 2026-05-04 | Owner: David Potgieter | Location: /root/9_manuals/*
