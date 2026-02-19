# Ruff - Python Linter & Formatter

Fast Python linter and formatter written in Rust. Replaces Black, isort, and multiple Flake8 plugins.

## Why Ruff Over Alternatives

- **Ruff > Black**: 10-100x faster, includes linting + formatting
- **Ruff > isort**: Built-in import sorting with same speed advantage
- **Ruff > Flake8/Pylint**: Single tool, faster, auto-fixes available

## Core Commands

```bash
# Lint code (check for issues)
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Lint + format in one go
uv run ruff check --fix . && uv run ruff format .
```

## Common Workflows

### Check Before Commit

```bash
uv run ruff check --fix .
uv run ruff format .
```

### CI/CD Integration

```bash
# Check only (no modifications)
uv run ruff check .
uv run ruff format --check .
```

### Specific Files/Directories

```bash
uv run ruff check path/to/file.py
uv run ruff format scripts/
```

## Configuration

Located in `pyproject.toml` or `ruff.toml`:

```toml
[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "UP",     # pyupgrade (modern Python syntax)
    "B",      # flake8-bugbear (common bugs)
    "SIM",    # flake8-simplify (simplification)
]
ignore = [
    "E501",   # line too long (formatter handles this)
]
```

## Rule Categories

Common rule prefixes:

- `E`, `W` - pycodestyle (style violations)
- `F` - Pyflakes (logical errors)
- `I` - isort (import sorting)
- `UP` - pyupgrade (modernize syntax)
- `B` - bugbear (likely bugs)
- `SIM` - simplify (code simplification)
- `C90` - mccabe (complexity)
- `N` - pep8-naming (naming conventions)

## Exit Codes

- `0` - No issues found
- `1` - Issues found (or errors during execution)

## Output Interpretation

```bash
# Example output
path/to/file.py:10:5: F841 Local variable `x` is assigned but never used
path/to/file.py:15:1: E302 Expected 2 blank lines, found 1
```

Format: `file:line:column: CODE Message`

## Integration with Tests

Run from `/tests` directory:

```bash
cd tests
uv run ruff check ../.opencode/skill
uv run ruff format ../.opencode/skill
```

## Best Practices

1. **Run before commits** - Catch issues early
2. **Use --fix** - Auto-fix most issues automatically
3. **Format last** - Run `check --fix` before `format`
4. **Ignore sparingly** - Only ignore rules with good reason
5. **Project-wide config** - Keep configuration in `pyproject.toml`

## Common Issues

### Import Sorting Conflicts

Ruff handles import sorting automatically. Remove isort if present.

### Line Length

Formatter respects `line-length` setting. Default is 88 (Black's default).

### Ignore Specific Lines

```python
# ruff: noqa: E501
very_long_line_that_should_not_be_checked()

# Or specific rule
x = 1  # noqa: F841
```

## Performance

Ruff is 10-100x faster than alternatives:

- Large codebase (~50k lines): ~0.1s vs 10s+ (Black/Flake8)
- Incremental checks: Near-instant

## Resources

- Docs: https://docs.astral.sh/ruff/
- Rules: https://docs.astral.sh/ruff/rules/
- Configuration: https://docs.astral.sh/ruff/configuration/
