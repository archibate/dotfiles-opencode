---
name: writing-python
description: Develop Python projects with uv (PEP 723 inline metadata, venv management, script execution). Use when user mentions uv, creates Python scripts, or needs Python environment setup.
---

# Python Development with UV

Modern Python development using `uv` for package management, PEP 723 for single-file scripts, and best-in-class tooling.

## Quick Start

### Single-File Scripts (Default)

By default, create self-contained scripts using PEP 723 format:

```python
#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "typer",
#     "rich",
# ]
# ///
"""
Script description and usage examples.

Usage:
    uv run python3 script.py --help
    uv run python3 script.py --option value
"""

import sys
# ... rest of script
```

**Run with**: `uv run python3 script.py`

### Multi-File Projects

For larger projects requiring multiple files:

```bash
# Pin Python version
uv python pin 3.12

# Create virtual environment
uv venv --python 3.12

# Activate environment
source .venv/bin/activate

# Add dependencies
uv add package-name

# Run script
uv run python script.py
```

## Development Tools

### Testing, Linting, Type Checking

All tooling configuration is centralized in `/tests/pyproject.toml`.

**Run from `/tests` directory:**

```bash
cd tests

# Run tests
uv run pytest
uv run pytest -v  # verbose

# Type checking
uv run pyright
uv run pyright --stats

# Linting & formatting
uv run ruff check ../.opencode/skill
uv run ruff check --fix ../.opencode/skill
uv run ruff format ../.opencode/skill
```

**Tool choices:**

- **Ruff** - Linter/formatter (replaces Black, isort, Flake8)
- **Pyright** - Type checker (replaces MyPy)
- **Pytest** - Test runner

For detailed usage, see:

- `references/ruff.md` - Linting and formatting
- `references/pyright.md` - Static type checking
- `references/pytest.md` - Testing framework

## Script Development Workflow

### Start Small - Build Incrementally

1. **Basic structure** - Create script with `--help` flag
2. **Test immediately** - Run with `uv run python3 script.py --help`
3. **Add `--dry-run`** - Show what would happen without executing
4. **Test again** - Verify dry-run output
5. **Add `--verbose`** - Detailed output for debugging
6. **Test again** - Verify verbose mode
7. **Continue incrementally** - Add features one at a time, testing each

### Shebang Format

```python
#!/usr/bin/env uv run python3
```

### PEP 723 Dependencies

```python
# /// script
# dependencies = [
#     "typer",      # Modern CLI framework
#     "rich",       # Beautiful terminal output
#     "httpx",      # Modern HTTP client
# ]
# ///
```

**Minimize dependencies** - Try using stdlib first.

## UV Commands Reference

### Package Management

```bash
uv add <package>           # Add package to pyproject.toml
uv remove <package>        # Remove package
uv sync                    # Install/sync dependencies
uv lock                    # Create/update lock file
```

### Python Version Management

```bash
uv python install <version>  # Install Python version
uv python list               # List installed versions
uv python pin <version>      # Set project Python version
```

### Running Scripts

```bash
uv run python script.py      # Run with project environment
uvx <tool>                   # Run tool in isolated environment
uv tool install <package>    # Install global tool
```

## Preferred Libraries

### Core Utilities

- **uv** - Package manager (never use pip/python3 directly)
- **typer** - Modern CLI framework (built on click)
- **rich** - Beautiful terminal output
- **python-dotenv** - Environment variables (or Pydantic-Settings)

### Development

- **pytest** - Testing framework
- **ruff** - Fast linting and formatting
- **pyright** - Static type checking

### When Needed

- **httpx** - Modern HTTP client (replaces requests)
- **Pydantic-Settings** - Type-safe configuration with validation
- **Polars** - Fast DataFrame library (pandas alternative)
- **DuckDB** - Embedded analytical database
- **Loguru** - Simple, powerful logging

## Test-Driven Development

### TDD Cycle

