<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">給 AI 代理上規矩——讓它照資深工程師的標準做事。</h3>

<p align="center">
  <a href="README.md">English</a> &bull;
  <strong>繁體中文</strong> &bull;
  <a href="README_ja.md">日本語</a> &bull;
  <a href="README_de.md">Deutsch</a> &bull;
  <a href="README_ko.md">한국어</a>
</p>

<p align="center">
  <a href="#安裝">30 秒快速安裝</a> &bull;
  <a href="#插件一覽">瀏覽插件</a> &bull;
  <a href="#參與貢獻">一起貢獻</a>
</p>

---

## 痛點

AI 寫程式確實猛——但沒人管的話，它會跳規格、漏測試、指令爆掉就無腦重試，最後丟給你一堆沒文件的 API。你本來想讓 AI 幫你出貨，結果反過來幫 AI 擦屁股。

## 解法

**Agent Skill Lab** 是一套 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的插件市集，把工程紀律打包成可安裝的 skill。每個插件封裝一項開發規範——規格先行的 API 開發、指令執行衛生、結構化開發日誌、SQL DDL 慣例——讓你的 AI 代理自動遵守資深工程師等級的標準。

## 安裝

```bash
# 1. 加入市集（只需一次）
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. 安裝你需要的插件（名稱見下方表格）
claude plugin install dev-discipline@agent-skill-lab
claude plugin install narrated-deck@agent-skill-lab
# …其他插件同樣格式：  <plugin-name>@agent-skill-lab
```

> 在 Claude Code 工作階段內，可改用 slash 指令——`/plugin marketplace add …`、`/plugin install …`，再 `/reload-plugins`。執行 `/plugin` 可開啟互動式瀏覽器。

## 更新

插件**不是**用 `git pull` 更新的——Claude Code 會自行在 `~/.claude/plugins/` 下維護一份複本，所以手動 pull 這個 repo 不會有任何效果。發布新版本後，請在 Claude Code 內重新整理：

```bash
# 1. 重新抓取本市集的目錄
claude plugin marketplace update agent-skill-lab

# 2. 把指定插件更新到最新版
claude plugin update narrated-deck@agent-skill-lab

# 3. 重新載入讓新版生效（不需重開）
/reload-plugins
```

- **非自動**：像本市集這類第三方市集，自動更新**預設關閉**——更新是手動步驟（或在 `/plugin` UI 內逐一市集開啟）。
- **版本控管**：插件的 `version`（位於 `plugin.json`）決定能否更新——維護者沒 bump 版本，你就收不到變更；只 push commit 而不改版本，已安裝的複本不會更新。

## 插件一覽

| 插件 | Skills | 功能 |
|------|--------|------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | 規格先行 API 開發、安全指令執行、結構化開發日誌 |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL 設計標準——審計欄位、索引、命名、Mermaid ERD 產出 |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | 撰寫新插件的 YAML frontmatter 與目錄結構指引 |
| **narrated-deck** | `narrated-deck` | 把 PPT／PDF／大綱變成自帶旁白的 HTML 頁面——逐字幕 TTS 語音、場景轉場、內建播放器 |
| **research-discipline** | `government-research-stance` | 讓政府委託研究維持技術幕僚身段，避免越界扮演立法／立規範角色 |
| **deploy-preflight** | `deploy-preflight` | 上線前置檢查——診斷目標主機資源，把防護措施寫進部署腳本 |
| **notebooklm-cleaner** | `notebooklm-watermark-remover` | 移除 NotebookLM 匯出 PDF 的浮水印 |

### dev-discipline

三個 skill，讓你的 AI 代理開發流程滴水不漏：

- **api-dev-workflow** — 強制規格先行：先寫 API 規格、取得確認、實作、測試、產出 Postman Collection 與 OpenAPI 文件。每一步都不准跳。
- **command-execution** — 杜絕盲目重試。執行一次、檢查結果、分析根因、再決定下一步。涵蓋工作目錄驗證、前置條件檢查、背景程序管理。
- **dev-log** — 每個開發階段自動記錄到 `doc/dev-log.md`，結構化條目涵蓋：做了什麼、發現了什麼、目前測試狀態。

### sql-ddl-convention

一套完整的 SQL DDL 規則集：

- `BIGINT` 主鍵、必備審計欄位（`creator`、`createDate`、`modifier`、`modifyDate`、`removed`）
- 外鍵命名 `<tableName>_id`，不建 FK 約束（由應用層負責）
- 索引規則、預設 `NOT NULL`、`camelCase` 命名、禁用 ENUM、金額禁用 `FLOAT`
- 每次產出 DDL 同步產出 Mermaid ER 圖

### skill-and-agent-authoring

元插件：教你撰寫新 skill 與 agent 的完整指南，涵蓋 YAML frontmatter、觸發詞組慣例、目錄結構、工具配置。

## 專案結構

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── dev-discipline/         # API 流程、指令安全、開發日誌
│   ├── sql-ddl-convention/     # SQL DDL 標準 + Mermaid ERD
│   ├── skill-and-agent-authoring/  # 插件撰寫指南
│   ├── narrated-deck/          # PPT/PDF/大綱 → 旁白 HTML 頁面（TTS）
│   ├── research-discipline/    # 政府研究身段與口吻
│   ├── deploy-preflight/       # 上線前置檢查
│   └── notebooklm-cleaner/     # 移除 NotebookLM PDF 浮水印
├── banner.svg
└── README.md
```

## 參與貢獻

你有一套自己的開發紀律？把它做成插件，讓全世界的 AI 代理都學會。歡迎發 PR。

1. Fork 這個 repo
2. 在 `plugins/your-plugin-name/` 下建立你的插件
3. 參考 **skill-and-agent-authoring** 插件的格式
4. 發送 PR

## 授權

MIT

---

<p align="center">
  <sub>你對自己有什麼要求，就該對你的 AI 代理有一樣的要求。</sub>
</p>
