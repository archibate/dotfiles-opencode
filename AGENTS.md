# User Preferences

- DO NOT use **Unicode hyphen** `‑` (U+2011); Use **ASCII hyphen** `-` (U+002D).
- Use bash **heredoc** syntax for executing one-liners.
- Always response in Chinese.

## Coding Style

Follow the same pattern in existing codebase.

For fresh project:
- Use **4 spaces** for indent by default.

## Online References

- When you need docs for a library, use `context7` tools.
- If you are unsure how to implement something, use `gh_grep` to search code examples from GitHub.
- Use `websearch` and `webfetch` tools to get other online resources.

# Skills

**IMPORTANT**: If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

## How to Access Skills

Use the `skill` tool to access skill. When you invoke a skill, its content is loaded and presented to you—follow it directly.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (git-worktree, debugging) - these determine HOW to approach the task
2. **Implementation skills second** (frontend-design, mcp-builder) - these guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

- **Rigid** (SDD, debugging): Follow exactly. Don't adapt away discipline.
- **Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
