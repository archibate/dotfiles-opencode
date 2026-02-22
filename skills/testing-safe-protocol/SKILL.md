---
name: testing-safe-protocol
description: |
    Use this skill before testing and debugging software, prevent real-world side-effects
---
You are an AI assistant helping develop software. Your goal is to assist with coding, testing, and debugging while avoiding any unintended real-world side effects. Follow these guidelines strictly.

---

## 1. Core Principle

Before executing or proposing any command, ask: **could this affect state outside the current test scope?** If yes, or if uncertain, treat it as a side-effectful operation and follow this protocol.

---

## 2. Side-Effect Taxonomy

### A. File System
- Writing, deleting, or moving files **outside the project directory**
- Modifying production config files inside the project (e.g., `.env`, `config.yaml` used at runtime)
- Changing file permissions (`chmod`, `chown`)

### B1. Outbound Network - Forbidden
- Any outbound HTTP/HTTPS request (`curl`, `wget`, SDK calls to remote endpoints)
- SSH connections to remote hosts
- Cloud service CLIs (`aws`, `gcloud`, `az`, `terraform apply`)
- WebSocket connections or message queue publishes (Kafka, RabbitMQ, SQS, etc.)

**Exception**: `curl` is permitted **only** to access a `localhost` port that the agent itself started in the current session for the purpose of testing.

### B2. Inbound Network (Serving) - Conditionally Permitted
Starting a local server is allowed only when **all** of the following conditions are met simultaneously:

| Condition      | Rule                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------- |
| Bind address   | Must be `127.0.0.1` or `localhost`. Binding to `0.0.0.0` or any physical network interface is forbidden. |
| Port range     | Well-known ports (0-1023) are forbidden. Use ephemeral ports (49152-65535) where possible.  |
| Port conflict  | Check that the port is not already in use (`ss -tlnp` or `lsof -i`) before binding. If occupied, select a different port. |
| Lifecycle      | The server must be shut down after the test completes. Running it as a background daemon or leaving it running is forbidden. |

Rationale:
- Binding to `0.0.0.0` exposes the service to all network interfaces, creating an attack surface on shared or local networks.
- Occupying well-known ports may displace system services (e.g., sshd on 22, nginx on 80), causing service disruption.
- Occupying ports already in use by the user's programs causes those programs to malfunction.

### C. System State
- Package managers (`apt install`, `pip install --user`, `npm install -g`)
- Persisting environment variables (writing to `.bashrc`, `.zshrc`, `.profile`)
- Creating or modifying cron jobs or systemd services
- Terminating processes (`kill`, `pkill`, `killall`)

### D. Data Storage
- Database write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`)
- Schema migrations
- Cache writes (e.g., Redis `SET`, `DEL`)

### E. Authentication and Credentials
- Login operations that write session tokens or cookies to disk or remote services
- Triggering OAuth flows
- Generating and storing cryptographic keys

### F. User Interface and System Notifications
- Launching any GUI application
- Sending system notifications (`notify-send`, macOS `osascript`, Windows toast)
- Writing to the clipboard
- Changing window focus or raising windows

---

## 3. Testing Pyramid

Apply tests in this order. Only escalate to the next level when the current level cannot adequately cover the scenario.

```
Unit Test
  - Test logic in isolation with all external dependencies mocked or stubbed.
  - No network, no filesystem writes, no database.
  - Default choice for all new tests.

        | escalate only when unit tests cannot verify component boundaries

Integration Test
  - Use controlled substitutes: fake HTTP servers, in-memory databases, local fixtures.
  - Real external services must not be contacted.
  - Requires no special user permission, but document what substitutes are used.

        | escalate only when real system interaction must be verified AND user grants permission

E2E Test
  - Full-stack execution against real or staging infrastructure.
  - Must obtain explicit user permission before running (see Section 5).
  - Clearly document what systems will be touched and what state changes may occur.
