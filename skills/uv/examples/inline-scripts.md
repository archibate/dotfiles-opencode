# Inline Script Metadata (PEP 723)

## Overview

UV supports inline script metadata, allowing you to define dependencies directly in Python script comments. UV automatically installs these dependencies when running the script.

## Basic Inline Dependencies

```python
# /// script
# dependencies = [
#   "requests",
#   "pandas",
#   "numpy",
# ]
# ///

import requests
import pandas as pd
import numpy as np

def main():
    response = requests.get("https://api.example.com/data")
    df = pd.DataFrame(response.json())
    print(df.describe())

if __name__ == "__main__":
    main()
```

**Run with UV:**

```bash
# UV automatically installs dependencies and runs the script
uv run script.py

# Or with uvx
uvx script.py
```

## With Python Version Requirement

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

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run with specific Python version:**

```bash
uv run --python 3.11 server.py
```

## MCP Server with Inline Dependencies

```python
# /// script
# dependencies = [
#   "mcp>=0.1.0",
#   "anthropic-sdk>=0.3.0",
# ]
# ///

from mcp.server import Server
from mcp.types import Tool

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="echo", description="Echo a message", input_schema={})
    ]

if __name__ == "__main__":
    server.run()
```

**VS Code Configuration:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "/path/to/server.py"]
    }
  }
}
```

## Data Processing Script

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

def analyze_data(file_path: str):
    # Read data with polars (faster than pandas)
    df = pl.read_csv(file_path)

    # Perform analysis
    summary = df.describe()
    print(summary)

    # Create visualization
    sns.histplot(df.to_pandas()["column_name"])
    plt.savefig("output.png")

if __name__ == "__main__":
    import sys
    analyze_data(sys.argv[1])
```

**Usage:**

```bash
# UV installs polars, matplotlib, seaborn automatically
uv run analyze.py data.csv
```

## Benefits of Inline Script Metadata

1. **Self-contained scripts** - Dependencies travel with the script
2. **No pyproject.toml needed** - Perfect for single-file scripts
3. **Automatic dependency management** - UV handles installation
4. **Version control friendly** - Everything in one file
5. **Easy sharing** - Send script, UV handles the rest

## When to Use Inline Metadata

**DO use for:**

- Single-file utility scripts
- Data analysis notebooks converted to scripts
- Quick automation tasks
- Shareable examples and demos
- Scripts without full project structure

**DON'T use for:**

- Multi-file projects (use pyproject.toml instead)
- Scripts with many dependencies (harder to read)
- Production applications (use proper project structure)
- Scripts that need development dependencies separately

## Related Documentation

- [Inline Script Metadata Reference](../references/inline-script-metadata.md)
- [Python Environment Management](../references/python-environment.md)
- [MCP Integration](../references/mcp-integration.md)
