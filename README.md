<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">Curated Claude Code plugins that give your AI agent real engineering discipline.</h3>

<p align="center">
  <strong>English</strong> &bull;
  <a href="README_zh_TW.md">繁體中文</a> &bull;
  <a href="README_ja.md">日本語</a> &bull;
  <a href="README_de.md">Deutsch</a> &bull;
  <a href="README_ko.md">한국어</a>
</p>

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

# 2. Install the plugins you want (any name from the table below)
claude plugin install dev-discipline@agent-skill-lab
claude plugin install narrated-deck@agent-skill-lab
# …same pattern for any other plugin:  <plugin-name>@agent-skill-lab
```

> Inside a Claude Code session, use the slash-command equivalents — `/plugin marketplace add …`, `/plugin install …`, then `/reload-plugins`. Run `/plugin` for an interactive browser.

## Updating

Plugins are **not** updated by `git pull` — Claude Code keeps its own managed copy under `~/.claude/plugins/`, so pulling this repo by hand changes nothing. After a new version ships, refresh from inside Claude Code:

```bash
# 1. Re-fetch this marketplace's catalog
claude plugin marketplace update agent-skill-lab

# 2. Update a plugin to its latest version
claude plugin update narrated-deck@agent-skill-lab

# 3. Reload so the new version takes effect (no restart needed)
/reload-plugins
```

- **Not automatic:** third-party marketplaces have auto-update **off by default** — updating is a manual step (or opt in per-marketplace from the `/plugin` UI).
- **Version-gated:** a plugin's `version` in its `plugin.json` controls updates — you only receive changes when the maintainer bumps it; new commits without a bump don't reach installed copies.

## Plugins

| Plugin | Skills | What It Does |
|--------|--------|------------------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | Spec-first API development, safe command execution, structured dev logging |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL design standards — audit fields, indexes, naming, Mermaid ERD generation |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | Correct YAML frontmatter and file structure for authoring new plugins |
| **narrated-deck** | `narrated-deck` | Turn a PPT/PDF/outline into a self-contained narrated HTML page — per-subtitle TTS audio, scene transitions, built-in player |
| **research-discipline** | `government-research-stance` | Keeps government-commissioned research in a technical-staff stance, avoiding overreach into legislative/regulatory roles |
| **deploy-preflight** | `deploy-preflight` | Production deploy preflight — diagnose target-host resources and wire safeguards into deploy scripts |
| **notebooklm-cleaner** | `notebooklm-watermark-remover` | Remove the NotebookLM watermark from exported PDFs |

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
│   ├── skill-and-agent-authoring/  # Plugin authoring guide
│   ├── narrated-deck/          # PPT/PDF/outline → narrated HTML page (TTS)
│   ├── research-discipline/    # Government-research stance & tone
│   ├── deploy-preflight/       # Production deploy preflight checks
│   └── notebooklm-cleaner/     # Strip NotebookLM watermark from PDFs
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
