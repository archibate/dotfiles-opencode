# Python Environment Management Reference

## Overview

This reference covers Python version management with UV, including installation paths, version pinning, and cross-platform compatibility. It also covers integration with pyenv and system Python.

## Python Installation Paths

### UV Python Installations

UV stores managed Python installations in platform-specific locations:

**Linux/macOS:**

```text
~/.local/share/uv/python/cpython-<version>-<platform>/bin/python3
```

**Windows:**

```text
%LOCALAPPDATA%\uv\python\cpython-<version>-<platform>\python.exe
```

**Example Paths:**

Linux:

```text
~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3
~/.local/share/uv/python/cpython-3.11.8-linux-x86_64-gnu/bin/python3
```

Windows:

```text
C:\Users\username\AppData\Local\uv\python\cpython-3.12.6-windows-x86_64\python.exe
C:\Users\username\AppData\Local\uv\python\cpython-3.11.8-windows-x86_64\python.exe
```

macOS:

```text
~/.local/share/uv/python/cpython-3.12.6-macos-aarch64/bin/python3
~/.local/share/uv/python/cpython-3.12.6-macos-x86_64/bin/python3
```

### Pyenv Python Installations

Pyenv stores Python installations in:

**Linux/macOS:**

```text
~/.pyenv/versions/<version>/bin/python
```

**Windows (pyenv-win):**

```text
%USERPROFILE%\.pyenv\pyenv-win\versions\<version>\python.exe
```

**Example Paths:**

```text
~/.pyenv/versions/3.12.4/bin/python3.12
~/.pyenv/versions/3.11.8/bin/python3.11
~/.pyenv/versions/3.10.13/bin/python3.10
```

### System Python

System Python locations vary by platform:

**Linux (Debian/Ubuntu):**

```text
/usr/bin/python3
/usr/bin/python3.8
/usr/bin/python3.10
```

**Linux (Fedora/RHEL):**

```text
/usr/bin/python3
/usr/bin/python3.9
```

**macOS:**

```text
/usr/bin/python3
/Library/Frameworks/Python.framework/Versions/3.x/bin/python3
```

**Windows:**

```text
C:\Python311\python.exe
C:\Program Files\Python311\python.exe
```

## UV Python Version Management

### Installation Commands

```bash
# Install latest Python version
uv python install

# Install specific version
uv python install 3.12

# Install specific patch version
uv python install 3.12.6

# Install multiple versions
uv python install 3.11 3.12 3.13

# Install from version file
uv python install --from-version-file .python-version
```

### Listing Python Versions

```bash
# List all available Python versions
uv python list

# List only installed versions
uv python list --installed

# List with detailed information
uv python list --all-versions
```

### Finding Python Paths

```bash
# Find path to specific Python version
uv python find 3.12

# Find path to specific patch version
uv python find 3.12.6

# Find path and show details
uv python find 3.12 --verbose
```

### Version Pinning

```bash
# Pin Python version for project
uv python pin 3.12

# Pin specific patch version
uv python pin 3.12.6

# Creates .python-version file:
# 3.12.6

# Use pinned version
uv run python script.py  # Uses version from .python-version
```

### Environment Variables

```bash
# Set custom Python installation directory
export UV_PYTHON_INSTALL_DIR=/custom/path/to/pythons

# On Windows
set UV_PYTHON_INSTALL_DIR=C:\custom\path\to\pythons
```

## Direct Path Execution

### Using Direct Paths

When shell wrappers (like pyenv) aren't available, use direct paths:

**UV Python:**

```bash
# Linux/macOS
~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3 script.py

# Windows
%LOCALAPPDATA%\uv\python\cpython-3.12.6-windows-x86_64\python.exe script.py
```

**Pyenv Python:**

```bash
# Linux/macOS
~/.pyenv/versions/3.12.4/bin/python3.12 script.py

# Windows (pyenv-win)
%USERPROFILE%\.pyenv\pyenv-win\versions\3.12.4\python.exe script.py
```

**System Python:**

```bash
# Linux
/usr/bin/python3.10 script.py

# Windows
C:\Python311\python.exe script.py
```

### With Working Directories

