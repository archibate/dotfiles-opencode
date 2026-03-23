---
name: pueue
description: TRIGGER when user mentioned "pueue", "in background". TRIGGER when running non-interactive long-running tasks run for >2 minutes, or any computation intensive tasks.
---

# Pueue

## Overview

Pueue is a daemon-based task queue manager. The daemon (`pueued`) runs persistently; `pueue` is the client CLI.

## When to Use

- Non-interactive long-running tasks expected to run for >2 minutes
- Computation intensive tasks with parallel job scheduling (prevent resource exhaustion)

## When NOT to Use

- Short tasks (<2 minutes): run in Bash directly
- Interactive commands: `tmux` instead for TUI access

## Workflow

- `pueue status` to check if daemon is started, start with `pueued -d`
- Create a group for current project using `pueue group add -p 4 [project-name]` if not exist yet
    - `-p 4` means allow up to 4 jobs to run concurrently in this group: prevent system resource exhaustion in CPU, memory, I/O
- Use `pueue add -g [project-name] -- "uv run python -u src/train.py"` to start task in background
    - Important: Python tasks MUST add the option `-u` or set environment `PYTHONUNBUFFERED=1` for real-time output (otherwise would appear stuck)
- Start `pueue follow [task id]` to wait for task complete

---

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

```bash
# Basic
pueue add 'python train.py'

# Use -- when command has its own flags
pueue add -- python train.py --epochs 100

# Print only the new task ID (useful for scripting)
pueue add -p 'python train.py'

# With label
pueue add -l 'training-run' -- python train.py

# With working directory
pueue add -w /path/to/project -- ./run.sh

# Start immediately (bypass queue)
pueue add -i -- python quick_check.py

# Stash (don't start automatically)
pueue add -s -- python heavy_job.py
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

# Follow a running task (like tail -f)
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
id1=$(pueue add -p -- python preprocess.py)
id2=$(pueue add -p --after $id1 -- python train.py)
pueue add --after $id2 -- python evaluate.py
```

### Poll task completion
```bash
while true; do
    state=$(pueue status --json | jq -r ".tasks.\"$id\".status")
    [ "$state" = "Done" ] || [ "$state" = "Failed" ] && break
    sleep 5
done
```

### Check exit code of finished task
```bash
pueue status --json | jq ".tasks.\"$id\".result"
# Returns: "Success", {"Failed": <exit_code>}, "Killed", etc.
```

## Key Pitfalls

- Always use `--` before commands that have their own flags: `pueue add -- ls -al`
- Wrap shell pipelines in quotes: `pueue add 'cmd1 | cmd2'`
- `--escape` disables shell syntax (no `&&`, pipes) — avoid for shell pipelines
- Task IDs are integers; quote them in `jq` with `.tasks.\"$id\"`
- `pueue clean` only removes finished tasks — running tasks are unaffected
- Not using `-g` with project name falls back to the `default` group
