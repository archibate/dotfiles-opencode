# UV Tool Management Reference

## Overview

UV's tool management system provides isolated installation and execution of Python CLI applications. This reference covers `uv tool` commands, `uvx` execution patterns, and decision frameworks for choosing the right approach.

## Quick Decision Guide

| Scenario | Use This | Why |
|----------|----------|-----|
| Install black code formatter | `uv tool install black` | Use daily, want persistent |
| Test an MCP server | `uvx mcp-server-sqlite` | Temporary, testing |
| Run script from local project | `uvx --from . script.py` | One-off execution |
| Install development tools | `uv tool install pytest` | Regular use |
| Try different package versions | `uvx package@1.0.0` | Version testing |
| Install CLI utilities | `uv tool install httpie` | Frequent use |

## UV Tool Install - Persistent Installation

### Purpose

Installs Python applications globally in isolated environments, making their commands available system-wide while preventing dependency conflicts.

### Basic Commands

```bash
# Install tool from PyPI
uv tool install package-name

# Install specific version
uv tool install package-name==1.2.3

# Install from local project (editable)
uv tool install -e .

# Install from git repository
uv tool install git+https://github.com/user/repo.git

# Install with extras
uv tool install "package-name[extra1,extra2]"
```

### Management Operations

```bash
# List installed tools
uv tool list

# Show tool details
uv tool show package-name

# Upgrade a tool
uv tool upgrade package-name

# Upgrade all tools
uv tool upgrade --all

# Uninstall a tool
uv tool uninstall package-name

# Reinstall (force)
uv tool install package-name --force
```

### Best Use Cases

**Development Tools:**

```bash
uv tool install black      # Code formatter
uv tool install flake8     # Linter
uv tool install mypy       # Type checker
uv tool install pytest     # Testing framework
```

**CLI Utilities:**

```bash
uv tool install httpie         # HTTP client
uv tool install rich-cli       # Terminal formatting
uv tool install tldr           # Command help
uv tool install cookiecutter   # Project templates
```

**Configuration-Dependent Tools:**

```bash
uv tool install pre-commit     # Git hooks
uv tool install commitizen     # Commit conventions
```

### Installation Locations

**Windows:**

```text
C:\Users\{username}\AppData\Roaming\uv\tools\
├── black\
│   ├── pyvenv.cfg
│   ├── Scripts\black.exe
│   └── Lib\site-packages\
├── flake8\
│   └── ...
└── pytest\
    └── ...
```

**Linux/macOS:**

```text
~/.local/share/uv/tools/
├── black/
│   ├── pyvenv.cfg
│   ├── bin/black
│   └── lib/python3.x/site-packages/
├── flake8/
│   └── ...
└── pytest/
    └── ...
```

### How It Works

1. **Isolation**: Each tool gets its own virtual environment
2. **Persistence**: Tools remain installed across sessions
3. **PATH Integration**: Tool commands added to system PATH
4. **Fast Execution**: No setup time after installation
5. **Manual Updates**: Run `uv tool upgrade` to update

## UVX - Temporary Execution

### UVX Purpose

Executes Python packages in temporary isolated environments without permanent installation. Ideal for one-off executions, testing, and MCP servers.

### UVX Basic Commands

```bash
# Execute package from PyPI
uvx package-name

# Execute specific version
uvx package-name@1.2.3

# Execute with arguments
uvx package-name arg1 arg2 --flag

# Execute from local project
uvx --from /path/to/project script.py

# Execute latest version
uvx package-name@latest
```

### UVX Best Use Cases

**MCP Servers (Recommended Pattern):**

```bash
uvx mcp-server-sqlite --db-path /path/to/db
uvx mcp-server-git --repository /path/to/repo
uvx awslabs.core-mcp-server@latest
```

**One-Off Executions:**

```bash
uvx create-react-app my-app
uvx cookiecutter gh:user/template
```

**Version Testing:**

