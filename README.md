# Layered Agent System for OpenCode

A structured multi-agent workflow architecture that separates planning, coordination, and execution into distinct specialized agents. This configuration demonstrates advanced prompt engineering techniques for building reliable AI-powered development workflows.

## The Three-Agent Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Brainstorm │     │   Executor  │     │   Worker    │
│   (Plan)    │────▶│ (Coordinate)│────▶│  (Execute)  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
  tasks.json        Task Tracking        PROGRESS.txt
   (Contract)        (Status)           (Audit Trail)
```

### Why Separation?

| Agent       | Responsibility                    | Temperature | Why Separate?                              |
|-------------|-----------------------------------|-------------|-------------------------------------------|
| Brainstorm  | Understand, research, decompose   | 0.7         | Creativity needed for exploration         |
| Executor    | Coordinate, delegate, track       | 0.0         | Determinism needed for reliable workflow  |
| Worker      | Implement, verify, report         | 0.0         | Precision needed for correct code         |

**Key Insight**: Mixing planning and execution in one agent leads to scope creep, missed edge cases, and unverified assumptions. Separation enforces discipline.

---

## 1. Brainstorm Agent

**Role**: Clarify intent → Gather context → Break down tasks → Generate `tasks.json`

### Core Responsibilities

1. **Clarify User Intent** - Engage in dialogue, identify ambiguities, challenge assumptions
2. **Gather Context** - Explore codebase, browse web for best practices
3. **Present Architecture Choices** - Trade-off analysis, high-level design
4. **Break Down into Layers** - Dependency-ordered decomposition (not feature slices)
5. **Plan Test Strategy** - Shift-Left testing with layer isolation

### Shift-Left Testing Strategy

The Brainstorm agent enforces a **Layer-by-Layer Isolation** approach:

```
Layer 0 (Foundation)  → Pure logic, zero dependencies
Layer 1 (IO/Render)   → Consumes Layer 0, test with mocks first
Layer 2 (UI Shell)    → User-facing, test with mock interactions
Layer N (Composition) → Integrates all layers below
```

**The Golden Rule**: For every potential bug, ask "At which layer can this be caught EARLIEST?" If a bug CAN be caught by a unit test, it MUST be caught by a unit test.

### Output: tasks.json Structure

```json
{
  "tasks": [
    {
      "task": "Implement user login form",
      "description": "Create and validate user login functionality.",
      "steps": [
        {"step": 1, "description": "Create LoginForm component"},
        {"step": 2, "description": "Add email validation logic"},
        {"step": 3, "description": "Implement error display"},
        {"step": 4, "description": "Add redirect on success"}
      ],
      "acceptance-criteria": "Form validates email format using regex. Form displays specific error messages for invalid input. User redirects to dashboard on successful authentication.",
      "test-plan": {
        "unit": ["Email regex accepts valid addresses", "Email regex rejects invalid formats"],
        "integration": ["Form submits credentials to auth API"],
        "e2e-manual": ["Visual: error styling looks correct"]
      },
      "skills": ["tdd-workflow"],
      "complete": false
    }
  ]
}
```

### Field Specifications

| Field                | Constraints                                        |
|----------------------|---------------------------------------------------|
| `task`               | 3-80 chars, imperative verb phrase, title case    |
| `description`        | 10-200 chars, single sentence, imperative mood    |
| `steps`              | Optional, 0-15 items, each independently verifiable |
| `acceptance-criteria`| 20-500 chars, measurable conditions with modal verbs |
| `test-plan`          | MUST have `unit`, `integration`, `e2e-manual` arrays |
| `skills`             | Predefined skill names only, no duplicates        |
| `complete`           | Always `false` initially                          |

---

## 2. Executor Agent

**Role**: Read `tasks.json` → Delegate to Worker → Track progress → Commit

### Workflow

```
1. READ PROGRESS
   └── Locate tasks.json → Parse → Find first incomplete task

2. PRE-TASK COMMIT
   └── Delegate to @committer → "Stage any unstaged changes"

3. EXECUTE TASK
   └── Delegate to @worker with exact task briefing
       ├── Task name (verbatim)
       ├── Description (verbatim)
       ├── Steps (if present)
       ├── Acceptance criteria (verbatim)
       └── Skills list

4. UPDATE STATUS
   └── Set complete: true in tasks.json

5. POST-TASK COMMIT
   └── Delegate to @committer → "Commit for task: [name]"

6. REPEAT
   └── Return to step 1
