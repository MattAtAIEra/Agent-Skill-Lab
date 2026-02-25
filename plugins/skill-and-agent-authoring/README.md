# skill-and-agent-authoring

Claude Code plugin skill/agent 撰寫規範指引。確保建立 SKILL.md 和 agent markdown 時使用正確的 YAML frontmatter 格式與檔案結構。

## 安裝

```bash
claude plugin add git@github.com:your-org/skill-and-agent-authoring.git
```

## 涵蓋內容

- Skill YAML frontmatter 必填欄位與格式
- Agent YAML frontmatter 必填欄位與 `<example>` 區塊規範
- `tools` 正確的 JSON array 格式
- 常見錯誤對照與修正方式
- 建立前的驗證檢查清單

## 使用方式

安裝後自動生效。當你對 Claude 說：

- 「幫我建立一個新的 skill」
- 「我要寫一個 agent」
- 「幫我加一個 skill 到 plugin 裡」

Claude 會自動參照此規範產出正確格式的檔案。
