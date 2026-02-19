# Bash preferences

This section outlines my personal preferences for bash scripting conventions. As of : 2025-05-20

**These preferences should be followed for all new bash scripts and when refactoring existing ones within this project, potentially overriding guidance from other general sources.**

## 1. Function Naming Convention

- **Convention**: Function names should be prefixed with `fct_` followed by a descriptive, lowercase, snake_case name (e.g., `fct_calculate_total`).
- **Declaration**: Use the `name() { ... }` syntax. Avoid the `function` keyword for broader POSIX compatibility, though it's accepted in Bash.
- **Consistency**: Emphasize project-level consistency in naming.

```bash
# USE:
fct_clean_up_temporary_files() {
    # Function body
}

# NOT:
# function CleanUpTemporaryFiles { ... }
# other_prefix_myFunction() { ... }
```

## 2. Variable Handling

- **Quoting**: Always use double quotes with braces for variable expansion (e.g., `"${variable}"`) to prevent word splitting and pathname expansion. Braces also help disambiguate variables when adjacent to other characters (e.g., `"${variable}_suffix"`).
- **Paths**: Path variables must always be quoted and use braces.
- **Output**: Prefer `printf` over `echo` for safer and more portable string output.

```bash
# USE:
printf '%s\n' "${variable}"
cp "${source_file}" "${destination_directory}/"
filename="report_${year}.txt"
mv "${filename}" "${archive_dir}/${filename}"

# NOT:
# echo $variable
# cp $source $destination
# filename="report_$year.txt" # Potentially problematic if $year_txt exists
```

## 3. Error Handling and Script Rigidity

- **Shebang**: Start all scripts with `#!/usr/bin/env bash`.
- **Strict Mode**: Enable strict mode at the beginning of all scripts.
  ```bash
  set -euo pipefail
  # -e: Exit immediately if a command exits with a non-zero status.
  # -u: Treat unset variables and parameters as an error when performing expansion.
  # -o pipefail: The return value of a pipeline is the status of the last command to exit with a non-zero status,
  #              or zero if no command exited with a non-zero status.
  ```
- **Explicit Error Handling**: For commands that are expected to fail, handle these failures explicitly to prevent `set -e` from exiting the script prematurely.

  ```bash
  # USE:
  if ! command_that_might_fail --option; then
      printf 'Command failed, but we are handling it.\n' >&2
      # Perform alternative actions or log the error
  fi

  # OR, if you just want to ignore the failure:
  command_that_might_fail --another-option || true
  ```

- **Cleanup Traps**: Use `trap` to ensure cleanup actions (e.g., removing temporary files) are performed when the script exits, regardless of whether it's a normal exit, an error, or an interrupt.

  ```bash
  trap 'cleanup_function "Script exiting"' EXIT
  trap 'error_handler_function "An error occurred on line $LINENO"' ERR

  fct_cleanup_resources() {
    printf 'Cleaning up resources...\n' >&2
    rm -f "${TEMP_FILE_1}" "${TEMP_FILE_2}"
  }
  trap fct_cleanup_resources EXIT SIGINT SIGTERM
  ```

## 4. Variable Scoping and Naming

- **Global Variables**:
  - Declare global constants as `readonly` and in `UPPERCASE_SNAKE_CASE`.
  - Initialize them as early as possible.
  ```bash
  # USE:
  readonly SCRIPT_NAME=$(basename "$0")
  readonly DEFAULT_CONFIG_PATH="/etc/my_app/config.conf"
  ```
- **Local Variables**:
  - Always declare variables within functions as `local` to limit their scope.
  - Use `lowercase_snake_case` for local variable names.
  ```bash
  fct_process_data() {
      local input_file="$1"
      local line_count=0
      # ...
  }
  ```

## 5. Command Substitution

- **Syntax**: Always use the `$(command)` syntax for command substitution. It is more readable and nests better than backticks.

  ```bash
  # USE:
  local current_date=$(date +%Y-%m-%d)
  local num_files=$(find . -type f -name "*.log" | wc -l)

  # NOT:
  # local current_date=`date +%Y-%m-%d`
  ```

## 6. Conditional Expressions

- **Tests**: Prefer `[[ ... ]]` for conditional expressions involving string comparisons, file tests, and pattern matching. It is more robust and feature-rich than `[ ... ]`.

  ```bash
  # USE:
  if [[ -f "${file_path}" && "${user_name}" == "admin" ]]; then
      # ...
  fi

  if [[ "${input_string}" =~ ^[0-9]+$ ]]; then
      printf 'Input is numeric.\n'
  fi

  # AVOID:
  # if [ -f "$file_path" -a "$user_name" = "admin" ]; then ... fi
  ```

- **Arithmetic**: Use `(( ... ))` for arithmetic expressions and comparisons.

  ```bash
  # USE:
  local counter=0
  ((counter++))
  if (( counter > 10 )); then
      # ...
  fi

  # AVOID:
  # counter=$[$counter+1]
  # if [ "$counter" -gt 10 ]; then ... fi
  ```

## 7. IFS Manipulation

