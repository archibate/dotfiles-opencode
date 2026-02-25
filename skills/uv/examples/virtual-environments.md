# Virtual Environment Workflows

## Overview

Virtual environment management patterns and best practices with UV.

## Basic Project Setup

```bash
# Create new project directory
mkdir my-project
cd my-project

# Create virtual environment
python -m venv .venv

# Activate (Windows Git Bash)
. .venv/Scripts/activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies with UV
uv pip install requests pandas numpy

# Freeze dependencies
uv pip freeze > requirements.txt

# Deactivate when done
deactivate
```

## Existing Project Migration

```bash
# Clone existing project
git clone https://github.com/user/project.git
cd project

# Create virtual environment
python -m venv .venv

# Activate
. .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate  # Linux/Mac

# Install from requirements with UV (much faster than pip)
uv pip install -r requirements.txt

# Verify installation
python -c "import requests; print('Success!')"
```

## Multi-Environment Project

```bash
# Development environment
python -m venv .venv-dev
. .venv-dev/Scripts/activate
uv pip install -r requirements-dev.txt
deactivate

# Production environment
python -m venv .venv-prod
. .venv-prod/Scripts/activate
uv pip install -r requirements.txt
deactivate

# Testing environment
python -m venv .venv-test
. .venv-test/Scripts/activate
uv pip install -r requirements.txt pytest coverage
deactivate

# Use specific environment
. .venv-test/Scripts/activate
pytest tests/
```

## Related Documentation

- [Python Environment Management Reference](../references/python-environment.md)
- [Installation and Setup](../references/installation-and-setup.md)
- [Tool Management](../references/tool-management.md)