```bash
# Change directory then execute
cd /path/to/working/directory && ~/.pyenv/versions/3.12.4/bin/python3.12 script.py

# Using UV run with directory
uv run --directory /path/to/working/directory --python 3.12 script.py

# Using Python's os.chdir (within script)
python -c "import os; os.chdir('/path/to/dir'); exec(open('script.py').read())"
```

## Temporary PATH Modification

### For Single Commands

```bash
# Prepend Python to PATH for one command
PATH=~/.pyenv/versions/3.12.4/bin:$PATH python script.py

# UV Python on Linux
PATH=~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin:$PATH python script.py

# With working directory
cd /path/to/dir && PATH=~/.pyenv/versions/3.12.4/bin:$PATH python script.py
```

**Windows:**

```cmd
set PATH=C:\Users\username\AppData\Local\uv\python\cpython-3.12.6-windows-x86_64;%PATH% && python script.py
```

## UV Run Command

### Basic Usage

```bash
# Run with specific Python version
uv run --python 3.12 script.py

# Run with specific patch version
uv run --python 3.12.6 script.py

# Run with direct path
uv run --python /path/to/python script.py

# Run with working directory
uv run --directory /path/to/dir --python 3.12 script.py
```

### Advanced Patterns

```bash
# Run with arguments
uv run --python 3.12 script.py arg1 arg2 --flag

# Run with environment variables
ENV_VAR=value uv run --python 3.12 script.py

# Run module
uv run --python 3.12 -m module_name

# Run with specific requirements
uv run --python 3.12 --with requests --with pandas script.py
```

## Shebang Lines

### Direct Path Shebangs

**UV Python:**

```python
#!/home/user/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3
import sys
print(sys.version)
```

**Pyenv Python:**

```python
#!/home/user/.pyenv/versions/3.12.4/bin/python3.12
import sys
print(sys.version)
```

**System Python:**

```python
#!/usr/bin/python3
import sys
print(sys.version)
```

### env-based Shebangs

```python
#!/usr/bin/env python3
# Uses first python3 found in PATH

#!/usr/bin/env python
# Uses first python found in PATH
```

## Cross-Platform Compatibility

### Path Separators

**Linux/macOS:**

```bash
# Use forward slashes
~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3
```

**Windows:**

```cmd
# Use backslashes or forward slashes
%LOCALAPPDATA%\uv\python\cpython-3.12.6-windows-x86_64\python.exe
C:/Users/username/AppData/Local/uv/python/cpython-3.12.6-windows-x86_64/python.exe
```

### Platform Detection

```python
import platform
import sys

# Get platform info
print(platform.system())      # Windows, Linux, Darwin
print(platform.machine())     # x86_64, aarch64, AMD64
print(sys.version_info)       # (3, 12, 6, 'final', 0)

# Construct UV Python path
import os
from pathlib import Path

if platform.system() == "Windows":
    uv_python_dir = Path(os.environ["LOCALAPPDATA"]) / "uv" / "python"
else:
    uv_python_dir = Path.home() / ".local" / "share" / "uv" / "python"
```

## Finding Python Installations

### UV Python Discovery

```bash
# Find specific version
uv python find 3.12

# Output:
# /home/user/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3

# List all installed
uv python list --installed

# Output:
# cpython-3.12.6-linux-x86_64-gnu    /home/user/.local/share/uv/python/...
# cpython-3.11.8-linux-x86_64-gnu    /home/user/.local/share/uv/python/...
```

### Pyenv Python Discovery

```bash
# Get global version
pyenv global

# Get path to global Python
pyenv which python

# List all versions
pyenv versions

# Find specific version path
echo ~/.pyenv/versions/$(pyenv global | head -1)/bin/python
```

### System Python Discovery

```bash
# Find Python in PATH
which python3       # Linux/macOS
where python        # Windows

# Find all Python installations
whereis python3     # Linux

# Check Python version
python3 --version
```

## Creating Symlinks and Wrappers

### Symlinks (Linux/macOS)

```bash
# Create symlink to specific UV Python
ln -s ~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3 \
      ~/bin/python3.12

# Create symlink to pyenv Python
ln -s ~/.pyenv/versions/3.12.4/bin/python3.12 \
      ~/bin/python3.12.4

# Add ~/bin to PATH in .bashrc or .zshrc
export PATH="$HOME/bin:$PATH"
```

### Wrapper Scripts

**Linux/macOS:**