```

### Task Briefing Format

The Executor passes EXACT content from `tasks.json` without modification:

```
Task Name: Implement user login form
Description: Create and validate user login functionality with email format validation.
Steps:
1. Create LoginForm component in src/components/
2. Add email regex validation logic
3. Implement error message display
4. Add redirect to dashboard on success
Acceptance Criteria: Form validates email format using regex. Form displays specific error messages for invalid input. User redirects to dashboard on successful authentication.
Relevant Skills: tdd-workflow, systematic-debugging
```

**Important**: The Executor never implements code. It only coordinates and tracks.

---

## 3. Worker Agent

**Role**: Execute single task → Verify acceptance criteria → Report completion

### Execution Guidelines

1. **Focus strictly** on the provided task only
2. **Steps are guidance** - prioritize acceptance-criteria over step order if conflicts arise
3. **Verify ALL acceptance criteria** before reporting completion
4. **Never commit** - git operations handled by Committer agent
5. **Write to PROGRESS.txt** with structured audit trail

### Completion Protocol

Before reporting done, the Worker must verify:

```
☐ Reviewed acceptance-criteria field
☐ Created numbered list of each criterion
☐ Verified each criterion with code/test evidence
☐ Executed all steps OR documented why changed
☐ Written and run tests (if applicable)
☐ Reviewed code style consistency
☐ Documented all files modified
☐ Prepared PROGRESS.txt summary
```

### PROGRESS.txt Format

```
================================================================================
TASK ID: task-001
TASK NAME: Implement user login form
STATUS: complete
TIMESTAMP: 2026-02-19T14:30:45Z
================================================================================
OBJECTIVE (Acceptance Criteria):
   Form validates email format using regex pattern. Form displays specific 
   error messages for invalid input. User redirects to dashboard on success.

STEPS PROVIDED:
   1. Create LoginForm component in src/components/
   2. Add email regex validation logic
   3. Implement error message display
   4. Add redirect to dashboard on success

STEPS EXECUTED:
   ✓ Step 1: Created LoginForm component in src/components/LoginForm.tsx
   ✓ Step 2: Implemented email validation with regex /^[^\s@]+@[^\s@]+\.[^\s@]+$/
   ✓ Step 3: Added error message display with useState hook
   ✓ Step 4: Integrated useNavigate for dashboard redirect

FILES MODIFIED:
   - src/components/LoginForm.tsx (created)
   - src/utils/validators.ts (added 1 function)
   - tests/LoginForm.test.tsx (created, 8 tests)

ACCEPTANCE CRITERIA VERIFICATION:
   ✓ Criterion 1: Form validates email format using regex - VERIFIED
   ✓ Criterion 2: Form displays specific error messages - VERIFIED
   ✓ Criterion 3: User redirects to dashboard on success - VERIFIED

TESTING RESULTS:
   ✓ Unit tests: 8/8 passing
   ✓ Manual testing: Form validation works, redirects correctly

