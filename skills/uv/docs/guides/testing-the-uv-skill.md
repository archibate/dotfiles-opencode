# Testing the UV Skill

This guide provides specific test cases for manually testing the UV skill to ensure it works correctly with Claude Code.

## Overview

Testing focuses on verifying that Claude Code correctly invokes the UV skill and provides accurate guidance for Python package management, tool installation, MCP server integration, and virtual environment management.

## Prerequisites

- [ ] UV skill installed in `~/.claude/skills/uv/` or `$USERPROFILE/.claude/skills/uv/`
- [ ] UV installed and accessible in PATH (`uv --version` works)
- [ ] Python 3.8+ installed
- [ ] Claude Code configured and running

## Installation for Testing

### Claude Code CLI

```bash
# Windows (Git Bash)
cd "$USERPROFILE/.claude/skills"
cp -r /path/to/uv-skill/ ./uv/

# Unix/Mac
cd ~/.claude/skills
cp -r /path/to/uv-skill/ ./uv/
```

### Verify Installation

```bash
# Check skill directory
ls -la ~/.claude/skills/uv/

# Verify SKILL.md exists
cat ~/.claude/skills/uv/SKILL.md | head -20
```

## Test Scenarios

### Test Case 1: Basic UV Installation Guidance

**User Request:**

```text
"How do I install UV on Windows?"
```

**Alternative Variations:**

- "Set up UV for Python development"
- "Install UV package manager"
- "Get started with UV"

**Expected Behavior:**

1. Claude should recognize this matches the UV skill
2. Claude should provide installation instructions for Windows
3. Should mention adding UV to PATH
4. Should reference the Installation & Setup reference document

**Expected Output:**

- Installation command (e.g., PowerShell installer or Scoop)
- PATH configuration instructions
- Verification command (`uv --version`)

**Validation:**

- [ ] Skill activated automatically
- [ ] Platform-specific installation provided
- [ ] PATH setup instructions included
- [ ] Verification step included

### Test Case 2: Tool Install vs UVX Decision

**User Request:**

```text
"Should I use uv tool install or uvx for Black formatter?"
```

**Alternative Variations:**

- "How to install Black with UV?"
- "Difference between uv tool install and uvx"
- "Best way to install development tools with UV"

**Expected Behavior:**

1. Claude should recognize this involves tool management decision
2. Should explain `uv tool install` is appropriate for daily tools
3. Should provide example: `uv tool install black`
4. Should explain UVX is for temporary/one-off execution

**Expected Output:**

```text
For Black formatter (daily development tool):
- Use: uv tool install black
- Reason: Used frequently, benefits from persistent installation
```

**Validation:**

- [ ] Correctly recommends `uv tool install` for Black
- [ ] Explains rationale (frequent use)
- [ ] Provides example command
- [ ] References decision tree if needed

### Test Case 3: MCP Server Configuration

**User Request:**

```text
"How do I configure mcp-server-sqlite with uvx in VS Code?"
```

**Alternative Variations:**

- "Set up MCP server with UV in VS Code"
- "Configure .vscode/mcp.json for UV"
- "Run MCP server using UVX"

**Expected Behavior:**

1. Claude should recognize this is MCP integration
2. Should provide VS Code configuration example
3. Should use `uvx` command (not `uv tool install`)
4. Should show proper JSON structure for .vscode/mcp.json

**Expected Output:**

```json
{
  "servers": {
    "sqlite": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "${workspaceFolder}/db.sqlite"]
    }
  }
}
```

**Validation:**

- [ ] Uses `uvx` (not `uv tool install`)
- [ ] Proper JSON structure
- [ ] Includes required fields (type, command, args)
- [ ] Uses VS Code variables if appropriate

### Test Case 4: Local MCP Server Development

**User Request:**

```text
"I'm developing a custom MCP server locally. How do I configure it with UV?"
```

**Alternative Variations:**

- "Run local Python MCP server with UVX"
- "Use --from flag with UVX for local development"
- "Configure local MCP server in VS Code with UV"

**Expected Behavior:**

1. Claude should recognize local development scenario
2. Should recommend `--from` flag approach
3. Should provide example configuration
4. Should emphasize absolute paths

**Expected Output:**

```json
{
  "servers": {
    "my-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "/absolute/path/to/project",
        "server.py",
        "--config", "config.json"
      ]
    }
  }
}
```

**Validation:**

- [ ] Uses `--from` flag correctly
- [ ] Explains absolute path requirement
- [ ] Proper argument structure
- [ ] References MCP Integration reference if needed

### Test Case 5: Virtual Environment Setup

**User Request:**

```text
"How do I create and activate a virtual environment with UV?"
```

**Alternative Variations:**