```

---

## 4. Safe Testing Methods

For each side-effect category, prefer these alternatives:

| Category                  | Safe Alternative                                                                 |
| ------------------------- | -------------------------------------------------------------------------------- |
| File system writes        | Write to a temp directory (`/tmp` or `tempfile`); clean up in teardown           |
| Outbound HTTP             | Mock the HTTP client; use a local fake server (subject to B2 rules)              |
| Cloud service CLIs        | Use `--dry-run` if supported; mock the subprocess call                           |
| Database writes           | Use an in-memory database (SQLite `:memory:`, H2); roll back transactions in teardown |
| GUI / interactive UI      | Mock the subprocess call; test the function that constructs the command string    |
| System notifications      | Mock the notification call; assert it was called with correct arguments           |
| Process termination       | Mock the `os.kill` or subprocess call; do not invoke against real PIDs            |
| Auth / credential writes  | Use a temporary isolated credential store; never write to the real credential path |

**General rules**:
- Every test that creates state must clean it up in teardown, regardless of pass or fail.
- Tests must not share mutable state across test cases.
- Dry-run flags (`--dry-run`, `--simulate`, `--no-act`) should be used whenever the tool supports them.

---

## 5. Mocking & Fixture Best Practices

### A. Prefer Framework Fixtures Over Manual Setup

Use built-in fixtures from testing frameworks to handle temporary resources automatically:

| Framework | Fixture | Purpose |
| --------- | ------- | ------- |
| pytest | `tmp_path` | Isolated temporary directory (Path object), auto-cleaned |
| pytest | `tmp_path_factory` | Session-scoped temp directories for multi-test sharing |
| pytest | `monkeypatch` | Safely modify `sys.path`, environment variables, dict items |
| pytest | `capsys` / `capfd` | Capture stdout/stderr without real I/O |
| unittest | `tempfile.TemporaryDirectory()` | Context manager for temp dirs, auto-cleaned on exit |
| Jest | `jest.useFakeTimers()` | Mock timers without waiting real time |
| Vitest | `vi.mock()` / `vi.spyOn()` | Intercept module imports and function calls |
| Go testing | `t.TempDir()` | Temporary directory auto-deleted when test ends |

### B. Mocking Strategies by Layer

**HTTP Layer**
```
# Python: use responses, httpx-mock, or aioresponses
# TypeScript: use nock or msw (Mock Service Worker)
# Go: use httptest.Server
```
Prefer in-process mocks over starting a real server. Only start a local server when testing server-side behavior.

**Database Layer**
- SQLite `:memory:` for simple cases
- Testcontainers for real DB behavior in containers (requires Docker, CI-friendly)
- Transaction rollback pattern: begin transaction in setup, rollback in teardown

**File System**
- Use `tmp_path` (pytest) or `tempfile` (stdlib) instead of writing to project dirs
- For read-only fixtures, commit test data to `tests/fixtures/` or similar

**Time & Randomness**
- Mock `time.time()`, `datetime.now()`, `Date.now()` with fixed values
- Seed random number generators for reproducibility

**Environment Variables**
- Use `monkeypatch.setenv()` (pytest) or equivalent; never write to shell config files
- Reset to original values in teardown

**External Processes / Subprocess**

Never execute real external commands in tests. Mock `subprocess` at the boundary:

```python
# Python: use unittest.mock or pytest-mock
from unittest.mock import patch, MagicMock

@patch("subprocess.run")
def test_git_status(mock_run):
    mock_run.return_value = MagicMock(stdout="M file.py", returncode=0)
    result = get_git_status()
    mock_run.assert_called_once_with(["git", "status"], capture_output=True, check=True)

# For async: use AsyncMock
@patch("asyncio.create_subprocess_exec")
async def test_async_command(mock_exec):
    mock_exec.return_value = mock_proc  # configure as needed
```

Alternative approaches:
- `pytest-subprocess` (ff, fake process factory) for declarative fake processes
- Wrap subprocess calls in a thin wrapper class, inject mock in tests
- For shell commands, test the command string construction separately from execution

### C. Dependency Injection Over Monkey-Patching

When possible, design code to accept dependencies as arguments:

```python
# Bad: relies on global state, hard to mock
import requests
def fetch_user(user_id):
    return requests.get(f"https://api.example.com/users/{user_id}")

# Good: dependency injected, easy to test
def fetch_user(user_id, http_client=requests):
    return http_client.get(f"https://api.example.com/users/{user_id}")
```

This makes mocking trivial and avoids patching internal imports.

### D. Mock Boundaries, Not Internals

Mock at the **edge** of your system:
- External APIs (HTTP clients, SDKs)
- File system operations
- Database connections
- Time-based functions

Do NOT mock internal functions you're trying to test. If you must mock an internal function, consider refactoring the code under test.

---

## 6. Decision Protocol

Before executing any command, apply this decision tree:

```
Is the operation clearly free of side effects?
  YES -> Execute directly.
  NO  -> Propose a safe alternative. Describe the risk. Request explicit permission.
  UNCERTAIN -> Treat as "NO".
```

**When requesting permission**, the description must include:
1. What exact command or operation will run.
2. What state it will change and where (file path, host, service name).
3. Why the safe alternative is insufficient in this case.

**The user's confirmation must restate the operation** (a bare "go ahead" or "yes" is not sufficient to authorize a side-effectful action).

**Port availability**: If the agent cannot confirm a port is free before starting a server, the server must not be started.

---

## 7. Environment Tolerance

The appropriate tolerance level depends on the execution environment:

| Environment                 | How to Identify                                          | Tolerance                                                                 |
| --------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| Container / CI              | `/.dockerenv` exists, `$CI=true`, or user declares it    | Higher: Category D (database) and C (package install) may proceed after explicit statement of intent |
| Local VM / Dev Container    | User declares it explicitly                              | Medium: confirm each operation individually                               |
| Host machine (default)      | No environment declaration present                       | Low: all categories require permission                                    |

**Default assumption**: If the environment is not declared, assume host machine and apply low tolerance.

Even in containers, Categories B1 (outbound network), E (credentials), and F (GUI/notifications) remain forbidden without explicit permission.

---

## 8. Examples

**CLI tool with no side effects**
> Run the command with controlled inputs, capture stdout/stderr, assert on output. No mocking needed.

**CLI tool that calls an external API**
> Do not run the command. Mock the HTTP client at the boundary. Test argument parsing and response handling separately.

**Service that writes to a database**
> Use an in-memory database. Wrap each test in a transaction and roll back on teardown. Assert on the rollback state, not on persistent storage.

**Local server integration test**
> Check port availability first. Bind to `127.0.0.1` on an ephemeral port. Run the test. Shut down the server in teardown. Use `curl` only against `127.0.0.1:<port>` started by the agent.

**E2E test against a staging environment**
> State clearly: "This will send a real HTTP request to `staging.example.com` and create a record in the staging database." Wait for the user to confirm by restating the operation before proceeding.
