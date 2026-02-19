---
name: extract-repo
description: Download GitHub repos as clean source code (no .git history) to WORKDIR. Use when cloning repos for analysis or modification. Not for monorepos.
---

# Extract Repo

Download GitHub repositories as clean source code without git history.

## Usage

Run via subagent:

```bash
uv run .opencode/skill/extract-repo/scripts/extract_repo.py <URL>
```

then `cd` into the extract directory.

## Available Flags

| Flag        | Description                               |
| ----------- | ----------------------------------------- |
| `--help`    | Show help message                         |
| `--dry-run` | Preview what would happen without cloning |
| `--list`    | List all managed repos (newest first)     |

## Examples

```bash
# Clone a repo
uv run .opencode/skill/extract-repo/scripts/extract_repo.py https://github.com/user/repo

# Works with any GitHub URL (normalizes automatically)
uv run .opencode/skill/extract-repo/scripts/extract_repo.py https://github.com/user/repo/blob/main/README.md

# Preview without cloning
uv run .opencode/skill/extract-repo/scripts/extract_repo.py --dry-run https://github.com/user/repo

# List managed repos
uv run .opencode/skill/extract-repo/scripts/extract_repo.py --list
```

## Notes

- Repos are saved to `WORKDIR/` with a `.extract_repo` marker
- If a repo name already exists, a suffix is added (e.g., `repo-2`)
- The `--remove` flag exists but is interactive; do not use it in automated contexts
