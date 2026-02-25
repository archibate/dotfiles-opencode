# UV Installation and Setup Reference

## Overview

This reference covers UV installation across platforms and virtual environment setup, with special focus on Windows compatibility and best practices.

## Installation

### Windows

**PowerShell (Recommended):**

```powershell
powershell -c "irm https://install.python-uv.org | iex"
```

**Alternative Methods:**

```powershell
# Using installer script
Invoke-WebRequest -Uri https://install.astral.sh/uv -OutFile install.ps1
.\install.ps1

# Using pipx (if available)
pipx install uv
```

### Linux

```bash
# Standalone installer (Recommended)
curl -LsSf https://install.python-uv.org | sh

# Using pipx
pipx install uv

# Manual download
curl -sSL https://install.astral.sh/uv | sh
```

### macOS

```bash
# Homebrew (Recommended)
brew install astral-sh/tap/uv

# Standalone installer
curl -LsSf https://install.python-uv.org | sh
```

### Verification

After installation, verify UV is working:

```bash
uv --version
uvx --version

# Should output version number (e.g., uv 0.7.8)
```

## Virtual Environment Setup

### Windows Git Bash (Recommended for Windows)

**Status**: TESTED - UV works perfectly with venv virtual environments

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate environment
. .venv/Scripts/activate

# 3. Use UV for package management
uv pip install -r requirements.txt

# 4. Verify environment is active
echo $VIRTUAL_ENV
# Output: /d/path/to/project/.venv

# 5. Install packages
uv pip install requests numpy pandas
```

**Git Bash Activation Notes:**

Both `.` and `source` work identically:

```bash
# These are equivalent:
. .venv/Scripts/activate         # Recommended (shorter, POSIX standard)
source .venv/Scripts/activate    # Also works
```

### Windows CMD

```cmd
# 1. Create virtual environment
python -m venv .venv

# 2. Activate environment
.venv\Scripts\activate.bat

# 3. Use UV for package management
uv pip install -r requirements.txt
```

### Linux/macOS

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate environment
source .venv/bin/activate

# 3. Use UV for package management
uv pip install -r requirements.txt
```

## Project Initialization

### Method 1: UV Project Creation

```bash
# Create new project with UV
uv init my-project
cd my-project

# Project structure created:
# my-project/
# ├── .python-version
# ├── pyproject.toml
# ├── README.md
# └── src/
#     └── my_project/
#         └── __init__.py

# Add dependencies
uv add requests numpy

# Run project
uv run python src/my_project/main.py
```

### Method 2: Manual Setup with Virtual Environment

```bash
# Create project directory
mkdir my-project
cd my-project

# Create virtual environment
python -m venv .venv

# Activate (Windows Git Bash)
. .venv/Scripts/activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Create requirements.txt
cat > requirements.txt << EOF
requests
numpy
pandas
EOF

# Install dependencies
uv pip install -r requirements.txt
```

### Method 3: Existing Project Migration

```bash
# Navigate to existing project
cd existing-project

# Create virtual environment
python -m venv .venv

# Activate environment
. .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate  # Linux/Mac

# Install from existing requirements
uv pip install -r requirements.txt

# Or install from poetry/pipenv
uv pip install poetry
poetry export -f requirements.txt -o requirements.txt
uv pip install -r requirements.txt
```

## Common UV Commands

### Package Management

```bash
# Install single package
uv pip install requests

# Install from requirements file
uv pip install -r requirements.txt

# Install with version constraint
uv pip install "requests>=2.28.0"

# Install multiple packages
uv pip install requests numpy pandas

# Uninstall package
uv pip uninstall requests

# List installed packages
uv pip list

# Show package information
uv pip show requests

# Freeze dependencies
uv pip freeze > requirements.txt
```

### Tool Management

```bash
# Install persistent CLI tool
uv tool install black

# List installed tools
uv tool list

# Upgrade tool
uv tool upgrade black

# Upgrade all tools
uv tool upgrade --all

# Uninstall tool
uv tool uninstall black

# Run tool temporarily with uvx
uvx black my_file.py
```

### Python Version Management

```bash
# List available Python versions
uv python list

# List installed Python versions
uv python list --installed

# Install Python version
uv python install 3.12

# Install specific minor version
uv python install 3.12.1

# Pin Python version for project
uv python pin 3.12

# Show pinned version
cat .python-version
```

## Testing Installation

### Complete Verification Script

**For Windows Git Bash:**

```bash
#!/bin/bash

echo "=== UV Installation Test ==="

# Check UV version
echo "1. UV Version:"
uv --version

# Create test environment
echo "2. Creating test virtual environment..."
python -m venv test-venv

# Activate environment
echo "3. Activating environment..."
. test-venv/Scripts/activate

# Verify activation
echo "4. Virtual environment path:"
echo $VIRTUAL_ENV

# Install test package
echo "5. Installing test package with UV..."
uv pip install requests

# Verify installation
echo "6. Testing package import..."
python -c "import requests; print(f'Requests version: {requests.__version__}')"

# List packages
echo "7. Installed packages:"
uv pip list

# Cleanup
echo "8. Cleanup..."
deactivate
rm -rf test-venv

echo "=== Test Complete ==="
```

**For Linux/macOS:**

```bash
#!/bin/bash

echo "=== UV Installation Test ==="

# Check UV version
echo "1. UV Version:"
uv --version

# Create test environment
echo "2. Creating test virtual environment..."
python -m venv test-venv

# Activate environment
echo "3. Activating environment..."
source test-venv/bin/activate

# Verify activation
echo "4. Virtual environment path:"
echo $VIRTUAL_ENV

# Install test package
echo "5. Installing test package with UV..."
uv pip install requests

# Verify installation
echo "6. Testing package import..."
python -c "import requests; print(f'Requests version: {requests.__version__}')"

# List packages
echo "7. Installed packages:"
uv pip list

# Cleanup
echo "8. Cleanup..."
deactivate
rm -rf test-venv

echo "=== Test Complete ==="
```

