---
name: skill-and-agent-authoring
description: This skill should be used when the user asks to "create a skill", "create an agent", "write a SKILL.md", "write an agent markdown", "add a new skill to plugin", "add a new agent to plugin", or needs guidance on YAML frontmatter format, skill structure, agent structure, or plugin component authoring for Claude Code plugins.
version: 1.0.0
---

# Skill and Agent Authoring Guide

This skill provides the definitive YAML frontmatter specifications and file structure requirements for creating Claude Code plugin skills and agents. Always consult this skill before authoring any SKILL.md or agent markdown file.

## Critical Rule

**Before writing any SKILL.md or agent file, read an existing official example first** to verify the format. Never rely solely on a plan or memory — always validate against a real reference.

---

## Skill Authoring (SKILL.md)

### File Location

```
plugin-name/skills/skill-name/SKILL.md
```

### YAML Frontmatter (Required)

Every SKILL.md **must** begin with YAML frontmatter containing `name` and `description`:

```yaml
---
name: my-skill-name
description: This skill should be used when the user asks to "phrase 1", "phrase 2", "phrase 3", or discusses topic-area. Provides guidance on specific-domain.
version: 0.1.0
---
```

### Frontmatter Fields

| Field | Required | Format | Notes |
|-------|----------|--------|-------|
| `name` | **Yes** | lowercase, hyphens, 3-50 chars | Must start/end with alphanumeric |
| `description` | **Yes** | Third-person with trigger phrases | "This skill should be used when..." |
| `version` | No | Semantic version | e.g. `0.1.0` |
| `license` | No | SPDX identifier | e.g. `MIT` |

### Description Rules

- **Must use third person**: "This skill should be used when the user asks to..."
- **Must include specific trigger phrases** in quotes
- **Must list concrete scenarios** the skill covers
- **Bad**: "Provides help with schemas." (vague, no trigger phrases)
- **Good**: "This skill should be used when the user asks to \"create a table\", \"design a schema\", \"write DDL\", or discusses database naming conventions."

### Body Writing Style

- Use **imperative/infinitive form** (verb-first instructions)
- Do NOT use second person ("You should...")
- Target **1,500-2,000 words** for the body
- Move detailed content to `references/` subdirectory

### Directory Structure

```
skill-name/
├── SKILL.md              # Required — frontmatter + core instructions
├── references/           # Optional — detailed docs loaded on demand
│   └── detailed-guide.md
├── examples/             # Optional — working examples
│   └── sample.sql
└── scripts/              # Optional — utility scripts
    └── validate.sh
```

---

## Agent Authoring (agents/*.md)

### File Location

```
plugin-name/agents/agent-name.md
```

### YAML Frontmatter (Required)

Every agent file **must** begin with YAML frontmatter containing `name`, `description`, `model`, and `color`:

```yaml
---
name: my-agent
description: |
  Use this agent when the user asks to "do X", "check Y", or needs Z. Examples:

  <example>
  Context: User has just written code and wants review
  user: "Review my code for issues"
  assistant: "I'll use the my-agent agent to review your code."
  <commentary>
  User explicitly requesting review, trigger agent.
  </commentary>
  </example>

  <example>
  Context: Another triggering scenario
  user: "Check this file for problems"
  assistant: "Let me use my-agent to analyze the file."
  <commentary>
  File analysis request matches agent scope.
  </commentary>
  </example>

model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
---

Agent system prompt body goes here...
```

### Frontmatter Fields

| Field | Required | Format | Notes |
|-------|----------|--------|-------|
| `name` | **Yes** | lowercase, hyphens, 3-50 chars | Pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| `description` | **Yes** | Text + 2-4 `<example>` blocks | "Use this agent when..." |
| `model` | **Yes** | `inherit` / `sonnet` / `opus` / `haiku` | Prefer `inherit` |
| `color` | **Yes** | Color name | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` |
| `tools` | No | JSON array of tool names | e.g. `["Read", "Grep"]` |

### Description Rules (Critical)

The description is the **most important field** — it controls when Claude triggers the agent.

**Must include:**
1. Triggering conditions ("Use this agent when...")
2. **2-4 `<example>` blocks** showing usage scenarios
3. Each example must have: `Context`, `user`, `assistant`, `<commentary>`

**Bad**: "Reviews schemas for compliance." (no examples, no trigger conditions)
**Good**: Multiline with `|` pipe, trigger conditions, and 2-4 concrete examples.

### Tools Format

- Use **JSON array** format: `["Read", "Grep", "Glob"]`
- Do NOT use YAML list format (`- Read`)
- Do NOT use comma-separated string (`Read, Grep, Glob`)
- If omitted, agent has access to all tools
- Apply **principle of least privilege** — only grant tools the agent needs

### Color Guidelines

| Color | Use Case |
|-------|----------|
| `blue` / `cyan` | Analysis, review |
| `green` | Success-oriented, generation |
| `yellow` | Caution, validation |
| `red` | Critical, security |
| `magenta` | Creative, transformation |

### System Prompt (Body)

- Write in **second person** ("You are...", "You will...")
- Define clear responsibilities, process steps, and output format
- Keep under 10,000 characters
- Include edge case handling

---

## Common Mistakes to Avoid

### Mistake 1: Missing SKILL.md Frontmatter

```markdown
<!-- WRONG — no frontmatter -->
# My Skill
Content here...
```

```markdown
<!-- CORRECT -->
---
name: my-skill
description: This skill should be used when...
---
# My Skill
Content here...
```

### Mistake 2: Agent Missing `<example>` Blocks

```yaml
# WRONG — description without examples
description: Reviews code for issues.
```

```yaml
# CORRECT — description with examples
description: |
  Use this agent when... Examples:
  <example>
  Context: ...
  user: "..."
  assistant: "..."
  <commentary>...</commentary>
  </example>
```

### Mistake 3: Wrong Tools Format

```yaml
# WRONG — YAML list
tools:
  - Read
  - Grep

# WRONG — comma string
tools: Read, Grep, Glob

# CORRECT — JSON array
tools: ["Read", "Grep", "Glob"]
```

### Mistake 4: Skill Description in Wrong Person

```yaml
# WRONG
description: Use this skill when you need to create tables.

# CORRECT
description: This skill should be used when the user asks to "create a table"...
```

---

## Authoring Checklist

### Before Creating Any File

- [ ] Read at least one existing official plugin example to verify format

### Skill Checklist

- [ ] YAML frontmatter with `name` and `description`
- [ ] `description` uses third person with quoted trigger phrases
- [ ] Body uses imperative form, not second person
- [ ] Body under 3,000 words (ideally 1,500-2,000)
- [ ] Detailed content moved to `references/`

### Agent Checklist

- [ ] YAML frontmatter with `name`, `description`, `model`, `color`
- [ ] `description` includes 2-4 `<example>` blocks with `<commentary>`
- [ ] `model` set (prefer `inherit`)
- [ ] `color` set with appropriate meaning
- [ ] `tools` in JSON array format (if restricting)
- [ ] System prompt in second person with clear structure
