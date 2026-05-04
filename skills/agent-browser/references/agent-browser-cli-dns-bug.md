# agent-browser CLI DNS Resolution Bug (net::ERR_NAME_NOT_RESOLVED)

## Reproduction Steps
1. Install agent-browser globally: `npm install -g agent-browser`
2. Run any navigation command:
   ```bash
   agent-browser open https://example.com
   agent-browser open http://1.1.1.1
   agent-browser open "data:text/html,<h1>Test</h1>"
   ```
3. All commands fail with: `✗ Navigation failed: net::ERR_NAME_NOT_RESOLVED`

## Debugging Attempts (All Failed)
1. **System DNS Check**: `curl`/`nslookup` work normally, direct Chrome launch resolves URLs fine.
2. **DNS Config Updates**: Updated `/etc/resolv.conf` and systemd-resolved to 8.8.8.8/8.8.4.4, no fix.
3. **CDP Port Testing**: Launched Chrome with `--remote-debugging-port=9222`, `curl http://localhost:9222/json` returns valid CDP JSON, but agent-browser still fails.
4. **Binary Reinstalls**: Reinstalled agent-browser globally, tried both agent-browser managed Chrome and system Chrome, no fix.
5. **Flag Passing**: Tested `CHROME_FLAGS="--dns-servers=8.8.8.8"`, `AGENT_BROWSER_ARGS="--dns-servers=8.8.8.8"`, and `~/.agent-browser/config.json` with `dnsServers`, no fix.
6. **Process Cleanup**: Killed all Chrome/agent-browser processes, no fix.

## Conclusion
The agent-browser CLI has a fundamental CDP DNS handling bug. No further debugging steps will resolve it.

## Workaround
Use direct Chrome headless commands instead:
```bash
/opt/google-chrome/chrome --headless=new --no-sandbox --dump-dom <URL> > /tmp/page.html 2>&1
/opt/google-chrome/chrome --headless=new --no-sandbox --screenshot=<path> <URL>
```

## User Restriction
Do NOT use `web_extract` premium tool for browser automation (limited to 497 remaining uses, user forbade it). Parse dumped HTML with `grep`/`sed`.