```bash
# Create wrapper script
cat > ~/bin/python3.12 << 'EOF'
#!/bin/bash
exec ~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3 "$@"
EOF

chmod +x ~/bin/python3.12
```

**Windows (Batch):**

```batch
@echo off
C:\Users\username\AppData\Local\uv\python\cpython-3.12.6-windows-x86_64\python.exe %*
```

**Windows (PowerShell):**

```powershell
# Save as python3.12.ps1
& "C:\Users\username\AppData\Local\uv\python\cpython-3.12.6-windows-x86_64\python.exe" @args
```

## PYTHONPATH Configuration

### Adding Module Search Paths

```bash
# Add directory to Python module search path
export PYTHONPATH=/path/to/modules:$PYTHONPATH

# Windows
set PYTHONPATH=C:\path\to\modules;%PYTHONPATH%

# Use in command
PYTHONPATH=/path/to/modules python script.py
```

**Note:** PYTHONPATH adds to module search path but doesn't change working directory.

## Best Practices

### Version Management

1. **Use UV for Python version management** - Faster and more reliable than manual downloads
2. **Pin versions in projects** - Create `.python-version` file for consistency
3. **Use `uv python list --installed`** - Track what's installed
4. **Clean old versions** - Remove unused Python installations periodically

### Path Management

1. **Use direct paths when needed** - More reliable than PATH manipulation
2. **Document required Python version** - In README.md or requirements
3. **Use `uv run --python`** - When you need specific version for script
4. **Create wrapper scripts** - For frequently used specific versions

### Cross-Platform

1. **Use pathlib** - For cross-platform path handling in Python
2. **Document platform differences** - In configuration or setup guides
3. **Test on target platforms** - Don't assume path compatibility
4. **Use environment variables** - For platform-specific paths

## Troubleshooting

### Python Version Not Found

**Symptoms:**

- "Python 3.x not found"
- Version mismatch errors

**Solutions:**

```bash
# List installed versions
uv python list --installed

# Install missing version
uv python install 3.12

# Verify installation
uv python find 3.12

# Check PATH
echo $PATH | grep python
```

### Version Conflict

**Symptoms:**

- Wrong Python version executing
- Unexpected module not found errors

**Solutions:**

```bash
# Pin version for project
uv python pin 3.12

# Use explicit version in command
uv run --python 3.12 script.py

# Check which Python is being used
which python
python --version

# Use full path to avoid ambiguity
~/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3 script.py
```

### PATH Issues

**Symptoms:**

- Commands not found
- Wrong version executing

**Solutions:**

```bash
# Check current PATH
echo $PATH

# Add UV Python to PATH (temporary)
export PATH="$HOME/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin:$PATH"

# Add to shell profile permanently (.bashrc, .zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission Errors

**Symptoms:**

- Cannot write to Python directory
- Installation fails

**Solutions:**

```bash
# Check Python installation directory permissions
ls -la ~/.local/share/uv/python/

# Fix permissions
chmod -R u+w ~/.local/share/uv/python/

# Use custom install directory
export UV_PYTHON_INSTALL_DIR=$HOME/python-versions
uv python install 3.12
```

## Recommended Approaches

### For Different Use Cases

**One-off commands:**

```bash
# Use uv run
uv run --python 3.12 script.py
```

**Scripts with shebangs:**

```python
#!/usr/bin/env python3
# Or use direct path for specific version
```

**Applications needing specific version:**

```bash
# Use direct path in configuration
python_path = "/home/user/.local/share/uv/python/cpython-3.12.6-linux-x86_64-gnu/bin/python3"
```

**Working with specific directories:**

```bash
# Use uv run with --directory
uv run --directory /path/to/project --python 3.12 script.py
```

**Comprehensive Python management:**

```bash
# Use UV for installation and management
uv python install 3.12
uv python pin 3.12
uv run python script.py
```

## Summary

UV provides comprehensive Python version management:

- **Automatic installation** of Python versions
- **Version pinning** with `.python-version` files
- **Direct path access** for shell-independent execution
- **Cross-platform compatibility** with consistent interfaces
- **Fast performance** compared to manual downloads
- **Integration** with existing Python tools (pyenv, system Python)

Use `uv python install` for version management and `uv run --python` for version-specific script execution.
