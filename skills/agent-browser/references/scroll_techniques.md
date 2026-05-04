# Agent-Browser Scroll Techniques (Session-Tested 2026-05-04)
## Scroll to Page Bottom (Verified Method)
### Workflow
1. **Open target page** (browser session persists via daemon for chained commands):
   ```bash
   agent-browser open talentbridgedubai.com
   ```
   Verification output:
   ```
   ✓ Best Recruitment Agency Company in Dubai
     https://talentbridgedubai.com/
   ```

2. **Execute JavaScript scroll to bottom**:
   ```bash
   agent-browser eval "window.scrollTo(0, document.body.scrollHeight)"
   ```
   Verification output: `null` (exit 0 ✅)

3. **Take screenshot of bottom**:
   ```bash
   agent-browser screenshot /tmp/talentbridge_bottom.png
   ```
   Verification output:
   ```
   ✓ Screenshot saved to /tmp/talentbridge_bottom.png
   ```

4. **Disk truth check (Rule1)**:
   ```bash
   ls -la /tmp/talentbridge_bottom.png
   ```
   Example output:
   ```
   -rw-r--r-- 1 root root 130806 May  4 00:19 /tmp/talentbridge_bottom.png
   ```

## Chained Command Shortcut
Combine all steps in one line (maintains browser session):
```bash
agent-browser open talentbridgedubai.com && agent-browser eval "window.scrollTo(0, document.body.scrollHeight)" && agent-browser screenshot /tmp/talentbridge_bottom.png
```

## Pitfalls
- ❌ Do NOT use `agent-browser scroll down` for full bottom scroll: only scrolls by fixed pixels (default ~100px)
- ❌ Do NOT run scroll command before opening page: browser session must have active page
- ✅ Always chain commands with `&&` to maintain session state
- ✅ Verify screenshot existence via `ls -la` before claiming completion (follow vibe-coding-prevention Rule1)

## Other Scroll Methods
- `agent-browser scroll down 500` → Scroll down 500px
- `agent-browser scrollintoview <selector>` → Scroll element into view
- `agent-browser eval "window.scrollTo(0, 0)"` → Scroll to top
