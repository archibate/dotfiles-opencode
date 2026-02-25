# UV MCP Server Integration Reference

## Overview

This reference covers using UVX for Model Context Protocol (MCP) server execution, including published package patterns, local development workflows, and IDE integration strategies.

## Core Concept: Working Directory with --from

### Why Most Examples Don't Show Working Directories

Most MCP server examples use **published PyPI packages** that don't require working directory references:

```json
{
  "servers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.db"]
    }
  }
}
```

**Why no working directory?**

- `mcp-server-sqlite` is published on PyPI
- UVX automatically downloads and caches the package
- Creates isolated temporary environment for execution
- No local project files needed

**Key Insight**: For local development, `--from` flag IS the working directory reference.

## Published Packages vs Local Development

### Published Packages (No Working Directory)

Use this pattern for packages available on PyPI:

```json
{
  "servers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    },
    "aws-core": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/db.sqlite"]
    }
  }
}
```

**How it works:**

1. UVX checks PyPI for the package
2. Downloads package + dependencies to isolated cache
3. Creates temporary environment
4. Runs from cache - no local files required

**Benefits:**

- No working directory configuration needed
- Automatic dependency management
- Version pinning available (`package@version`)
- Consistent across machines

### Local Development (Use --from Flag)

Use this pattern for developing your own MCP servers:

```json
{
  "servers": {
    "my-local-server": {
      "command": "uvx",
      "args": [
        "--from", "/absolute/path/to/project",
        "server_script.py",
        "--arg1", "value1"
      ]
    }
  }
}
```

**How it works:**

1. UVX looks in specified directory for `pyproject.toml`
2. Creates isolated environment with project dependencies
3. Runs local script with project context
4. **`--from` flag IS the working directory reference**

**Benefits:**

- Immediate code changes (no reinstall)
- Access to local project dependencies
- Full development workflow support
- Easy debugging

## Command Patterns

### Published Package Patterns

```bash
# Basic execution
uvx mcp-server-sqlite --db-path /path/to/db

# Specific version
uvx mcp-server-git@1.0.0 --repository /path/to/repo

# Latest version (auto-update)
uvx awslabs.core-mcp-server@latest

# With package-specific arguments
uvx mcp-server-fetch --user-agent "MyApp/1.0"
```

### Local Development Patterns

```bash
# Execute from absolute path
uvx --from /d/mcp/my-server server.py

# Execute from current directory
uvx --from . main.py

# With configuration file
uvx --from /project server.py --env config.env

# With multiple arguments
uvx --from /project server.py --db /path/to/db --port 8080
```

### Package Execution Matrix

| Pattern | Use Case | Example |
|---------|----------|---------|
| `uvx package` | Published package | `uvx mcp-server-sqlite` |
| `uvx package@version` | Specific version | `uvx mcp-server-git@1.0.0` |
| `uvx package@latest` | Auto-update | `uvx awslabs.core@latest` |
| `uvx --from path script.py` | Local development | `uvx --from . server.py` |

## IDE Integration

### VS Code Configuration

#### Location Options

**User Settings** (Global):

- Windows: `%APPDATA%\Code\User\globalStorage\ms-vscode.vscode-mcp\settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/ms-vscode.vscode-mcp/settings.json`
- Linux: `~/.config/Code/User/globalStorage/ms-vscode.vscode-mcp/settings.json`

**Workspace Settings** (Project-specific):

```text
.vscode/mcp.json
```

#### Published Package Example

```json
{
  "mcpServers": {
    "sqlite": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "${workspaceFolder}/database.db"]
    },
    "git": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "${workspaceFolder}"]
    },
    "fetch": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

#### Local Development Example

```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "${workspaceFolder}",
        "src/server.py",
        "--config", "${workspaceFolder}/config.json"
      ]
    },
    "dev-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "d:/mcp/projects/my-mcp-server",
        "main.py",
        "--debug"
      ]
    }
  }
}
```

#### Environment Variables

```json
{
  "mcpServers": {
    "aws-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "github-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

### Continue IDE Configuration

Location: `.continue/config.json`

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uvx",
          "args": ["mcp-server-sqlite", "--db-path", "/Users/NAME/test.db"]
        }
      },
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

### Other IDE Patterns

**Generic MCP Client Configuration:**

```json
{
  "servers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name", "--arg", "value"],
      "env": {
        "VAR": "value"
      }
    }
  }
}
```

## Real-World Examples

### Official MCP Servers Repository

