---
name: github-fetch
description: Use this skill when studying GitHub repositories for one-off analysis, reading source code, or fetching single files from GitHub. TRIGGER when "study this repo", "install this repo", "read the README of X", "inspect source of X", "fetch file from GitHub", or any request to explore/analyze a GitHub project without making it a permanent workspace.
color: cyan
---

# GitHub Fetch

## When to Use
- Studying source code of a GitHub repo for one-off analysis
- Reading a single file or small number of files from a repo
- Exploring project structure, implementation patterns, or API design
- Not for permanent work — use a proper workspace for that

## Mode 1: Full Repo Clone

Clone to the standard temp location with shallow depth:

```bash
git clone https://github.com/{user}/{repo} --depth=1 /tmp/github/{user}/{repo}
```

Then work in `/tmp/github/{user}/{repo}` using Read, Grep, Glob tools.

If the repo is already cloned, reuse it — do not re-clone.

```bash
# Check first
ls /tmp/github/{user}/{repo} 2>/dev/null || git clone https://github.com/{user}/{repo} --depth=1 /tmp/github/{user}/{repo}
```

## Mode 2: Single File Fetch

For reading one file without cloning the whole repo, use WebFetch with the raw URL:

```
https://raw.githubusercontent.com/{user}/{repo}/main/{path/to/file}
```

Or with curl:

```bash
curl -fsSL https://raw.githubusercontent.com/{user}/{repo}/main/{path/to/file}
```

Try `main` first; fall back to `master` if the file is not found.

## Rules
- Always use `--depth=1` — no history needed for study
- `/tmp/github/` is the standard clone location (auto-cleaned on reboot)
- Do not commit or push changes from `/tmp` clones
- Prefer Mode 2 (single file) when only one or two files are needed — faster and lighter
- Prefer Mode 1 (full clone) when exploring structure, searching across files, or reading many files
