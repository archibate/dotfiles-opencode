#!/usr/bin/env bash
#
# ==============================================================================
# Universal Bash Script Template
# ==============================================================================
# Why: A consistent, defensive template reduces copy/paste bugs and makes scripts
#      easier to operate (clear flags, predictable exits, logging, cleanup).
#
# Copy this file for new scripts, then update the "Script metadata" section.
# ==============================================================================

# ==============================================================================
# Script metadata
# ==============================================================================
# Why: Keep these constants in one place so `--help/--version` stay correct.

readonly SCRIPT_VERSION="0.1.0"
readonly SCRIPT_AUTHOR="Your Name"
readonly SCRIPT_DESCRIPTION="Describe what this script does."

# Why: Prefer BASH_SOURCE for reliable path resolution across invocation modes.
readonly SCRIPT_PATH="${BASH_SOURCE[0]}"
readonly SCRIPT_NAME="${SCRIPT_PATH##*/}"

fct_get_script_dir() {
	# Why: Avoid external tools (dirname/realpath) for portability and speed.
	local source="${SCRIPT_PATH}"
	local dir="${source%/*}"
	if [[ "${dir}" == "${source}" ]]; then
		dir="."
	fi

	(cd "${dir}" >/dev/null 2>&1 && pwd -P)
}
SCRIPT_DIR="$(fct_get_script_dir)"
readonly SCRIPT_DIR

# ==============================================================================
# Runtime options (overridable via CLI flags)
# ==============================================================================
# Why: Defaults allow the template to run out-of-the-box without surprises.

VERBOSE=0
LOG_FILE=""              # When set, logs also append here (without ANSI color codes).
NO_COLOR="${NO_COLOR:-}" # Respect the NO_COLOR convention when already set.

# ==============================================================================
# Internal state (used by traps/cleanup)
# ==============================================================================
# Why: Predeclare variables so `set -u` won't crash cleanup on early exits.

TMP_DIR=""
LOCK_DIR=""
POSITIONAL_ARGS=()

# ==============================================================================
# Execution mode helpers
# ==============================================================================
# Why: Sourcing a script should not change caller options or auto-run main().

IS_SOURCED=0
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
	IS_SOURCED=1
fi
readonly IS_SOURCED

fct_exit() {
	# Why: Avoid exiting the parent shell when the script is sourced.
	local code="${1:-0}"

	if [[ "${IS_SOURCED}" -eq 1 ]]; then
		return "${code}"
	fi
	exit "${code}"
}

# ==============================================================================
# Strict mode
# ==============================================================================
# Why: Strict mode makes failures loud/early instead of silently wrong output.
#
# -e: Exit on command failure (fail fast; handle expected failures explicitly).
# -u: Error on unset variables (catch typos and missing env/args early).
# -o pipefail: Pipelines fail if any command fails (not just the last one).

fct_enable_strict_mode() {
	set -euo pipefail
	# Why: ERR traps are not inherited by functions unless errtrace is set.
	set -o errtrace
}

# ==============================================================================
# Logging
# ==============================================================================
# Why: Consistent logs make scripts debuggable in CI and on laptops. Logs go to
#      stderr so stdout can be reserved for machine-readable output.

fct_timestamp() {
	date '+%Y-%m-%d %H:%M:%S%z'
}

fct_ansi() {
	# Why: Centralize ANSI emission; it becomes a no-op when color is disabled.
	local code="${1}"
	if [[ -t 2 && -z "${NO_COLOR}" ]]; then
		printf '\033[%sm' "${code}"
	fi
}

fct_log() {
	local level="${1}"
	shift

	local message="$*"
	local ts
	ts="$(fct_timestamp)"

	local plain="${ts} [${SCRIPT_NAME}] ${level}: ${message}"
	local rendered="${plain}"

	if [[ -t 2 && -z "${NO_COLOR}" ]]; then
		local prefix=""
		local reset=""
		reset="$(fct_ansi '0')"

		case "${level}" in
		DEBUG) prefix="$(fct_ansi '36')" ;; # cyan
		INFO) prefix="$(fct_ansi '32')" ;;  # green
		WARN) prefix="$(fct_ansi '33')" ;;  # yellow
		ERROR) prefix="$(fct_ansi '31')" ;; # red
		*) prefix="" ;;
		esac

		rendered="${prefix}${plain}${reset}"
	fi

	printf '%s\n' "${rendered}" >&2

	if [[ -n "${LOG_FILE}" ]]; then
		printf '%s\n' "${plain}" >>"${LOG_FILE}"
	fi
}

log_debug() {
	if [[ "${VERBOSE}" -eq 1 ]]; then
		fct_log "DEBUG" "$@"
	fi
}
log_info() { fct_log "INFO" "$@"; }
log_warn() { fct_log "WARN" "$@"; }
log_error() { fct_log "ERROR" "$@"; }

# Repo convention wrappers (optional, keep project naming consistent).
fct_log_debug() { log_debug "$@"; }
fct_log_info() { log_info "$@"; }
fct_log_warn() { log_warn "$@"; }
fct_log_error() { log_error "$@"; }

# ==============================================================================
# Error handling
# ==============================================================================
# Why: Centralize fatal exits for consistent messages and exit codes.

die() {
	local message="${1:-Unknown error}"
	local exit_code="${2:-1}"

	log_error "${message}"
	fct_exit "${exit_code}"
}
fct_die() { die "${1:-Unknown error}" "${2:-1}"; }

# ==============================================================================
# Usage / version
# ==============================================================================
# Why: A good help block prevents misuse and reduces support/debug time.

