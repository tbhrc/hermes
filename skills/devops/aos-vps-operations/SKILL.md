---
name: aos-vps-operations
description: "AOS Hub VPS operations — GitHub sync, secrets management, repo maintenance, and VPS-level procedures for the Agentic Operating System (Pillar 5)."
trigger:
  - User mentions syncing VPS files to GitHub
  - User mentions secrets, API keys, or .env management in AOS context
  - User asks to create/push to GitHub repo for VPS backup
  - Working with /root/ files, pillar structure, or VPS maintenance
---

# AOS VPS Operations

Procedures for managing the AOS Hub VPS — GitHub synchronization, secrets handling, and repository operations.

## Secrets Management Procedure (MANDATORY)

User established this procedure explicitly — follow it for ALL secret/API key handling:

1. **Never request secrets in chat** — "It is not a good idea And it is not smart to put any API keys and tokens over a public chat."
2. **Create entry in `.env`** — Add the key name to `/root/3_core_tools/hermes/data/.env`
3. **User provides the value** — User puts the actual secret value in the .env file
4. **Read programmatically** — Use `sed -n '11p' /root/3_core_tools/hermes/data/.env` (or appropriate line) to read tokens
5. **Never share in chat** — Never echo tokens, never request them via messaging platforms

### Reading Secrets Example

```bash
# Read token from .env (line 11 in our case)
TOKEN=$(sed -n '11p' /root/3_core_tools/hermes/data/.env | cut -d= -f2)
```

## File Management (Stale/Obsolete Files)
- **Stale files**: Move to `/root/archive/` (create with `mkdir -p /root/archive` if missing)
- **9_to_be_foldered/**: Only for unprocessed incoming files, NOT stale files
- **Update registry**: Log all archived files in `/root/7_vault/REPO/file_registry.md`
- **Never delete stale files**: Always archive to preserve history

## AOS Document Management (MANDATORY)
Covers discussion docs, manuals, and index updates per AOS Hub 12-pillar structure and user corrections.

### Discussion Doc Rules
- **Location**: All discussion docs (unimplemented plans, research notes) go to `/root/12_lab/3_discussions/` (Pillar 12 scratchpad)
- **Promotion**: Only move to `/root/9_manuals/` (Pillar 9, Master Manuals) after full implementation and verification
- **Examples**: `memory_system_selection.md`, `github_agent_tools_v2.md`, `google_workspace_discussion.md` are discussion docs, not manuals

### File Movement Protocol
When moving files between `/root/12_lab/3_discussions/` and `/root/9_manuals/`:
1. Update `/root/workspace_map.md` (high-level index): Add/remove entries from respective sections
2. Update `/root/7_vault/REPO/file_registry.md` (detailed account): Add/remove file entries
3. Verify disk existence: Always run `ls -la <path>` to confirm file is on disk before claiming movement/creation

### Disk-First Verification
- Never claim a file is created/moved without checking disk first (no phantom file references)
- Use `ls`, `search_files`, or `terminal` commands to verify file existence before updating indexes

### Canonical Output Standards
All output rules for WhatsApp/Telegram/CLI are documented in `/root/9_manuals/output_standards.md` (Pillar 9). Reference this manual for formatting, tone, and delivery rules.

## VPS-to-GitHub Sync Procedure

### Step 1: Check/Initialize Git Repo

```bash
cd /root
git status 2>/dev/null || git init
```

### Step2: Configure .gitignore (CRITICAL — DO THIS BEFORE FIRST COMMIT)

Per AOS Hub `AGENTS.md` rules, NEVER commit:
- `.env`, `.n8n/`, `.openclaw/`, `.ssh/` (sensitive)
- Large files (>100MB) — GitHub rejects these
- Runtime caches, node_modules, media data — causes 10,000+ file count

**Comprehensive .gitignore template:**
```
# Sensitive (per AGENTS.md)
.env
*.env
.n8n/
.openclaw/
.ssh/

# Runtime data (CAUSES 10,000+ FILES)
.openclaw/credentials/
.openclaw/media/
.openclaw/extensions/
.openclaw/plugin-runtime-deps/
.cache/
.local/
.config/
.azure/
.codex/
.gemini/
.npm/
.vscode-server/
.copilot/
.dotnet/

# Node.js (CAUSES 10,000+ FILES)
node_modules/
*/node_modules/
**/node_modules/

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/

