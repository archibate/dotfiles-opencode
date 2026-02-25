---
name: uv
description: This skill should be used when the user asks about UV (Python package manager), needs to set up Python virtual environments, install/manage Python CLI tools, run MCP servers with UVX, decide between uv tool install vs uvx, configure VS Code or IDEs for MCP server integration, migrate from pip/pipx/poetry to UV, or troubleshoot UV-related issues. Use when queries mention UV, UVX, Python package management, virtual environments, MCP servers, tool installation, or Python version management.
---

# UV - Python Package Manager Skill

## Overview

UV is an extremely fast Python package and project manager written in Rust. This skill provides guidance on using UV for Python development, with particular focus on MCP (Model Context Protocol) server integration and modern tool management workflows.

UV replaces multiple tools: pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more - delivering 10-100x faster performance through intelligent caching and parallel operations.

## Version Awareness

**Recommended Version: UV 0.9.7+** (Latest as of October 2025)

Before starting, check your UV version:

```bash
uv --version
```

**Important Version-Specific Changes:**

- **UV 0.9.6+**: Python 3.14 is now the default (previously 3.13)
- **UV 0.9.6+**: Free-threaded Python 3.14+ supported without explicit opt-in
- **UV 0.9.6+**: `uv build --clear` flag available for cleaning build artifacts
- **UV 0.9.7+**: Security updates for tar/ZIP archive handling

If your version is older than 0.9.0, upgrade for the best experience:

```bash
# Using pip
pip install --upgrade uv

# Or reinstall using official installer
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Unix/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See [Recent Changes Reference](references/recent-changes.md) for detailed version information and migration guidance.

## When to Use This Skill

Use this skill when:

- Setting up Python virtual environments and managing Python versions
- Installing and managing Python CLI tools (development tools, utilities)
- Running MCP servers with UVX
- Deciding between `uv tool install` vs `uvx` for package execution
- Configuring VS Code or other IDEs for MCP server integration
- Migrating from pip, pipx, or poetry to UV
- Troubleshooting UV-related issues

Skip this skill when:

- You need basic Python package installation only (standard pip documentation may suffice)
- Working with legacy Python 2.x projects

## Core Concepts

### 1. UV Commands Overview

UV provides several commands for different use cases:

| Command | Purpose | Example |
|---------|---------|---------|
| `uv pip install` | Install packages in current environment | `uv pip install requests` |
| `uv tool install` | Install CLI tools globally with isolation | `uv tool install black` |
| `uvx` | Execute packages in temporary environments | `uvx mcp-server-sqlite` |
| `uv venv` | Create virtual environments | `uv venv .venv` |
| `uv python install` | Install Python versions | `uv python install 3.12` |

### 2. Tool vs UVX Decision Tree

```text
Need to run a Python package?
|
├─ Use daily/frequently?
|  └─ YES → `uv tool install package`
|     Examples: black, pytest, flake8, mypy
|
├─ MCP server?
|  └─ YES → `uvx package` or `uvx --from path script.py`
|     Examples: mcp-server-sqlite, custom MCP servers
|
├─ Testing/one-off execution?
|  └─ YES → `uvx package`
|     Examples: testing new tools, version comparison
|
└─ Local development script?
   └─ YES → `uvx --from . script.py`
      Examples: project-specific scripts
```

### 3. MCP Server Execution Patterns

**Published Packages (No working directory needed):**

```json
{
  "servers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/db"]
    }
  }
}
```

**Local Development (Use --from flag):**

```json
{
  "servers": {
    "my-server": {
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

**Key insight**: `--from` flag IS the working directory reference for UVX.

### 4. Virtual Environment Management

UV works seamlessly with Python's built-in venv:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows Git Bash)
. .venv/Scripts/activate

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Linux/Mac)
source .venv/bin/activate

# Install packages with UV
uv pip install -r requirements.txt
```

## Common Workflows

### Development Tools Setup

```bash
# Install development tools once
uv tool install black
uv tool install flake8
uv tool install mypy
uv tool install pytest

# Use daily
black .
flake8 src/
mypy src/
pytest tests/
```

### MCP Server Usage

```bash
# Test published MCP servers
uvx mcp-server-sqlite --db-path test.db
uvx mcp-server-git --repository /path/to/repo

# Local MCP server development
uvx --from /path/to/project server.py --env config.env
```

### Project Initialization

```bash
# Create new project with UV
uv init my-project
cd my-project

# Add dependencies
uv add requests fastapi

# Run project
uv run python main.py
```

### Python Version Management

```bash
# List available Python versions
uv python list

# Install default Python version (3.14 in UV 0.9.6+)
uv python install

# Install specific Python version
uv python install 3.12
uv python install 3.13

# Use in project
uv python pin 3.12
```

**Note:** As of UV 0.9.6, Python 3.14 is the default version. If you need Python 3.13 or earlier, explicitly specify the version.

### Inline Script Dependencies (PEP 723)

UV supports defining dependencies directly in Python script comments:

```python
# /// script
# dependencies = [
#   "requests",
#   "pandas",
# ]
# ///

import requests
import pandas as pd

# Your code here
```

Run with automatic dependency installation:

```bash
# UV installs dependencies automatically
uv run script.py
```

**Benefits:**

- Self-contained single-file scripts
- No pyproject.toml needed
- Easy sharing and distribution
- Perfect for utilities and automation

See [Inline Script Metadata Reference](references/inline-script-metadata.md) for comprehensive examples including MCP servers, web applications, data processing, and CLI tools.

## Integration Patterns

### VS Code MCP Configuration

For `.vscode/mcp.json` or user settings:

```json
{
  "servers": {
    "published-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "${workspaceFolder}/db.sqlite"]
    },
    "local-dev": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "${workspaceFolder}",
        "src/server.py"
      ]
    }
  }
}
```

### Continue IDE Configuration

For `.continue/config.json`:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uvx",
          "args": ["mcp-server-fetch"]
        }
      }
    ]
  }
}
```

