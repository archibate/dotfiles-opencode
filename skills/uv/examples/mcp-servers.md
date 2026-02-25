# MCP Server Examples

## Overview

Complete MCP server configuration examples for various platforms and use cases.

## Published MCP Servers

### Official MCP Servers Repository

From: `github.com/modelcontextprotocol/servers`

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.db"]
    },
    "filesystem": {
      "command": "uvx",
      "args": [
        "mcp-server-filesystem",
        "/allowed/path1",
        "/allowed/path2"
      ]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

### AWS MCP Servers

From: `github.com/awslabs/mcp`

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
    "bedrock": {
      "command": "uvx",
      "args": ["awslabs.bedrock-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default"
      }
    },
    "nova-canvas": {
      "command": "uvx",
      "args": ["awslabs.nova-canvas-mcp-server@latest"]
    }
  }
}
```

### VS Code MCP Documentation

From: `code.visualstudio.com/docs/copilot/chat/mcp-servers`

```json
{
  "servers": {
    "fetch": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

### Continue IDE

From: Continue IDE Documentation

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

## Local MCP Server Development

### Basic Local Development

```json
{
  "mcpServers": {
    "sql-plugins": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "d:/mcp/my.python/sqlplugins",
        "mcp_server.py",
        "--env", "d:/mcp/my.python/sqlplugins/hr2.env"
      ]
    }
  }
}
```

### Development with Multiple Configurations

```json
{
  "mcpServers": {
    "dev-server": {
      "command": "uvx",
      "args": [
        "--from", "${workspaceFolder}",
        "src/server.py",
        "--debug"
      ]
    },
    "test-server": {
      "command": "uvx",
      "args": [
        "--from", "${workspaceFolder}",
        "src/server.py",
        "--config", "test_config.json"
      ]
    },
    "prod-server": {
      "command": "uvx",
      "args": ["my-mcp-server@1.0.0"]
    }
  }
}
```

## Related Documentation

- [MCP Integration Reference](../references/mcp-integration.md)
- [Inline Script Metadata](../references/inline-script-metadata.md)
- [Installation and Setup](../references/installation-and-setup.md)
