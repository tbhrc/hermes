---
name: aos-hub-task-protocol
description: "Mandatory AOS Hub task execution workflow: Research → Document → Tracker → Execute with Verification."
version: 1.0.0
author: A1 Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [AOS Hub, Protocol, Task Management, Verification]
---

# AOS Hub Task Execution Protocol

Mandatory workflow for ALL AOS Hub implementation tasks. Enforced by Founder (David) for consistency and quality.

## The Protocol (4 Phases)

### Phase 1: Research
1. Gather information via `web_search`, `web_extract`, `skill_view`.
2. Document findings with sources.
3. Identify dependencies, pitfalls, and prerequisites.
4. **Output**: Research notes ready for documentation.

### Phase 2: Document
1. Write discussion doc to `/root/12_lab/3_discussions/YYYY-MM-DD_<topic>_research_plan.md`.
2. Include: Executive Summary, Technical Details, Dependencies, Risks, Implementation Steps.
3. **Verify**: File exists with `read_file` or `ls`.

### Phase 3: Tracker
1. Read `/root/TRACKER.md`.
2. Add new section with timestamp: `### YYYY-MM-DD (Dubai) — EXECUTE: <Task Name>`.
3. List ALL subtasks as unchecked `- [ ]` items.
4. **Verify**: `grep` TRACKER.md to confirm tasks added.

### Phase 4: Execute with Verification
1. Work through subtasks **sequentially**.
2. After each subtask:
   - **Execute** the work.
   - **Verify** the result (file exists, command succeeds, endpoint responds).
   - **Update TRACKER** immediately: replace `- [ ]` with `- [x]` + verification note.
3. **NEVER** move to next subtask without verifying current one.
4. If verification fails, debug and fix before proceeding.

## Example: Firecrawl Implementation

```
Phase 1: Research → web_search "Firecrawl documentation", web_extract docs.firecrawl.dev
Phase 2: Document → write_file /root/12_lab/3_discussions/2026-05-04_firecrawl_research_plan.md
Phase 3: Tracker → patch TRACKER.md, add "2026-05-04 (Dubai) — EXECUTE: Firecrawl Implementation" with 8 subtasks
Phase 4: Execute →
  Task 1: Clone repo → verify with ls → mark [x]
  Task 2: Check dependencies → verify with which/version → mark [x]
  Task 3: Install missing deps → verify installation → mark [x]
  ... (continue sequentially with verification)
```

## Founder Directive (Mandatory Enforcement)
> **User Voice (2026-05-04)**: "Start with your research and then document it in the lab. Then you add your tasks into the tracker and then you start the work. Do it properly, do it thoroughly, verify it each step. Don't move on to the next step if you did not verify."

This is NOT a suggestion. It is the mandatory AOS Hub workflow. Violations result in:
- Phantom completions (marked [x] without verification)
- Fake checkmarks (claiming success without disk proof)
- Rework when user catches the error

**Enforcement**: Before starting ANY implementation task, recite: "Research → Document → Tracker → Execute with Verification."

## Pitfalls
- **Skipping Documentation**: Never skip Phase 2. Discussion doc is mandatory reference.
- **Phantom Completions**: Never mark `- [x]` without verification. "Task completed" without file/command proof is a violation.
- **Parallel Subtasks**: Avoid parallel execution of subtasks. Sequential with verification ensures quality.
- **TRACKER Stale Read**: Re-read TRACKER.md before patching if last read >5 minutes ago (sibling agents may update).

## Verification Commands by Task Type

| Task Type | Verification Command |
|-----------|---------------------|
| File creation | `ls -la <file>` or `read_file` |
| Git clone | `ls <dir>/README.md` |
| Service install | `command --version` or `which command` |
| Service running | `curl -s http://localhost:port/` or `systemctl status` |
| Config change | `grep "key" config.file` |
| API endpoint | `curl -s -o /dev/null -w "%{http_code}" http://endpoint` |

## Related Skills
- `persistent-task-tracker`: TRACKER.md management
- `writing-plans`: Detailed implementation plans
- `firecrawl`: Example implementation following this protocol
