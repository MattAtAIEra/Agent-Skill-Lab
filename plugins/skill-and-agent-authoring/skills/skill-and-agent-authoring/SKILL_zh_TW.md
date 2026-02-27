---
name: skill-and-agent-authoring
description: This skill should be used when the user asks to "create a skill", "create an agent", "write a SKILL.md", "write an agent markdown", "add a new skill to plugin", "add a new agent to plugin", or needs guidance on YAML frontmatter format, skill structure, agent structure, or plugin component authoring for Claude Code plugins.
version: 1.0.0
---

# Skill 與 Agent 撰寫指南

本 skill 提供建立 Claude Code plugin skill 與 agent 的完整 YAML frontmatter 規格與檔案結構要求。撰寫任何 SKILL.md 或 agent markdown 檔案前，務必先參考本指南。

## 重要原則

**在撰寫任何 SKILL.md 或 agent 檔案之前，先閱讀一個現有的官方範例**以驗證格式。切勿僅依賴計畫或記憶——務必對照實際參考。

---

## Skill 撰寫 (SKILL.md)

### 檔案位置

```
plugin-name/skills/skill-name/SKILL.md
```

### YAML Frontmatter（必要）

每個 SKILL.md **必須**以包含 `name` 和 `description` 的 YAML frontmatter 開頭：

```yaml
---
name: my-skill-name
description: This skill should be used when the user asks to "phrase 1", "phrase 2", "phrase 3", or discusses topic-area. Provides guidance on specific-domain.
version: 0.1.0
---
```

### Frontmatter 欄位

| 欄位 | 必要 | 格式 | 備註 |
|------|------|------|------|
| `name` | **是** | 小寫、連字號、3-50 字元 | 必須以英數字元開頭及結尾 |
| `description` | **是** | 第三人稱加觸發詞組 | "This skill should be used when..." |
| `version` | 否 | 語意化版本 | 例如 `0.1.0` |
| `license` | 否 | SPDX 識別碼 | 例如 `MIT` |

### Description 規則

- **必須使用第三人稱**："This skill should be used when the user asks to..."
- **必須包含具體的觸發詞組**，用引號括起
- **必須列出 skill 涵蓋的具體情境**
- **不佳**："Provides help with schemas."（太模糊，無觸發詞組）
- **良好**："This skill should be used when the user asks to \"create a table\", \"design a schema\", \"write DDL\", or discusses database naming conventions."

### 本文撰寫風格

- 使用**祈使句/不定式**（動詞開頭的指令）
- 不要使用第二人稱（"You should..."）
- 目標本文 **1,500-2,000 字**
- 詳細內容移至 `references/` 子目錄

### 目錄結構

```
skill-name/
├── SKILL.md              # 必要——frontmatter + 核心指令
├── references/           # 選用——按需載入的詳細文件
│   └── detailed-guide.md
├── examples/             # 選用——實際範例
│   └── sample.sql
└── scripts/              # 選用——工具腳本
    └── validate.sh
```

---

## Agent 撰寫 (agents/*.md)

### 檔案位置

```
plugin-name/agents/agent-name.md
```

### YAML Frontmatter（必要）

每個 agent 檔案**必須**以包含 `name`、`description`、`model` 和 `color` 的 YAML frontmatter 開頭：

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

### Frontmatter 欄位

| 欄位 | 必要 | 格式 | 備註 |
|------|------|------|------|
| `name` | **是** | 小寫、連字號、3-50 字元 | 格式：`^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| `description` | **是** | 文字 + 2-4 個 `<example>` 區塊 | "Use this agent when..." |
| `model` | **是** | `inherit` / `sonnet` / `opus` / `haiku` | 建議使用 `inherit` |
| `color` | **是** | 顏色名稱 | `blue`、`cyan`、`green`、`yellow`、`magenta`、`red` |
| `tools` | 否 | JSON 陣列的工具名稱 | 例如 `["Read", "Grep"]` |

### Description 規則（關鍵）

description 是**最重要的欄位**——它控制 Claude 何時觸發此 agent。

**必須包含：**
1. 觸發條件（"Use this agent when..."）
2. **2-4 個 `<example>` 區塊**展示使用情境
3. 每個範例必須包含：`Context`、`user`、`assistant`、`<commentary>`

**不佳**："Reviews schemas for compliance."（無範例、無觸發條件）
**良好**：使用 `|` 管道符的多行文字，包含觸發條件和 2-4 個具體範例。

### Tools 格式

- 使用 **JSON 陣列**格式：`["Read", "Grep", "Glob"]`
- 不要使用 YAML 列表格式（`- Read`）
- 不要使用逗號分隔字串（`Read, Grep, Glob`）
- 若省略，agent 將擁有所有工具的存取權
- 遵循**最小權限原則**——僅授予 agent 所需的工具

### 顏色指引

| 顏色 | 使用情境 |
|------|---------|
| `blue` / `cyan` | 分析、審查 |
| `green` | 成功導向、生成 |
| `yellow` | 警告、驗證 |
| `red` | 關鍵、安全性 |
| `magenta` | 創意、轉換 |

### System Prompt（本文）

- 使用**第二人稱**撰寫（"You are..."、"You will..."）
- 定義清楚的職責、流程步驟與輸出格式
- 保持在 10,000 字元以內
- 包含邊界情況處理

---

## 常見錯誤

### 錯誤 1：SKILL.md 缺少 Frontmatter

```markdown
<!-- 錯誤——沒有 frontmatter -->
# My Skill
Content here...
```

```markdown
<!-- 正確 -->
---
name: my-skill
description: This skill should be used when...
---
# My Skill
Content here...
```

### 錯誤 2：Agent 缺少 `<example>` 區塊

```yaml
# 錯誤——description 沒有範例
description: Reviews code for issues.
```

```yaml
# 正確——description 包含範例
description: |
  Use this agent when... Examples:
  <example>
  Context: ...
  user: "..."
  assistant: "..."
  <commentary>...</commentary>
  </example>
```

### 錯誤 3：Tools 格式錯誤

```yaml
# 錯誤——YAML 列表
tools:
  - Read
  - Grep

# 錯誤——逗號字串
tools: Read, Grep, Glob

# 正確——JSON 陣列
tools: ["Read", "Grep", "Glob"]
```

### 錯誤 4：Skill Description 使用錯誤人稱

```yaml
# 錯誤
description: Use this skill when you need to create tables.

# 正確
description: This skill should be used when the user asks to "create a table"...
```

---

## 撰寫檢查清單

### 建立任何檔案之前

- [ ] 已閱讀至少一個現有的官方 plugin 範例以驗證格式

### Skill 檢查清單

- [ ] YAML frontmatter 包含 `name` 和 `description`
- [ ] `description` 使用第三人稱，包含引號括起的觸發詞組
- [ ] 本文使用祈使句，非第二人稱
- [ ] 本文在 3,000 字以內（理想為 1,500-2,000）
- [ ] 詳細內容已移至 `references/`

### Agent 檢查清單

- [ ] YAML frontmatter 包含 `name`、`description`、`model`、`color`
- [ ] `description` 包含 2-4 個帶 `<commentary>` 的 `<example>` 區塊
- [ ] `model` 已設定（建議使用 `inherit`）
- [ ] `color` 已設定，語意適當
- [ ] `tools` 使用 JSON 陣列格式（若有限制）
- [ ] System prompt 使用第二人稱，結構清晰
