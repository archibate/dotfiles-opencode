---
name: writing-commit-messages
description: Create atomic commits with clear, specific messages. Use when committing changes to git repositories. Load before any git commit operation.
---

# Skill: Commit

Create **truly atomic commits** — one logical change per commit, no exceptions.

> **See also**: `writing-clearly-concisely` for deeper guidance on Strunk's principles.

## Core Principle: Atomicity First

> **An atomic commit contains exactly ONE logical change that can be described in a single sentence without using "and".**

If you need the word "and" to describe what a commit does, it should be split into multiple commits.

## Rules

- **Do not push by default** — Let the user review their commits first
- Only push when the user explicitly asks
- **NEVER combine unrelated changes** in a single commit
- **ALWAYS analyze and split** before committing
- **ALWAYS use the commit body** for non-trivial commits — the body explains the "why", the impact, and provides context for future readers. Only trivial changes (typo fixes, formatting) may use a minimal body.

---

## Mandatory Process

### Step 1: Analyze All Changes

Run `git status` and `git diff --stat` to identify all modified files.

### Step 2: Group by Logical Change

Categorize each change into logical groups. A logical group is:

- Changes that serve **one single purpose**
- Changes that would be **reverted together**
- Changes that have **one commit type**

### Step 3: Identify Split Points

**MUST SPLIT when changes involve:**

| Situation                                       | Action                    |
| ----------------------------------------------- | ------------------------- |
| Different purposes (delete old + add new)       | Separate commits          |
| Different file types (code + docs)              | Separate commits          |
| Different features                              | Separate commits          |
| Different commit types (feat vs docs vs remove) | Separate commits          |
| Unrelated directories                           | Consider separate commits |

### Step 4: Commit Sequentially

For each logical group:

1. Stage ONLY files for that group: `git add <specific-files>`
2. Commit with appropriate message (including body if necessary)
3. Repeat for next group

---

## Atomicity Decision Tree

```
Is this change describable in ONE sentence without "and"?
├── YES → Single commit OK
└── NO → MUST SPLIT
    │
    Ask: "What are the distinct actions?"
    │
    For each distinct action:
    └── Create separate commit
```

## Split Examples

### ❌ BAD: Combined Commit

```
📚 docs: Remove old docs directory and update README with new section
```

### ✅ GOOD: Atomic Commits (in order)

```
🧹 remove: Delete deprecated /docs directory
📚 docs: Add installation section to README
```

### ✅ GOOD: Atomic Commit with Body

```
✨ feat: dufuddle (cli): add timeout flag and non-blocking server check

- File(s) changed:
  - WORKDIR/dufuddle/dufuddle.ts
- Nature of changes: Feature addition
- Purpose: Add --timeout flag (default 30s) and switch to async server pings
- Impact: CLI exits cleanly on hung servers; users can set custom timeouts
```

### ❌ BAD: Mixed Changes

```
✨ feat: Add user dashboard and fix login bug and update config
```

### ✅ GOOD: Atomic Commits (in order)

```
🚑 fix: Resolve null pointer in login validation
🧑‍💻 chore: Update database config for production
✨ feat: Add user dashboard with activity summary
```

---

## Staging Strategy for Splits

When you have multiple logical changes in the working directory:

```bash
# First commit: Remove deprecated docs
git add docs/old-directory/
git commit -m "🧹 remove: Delete deprecated /docs/old-directory"

# Second commit: Update README
git add README.md
git commit -m "📚 docs: Add installation section to README"
```

**Never use `git add .` or `git add -A` when splitting commits.**

---

## Commit Types

| Emoji | Type       | Description                                       |
| ----- | ---------- | ------------------------------------------------- |
| ✨    | `feat`     | New features, changes in existing functionality   |
| 🧑‍💻    | `chore`    | Tooling, configuration, maintenance               |
| 📚    | `docs`     | Documentation changes                             |
| 🎨    | `style`    | Code formatting, missing semicolons, etc.         |
| 🧪    | `test`     | Adding or correcting tests                        |
| ♻️    | `refactor` | Code restructuring without changing functionality |
| 🧹    | `remove`   | Removing code, features, or files                 |
| 🚑    | `fix`      | Bug fixes                                         |
| ⚡️    | `perf`     | Performance improvements                          |
| 🚧    | `wip`      | Work in progress                                  |
| 🔒    | `security` | Security improvements                             |

## Message Format

```
<emoji> <type>: <scope> (<context>): <imperative description>

- File(s) changed:
  - path/to/file1.ts
  - path/to/file2.ts
- Nature of changes: <what kind of work was done>
- Purpose: <why this change was made>
- Impact: <what effect this has on users/system/codebase>
```

- **Subject line**: imperative mood ("Add feature" not "Added feature"), under 72 characters
- **Scope**: the affected module, component, or area (e.g., `auth`, `dashboard`, `api`)
- **Context** (optional): additional categorization like `skill`, `ui`, `backend`
- **Body**: adapt to context — simple changes may only need 1-2 fields, complex changes should include all relevant fields
- **No periods** at the end of body lines

---

## Writing Style for Commit Messages

Apply Strunk's principles to every commit message:

### Use Active Voice

| Passive (weak) | Active (strong) |
|----------------|-----------------|
| "Users are shown their activity" | "Show users their activity" |
| "The config was updated" | "Update config" |
| "Errors are now handled" | "Handle errors" |

### Use Specific, Concrete Language