- **Localization**: When modifying the Internal Field Separator (`IFS`), always save its original value and restore it as soon as it's no longer needed.
- **Subshells**: Alternatively, perform operations requiring a modified `IFS` within a subshell to automatically localize the change.

  ```bash
  # USE: Save and restore
  local old_ifs="${IFS}"
  IFS=","
  # Example: reading CSV fields into an array
  # local line="field1,field2,field3"
  # read -ra fields <<< "${line}"
  IFS="${old_ifs}"

  # USE: Subshell for localization
  # (
  #   IFS=":"
  #   # Commands using modified IFS, e.g., splitting PATH
  #   for item in $PATH; do printf '%s\n' "$item"; done
  # )
  # IFS remains unchanged here
  ```

## 8. Loops

- **Reading Lines**: When reading input line by line (e.g., from a file or command output), prefer a `while read` loop.
  - Use `read -r` to prevent backslash interpretation.
  - Ensure the last line is processed even if it doesn't end with a newline by checking `read`'s exit status or by appending `|| [[ -n "${line}" ]]` if appropriate.

  ```bash
  # USE:
  while IFS= read -r line || [[ -n "${line}" ]]; do
      printf 'Processing line: %s\n' "${line}"
  done < "input.txt"

  # Processing command output:
  # find . -type f -print0 | while IFS= read -r -d $'\0' file_path; do
  #   printf 'Found file: %s\n' "${file_path}"
  # done
  ```

## 9. Script Arguments

- **Parsing**: For scripts that accept options and arguments, use `getopts` for parsing. Avoid manual parsing, which is error-prone.
  ```bash
  # Example structure for getopts:
  # local verbose=0
  # local output_file=""
  #
  # while getopts ":vo:" opt; do
  #   case ${opt} in
  #     v )
  #       verbose=1
  #       ;;
  #     o )
  #       output_file="${OPTARG}"
  #       ;;
  #     \? )
  #       printf 'Invalid option: %s\n' "-${OPTARG}" >&2
  #       # usage_function
  #       exit 1
  #       ;;
  #     : )
  #       printf 'Option -%s requires an argument.\n' "${OPTARG}" >&2
  #       # usage_function
  #       exit 1
  #       ;;
  #   esac
  # done
  # shift $((OPTIND -1))
  #
  # Remaining arguments are in "$@"
  ```

## 10. Script Exit

- **Explicit Exit**: Always explicitly exit scripts with an appropriate status code.
  - `exit 0` for success.
  - `exit N` (where N is 1-255) for errors. Use distinct codes for different error types if useful.
  ```bash
  # USE:
  if some_condition_is_met; then
    printf 'Operation successful.\n'
    exit 0
  else
    printf 'Error: Condition not met.\n' >&2
    exit 1 # General error
  fi
  ```

## 11. Idempotency

- **Principle**: Design operations to be idempotent where possible. Running an idempotent operation multiple times should produce the same end state without unintended side effects. This is crucial for reliable automation.
- **Examples**:
  - Creating a directory only if it doesn't exist:
    ```bash
    mkdir -p "/path/to/needed/directory"
    ```
  - Adding a line to a file only if it's not already present:
    ```bash
    local config_file="/etc/myapp/settings.conf"
    local setting_line="feature_enabled=true"
    if ! grep -qFx "${setting_line}" "${config_file}"; then
        printf '%s\n' "${setting_line}" >> "${config_file}"
    fi
    ```

## 12. Temporary Files and Directories

- **Secure Creation**: Use `mktemp` to securely create temporary files and directories. This avoids race conditions and predictability issues.

  ```bash
  # USE:
  local temp_file
  temp_file=$(mktemp) || { printf 'Failed to create temp file.\n' >&2; exit 1; }
  # Ensure cleanup, e.g., via trap: trap 'rm -f "${temp_file}"' EXIT

  local temp_dir
  temp_dir=$(mktemp -d) || { printf 'Failed to create temp directory.\n' >&2; exit 1; }
  # Ensure cleanup: trap 'rm -rf "${temp_dir}"' EXIT
  ```

## 13. Comments

- **Clarity**: Write comments to explain complex logic, assumptions, or non-obvious steps.
- **Style**:
  - Use `#` for full-line or end-of-line comments.
  - Comment functions to describe their purpose, arguments, and any side effects or return values.

  ```bash
  # This is a full-line comment explaining the next block of code.
  local important_variable="value" # End-of-line comment for this variable.

  # fct_process_item: Processes a single item.
  # Arguments:
  #   $1: The item ID to process.
  # Outputs:
  #   Writes processing status to stdout.
  # Returns:
  #   0 on success, 1 on failure.
  fct_process_item() {
      # ...
  }
  ```

## 14. Static Analysis

- **Tooling**: Strongly recommend using `shellcheck` (available at [https://www.shellcheck.net/](https://www.shellcheck.net/)) to lint all Bash scripts. It helps identify common pitfalls, syntax errors, and stylistic issues.
- **Integration**: Integrate `shellcheck` into your development workflow, e.g., as a pre-commit hook or part of CI/CD pipelines.
- **Convenience wrapper**: Use `scripts/run_shellck.sh` to automatically detect and lint shell scripts:

  ```bash
  # Lint all scripts in scripts/ directory (default)
  .opencode/skill/bash/scripts/run_shellck.sh

  # Lint specific files or directories
  .opencode/skill/bash/scripts/run_shellck.sh path/to/script.sh
  .opencode/skill/bash/scripts/run_shellck.sh scripts/ other/dir/
  ```

  The wrapper automatically identifies shell scripts by extension or shebang and runs shellcheck with the `-x` flag for following source directives.