- "Set up Python venv with UV"
- "Create virtual environment for Python project"
- "Activate virtual environment on Windows"

**Expected Behavior:**

1. Claude should provide venv creation command
2. Should provide platform-specific activation instructions
3. Should explain using `uv pip install` in activated environment
4. Should mention faster performance vs regular pip

**Expected Output:**

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows Git Bash)
. .venv/Scripts/activate

# Install packages with UV
uv pip install -r requirements.txt
```

**Validation:**

- [ ] Shows venv creation
- [ ] Platform-specific activation
- [ ] Shows UV usage in activated environment
- [ ] Mentions performance benefits

### Test Case 6: Python Version Management

**User Request:**

```text
"How do I install and use Python 3.12 with UV?"
```

**Alternative Variations:**

- "Manage Python versions with UV"
- "Switch Python version in UV project"
- "Install specific Python version"

**Expected Behavior:**

1. Claude should explain Python version installation
2. Should show `uv python install` command
3. Should show `uv python pin` for project-specific version
4. Should mention listing available versions

**Expected Output:**

```bash
# Install Python 3.12
uv python install 3.12

# Pin to project
uv python pin 3.12

# List available versions
uv python list
```

**Validation:**

- [ ] Shows installation command
- [ ] Shows pinning command
- [ ] Mentions listing versions
- [ ] Explains project-specific configuration

### Test Case 7: Inline Script Dependencies (PEP 723)

**User Request:**

```text
"How can I create a single Python script with dependencies using UV?"
```

**Alternative Variations:**

- "Use PEP 723 inline dependencies with UV"
- "Self-contained Python script with dependencies"
- "UV inline script metadata"

**Expected Behavior:**

1. Claude should explain PEP 723 inline dependencies
2. Should provide example with comment-based dependencies
3. Should show `uv run script.py` command
4. Should reference Inline Script Metadata reference

**Expected Output:**

```python
# /// script
# dependencies = [
#   "requests",
#   "pandas",
# ]
# ///

import requests
import pandas as pd
```

Run with: `uv run script.py`

**Validation:**

- [ ] Shows correct comment syntax
- [ ] Explains automatic dependency installation
- [ ] Provides execution command
- [ ] Mentions reference document

### Test Case 8: Migration from pip/pipx

**User Request:**

```text
"I'm currently using pip and pipx. How do I migrate to UV?"
```

**Alternative Variations:**

- "Switch from pipx to UV"
- "Convert pip commands to UV"
- "Migrate Python tools to UV"

**Expected Behavior:**

1. Claude should provide migration comparison
2. Should show before/after examples
3. Should explain benefits (speed, isolation)
4. Should cover both package and tool installation

**Expected Output:**

```bash
# Old way (pip)
pip install requests

# New way (UV)
uv pip install requests

# Old way (pipx)
pipx install black

# New way (UV)
uv tool install black
```

**Validation:**

- [ ] Shows clear before/after comparison
- [ ] Covers both pip and pipx migration
- [ ] Explains benefits
- [ ] Mentions tool isolation

### Test Case 9: Error Handling - UV Not Found

**Setup:**

Simulate scenario where UV is not installed or not in PATH.

**User Request:**

```text
"I'm getting 'spawn uvx ENOENT' error when running MCP server"
```

**Alternative Variations:**

- "UV command not found"
- "uvx not in PATH"
- "Can't find UV executable"

**Expected Behavior:**

1. Claude should recognize this as PATH/installation issue
2. Should suggest verifying UV installation
3. Should provide PATH verification commands
4. Should suggest reinstallation if needed

**Expected Output:**

- Check UV installation: `uv --version`
- Check PATH configuration
- Reinstallation instructions if needed
- Link to troubleshooting in references

**Validation:**

- [ ] Identifies PATH/installation issue
- [ ] Provides verification commands
- [ ] Suggests solutions
- [ ] References troubleshooting documentation

### Test Case 10: Advanced - GitHub Actions Integration

**User Request:**

```text
"How do I use UV in GitHub Actions for CI/CD?"
```

**Alternative Variations:**

- "Set up UV in GitHub Actions workflow"
- "CI/CD configuration for UV"
- "Install dependencies with UV in Actions"

**Expected Behavior:**

1. Claude should provide GitHub Actions workflow example
2. Should use official `astral-sh/setup-uv` action
3. Should show dependency installation and test execution
4. Should explain benefits for CI performance

**Expected Output:**

```yaml
- name: Setup UV
  uses: astral-sh/setup-uv@v1

- name: Install dependencies
  run: uv pip install -r requirements.txt

- name: Run tests
  run: uv run pytest