```bash
uvx black@22.0.0 --check .
uvx black@23.0.0 --check .
uvx black@24.0.0 --check .
```

**Local Development Scripts:**

```bash
uvx --from . manage.py migrate
uvx --from . scripts/data_processing.py
```

### UVX How It Works

1. **Temporary Environment**: Creates isolated environment per execution
2. **Caching**: Environments cached for faster subsequent runs
3. **No Persistence**: No permanent global installation
4. **Auto-Updates**: Use `@latest` for automatic version updates
5. **Setup Time**: First run downloads package (cached afterward)

## Detailed Comparison

### Feature Matrix

| Feature | `uv tool install` | `uvx` |
|---------|------------------|-------|
| **Purpose** | Install globally | Execute temporarily |
| **Persistence** | Permanent | Temporary (cached) |
| **Use Case** | Daily use tools | One-off execution |
| **Storage** | Persistent disk space | Temporary cache |
| **Updates** | Manual (`uv tool upgrade`) | Automatic (`@latest`) |
| **Execution Speed** | Instant (installed) | Setup time first run |
| **Version Switching** | Reinstall required | Easy (`@version`) |
| **Local Development** | Editable install (`-e`) | `--from` flag |

### Storage Comparison

**UV Tool Install:**

```text
~/.local/share/uv/tools/
├── black/              # ~15 MB
├── flake8/             # ~8 MB
├── mypy/               # ~25 MB
└── pytest/             # ~12 MB

Total: ~60 MB persistent storage
```

**UVX Execution:**

```text
~/.cache/uv/
├── cached-environments/
│   ├── black-23.1.0-a1b2c3/    # Temporary
│   ├── flake8-6.0.0-d4e5f6/    # Temporary
│   └── ...
└── downloaded-packages/
    └── ... # Shared package cache

Cache automatically managed by UV
```

## Real-World Workflows

### Development Environment Setup

```bash
# Install core development tools once
uv tool install black
uv tool install flake8
uv tool install mypy
uv tool install pytest
uv tool install coverage

# Use daily without setup time
black .
flake8 src/
mypy src/
pytest tests/
coverage run -m pytest
```

### MCP Server Configuration

**VS Code `.vscode/mcp.json`:**

```json
{
  "servers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/db"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    },
    "local-dev": {
      "command": "uvx",
      "args": [
        "--from", "/path/to/project",
        "server.py",
        "--config", "config.json"
      ]
    }
  }
}
```

### Local Development Workflow

```bash
# Develop a CLI tool
cd my-cli-project

# Install in development mode
uv tool install -e .

# Tool globally available during development
my-tool --help

# Make code changes...
# Changes immediately reflected (editable install)
my-tool --version  # Shows updated version
```

### Version Testing Workflow

```bash
# Test multiple versions without installing
uvx black@22.0.0 --check src/
uvx black@23.0.0 --check src/
uvx black@24.0.0 --check src/

# Find preferred version
uvx black@23.0.0 src/  # Works best

# Install preferred version permanently
uv tool install black==23.0.0
```

## Migration Patterns

### Wrong Global Pip Install

```bash
# DON'T DO THIS - causes conflicts
pip install black flake8 mypy

# Problems:
# - Dependency conflicts between tools
# - Difficult to uninstall cleanly
# - Pollutes global Python environment
# - Version conflicts with projects
```

### Right UV Tool Install

```bash
# DO THIS - isolated tools
uv tool install black
uv tool install flake8
uv tool install mypy

# Benefits:
# - Each tool in own environment
# - Clean uninstall: uv tool uninstall
# - No dependency conflicts
# - Fast 10-100x vs pip
```

### Wrong Installing MCP Servers Persistently

```bash
# NOT RECOMMENDED for MCP servers
uv tool install mcp-server-sqlite

# Problems:
# - Goes against community patterns
# - Less flexible for version testing
# - Requires reinstall for updates
# - Not what documentation recommends
```

