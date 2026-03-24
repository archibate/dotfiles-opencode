# Skill Self-Update Guide

This document describes how an AI agent can self-update this skill when bilibili-api releases new versions.

## Current Version

- **Version:** v17.4.1 (stable)
- **Commit:** 0147ab61
- **Original Repo:** https://github.com/Nemo2011/bilibili-api

## Prerequisites

The skill is self-contained and does not require a local clone of bilibili-api. It will clone the repo to a temporary directory when updates are needed.

## Update Workflow

### Step 1: Check for New Releases

```bash
# List recent tags from the original repo (no clone needed)
git ls-remote --tags --sort=-v:refname https://github.com/Nemo2011/bilibili-api | head -10

# Or use GitHub API
gh api repos/Nemo2011/bilibili-api/releases --jq '.[0:5] | .[] | "\(.tag_name) - \(.published_at)"'
```

### Step 2: Clone and Compare

```bash
# Clone the repo to a temp location
TEMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/Nemo2011/bilibili-api "$TEMP_DIR"

# Skill directory (relative to this file)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Compare docs folder
diff -r "$SKILL_DIR/references/docs" "$TEMP_DIR/docs" --brief
```

### Step 3: Identify Changed Modules

```bash
# If you have a previous version cloned, compare versions
OLD_DIR="/tmp/bilibili-api-old"
NEW_DIR="/tmp/bilibili-api-new"

git clone --depth 1 --branch v17.4.1 https://github.com/Nemo2011/bilibili-api "$OLD_DIR" 2>/dev/null || true
git clone --depth 1 https://github.com/Nemo2011/bilibili-api "$NEW_DIR"

# List changed docs
diff -rq "$OLD_DIR/docs" "$NEW_DIR/docs" | grep -E "differ|Only in $NEW_DIR"
```

### Step 4: Update Skill Files

For each changed module, update the corresponding skill reference:

| Changed File | Update This Skill File |
|--------------|------------------------|
| `docs/modules/video.md` | `references/video-guide.md` |
| `docs/modules/user.md` | `references/user-guide.md` |
| `docs/modules/live.md` | `references/live-guide.md` |
| `docs/modules/video_uploader.md` | `references/upload-guide.md` |
| `docs/get-credential.md` | `references/credential-setup.md` |
| `docs/configuration.md` | `references/configuration.md` |
| Any `docs/modules/*.md` | `references/api-modules.md` |

Sync the entire docs folder:
```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp -r "$TEMP_DIR/docs/"* "$SKILL_DIR/references/docs/"
```

### Step 5: Update Version Info

Update this file (`references/self-update.md`) with the new version:

```markdown
## Current Version

- **Version:** vX.Y.Z
- **Commit:** <new_commit_hash>
- **Original Repo:** https://github.com/Nemo2011/bilibili-api
```

Also update `SKILL.md` version in overview if major version changes.

## Update Script Template

```bash
#!/bin/bash
# update-skill.sh - Self-update bilibili-api skill
# Works independently - clones repo fresh when needed

set -e

# Resolve skill directory (script is in references/)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_URL="https://github.com/Nemo2011/bilibili-api"
TEMP_DIR=$(mktemp -d)

echo "=== bilibili-api Skill Updater ==="
echo "Skill directory: $SKILL_DIR"
echo ""

# Clone latest
echo "Cloning latest version..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

# Get version info
NEW_VERSION=$(cd "$TEMP_DIR" && git describe --tags --always 2>/dev/null || echo "unknown")
NEW_COMMIT=$(cd "$TEMP_DIR" && git rev-parse --short HEAD)

echo "Latest version: $NEW_VERSION (commit $NEW_COMMIT)"
echo ""

# Show what changed in docs
echo "=== Recent Documentation Files ==="
ls -la "$TEMP_DIR/docs/modules/" | head -20
echo ""

# Prompt for confirmation
read -p "Sync docs to skill? [y/N] " confirm
if [ "$confirm" != "y" ]; then
    echo "Aborted."
    rm -rf "$TEMP_DIR"
    exit 0
fi

# Sync docs to skill
echo ""
echo "Syncing docs..."
cp -r "$TEMP_DIR/docs/"* "$SKILL_DIR/references/docs/"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "=== Update Complete ==="
echo "Version: $NEW_VERSION"
echo "Commit: $NEW_COMMIT"
echo ""
echo "Next steps:"
echo "  1. Review docs in references/docs/"
echo "  2. Update affected reference guides (video-guide.md, user-guide.md, etc.)"
echo "  3. Update version info in references/self-update.md"
echo "  4. Test scripts/quickstart.py"
```

## Manual Update Checklist

When updating the skill manually:

1. [ ] Check for new releases at https://github.com/Nemo2011/bilibili-api/releases
2. [ ] Clone repo to temp: `git clone --depth 1 https://github.com/Nemo2011/bilibili-api /tmp/bili-update`
3. [ ] Sync `docs/` folder: `cp -r /tmp/bili-update/docs/* references/docs/`
4. [ ] Review changed modules
5. [ ] Update affected reference guides:
   - [ ] `references/credential-setup.md` (if auth changes)
   - [ ] `references/api-modules.md` (if new modules added)
   - [ ] `references/configuration.md` (if settings change)
   - [ ] `references/common-patterns.md` (if patterns change)
   - [ ] `references/video-guide.md` (if video module changes)
   - [ ] `references/user-guide.md` (if user module changes)
   - [ ] `references/live-guide.md` (if live module changes)
   - [ ] `references/upload-guide.md` (if uploader changes)
6. [ ] Update version in `references/self-update.md`
7. [ ] Test `scripts/quickstart.py` still works
8. [ ] Update `SKILL.md` description triggers if new features added
9. [ ] Cleanup temp clone: `rm -rf /tmp/bili-update`

## Breaking Changes to Watch For

- New required credential fields
- API method signature changes
- Deprecated methods removal
- New HTTP client requirements
- WebSocket event format changes
- Upload workflow changes
