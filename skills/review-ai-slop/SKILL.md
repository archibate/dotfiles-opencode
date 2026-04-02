---
name: review-ai-slop
disable-model-invocation: true
user-invocable: true
description: >
  Review code for AI slop patterns. TRIGGER when user says "review for AI slop",
  "check for AI patterns", "clean up AI code", "audit AI-generated code",
  or "review AI slop".
---

# AI Slop Review Checklist

Review the specified code for AI-generated slop patterns.

**Target:** `$ARGUMENTS` (or current git diff if no arguments provided)

**Output format:** Group findings by category. For each: file path, line number, pattern name, brief description, suggested fix. Do not make inline edits — report findings and let user decide what to fix.

---

## A. Defensive Programming

Load the **`anti-defensive`** skill and apply all 10 patterns:
1. Swallowing exceptions
2. Dictionary defaults on required fields
3. Null coalescing to fabricate data
4. Type coercion instead of validation
5. Compatibility shims
6. Unnecessary null checks
7. Catch-all exception handlers
8. Over-validation at internal boundaries
9. Fabricated default values
10. Logging warnings instead of raising

---

## B. Over-Engineering

| Pattern | Flag When |
|---------|-----------|
| **Premature abstraction** | Factory/strategy/abstract base class for a single implementation. "In case we need it later." |
| **Unnecessary wrappers** | `get_config()` that just calls `os.environ.get()`. Utility functions invoked only once. |
| **Over-modularization** | Simple logic split across many files when one suffices. Deep directory nesting for small codebase. |

---

## C. Unnecessary Infrastructure

| Pattern | Flag When |
|---------|-----------|
| **Retry logic everywhere** | Exponential backoff on local function calls or non-transient operations. |
| **Config/env var overuse** | Every constant configurable via env var, even ones that should never change (math constants, format strings). |
| **Unnecessary async** | asyncio/threading on CPU-bound or already-fast operations (<10ms). |
| **Feature flags for no reason** | Boolean toggles controlling behavior that has no reason to vary. |

---

## D. Code Bloat

| Pattern | Flag When |
|---------|-----------|
| **Excessive logging** | `logger.info` on every function entry/exit. Logging parameter values and return values of internal functions. |
| **Magic number extraction** | `MAX_SIZE = 100` when `100` is obvious from context. Constants that add no clarity. |
| **Trivial docstrings** | `def add(a, b): """Add a and b."""` — docstring restates function name. |
| **Unnecessary data classes** | dataclass/TypedDict created for one-off use instead of just using a dict or tuple. |

---

## E. Testing Slop

| Pattern | Flag When |
|---------|-----------|
| **Tests that test nothing** | Asserting a function exists or returns the right type, not that it returns correct values. Tests with no assertions. |
| **Over-mocking** | Mocking so heavily the test only validates the mock, not the real logic. Mocking what you're trying to test. |

---

## F. Other Patterns

| Pattern | Flag When |
|---------|-----------|
| **Callback/event overuse** | Event emitters, hook systems, or pub/sub for simple linear flows. |
| **Runtime type checking** | `isinstance` checks inside functions that duplicate what type hints + static analysis already handle. |
| **Hallucinated imports** | Using APIs from wrong library version. Importing packages that don't exist. |
| **Boilerplate generators** | Code that exists to satisfy a template rather than solve a problem. Empty `__init__.py` with docstrings. |

---

## Summary Table

| Category | Count | Source |
|----------|-------|--------|
| A. Defensive Programming | 10 | `anti-defensive` skill |
| B. Over-Engineering | 3 | This skill |
| C. Unnecessary Infrastructure | 4 | This skill |
| D. Code Bloat | 4 | This skill |
| E. Testing Slop | 2 | This skill |
| F. Other | 4 | This skill |
| **Total** | **27** | |