### Right UVX for MCP Servers

```bash
# RECOMMENDED for MCP servers
uvx mcp-server-sqlite --db-path /path/to/db

# Or in VS Code config:
{
  "command": "uvx",
  "args": ["mcp-server-sqlite", "--db-path", "/path/to/db"]
}

# Benefits:
# - Follows established MCP patterns
# - Easy version testing with @version
# - Immediate code changes with --from
# - Matches GitHub examples
```

## Advanced Patterns

### Project-Specific Scripts

```bash
# Run management scripts without global install
uvx --from . scripts/setup_database.py
uvx --from . scripts/generate_docs.py
uvx --from . scripts/deploy.py

# Scripts run with project dependencies
# No need to install scripts globally
```

### Multi-Version Development

```bash
# Test tool against multiple Python versions
uv python install 3.10 3.11 3.12

# Test with each version
uv python pin 3.10
uvx --from . my_tool.py

uv python pin 3.11
uvx --from . my_tool.py

uv python pin 3.12
uvx --from . my_tool.py
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Install development tools
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv tool install black
    uv tool install flake8
    uv tool install pytest

- name: Run checks
  run: |
    black --check .
    flake8 .
    pytest tests/
```

## Maintenance Workflows

### Regular Maintenance

```bash
# Weekly maintenance routine
uv tool list                    # Check installed tools
uv tool upgrade --all           # Update all tools
uv cache clean                  # Clean old cache

# Check for outdated tools
uv tool list  # Shows current versions

# Remove unused tools
uv tool uninstall unused-tool

# Check tool details
uv tool show black              # See version, dependencies
```

### Cache Management

```bash
# UVX automatically manages cache
# Manual cleanup if needed

# Clean all caches
uv cache clean

# Check cache size
du -sh ~/.cache/uv/                    # Linux/Mac
dir /s "%LOCALAPPDATA%\uv\cache"       # Windows

# Selective cleanup (manual)
rm -rf ~/.cache/uv/cached-environments/old-env/
```

### Tool Documentation

Create `tools.txt` for team consistency:

```text
# Development tools
black==23.1.0
flake8==6.0.0
mypy==1.0.0
pytest==7.2.0
coverage==7.0.0

# Utilities
httpie==3.2.0
rich-cli==1.8.0
tldr==3.1.0
```

Install from file:

```bash
cat tools.txt | grep -v '^#' | xargs -n1 uv tool install
```

## Best Practice Summary

### Use UV Tool Install For

1. **Development tools**: black, flake8, mypy, pytest
2. **Daily utilities**: httpie, rich-cli, tldr
3. **Project generators**: cookiecutter, copier
4. **CLI applications**: youtube-dl, magic-wormhole
5. **Tools with config files**: pre-commit, commitizen

### Use UVX For

1. **MCP servers**: All MCP server execution
2. **Script testing**: Running unfamiliar packages
3. **Version testing**: Comparing tool versions
4. **Local scripts**: Project-specific executables
5. **One-off tasks**: Temporary package execution

### Anti-Patterns to Avoid

1. **Don't**: Use global pip for CLI tools
2. **Don't**: Install MCP servers with `uv tool install`
3. **Don't**: Use uvx for daily development tools
4. **Don't**: Mix pip and uv tool installations
5. **Don't**: Forget to upgrade tools regularly

## Troubleshooting

### Tool Command Not Found

**Symptoms:**

- Command not recognized after installation
- PATH doesn't include UV tools

**Solutions:**

```bash
# Check if tool is installed
uv tool list

# Check PATH (Linux/Mac)
echo $PATH | grep -o '[^:]*uv[^:]*'

# Check PATH (Windows)
echo %PATH% | findstr uv

# Add to PATH manually if needed
export PATH="$HOME/.local/bin:$PATH"  # Linux/Mac bashrc/zshrc
```

### Dependency Conflicts

**Symptoms:**

