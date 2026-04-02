#!/bin/bash
set -euo pipefail

# Usage
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 'command arg1 arg2'" >&2
    echo "  Wraps pueue add with auto daemon start, per-project grouping, and follow." >&2
    exit 1
fi

command="$1"

# 1. Derive project group name from current working directory
#    Replace / with - and strip leading -
group_name="$(pwd | sed 's|/|-|g; s|^-||')"

# 2. Ensure pueue daemon is running
if ! pueue status &>/dev/null; then
    echo "🔄 Starting pueue daemon..."
    pueued -d
    sleep 1
    if ! pueue status &>/dev/null; then
        echo "❌ Failed to start pueue daemon" >&2
        exit 1
    fi
    echo "✅ Daemon started"
fi

# 3. Create project group if it doesn't exist
if ! pueue group --json 2>/dev/null | jq -e --arg g "$group_name" '.[$g]' &>/dev/null; then
    pueue group add -p 0 "$group_name"
    echo "✅ Created group: $group_name (parallel: unlimited)"
fi

# 4. Add the task
id=$(pueue add -g "$group_name" --print-task-id -- "$command")

if [[ -z "$id" ]]; then
    echo "❌ Failed to add task" >&2
    exit 1
fi

echo "✅ Task #$id added to group '$group_name'"

echo ""
echo "📝 Task output:"

# 5. Follow the task output
exec pueue follow "$id"
