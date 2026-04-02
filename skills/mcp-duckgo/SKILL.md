---
name: mcp-duckgo
description: This skill should be used for web search and content scraping via DuckDuckGo MCP Server.
---

# DuckDuckGo Search
Use DuckDuckGo MCP by executing shell commands.

## Web search
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' search query="{keyword}" max_results=10`

## Web fetch
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' fetch_content url="https://..."`
