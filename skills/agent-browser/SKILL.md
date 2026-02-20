---
name: agent-browser
description: Use this skill for browser automation.
---

# Browser Automation with agent-browser
## HOW IT WORKS
agent-browser maintains its own browser session with cookies.
- Login once → cookies saved → stay authenticated for future navigations
- **WARNING: `agent-browser close` DELETES ALL COOKIES** - you will need to re-login!
- To keep authentication: NEVER close the session, just navigate to new URLs
## WORKFLOW
### 1. Open Browser (MUST use this pattern)
```bash
# ALWAYS use this on first open - sets viewport to 1920x1080:
agent-browser close && agent-browser open <url> --headed && agent-browser set viewport 1920 1080
# If browser already running, just navigate:
agent-browser open <url> --headed
```
### 2. Handle Cookie Banner (MUST DO on public sites)
After opening a page, ALWAYS:
1. Run `agent-browser snapshot -i` to check for cookie consent banner
2. If cookie banner present: click "Accept" / "Accetta" / "Accept all" button
3. Unless user explicitly asks to keep it open (for development/debugging)
```bash
agent-browser snapshot -i                     # Look for cookie banner
agent-browser click @eX                       # Click accept button (use correct @ref)
```
### 3. Analyze Page
```bash
agent-browser snapshot -i                     # Get interactive elements with @refs
agent-browser snapshot -i -c                  # Compact output
```
### 4. Interact (use @refs from snapshot)
```bash
agent-browser click @e1                       # Click element
agent-browser fill @e2 "text"                 # Clear and fill input
agent-browser type @e2 "text"                 # Type without clearing
agent-browser press Enter                     # Press key
agent-browser select @e1 "value"              # Select dropdown
agent-browser scroll down 500                 # Scroll page
agent-browser hover @e1                       # Hover element
agent-browser check @e1                       # Check checkbox
```
### 5. Get Information
```bash
agent-browser get text @e1                    # Element text
agent-browser get value @e1                   # Input value
agent-browser get html @e1                    # Element HTML
agent-browser get attr data-id @e1            # Element attribute
agent-browser get title                       # Page title
agent-browser get url                         # Current URL
agent-browser get box @e1                     # Element bounding box
```
### 6. Navigate
```bash
agent-browser open <url>                      # Go to URL (keeps cookies!)
agent-browser back                            # Go back
agent-browser forward                         # Go forward
agent-browser reload                          # Reload page
```
### 7. Wait
```bash
agent-browser wait @e1                        # Wait for element
agent-browser wait 2000                       # Wait milliseconds
agent-browser wait --text "Success"           # Wait for text
```
### 8. Screenshots
```bash
mkdir -p /tmp/agent-screenshots
agent-browser screenshot /tmp/agent-screenshots/YYYYMMDD-HHMMSS-description.png
agent-browser screenshot /tmp/agent-screenshots/YYYYMMDD-HHMMSS-description.png --full
```
**IMPORTANT**: ALWAYS save screenshots in this exact format: `/tmp/agent-screenshots/YYYYMMDD-HHMMSS-description.png`.
## DEV TOOLS (ALWAYS USE --json)
### Console Logs (CRITICAL - always use --json!)
```bash
agent-browser console --json                  # View ALL console logs (log, warn, error, debug)
agent-browser console --clear                 # Clear console buffer
agent-browser errors --json                   # View page errors only
```
### Cookies & Storage
```bash
agent-browser cookies get --json              # Get all cookies
agent-browser cookies clear                   # Clear cookies
agent-browser storage local --json            # Get localStorage
agent-browser storage session --json          # Get sessionStorage
```
### Network Requests
```bash
agent-browser network requests --filter "" --json    # View captured requests
agent-browser network requests --clear               # Clear request buffer
agent-browser network route "*/api/*" --abort        # Block requests
agent-browser network route "*/api/*" --body '{"mock":true}'  # Mock response
agent-browser network unroute                        # Remove all routes
```
### Execute JavaScript
```bash
agent-browser eval "window.location.href"            # Run JS, get result
agent-browser eval "document.title"
agent-browser eval "localStorage.getItem('key')"
agent-browser eval "console.log('test')"             # Log to console
```
### Debug Helpers
```bash
agent-browser highlight @e1                   # Highlight element visually
agent-browser trace start                     # Start recording trace
agent-browser trace stop ./trace.zip          # Stop and save trace file
```
## RULES
1. **First open**: ALWAYS use the open+viewport pattern from section 1
2. **Cookie banner**: ALWAYS dismiss cookie banners on public sites (accept cookies), unless user asks to keep for debugging
3. **--headed**: Always use for `open` command (user must see browser) unless headless browser is instructed
4. **--json**: Always use for console, errors, cookies, storage, network
5. **snapshot before interact**: Always get fresh @refs before clicking/filling
6. **re-snapshot after navigation**: Page changes = new @refs
7. **screenshots**: Save to `.agent-screenshots/YYYYMMDD-HHMMSS-description.png`
8. **NEVER close session**: `close` deletes cookies = re-login required
## AUTHENTICATION
For sites requiring login:
1. Navigate to login page
2. Use `fill` for credentials, `click` for submit
3. Cookies are saved automatically
4. Future navigations stay authenticated
## BROWSER SETTINGS
```bash
agent-browser set viewport 1920 1080          # Viewport size
agent-browser set media dark                  # Dark mode
agent-browser set media light                 # Light mode
agent-browser set headers '{"Accept-Language": "it-IT"}'   # Italian
agent-browser set headers '{"Accept-Language": "en-US"}'   # English
```
## SESSION MANAGEMENT
```bash
agent-browser session list                    # List active sessions
agent-browser session                         # Current session name
```
**CRITICAL**: `agent-browser close` DESTROYS the session and ALL cookies!
- After close, you MUST re-login to authenticated sites
- To preserve auth: just navigate with `open <url>`, never close
- Only close when you're completely done OR want a fresh start
## TROUBLESHOOTING
**Browser not responding**:
```bash
pkill -x agent-browser                        # Kill daemon (loses cookies!)
sleep 5
agent-browser open <url> --headed             # Restart fresh (need re-login)
```
