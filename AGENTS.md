# User Preferences

- DO NOT use **Unicode hyphen** `‑` (U+2011); Use **ASCII hyphen** `-` (U+002D)
- Always respond in **Chinese**
- Write code comments and documentation in **English**

## CLI Tools

- Use bash **heredoc** syntax for one-off scripts (e.g., `python <<EOF ... EOF`)
- Use `uv` for Python tasks; if not installed, fallback to `python` and `pip`

## Coding Style

- For **fresh projects** (newly created, seemingly empty): use **4 spaces** for indent
- For **existing projects**: detect existing style first by checking:
  - Styling config files (`.editorconfig`, `pyproject.toml`, `.stylua.json`, `.clang-format`, etc.)
  - Existing code indentation patterns
  - Then follow the detected style
