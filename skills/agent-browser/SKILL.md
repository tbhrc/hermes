---
name: agent-browser
category: software-development
description: Browser automation using Chrome headless fallback (agent-browser CLI broken via DNS/CDP bug, verified 2026-05-04).
---

# agent-browser Skill (Fixed)

## Trigger Conditions
Use this skill when you need to:
- Open a URL and extract page content.
- Take screenshots of web pages.
- Automate browser interactions (click, type, navigate).

## Working Method: Chrome Headless Direct (Only Functional Option)

agent-browser CLI is **BROKEN** for all DNS/CDP operations (`net::ERR_NAME_NOT_RESOLVED` for all URLs, verified 2026-05-04). Use direct Chrome headless for all browser automation:
```bash
/opt/google-chrome/chrome --headless=new --no-sandbox --dump-dom <URL>
```
- Screenshot: Add `--screenshot=/path/to/file.png` flag
- Scroll techniques: See `references/scroll_techniques.md`
- No AI features: Loses agent-browser's accessibility snapshots, semantic locators, batch execution (similar to Playwright basic usage)

### Non-Functional: agent-browser CLI
- All CLI commands fail with DNS errors, even with `CHROME_PATH=/usr/local/bin/google-chrome` override (tested 2026-05-04)
- Upstream fixes pending: PR #445 (CDP improvements), #459 (custom CDP headers), #1274 (reconnection fix)
If agent-browser CLI fails (rare), use Chrome headless directly:

### Steps
1. **Dump DOM**: Use Chrome headless to dump page HTML:
   ```bash
   /opt/google-chrome/chrome --headless=new --no-sandbox --user-agent="Mozilla/5.0 (compatible; Googlebot/2.1)" --dump-dom <URL> > /tmp/page.html 2>&1
   ```

2. **Extract Content**: Parse the dumped HTML with terminal tools (grep, sed, awk).

3. **Screenshot**: Use Chrome headless to take screenshot:
   ```bash
   /opt/google-chrome/chrome --headless=new --no-sandbox --screenshot=/tmp/screenshot.png --window-size=1920,1080 <URL>
   ```

4. **Click/Navigate**: For multi-step navigation, dump DOM of each page sequentially.

### Example: Get Jobs from talentbridgedubai.com
```bash
# Step 1: Dump homepage
/opt/google-chrome/chrome --headless=new --no-sandbox --dump-dom https://talentbridgedubai.com > /tmp/home.html 2>&1

# Step 2: Find jobs link and navigate
grep -o 'href="[^"]*jobs[^"]*"' /tmp/home.html | head -1

# Step 3: Dump jobs page
/opt/google-chrome/chrome --headless=new --no-sandbox --dump-dom https://talent-bridge-dubai.careers-page.com/ > /tmp/jobs.html 2>&1

# Step 4: Extract job titles
grep -o '<h6 class="text-brand-blue job-title[^>]*>[^<]*</h6>' /tmp/jobs.html | sed 's/<[^>]*>//g' | head -3
```

## Pitfalls

### 1. agent-browser CLI DNS Bug (ROOT CAUSE IDENTIFIED 2026-05-04)
The `agent-browser` CLI has a persistent, unfixable DNS resolution error via CDP (`net::ERR_NAME_NOT_RESOLVED` for ALL URLs).

**Root Cause**: Rust reqwest DNS resolver can't use systemd-resolved stub (127.0.0.53). Even with:
- systemd-resolved configured (DNS=1.1.1.1, resolv.conf mode stub)
- /etc/hosts entries (8.8.8.8 example.com)
- CHROME_PATH=/usr/local/bin/google-chrome override
- CDP endpoints tested manually (curl http://localhost:9222/json works)
- All Chrome binaries tested (bundled 146, system 145, our 148)
- Daemon restarted, processes killed, temp files cleaned

The agent-browser CLI still fails. Chrome directly works perfectly.

**Confirmed via GitHub Issues**:
- Issue #941: Bundled Chrome 146 DNS timeout, system Chrome works
- Issue #69: CDP mode undocumented/broken
- Issue #1272: Daemon caches stale webSocketDebuggerUrl UUIDs

**Workaround**: Use Chrome headless directly (see Working Method above).

**Upstream Fixes Pending**:
- PR #445: CDP connection improvements
- PR #459: Custom headers for CDP
- PR #1274: Fix CDP reconnection when Chrome restarts

### 2. No AI Features
Direct Chrome headless loses all agent-browser AI-specific features (accessibility snapshots, semantic locators, batch execution, React inspection, Web Vitals).

### 3. Playwright Parity
Workaround reduces agent-browser to basic Playwright-like functionality (navigate + dump DOM).

### 4. No web_extract for Browser Automation
The `web_extract` premium tool is forbidden for browser automation tasks (user restriction, limited to 497 remaining uses). Parse dumped HTML with `grep`/`sed` or terminal tools instead.

### 5. JS Rendering Delay
Chrome headless may need `--virtual-time-budget=15000` for JS-heavy pages like talentbridge.com careers page.

## References
- Full DNS bug debug log and workaround details: `references/agent-browser-cli-dns-bug.md`
- DNS debug session (2026-05-04): `references/dns-debug-2026-05-04.md` (systemd-resolved, resolv.conf stub, /etc/hosts, Chrome works but agent-browser doesn't)
- Scroll techniques (scroll to bottom, JS eval methods): `references/scroll_techniques.md`
- JS-rendered page examples: `references/js-rendered-page-example.md`
- Upstream issue research summary: `references/upstream-dns-cdp-issues.md`
- Full lab discussion doc: `/root/12_lab/3_discussions/2026-05-04_agent-browser-dns-cdp-issue-research.md`
