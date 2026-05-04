# 10,000+ Files Issue — VPS GitHub Sync

## Symptoms
- VS Code shows 10,000+ files to commit
- `git ls-files | wc -l` returns 15,000+
- Push fails or times out
- Nested `.git` directory errors

## Root Causes (from 2026-05-03 session)

### 1. node_modules/ (everywhere)
- `.openclaw/extensions/` has 50+ nested node_modules
- `.openclaw/plugin-runtime-deps/` has 30+ nested node_modules
- `3_core_tools/hermes/engine/node_modules/`
- Total: 10,000+ files

**Fix:** Add to .gitignore:
```
node_modules/
*/node_modules/
**/node_modules/
```

### 2. .openclaw/ runtime data
- `.openclaw/credentials/whatsapp/` — 5,111 + 2,077 files
- `.openclaw/media/inbound/` — 571 files
- `.openclaw/extensions/` — runtime extensions
- `.openclaw/plugin-runtime-deps/` — dependencies

**Fix:** Add to .gitignore:
```
.openclaw/credentials/
.openclaw/media/
.openclaw/extensions/
.openclaw/plugin-runtime-deps/
```

### 3. WhatsApp data (Hermes)
- `3_core_tools/hermes/data/whatsapp/` — 14,140 files

**Fix:** Add to .gitignore:
```
3_core_tools/hermes/data/whatsapp/
3_core_tools/hermes/data/sessions/
3_core_tools/hermes/data/memories/
3_core_tools/hermes/data/*.db*
```

### 4. .cache/ and other runtime dirs
- `.cache/camoufox/` — fonts, addons
- `.cache/n8n/` — public assets
- `.cache/uv/` — Python packages
- `.vscode-server/` — VS Code server files

**Fix:** Add to .gitignore:
```
.cache/
.vscode-server/
.codex/
.gemini/
```

### 5. Nested .git directories
- `.openclaw/workspace/.git`
- `3_core_tools/hermes/engine/.git`
- `.cache/uv/git-v0/.../.git`

**Symptom:** `error: '.openclaw/workspace/' does not have a commit checked out`

**Fix:**
```bash
find /root -name '.git' ! -path '/root/.git' -exec rm -rf {} +
```

## Prevention Checklist

Before first commit:
```bash
# 1. Check file count (should be <2000)
cd /root && git ls-files | wc -l

# 2. Check top directories
cd /root && git ls-files | cut -d'/' -f1-2 | sort | uniq -c | sort -rn | head -10

# 3. If >2000 files, fix .gitignore first
# 4. Remove nested .git dirs
find /root -name '.git' ! -path '/root/.git' -exec rm -rf {} +

# 5. Re-add with corrected .gitignore
git reset HEAD .
git add -A
git commit -m "VPS backup (files reduced)"
```

## Result (2026-05-03)
- Before: 15,205 files (untracked thousands more)
- After: 1,035 files (33.4 MB)
- Push successful to `tbhrc/vps` (private)
