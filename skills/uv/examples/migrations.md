# Migration Examples

## Overview

Migration guides from other Python tools to UV.

## From pip to UV

**Before (pip):**

```bash
# Old workflow
pip install requests pandas numpy
pip freeze > requirements.txt

# Problems:
# - Slow installation
# - Dependency conflicts
# - No isolation
```

**After (UV):**

```bash
# New workflow
python -m venv .venv
. .venv/Scripts/activate
uv pip install requests pandas numpy
uv pip freeze > requirements.txt

# Benefits:
# - 10-100x faster
# - Better dependency resolution
# - Virtual environment isolation
```

## From pipx to UV tool

**Before (pipx):**

```bash
# Old tool management
pipx install black
pipx install flake8
pipx install pytest
pipx upgrade-all
```

**After (UV tool):**

```bash
# New tool management
uv tool install black
uv tool install flake8
uv tool install pytest
uv tool upgrade --all

# Migration:
pipx list --short > tools.txt
cat tools.txt | xargs -n1 uv tool install
```

## From poetry to UV

**Before (poetry):**

```bash
# Old project management
poetry new my-project
cd my-project
poetry add requests
poetry install
poetry run python script.py
```

**After (UV):**

```bash
# New project management
uv init my-project
cd my-project
uv add requests
uv sync
uv run python script.py

# Migration from existing poetry project:
poetry export -f requirements.txt -o requirements.txt
python -m venv .venv
. .venv/Scripts/activate
uv pip install -r requirements.txt
```

## Related Documentation

- [Installation and Setup Reference](../references/installation-and-setup.md)
- [Tool Management](../references/tool-management.md)
- [Python Environment Management](../references/python-environment.md)
