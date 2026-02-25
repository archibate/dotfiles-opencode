# Anti-Patterns to Avoid

## Overview

Common mistakes to avoid when using UV.

## Global pip Installs

**DON'T:**

```bash
# BAD: Global pip installs
pip install black flake8 mypy
# Problems:
# - Dependency conflicts
# - Pollutes global Python
# - Difficult to uninstall
# - Version conflicts with projects
```

**DO:**

```bash
# GOOD: UV tool installs
uv tool install black
uv tool install flake8
uv tool install mypy
# Benefits:
# - Isolated environments
# - No conflicts
# - Easy management
# - Clean uninstall
```

## Installing MCP Servers with uv tool

**DON'T:**

```bash
# BAD: Installing MCP servers persistently
uv tool install mcp-server-sqlite
# Problems:
# - Goes against community patterns
# - Less flexible for testing
# - Requires reinstall for updates
# - Not what docs recommend
```

**DO:**

```bash
# GOOD: Use uvx for MCP servers
uvx mcp-server-sqlite --db-path /path/to/db

# In VS Code config:
{
  "command": "uvx",
  "args": ["mcp-server-sqlite", "--db-path", "/path/to/db"]
}
# Benefits:
# - Follows community patterns
# - Easy version testing
# - Matches documentation
# - Immediate updates
```

## Using uvx for Daily Tools

**DON'T:**

```bash
# BAD: Using uvx for frequently used tools
uvx black my_file.py  # Every time
uvx flake8 .         # Every time
uvx pytest          # Every time
# Problems:
# - Unnecessary overhead
# - Slower execution
# - Cache management needed
# - Not optimal use case
```

**DO:**

```bash
# GOOD: Install tools with uv tool
uv tool install black flake8 pytest

# Then use directly
black my_file.py
flake8 .
pytest
# Benefits:
# - Instant execution
# - No overhead
# - Persistent installation
# - Optimal performance
```

## Mixed Tool Management

**DON'T:**

```bash
# BAD: Mixing pip and uv tool
pip install --user black
uv tool install flake8
pipx install pytest
# Problems:
# - Inconsistent management
# - Difficult to track
# - Potential conflicts
# - Hard to maintain
```

**DO:**

```bash
# GOOD: Use UV tool exclusively
uv tool install black
uv tool install flake8
uv tool install pytest
# Benefits:
# - Consistent management
# - Easy to track
# - No conflicts
# - Simple maintenance
```

## Forgetting Virtual Environments

**DON'T:**

```bash
# BAD: Installing packages globally
cd my-project
uv pip install requests  # Installs to global Python
# Problems:
# - Pollutes global environment
# - Version conflicts
# - Difficult to reproduce
# - No isolation
```

**DO:**

```bash
# GOOD: Always use virtual environments
cd my-project
python -m venv .venv
. .venv/Scripts/activate
uv pip install requests
# Benefits:
# - Project isolation
# - Clean environments
# - Easy reproduction
# - No global pollution
```

## Related Documentation

- [Tool Management Reference](../references/tool-management.md)
- [MCP Integration](../references/mcp-integration.md)
- [Python Environment Management](../references/python-environment.md)
