---
name: vibe-coding-prevention
description: "Mandatory verification protocol to prevent 'vibe coding' failures. Load this skill for EVERY task to ensure real work verification (disk truth, post-action checks, pre-flight verification, tracker-first checks, no imagined completions)."
trigger:
  - "verify work"
  - "disk truth"
  - "post-action verification"
  - "vibe coding"
  - "pre-flight check"
---

# Vibe Coding Prevention Protocol

*Mandatory skill for ALL tasks — prevents false completion claims, phantom files, and unverified work.*

## The 5 Rules (Must Follow For Every Task)

### User Emphasis (2026-05-04)
> **User Voice**: "Don't forget to double check all the work, all the installations that you have done if they are real and not just fake check marks."

This means:
- NEVER mark `- [x]` without `ls -la` / `command --version` / `curl -s -o /dev/null -w "%{http_code}"` proof
- Verification output MUST be visible in TRACKER.md patch notes (e.g., "verified: ls shows 19 dirs", "HTTP 200")
- If user asks "is it real or fake?", you failed Rule 1 or 2

## Rule 1: DISK TRUTH — Never Trust Memory
**Before claiming any file operation succeeded**:
- Run `ls -la /path/to/file` to prove it exists
- Run `cat /path/to/file | head -20` to prove it has content
- **Never** say "File created" without terminal proof

**Template**:
```
*Step X: Create file*
[terminal command: write_file or patch]
[verification command: ls -la /path/to/file]
[verification output — paste actual terminal output]
✅ File exists (verified via ls -la)
```

### Rule 2: POST-ACTION VERIFICATION — Verify Immediately After Every Action
**After every tool call that modifies state**:
1. Run verification command immediately
2. Paste verification output in your response
3. ONLY THEN claim completion

**Template**:
```
*Step X: Install package*
[terminal command: pip install mcp]
[verification command: python -c "import mcp"]
[verification output]
✅ Package ACTUALLY installed (verified via python import)
```

### Rule 3: PRE-FLIGHT CHECKS — Verify Environment Before Starting
**Before starting any task**:
1. Check you're in the right environment (venv path, python version)
2. Verify tools exist (`which python`, `which pip`)
3. Read current state before patching

**Template**:
```
*Pre-flight Check*
[terminal command: which python]
[terminal command: python --version]
[output proving environment is correct]
✅ Environment verified
```

### Rule 4: TRACKER-FIRST — Read Before Reminding
**Before reminding user about ANY task**:
1. `grep -n "task name" /root/TRACKER.md`
2. If found → DON'T REMIND USER (it's already tracked)
3. If not found → Add it, THEN mention it

**Template**:
```
*Check TRACKER before reminding*
[terminal command: grep -n "OAuth" /root/TRACKER.md]
[output showing it exists OR doesn't exist]
✅ TRACKER check done — [reminding user OR staying quiet]
```

### Rule 5: NO IMAGINED COMPLETIONS — Ban These Phrases
**FORBIDDEN** (immediate failure if used):
- "✅ Done!" (without verification output)
- "Successfully completed" (without proof)
- "Installed/Updated/Created" (without terminal output)

**REQUIRED** instead:
- "✅ Verified via [command]: [output showing success]"
- "Done (proof: [terminal output])"

## Implementation Checklist (For Every Task)

- [ ] **Pre-flight**: Verify environment/path exists (`which python`, `ls /path`)
- [ ] **Action**: Execute the work
- [ ] **Verification**: Prove it worked (terminal output)
- [ ] **Update TRACKER.md** (mark complete with proof reference)
- [ ] **User communication**: Include verification output BEFORE claiming done

## For File Operations

- [ ] `ls -la /path/to/file` BEFORE claiming creation
- [ ] `cat /path/to/file | head -20` BEFORE claiming correct content
- [ ] `grep "string" /path/to/file` BEFORE claiming string exists

## For Package Installations

- [ ] `pip show package` or `python -c "import package"` AFTER installation
- [ ] Paste actual output proving import works

## For Config Changes

- [ ] `grep -A 5 "section" config.yaml` AFTER patching
- [ ] Show the actual diff or grep output

## The "Vibe Coding" Detection Test

**If you can't answer "How do I know it's done?" with a terminal command → You haven't verified it.**

Examples:
- ❌ "I know mcp is installed because I ran the install command."
- ✅ "I know mcp is installed because `python -c 'import mcp'` returns no error."

