# How to Release Your Skill

This guide explains how to create a new release using GitHub Actions.

## Prerequisites

- Repository pushed to GitHub
- GitHub Actions workflow configured (`.github/workflows/release-skill.yml`)
- `gh` CLI installed and authenticated
- Git configured with proper credentials

## Release Process

### Step 1: Update Version

Update the VERSION file with the new release version:

```bash
# Navigate to repository
cd /path/to/your-skill-name

# Update version (example: 1.0.0)
echo "1.0.0" > VERSION

# Verify version
cat VERSION
```

### Step 2: Commit Version Change

```bash
# Stage version file
git add VERSION

# Commit with clear message
git commit -m "Release v1.0.0"

# Push to GitHub
git push origin main
```

### Step 3: Create GitHub Release

**Using gh CLI (Recommended):**

```bash
# Create release with auto-generated notes
gh release create v1.0.0 \
  --title "v1.0.0" \
  --generate-notes

# OR with custom notes
gh release create v1.0.0 \
  --title "Your Skill v1.0.0" \
  --notes "First stable release.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
Download {skill-name}-skill.zip from assets and extract to your Claude Code skills directory."
```

**Using GitHub Web UI:**

1. Go to your repository releases page
2. Click "Draft a new release"
3. Click "Choose a tag" → Type `v1.0.0` → "Create new tag: v1.0.0 on publish"
4. Set "Release title" to `v1.0.0`
5. Click "Generate release notes" or write custom notes
6. Click "Publish release"

### Step 4: Monitor GitHub Actions

GitHub Actions will automatically:

1. Checkout code at the release tag
2. Extract version from VERSION file
3. Verify skill structure (SKILL.md with frontmatter)
4. Build distribution (create {skill-name}-skill.zip)
5. Validate archive structure
6. Upload artifact (90-day retention)
7. Attach to release

**Monitor the workflow:**

```bash
# Watch workflow status
gh run watch

# OR view in browser
gh run view --web
```

### Step 5: Verify Release

```bash
# Open release in browser
gh release view v1.0.0 --web

# View release details
gh release view v1.0.0
```

**Verify assets:**

1. Check release page has `{skill-name}-skill.zip` attached
2. Download and test:

```bash
# Download release asset
gh release download v1.0.0

# Test extraction
mkdir -p test-install
unzip {skill-name}-skill.zip -d test-install

# Verify structure
ls -la test-install/{skill-name}/
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
  - **MAJOR**: Breaking changes
  - **MINOR**: New features (backward compatible)
  - **PATCH**: Bug fixes (backward compatible)

**Examples:**

- `0.0.1` - Initial development
- `0.1.0` - First feature complete
- `1.0.0` - First stable release
- `1.1.0` - Added new feature
- `1.1.1` - Bug fix
- `2.0.0` - Breaking change

## Troubleshooting

### Workflow Fails

```bash
# Check logs
gh run list --workflow=release-skill.yml
gh run view <failed-run-id> --log
```

**Common issues:**

- VERSION file not found → Ensure VERSION exists in root
- SKILL.md validation failed → Check YAML frontmatter
- Archive validation failed → Verify required files exist

### Re-running Failed Release

```bash
# Delete and recreate release
gh release delete v1.0.0 --yes
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
# Then recreate release (Step 3)
```

## Release Checklist

- [ ] Update VERSION file
- [ ] Update README.md if needed
- [ ] Test locally
- [ ] Commit all changes
- [ ] Push to GitHub
- [ ] Create release tag
- [ ] Monitor GitHub Actions
- [ ] Verify release assets
- [ ] Test installation from release ZIP

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Reference](https://cli.github.com/manual/)
- [Semantic Versioning](https://semver.org/)
