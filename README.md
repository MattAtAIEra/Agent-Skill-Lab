# Agent Skill Lab

公司內部 Claude Code plugin marketplace，包含團隊共用的開發規範與工具。

## 安裝方式

```bash
# 1. 加入此 marketplace（一次性）
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. 安裝需要的 plugin
claude plugin install dev-discipline@agent-skill-lab
claude plugin install sql-ddl-convention@agent-skill-lab
claude plugin install skill-and-agent-authoring@agent-skill-lab
```

## 收錄 Plugins

| Plugin | 說明 |
|--------|------|
| **dev-discipline** | API 開發流程、指令執行規範、開發日誌撰寫 |
| **sql-ddl-convention** | SQL DDL 設計規範（審計欄位、索引、命名、Mermaid ERD） |
| **skill-and-agent-authoring** | Plugin skill/agent 撰寫格式指引 |

## 目錄結構

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json    # Marketplace 宣告
├── plugins/
│   ├── dev-discipline/
│   ├── sql-ddl-convention/
│   └── skill-and-agent-authoring/
├── .gitignore
└── README.md
```
