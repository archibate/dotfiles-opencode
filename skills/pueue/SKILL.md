---
name: pueue
description: This skill should be used before running non-interactive long-running tasks, computation intensive tasks, background tasks, or needs guidance on the pueue CLI tool usage. TRIGGER when user says "use pueue", "run in background", "queue this task", or when about to run any long-running (>2 min) task.
---

# Pueue - Background Task Manager

## When to Use

- Non-interactive long-running tasks expected to run for >2 minutes
- Computation intensive tasks with parallel job scheduling (prevent resource exhaustion)
- Tasks that should continue even if you disconnect

## When NOT to Use

- Short tasks (<2 minutes): run directly
- Interactive commands: use `tmux` instead for TUI access

## Workflow

### Option 1: Add and Follow (Recommended)

Start task and follow its output (blocks until complete):

```bash
# Add task and get its ID
pueue add 'PYTHONUNBUFFERED=1 uv run python -u train.py'

# Follow task output (blocks until complete)
pueue follow <task_id>
```

### Option 2: Add and Check Later

Start task without blocking, check status later:

```bash
# Add task
pueue add 'PYTHONUNBUFFERED=1 uv run python -u train.py'

# Later, check status
pueue status

# View output when done
pueue log <task_id>
```

### Option 3: Using the Helper Script

```bash
scripts/run_in_pueue.sh 'PYTHONUNBUFFERED=1 uv run python -u train.py'
```

This script:
- Auto-starts daemon if needed
- Creates a project-specific group
- Adds the task and follows output

## Conversation Example

User:
Start training in the background.

Assistant:
```bash
pueue add 'PYTHONUNBUFFERED=1 uv run python -u train.py'
```

Then I'll follow the output:
```bash
pueue follow <task_id>
```

Training started. I'll monitor progress and report when complete.

## Quick Reference

| Command | Description |
|---------|-------------|
| `pueue status` | List all tasks |
| `pueue add 'cmd'` | Queue a task |
| `pueue follow <id>` | Follow task output (blocks) |
| `pueue log <id>` | View completed task output |
| `pueue kill <id>` | Kill a running task |
| `pueue clean` | Remove finished tasks |

## Key Pitfalls

- **Always quote the command**: `pueue add 'cmd --flag'` not `pueue add -- cmd --flag`
- **Python needs unbuffered output**: Use `PYTHONUNBUFFERED=1` or `python -u`
- **Use project groups**: `pueue add -g myproject 'cmd'` to avoid mixing tasks

## Skill Files

- `scripts/run_in_pueue.sh` — wraps pueue add with auto daemon start, per-project grouping, and follow
- `references/pueue.md` — comprehensive pueue CLI usage documentation
