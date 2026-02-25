# UV Real-World Examples

## Overview

This directory contains real-world examples, common patterns, and anti-patterns for UV usage across different scenarios.

## Example Categories

### [Inline Script Metadata](inline-scripts.md)

PEP 723 inline script metadata examples with UV. Learn how to create self-contained Python scripts with embedded dependencies.

**Topics:**

- Basic inline dependencies
- Python version requirements
- MCP server with inline dependencies
- Data processing scripts
- When to use inline metadata

### [MCP Server Examples](mcp-servers.md)

Complete MCP server configuration examples for various platforms and use cases.

**Topics:**

- Published MCP servers (official, AWS, etc.)
- VS Code and Continue IDE configurations
- Local development setup
- Multi-configuration development

### [Development Workflows](development-workflows.md)

Complete development tool setup and daily workflow patterns.

**Topics:**

- Python development environment setup
- Project-specific script execution
- Multi-version testing workflows

### [Virtual Environment Workflows](virtual-environments.md)

Virtual environment management patterns and best practices.

**Topics:**

- Basic project setup
- Existing project migration
- Multi-environment projects

### [CI/CD Examples](ci-cd.md)

Continuous integration and deployment configurations.

**Topics:**

- GitHub Actions workflows
- GitLab CI pipelines

### [Migration Examples](migrations.md)

Migration guides from other Python tools to UV.

**Topics:**

- From pip to UV
- From pipx to UV tool
- From poetry to UV

### [Common Patterns](common-patterns.md)

Frequently used patterns and configurations.

**Topics:**

- Development tool suite setup
- Pre-commit integration
- Shell configuration

### [Anti-Patterns](anti-patterns.md)

Common mistakes to avoid when using UV.

**Topics:**

- Global pip installs
- Installing MCP servers with uv tool
- Using uvx for daily tools
- Mixed tool management
- Forgetting virtual environments

### [Complete Workflow](complete-workflow.md)

End-to-end example of setting up a new Python project with UV.

**Topics:**

- Full project initialization
- Git setup
- Dependency management
- Testing and formatting
- Documentation

## How to Use These Examples

1. **Browse by topic** - Use the category links above to find relevant examples
2. **Copy and adapt** - All examples are designed to be copied and modified for your needs
3. **Follow patterns** - Use the "DO" examples and avoid the "DON'T" anti-patterns
4. **Refer to related docs** - Each example file links to relevant reference documentation

## Related Documentation

- [Installation and Setup](../references/installation-and-setup.md)
- [Tool Management](../references/tool-management.md)
- [Python Environment Management](../references/python-environment.md)
- [Inline Script Metadata](../references/inline-script-metadata.md)
- [MCP Integration](../references/mcp-integration.md)
