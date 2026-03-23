---
name: send-notify
description: Send notifications to the user. TRIGGER when user says "notify me", "send notification", "alert me".
---

# Send Notification

## Environment Detection

Check which method is available:

```bash
# Linux desktop
echo $DISPLAY

# ntfy.sh remote
echo $NTFY_SH_PRIVATE_TOPIC

# macOS
uname -s
```

## Methods

| Condition | Method |
|-----------|--------|
| `$DISPLAY` non-empty | Linux desktop (`notify-send`) |
| `uname -s` = `Darwin` | macOS (`terminal-notifier`) |
| `$NTFY_SH_PRIVATE_TOPIC` non-empty | Remote via ntfy.sh |
| None of the above | Fallback: write to `/tmp/claude-notify` |

### Linux Desktop

```bash
notify-send -a "claude" -u critical "Claude" "<message>"
```

### macOS

```bash
terminal-notifier -title "Claude" -message "<message>"
```

### Remote via ntfy.sh

User must set up topic first:

```bash
export NTFY_SH_PRIVATE_TOPIC="your-secret-topic-name"
```

Send:

```bash
curl -s -d "<message>" "https://ntfy.sh/$NTFY_SH_PRIVATE_TOPIC"
```

**Privacy:** ntfy.sh topics are public. Never include sensitive data in notifications.

### Fallback

```bash
echo "$(date -Iseconds): <message>" >> /tmp/claude-notify
```
