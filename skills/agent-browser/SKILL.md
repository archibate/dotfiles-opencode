---
name: agent-browser
description: Use this skill for browser automation.
---

# agent-browser

A CLI tool for browser automation. It maintains a persistent browser session with cookies - login once and stay authenticated across all subsequent navigations.

## Before You Start

### Use agent-browser only for interaction
For reading or fetching web content, prefer standard web search and
fetch tools. Use agent-browser only when the task requires interaction:
clicking, form submission, or stateful navigation.

### Subagent safety gate
If running as a subagent, you MUST load the `testing-safety-protocol`
skill before using agent-browser. Only proceed if the protocol permits.
If it does not permit, stop and do not use agent-browser.

### --headed
- Primary agent (interactive session with user): always `--headed`
- Subagent: headless by default; use `--headed` only if explicitly instructed

## Prerequisites

If `agent-browser` is not installed, it is a system-level CLI tool. Load the `installing-dependencies` skill, inform the user what needs to be installed and where it writes, and wait for explicit permission before proceeding.

## Session

agent-browser keeps a single browser session. Cookies persist across `open` calls as long as the session is alive.

```bash
agent-browser session --json                   # Show current session name
agent-browser session list --json              # List all active sessions
```

### Opening a browser

```bash
# First open: reset any stale state, then set a consistent viewport
agent-browser close && agent-browser open https://example.com [--headed]
agent-browser set viewport 1920 1080

# Subsequent navigations: just open, cookies are preserved
agent-browser open https://example.com/dashboard [--headed]
```

`--headed` follows the decision in "Before You Start".

### Browser settings

```bash
agent-browser set viewport 1920 1080                         # Viewport size
agent-browser set media dark                                 # Dark mode
agent-browser set media light                                # Light mode
agent-browser set headers '{"Accept-Language": "en-US"}'    # Request headers
```

### Closing the session

`close` destroys the session and deletes all cookies. Only use it when you want a completely fresh start or are fully done with the task. After closing, any authenticated site will require re-login.

```bash
agent-browser close
```

## Snapshot

Snapshot returns the current page's interactive elements, each assigned a reference handle (`@e1`, `@e2`, ...). Always take a fresh snapshot before interacting, and re-snapshot whenever the page content changes (navigation, modal open/close, AJAX update).

```bash
agent-browser snapshot -i --json               # Get interactive elements with @refs
```

## Interaction

All interaction commands use `@ref` handles from the most recent snapshot.

```bash
agent-browser click @e1                        # Click element
agent-browser fill @e2 "text"                  # Clear field and fill with text
agent-browser type @e2 "text"                  # Type into field without clearing first
agent-browser press Enter                      # Press a keyboard key
agent-browser select @e3 "option-value"        # Select a dropdown option
agent-browser check @e4                        # Check a checkbox
agent-browser hover @e5                        # Hover over element
agent-browser scroll down 500                  # Scroll page by pixels
```

### Cookie banners

After opening any public-facing page, check for a cookie consent banner and dismiss it before proceeding - unless the user explicitly asks to leave it for debugging.

```bash
agent-browser snapshot -i --json               # Check if cookie banner is present
agent-browser click @eX                        # Click "Accept" / "Accept all" (use correct @ref)
```

## Navigation

```bash
agent-browser open https://example.com         # Navigate to URL (session and cookies preserved)
agent-browser back                             # Go back in history
agent-browser forward                          # Go forward in history
agent-browser reload                           # Reload current page
```

## Waiting

```bash
agent-browser wait @e1                         # Wait until element exists in DOM
agent-browser wait 2000                        # Wait fixed milliseconds (use sparingly)
agent-browser wait --text "Success"            # Wait until text appears on page
```

Prefer `wait @ref` or `wait --text` over a fixed-time wait - they resolve as soon as the condition is met and fail fast if it never arrives.

## Extracting Data

```bash
agent-browser get text @e1 --json             # Text content of element
agent-browser get value @e2 --json            # Current value of an input
agent-browser get html @e1 --json             # Outer HTML of element
agent-browser get attr data-id @e1 --json     # Attribute value
agent-browser get title --json                # Page title
agent-browser get url --json                  # Current URL
agent-browser get box @e1 --json              # Bounding box (x, y, width, height)
```

### Reading page text

```bash
agent-browser eval "document.body.innerText.split('\n').slice(0, 80).join('\n')"
```

## Screenshots

Always save to `/tmp/agent-screenshots/` to avoid polluting the project directory. Replace `YYYYMMDD-HHMMSS` with the actual timestamp (e.g. `20260220-143000`).

```bash
mkdir -p /tmp/agent-screenshots
agent-browser screenshot /tmp/agent-screenshots/YYYYMMDD-HHMMSS-description.png
agent-browser screenshot /tmp/agent-screenshots/YYYYMMDD-HHMMSS-description.png --full
```

## DevTools

### Console and errors

`console` captures all log levels (log, warn, error, debug). `errors` is a subset showing only page errors.

```bash
agent-browser console --json                  # All console output
agent-browser console --clear                 # Clear the console buffer
agent-browser errors --json                   # Page errors only
```

### Cookies and storage

```bash
agent-browser cookies get --json              # All cookies for current session
agent-browser cookies clear                   # Delete all cookies
agent-browser storage local --json            # localStorage contents
agent-browser storage session --json          # sessionStorage contents
```

### Network

```bash
agent-browser network requests --json         # All captured network requests
agent-browser network requests --filter "api" --json   # Filter by URL substring
agent-browser network requests --clear        # Clear the request buffer
agent-browser network route "*/api/*" --abort          # Block matching requests
agent-browser network route "*/api/*" --body '{"mock":true}'  # Mock a response
agent-browser network unroute                 # Remove all route rules
```

### JavaScript evaluation

```bash
agent-browser eval "window.location.href"            # Read a value from the page
agent-browser eval "localStorage.getItem('token')"   # Inspect storage
agent-browser eval "document.title"                  # Any JS expression
```

## Authentication

For form-based login:

```bash
agent-browser open https://example.com/login [--headed]
agent-browser snapshot -i --json
agent-browser fill @eUsername "user@example.com"
agent-browser fill @ePassword "secret"
agent-browser click @eSubmit
# Cookies are saved automatically - future open calls stay authenticated
```

For token-based APIs or localized content, inject headers before navigating:

```bash
agent-browser set headers '{"Authorization": "Bearer <token>"}'
agent-browser set headers '{"Accept-Language": "zh-CN"}'
agent-browser open https://example.com/api/resource [--headed]
```

## Debugging

```bash
agent-browser highlight @e1                   # Visually highlight an element in the browser
agent-browser trace start                     # Begin recording a Playwright trace
agent-browser trace stop /tmp/trace.zip       # Save trace for inspection
```

### Recovery when browser stops responding

`pkill` loses all cookies. After recovery, re-login to any authenticated sites.

```bash
pkill -x agent-browser
sleep 5
agent-browser open https://example.com --headed
agent-browser set viewport 1920 1080
```
