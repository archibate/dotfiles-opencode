---
name: writing-bash-scripts
description: Create and refactor Bash scripts following conventions (strict mode, fct_ naming, quoting). Includes shellcheck linting. Use when creating shell scripts, refactoring existing scripts, debugging shell errors, or linting scripts.
---

# Bash

Use this skill whenever the user asks to create/update/refactor a Bash script (`.sh`) or lint shell scripts.

## Defaults

- Shebang: `#!/usr/bin/env bash`
- Strict mode: `set -Eeuo pipefail`
- Functions: `fct_<descriptive_snake_case>() { ... }`
- Variables: quote expansions like `"${var}"`, prefer `printf`, use `readonly` for constants and `local` inside functions

## Workflow

### Creating/Refactoring Scripts

1. Copy `scripts/pref_bash_script_template.sh` to the target path and rename it.
2. Update the SCRIPT INFO / USAGE header blocks.
3. Implement behavior in `fct_execute_this`, keep `fct_main` + `trap` structure.
4. Follow the detailed conventions in `references/pref_bash.md`.
5. Run shellcheck linting (see below).

### Linting Scripts

Run shellcheck on scripts using the provided wrapper:

```bash
# Lint all scripts in scripts/ directory (default)
.opencode/skill/bash/scripts/run_shellck.sh

# Lint specific files or directories
.opencode/skill/bash/scripts/run_shellck.sh path/to/script.sh
.opencode/skill/bash/scripts/run_shellck.sh scripts/ other/dir/
```

The linting script:

- Automatically detects shell scripts by extension (`.sh`, `.bash`, `.zsh`) or shebang
- Exits non-zero on shellcheck failures
- Defaults to scanning `scripts/` when no arguments provided

See `references/pref_bash.md` section 14 for shellcheck integration details.
