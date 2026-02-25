# dev-discipline

開發紀律 Plugin — 提供 Claude Code 在軟體開發過程中應遵循的紀律規範。

## 包含的 Skills

| Skill | 說明 |
|-------|------|
| `api-dev-workflow` | API 開發流程紀律：spec → 確認 → 開發 → 測試 → Postman → Swagger |
| `command-execution` | 指令執行紀律：避免盲目重試，確認結果後再行動 |
| `dev-log` | 開發日誌紀律：每個階段完成時記錄摘要到 `doc/dev-log.md` |

## 安裝

在專案的 `.claude/settings.json` 加入：

```json
{
  "plugins": [
    "/path/to/agent-skill-lab/dev-discipline"
  ]
}
```

或使用 `/install-plugin` 指令。

## 使用方式

Skills 會在符合觸發條件時自動啟用，也可手動呼叫：

- `/api-dev-workflow` — 進入 API 開發流程
- `/command-execution` — 查看指令執行規範
- `/dev-log` — 撰寫或更新開發日誌
