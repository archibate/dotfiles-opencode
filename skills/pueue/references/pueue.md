# Pueue CLI References

## Overview

Pueue is a daemon-based task queue manager. The daemon (`pueued`) runs persistently; `pueue` is the client CLI.

## Daemon Setup

```bash
# Start daemon (if not already running via systemd)
pueued -d

# Check if running (errors if daemon is down)
pueue status

# Shut down daemon
pueue shutdown
```

Systemd (optional):
```bash
systemctl --user enable --now pueued
systemctl --user status pueued
```

## Adding Tasks

Always pass the full command as a **single quoted string**. This preserves quoting, env var prefixes, and shell operators exactly as written.

```bash
# Basic
pueue add 'uv run python -u train.py'

# Env var prefix — must be inside the quoted string
pueue add 'PYTHONUNBUFFERED=1 uv run src/train.py'

# Shell pipeline or &&
pueue add 'cmd1 | cmd2'
pueue add 'step1.sh && step2.sh'

# Print only the new task ID (useful for scripting)
pueue add -p 'uv run python -u train.py'

# With label
pueue add -l 'training-run' 'uv run python -u train.py'

# With working directory
pueue add -w /path/to/project './run.sh'

# Start immediately (bypass queue)
pueue add -i 'uv run python -u quick_check.py'

# Stash (don't start automatically)
pueue add -s 'uv run python -u heavy_job.py'
pueue start <id>  # start manually later
```

## Dependencies

```bash
# Run after task 3 completes
pueue add --after 3 -- python step2.py

# Run after tasks 3 AND 4 both complete
pueue add --after 3 --after 4 -- python final.py
```

## Status & Output

```bash
# Human-readable status
pueue status

# JSON output (for parsing)
pueue status --json

# Follow a running task (like tail -f, blocks until complete)
pueue follow <id>

# View completed task output
pueue log <id>
pueue log <id> --json     # JSON output
pueue log <id> -f         # full output (not truncated)
pueue log <id> -l 100     # last 100 lines
```

## Task Control

```bash
pueue pause <id>          # pause a task
pueue start <id>          # resume or start a stashed task
pueue kill <id>           # kill a running task
pueue remove <id>         # remove a task (must not be running)
pueue restart <id>        # re-queue a finished/failed task

pueue pause               # pause entire default group
pueue start               # resume entire default group
```

## Cleanup

```bash
pueue clean               # remove all finished/failed tasks
pueue clean -s            # remove only successful tasks
pueue clean -g <group>    # clean specific group only
```

## Groups & Concurrency

Groups allow separate queues with independent concurrency limits.

```bash
# Create a group with concurrency limit
pueue group add gpu -p 1      # max 1 parallel task in "gpu" group
pueue group add cpu -p 4      # max 4 parallel tasks in "cpu" group
pueue group                   # list all groups
pueue group --json            # JSON output

# Assign task to group
pueue add -g gpu -- python train.py

# Change concurrency limit later
pueue parallel -g gpu 2
pueue parallel 0              # 0 = unlimited (default group)
```

## Programmatic Usage Patterns

### Queue a pipeline with dependencies
```bash
id1=$(pueue add -p 'uv run python -u preprocess.py')
id2=$(pueue add -p --after $id1 'uv run python -u train.py')
pueue add --after $id2 'uv run python -u evaluate.py'
```

### Check exit code of finished task
```bash
pueue status --json | jq ".tasks.\"$id\".result"
# Returns: "Success", {"Failed": <exit_code>}, "Killed", etc.
```

## Key Pitfalls

- Always pass the full command as a single quoted string: `pueue add 'cmd --flag'` — never `pueue add -- cmd --flag`
- Python tasks MUST use `-u` flag or `PYTHONUNBUFFERED=1` prefix for real-time output (otherwise appears stuck): `pueue add 'PYTHONUNBUFFERED=1 uv run src/train.py'`
- Use `-g` with project name to avoid mixing tasks from different projects
- `--escape` disables shell syntax (no `&&`, pipes) — avoid for shell pipelines
- Task IDs are integers; quote them in `jq` with `.tasks.\"$id\"`
- `pueue clean` only removes finished tasks — running tasks are unaffected