From: `modelcontextprotocol/servers`

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
    },
    "filesystem": {
      "command": "uvx",
      "args": [
        "mcp-server-filesystem",
        "/allowed/path1",
        "/allowed/path2"
      ]
    }
  }
}
```

### AWS MCP Servers

From: `awslabs/mcp`

```json
{
  "mcpServers": {
    "core": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "lambda": {
      "command": "uvx",
      "args": ["awslabs.lambda-mcp-server@latest"],
      "env": {
        "AWS_REGION": "us-east-1"
      }
    },
    "nova-canvas": {
      "command": "uvx",
      "args": ["awslabs.nova-canvas-mcp-server@latest"]
    }
  }
}
```

### Database Servers

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.sqlite"]
    },
    "postgres": {
      "command": "uvx",
      "args": [
        "mcp-server-postgres",
        "postgresql://user:pass@localhost/dbname"
      ]
    },
    "mysql": {
      "command": "uvx",
      "args": [
        "mcp-server-mysql",
        "--host", "localhost",
        "--database", "mydb"
      ]
    }
  }
}
```

### Cloud Service Integrations

```json
{
  "mcpServers": {
    "aws-bedrock": {
      "command": "uvx",
      "args": ["awslabs.bedrock-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default"
      }
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "slack": {
      "command": "uvx",
      "args": ["mcp-server-slack"],
      "env": {
        "SLACK_TOKEN": "${env:SLACK_TOKEN}"
      }
    }
  }
}
```

## Development Workflows

### Local MCP Server Development

**Project Structure:**

```text
my-mcp-server/
├── pyproject.toml
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── server.py
│       └── handlers.py
├── tests/
│   └── test_server.py
├── config.env
└── README.md
```

**pyproject.toml:**

```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
dependencies = [
    "mcp>=0.1.0",
    "fastapi>=0.100.0"
]

[project.scripts]
my-server = "my_server.server:main"
```

**VS Code Configuration:**

```json
{
  "mcpServers": {
    "my-server-dev": {
      "command": "uvx",
      "args": [
        "--from", "${workspaceFolder}",
        "src/my_server/server.py",
        "--env", "${workspaceFolder}/config.env"
      ]
    }
  }
}
```

**Benefits:**

- Code changes immediately reflected (no reinstall)
- Full debugger support
- Access to local dependencies
- Fast iteration cycle

### Testing Different Versions

```bash
# Test development version
uvx --from . server.py

# Test published version
uvx my-mcp-server@0.1.0

# Test latest PyPI version
uvx my-mcp-server@latest

# Compare behaviors
diff <(uvx --from . server.py --test) <(uvx my-mcp-server@latest --test)
```

### Multi-Server Development

```json
{
  "mcpServers": {
    "server-stable": {
      "command": "uvx",
      "args": ["my-mcp-server@1.0.0"]
    },
    "server-dev": {
      "command": "uvx",
      "args": ["--from", "${workspaceFolder}/servers/dev", "server.py"]
    },
    "server-experimental": {
      "command": "uvx",
      "args": ["--from", "${workspaceFolder}/servers/experimental", "server.py"]
    }
  }
}
```

## Benefits of UVX for MCP Servers

### 1. Automatic Dependency Management

- Downloads required packages automatically
- Handles version conflicts in isolation
- No global package pollution
- Consistent environments

### 2. Development-Friendly

- Code changes immediately available (with `--from`)
- No reinstallation needed
- Isolated environments prevent conflicts
- Easy debugging

### 3. Cross-Platform Consistency

- Works identically on Windows, macOS, Linux
- Handles path differences automatically
- Consistent behavior across environments
- Same configuration format

### 4. Performance

- 10-100x faster than pip for package operations
- Intelligent caching and parallel downloads
- Optimized dependency resolution
- Minimal startup overhead

### 5. Version Management

- Easy version pinning (`package@version`)
- Auto-update capability (`@latest`)
- Test multiple versions easily
- No version conflicts

## Troubleshooting

### "spawn uvx ENOENT" Error

**Symptoms:**

- IDE cannot find uvx command
- Server fails to start

**Solutions:**

```bash
# Verify UVX installation
uvx --version

# Check PATH includes UV binary
echo $PATH | grep uv  # Linux/Mac
echo %PATH% | findstr uv  # Windows

# Add to PATH if missing
export PATH="$HOME/.local/bin:$PATH"  # Linux/Mac

# Windows: Add to system PATH
# %LOCALAPPDATA%\Programs\uv
```

**IDE-Specific:**

For VS Code:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "/full/path/to/uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/db"]
    }
  }
}
```

### Package Not Found

**Symptoms:**

- "Package not found on PyPI"
- 404 errors

**Solutions:**

```bash
# Verify package name on PyPI
uvx --help mcp-server-name

# Check package exists
curl https://pypi.org/pypi/mcp-server-name/json

# For local development, ensure pyproject.toml exists
ls -la /path/to/project/pyproject.toml

# Verify --from path is correct
uvx --from /absolute/path/to/project server.py
```

### Permission Errors

**Symptoms:**

- Cannot write to cache
- Access denied errors

**Solutions:**

```bash
# Check UV cache permissions
ls -la ~/.cache/uv/  # Linux/Mac
dir %LOCALAPPDATA%\uv\cache  # Windows

