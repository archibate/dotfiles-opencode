#!/usr/bin/env bash
set -euo pipefail

if ! command -v shellcheck >/dev/null 2>&1; then
	echo "shellck: shellcheck not found (install with brew install shellcheck)" >&2
	exit 1
fi

is_shell_file() {
	local path="$1"
	case "$path" in
	*.sh | *.bash | *.zsh | *.command)
		return 0
		;;
	esac
	if [[ -f "$path" ]]; then
		local first
		first="$(head -n 1 "$path" 2>/dev/null || true)"
		if [[ "$first" =~ ^#!.*\b(sh|bash|zsh)\b ]]; then
			return 0
		fi
	fi
	return 1
}

add_targets_from_dir() {
	local dir="$1"
	while IFS= read -r -d '' f; do
		if is_shell_file "$f"; then
			TARGETS+=("$f")
		fi
	done < <(find "$dir" -type f -print0)
}

add_target() {
	local path="$1"
	if [[ -d "$path" ]]; then
		add_targets_from_dir "$path"
		return
	fi
	if [[ -f "$path" ]]; then
		if is_shell_file "$path"; then
			TARGETS+=("$path")
		fi
		return
	fi
	echo "shellck: path not found: $path" >&2
	exit 2
}

TARGETS=()
if [[ $# -gt 0 ]]; then
	for arg in "$@"; do
		add_target "$arg"
	done
else
	if [[ -d "scripts" ]]; then
		add_targets_from_dir "scripts"
	else
		echo "shellck: no targets provided and scripts/ not found" >&2
		exit 2
	fi
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
	echo "shellck: no shell scripts found" >&2
	exit 0
fi

shellcheck -x "${TARGETS[@]}"
