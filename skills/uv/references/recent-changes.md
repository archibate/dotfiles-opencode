# UV Recent Changes and Version Information

## Current Recommended Version

**Latest Stable Version: 0.9.7** (Released October 30, 2025)

This document tracks recent changes in UV that may affect your workflows, especially features that are not well-known or documented elsewhere yet.

## Version Check

Before using UV, verify your installed version:

```bash
uv --version
```

### Minimum Recommended Version: 0.9.0

If you have an older version, upgrade using:

```bash
# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# On Unix/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Using pip
pip install --upgrade uv

# Using pipx
pipx upgrade uv
```

## Major Changes in Recent Releases

### Version 0.9.7 (October 30, 2025)

#### Security Update - Tar Extraction

**What Changed:**
Upgraded to `astral-tokio-tar` to address vulnerabilities in tar extraction on malformed archives with mismatching size information.

**Impact:**

- More secure handling of tar archives
- Protection against malformed archive exploitation

**Action Required:**
Update to 0.9.7 or later if you frequently work with tar archives or install packages from untrusted sources.

#### Windows x86-32 Emulation Support

**What Changed:**
Added support for Windows x86-32 emulation for interpreter architecture checks.

**Impact:**

- Better compatibility on Windows systems
- Improved architecture detection

**Example:**

```bash
# Now works correctly on Windows x86-32 emulation
uv python install 3.14
uv python list
```

### Version 0.9.6 (October 29, 2025)

#### Python 3.14 Now Default

**What Changed:**
The default Python version changed from **3.13 to 3.14**.

**Impact:**
When you run `uv python install` without specifying a version, UV will now install Python 3.14 instead of 3.13.

**Examples:**

```bash
# Old behavior (before 0.9.6)
uv python install
# Would install Python 3.13

# New behavior (0.9.6+)
uv python install
# Installs Python 3.14

# To explicitly install specific version
uv python install 3.13
uv python install 3.12
```

**Migration Notes:**

If your project requires Python 3.13 or earlier:

```bash
# Pin your project to specific Python version
cd your-project
uv python pin 3.13

# Verify pinned version
cat .python-version
# Output: 3.13
```

**Test Case:**

```bash
# Create new project - should use Python 3.14 by default
mkdir test-project
cd test-project
uv init

# Check Python version being used
uv run python --version
# Should show: Python 3.14.x
```

#### Free-Threaded Python 3.14+ Support

**What Changed:**
Free-threaded variants of Python 3.14+ are no longer experimental and don't require explicit opt-in.

**Previous Behavior:**

```bash
# Required explicit selection with 't' suffix
uv python install 3.14t
```

**New Behavior:**

```bash
# Free-threaded Python automatically allowed
uv python install 3.14
# UV will use free-threaded variant if available and appropriate

# You can still explicitly select if needed
uv python install 3.14t
```

**What is Free-Threaded Python?**

Free-threaded Python (PEP 703) removes the Global Interpreter Lock (GIL), enabling true parallel execution of Python code on multiple CPU cores.

**Benefits:**

- True multi-core parallelism
- Better performance for CPU-intensive tasks
- Improved concurrency for multi-threaded applications

**When to Use:**

Use free-threaded Python when:

- Running CPU-intensive multi-threaded code
- Parallel processing is critical to performance
- Working with libraries that support free-threading

**Example:**

```python
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import threading
import time

def cpu_intensive_task(n):
    """Simulate CPU-intensive work"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result

# With free-threaded Python 3.14+, these threads run in parallel
threads = []
for i in range(4):
    t = threading.Thread(target=cpu_intensive_task, args=(10_000_000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All threads completed in parallel")
```

Run with:

```bash
uv run --python 3.14 script.py
```

#### Build --clear Flag

**What Changed:**
Added `--clear` flag to `uv build` command for removing old build artifacts before building.

**Usage:**

```bash
# Old workflow - manual cleanup
rm -rf dist/
uv build

# New workflow - automatic cleanup
uv build --clear
```

**Example Use Case:**

```bash
# Building a Python package for distribution
cd my-package

# Build with automatic cleanup of old artifacts
uv build --clear

# Artifacts are now in dist/ directory
ls dist/
# Output: my-package-1.0.0.tar.gz  my-package-1.0.0-py3-none-any.whl
```

**Benefits:**

- Prevents mixing old and new build artifacts
- Ensures clean builds
- Simplifies CI/CD workflows

**GitHub Actions Example:**

```yaml
- name: Build package
  run: uv build --clear

- name: Upload artifacts
  uses: actions/upload-artifact@v3
  with:
    name: dist
    path: dist/
```

#### Security Update - ZIP Parsing

**What Changed:**
Upgraded to Astral's fork of `async_zip` to address ZIP parsing differentials between UV and other Python packaging tools.

**Impact:**

- More consistent package installation behavior
- Reduced parsing differences with pip, poetry, etc.
- Better security against malformed ZIP archives

**Action Required:**
Update to 0.9.6 or later for improved security and compatibility.

### Version 0.9.5 (October 21, 2025)

#### Improved Error Messages

**What Changed:**
Enhanced error messages for externally managed Python environments and HTTP 403 Forbidden responses.

**Examples:**

**Before:**

```text
error: Failed to install package
```

**After:**

