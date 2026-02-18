---
name: mistake-notebook
description: |
    Skill to query and update a mistake notebook to memorize mistake. Use this skill when:
    1. Encountered a severe problem, needs to recall for historical problem solving experience
    2. After fixed a severe mistake with a clear solution valuable to be recorded
    3. User requested 'Do not make this mistake again'
---
# Mistake Notebook

## Location

Mistake Notebook appear in two locations:

- Project-local Mistake Notebook: `MISTAKE.md` in project root folder.
- Universal Mistake Notebook: `~/MISTAKE.md` in user home directory.

Mistake Notebook is used to record common mistakes made in previous conversation, memorizing problem solving experience for future use. Agents can:

1. Read Mistake Notebook for quick problem -> solution look up.
2. Append to Mistake Notebook when new problem being solved.

This prevents agents from making the same mistake again.

### Project-local vs Universal

Project-local Mistake Notebook `MISTAKE.md`:
- Record **project related** mistakes not applies universally.
- Tracked by git if in a git repository.

Universal Mistake Notebook `~/MISTAKE.md`:
- Record **generic**, **programmatic** mistakes that has no project-local context.
- Appears in user home directory.

## Triggers

### Trigger 1: Severe Problem Encountered

When encounter a severe problem:

- Look for solution in both `MISTAKE.md` and `~/MISTAKE.md`.
- If found:
    - Try fix the problem using the solution found in Mistake Notebook.
    - If problem fixed:
        - Done.
    - If problem persists:
        - Figure out why the existing solution in Mistake Notebook didn't work.
        - If the problem solved:
            - Goto 'Trigger 2: Severe Problem Fixed'
- If not found:
    - Work out the problem on ourselves.
    - If the problem solved:
        - Goto 'Trigger 2: Severe Problem Fixed'

### Trigger 2: Severe Problem Fixed

After you fixed a severe mistake:

- If the problem is solved with a **clear solution** that is **valuable to be recorded**:
    - Goto 'Memorizing Problem Solutions'.

### Trigger 3: User Ask for Memorizing Mistake

When user requested 'Do not make this mistake again':

- If the problem not solved yet according to conversation context:
    - Work on solve the problem first.
    - If the problem is solved:
        - Report user for your discovery.
        - Goto 'Memorizing Problem Solutions'.
- If the problem is solved as user intented:
    - Goto 'Memorizing Problem Solutions'.

## Memorizing Problem Solutions

- If a problem is solved with a clear solution:
    - Check if this problem is already recorded in `MISTAKE.md` and `~/MISTAKE.md`:
        - Already recorded:
            - If the recorded solution is not working or out-of-date:
                - Update the recorded solution according to 'Mistake Solution Format'.
        - Not recorded yet:
            - If the problem is related to this project:
                - Choose `MISTAKE.md`.
            - If the problem is generic and universal:
                - Choose `~/MISTAKE.md`.
            - Append soltuion to the choosen Mistake Notebook according to 'Mistake Solution Format'.
            - Make a brief report in response for:
                - The mistake you made.
                - What you learnt from this mistake.
                - What is the solution to the problem.
                - Report that you have updated the Mistake Notebook.

## Mistake Solution Format

Mistake Notebook maintains a quick problem -> solution look up reference in the following format:

```markdown
# Mistake Notebook

This is the Mistake Notebook, use the mistake-notebook skill to retrive more details.

Below is a list of mistakes I previously made and solved:

## Mistake - [A short title]

- Creation Date: YYYY-MM-DD
- Last Update Date: YYYY-MM-DD
- Project: [project folder path when this mistake was found]
- Branch: [branch when this mistake was happening]
- Commit: [commit SHA when this mistake was happening]

### Problem:

[list situations when the problem occurred:]
- XXX fails.
- YYY reports ZZZ.
- ...

### Insights:

[list your insights and discoveries when solving this problem:]
- This is because XXX lacks AAA.
- I found that YYY depends on BBB for CCC.
- ...

### Solution:

[A brief explaination (<10 words) on how this problem was solved.]

[list steps how this problem was solved:]
- Try turn on AAA.
- Try add BBB for CCC.
- ...
- And XXX fixed.
```

## Edge Cases

- If Mistake Notebook not exist, create one.
- If Mistake Notebook exist, append to it.
- If writting into Mistake Notebook failed due to permission issues, report by outputing response in the 'Mistake' format.
