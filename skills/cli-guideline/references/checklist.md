# CLI Stress Checklist

Replace `<cmd>` with your command. Mark: PASS / FAIL / N/A.

## Setup

- Command under test: `<cmd>`
- Known-success invocation: `<cmd> ...`
- Known-failure invocation: `<cmd> ...`
- Piped invocation (if applicable): `echo "..." | <cmd> ...`

Helpers:

- Split streams: `<cmd> ... >out.txt 2>err.txt`
- Exit code: `echo $?`
- Non-interactive stdin: `<cmd> ... </dev/null`

---

## 1. The Basics

- [ ] 1.1 Uses argument parser (not ad-hoc). `--help`, unknown flags → consistent errors
- [ ] 1.2 Exit `0` on success
- [ ] 1.3 Exit non-zero on failure
- [ ] 1.4 Primary output → stdout
- [ ] 1.5 Messages/logs/errors → stderr

## 2. Help

- [ ] 2.1 `-h` and `--help` show full help (exit 0)
- [ ] 2.2 Help ignores other args (`--badflag -h` → help, not error)
- [ ] 2.3 Subcommands have own help
- [ ] 2.4 `help` subcommand works (if git-like)
- [ ] 2.5 Missing required args → concise help (not stack trace, not hang)
- [ ] 2.6 Includes support path (URL/instructions)
- [ ] 2.7 Leads with examples
- [ ] 2.8 Suggests fixes on typos ("Did you mean...?")
- [ ] 2.9 Doesn't hang when expecting piped input on TTY

## 3. Documentation

- [ ] 3.1 Web docs linked from help
- [ ] 3.2 Terminal docs complete (works offline)
- [ ] 3.3 Man page considered (optional)

## 4. Output

- [ ] 4.1 Human output readable in terminal
- [ ] 4.2 Pipe-friendly (no progress/spinners in stdout)
- [ ] 4.3 `--plain` for stable tabular output
- [ ] 4.4 `--json` for structured output (valid JSON only)
- [ ] 4.5 Success output brief
- [ ] 4.6 `-q`/`--quiet` suppresses non-essential output
- [ ] 4.7 State changes reported ("did X to Y")
- [ ] 4.8 Current state viewable (status/list/show)
- [ ] 4.9 Suggests next commands
- [ ] 4.10 Explicit about boundary crossing (files/network)
- [ ] 4.11 Color intentional, not decorative
- [ ] 4.12 Color disables: `NO_COLOR=1`, `TERM=dumb`, `--no-color`
- [ ] 4.13 No animations when stdout not TTY
- [ ] 4.14 No debug noise by default
- [ ] 4.15 stderr not log-file formatted by default
- [ ] 4.16 Pager for long output (optional)

## 5. Errors

- [ ] 5.1 Errors rewritten for humans (what + how to fix)
- [ ] 5.2 High signal-to-noise (grouped, not spam)
- [ ] 5.3 Important info easy to spot (near end)
- [ ] 5.4 Unexpected errors have debug path
- [ ] 5.5 Bug reports easy (URL + what to include)

## 6. Arguments & Flags

- [ ] 6.1 Prefers flags over many positional args
- [ ] 6.2 Full-length flags for everything
- [ ] 6.3 One-letter flags for common options only
- [ ] 6.4 Multiple file args work for bulk actions
- [ ] 6.5 Avoids multiple positional args for different concepts
- [ ] 6.6 Standard flag names used
- [ ] 6.7 Sensible defaults
- [ ] 6.8 Prompts for missing input (TTY only)
- [ ] 6.9 Never requires prompt (fails fast with flag hint)
- [ ] 6.10 Confirms dangerous actions
- [ ] 6.11 `--dry-run` for risky actions
- [ ] 6.12 `-` for stdin/stdout
- [ ] 6.13 Optional flag values allow `none`
- [ ] 6.14 Flags/subcommands order-independent
- [ ] 6.15 No secrets via flags (use `--password-file` or stdin)

## 7. Interactivity

- [ ] 7.1 Prompts only when stdin is TTY
- [ ] 7.2 `--no-input` disables prompts
- [ ] 7.3 Password prompts don't echo
- [ ] 7.4 Ctrl-C exits cleanly
- [ ] 7.5 Escape documented if Ctrl-C can't quit