1. **Red** - Write failing test for new functionality
2. **Green** - Write minimal code to pass test
3. **Refactor** - Improve code while keeping tests green

### When to Use TDD

**General approach**: Code directly as you see fit.

**Use TDD when**: Facing issues or building complex components.

### Development Sequence (When Using TDD)

1. **Stubs** - Define basic structure and interfaces
2. **Pseudocode** - Plan detailed logic within stubs
3. **Data Layer** - Implement data persistence and management
4. **Business Logic** - Implement core application rules
5. **CLI/Frontend** - Implement user interaction

## Test Structure

See `references/pytest.md` for comprehensive testing guide.

### Directory Structure

```
.opencode/skill/<skill>/
├── SKILL.md
└── scripts/
    ├── <script>.py
    └── tests/
        └── test_<script>.py
```

### Helper Function Pattern

```python
from pathlib import Path
import subprocess

SCRIPT_PATH = Path(__file__).parent.parent / "script.py"

def run_script(*args, env=None):
    """Execute script with uv run."""
    cmd = ["uv", "run", str(SCRIPT_PATH)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.stdout, result.stderr, result.returncode
```

### Test Class Organization

```python
class TestVersion:
    """Test --version flag."""

    def test_version_flag(self):
        """--version should output version and exit with 0."""
        stdout, stderr, code = run_script("--version")
        assert code == 0
        assert "version" in stdout.lower()
```

### Exit Code Standards

| Code | Meaning                          |
| ---- | -------------------------------- |
| 0    | Success (version, help, dry-run) |
| 1    | Runtime/API error                |
| 2    | Validation error                 |
| 130  | Keyboard interrupt               |

## Type Checking

See `references/pyright.md` for comprehensive type checking guide.

### Basic Type Hints

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def find_user(id: int) -> str | None:
    return None

def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

### Docstrings

Use structured docstrings with Args, Returns, and Raises sections:

```python
def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Calculate the total cost of items including tax.

    Args:
        items: List of item dictionaries with 'price' keys
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)

    Returns:
        Total cost including tax

    Raises:
        ValueError: If items is empty or tax_rate is negative
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item["price"] for item in items)
    return subtotal * (1 + tax_rate)
```

## Best Practices

1. **Use uv exclusively** - Never run `python3` or `pip` directly
2. **Start with PEP 723** - Single-file scripts by default
3. **Minimize dependencies** - Try stdlib first
4. **Test incrementally** - Build and test feature by feature
5. **Use type hints** - Catch errors early with pyright
6. **Format with ruff** - Consistent code style
7. **Follow exit codes** - 0 for success, 1 for runtime errors, 2 for validation

## Common Pitfalls

### Mutable Default Arguments

Never use mutable objects (lists, dicts) as default argument values:

```python
# BAD - The list persists across calls!
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] - Unexpected!

# GOOD - Use None and create inside function
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Bare Except Clauses

Never use bare `except:` - always catch specific exceptions:

```python
# BAD - Catches everything including KeyboardInterrupt
try:
    do_something()
except:
    pass

# GOOD - Catch specific exceptions
try:
    do_something()
except (ValueError, TypeError) as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Comparing with None

Use `is` / `is not` for None comparisons:

```python
# BAD
if value == None:
    ...

# GOOD
if value is None:
    ...
```

## Security

### Environment Variables

Store secrets in `.env` files, never in code:

```python
# Load from .env file
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    print("Error: API_KEY not set", file=sys.stderr)
    sys.exit(1)
```

### Required Practices

- **Never commit secrets** - Add `.env` to `.gitignore`
- **Never log secrets** - Don't print API keys, passwords, or tokens
- **Never hardcode** - Use environment variables for all credentials
- **Validate early** - Check for required env vars at startup

### .gitignore Entry

```gitignore
# Environment variables
.env
.env.local
.env.*.local
```

## Bundled Resources

- `references/ruff.md` - Linting and formatting guide
- `references/pyright.md` - Type checking guide
- `references/pytest.md` - Testing framework guide