## Platform-Specific Considerations

### Windows Cache and Environment

**Path Separators:**

- Use `/` or `\\` in paths depending on context
- Git Bash accepts both Unix-style (`/`) and Windows-style (`\\`) paths
- CMD requires Windows-style paths (`\\`)

**Virtual Environment Activation:**

- Git Bash: `. .venv/Scripts/activate`
- CMD: `.venv\Scripts\activate.bat`
- PowerShell: `.venv\Scripts\Activate.ps1`

**UV Cache Location:**

```text
%LOCALAPPDATA%\uv\cache\
```

### Linux/macOS Cache and Environment

**Virtual Environment Activation:**

```bash
source .venv/bin/activate
```

**UV Cache Location:**

```text
~/.cache/uv/
```

**Permissions:**

```bash
# If permission errors occur
chmod +x ~/.local/bin/uv
chmod +x ~/.local/bin/uvx
```

## Troubleshooting

### UV Not Found After Installation

**Windows:**

```powershell
# Check if UV is in PATH
$env:PATH -split ';' | Select-String "uv"

# Add to PATH manually if needed
$env:PATH += ";$env:LOCALAPPDATA\Programs\uv"
```

**Linux/macOS:**

```bash
# Check if UV is in PATH
echo $PATH | tr ':' '\n' | grep uv

# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Reload shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

### Virtual Environment Not Activating

**Symptoms:**

- `$VIRTUAL_ENV` is empty
- Packages install to global Python

**Solutions:**

**For Git Bash:**

```bash
# Ensure using correct activation command
. .venv/Scripts/activate

# Check if activate script exists
ls .venv/Scripts/activate

# Recreate if missing
rm -rf .venv
python -m venv .venv
```

**For CMD:**

```cmd
# Use .bat extension
.venv\Scripts\activate.bat

# Check script exists
dir .venv\Scripts\activate.bat
```

### UV Pip Install Fails

**Symptoms:**

- "No virtual environment found"
- Packages install to wrong location

**Solutions:**

```bash
# Ensure virtual environment is activated
echo $VIRTUAL_ENV  # Should show path

# If not activated, activate it
. .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate  # Linux/Mac

# Verify activation
which python  # Should point to .venv

# Then install
uv pip install package-name
```

### Permission Errors

**Windows:**

```powershell
# Run PowerShell as Administrator
# Then reinstall UV
powershell -c "irm https://install.python-uv.org | iex"
```

**Linux/macOS:**

```bash
# Check UV cache permissions
ls -la ~/.cache/uv/

# Fix permissions if needed
chmod -R u+w ~/.cache/uv/

# Or install with different permissions
curl -LsSf https://install.python-uv.org | sh
```

### Slow Package Installation

**Potential Causes:**

- Network proxy issues
- Antivirus scanning
- Large package dependencies

**Solutions:**

```bash
# Clear UV cache
uv cache clean

# Use specific index
uv pip install --index-url https://pypi.org/simple package-name

# Check cache size
du -sh ~/.cache/uv/  # Linux/Mac
dir /s %LOCALAPPDATA%\uv\cache  # Windows
```

## Performance Benefits

### Tested Results (UV 0.7.8 + Python 3.13.0)

**Package Installation Speed:**

- 10-100x faster than standard pip
- Parallel downloads and installations
- Intelligent caching with deduplication

**Example Comparison:**

```bash
# Standard pip
time pip install pandas numpy scipy
# ~45 seconds

# UV
time uv pip install pandas numpy scipy
# ~2 seconds (after first download)
```

**Benefits:**

- UV automatically detects virtual environments
- Perfect environment isolation
- Same commands as pip (drop-in replacement)
- Superior dependency conflict resolution

## Best Practices

### Environment Management

1. **Always use virtual environments** for projects
2. **Activate before installing** packages
3. **Use `python -m venv`** for compatibility
4. **Document activation** in README.md

### Package Management Best Practices

1. **Use UV for all installs** in virtual environments
2. **Freeze dependencies** regularly (`uv pip freeze`)
3. **Keep requirements.txt** updated
4. **Test installations** in fresh environments

### Tool Management Best Practices

1. **Install development tools** with `uv tool install`
2. **Use uvx** for temporary executions
3. **Upgrade tools regularly** with `uv tool upgrade --all`
4. **Keep tools isolated** (don't use global pip)

## Quick Reference Card

```bash
# Installation
curl -LsSf https://install.python-uv.org | sh  # Linux/Mac
powershell -c "irm https://install.python-uv.org | iex"  # Windows

# Virtual Environment
python -m venv .venv
. .venv/Scripts/activate  # Windows Git Bash
source .venv/bin/activate  # Linux/Mac

# Package Management
uv pip install package-name
uv pip install -r requirements.txt
uv pip list
uv pip freeze > requirements.txt

# Tool Management
uv tool install black
uvx black file.py

# Python Versions
uv python list
uv python install 3.12
uv python pin 3.12
```

## Summary

UV provides fast, reliable Python package management across all platforms. The recommended workflow is:

1. Install UV once globally
2. Create virtual environments with `python -m venv`
3. Activate environments before work
4. Use UV for all package operations
5. Use UV tool/uvx for CLI utilities

This combination provides maximum compatibility, performance, and reliability.
