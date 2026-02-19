# Pyright - Python Static Type Checker

Fast static type checker for Python. Catches type errors before runtime.

## Why Pyright Over MyPy

- **Speed**: 5-10x faster than MyPy (written in TypeScript/Node.js)
- **Modern**: Better support for recent Python features
- **IDE Integration**: Powers VS Code's Python extension
- **Zero Config**: Works out of the box with sensible defaults

## Core Commands

```bash
# Check all files
uv run pyright

# Check specific files
uv run pyright path/to/file.py

# Show statistics
uv run pyright --stats

# Watch mode (re-check on file changes)
uv run pyright --watch
```

## Type Checking Modes

Set in `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "basic"  # or "standard" or "strict"
```

- **basic**: Minimal type checking (recommended for most projects)
- **standard**: Moderate type checking (catches more issues)
- **strict**: Maximum type checking (requires extensive type annotations)

## Configuration

Located in `pyproject.toml`:

```toml
[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "basic"

include = [
    ".opencode/skill",
    ".agents/scripts",
]

exclude = [
    "**/__pycache__",
    "**/.venv",
    "**/node_modules",
]

# Downgrade specific diagnostics
reportAttributeAccessIssue = "warning"  # error -> warning
reportMissingImports = "none"           # Disable entirely
```

## Common Error Types

### Import Errors

```
ERROR: Import "requests" could not be resolved
```

**Cause**: Package not installed or not in virtual environment
**Fix**: Install package with `uv add requests`

### Type Mismatch

```
ERROR: Argument of type "str" cannot be assigned to parameter "x" of type "int"
```

**Cause**: Passing wrong type to function
**Fix**: Convert type or update type hints

### Attribute Access

```
WARNING: "error" is not a known attribute of module "urllib"
```

**Cause**: Missing import or incorrect attribute access
**Fix**: Import correct submodule (e.g., `urllib.error`)

### Optional Member Access

```
ERROR: "read" is not a known attribute of "None"
```

**Cause**: Accessing attribute on potentially None value
**Fix**: Add None check before access

## Exit Codes

- `0` - No errors found
- `1` - Errors found

## Output Interpretation

```bash
# Example output
path/to/file.py:10:5 - error: "str" is not assignable to "int" (reportArgumentType)
path/to/file.py:15:8 - warning: Import "requests" could not be resolved (reportMissingImports)
```

Format: `file:line:column - level: message (ruleCode)`

## Diagnostic Rules

Common diagnostic rules:

- `reportMissingImports` - Unresolved imports
- `reportArgumentType` - Type mismatch in function arguments
- `reportAttributeAccessIssue` - Invalid attribute access
- `reportOptionalMemberAccess` - Accessing members on Optional types
- `reportGeneralTypeIssues` - General type inconsistencies

## Suppressing Errors

### Inline Suppression

```python
# pyright: ignore[reportArgumentType]
result = function("string")  # Expects int

# Or suppress all errors on line
result = function("string")  # pyright: ignore
```

### File-Level Suppression

```python
# pyright: reportMissingImports=false
import some_untyped_package
```

### Configuration Suppression

```toml
[tool.pyright]
reportMissingImports = "none"
reportAttributeAccessIssue = "warning"
```

## Integration with Tests

Run from `/tests` directory:

```bash
cd tests
uv run pyright
uv run pyright --stats
```

## Type Hints Quick Reference

```python
# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}"

# Optional types
from typing import Optional
def find_user(id: int) -> Optional[str]:
    return None

# Lists, dicts
from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Modern syntax (Python 3.10+)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

## Best Practices

1. **Start with basic mode** - Gradually increase strictness
2. **Fix errors before warnings** - Prioritize actual type errors
3. **Use type hints incrementally** - Don't annotate everything at once
4. **Exclude generated code** - Add to exclude list in config
5. **Run in CI/CD** - Catch type errors before deployment

## Common Patterns

### Handling PEP 723 Scripts

Scripts with inline dependencies may show import errors (expected):

```toml
[tool.pyright]
reportMissingImports = "warning"  # Downgrade to warning
```

### Checking Specific Directories

```toml
[tool.pyright]
include = [
    "../.opencode/skill/**/scripts/*.py",  # Only check scripts
]
```

### Excluding Virtual Environments

```toml
[tool.pyright]
exclude = [
    "**/.venv/**",
    "**/venv/**",
]
```

## Performance

Pyright is fast:

- Large codebase (~50k lines): ~1-2s
- Incremental checks: Near-instant with watch mode

## Resources

- Docs: https://microsoft.github.io/pyright/
- Configuration: https://microsoft.github.io/pyright/#/configuration
- Type Checking Modes: https://microsoft.github.io/pyright/#/type-checking-modes
