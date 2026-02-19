# Review Command

You are tasked with reviewing an opencode command file to ensure it follows best practices, uses opencode features properly, and adheres to Anthropic's prompting guidelines.

## Review Instructions

Carefully analyze the provided command file against the following criteria:

### 1. Command Structure & Format

- Verify the command has a clear, descriptive title
- Check for proper markdown formatting and structure
- Ensure the command has a clear purpose statement at the beginning
- Verify sections are logically organized and easy to follow

### 2. Opencode Command-Specific Features

- **Shell Output Injection**:
  - Verify use of backtick-wrapped !`command` syntax for embedding shell output (e.g., !`npm test`, !`git status` )
  - Check that injected output is wrapped in descriptive XML tags (e.g., `<git-status>`, `<file-list>`, `<test-results>`)
  - Ensure shell injection is used when the output provides valuable context for the task
  - Verify the command doesn't instruct the model to run commands when shell injection would be more appropriate
  - Confirm the backticks properly surround the !command syntax
- **$ARGUMENTS Handling**:
  - Check that `$ARGUMENTS` is properly wrapped in XML tags
  - Verify specific XML tag names for specific inputs (e.g., `<file-path>`, `<component-name>`)
  - Ensure default `<user-query>` tag is used for general/unspecified inputs
  - Confirm the command properly references the argument tag throughout
- **Tool Instructions**:
  - Verify clear, explicit mention of which tools to use (bash, read, write, edit, grep, glob, list, etc.)
  - Check that tool usage instructions are specific, not vague suggestions
- **Subagent Usage**:
  - Ensure subagents are explicitly named when appropriate (codebase-analyzer, codebase-locator, etc.)
  - Verify clear instructions on what input to provide to subagent prompts
  - Check that the expected output format from subagents is specified

### 3. Prompting Best Practices (Anthropic Guidelines)

- **Clarity**: Instructions should be clear, specific, and unambiguous
- **Context Setting**: Command should properly set context for the task
- **Step-by-Step Instructions**: Complex tasks should be broken down into clear steps
- **Examples**: Check if examples are provided where helpful
- **Output Format**: Verify clear specification of expected output format
- **Error Handling**: Check for instructions on handling edge cases or errors
- **Tone Guidelines**: Ensure appropriate tone instructions (concise, direct, helpful)

### 4. Performance & Efficiency

- **Parallel Operations**: Check if independent operations are batched for parallel execution
- **Resource Usage**: Verify efficient use of tools to minimize unnecessary operations
- **Context Optimization**: Ensure the command doesn't unnecessarily consume context
- **Agent Delegation**: Check if complex tasks are properly delegated to specialized agents
- **Output Structure**: Verify the command produces well-structured, parseable output

## Review Process

1. Read the entire command file thoroughly
2. Check for proper !`command` shell injection and $ARGUMENTS usage
3. Verify explicit tool and subagent instructions
4. Analyze prompting clarity and structure
5. Provide specific, actionable feedback with examples

## Review Report Template

After reviewing the command file, provide your feedback in the following format:

```markdown
# Command Review Report

## Command: [Command Name]

### Summary
[Brief 2-3 sentence overview of the command's purpose and overall quality]

### Strengths ✅
- [List positive aspects of the command]
- [Things that are well-implemented]
- [Good practices being followed]

### Issues Found 🔍

#### Critical Issues (Must Fix)
1. **[Issue Category]**: [Specific issue description]
   - Location: [Where in the file]
   - Impact: [Why this is critical]
   - Suggested Fix: [Concrete improvement suggestion]

#### Recommended Improvements
1. **[Improvement Area]**: [Description]
   - Current: [What exists now]
   - Suggested: [What would be better]
   - Example: [Code/text example if applicable]

#### Minor Suggestions
- [Less critical improvements or style suggestions]

### Opencode Command Compliance
- [ ] Shell injection !`command` syntax used correctly
- [ ] Shell output wrapped in descriptive XML tags
- [ ] $ARGUMENTS properly wrapped in XML tags
- [ ] Specific XML tag names for specific inputs
- [ ] Tools explicitly mentioned by name
- [ ] Subagents clearly identified with input instructions

### Anthropic Prompting Guidelines Compliance
- [ ] Clear and specific instructions
- [ ] Proper context setting
- [ ] Step-by-step breakdown for complex tasks
- [ ] Appropriate tone guidelines
- [ ] Output format specification

### Overall Score
**[Score]/10** - [Brief justification]

### Priority Actions
1. [Most important fix]
2. [Second priority]
3. [Third priority]
```

## Example Issues and Fixes

### Example 1: Missing Shell Output Injection

**Issue**: Command tells model to "run git status" instead of embedding the output
**Fix**: Use backtick-wrapped !command syntax with proper XML tagging

```markdown
# Instead of:
First, run git status to see what files have changed.

# Use:
<git-status>
!`git status --porcelain`
</git-status>

Analyze the changes shown in <git-status> above.
```

### Example 2: Improper $ARGUMENTS Handling

**Issue**: Command uses $ARGUMENTS without XML wrapping or uses generic tag for specific input
**Fix**: Wrap $ARGUMENTS in appropriate XML tags

```markdown
# Instead of:
Analyze the file at $ARGUMENTS

# Use (for specific file input):
<file-path>
$ARGUMENTS
</file-path>

Analyze the file at <file-path>.

# Or use (for general query):
<user-query>
$ARGUMENTS
</user-query>
```

### Example 3: Vague Tool Instructions

**Issue**: Command says "search for the pattern" without specifying which tool
**Fix**: Explicitly specify the tool to use

```markdown
# Instead of:
Search the codebase for usages of this function.

# Use:
Use the grep tool to search for "functionName(" pattern across all .ts and .tsx files.
```

### Example 4: Missing Subagent Instructions

**Issue**: Command mentions using a subagent without clear input instructions
**Fix**: Provide explicit subagent name and input format

```markdown
# Instead of:
Use an agent to analyze the codebase structure.

# Use:
Use the codebase-analyzer subagent with the following prompt:
"Analyze the authentication flow starting from login.tsx, including all middleware and API routes involved. Focus on security checks and token handling."
```

## Additional Notes

- Pay special attention to proper !`command` shell injection syntax (with backticks) vs instructing the model to run commands
- Understand that !`agentic metadata` or similar commands are valid shell injections, not instructions to the model
- Verify XML tag naming is semantic and consistent throughout the command
- Ensure $ARGUMENTS is always wrapped and referenced consistently
- Check that injected shell output provides valuable context, not just noise
- Verify subagent prompts are complete and self-contained

Remember: The goal is to ensure commands follow opencode's specific features and best practices

## Command File to Review

**IMPORTANT**: First, use the Read tool to read the entire file below without any line limits to ensure you have the complete context before beginning your evaluation.

<file>
$ARGUMENTS
</file>

**CRITICAL**: If the <file> tag below contains exactly $ARGUMENTS (meaning no file path was provided), stop immediately and ask the user to provide a command file path to review.
