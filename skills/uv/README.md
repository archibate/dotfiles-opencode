# UV Skill for Claude Code

A comprehensive skill for working with UV, the extremely fast Python package and project manager. This skill provides guidance on Python environment management, MCP server integration, and modern Python development workflows.

**Stay Current:** This skill is aware of recent UV changes including Python 3.14 default, free-threaded Python support, and new features in UV 0.9.6+.

## Overview

UV is a Rust-powered Python package manager that replaces pip, pipx, poetry, pyenv, and more - delivering 10-100x faster performance. This skill helps Claude Code users:

- Set up and manage Python virtual environments
- Install and manage Python CLI tools efficiently
- Run MCP (Model Context Protocol) servers with UVX
- Configure VS Code and other IDEs for MCP integration
- Migrate from pip, pipx, or poetry to UV
- Stay current with latest UV features and version-specific changes
- Troubleshoot UV-related issues

## Features

- **Version-Aware Guidance** - Tracks recent UV changes (0.9.6+) including Python 3.14 default and free-threaded Python
- **Complete UV Command Reference** - Coverage of uv pip, uv tool, uvx, uv venv, and uv python
- **Inline Script Metadata (PEP 723)** - Single-file scripts with dependencies in comments
- **MCP Server Integration** - Detailed patterns for both published packages and local development
- **Cross-Platform Support** - Instructions for Windows, Linux, and macOS
- **Real-World Examples** - GitHub Actions, VS Code, Continue IDE configurations
- **Migration Guides** - Step-by-step migration from pip, pipx, and poetry
- **Performance Insights** - Understanding UV's 10-100x speed improvements
- **Troubleshooting** - Common issues and solutions

## Installation

### Install the Skill

Copy the skill to your Claude Code skills directory:

**Windows (Git Bash):**

```bash
cp -r . "$USERPROFILE/.claude/skills/uv"
```

**Linux/macOS:**

```bash
cp -r . ~/.claude/skills/uv
```

### Verify Installation

Ask Claude Code: "How do I install UV?" or "Help me set up a Python virtual environment with UV"

Claude should activate this skill and provide UV-specific guidance.

## Skill Structure

```text
uv-skill/
├── SKILL.md                          # Main skill file with core UV concepts
├── references/
│   ├── recent-changes.md             # Latest UV version changes (0.9.6+)
│   ├── installation-and-setup.md     # Installation and virtual environment setup
│   ├── tool-management.md            # UV tool install vs uvx comparison
│   ├── mcp-integration.md            # MCP server execution patterns
│   ├── python-environment.md         # Python version management
│   ├── inline-script-metadata.md     # PEP 723 inline dependencies
│   └── examples.md                   # Real-world configurations
├── docs/
│   └── guides/
│       └── testing-the-uv-skill.md   # Testing framework with test cases
├── README.md                         # This file
├── VERSION                           # Current version
└── LICENSE                           # MIT License
```

## When Claude Uses This Skill

Claude will automatically activate this skill when you:

- Ask about UV or UVX
- Need to install or manage Python packages
- Want to set up virtual environments
- Work with MCP servers
- Ask about Python tool management
- Need help migrating from pip, pipx, or poetry
- Troubleshoot UV-related errors

## Quick Start Examples

### Ask Claude

**Version & Recent Changes:**

- "What version of UV should I be using?"
- "What's new in UV 0.9.6?"
- "How do I use free-threaded Python with UV?"
- "What Python version will UV install by default?"

**Virtual Environments:**

- "How do I create a Python virtual environment with UV?"
- "Help me activate my venv and install packages using UV"

**Tool Management:**

- "Should I use uv tool install or uvx for black?"
- "How do I install development tools with UV?"

**MCP Servers:**

- "How do I run mcp-server-sqlite with uvx?"
- "Configure VS Code to use uvx for MCP servers"
- "How do I run a local MCP server with uvx --from?"

**Migration:**

- "Help me migrate from pip to UV"
- "Convert my pipx installations to UV tool"

**Troubleshooting:**

- "I'm getting spawn uvx ENOENT error"
- "UV can't find my package"

## What's Included

### Core Concepts (SKILL.md)

- UV command overview (uv pip, uv tool, uvx, uv venv, uv python)
- Tool vs UVX decision tree
- MCP server execution patterns
- Virtual environment management
- Common workflows and integration patterns
- Best practices and anti-patterns

### Reference Documentation

