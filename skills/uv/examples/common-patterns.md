# Common Patterns

## Overview

Frequently used patterns and configurations for UV development.

## Development Tool Suite

```bash
# Install complete development suite
uv tool install black         # Code formatter
uv tool install flake8        # Linter
uv tool install mypy          # Type checker
uv tool install pytest        # Testing
uv tool install coverage      # Coverage
uv tool install pre-commit    # Git hooks
uv tool install commitizen    # Commit conventions
uv tool install cookiecutter  # Project templates

# Verify installations
uv tool list

# Weekly maintenance
uv tool upgrade --all
uv cache clean
```

## Pre-commit Integration

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: local
    hooks:
      - id: black
        name: Format with black
        entry: black
        language: system
        types: [python]

      - id: flake8
        name: Lint with flake8
        entry: flake8
        language: system
        types: [python]

      - id: mypy
        name: Type check with mypy
        entry: mypy
        language: system
        types: [python]
```

**Setup:**

```bash
# Install tools
uv tool install black flake8 mypy pre-commit

# Install hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

## Shell Configuration

**~/.bashrc or ~/.zshrc:**

```bash
# UV aliases
alias uv-update='uv tool upgrade --all'
alias uv-clean='uv cache clean'

# Development aliases
alias fmt='black'
alias lint='flake8'
alias type='mypy'
alias test='pytest'

# Project shortcuts
alias venv-activate='. .venv/Scripts/activate'  # or source .venv/bin/activate
alias venv-create='python -m venv .venv'
alias deps-install='uv pip install -r requirements.txt'
alias deps-freeze='uv pip freeze > requirements.txt'

# Ensure UV tools in PATH
export PATH="$HOME/.local/bin:$PATH"
```

## Related Documentation

- [Tool Management Reference](../references/tool-management.md)
- [Installation and Setup](../references/installation-and-setup.md)
- [Development Workflows](development-workflows.md)
