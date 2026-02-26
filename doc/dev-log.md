# Agent Skill Lab 開發日誌

> 本文件記錄每個開發階段的工作摘要，供回顧與追蹤。

---

## Phase 1：建立 sql-ddl-convention Plugin

**日期**：2026-02-19
**觸發**：團隊需要統一的 RDBMS table schema 設計規範

### 完成項目

1. **Plugin 結構建立**
   - `plugins/sql-ddl-convention/.claude-plugin/plugin.json` — plugin 宣告
   - `plugins/sql-ddl-convention/skills/sql-ddl-convention/SKILL.md` — DDL 規範本體（14 條規則 + 產出模板 + 驗證檢查清單）
   - `plugins/sql-ddl-convention/agents/schema-reviewer.md` — DDL 審查 agent
   - `plugins/sql-ddl-convention/README.md` — plugin 說明文件

### 發現與修正

- **問題描述**：Plugin 安裝時發生 HTTP 500 錯誤
- **原因**：SKILL.md 缺少必要的 YAML frontmatter（`name`、`description`），agent 的 `description` 缺少 `<example>` 區塊，`tools` 使用了錯誤的 YAML list 格式
- **修正**：補上 SKILL.md frontmatter，agent description 加入 3 個 `<example>` 區塊，`tools` 改為 JSON array 格式 `["Read", "Glob", "Grep"]`
- **教訓**：建立任何 SKILL.md 或 agent 檔案前，必須先讀取一個現有官方 plugin 範例來驗證格式，不能僅依賴計畫文件

### 測試結果

- Plugin 載入：修正後成功
- Skill 觸發：待驗證
- Agent 觸發：待驗證

---

## Phase 2：建立 skill-and-agent-authoring Plugin

**日期**：2026-02-19
**觸發**：Phase 1 的錯誤經驗需要被記錄成規範，避免重複犯錯

### 完成項目

1. **Plugin 建立**
   - `plugins/skill-and-agent-authoring/.claude-plugin/plugin.json`
   - `plugins/skill-and-agent-authoring/skills/skill-and-agent-authoring/SKILL.md` — 完整的 skill/agent 撰寫規範，含 frontmatter 規格、4 個常見錯誤對照、驗證檢查清單
   - `plugins/skill-and-agent-authoring/README.md`

2. **從 sql-ddl-convention 拆出**
   - 原本錯誤地將此 skill 放在 sql-ddl-convention plugin 內，因為兩者受眾不同，拆為獨立 plugin

---

## Phase 3：加入 Mermaid ER Diagram 產出規則

**日期**：2026-02-25
**觸發**：使用者要求產出 DDL 時同時產出 Mermaid erDiagram

### 完成項目

1. **SKILL.md 更新** (`plugins/sql-ddl-convention/skills/sql-ddl-convention/SKILL.md`)
   - 新增規則 15：Mermaid ER Diagram 產出規範
   - 新增 Mermaid relationship 語法表與欄位標記說明
   - 新增完整 Mermaid erDiagram 範例（一般表 + many-to-many join table）
   - 驗證檢查清單新增 3 項 Mermaid 相關檢查
   - description 新增 "generate ER diagram"、"draw mermaid ERD" 觸發短語

---

## Phase 4：Marketplace 結構重構

**日期**：2026-02-26
**觸發**：需要以公司內部 git repo 方式分享 plugins，須符合 Anthropic marketplace 規範

### 完成項目

1. **目錄結構重構**
   - 三個 plugin（dev-discipline、sql-ddl-convention、skill-and-agent-authoring）搬入 `plugins/` 子目錄
   - 建立 `.claude-plugin/marketplace.json`，對齊官方 `claude-plugins-official` 格式
   - 建立根目錄 `.gitignore` 和 `README.md`（含安裝指引）

2. **Git 初始化與推送**
   - 初始化 git repo 並推送至 `https://github.com/MattAtAIEra/Agent-Skill-Lab.git`

### 發現與修正

- **問題描述**：完成 Phase 4 後未撰寫開發日誌
- **原因**：未遵守 dev-log skill 規範中「每次對話結束前」撰寫日誌的要求
- **修正**：補寫完整開發日誌，涵蓋 Phase 1–4
- **教訓**：即使是管理 plugin 的 repo 本身，也應遵守已安裝的 skill 規範

---

## 待辦

- [ ] 將所有 SKILL.md 內容翻譯為英文
- [ ] 驗證 sql-ddl-convention skill 觸發效果（測試建立 order + orderItem 表）
- [ ] 驗證 schema-reviewer agent 觸發效果
