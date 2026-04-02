---
name: code-quality-metrics
description: This skill should be used when the user asks about "code complexity", "cyclomatic complexity", "cognitive complexity", "code metrics", "maintainability index", "code coverage", or when measuring code quality quantitatively. Provides metrics thresholds and measurement techniques.
disable-model-invocation: true
version: 0.1.0
---

# Code Quality Metrics Guide

## Overview

Code quality metrics provide quantitative measures of code characteristics. This skill covers complexity metrics, maintainability indices, and their practical thresholds across different languages.

## Complexity Metrics

### Cyclomatic Complexity (CC)

Measures the number of linearly independent paths through code.

**Calculation**: CC = E - N + 2P
- E = edges in control flow graph
- N = nodes in control flow graph
- P = connected components (usually 1)

**Simplified**: Count decision points + 1
- Each `if`, `elif`, `else`, `for`, `while`, `case`, `catch`, `&&`, `||`, `?:` adds 1

**Thresholds**:
| Range | Risk | Action |
|-------|------|--------|
| 1-10 | Low | Simple, well-structured |
| 11-20 | Moderate | More complex, consider refactoring |
| 21-50 | High | Complex, difficult to test |
| >50 | Very High | Untestable, must refactor |

### Cognitive Complexity

Measures how difficult code is to understand (introduced by SonarQube).

**Key differences from CC**:
- Penalizes nested structures more heavily
- Doesn't count all decision points equally
- Focuses on human comprehension

**Calculation rules**:
1. +1 for each break in linear flow (`if`, `for`, `while`, `switch`, `catch`, `?:`)
2. +1 for each nesting level inside these structures
3. +1 for binary logical operators (`&&`, `||`)
4. Recursion adds +1

**Thresholds**:
| Range | Assessment |
|-------|------------|
| 0-7 | Easy to understand |
| 8-15 | Moderate complexity |
| 16-24 | High complexity, refactor |
| 25+ | Very high, immediate refactoring |

**Example**:
```python
def process(items):           # 0
    for item in items:        # +1 (loop)
        if item.active:       # +1 (if) +1 (nesting=1)
            if item.valid:    # +1 (if) +2 (nesting=2)
                handle(item)
    return items              # Total: 6
```

### Halstead Metrics

Based on counting operators and operands:

| Metric | Formula | Meaning |
|--------|---------|---------|
| Vocabulary | n = n1 + n2 | Unique operators + operands |
| Length | N = N1 + N2 | Total operators + operands |
| Volume | V = N × log2(n) | Size of implementation |
| Difficulty | D = (n1/2) × (N2/n2) | Error-proneness |
| Effort | E = D × V | Mental effort to understand |

## Maintainability Metrics

### Maintainability Index (MI)

Composite metric combining complexity, size, and comments.

**Formula**: MI = 171 - 5.2 × ln(V) - 0.23 × CC - 16.2 × ln(LOC)

**Thresholds**:
| Range | Maintainability |
|-------|-----------------|
| 85-100 | High maintainability |
| 65-84 | Moderate maintainability |
| 0-64 | Low maintainability |

### Lines of Code (LOC)

| Metric | Description | Threshold |
|--------|-------------|-----------|
| Physical LOC | All lines including blanks/comments | Method: <100, Class: <500 |
| Logical LOC | Executable statements | Method: <30, Class: <200 |
| Comment Ratio | Comments / Total | 10-30% typical |

## Coupling Metrics

### Afferent Coupling (Ca)
Number of classes that depend on this class.
- High Ca = Many dependents, changes are risky

### Efferent Coupling (Ce)
Number of classes this class depends on.
- High Ce = Many dependencies, class is fragile

### Instability (I)
I = Ce / (Ca + Ce)
- 0 = Stable (many dependents, few dependencies)
- 1 = Unstable (few dependents, many dependencies)

## Cohesion Metrics

### Lack of Cohesion of Methods (LCOM)

Measures how related methods are within a class.

**LCOM1**: Number of method pairs without shared instance variables
- 0 = Perfect cohesion
- High = Low cohesion, consider splitting

**LCOM4**: Number of connected components in method-field graph
- 1 = Cohesive class
- >1 = Multiple responsibilities

## Quick Reference Table

| Metric | Tool | Good | Warning | Critical |
|--------|------|------|---------|----------|
| Cyclomatic | ESLint, SonarQube | ≤10 | 11-20 | >20 |
| Cognitive | SonarQube | ≤15 | 16-24 | >24 |
| Method LOC | - | ≤30 | 31-50 | >50 |
| Class LOC | - | ≤300 | 301-500 | >500 |
| Parameters | ESLint | ≤3 | 4-5 | >5 |
| Nesting Depth | ESLint | ≤3 | 4 | >4 |
| LCOM4 | - | 1 | 2 | >2 |

## Measurement Commands

### ESLint Complexity
```bash
npx eslint --rule 'complexity: ["error", 10]' src/
```

### SonarQube Analysis
```bash
sonar-scanner -Dsonar.projectKey=myproject
```

### Python Radon
```bash
radon cc src/ -a -s  # Cyclomatic complexity
radon mi src/ -s     # Maintainability index
```

## Additional Resources

### Reference Files

For detailed measurement techniques:
- **`references/measurement-tools.md`** - Tool configurations and usage
- **`references/thresholds-by-language.md`** - Language-specific thresholds

### Integration with Other Skills

Combine with:
- `solid-principles` for structural analysis
- `refactoring-patterns` for improvement strategies