## 8. Subcommands

- [ ] 8.1 Consistent flags across subcommands
- [ ] 8.2 Consistent naming (noun/verb pattern)
- [ ] 8.3 No ambiguous command names

## 9. Robustness

- [ ] 9.1 Validates input early
- [ ] 9.2 Responsive (<100ms feedback)
- [ ] 9.3 Progress for long operations
- [ ] 9.4 Logs visible on error (even with progress UI)
- [ ] 9.5 Parallel work doesn't garble output
- [ ] 9.6 Network calls timeout (configurable)
- [ ] 9.7 Recoverable on rerun
- [ ] 9.8 Crash-only (no manual cleanup)
- [ ] 9.9 Handles misuse (scripts, bad networks, concurrent)

## 10. Future-Proofing

- [ ] 10.1 Interfaces treated as contracts
- [ ] 10.2 Changes additive when possible
- [ ] 10.3 Deprecations warn users
- [ ] 10.4 Stable output modes documented (`--plain`/`--json`)
- [ ] 10.5 No catch-all default subcommand
- [ ] 10.6 No arbitrary abbreviations
- [ ] 10.7 No time bombs (external dependencies)

## 11. Signals

- [ ] 11.1 Ctrl-C exits quickly
- [ ] 11.2 Cleanup can't hang forever
- [ ] 11.3 Second Ctrl-C behavior clear

## 12. Configuration

- [ ] 12.1 Right config mechanism (flags/env/files)
- [ ] 12.2 XDG base dirs for user config
- [ ] 12.3 Never silently edits other programs' config
- [ ] 12.4 Precedence: flag > env > project > user > system

## 13. Environment Variables

- [ ] 13.1 Env vars for context, not everything
- [ ] 13.2 Names portable (`UPPERCASE_UNDERSCORES`)
- [ ] 13.3 Single-line values
- [ ] 13.4 Doesn't steal common names
- [ ] 13.5 Respects `NO_COLOR`, `DEBUG`, `EDITOR`, proxies, `PAGER`, etc.
- [ ] 13.6 Reads `.env` for project context
- [ ] 13.7 No secrets from env vars

## 14. Naming

- [ ] 14.1 Simple, memorable name
- [ ] 14.2 Lowercase, dashes if needed
- [ ] 14.3 Short but not cryptic

## 15. Distribution

- [ ] 15.1 Installation clear, minimal
- [ ] 15.2 Uninstall easy, documented

## 16. Analytics

- [ ] 16.1 No telemetry without consent
- [ ] 16.2 Collection transparent
- [ ] 16.3 Alternatives considered

---

## Language-Specific

### Python

- [ ] 17.1 Entry point returns exit code
- [ ] 17.2 Uses real CLI parser (`argparse`/`click`/`typer`)
- [ ] 17.3 No tracebacks for expected errors
- [ ] 17.4 Debug path for unexpected errors
- [ ] 17.5 Ctrl-C clean (exit 130, no traceback)
- [ ] 17.6 Separate TTY detection for stdout/stderr
- [ ] 17.7 `--json` output is valid JSON only
- [ ] 17.8 No secrets via flags

### TypeScript/Node

- [ ] 18.1 Uses real CLI parser
- [ ] 18.2 stdout for data, stderr for messages
- [ ] 18.3 Async failures handled predictably
- [ ] 18.4 Debug mode with stack traces
- [ ] 18.5 Avoids premature `process.exit()`
- [ ] 18.6 Separate TTY detection
- [ ] 18.7 Respects `--no-input`
- [ ] 18.8 `--json` output is valid JSON only

### Bash

- [ ] 19.1 Shebang matches features
- [ ] 19.2 Flags parsed robustly
- [ ] 19.3 Quotes/whitespace handled
- [ ] 19.4 stdout/stderr correct
- [ ] 19.5 Prompts only on TTY
- [ ] 19.6 Ctrl-C/cleanup safe (`trap`, `mktemp`)
- [ ] 19.7 Avoids shell footguns
- [ ] 19.8 Lints clean (`shellcheck`)
