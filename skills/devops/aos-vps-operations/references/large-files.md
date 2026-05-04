# Large Files — GitHub Push Exclusions

GitHub rejects files >100MB during push. These patterns must be in `.gitignore` before pushing.

## Files Found Too Large (this session)

| File | Size | Resolution |
|------|------|------------|
| `.agent-browser/browsers/chrome-148.0.7778.97/chrome` | 264.09 MB | Add `.agent-browser/` to `.gitignore` |
| `openclaw_backup_20260503.tar.gz` | 1,102.93 MB | Add `*.tar.gz` to `.gitignore` |

## Patterns to Exclude (add to `.gitignore`)

```
# Large files (exceed GitHub 100MB limit)
*.tar.gz
*.tar
*.zip
*.bak
.agent-browser/
5_vps/3_storage/
```

## Removing Large Files from Git Index

If already committed, remove from index (keeps local file):

```bash
cd /root
git rm --cached path/to/large-file
git rm --cached -r .agent-browser/  # Directory
git commit --amend -m "Removed large files"
```

## Verify Before Push

```bash
# Check for large files before pushing
cd /root
find . -type f -size +100M | grep -v ".git/"
```

## GitHub Limits

- Max file size: 100MB (hard limit)
- For larger files, use [Git LFS](https://git-lfs.github.com/) (not configured for AOS VPS)
- Push buffer: increase if timeout occurs: `git config --global http.postBuffer 524288000`
