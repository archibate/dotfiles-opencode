---
name: spec-document
description: |
    The format of spec documents.
---

## 📄 Specification Document Format

All spec documents **MUST** follow this Markdown template.
The file should be stored under `specs/` with a meaningful name, e.g., `specs/feature-authentication.md`.

```markdown
# Specification: <Title>

## Metadata
- **Version**: <semver, e.g., 1.0.0>
- **Status**: Draft | Active | Realized | Regressible | Deprecated
- **Author**: <agent or user>
- **Created**: <YYYY-MM-DD>
- **Last Updated**: <YYYY-MM-DD>

## Overview
<Brief description of the feature or system>

## Requirements
### Functional Requirements
- FR-1: <description>
- FR-2: ...

### Non-functional Requirements
- NFR-1: <architecture, performance, security, etc.>

## Test Steps
<Step-by-step verification instructions. May be shell commands, manual actions, or both.>

## Acceptance Criteria
<Conditions that must be satisfied for completion>

## Change Log
| Date       | Version | Description       | Author     |
|------------|---------|-------------------|------------|
| <date>     | 1.0.0   | Initial draft     | <author>   |
```

### 🎯 Document Quality

When writting specification document:
- Focus on **big-picture**.
- DO NOT be too specific on implementation details.
- Avoid ambiguous wording.
- Include **edge cases** in test steps when appliable.
- DO NOT hallucinate.

### 💡 Example Spec Document

Read @memo-app-spec-example.md as a good example of a complete spec document.