- Tool installation fails
- Version conflicts reported

**Solutions:**

```bash
# Tools are isolated, but if issues occur:
uv tool uninstall package-name
uv cache clean
uv tool install package-name

# Use specific version
uv tool install package-name==1.2.3

# Install with force
uv tool install package-name --force
```

### UVX Execution Errors

**Symptoms:**

- Package not found
- Local script fails with --from

**Solutions:**

```bash
# Verify package exists on PyPI
uvx --help package-name

# For local development, ensure pyproject.toml exists
ls -la /path/to/project/pyproject.toml

# Check --from path is absolute
uvx --from /absolute/path/to/project script.py

# Clear cache and retry
uv cache clean
uvx package-name
```

### Permission Errors

**Symptoms:**

- Cannot write to tool directory
- Installation fails with permission denied

**Solutions:**

```bash
# Check tool directory permissions
ls -la $(uv tool dir)

# Fix permissions (Linux/Mac)
chmod -R u+w ~/.local/share/uv/tools/

# Windows: Run as Administrator or check folder permissions
```

### Outdated Tools

**Symptoms:**

- Tools behave differently than expected
- New features missing

**Solutions:**

```bash
# Check installed versions
uv tool list

# Upgrade specific tool
uv tool upgrade package-name

# Upgrade all tools
uv tool upgrade --all

# Force reinstall latest
uv tool uninstall package-name
uv tool install package-name
```

## Performance Characteristics

### UV Tool Install Performance

**Installation Speed:**

- 10-100x faster than pip
- Parallel dependency resolution
- Cached package downloads

**Example:**

```bash
# pip
time pip install black
# ~15 seconds

# uv tool
time uv tool install black
# ~2 seconds (first install)
# <1 second (cached)
```

**Execution Speed:**

- Instant startup (already installed)
- No environment creation overhead
- Direct binary execution

### UVX Performance

**First Execution:**

- Package download time
- Environment creation (~2-5 seconds)
- Execution time

**Cached Execution:**

- Environment reused from cache
- Startup <1 second
- Near-instant for small packages

**Example:**

```bash
# First run
time uvx black --version
# ~5 seconds (download + setup)

# Second run
time uvx black --version
# <1 second (cached)
```

## Integration Patterns

### Shell Configuration

Add to `.bashrc`, `.zshrc`, or `.bash_profile`:

```bash
# Ensure UV tools in PATH
export PATH="$HOME/.local/bin:$PATH"

# Aliases for common tools
alias fmt="black"
alias lint="flake8"
alias type="mypy"
alias test="pytest"

# Quick UVX execution
alias uvrun="uvx"

# Tool maintenance
alias uv-update="uv tool upgrade --all"
alias uv-clean="uv cache clean"
```

### VS Code Integration

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,

  "python.formatting.blackPath": "black",
  "python.linting.flake8Path": "flake8",
  "python.linting.mypyPath": "mypy"
}
```

Tools installed with `uv tool install` are automatically available to VS Code.

### Pre-commit Integration

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: black
        name: black
        entry: black
        language: system
        types: [python]

      - id: flake8
        name: flake8
        entry: flake8
        language: system
        types: [python]
```

Install tools:

```bash
uv tool install black flake8
uv tool install pre-commit
pre-commit install
```

## Summary

UV tool management provides two complementary approaches:

1. **`uv tool install`** - Persistent, fast, isolated installations for daily-use tools
2. **`uvx`** - Temporary, flexible, cached execution for testing and MCP servers

Choose based on:

- **Frequency of use**: Daily → `uv tool install`; Occasional → `uvx`
- **Tool type**: Development tools → `uv tool install`; MCP servers → `uvx`
- **Version needs**: Stable → `uv tool install`; Testing → `uvx @version`
- **Community patterns**: Follow established patterns (MCP = uvx)

By following these patterns, you maintain a clean, efficient, and conflict-free tool management system.
