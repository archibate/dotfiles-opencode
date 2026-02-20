---
name: interactive-test
description: |
    Use this skill before testing interactive applications (GUI/TUI).
---

# Interactive Application Test Guide

Use this skill when testing interactive applications.

This skill does not apply to non-interactive applications.

## CRITICAL RULES

**IMPORTANT:**
- You are a **CLI agent**.
- You run in **terminals** by default.
- You have NO ability to manipulate GUI directly.
- NEVER start **non-headless GUI applications** without user permission - an accidental popup window will confuse and annoy the human user.

## Testing GUI Applications

GUI Application typically requires interactive test which is not available from terminal.

Heres are the common solutions:

- Web-based GUI (e.g. Vite, Vue, React):
    - If the project offers standard non-interactive test suite (e.g. `vite test`), run that first.
    - If non-interactive test passed:
        - Check if its necessary for interactive test.
        - Use browser automation tools for headless interactive test.
        - Capture screenshot using browser automation tools, then read saved image for vision analysis (if the agent have vision capbility).

- Traditional local GUI (e.g. Qt, Pygame):
    - If the project offers standard unit tests for non-interactive functionalities, run that first.
    - For e2e test with GUI running:
        - Must ask human user for manual test.

### Browser Automation Tools

- `playwright`
- `chrome-dev-tools`
- `agent-browser`

## Testing TUI Applications

TUI Applications typically interacts with terminal key strokes.

The builtin `bash` tool does not allow interactive TTY/PTY.

Use the `tmux-guide` skill for starting TUI applications in PTY and send key strokes.
