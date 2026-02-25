# User Preferences

- DO NOT use **Unicode hyphen** `‑` (U+2011); Use **ASCII hyphen** `-` (U+002D)
- Always respond in **Chinese**
- Write code comments and documentation in **English**

## CLI Tools

- Use `uv` for Python tasks; if not installed, fallback to `python` and `pip`

## Coding Style

- For **fresh projects** (newly created, seemingly empty): use **4 spaces** for indent
- For **existing projects**: detect existing style first by checking:
  - Styling config files (`.editorconfig`, `pyproject.toml`, `.stylua.json`, `.clang-format`, etc.)
  - Existing code indentation patterns
  - Then follow the detected style

## Project Structure

- Make sure `git status` shows no garbage files; update `.gitignore` accordingly
- Write one-off analyzation scripts to `/tmp` folder; do not pollute project follder
- Use setup-fresh-project skill to getting started on an empty project

## Background Tasks

Use the PTY tools when:
1. Before any tasks that can potentially run for more than 2 minutes (e.g.: package install, many tests, model training)
2. Before any tasks that are expected to run indefinitely in background (e.g.: web servers, port forwarding)
3. Bash tool reports `timeout after 120000ms`
4. User request to run tasks in background

PTY tools are available as `pty_*`.
