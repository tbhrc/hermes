# Upstream agent-browser DNS/CDP Issues Summary
*Last updated: 2026-05-04*

## Confirmed Bugs (Matched Our Environment)
1. **Issue #69**: CDP mode undocumented, connection fails. Fixed in PR #445 (CDP improvements), #459 (custom headers).
2. **Issue #941**: Bundled Chrome 146 DNS timeouts, system Chrome works. `CHROME_PATH` override suggested, but tested and failed in our environment (2026-05-04).
3. **Issue #1272**: CDP connection fails on Chrome restart due to stale `webSocketDebuggerUrl` caching. Fixed in PR #1274.

## Test Results (2026-05-04)
- `CHROME_PATH=/usr/local/bin/google-chrome agent-browser open https://example.com`: FAILED (command killed, exit -9, DNS error persists)
- Direct Chrome headless `/opt/google-chrome/chrome --headless=new --dump-dom <URL>`: WORKS perfectly for all URL rendering

## Upstream PRs to Monitor
| PR # | Description | Status |
|------|-------------|--------|
| #445 | CDP connection improvements | Open/In Progress |
| #459 | Custom headers for CDP | Open/In Progress |
| #1274 | Fix CDP reconnection when Chrome restarts | Open/In Progress |

## Key Takeaway
agent-browser CLI DNS/CDP implementation is fundamentally broken for our use case. Wait for upstream PR merges before re-testing CLI functionality. Use direct Chrome headless as stable workaround.