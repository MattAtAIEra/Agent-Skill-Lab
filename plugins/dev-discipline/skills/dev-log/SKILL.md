---
name: dev-log
description: This skill should be used when "completing a development phase", "finishing a task milestone", "wrapping up implementation", or when the user asks to "update the dev log", "write a summary", "record what was done". Ensures development progress is persistently documented.
version: 1.0.0
---

# Dev Log Discipline

At the end of each development phase, write a work summary to `doc/dev-log.md` to ensure the development history is traceable and reviewable.

## When to Write

Write or update the dev log at these points:

- When a feature module is completed
- When a bug fix is completed
- When a refactoring task is completed
- When tests are written and passing
- When documentation is generated
- When a major issue is discovered and fixed
- Before the end of each conversation (if substantive development work was done)

## Log Entry Format

Each phase entry uses the following format:

```markdown
## Phase N: Brief Title

**Date**: YYYY-MM-DD
**Trigger**: What initiated this phase (user instruction, bug report, spec change, etc.)

### Completed Items

List completed work by category:

1. **Category Name** (e.g., Schema Changes, API Development, Testing)
   - Specific item 1
   - Specific item 2

### Discoveries & Fixes (if any)

Record issues encountered during development:

- **Symptom**: What was observed
- **Cause**: Root cause analysis
- **Fix**: How it was resolved
- **Lesson**: How to prevent it in the future

### Test Results

- Unit tests: X/Y passed
- Integration tests: X/Y passed
- Build: success/failure
```

## Content Requirements

### Must Include

- Phase number and title
- Date
- Trigger reason
- Completed items list (with file paths)
- Test results

### Should Include

- Issues discovered and how they were fixed
- Impact on other modules
- Remaining TODOs or follow-up work

### Avoid Including

- Overly trivial operational details (e.g., "installed a package")
- Duplicate code (use file paths instead)
- Subjective opinions or emotional descriptions

## File Location and Structure

The dev log file is located at `doc/dev-log.md`. Structure:

```markdown
# {Project Name} Dev Log

> This document records a work summary for each development phase, for review and tracking.

---

## Phase 1: ...
## Phase 2: ...
...

---

## TODO

- [ ] Items not yet completed
- [x] Completed items
```

## Procedure

1. Read the existing `doc/dev-log.md` (if it exists)
2. Determine the current latest Phase number
3. Append the new Phase entry before the TODO section
4. Update the TODO section
5. Save the file

If `doc/dev-log.md` does not exist, create a new file starting from Phase 1.

## Relationship with Other Disciplines

- **api-dev-workflow**: When API development is complete, record the list of new/modified endpoints in the log
- **command-execution**: When command execution issues are encountered, record them in the "Discoveries & Fixes" section

## Quality Standard

A good dev log entry should enable someone completely unfamiliar with the project (or a future AI agent) to:

1. Understand what was done in this phase
2. Know which files were changed
3. Understand why these changes were made
4. Know the current test status
5. Be aware of any known issues or remaining TODOs
