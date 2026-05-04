# GitHub API Patterns for AOS VPS Operations

## Create Private Repository

```python
import urllib.request
import json

token = "..."  # Read from .env programmatically

url = "https://api.github.com/user/repos"
data = json.dumps({
    "name": "vps",
    "private": True,
    "description": "AOS Hub VPS backup",
    "auto_init": False
}).encode('utf-8')

req = urllib.request.Request(url, data=data)
req.add_header("Authorization", f"token {token}")
req.add_header("Accept", "application/vnd.github.v3+json")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"SUCCESS! Repository created: {result.get('html_url')}")
        print(f"  Private: {result.get('private')}")
except urllib.error.HTTPError as e:
    error_body = json.loads(e.read().decode())
    print(f"ERROR {e.code}: {error_body.get('message')}")
```

## Check Repository Commits

```python
import urllib.request

url = "https://api.github.com/repos/tbhrc/vps/commits"
req = urllib.request.Request(url)
req.add_header("Authorization", f"token {token}")

with urllib.request.urlopen(req) as response:
    commits = json.loads(response.read().decode())
    print(f"Repository has {len(commits)} commit(s)")
    if commits:
        print(f"Latest: {commits[0]['commit']['message'][:60]}...")
```

## Common API Endpoints

| Operation | Endpoint |
|-----------|-----------|
| Create repo | `POST /user/repos` |
| List repos | `GET /user/repos` |
| Check commits | `GET /repos/{owner}/{repo}/commits` |
| Repo info | `GET /repos/{owner}/{repo}` |

## Notes

- Use `urllib.request` (stdlib) — no external dependencies needed
- Token format: `ghp_` prefix for Personal Access Tokens
- API docs: https://docs.github.com/en/rest/repos/repos
