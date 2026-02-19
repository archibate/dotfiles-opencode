## High-Level Concepts

- Design for humans first: make the common path easy, and mistakes easy to recover from.
- Keep tools composable: work well with pipes, files, and other commands.
- Be consistent: names, flags, defaults, and behaviors should match across commands.
- Make it discoverable: strong --help, good examples, and clear error messages.
- Keep I/O clean: data to stdout; errors/logs/progress to stderr; meaningful exit codes.
- Be safe and predictable: sensible defaults, avoid surprise prompts, make destructive actions explicit.
- Be robust: handle non-interactive use, signals, partial failures, and change over time.

## Framework To Apply To Your Scripts

- Write the “contract” first: inputs (args/flags/config/env), outputs (human vs machine), and exit codes.
- Validate early; fail fast with one clear, actionable error message.
- Design output intentionally: default human-readable; add a machine mode like --json; keep stdout pipe-friendly.
- Define interaction rules: only prompt on TTY; support --yes/--no-input; make CI behavior stable.
- Add reliability basics: timeouts/retries where needed, atomic writes, and cleanup on Ctrl‑C.
- Treat it like a product: --help/--version, a few examples, and a small set of “golden” tests for output/help.

## Language Notes

- Python: use argparse (stdlib) or typer; write to stdout/stderr intentionally; return real exit codes.
- TypeScript: use commander/yargs; check process.stdout.isTTY; keep stdout/stderr separated; set process.exitCode.
- Bash: keep it small; use getopts, strict quoting, trap for cleanup, and avoid noisy stdout so piping stays reliable.