```

**Validation:**

- [ ] Uses official action
- [ ] Shows proper workflow structure
- [ ] Includes dependency installation
- [ ] Shows test execution example

### Test Case 11: Python 3.14 Default Version (UV 0.9.6+)

**User Request:**

```text
"What Python version will UV install by default?"
```

**Alternative Variations:**

- "Install Python with UV without specifying version"
- "What's the default Python version in UV?"
- "Create new UV project - which Python version?"

**Expected Behavior:**

1. Claude should mention Python 3.14 is now the default (as of UV 0.9.6)
2. Should explain how to check UV version
3. Should show how to explicitly pin to different version if needed
4. Should reference the Recent Changes documentation

**Expected Output:**

```bash
# Check UV version first
uv --version

# UV 0.9.6+ installs Python 3.14 by default
uv python install
# Installs Python 3.14

# To use a specific version
uv python install 3.13
uv python pin 3.13
```

**Validation:**

- [ ] Mentions Python 3.14 as default (for UV 0.9.6+)
- [ ] Shows version check command
- [ ] Explains how to pin specific version
- [ ] References version compatibility

### Test Case 12: Free-Threaded Python Support (UV 0.9.6+)

**User Request:**

```text
"How do I use free-threaded Python with UV?"
```

**Alternative Variations:**

- "Does UV support Python without GIL?"
- "Install free-threaded Python 3.14"
- "How to enable parallel threading in Python with UV?"

**Expected Behavior:**

1. Claude should explain free-threaded Python concept (PEP 703)
2. Should mention it's available in Python 3.14+ without explicit opt-in
3. Should provide example showing parallel execution benefits
4. Should reference Recent Changes documentation

**Expected Output:**

```bash
# Install Python 3.14 (includes free-threading support)
uv python install 3.14

# Verify installation
uv python list

# Use in project
uv python pin 3.14
```

Example showing benefits:

```python
# Multi-threaded code runs in true parallel with Python 3.14+
import threading

def cpu_task():
    result = sum(i**2 for i in range(10_000_000))
    return result