1. **Recent Changes** - Latest UV version information (0.9.6+), Python 3.14 default, free-threaded Python, new features
2. **Installation & Setup** - Cross-platform installation, virtual environment setup
3. **Tool Management** - Persistent vs temporary execution, maintenance workflows
4. **MCP Integration** - Published packages, local development, IDE configuration
5. **Python Environment** - Version management, cross-platform paths
6. **Inline Script Metadata** - PEP 723 dependencies in comments, single-file scripts
7. **Examples** - Real-world GitHub configurations, workflow patterns

## Recent Changes Awareness

This skill stays current with the latest UV developments. Claude Code will be aware of:

### UV 0.9.6+ Features

- **Python 3.14 Default** - UV now installs Python 3.14 by default (previously 3.13)
- **Free-Threaded Python** - Python 3.14+ without GIL for true parallel execution
- **Build --clear Flag** - Automatic cleanup of old build artifacts with `uv build --clear`

### UV 0.9.7 Features

- **Security Updates** - Improved tar/ZIP archive handling
- **Windows x86-32 Support** - Better compatibility on Windows systems

### Version-Aware Guidance

Claude Code will:

- Recommend upgrading if your UV version lacks needed features
- Provide version-specific instructions
- Warn about deprecated features
- Explain breaking changes and migration paths

Ask questions like:

- "What Python version will UV install by default?"
- "How do I use free-threaded Python with UV?"
- "Do I need to upgrade UV for Python 3.14?"
- "What's new in UV 0.9.6?"

## Key Concepts

### UV Commands

| Command | Purpose | Use Case |
|---------|---------|----------|
| `uv pip install` | Install packages | In virtual environments |
| `uv tool install` | Install CLI tools | Daily development tools |
| `uvx` | Temporary execution | MCP servers, testing |
| `uv venv` | Create venv | Project isolation |
| `uv python install` | Install Python | Version management |

### Tool vs UVX Decision

- **Use `uv tool install`** for: black, flake8, mypy, pytest (daily tools)
- **Use `uvx`** for: MCP servers, one-off executions, testing

### MCP Server Patterns

- **Published packages**: `uvx mcp-server-sqlite --db-path /path/to/db`
- **Local development**: `uvx --from /path/to/project server.py`

## Best Practices

### DO

- Use `python -m venv` for project virtual environments
- Use `uv tool install` for frequently used development tools
- Use `uvx` for all MCP server execution
- Use `--from` flag for local MCP server development
- Pin versions in production (`package@1.2.3`)

### DON'T

- Install packages globally without virtual environments
- Mix pip and uv tool installations
- Install MCP servers with `uv tool install`
- Use `uvx` for daily development tools
- Use `@latest` in production

## Performance

UV delivers exceptional performance:

- **10-100x faster** than pip for package operations
- **Parallel downloads** and installations
- **Global cache** with deduplication
- **Rust-powered** dependency resolution
- **Sub-second** virtual environment creation

## Troubleshooting

Common issues covered:

- "spawn uvx ENOENT" errors (PATH issues)
- Package not found (PyPI vs local)
- Permission errors (cache directory)
- Version conflicts (Python versions)

See detailed troubleshooting in reference documentation.

## Development

### Testing the Skill Locally

1. Copy skill to Claude skills directory
2. Restart Claude Code (if needed)
3. Ask UV-related questions
4. Verify Claude activates the skill
5. Check responses match documentation

### Updating the Skill

1. Edit SKILL.md or reference files
2. Test changes locally
3. Update VERSION file
4. Commit and push changes

## Version History

- **0.1.0** - Initial release
  - Complete UV command reference
  - Version-aware guidance for UV 0.9.6+ features
  - Python 3.14 default version documentation
  - Free-threaded Python support (PEP 703)
  - New `uv build --clear` flag documentation
  - Security updates awareness (tar/ZIP handling)
  - MCP server integration patterns
  - Cross-platform installation guides
  - Migration guides from pip/pipx/poetry
  - Real-world examples and configurations
  - Enhanced testing guide with version-specific test cases
  - Comprehensive version compatibility matrix

## Contributing

Contributions welcome! Areas for improvement:

- Additional real-world examples
- More troubleshooting scenarios
- Integration patterns for other IDEs
- Performance benchmarks
- Platform-specific optimizations

## Resources

### Official Documentation

- [UV Official Docs](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [VS Code MCP Support](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

### Claude Code

- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Skill Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

## License

MIT License - See LICENSE file

## Support

For issues or questions:

- Check the reference documentation in `references/`
- Ask Claude Code using this skill
- Review troubleshooting sections
- Consult official UV documentation

## Acknowledgments

This skill is based on:

- Official UV documentation and community practices
- Real-world MCP server integration patterns
- Claude Code skill best practices
- Community feedback and testing
