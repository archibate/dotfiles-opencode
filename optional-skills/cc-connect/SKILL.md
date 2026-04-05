---
name: cc-connect
description: >
  This skill should be used when sending images, files, or notifications back to the user via messaging platforms (Discord, Feishu, Telegram, etc.) through cc-connect.
  TRIGGER when agent generates a plot/chart/screenshot and wants to show the user; agent creates a report/PDF/file the user should receive; agent needs to proactively notify the user (e.g. task completed, alert, reminder); user asks to "send image", "show me the chart", "notify me", "send the file", "send to Telegram", "show plot in Discord".
version: 0.1.0
---

# cc-connect: Send Images, Files, and Notifications

## Purpose

Claude Code cannot send images or files back to users. The terminal output
is text-only. cc-connect bridges this gap by providing a `send` command
that delivers images, files, and text notifications directly through
messaging platforms (Discord, Feishu, Telegram, etc.).

### When to use

- **Send generated charts/plots** — matplotlib, plotly, seaborn, etc.
- **Send screenshots** — captured via agent-browser or other tools
- **Send reports/files** — PDFs, CSVs, logs, any artifact to transfer
- **Proactive notifications** — task completed, long job done, alerts
- **Send links** — share URL links to user (easier to click)

### When NOT to use

- **Short text report** — response directly
- **Service not available** — skip this skill if cc-connect daemon not running

## Commands

All commands use `cc-connect send` with different flags.

### Send an Image

```bash
cc-connect send --image /absolute/path/to/image.png -p <project> -m "Description"
```

- Repeat `--image` for multiple images in one message.
- Supported formats: PNG, JPG, JPEG, GIF.
- Always use absolute paths.

### Send a File

```bash
cc-connect send --file /absolute/path/to/report.pdf -p <project> -m "Description"
```

- Repeat `--file` for multiple files.
- Works with any file type: PDF, CSV, ZIP, etc.

### Send a Text Notification

```bash
cc-connect send -m "Task completed successfully" -p <project>
```

- For long or multi-line messages, use heredoc:

```bash
cc-connect send --stdin -p <project> <<'EOF'
Build completed!
- Tests: PASS
- Coverage: 87%
EOF
```

### Combine Image + File + Message

```bash
cc-connect send --image /path/to/chart.png --file /path/to/data.csv -p <project> -m "Results attached"
```

## Common Options

| Flag | Description |
|------|-------------|
| `-p, --project <name>` | Target project name (required when multiple projects exist) |
| `-s, --session <key>` | Target specific session key (optional, defaults to first active) |
| `-m, --message <text>` | Text message to accompany the attachment |
| `--image <path>` | Image file to send (repeatable) |
| `--file <path>` | File to send (repeatable) |
| `--stdin` | Read message body from stdin |

## Project Names

Project names come from `~/.cc-connect/config.toml`. Check the config to find
available project names:

```bash
grep -A1 'name = ' ~/.cc-connect/config.toml
```

If only one project is configured, `-p` can be omitted.

## Workflow Patterns

### Pattern 1: Generate and Send a Chart

After generating a plot with matplotlib, save it to disk and send:

```python
import matplotlib.pyplot as plt

plt.savefig("/tmp/chart.png", dpi=150, bbox_inches="tight")
plt.close()
```

Then:

```bash
cc-connect send --image /tmp/chart.png -p <project> -m "Here is the chart"
```

### Pattern 2: Notify After Long Task

When a long-running task completes (training, backtest, build), notify the user
even if they are away from the screen:

```bash
cc-connect send -m "Training complete! Loss: 0.023, Accuracy: 97.2%" -p <project>
```

### Pattern 3: Send Report with Multiple Files

```bash
cc-connect send \
  --file /tmp/report.pdf \
  --file /tmp/data.csv \
  --image /tmp/summary_chart.png \
  -p <project> \
  -m "Weekly report attached"
```

## Troubleshooting

### "no active session found"

Try specifying the full session key found in daemon logs:

```bash
journalctl --user -u cc-connect -n 20 --no-pager | grep session_key
```

> If not found: The user has not started a chat session yet. The user
> must send at least one message on the platform before `cc-connect send`
> can deliver to them.

Then use the session key:

```bash
cc-connect send --image /path/to/img.png -p <project> -s "discord:xxx:xxx" -m "Image"
```

### "project not found"

Check available projects with `grep 'name = ' ~/.cc-connect/config.toml` and
use the exact project name with `-p`.

### Beta Version Required

The `--image` and `--file` flags require cc-connect >= v1.2.2-beta. Install
via:

```bash
npm install -g cc-connect@beta
```

Stable versions (v1.2.1 and below) only support text messages (`-m`, `--stdin`).

## Requirements

- cc-connect daemon must be running: `cc-connect daemon status`
- `attachment_send = "on"` in `~/.cc-connect/config.toml` (global or per-project)
- For image/file sending: cc-connect >= v1.2.2-beta (`cc-connect --version`)
