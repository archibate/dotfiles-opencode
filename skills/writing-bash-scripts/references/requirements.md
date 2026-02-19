# Requirements from our Bash Script Template

## Goals

- Provide a universal Bash script template that is safe-by-default and easy to customize.
- Support common CLI flags (`--help`, `--verbose`, etc.) and clear self-documentation.
- Add reliable error handling (failed commands, pipelines, signals) with cleanup.
- Ensure portability across macOS (Darwin) and Linux without code changes.
- Ensure `shellcheck -x -o all` returns **zero** findings on the template.

## Non-Goals

- Implementing any specific “business logic” beyond a clearly-marked stub function.
- Adding CI/CD, pre-commit hooks, or repo-wide lint tooling (optional future work).
- Refactoring other skills or changing the skill trigger system in `AGENTS.md`.

## Requirements

### Functional requirements

- Shebang uses env Bash: `#!/usr/bin/env bash`.
- Strict mode uses `set -euo pipefail` with a brief “why” explanation for each flag.
- Script metadata exists (version, author, description) and is displayed by `--help/--version`.
- Dependency checking exists (a function to verify required commands exist).
- Argument parsing supports at least:
  - `-h` / `--help`
  - `-v` / `--verbose`
  - (recommended) `-V` / `--version`
  - (recommended) `--no-color` and `--log-file <path>`
- Logging functions exist with these names and behaviors:
  - `log_info`, `log_warn`, `log_error`, `log_debug`
  - Include timestamps
  - Colorized output to terminal (stderr) only when appropriate
  - Respect `NO_COLOR` (disable colors when set)
- Cleanup pattern exists:
  - `cleanup()` function
  - `trap cleanup EXIT`
  - Cleanup includes temp files/dirs and optional lock resources
- `die()` exists for fatal errors and supports explicit exit codes.
- Main pattern exists:
  - `main()` encapsulates execution
  - script ends by calling `main "$@"` only when executed directly
- Portable path resolution exists using `${BASH_SOURCE[0]}` to compute script directory.
- When sourced, the script must not auto-run `main` and must not `exit` the caller shell.

### Non-functional requirements

- Use `local` for function-scoped variables.
- Quote all variable expansions unless intentional splitting is required.
- Avoid unnecessary non-portable dependencies; keep macOS/Linux compatibility.
- Add short comments explaining “why” for each section (not only “what”).
- Must pass `shellcheck -x -o all .opencode/skill/bash/scripts/pref_bash_script_template.sh` with **zero** findings.
- Drop the existing Raycast header (template must be universal, not app-specific).

## Assumptions & Constraints

- The template is Bash (not POSIX `sh`) and uses `#!/usr/bin/env bash`.
- ShellCheck is available to developers implementing this plan; if not, they must install it before final validation.
- Repository conventions for Bash scripts (function prefix `fct_`, quoting, `printf`) are documented and must be respected where they do not conflict with the user requirements:
  - `.opencode/skill/bash/SKILL.md`
  - `.opencode/skill/bash/references/pref_bash.md`

### CLI contract

- `-h`, `--help`: print `usage()` to stdout and exit 0.
- `-V`, `--version`: print version line and exit 0.
- `-v`, `--verbose`: enable debug logs (`log_debug` outputs).
- `--no-color`: disable colored output (also respect pre-set `NO_COLOR`).
- `--log-file PATH`: append plain (non-colored) logs to PATH; error if not writable.
- `--`: stop option parsing; all remaining args are positional.

### Environment contract

- `NO_COLOR`: when set (any value), disable colored terminal output.
- `TMPDIR`: if set, use as base directory for `mktemp -d`; otherwise default to `/tmp`.

### Output contract

- Logs go to stderr (human-readable, optionally colorized).
- Stdout is reserved for command outputs or machine-readable results (template uses stdout for `--help/--version`).

### Exit codes

- `0`: success.
- `1`: general failure (default for `die` when no explicit code is provided).
- `2`: CLI usage/argument error (unknown option, missing option arg).
- `4`: missing dependency (required command not found).
- `130`: interrupted by SIGINT.
- `143`: terminated by SIGTERM.
- On unexpected command failure under strict mode: exit with the failing command’s status (via `ERR` trap).

## Verification Checklist

- [ ] Template contains required metadata and `usage()` block.
- [ ] `set -euo pipefail` exists with explanation comments.
- [ ] `log_info`, `log_warn`, `log_error`, `log_debug` exist and include timestamps.
- [ ] Colors are disabled when `NO_COLOR` is set and never written to `--log-file`.
- [ ] `cleanup()` runs on normal exit, error exit, and Ctrl+C.
- [ ] Unknown options return exit code 2 with an error message.
- [ ] Script does not auto-run and does not `exit` when sourced.
- [ ] ShellCheck reports zero findings with `-x -o all`.

## Completeness Audit

- Verified the target template path exists: `.opencode/skill/bash/scripts/pref_bash_script_template.sh`.
- Verified repo Bash conventions and workflow docs exist: `.opencode/skill/bash/SKILL.md`, `.opencode/skill/bash/references/pref_bash.md`.
- Extracted requirements from the repo task prompt: `INSTRUCT/instruct_v15.md`.
- Defined explicit CLI, environment, logging, and exit-code contracts.
- Included ShellCheck command and common pitfalls to avoid (to reach zero findings).
- Included manual verification scenarios: no args, `--help`, mid-execution failure, SIGINT, sourced vs executed.