threads = [threading.Thread(target=cpu_task) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Validation:**

- [ ] Explains free-threaded Python concept
- [ ] Mentions no explicit opt-in needed (UV 0.9.6+)
- [ ] Shows installation command
- [ ] Provides practical example
- [ ] Explains performance benefits

### Test Case 13: Build --clear Flag (UV 0.9.6+)

**User Request:**

```text
"How do I clean old build artifacts before building with UV?"
```

**Alternative Variations:**

- "Remove dist folder before building"
- "Clean build with UV"
- "UV build with automatic cleanup"

**Expected Behavior:**

1. Claude should mention `--clear` flag added in UV 0.9.6
2. Should show command usage
3. Should explain it removes old artifacts automatically
4. Should mention version requirement

**Expected Output:**

```bash
# Check UV version (needs 0.9.6+)
uv --version

# Build with automatic cleanup
uv build --clear

# Old workflow (no longer needed)
# rm -rf dist/
# uv build
```

**Validation:**

- [ ] Mentions `--clear` flag
- [ ] Shows correct command syntax
- [ ] Explains automatic cleanup behavior
- [ ] Mentions version requirement (0.9.6+)

### Test Case 14: UV Version Check and Upgrade

**User Request:**

```text
"How do I check if my UV is up to date?"
```

**Alternative Variations:**

- "Check UV version"
- "Upgrade UV to latest version"
- "What version of UV do I have?"

**Expected Behavior:**

1. Claude should show version check command
2. Should provide upgrade instructions
3. Should mention latest version (0.9.7 as of October 2025)
4. Should reference Recent Changes documentation

**Expected Output:**

```bash
# Check current version
uv --version

# Upgrade using pip
pip install --upgrade uv

# Or reinstall using official installer
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Unix/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Validation:**

- [ ] Shows version check command
- [ ] Provides upgrade instructions
- [ ] Mentions latest stable version
- [ ] Shows platform-specific installers

### Test Case 15: Version-Specific Feature Guidance

**User Request:**

```text
"I'm using UV 0.9.5. Can I use the --clear flag?"
```

**Alternative Variations:**

- "What features are available in my UV version?"
- "Do I need to upgrade UV for Python 3.14?"
- "Version compatibility check"

**Expected Behavior:**

1. Claude should identify that `--clear` requires UV 0.9.6+
2. Should recommend upgrading if needed
3. Should explain what features are available in user's version
4. Should reference version compatibility matrix

**Expected Output:**

```text
The --clear flag was added in UV 0.9.6. Your version (0.9.5) doesn't support it yet.

To use this feature, upgrade UV:

pip install --upgrade uv

After upgrading, you can use:
uv build --clear
```

**Validation:**

- [ ] Correctly identifies version requirements
- [ ] Recommends upgrade when needed
- [ ] Provides clear upgrade path
- [ ] References compatibility information

## Troubleshooting

### Skill Doesn't Activate

**Symptoms:**

- Claude doesn't use the UV skill when expected
- Claude says "I don't have access to that information"

**Checks:**

1. **Verify installation:**

   ```bash
   ls ~/.claude/skills/uv/SKILL.md
   ```

2. **Check SKILL.md format:**

   ```bash
   head -10 ~/.claude/skills/uv/SKILL.md
   ```

   Should show:

   ```yaml
   ---
   name: uv
   description: This skill should be used when...
   ---
   ```

3. **Try being explicit:**
   Instead of: "How do I install packages?"
   Try: "Use the UV skill to help me install Python packages"

4. **Restart Claude Code:**
   - Skills are loaded on startup
   - Restart may be needed after installation

### Incorrect Guidance Provided

**Symptoms:**

- Claude recommends `uv tool install` for MCP servers (incorrect)
- Claude suggests wrong configuration pattern

**Checks:**

1. **Verify skill version:**
   Check VERSION file and ensure it's the latest

2. **Check reference documents:**
   Ensure references/ directory is included and accessible

3. **Report issue:**
   If guidance is consistently incorrect, report in GitHub issues

## Testing Checklist

### Pre-Test Setup

- [ ] Skill installed in correct directory
- [ ] UV installed and in PATH
- [ ] SKILL.md has valid frontmatter
- [ ] Reference documents present

### Core Functionality

- [ ] Test Case 1: Basic UV installation ✓
- [ ] Test Case 2: Tool install vs UVX ✓
- [ ] Test Case 3: MCP server configuration ✓
- [ ] Test Case 4: Local MCP development ✓
- [ ] Test Case 5: Virtual environment setup ✓
- [ ] Test Case 6: Python version management ✓
- [ ] Test Case 7: Inline script dependencies ✓
- [ ] Test Case 8: Migration guidance ✓
- [ ] Test Case 9: Error handling ✓
- [ ] Test Case 10: GitHub Actions integration ✓

### Recent Features (UV 0.9.6+)

- [ ] Test Case 11: Python 3.14 default version ✓
- [ ] Test Case 12: Free-threaded Python support ✓
- [ ] Test Case 13: Build --clear flag ✓
- [ ] Test Case 14: UV version check and upgrade ✓
- [ ] Test Case 15: Version-specific feature guidance ✓

### Documentation Quality

- [ ] SKILL.md description triggers skill correctly
- [ ] Instructions are clear and accurate
- [ ] Examples work as documented
- [ ] References are accessible and relevant

## Test Results Template

```markdown
# UV Skill Test Results

**Date:** YYYY-MM-DD
**Platform:** Windows/macOS/Linux
**Claude Code Version:** X.X.X
**UV Version:** X.X.X
**Tester:** [Name]

## Environment

- OS: [OS details]
- Shell: [bash/zsh/Git Bash/PowerShell]
- Python Version: [version]
- UV Version: [version]

## Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| 1. Basic UV installation | ✓ PASS | |
| 2. Tool install vs UVX | ✓ PASS | |
| 3. MCP server config | ✓ PASS | |
| 4. Local MCP development | ✓ PASS | |
| 5. Virtual environment | ✓ PASS | |
| 6. Python version mgmt | ✓ PASS | |
| 7. Inline script deps | ✓ PASS | |
| 8. Migration guidance | ✓ PASS | |
| 9. Error handling | ✓ PASS | |
| 10. GitHub Actions | ✓ PASS | |
| 11. Python 3.14 default | ✓ PASS | |
| 12. Free-threaded Python | ✓ PASS | |
| 13. Build --clear flag | ✓ PASS | |
| 14. Version check/upgrade | ✓ PASS | |
| 15. Version-specific features | ✓ PASS | |

## Issues Found

[List any issues with detailed descriptions]

## Recommendations

[Suggestions for improvements to SKILL.md or reference documents]

## Overall Assessment

☐ Ready for release
☐ Needs minor fixes
☐ Needs major revision
```

## Best Practices

### 1. Test Incrementally

- Test after each change to SKILL.md or references
- Don't build everything before testing
- Catch issues early

### 2. Use Real Scenarios

- Test with actual use cases from UV documentation
- Get feedback from real UV users
- Verify against official UV patterns

### 3. Cross-Platform Testing

- Test on Windows (Git Bash and PowerShell)
- Test on macOS (if available)
- Test on Linux (if available)
- Document platform-specific issues

### 4. Version Testing

- Test each version before release
- Keep test results for each version
- Track regression issues

### 5. Reference Document Testing

- Verify references load correctly
- Check that grep patterns work
- Ensure examples in references are accurate

## Resources

- [UV Official Documentation](https://docs.astral.sh/uv/)
- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Skill Authoring Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