usage() {
	cat <<EOF
${SCRIPT_NAME} v${SCRIPT_VERSION}
${SCRIPT_DESCRIPTION}
Author: ${SCRIPT_AUTHOR}

Usage:
  ${SCRIPT_NAME} [options] [--] [args...]

Options:
  -h, --help         Show this help and exit
  -V, --version      Show version and exit
  -v, --verbose      Enable debug logging
      --no-color     Disable colored output (also respects NO_COLOR)
      --log-file P   Append logs to file P (no color codes)

Examples:
  ${SCRIPT_NAME} --help
  ${SCRIPT_NAME} -v --log-file "/tmp/${SCRIPT_NAME}.log" -- arg1 arg2
EOF
}

show_version() {
	printf '%s\n' "${SCRIPT_NAME} v${SCRIPT_VERSION}"
}

# ==============================================================================
# Argument parsing
# ==============================================================================
# Why: Manual parsing keeps long options readable without extra dependencies.

fct_parse_arguments() {
	POSITIONAL_ARGS=()

	while [[ $# -gt 0 ]]; do
		case "$1" in
		-h | --help)
			usage
			fct_exit 0
			;;
		-V | --version)
			show_version
			fct_exit 0
			;;
		-v | --verbose)
			VERBOSE=1
			shift
			;;
		--no-color)
			NO_COLOR="1"
			shift
			;;
		--log-file)
			if [[ $# -lt 2 ]]; then
				die "Option --log-file requires a path." 2
			fi
			if [[ "${2}" == -* ]]; then
				die "Option --log-file requires a path (got: ${2})." 2
			fi
			LOG_FILE="${2}"
			if ! : >>"${LOG_FILE}"; then
				LOG_FILE=""
				die "Cannot write to log file: ${2}" 1
			fi
			shift 2
			;;
		--log-file=*)
			LOG_FILE="${1#*=}"
			if ! : >>"${LOG_FILE}"; then
				LOG_FILE=""
				die "Cannot write to log file: ${1#*=}" 1
			fi
			shift
			;;
		--)
			shift
			POSITIONAL_ARGS+=("$@")
			break
			;;
		-*)
			die "Unknown option: $1" 2
			;;
		*)
			POSITIONAL_ARGS+=("$1")
			shift
			;;
		esac
	done
}

# ==============================================================================
# Dependency checking
# ==============================================================================
# Why: Fail early with actionable errors when required tools are missing.

fct_require_command() {
	local cmd="${1}"
	local hint="${2:-}"

	if ! command -v "${cmd}" >/dev/null 2>&1; then
		if [[ -n "${hint}" ]]; then
			die "Missing required command: ${cmd}. ${hint}" 4
		fi
		die "Missing required command: ${cmd}." 4
	fi
}

fct_check_dependencies() {
	# Add commands your script needs (examples):
	# fct_require_command "jq" "Install: brew install jq (macOS) or apt-get install jq (Debian/Ubuntu)"
	:
}

# ==============================================================================
# Cleanup & traps
# ==============================================================================
# Why: Always release resources (temp dirs, locks) even on errors or Ctrl+C.

cleanup() {
	local exit_status=$?

	# Ensure cleanup never masks the original exit status.
	set +e

	if [[ -n "${LOCK_DIR}" && -d "${LOCK_DIR}" ]]; then
		rmdir "${LOCK_DIR}" 2>/dev/null || true
	fi

	if [[ -n "${TMP_DIR}" && -d "${TMP_DIR}" ]]; then
		rm -rf "${TMP_DIR}" 2>/dev/null || true
	fi

	return "${exit_status}"
}
fct_cleanup() { cleanup; }

fct_on_error() {
	local exit_status=$?
	local line_no="${1:-?}"
	local command="${2:-?}"

	# Prevent recursive ERR trapping while handling an error.
	trap - ERR

	log_error "Command failed (exit ${exit_status}) at line ${line_no}: ${command}"
	exit "${exit_status}"
}

fct_on_signal() {
	local signal="${1:-INT}"
	local exit_code=130

	case "${signal}" in
	INT) exit_code=130 ;;
	TERM) exit_code=143 ;;
	*) exit_code=1 ;;
	esac

	log_warn "Received ${signal}, exiting."
	exit "${exit_code}"
}

fct_setup_traps() {
	trap 'cleanup' EXIT
	trap 'fct_on_error "${LINENO}" "${BASH_COMMAND}"' ERR
	trap 'fct_on_signal INT' INT
	trap 'fct_on_signal TERM' TERM
}

# ==============================================================================
# Main logic
# ==============================================================================
# Why: Keeping business logic in one function improves testability and reuse.

fct_execute_this() {
	# Replace this stub with your script's real work.
	log_info "TODO: implement script logic in fct_execute_this()"

	if [[ ${#POSITIONAL_ARGS[@]} -gt 0 ]]; then
		log_debug "Positional args: ${POSITIONAL_ARGS[*]}"
	fi
}

main() {
	# Why: Only enable strict mode/traps when executed, not when sourced.
	fct_enable_strict_mode
	fct_setup_traps

	fct_parse_arguments "$@"
	fct_check_dependencies

	# Why: A temp workspace prevents clobbering user directories and is easy to
	#      tear down via cleanup() on all exit paths.
	TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/${SCRIPT_NAME}.XXXXXXXX")" || die "Failed to create temp dir." 1

	log_debug "Script dir: ${SCRIPT_DIR}"
	log_debug "Temp dir: ${TMP_DIR}"
	if [[ -n "${LOG_FILE}" ]]; then
		log_debug "Logging to file: ${LOG_FILE}"
	fi

	fct_execute_this
	log_info "Done."
}

# Repo convention wrapper.
fct_main() { main "$@"; }

# Why: Avoid side effects when sourced; only auto-run when executed directly.
if [[ "${IS_SOURCED}" -eq 0 ]]; then
	main "$@"
fi
