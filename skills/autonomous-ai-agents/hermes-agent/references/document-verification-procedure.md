# Document Verification Procedure (A1 Mandatory)

**When to use:** Anytime you encounter existing documentation in AOS Hub folders (`9_manuals/`, `3_core_tools/*/docs/`, etc.)

**Mandate from David (2026-05-03):** "Anytime you come across old documentation that is sitting in our folders then you must check online for the latest. You are not allowed to assume."

## Verification Steps

1. **Identify the technology/topic** (e.g., OpenClaw, Hermes, n8n, etc.)
2. **Search for official docs:**
   ```
   web_search(query="<technology> official documentation")
   web_search(query="<specific command/syntax> reference")
   ```
3. **Extract canonical info:**
   ```
   web_extract(urls=["https://docs.<technology>.ai/..."])
   ```
4. **Compare** existing doc with official source:
   - Command syntax changes?
   - Default values different?
   - New features added?
   - Deprecated methods?
5. **Update document** with:
   - Version number + Date
   - "Verified against <official_source> on <date>"
   - Corrected information
6. **Update skill** that references this document (add verification step)

## Example: OpenClaw Docs Update (2026-05-03)

**Found:** `/root/3_core_tools/openclaw/docs/openclaw-multi-agent-guide.md` (existing)

**Verified against:** `https://docs.openclaw.ai/concepts/multi-agent`

**Corrections made:**
- Agent creation: NO `--workspace` flag (was incorrectly documented)
- Default agent ID: `main` (not custom names)
- Telegram DM policy: Default is `pairing` (not `allowlist`)
- Verification command: `openclaw agents list --bindings` (not just `openclaw agents list`)

**Result:** Updated `/root/9_manuals/openclaw-complete-reference.md` (v2.0.0)

## Red Flags (Assume Nothing)

| Situation | Action |
|-----------|--------|
| Old doc says "default is X" | Verify with official docs |
| Doc hasn't been updated in months | Check for newer syntax/commands |
| Command fails unexpectedly | Search online for syntax changes |
| User says "check online" | Drop everything and verify |

**Remember:** David's trust is based on accuracy. Verification is cheaper than correction.