================================================================================
```

---

## 4. Complete Workflow Example: SPH Fluid Simulation

### Phase 1: Brainstorming

**User Request**: "Build a SPH fluid simulation web application"

**Brainstorm Agent**:
1. Clarifies: What physics properties? What visualization? What UI controls?
2. Researches: SPH algorithms, WebGL rendering options
3. Decomposes into dependency layers:

```json
{
  "tasks": [
    {
      "task": "Implement SPH Simulation Algorithm",
      "description": "Create core SPH physics simulation with particle interactions.",
      "steps": [
        {"step": 1, "description": "Implement spatial hash grid for neighbor search"},
        {"step": 2, "description": "Implement SPH kernel functions"},
        {"step": 3, "description": "Implement density and pressure computation"},
        {"step": 4, "description": "Implement force accumulation and integration"}
      ],
      "acceptance-criteria": "Simulation can reset to initial state. No NaN or Infinity after 1000 steps. Total energy conservation within 1% tolerance over 500 steps. Total momentum conservation within 1% tolerance. Boundary conditions correctly reflect particles.",
      "test-plan": {
        "unit": [
          "Simulation reset produces identical results from same seed",
          "Particle loading accepts valid data, rejects malformed input",
          "No NaN/Infinity in position/velocity after 1000 steps",
          "Energy conservation within 1% over 500 steps",
          "Momentum conservation within 1% over 500 steps",
          "Boundary conditions reflect particles at domain edges",
          "Kernel function returns zero beyond smoothing radius",
          "Density computation matches analytical solution for uniform distribution",
          "Pressure force is symmetric between particle pairs"
        ],
        "integration": [],
        "e2e-manual": []
      },
      "skills": ["tdd-workflow"],
      "complete": false
    },
    {
      "task": "Implement Canvas Particle Renderer",
      "description": "Create canvas-based particle visualization consuming simulation output.",
      "steps": [
        {"step": 1, "description": "Set up canvas element and render loop"},
        {"step": 2, "description": "Implement particle position mapping"},
        {"step": 3, "description": "Add velocity-based color mapping"},
        {"step": 4, "description": "Optimize for 5000+ particles"}
      ],
      "acceptance-criteria": "Particles render at correct positions. Color mapping reflects velocity magnitude. Renderer maintains 30+ FPS with 5000 particles.",
      "test-plan": {
        "unit": [
          "Static mock particles render at correct canvas coordinates",
          "Particle color mapping correctly reflects velocity magnitude from mock data",
          "Canvas clears and redraws without artifacts",
          "Renderer handles zero-particle and single-particle edge cases"
        ],
        "integration": [
          "Renderer displays real SPH algorithm output correctly",
          "Particle positions match simulation state within pixel tolerance",
          "Renderer maintains 30+ FPS with real algorithm at 5000 particles"
        ],
        "e2e-manual": []
      },
      "skills": ["tdd-workflow"],
      "complete": false
    },
    {
      "task": "Implement UI Controls and Layout",
      "description": "Create user interface for simulation control and parameter adjustment.",
      "steps": [
        {"step": 1, "description": "Create start/pause/reset button controls"},
        {"step": 2, "description": "Add parameter sliders for physics properties"},
        {"step": 3, "description": "Implement responsive layout"}
      ],
      "acceptance-criteria": "Start button triggers simulation. Pause button freezes state. Reset button restores initial conditions. Parameter changes affect simulation in real-time.",
      "test-plan": {
        "unit": [
          "Start/pause/reset buttons toggle correct states",
          "Parameter sliders clamp values within valid ranges",
          "Parameter change fires callback with new value"
        ],
        "integration": [
          "Start button triggers simulation loop and canvas rendering",
          "Parameter slider change propagates to SPH algorithm",
          "Reset button stops simulation and clears canvas"
        ],
        "e2e-manual": [
          "Visual: fluid behavior looks physically plausible",
          "Interactive: parameter adjustments produce visible real-time changes",
          "Responsive: layout adapts on mobile and desktop"
        ]
      },
      "skills": ["tdd-workflow", "verification-before-completion"],
      "complete": false
    }
  ]
}
```

### Phase 2: Execution

**Executor Agent** starts first task:

```
→ Pre-commit: (no changes)
→ Delegate to @worker: "Implement SPH Simulation Algorithm"
→ Worker implements, runs 9 unit tests, all pass
→ Worker writes PROGRESS.txt
→ Executor sets complete: true
→ Post-commit: "Implement SPH simulation algorithm"
```

**Executor Agent** continues to second task:

```
→ Pre-commit: (no new changes)
→ Delegate to @worker: "Implement Canvas Particle Renderer"
→ Worker runs 4 unit tests with mock data → all pass
→ Worker runs 3 integration tests with real SPH → all pass
→ Worker writes PROGRESS.txt
→ Executor sets complete: true
→ Post-commit: "Implement canvas particle renderer"
```

**Executor Agent** final task:

```
→ Pre-commit: (no new changes)
→ Delegate to @worker: "Implement UI Controls and Layout"
→ Worker runs 3 unit tests, 3 integration tests → all pass
→ Worker notes: e2e-manual tests require human
→ Worker writes PROGRESS.txt with manual test checklist
→ Executor sets complete: true
→ Post-commit: "Implement UI controls and layout"
→ Executor reports: "All tasks complete. 3 e2e-manual items require human verification."
```

---

## 5. Design Principles

### Separation of Concerns

| Phase      | Agent      | Output              | Next Agent |
|------------|------------|---------------------|------------|
| Planning   | Brainstorm | tasks.json          | Executor   |
| Coordinating| Executor   | Task briefings      | Worker     |
| Executing  | Worker     | Code + PROGRESS.txt | Executor   |

### Structured Communication

- **tasks.json** acts as a contract between agents
- **PROGRESS.txt** provides audit trail for each task
- Both are human-readable and machine-parseable

### Shift-Left Testing

Catch bugs at the earliest possible layer:

```
❌ BAD:  Algorithm bug found in E2E visual test
✅ GOOD: Algorithm bug caught by unit test (Layer 0)

❌ BAD:  Renderer position error found in integration
✅ GOOD: Renderer position tested with mock coordinates first
```

### Single Responsibility

- Brainstorm NEVER implements code
- Executor NEVER modifies code
- Worker NEVER commits changes
- Committer ONLY handles git operations

---

## 6. Quick Reference

### Invoking Agents

```bash
# Start brainstorming session
@brainstorm Build a user authentication system

# Execute task list (after tasks.json exists)
@executor

# Quick questions (lightweight agent)
@quick What is the time complexity of quicksort?
```

### tasks.json Field Reference

| Field      | Required | Type    | Description                          |
|------------|----------|---------|--------------------------------------|
| task       | Yes      | string  | Short name (3-80 chars)              |
| description| Yes      | string  | Single sentence summary (10-200 chars)|
| steps      | No       | array   | Ordered subtasks (0-15 items)        |
| acceptance-criteria| Yes| string | Measurable conditions (20-500 chars) |
| test-plan  | Yes      | object  | {unit: [], integration: [], e2e-manual: []} |
| skills     | No       | array   | Relevant skill names                 |
| complete   | Yes      | boolean | Always false initially               |

### Available Skills

| Skill                        | When to Use                              |
|------------------------------|------------------------------------------|
| `tdd-workflow`               | Test-driven development applicable       |
| `systematic-debugging`       | Encountering bugs or unexpected behavior |
| `setup-fresh-project`        | Starting new project                     |
| `installing-dependencies`    | Installing packages or tools             |
| `verification-before-completion` | Critical verification needed         |
| `writing-python`             | Python development with uv               |
| `writing-bash-scripts`       | Creating or refactoring shell scripts    |
| `cli-creator`                | Designing CLI interfaces                 |
| `mistake-notebook`           | Learning from historical problems        |

---

## License

Personal configuration - use freely for learning and reference.