# Fix permissions
chmod -R u+w ~/.cache/uv/  # Linux/Mac

# Clear and rebuild cache
uv cache clean
uvx package-name
```

### Connection/Startup Failures

**Symptoms:**

- Server starts but doesn't respond
- Timeout errors in IDE

**Solutions:**

```bash
# Test server manually
uvx mcp-server-sqlite --db-path test.db

# Check server logs (if available)
uvx package-name --verbose

# Verify arguments are correct
# Check for typos in paths, flags

# Test with minimal configuration
{
  "command": "uvx",
  "args": ["package-name"]  # No extra args
}
```

### Environment Variable Issues

**Symptoms:**

- Server can't access credentials
- Configuration not loaded

**Solutions:**

```json
{
  "mcpServers": {
    "server": {
      "command": "uvx",
      "args": ["package-name"],
      "env": {
        "API_KEY": "actual-value-not-reference",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}

# Or use IDE variable substitution
{
  "env": {
    "API_KEY": "${env:MY_API_KEY}"  # References system env var
  }
}
```

### Debugging Commands

```bash
# Verify UVX works
uvx --version

# Test package availability
uvx --help mcp-server-name

# Check local project
ls -la /path/to/project/pyproject.toml
cat /path/to/project/pyproject.toml

# Clear cache
uv cache clean

# Test with verbose output
uvx --verbose package-name

# Check UV configuration
uv --version
```

## Performance Considerations

### Published Packages

**First Run:**

- Downloads package from PyPI
- Installs dependencies
- Creates cached environment
- Typical time: 5-15 seconds

**Subsequent Runs:**

- Uses cached environment
- No downloads needed
- Typical startup: <1 second

**Using @latest:**

- Checks for updates each run
- Downloads if new version available
- Use with caution in production

### Local Development

**Startup Performance:**

- Faster than published (no download)
- Creates environment from local pyproject.toml
- Typical startup: 1-3 seconds first run
- Cached runs: <1 second

**Code Changes:**

- Immediate reflection (no cache invalidation needed)
- No reinstall required
- Perfect for development iteration

## Best Practices

### 1. Use Published Packages for Production

```json
{
  "production-server": {
    "command": "uvx",
    "args": ["mcp-server-name"]  // Not @latest for stability
  }
}
```

**Why:**

- Stable, tested versions
- Predictable behavior
- No unexpected changes

### 2. Use --from for Development

```json
{
  "dev-server": {
    "command": "uvx",
    "args": ["--from", "/absolute/path", "server.py"]
  }
}
```

**Why:**

- Immediate code changes
- Easy debugging
- Fast iteration

### 3. Pin Versions for Reliability

```json
{
  "stable-server": {
    "command": "uvx",
    "args": ["awslabs.core-mcp-server@1.2.3"]  // Specific version
  }
}
```

**Why:**

- Consistent behavior
- No breaking changes
- Easier troubleshooting

### 4. Use Environment Variables for Config

```json
{
  "configurable-server": {
    "command": "uvx",
    "args": ["server-name"],
    "env": {
      "CONFIG_PATH": "/path/to/config",
      "LOG_LEVEL": "INFO",
      "API_KEY": "${env:API_KEY}"
    }
  }
}
```

**Why:**

- Secure credential management
- Easy configuration changes
- No hardcoded secrets

### 5. Use Absolute Paths

```json
{
  "my-server": {
    "command": "uvx",
    "args": [
      "--from", "/d/mcp/projects/server",  // Absolute
      "server.py",
      "--db", "/d/data/database.db"  // Absolute
    ]
  }
}
```

**Why:**

- No path resolution issues
- Works from any working directory
- Consistent across machines

## Migration from Other Tools

### From uv run

```bash
# Old way
uv run python server.py

# New way
uvx --from . server.py
```

### From pip + python

```bash
# Old way
pip install package && python -m package

# New way
uvx package
```

### From uv tool install

```bash
# Old way (not recommended for MCP servers)
uv tool install mcp-server-sqlite
mcp-server-sqlite --db-path /path/to/db

# New way (recommended)
uvx mcp-server-sqlite --db-path /path/to/db
```

## Summary

UVX provides the optimal way to run MCP servers:

- **Published packages** work without working directory configuration
- **Local development** uses `--from` for project context
- **Isolated environments** prevent dependency conflicts
- **Automatic dependency management** simplifies deployment
- **Cross-platform consistency** ensures reliable operation
- **Fast performance** with intelligent caching

The absence of working directory references in most GitHub examples is **by design** - UVX handles package resolution and environment creation automatically for published packages, only requiring explicit paths (`--from`) for local development scenarios.