# Large files (GitHub 100MB limit)
.agent-browser/
*.tar.gz
*.tar
*.zip
*.bak
*.sqlite
*.log.*
5_vps/3_storage/

# Build artifacts
dist/
build/

# OS files
.DS_Store
Thumbs.db
```

**Pre-commit check:**
```bash
# If this returns >2000, you have a problem
git ls-files | wc -l
```

**Common root causes of 10,000+ files:**
| Symptom | Root Cause | Fix |
|----------|-----------|-----|
| 15,000+ files | `node_modules/` not ignored | Add `node_modules/` and `**/node_modules/` |
| 5,000+ files | `.openclaw/whatsapp/` credentials/media | Add `.openclaw/credentials/`, `.openclaw/media/` |
| 500+ files | Hermes sessions, memories, state | Add `3_core_tools/hermes/data/sessions/`, `memories/`, `*.db*` |
| Push rejected | Nested `.git` directories | `find /root -name '.git' ! -path '/root/.git' -exec rm -rf {} +` |

### Step 3: Create Private GitHub Repo (if needed)

Use GitHub API with token from .env:

```python
import urllib.request
import json

# Read token
token = "..."  # Read from .env programmatically

url = "https://api.github.com/user/repos"
data = json.dumps({
    "name": "vps",
    "private": True,
    "auto_init": False
}).encode('utf-8')

req = urllib.request.Request(url, data=data)
req.add_header("Authorization", f"token {token}")
req.add_header("Accept", "application/vnd.github.v3+json")

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode())
    print(f"Repo created: {result['html_url']}")
```

### Step 4: Commit and Push

```bash
cd /root
git config user.name "AOS Hub"
git config user.email "admin@xva.ae"
git remote remove origin 2>/dev/null
git remote add origin https://${TOKEN}@github.com/tbhrc/vps.git
git add -A
git commit -m "Sync VPS files (large files excluded)"
git config --global http.postBuffer 524288000  # 500MB buffer
git push -u origin master
```

## Pitfalls

| Issue | Cause | Solution |
|-------|------|----------|
| `Host key verification failed` | SSH remote when using HTTPS token | Use `git remote add origin https://TOKEN@github.com/...` (not set-url) |
| `HTTP 408` timeout | Push too large | Increase `http.postBuffer` to 500MB, check file count |
| `file is 264.09 MB; exceeds 100.00 MB` | GitHub file size limit | Add to `.gitignore`, `git rm --cached`, amend commit |
| `fatal: the remote end hung up unexpectedly` | Push too large for default buffer | `git config --global http.postBuffer 524288000` |
| SSH still used after setting HTTPS URL | Shell escaping issue with token in URL | Remove and re-add remote: `git remote remove origin && git remote add origin https://TOKEN@...` |
| **`10,000+ files` in VS Code/git status** | **node_modules, .openclaw, .cache, whatsapp data** | **Use comprehensive .gitignore (see Step2), run `git ls-files | wc -l` before commit** |
| **`error: '.openclaw/workspace/' does not have a commit checked out`** | **Nested .git directories** | **`find /root -name '.git' ! -path '/root/.git' -exec rm -rf {} +` before `git add -A`** |
| **Push blocked/fails repeatedly** | Force push (-f) prompts confirmation | Use normal push if repo is empty, or push via URL directly: `git push https://TOKEN@github.com/...` |

## GitHub API Reference

See `references/github-api.md` for detailed API patterns.

## Large Files Reference

See `references/large-files.md` for patterns to exclude from VPS sync.

## 10,000+ Files Issue

If VS Code shows 10,000+ files to commit, see `references/10000-files-issue.md` for root causes (node_modules, .openclaw, .cache, nested .git) and prevention checklist.