### GitHub Actions CI/CD

```yaml
- name: Setup UV
  uses: astral-sh/setup-uv@v1

- name: Install dependencies
  run: uv pip install -r requirements.txt

- name: Run tests
  run: uv run pytest
```

## Best Practices

### Tool Management

**DO:**

- Use `uv tool install` for development tools used frequently
- Use `uvx` for MCP servers (follows community patterns)
- Keep tools isolated in their own environments
- Regularly upgrade tools with `uv tool upgrade --all`

**DON'T:**

- Use global pip for CLI tools (causes dependency conflicts)
- Install MCP servers with `uv tool install` (against community patterns)
- Use `uvx` for daily development tools (unnecessary overhead)
- Mix pip and uv tool installations

### MCP Server Patterns

**DO:**

- Use UVX for all MCP server execution
- Use `--from` for local development
- Pin versions for production (`package@1.2.3`)
- Use environment variables for configuration

**DON'T:**

- Install MCP servers globally
- Mix working directory approaches
- Use `@latest` in production (unstable)
- Forget to specify absolute paths with `--from`

### Virtual Environments

**DO:**

- Use `python -m venv` for project environments
- Activate before installing packages
- Use `uv pip install` for faster package installation
- Document activation commands in README

**DON'T:**

- Install packages globally
- Mix venv and system Python packages
- Forget to activate before development
- Commit .venv directory to version control

## Performance Characteristics

UV's performance advantages:

- **10-100x faster** than pip for package operations
- **Parallel downloads** and installations
- **Global cache** with deduplication
- **Rust-powered** dependency resolution
- **Disk-efficient** storage with hard links

Typical operation times:

- Package installation: 100-1000x faster than pip
- Dependency resolution: Near-instant for cached packages
- Virtual environment creation: <1 second
- UVX first run: Package download time + execution
- UVX cached run: <1 second startup

## Troubleshooting

### Common Issues

**"spawn uvx ENOENT" Error:**

- UV/UVX not in PATH
- Solution: Reinstall UV or add to PATH manually

**Package Not Found:**

- Check package name on PyPI
- For local development, verify `--from` path
- Ensure `pyproject.toml` exists

**Permission Errors:**

- UV cache directory not writable
- Solution: Check permissions on `~/.cache/uv/`

**Version Conflicts:**

- Multiple Python versions
- Solution: Use `uv python pin` to set project version

See detailed troubleshooting in:

- [Installation & Setup Reference](references/installation-and-setup.md#troubleshooting)
- [Tool Management Reference](references/tool-management.md#troubleshooting)
- [MCP Integration Reference](references/mcp-integration.md#troubleshooting)

## Reference Documentation

This skill includes detailed reference documentation:

1. **[Recent Changes](references/recent-changes.md)** ⭐ NEW
   - Latest version information (0.9.7+)
   - Python 3.14 default and free-threading support
   - New features and breaking changes
   - Version compatibility matrix
   - Upgrade guidance

2. **[Installation & Setup](references/installation-and-setup.md)**
   - Installation methods (Windows, Linux, Mac)
   - Virtual environment setup
   - Platform-specific considerations

3. **[Tool Management](references/tool-management.md)**
   - UV tool install vs UVX comparison
   - Persistent vs temporary execution
   - Maintenance workflows

4. **[MCP Integration](references/mcp-integration.md)**
   - Published package patterns
   - Local development with --from
   - VS Code and IDE configuration

5. **[Python Environment](references/python-environment.md)**
   - Python version management
   - System paths (pyenv, uv, system)
   - Cross-platform compatibility

6. **[Inline Script Metadata](references/inline-script-metadata.md)**
   - PEP 723 inline dependencies in comments
   - Single-file scripts with automatic dependency management
   - MCP servers, web apps, and CLI tools
   - Best practices and troubleshooting

7. **[Examples](examples/README.md)**
   - Real-world GitHub configurations
   - Common workflow patterns
   - Anti-patterns to avoid

## External Resources

- **UV Official Documentation**: <https://docs.astral.sh/uv/>
- **UV GitHub Repository**: <https://github.com/astral-sh/uv>
- **MCP Official Documentation**: <https://modelcontextprotocol.io/>
- **MCP Servers Repository**: <https://github.com/modelcontextprotocol/servers>
- **VS Code MCP Support**: <https://code.visualstudio.com/docs/copilot/chat/mcp-servers>

## Migration Guides

### From pip

```bash
# Old way
pip install requests

# New way
uv pip install requests
```

### From pipx

```bash
# Old way
pipx install black

# New way
uv tool install black
```

### From poetry

```bash
# Old way
poetry add requests
poetry install

# New way
uv add requests
uv sync
```

## Summary

UV provides a unified, fast, and modern approach to Python package management. The key to effective UV usage is:

1. **Understand the tool landscape**: uv pip, uv tool, uvx each serve specific purposes
2. **Follow community patterns**: Use UVX for MCP servers, uv tool for development tools
3. **Leverage isolation**: Each tool gets its own environment preventing conflicts
4. **Use --from for local development**: Essential pattern for MCP server development
5. **Keep tools updated**: Regular maintenance prevents issues

By following these patterns and utilizing the reference documentation, you'll have a clean, efficient, and maintainable Python development environment.
