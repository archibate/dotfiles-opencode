# Development Tool Workflows

## Overview

Complete development tool setup and daily workflow patterns with UV.

## Python Development Environment

```bash
# One-time setup: Install development tools
uv tool install black
uv tool install flake8
uv tool install mypy
uv tool install pytest
uv tool install coverage

# Daily development workflow
# Format code
black .

# Lint code
flake8 src/

# Type check
mypy src/

# Run tests
pytest tests/

# Run with coverage
coverage run -m pytest
coverage report
```

## Project-Specific Script Execution

```bash
# Project structure:
# my-project/
# ├── scripts/
# │   ├── setup_database.py
# │   ├── generate_docs.py
# │   └── deploy.py
# └── pyproject.toml

# Run scripts without installing globally
uvx --from . scripts/setup_database.py
uvx --from . scripts/generate_docs.py --format html
uvx --from . scripts/deploy.py --environment production
```

## Multi-Version Testing

```bash
# Test code against multiple Python versions
uv python install 3.10 3.11 3.12

# Test with Python 3.10
uv python pin 3.10
uvx --from . tests/run_tests.py

# Test with Python 3.11
uv python pin 3.11
uvx --from . tests/run_tests.py

# Test with Python 3.12
uv python pin 3.12
uvx --from . tests/run_tests.py

# Compare results
diff <(uv run --python 3.10 tests/test.py) \
     <(uv run --python 3.12 tests/test.py)
```

## Related Documentation

- [Tool Management Reference](../references/tool-management.md)
- [Python Environment Management](../references/python-environment.md)
- [Installation and Setup](../references/installation-and-setup.md)
