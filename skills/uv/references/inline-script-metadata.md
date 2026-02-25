# UV Inline Script Metadata Reference (PEP 723)

## Overview

UV supports PEP 723 inline script metadata, allowing you to define dependencies directly in Python script comments. This eliminates the need for separate `pyproject.toml` files for single-file scripts and enables self-contained, shareable Python scripts.

## What is Inline Script Metadata?

Inline script metadata is a standardized way (PEP 723) to embed dependency information directly in Python script comments. UV reads these metadata blocks and automatically manages dependencies when running the script.

### Basic Syntax

```python
# /// script
# dependencies = [
#   "package-name",
#   "another-package>=1.0.0",
# ]
# requires-python = ">=3.10"
# ///

# Your Python code here
```

**Key Elements:**

- `# /// script` - Opening marker (must be exact)
- `# dependencies = [...]` - List of package dependencies
- `# requires-python = "..."` - Optional Python version constraint
- `# ///` - Closing marker (must be exact)

**Important:** The markers `# /// script` and `# ///` must be on their own lines with exact spacing.

## Basic Examples

### Simple Script with Dependencies

```python
# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///

import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.title.string

if __name__ == "__main__":
    title = scrape_website("https://example.com")
    print(f"Page title: {title}")
```

**Run with UV:**

```bash
# UV automatically installs requests and beautifulsoup4
uv run scraper.py
```

### With Specific Versions

```python
# /// script
# dependencies = [
#   "requests>=2.28.0,<3.0.0",
#   "pandas==2.1.0",
#   "numpy>=1.24.0",
# ]
# requires-python = ">=3.10"
# ///

import pandas as pd
import numpy as np
import requests

def fetch_and_analyze(api_url):
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)
    return df.describe()

if __name__ == "__main__":
    stats = fetch_and_analyze("https://api.example.com/data")
    print(stats)
```

**Run with UV:**

```bash
# UV ensures Python 3.10+ and specific package versions
uv run analysis.py
```

## Data Processing Examples

### Polars Data Analysis

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "polars>=0.19.0",
#   "matplotlib>=3.8.0",
#   "seaborn>=0.12.0",
# ]
# ///

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def analyze_csv(file_path: str):
    # Read data with polars (faster than pandas)
    df = pl.read_csv(file_path)

    # Print summary statistics
    print(df.describe())

    # Create visualization
    plt.figure(figsize=(10, 6))
    data_pandas = df.to_pandas()
    sns.histplot(data=data_pandas, x="column_name", bins=30)
    plt.title("Data Distribution")
    plt.savefig("distribution.png")
    print("Saved visualization to distribution.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <file.csv>")
        sys.exit(1)
    analyze_csv(sys.argv[1])
```

**Usage:**

```bash
uv run analyze.py data.csv
```

### Excel Processing

```python
# /// script
# dependencies = [
#   "openpyxl>=3.1.0",
#   "pandas>=2.0.0",
# ]
# ///

import pandas as pd
import sys

def process_excel(input_file: str, output_file: str):
    # Read Excel file
    df = pd.read_excel(input_file)

    # Perform transformations
    df['total'] = df['quantity'] * df['price']
    summary = df.groupby('category')['total'].sum()

    # Write to new Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        summary.to_excel(writer, sheet_name='Summary')

    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process.py input.xlsx output.xlsx")
        sys.exit(1)
    process_excel(sys.argv[1], sys.argv[2])