| Vague | Specific |
|-------|----------|
| "Improve performance" | "Reduce query time from 2s to 200ms" |
| "Fix bug" | "Fix null pointer when user has no profile" |
| "Update dependencies" | "Update React 17→18, fix breaking changes" |
| "Better UX" | "Add loading spinner during API calls" |

### Omit Needless Words

| Wordy | Concise |
|-------|---------|
| "This commit adds the ability to" | "Add" |
| "In order to improve" | "To improve" |
| "Due to the fact that" | "Because" |
| "Make changes to the way" | "Change how" |

### Put Statements in Positive Form

| Negative | Positive |
|----------|----------|
| "Don't fail silently" | "Log errors explicitly" |
| "Avoid blocking the UI" | "Run async to keep UI responsive" |
| "Not working on Safari" | "Fix Safari compatibility" |

### Avoid AI Puffery

These words add noise without meaning. Cut them:

- **Buzzwords**: robust, seamless, leverage, streamline, enhance, optimize
- **Vague adjectives**: better, improved, various, significant
- **Empty impact claims**: "improved engagement", "better UX", "enhanced reliability"

| Puffy | Direct |
|-------|--------|
| "Enhanced user experience" | "Add search autocomplete" |
| "Improved reliability" | "Retry failed requests 3 times" |
| "Streamlined workflow" | "Remove 2 clicks from checkout" |
| "Leverage caching" | "Cache API responses for 5 min" |

### Place Key Information at the End

The end of a sentence carries emphasis. Put the most important word there:

| Buried | Emphasized |
|--------|------------|
| "For users who leave tabs open, this prevents logout" | "Prevent logout for users with idle tabs" |
| "The admin page loads faster due to query optimization" | "Optimize queries to speed up admin page" |

---

## Commit Body Guidelines

The subject line answers **"what changed?"** — the body answers **"why does it matter?"**

### When to include each field

| Field                 | When to use                                                                           |
| --------------------- | ------------------------------------------------------------------------------------- |
| **File(s) changed**   | Multi-file commits, or when the path isn't obvious from context                       |
| **Nature of changes** | Always helpful — categorizes the work (bug fix, refactor, new feature, cleanup, etc.) |
| **Purpose**           | Always — the human-readable "why" behind the change                                   |
| **Impact**            | When the change affects UX, performance, behavior, or other developers                |

### Flexibility

Adapt the body to the commit's complexity:

- **Trivial** (typo, formatting): Body optional or minimal
- **Simple** (single-file fix): 1-2 fields
- **Complex** (multi-file feature, refactor): All fields recommended

### Think about future readers

Someone reading `git log` in 6 months should understand:

1. What was changed
2. Why it was changed
3. What impact it has

If your commit message doesn't answer these questions, add more context.

---

## Examples

### Feature

```
✨ feat: dashboard (ui): add real-time activity feed widget

- File(s) changed:
  - src/components/Dashboard/ActivityFeed.tsx
  - src/hooks/useActivityStream.ts
- Nature of changes: New feature
- Purpose: Show users their recent actions (logins, purchases, settings changes)
- Impact: Users see activity within 2 seconds of occurrence via WebSocket
```

### Bug Fix

```
🚑 fix: auth: resolve session timeout on idle users

- File(s) changed:
  - src/services/auth.ts
- Nature of changes: Bug fix
- Purpose: Extend session refresh interval from 5 min to 30 min
- Impact: Users stay logged in with idle tabs; reduces re-auth complaints
```

### Refactoring

```
♻️ refactor: api: extract payment logic into dedicated service

- File(s) changed:
  - src/services/payment.ts
  - src/controllers/checkout.ts
  - src/utils/stripe.ts
- Nature of changes: Code restructuring
- Purpose: Move Stripe calls out of checkout controller into payment.ts
- Impact: Payment tests run without checkout dependencies; adding PayPal requires one file
```

### Removal

```
🧹 remove: legacy: delete deprecated v1 API endpoints

- File(s) changed:
  - src/routes/v1/
  - src/controllers/legacy/
- Nature of changes: Cleanup
- Purpose: Delete v1 endpoints unused since March 2024 migration
- Impact: Remove 1,200 lines of dead code; shrink bundle by 15KB
```

### Documentation

```
📚 docs: readme: add installation instructions for Windows

- File(s) changed:
  - README.md
- Nature of changes: Documentation
- Purpose: Document winget install, PATH setup, and PowerShell config
- Impact: Windows users can install in 3 commands instead of guessing
```

### Maintenance

```
🧑‍💻 chore: deps: update React 18.2→18.3, fix CVE-2024-1234 in lodash

- File(s) changed:
  - package.json
  - bun.lock
- Nature of changes: Dependency update
- Purpose: Patch lodash prototype pollution vulnerability (CVE-2024-1234)
- Impact: Closes security advisory; React update is compatible, no code changes
```

### Test

```
🧪 test: auth: add unit tests for session management

- File(s) changed:
  - src/services/__tests__/auth.test.ts
- Nature of changes: Test coverage
- Purpose: Cover session refresh, expiry, and concurrent login scenarios
- Impact: 12 new tests; auth coverage goes from 45% to 82%
```

### Performance

```
⚡️ perf: api: optimize database queries for user listing

- File(s) changed:
  - src/repositories/user.ts
- Nature of changes: Query optimization
- Purpose: Add index on (org_id, created_at), batch N+1 role lookups
- Impact: Admin user list loads in 200ms instead of 2.1s (10x faster)
```

### Trivial (minimal body)

```
🎨 style: readme: fix typo in header

- File(s) changed: README.md
- Nature of changes: Typo correction
```