```text
error: Cannot install package in externally managed environment
hint: This Python environment is managed by your system package manager.
hint: Use --system flag to override, or create a virtual environment:
      python -m venv .venv && source .venv/bin/activate
```

**HTTP 403 Forbidden:**

```text
error: Failed to download package from https://pypi.org/simple/package-name/
error: 403 Forbidden
hint: This may be due to authentication required or network restrictions.
hint: Check your network connection and PyPI credentials.
```

### Version 0.9.0 (October 7, 2025)

#### Docker Image Updates

**What Changed:**
Updated base images to Alpine 3.22 and Debian 13 "Trixie".

**Impact:**

- More secure base images
- Latest system packages
- Better compatibility

**Dockerfile Example:**

```dockerfile
FROM ghcr.io/astral-sh/uv:latest

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv pip install -e .

CMD ["uv", "run", "python", "-m", "src.main"]
```

## Breaking Changes

### Python 3.14 Default (Version 0.9.6)

**What Breaks:**

If you have scripts or CI/CD pipelines that rely on Python 3.13 being installed by default:

```bash
# This now installs 3.14 instead of 3.13
uv python install
```

**Fix:**

Pin your Python version explicitly:

```bash
# In projects - use .python-version
uv python pin 3.13

# In scripts - specify version explicitly
uv python install 3.13
uv run --python 3.13 script.py

# In CI/CD - add version to workflow
- name: Install Python
  run: uv python install 3.13
```

## Testing New Features

### Test Python 3.14 Default

```bash
# Remove existing Python versions (optional)
rm -rf ~/.local/share/uv/python/

# Install default version
uv python install

# Verify it's 3.14
uv python list
# Should show 3.14.x as installed

# Create test project
mkdir test-py314
cd test-py314
uv init
uv run python --version
# Should output: Python 3.14.x
```

### Test Free-Threaded Python

```bash
# Install free-threaded Python
uv python install 3.14

# Check if free-threaded variant is available
uv python list --all-versions | grep 3.14

# Create test script
cat > test_threads.py << 'EOF'
import sys
import threading

def worker():
    print(f"Thread {threading.current_thread().name} running")

threads = [threading.Thread(target=worker, name=f"Worker-{i}") for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Python version: {sys.version}")
print(f"Thread-safe: {sys.flags.no_gil if hasattr(sys.flags, 'no_gil') else 'N/A'}")
EOF

# Run with Python 3.14
uv run --python 3.14 test_threads.py
```

### Test Build --clear Flag

```bash
# Create test package
mkdir test-package
cd test-package

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-package"
version = "0.1.0"
EOF

# Create source
mkdir src
echo 'print("Hello from test package")' > src/__init__.py

# Build with --clear flag
uv build --clear

# Verify artifacts
ls dist/
# Should show: test-package-0.1.0.tar.gz, test-package-0.1.0-py3-none-any.whl
```

## Compatibility Matrix

| UV Version | Python 3.10 | Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 | Free-Threading |
|------------|-------------|-------------|-------------|-------------|-------------|----------------|
| 0.9.0-0.9.5 | Full | Full | Full | Full (default) | Beta | Experimental |
| 0.9.6+ | Full | Full | Full | Full | Full (default) | Stable |
| 0.9.7+ | Full | Full | Full | Full | Full (default) | Stable |

## Deprecation Warnings

Currently, no major features are deprecated. UV maintains backward compatibility while adding new features.

## Future Changes

Based on UV development roadmap:

- Enhanced caching mechanisms
- Improved dependency resolution
- Better integration with IDEs
- Extended MCP server support

Stay updated by watching:

- UV GitHub releases: <https://github.com/astral-sh/uv/releases>
- UV documentation: <https://docs.astral.sh/uv/>

## Version-Specific Troubleshooting

### Issue: Python 3.14 Not Found

**Symptoms:**

```text
error: Python 3.14 not found
```

**Solution:**

```bash
# Update UV to latest version
pip install --upgrade uv

# Or reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh

# Then install Python 3.14
uv python install 3.14
```

### Issue: Free-Threaded Python Not Working

**Symptoms:**
Code doesn't show parallel execution improvements.

**Diagnosis:**

```bash
# Check if free-threaded variant is installed
uv python list --all-versions | grep -i "free\|gil"

# Verify Python build
uv run python -c "import sys; print(sys.flags)"
```

**Solution:**
Some libraries may not support free-threading yet. Check library compatibility before using free-threaded Python in production.

### Issue: Build --clear Not Working

**Symptoms:**

```text
error: unrecognized option '--clear'
```

**Solution:**
Update to UV 0.9.6 or later:

```bash
pip install --upgrade uv
uv --version  # Should be 0.9.6 or higher
```

## Additional Resources

- **UV Changelog**: <https://github.com/astral-sh/uv/blob/main/CHANGELOG.md>
- **Python 3.14 Release Notes**: <https://docs.python.org/3.14/whatsnew/3.14.html>
- **PEP 703 (Free-Threading)**: <https://peps.python.org/pep-0703/>
- **UV Discord Community**: <https://discord.gg/astral-sh>

## Summary

Keep UV updated to benefit from:

1. **Security improvements** (tar/ZIP parsing fixes)
2. **Python 3.14 support** with free-threading
3. **Better tooling** (build --clear flag)
4. **Enhanced error messages** for troubleshooting
5. **Performance optimizations** in every release

Check your version regularly and upgrade when new releases are available.
