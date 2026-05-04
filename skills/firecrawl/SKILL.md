---
name: firecrawl
description: "Firecrawl web scraping: local setup, API usage, MCP integration with Hermes."
version: 1.1.0
author: A1 Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Web Scraping, Firecrawl, MCP, API]
    related_skills: [native-mcp, agent-browser]
---

# Firecrawl Skill

## Trigger Conditions
- User asks to scrape a website, crawl a website, or search the web
- User mentions "Firecrawl" or "web scraping for AI"
- Need to extract clean markdown/JSON from a URL
- Need to crawl entire website or discover all URLs

## Prerequisites
- Firecrawl API server running at http://localhost:3002 (or cloud API key)
- For local setup: Redis + PostgreSQL running, .env configured (see /root/3_core_tools/firecrawl/apps/api/.env)
- Go 1.26.2+ (snap install go --classic) for API server

## Core Endpoints

### 1. Scrape (Single URL)
Extract content from a single URL as markdown, HTML, or JSON.

**curl example:**
```bash
curl -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown", "html"]}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "markdown": "# Page Title\n\nContent here...",
    "html": "<html>...</html>",
    "metadata": {"title": "...", "description": "..."},
    "statusCode": 200
  }
}
```

### 2. Crawl (Entire Website)
Scrape all URLs on a website.

**curl example:**
```bash
curl -X POST http://localhost:3002/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "limit": 100}'
```

### 3. Map (Discover URLs)
Get all URLs on a website instantly.

**curl example:**
```bash
curl -X POST http://localhost:3002/v1/map \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 4. Search
Search the web and get full page content.

**curl example:**
```bash
curl -X POST http://localhost:3002/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "firecrawl", "limit": 5}'
```

## Step-by-Step: Scrape a URL

1. **Verify Firecrawl is running:**
   ```bash
   curl -s http://localhost:3002/ | grep -o "Firecrawl API"
   ```

2. **Scrape the URL:**
   ```bash
   curl -X POST http://localhost:3002/v1/scrape \
     -H "Content-Type: application/json" \
     -d '{"url": "<URL_TO_SCRAPE>"}' | python3 -m json.tool
   ```

3. **Extract markdown from response:**
   Use `jq` or Python to parse the JSON response and extract `data.markdown`.

## Pitfalls

### DNS Resolution (VPS-Specific)
The VPS has DNS issues (systemd-resolved 127.0.0.53 misbehaving). Fix:
```bash
systemctl stop systemd-resolved
echo "nameserver 1.1.1.1" > /etc/resolv.conf
echo "nameserver 1.0.0.1" >> /etc/resolv.conf
```
Cloudflare DNS (1.1.1.1) works; Google DNS (8.8.8.8) may fail for some npm registries.
**Verification**: `curl -s -o /dev/null -w "%{http_code}" https://registry.npmjs.org` should return 200.

### Go Dependency
Firecrawl API requires Go (snap install go --classic). Without Go, server exits immediately.
Verify: `go version` should show 1.26.2+.

### Harness Errors
Don't use `pnpm start` (tries to manage Docker containers/RabbitMQ). Run directly:
```bash
cd /root/3_core_tools/firecrawl/apps/api && node dist/src/index.js
```

### Port Conflicts
Default port is 3002. Check .env if changed.

### PostgreSQL/Redis
Must be running locally if not using Docker:
```bash
systemctl start redis-server && systemctl start postgresql
```

### pnpm DNS Cache
Even with /etc/resolv.conf fixed, Node.js/pnpm may cache bad DNS. If pnpm install fails, verify curl works first.

## Verification
After scraping, verify:
1. Response has `"success": true`
2. `data.markdown` is not empty
3. `data.statusCode` is 200

## MCP Integration with Hermes

Add to `/root/3_core_tools/hermes/data/config.yaml` under `mcp_servers:`:
```yaml
  firecrawl-mcp:
    command: npx
    args: ["-y", "firecrawl-mcp"]
    env:
      FIRECRAWL_API_URL: "http://localhost:3002"
```

Restart Hermes to discover tools (appear as `mcp_firecrawl-mcp_*`).

## Local Setup Checklist

1. Clone: `git clone https://github.com/firecrawl/firecrawl.git /root/3_core_tools/firecrawl/`
2. Install deps: `apt install -y redis-server postgresql`
3. Install Go: `snap install go --classic`
4. Fix DNS: Use 1.1.1.1 (see Pitfalls)
5. Configure .env: Set REDIS_URL=redis://localhost:6379, USE_DB_AUTHENTICATION=false
6. Install packages: `cd /root/3_core_tools/firecrawl/apps/api && pnpm install`
7. Start server: `node dist/src/index.js`
8. Verify: `curl http://localhost:3002/` → "Firecrawl API"

## References
- Documentation: https://docs.firecrawl.dev/
- API Reference: https://docs.firecrawl.dev/api-reference/introduction
- GitHub: https://github.com/firecrawl/firecrawl
- Local Setup: /root/3_core_tools/firecrawl/
- Discussion Doc: /root/12_lab/3_discussions/2026-05-04_firecrawl_research_plan.md
- AOS Hub Protocol: `aos-hub-task-protocol` skill