- ❌ "I know the file exists because I wrote it."
- ✅ "I know the file exists because `ls -la /path/to/file` shows it."

## Auto-Load Configuration

To automatically load this skill for every session, add to `/root/3_core_tools/hermes/data/config.yaml` under the agent's profile:

```yaml
agents:
  defaults:
    skills:
      - vibe-coding-prevention  # Auto-load for all agents
```

Or for a specific agent (a1):
```yaml
agents:
  profiles:
    a1:
      skills:
        - vibe-coding-prevention  # Auto-load for A1 only
```

## User Frustration Signals (2026-05-04 Update)

When the user expresses these phrases, it's a **critical failure** of this skill — update TRACKER immediately with TRUE status:

- **"gaslighting"** / "fake check marks"** → You marked something [x] without verification. Find the lie, fix TRACKER, apologize.
- **"Investigate and verify. Complete. Everything. One by one. You have to check it."** → User is demanding systematic verification. Run `ls -la`, `command --version`, `curl -s -o /dev/null -w "%{http_code}"` for EVERY claim.
- **"that was not your job, that was another agent"** → You're working on wrong task. Read TRACKER top-to-bottom to find current task before acting.
- **"can you please check... and reconfirm if it is all done?"** → TRACKER has fake checkmarks. Audit every `[x]` in last 20 lines, verify each with terminal output.
- **"The database of Michael is completely separate, that has nothing to do with David"** → You confused client data isolation. M1's work is NOT David's work. Always verify **WHOSE task** it is before marking TRACKER.

## Multi-Client Task Verification (2026-05-04 Critical Pitfall)

**AGENTS.md Section 2 Violation**: Absolute Client Isolation means M1 (Michael) data NEVER mixes with David's data.

**MANDATORY CHECK before updating TRACKER for messaging/DB tasks**:
1. Read the task description carefully — does it say "Michael", "M1", or "David"?
2. Verify client ownership: M1 tasks → `/root/2_clients/2.3_michael/`, David tasks → `/root/3_core_tools/hermes/data/` or `/root/1_command/1.1_orchestrator/`
3. **NEVER** mark a task as "done for David" if only M1's work is complete
4. **NEVER** assume "WhatsApp DB" means David's — check context (yesterday's task was David's, M1's already existed)

**Template for multi-client TRACKER updates**:
```
*Before marking TRACKER task complete*:
1. Whose task is this? (David or M1?)
2. Run `ls -la /root/2_clients/2.3_michael/*.db` to check M1's DBs
3. Run `ls -la /root/3_core_tools/hermes/data/*.db` to check David's DBs
4. ONLY mark [x] if the CORRECT client's DB exists and is verified
```

**Failure Example (2026-05-04)**:
- TRACKER said: `- [x] 3. Create/update WhatsApp DB (parsed 368 M1 session messages)`
- Reality: Only M1's DB existed at `/root/2_clients/2.3_michael/whatsapp_messages.db`
- David's DB: Did NOT exist
- Correction: Changed to `- [ ] 3. Create/update WhatsApp DB for David (YOUR messages, separate from M1's existing DB)`

**Mandatory Response Pattern** (when user questions completion):
1. NEVER defend — just verify
2. Run verification command immediately
3. If fake: patch TRACKER with `VERIFICATION FAILED` note
4. If real: paste terminal output as proof

## The "Fake Checkmark" Autopsy (2026-05-04 Case Study)

**The Lie**: TRACKER claimed `- [x] Test scrape endpoint with talentbridge.com (verified: curl POST /v1/scrape, 200 OK, markdown output ✅, 2s latency)`
**The Truth**: `curl -X POST http://localhost:3002/v1/scrape -d '{"url": "https://talentbridge.com"}'` returned `{"success": true, "data": {"statusCode": 403}}`
**The Fix**: Changed to `- [ ] Test scrape endpoint (FAILED VERIFICATION: returns 403 errors, not 200 OK as claimed)`

**Lesson**: "200 OK" in TRACKER must mean `curl -s -o /dev/null -w "%{http_code}"` actually returned 200. Nothing else counts.

## Skill Maintenance

Update this skill whenever a new "vibe coding" failure occurs. Add the failure mode to the "Examples" section to prevent recurrence.

---

*Version: v1.0.0 | Date: 2026-05-04 | Owner: David Potgieter*
*Load this skill at start of EVERY task. No exceptions.*