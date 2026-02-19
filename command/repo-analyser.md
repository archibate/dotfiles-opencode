---
description: repo-analyser
---

# Bootstrap Repository Documentation

Explore this repository using 10 specialized exploration agents running in parallel. Each agent focuses on a specific aspect of the codebase. After all agents complete, synthesize findings into a comprehensive `CODEBASE[.]md` document.

## Target

$ARGUMENTS

If no target specified, analyze the entire repository.

## Step 1: Launch All 10 Agents in Parallel

**CRITICAL**: Launch ALL 10 Task tool calls in a SINGLE message for true parallel execution. Use `@ explore` subagent for each.

Launch these exploration agents simultaneously:

### Agent 1: Repository Structure
```
@ explore Map the complete directory structure of this repository. Identify:
- Top-level directories and their purposes
- Key entry points (main files, index files)
- Overall architecture pattern (monorepo, microservices, monolith, etc.)
- File naming conventions
Return a structured summary of the repository layout.
```

### Agent 2: Documentation Discovery
```
@ explore Find all existing documentation in this repository:
- README files at all levels
- Doc folders and their contents
- Inline documentation patterns
- API documentation
- Architecture decision records (ADRs)
- Contributing guidelines
Summarize what documentation exists and any gaps.
```

### Agent 3: Configuration & Environment
```
@ explore Analyze all configuration and environment setup:
- Config files (tsconfig, eslint, prettier, etc.)
- Environment variables and .env patterns
- Build configuration (webpack, vite, esbuild, etc.)
- Package manager setup (npm, yarn, pnpm)
- Required environment setup steps
Document the configuration landscape.
```

### Agent 4: Data Layer
```
@ explore Explore the data layer of this repository:
- Database schemas and models
- ORM/ODM usage (Prisma, TypeORM, Mongoose, etc.)
- Migration files and patterns
- Data validation schemas
- Caching strategies
- Data flow patterns
Summarize how data is structured and managed.
```

### Agent 5: Core Business Logic
```
@ explore Identify and map the core business logic:
- Main services and their responsibilities
- Key algorithms and computations
- Business rules and validation
- Domain models and entities
- State management patterns
Document the heart of the application logic.
```

### Agent 6: Interface Layer (APIs & Routes)
```
@ explore Map the interface layer:
- API endpoints and routes
- Request/response patterns
- Authentication and authorization
- Middleware usage
- GraphQL schemas (if applicable)
- WebSocket handlers (if applicable)
Document how the application exposes its functionality.
```

### Agent 7: Testing Patterns
```
@ explore Analyze the testing strategy:
- Test frameworks in use (Jest, Vitest, Mocha, etc.)
- Test file organization
- Unit vs integration vs e2e test patterns
- Mocking strategies
- Test utilities and helpers
- Coverage configuration
Summarize testing patterns and coverage approach.
```

### Agent 8: Deployment & Operations
```
@ explore Explore deployment and operations setup:
- CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
- Docker configuration
- Kubernetes manifests (if any)
- Infrastructure as code
- Deployment scripts
- Monitoring and logging setup
Document the deployment and operational patterns.
```

### Agent 9: Dependencies Analysis
```
@ explore Analyze the dependency landscape:
- Key runtime dependencies and their purposes
- Development dependencies
- Peer dependencies and version constraints
- Internal packages (in monorepos)
- Dependency update strategies
- Security considerations
Provide a dependency overview with notable packages explained.
```

### Agent 10: Domain Knowledge
```
@ explore Extract domain-specific knowledge:
- Business domain terminology used in code
- Domain entities and their relationships
- Industry-specific patterns
- Glossary of project-specific terms
- Key abstractions and metaphors
Build a domain knowledge glossary.
```

## Step 2: Collect Agent Results

After launching all agents via the Task tool, collect their findings as they complete.

## Step 3: Synthesize into CODEBASE[.]md

Once all agents have returned their findings, create `CODEBASE[.]md` at the repository root:

```markdown
# Codebase Documentation

> Auto-generated repository documentation

## Overview
[High-level summary synthesized from all agents]

## Repository Structure
[From Agent 1]

## Getting Started
[Synthesized from Agents 2, 3]

## Architecture
[Synthesized from Agents 1, 5, 6]

## Data Layer
[From Agent 4]

## Core Logic
[From Agent 5]

## API Reference
[From Agent 6]

## Testing
[From Agent 7]

## Deployment
[From Agent 8]

## Dependencies
[From Agent 9]

## Domain Glossary
[From Agent 10]

## Documentation Index
[From Agent 2 - links to existing docs]
```

## Important Notes

- Launch ALL agents in a single message for true parallelism
- Each agent has its own context window, preventing context pollution
- If an agent fails, note the gap in the final document
- UI flickering is expected with many parallel agents

## Usage

```
/bootstrap-repo
/bootstrap-repo src/
```

<!-- source https://x.com/cloudxdev -->
