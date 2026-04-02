---
name: anti-defensive
description: Review common AI slops of defensive programming patterns, avoid silent errors. TRIGGER when reviewing code for defensive anti-patterns, writing fail-fast code, or auditing error handling quality.
---

# Anti-Defensive Programming Guide

## Philosophy

AI coding assistants systematically over-produce defensive code due to:
- **Training data bias** — Web/app code dominates GitHub, where graceful degradation IS correct
- **RLHF reinforcement** — Humans penalize crashes more than silent incorrectness

The result: code that swallows errors, fabricates data, and fails silently instead of failing fast.

**Fail-fast principle**: Internal errors should crash immediately and loudly. Problems get fixed instead of hidden. Systems that fail fast actually have fewer outages because they are honest about what can go wrong.

**When defensive IS correct**: At system boundaries handling external input (APIs, user forms, file uploads). Internal code should trust contracts and crash on violations.

## Anti-Patterns

### 1. Swallowing Exceptions

```python
# BAD — Error buried, pipeline continues with None
try:
    result = transform(data)
except Exception as e:
    logger.warning(f"Transform failed: {e}")
    result = None

# GOOD — Let it fail
result = transform(data)
```

Harm: Downstream code receives `None`, causing JOIN failures or corrupted data. Monitoring shows "fine" because no exceptions were thrown.

### 2. Dictionary Defaults on Required Fields

```python
# BAD — Fabricates data for missing required field
user_id = record.get('user_id', -1)
amount = record.get('amount', 0.0)

# GOOD — Required fields should error if missing
user_id = record['user_id']
amount = record['amount']
```

Harm: The `-1` user_id joins with user tables, returns nothing, analytics silently show zero activity.

### 3. Null Coalescing to Fabricate Data

```python
# BAD — Invisible default, hides missing data
email = record.get('email') or 'no-email@example.com'
price = data.get('price') or 0.0

# GOOD — Explicit handling
email = record['email']  # Required
price = record.get('price')  # Nullable is intentional
if price is None:
    price = calculate_default_price(record)
```

Harm: The `or` operator makes defaults invisible. If a default is needed, make it explicit and documented.

### 4. Type Coercion Instead of Validation

```python
# BAD — Silently converts wrong type, hides upstream bug
age = int(record.get('age', 0))
price = float(str(record.get('price', '0.0')))

# GOOD — Let type mismatches surface
age = record['age']
assert isinstance(age, int), f"Expected int, got {type(age)}"
```

Harm: Type mismatches indicate upstream problems. Coercing them hides the root cause.

### 5. Compatibility Shims

```python
# BAD — Turns temporary debt into permanent debt
try:
    result = new_api_call(params)
except AttributeError:
    result = old_api_call(params)

# GOOD — Force migration
result = new_api_call(params)
```

Harm: Breaking changes remain undetected. Technical debt compounds.

### 6. Unnecessary Null Checks

```python
# BAD — Misleading; type contract guarantees non-null
if user is not None and user.name is not None:
    return user.name

# GOOD — Trust the contract
return user.name
```

Harm: Readers assume the value can be null. Checks multiply across codebase.

### 7. Catch-All Exception Handlers

```python
# BAD — Catches KeyboardInterrupt, SystemExit, MemoryError
try:
    process(data)
except:
    pass

# GOOD — Catch specific exceptions or let them propagate
try:
    process(data)
except ValidationError as e:
    raise ValueError(f"Invalid data: {e}") from e
```

Harm: Catches things no programmer should handle. Masks real problems.

### 8. Over-Validation at Internal Boundaries

```python
# BAD — Validates what caller already guarantees
def process(data):
    if data is None:
        return None
    if not isinstance(data, dict):
        return None
    if 'id' not in data:
        return None
    return transform(data['id'])

# GOOD — Validate once at boundary, trust internally
def process(data: dict) -> Result:
    """Expects data with 'id' key. Validated at API boundary."""
    return transform(data['id'])
```

Harm: Validation logic duplicates across call chain. Returns `None` instead of surfacing contract violations.

### 9. Fabricated Default Values

```python
# BAD — Corrupts data with fake values
created_at = record.get('created_at', datetime.now())
name = record.get('name', '')
status = record.get('status', 'unknown')

# GOOD — Required fields must be present
created_at = record['created_at']
name = record['name']
status = record.get('status')  # Only if nullable by design
```

Harm: Historical records get current timestamps. Empty names break downstream logic. 'unknown' status corrupts analytics.

### 10. Logging Warnings Instead of Raising

```python
# BAD — Warnings are ignored
logger.warning(f"Unexpected state: {state}")
continue

# GOOD — Errors demand attention
raise ValueError(f"Unexpected state: {state}")
```

Harm: Problems remain undetected until they cascade into larger failures.

## When Defensive IS Correct

Defensive programming is appropriate at **system boundaries**:

- **External input validation** — API payloads, form submissions, file uploads
- **User-facing error messages** — Graceful UX for invalid user actions
- **Transient failures** — Network timeouts, rate limits, temporary resource unavailability
- **Public libraries** — Cannot control caller behavior

Internal code should trust contracts and fail fast on violations.

## Quick Reference

| Pattern | Anti-Pattern | Correct Approach |
|---------|--------------|------------------|
| Exception handling | `except Exception: pass` | Let it crash or catch specific |
| Dict access | `d.get('required', default)` | `d['required']` |
| Null coalescing | `x or fake_value` | Explicit `if None` logic |
| Type coercion | `int(d.get('x', 0))` | Let type errors surface |
| Compatibility | `try: new except: old` | Migrate to new |
| Null checks | Check guaranteed values | Trust contracts |
| Catch-all | `except:` | Specific exceptions |
| Validation | Validate at every function | Validate at boundary once |
| Defaults | Fabricate required values | Require presence |
| Errors | `logger.warning()` | `raise ValueError()` |