```

**Usage:**

```bash
uv run process.py input.xlsx output.xlsx
```

## Web Application Examples

### FastAPI Server

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi>=0.100.0",
#   "uvicorn[standard]>=0.24.0",
# ]
# ///

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Simple API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run server:**

```bash
uv run server.py
# Visit http://localhost:8000
```

### Flask Application

```python
# /// script
# dependencies = [
#   "flask>=3.0.0",
#   "flask-cors>=4.0.0",
# ]
# ///

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask API"})

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        return jsonify({"received": data}), 201
    else:
        return jsonify({"data": ["item1", "item2", "item3"]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Run server:**

```bash
uv run app.py
```

## MCP Server Examples

### Basic MCP Server

```python
# /// script
# dependencies = [
#   "mcp>=0.1.0",
# ]
# ///

from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("example-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="Greet someone by name",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        person_name = arguments.get("name", "World")
        return [TextContent(
            type="text",
            text=f"Hello, {person_name}!"
        )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```

**VS Code Configuration:**

```json
{
  "mcpServers": {
    "example": {
      "command": "uv",
      "args": ["run", "/path/to/mcp_server.py"]
    }
  }
}
```

### MCP Server with Database

```python
# /// script
# dependencies = [
#   "mcp>=0.1.0",
#   "aiosqlite>=0.19.0",
# ]
# ///

from mcp.server import Server
from mcp.types import Tool, TextContent
import aiosqlite
import os

server = Server("database-server")
DB_PATH = os.getenv("DB_PATH", "data.db")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_db",
            description="Execute SQL query",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query_db":
        query = arguments.get("query")
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(query)
            results = await cursor.fetchall()
            return [TextContent(
                type="text",
                text=str(results)
            )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```

**VS Code Configuration with Environment:**

```json
{
  "mcpServers": {
    "database": {
      "command": "uv",
      "args": ["run", "/path/to/db_server.py"],
      "env": {
        "DB_PATH": "/path/to/database.db"
      }
    }
  }
}
```

## Automation and CLI Tools

### File Processor

```python
# /// script
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///

import typer
from rich.console import Console
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def process(
    input_dir: Path = typer.Argument(..., help="Input directory"),
    output_dir: Path = typer.Argument(..., help="Output directory"),
    pattern: str = typer.Option("*.txt", help="File pattern to match")
):
    """Process files matching pattern from input to output directory."""
    files = list(input_dir.glob(pattern))

    with console.status(f"Processing {len(files)} files..."):
        for file in files:
            # Your processing logic here
            output_path = output_dir / file.name
            output_path.write_text(file.read_text().upper())

    console.print(f"[green]✓[/green] Processed {len(files)} files")

if __name__ == "__main__":
    app()
```

**Usage:**

```bash
uv run processor.py input/ output/ --pattern "*.txt"
```

### AWS Resource Lister

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "boto3>=1.28.0",
#   "rich>=13.0.0",
# ]
# ///

import boto3
from rich.console import Console
from rich.table import Table

def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    console = Console()
    table = Table(title="S3 Buckets")
    table.add_column("Name", style="cyan")
    table.add_column("Creation Date", style="magenta")

    for bucket in response['Buckets']:
        table.add_row(
            bucket['Name'],
            bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
        )

    console.print(table)

if __name__ == "__main__":
    list_s3_buckets()
```

**Usage:**

```bash
# Assumes AWS credentials are configured
uv run list_buckets.py
```

## Running Inline Scripts

### Basic Execution

```bash
# UV installs dependencies and runs the script
uv run script.py

# With arguments
uv run script.py arg1 arg2 --flag

# With specific Python version
uv run --python 3.11 script.py
```

### Using uvx

```bash
# Run from any location
uvx /path/to/script.py

# With arguments
uvx script.py --input data.csv --output results.csv
```

### In IDE Configurations

**VS Code tasks.json:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Script with UV",
      "type": "shell",
      "command": "uv",
      "args": ["run", "${file}"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

**VS Code launch.json:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "UV Run",
      "type": "python",
      "request": "launch",
      "module": "uv",
      "args": ["run", "${file}"]
    }
  ]
}
```

## Best Practices

### When to Use Inline Script Metadata

**DO use for:**

- Single-file utility scripts
- Quick automation tasks
- Data analysis scripts
- Shareable examples and demos
- Scripts without complex project structure
- CLI tools that fit in one file
- Learning and experimentation

**DON'T use for:**

- Multi-file projects (use `pyproject.toml` instead)
- Applications with many dependencies (>10-15 packages)
- Projects requiring separate dev/test dependencies
- Production applications with complex deployment
- Scripts that need package extras or complex configurations

### Dependency Management

**Prefer specific versions for reproducibility:**

```python
# Good - reproducible
# dependencies = [
#   "requests==2.31.0",
#   "pandas==2.1.0",
# ]
```

**Use version ranges for flexibility:**

```python
# Good for utilities - allows newer compatible versions
# dependencies = [
#   "requests>=2.28.0,<3.0.0",
#   "pandas>=2.0.0",
# ]
```

**Avoid unpinned versions in production:**

```python
# Risky - behavior can change unexpectedly
# dependencies = [
#   "requests",
#   "pandas",
# ]
```

### Python Version Constraints

```python
# Require minimum Python version
# requires-python = ">=3.10"

# Require specific version range
# requires-python = ">=3.10,<3.13"

# Require exact version (rarely needed)
# requires-python = "==3.11"
```

### Organizing Dependencies

**Alphabetical order for readability:**

```python
# /// script
# dependencies = [
#   "aiohttp>=3.9.0",
#   "beautifulsoup4>=4.12.0",
#   "pandas>=2.0.0",
#   "requests>=2.28.0",
# ]
# ///
```

**Group by purpose with comments:**

```python
# /// script
# dependencies = [
#   # Web scraping
#   "requests>=2.28.0",
#   "beautifulsoup4>=4.12.0",
#   # Data processing
#   "pandas>=2.0.0",
#   "numpy>=1.24.0",
#   # Visualization
#   "matplotlib>=3.8.0",
#   "seaborn>=0.12.0",
# ]
# ///
```

## Performance Considerations

### First Run

- UV downloads and installs all dependencies
- Creates isolated environment
- Caches packages for future use
- Typical time: 5-30 seconds depending on dependencies

### Subsequent Runs

- UV uses cached packages
- Environment reused if dependencies unchanged
- Typical startup: <1 second

### Cache Management

```bash
# Check UV cache size
du -sh ~/.cache/uv/  # Linux/Mac
dir /s %LOCALAPPDATA%\uv\cache  # Windows

# Clean UV cache
uv cache clean
```

## Troubleshooting

### Invalid Metadata Format

**Error:**

```text
Failed to parse inline script metadata
```

**Solution:**
Ensure exact syntax:

```python
# /// script    <- Must be exactly "# /// script"
# dependencies = [
#   "package",  <- Proper TOML array format
# ]
# ///           <- Must be exactly "# ///"
```

### Dependency Not Found

**Error:**

```text
Package 'package-name' not found on PyPI
```

**Solution:**

- Verify package name on PyPI
- Check for typos in package name
- Ensure package is available on PyPI

### Version Conflict

**Error:**

```text
Unable to resolve dependencies
```

**Solution:**

- Check version constraints are compatible
- Loosen version requirements if too restrictive
- Remove version constraints to find compatible versions

### Python Version Mismatch

**Error:**

```text
Requires Python >=3.11 but found 3.10
```

**Solution:**

```bash
# Install required Python version
uv python install 3.11

# Run with specific version
uv run --python 3.11 script.py
```

## Comparison with Other Approaches

### vs pyproject.toml

**Inline Script Metadata:**

- ✅ Single file - easy to share
- ✅ No project structure needed
- ✅ Perfect for utilities
- ❌ Limited to one file
- ❌ No dev dependencies separation

**pyproject.toml:**

- ✅ Multi-file projects
- ✅ Separate dev dependencies
- ✅ More configuration options
- ❌ Requires project structure
- ❌ Multiple files to share

### vs requirements.txt

**Inline Script Metadata:**

- ✅ Dependencies in same file as code
- ✅ UV manages everything automatically
- ✅ Version control friendly
- ✅ Self-documenting

**requirements.txt:**

- ✅ Separate from code
- ✅ Familiar to most Python developers
- ❌ Requires manual management
- ❌ Two files to maintain

### vs Docker

**Inline Script Metadata:**

- ✅ No Docker required
- ✅ Faster startup
- ✅ Native Python execution
- ✅ Simpler for users

**Docker:**

- ✅ Complete environment isolation
- ✅ System dependencies included
- ✅ Cross-platform guaranteed
- ❌ Heavier weight
- ❌ Slower startup

## Summary

Inline script metadata (PEP 723) is perfect for:

- **Single-file scripts** that need dependencies
- **Quick utilities** and automation tasks
- **Shareable examples** that "just work"
- **Learning and experimentation**
- **CLI tools** that fit in one file

Use `uv run script.py` and UV handles the rest - no virtual environments, no pip install, no project setup. Just write your script and run it.

For multi-file projects or complex applications, use traditional `pyproject.toml` instead.
