---
name: tmux-guide
description: |
    Tmux skill for running background tasks.
    Use this skill when:
    1. Before any tasks that can potentially run for more than 2 minutes (e.g.: package install, many tests, model training)
    2. Before any tasks that are expected to run indefinitely in background (e.g.: web servers, port forwarding)
    3. Bash tool reports `timeout after 120000ms`
    4. User request to run tasks in background
---
# Tmux guidelines

Use `tmux` for any tasks run for more than 2 minutes or run indefinitely.

Examples are: package install, many tests, web servers, port forwarding, dataset pipeline, model training.

If bash tool reports `timeout after 120000ms`:
- This means the task you are running is expected to run for more than 2 minutes.
- Must use `tmux` for running this task.

## New session

```bash
tmux new-session -d -s agent-<task name> bash -c 'cd /path/to/project && <command to run>; echo "Process exited with $?"; sleep infinity'
```

**IMPORTANT:**
- ALWAYS name sessions with the `agent-` prefix.
- ALWAYS use `bash -c '...'` to encapsulate.
- ALWAYS use `cd /path/to/project` before running command.
- ALWAYS use `echo "Process exited with $?"; sleep infinity` after running command.

## List sessions

```bash
tmux ls | grep agent-
```

**IMPORTANT:**
- ALWAYS use `| grep agent-` to show agent created sessions only.

## Capture pane

Fetch the last 80 log lines for a task without attaching (returns immediately):

```bash
tmux capture-pane -t agent-vite-dev -S -80 -p
```

**IMPORTANT:**
- NEVER attach to a session.

## Clean up

Please clean up agent session after process exited:

```bash
tmux kill-session -t agent-vite-dev
```

**IMPORTANT:**
- NEVER kill-server.
- NEVER kill any sessions without `agent-` prefix.
