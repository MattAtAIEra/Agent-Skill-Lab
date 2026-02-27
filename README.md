<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">Curated Claude Code plugins that give your AI agent real engineering discipline.</h3>

<p align="center">
  <a href="#installation">Install in 30 seconds</a> &bull;
  <a href="#plugins">Browse Plugins</a> &bull;
  <a href="#contributing">Contribute</a>
</p>

---

## The Problem

AI coding agents are powerful — but without guardrails they skip specs, forget tests, blindly retry failing commands, and produce undocumented APIs. You end up babysitting the agent instead of shipping.

## The Solution

**Agent Skill Lab** is a plugin marketplace for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that enforces engineering best practices as installable skills. Each plugin encodes a specific discipline — spec-first API development, command execution hygiene, structured dev logging, SQL DDL conventions — so your agent follows the same standards a senior engineer would.

## Installation

```bash
# 1. Add this marketplace (one-time)
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. Install the plugins you need
claude plugin install dev-discipline@agent-skill-lab
claude plugin install sql-ddl-convention@agent-skill-lab
claude plugin install skill-and-agent-authoring@agent-skill-lab
```

## Plugins

| Plugin | Skills | What It Enforces |
|--------|--------|------------------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | Spec-first API development, safe command execution, structured dev logging |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL design standards — audit fields, indexes, naming, Mermaid ERD generation |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | Correct YAML frontmatter and file structure for authoring new plugins |

### dev-discipline

Three skills that keep your agent's development workflow tight:

- **api-dev-workflow** — Forces spec-first development: write API spec, get user confirmation, implement, test, generate Postman collection & OpenAPI docs. No skipping steps.
- **command-execution** — Prevents blind retries. Execute once, check the result, analyze the root cause, then decide next steps. Covers working directory validation, prerequisite checks, and background process management.
- **dev-log** — Automatically documents each development phase in `doc/dev-log.md` with structured entries: what was done, what was discovered, and current test status.

### sql-ddl-convention

A comprehensive SQL DDL ruleset covering:

- `BIGINT` primary keys, mandatory audit fields (`creator`, `createDate`, `modifier`, `modifyDate`, `removed`)
- Foreign key naming (`<tableName>_id`), no FK constraints (application-layer responsibility)
- Index rules, `NOT NULL` by default, `camelCase` naming, no ENUMs, no `FLOAT` for money
- Auto-generated Mermaid ER diagrams alongside every DDL output

### skill-and-agent-authoring

The meta-plugin: a guide for writing new skills and agents with correct YAML frontmatter, trigger phrase conventions, directory structure, and tool configuration.

## Project Structure

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── dev-discipline/         # API workflow, command safety, dev logging
│   ├── sql-ddl-convention/     # SQL DDL standards + Mermaid ERD
│   └── skill-and-agent-authoring/  # Plugin authoring guide
├── banner.svg
└── README.md
```

## Contributing

Have a discipline you want to codify? PRs welcome.

1. Fork this repo
2. Create your plugin under `plugins/your-plugin-name/`
3. Use the **skill-and-agent-authoring** plugin as your formatting guide
4. Submit a PR

## License

MIT

---

<p align="center">
  <sub>Built for engineers who want their AI agents to follow the same standards they do.</sub>
</p>
