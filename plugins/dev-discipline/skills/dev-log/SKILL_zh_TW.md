---
name: dev-log
description: This skill should be used when "completing a development phase", "finishing a task milestone", "wrapping up implementation", or when the user asks to "update the dev log", "write a summary", "record what was done". Ensures development progress is persistently documented.
version: 1.0.0
---

# 開發日誌紀律

每個開發階段完成時，將工作摘要寫入 `doc/dev-log.md`，確保開發歷程可追溯、可回顧。

## 何時撰寫

在以下時機點撰寫或更新開發日誌：

- 一個功能模組開發完成時
- 一個 bug 修復完成時
- 一個重構作業完成時
- 測試撰寫完成且通過時
- 文件產出完成時
- 發現並修正重大問題時
- 每次對話結束前（如有實質開發工作）

## 日誌格式

每個階段的日誌條目使用以下格式：

```markdown
## Phase N：簡短標題

**日期**：YYYY-MM-DD
**觸發**：什麼原因開始這個階段（用戶指示、bug 回報、規格變更等）

### 完成項目

依類別列出完成的工作：

1. **類別名稱**（如：Schema 變更、API 開發、測試）
   - 具體項目 1
   - 具體項目 2

### 發現與修正（如有）

記錄開發過程中遇到的問題：

- **問題描述**：什麼現象
- **原因**：根本原因分析
- **修正**：如何解決
- **教訓**：未來如何避免

### 測試結果

- 單元測試：X/Y 通過
- 整合測試：X/Y 通過
- Build：成功/失敗
```

## 日誌內容要求

### 必須包含

- 階段編號與標題
- 日期
- 觸發原因
- 完成項目清單（含檔案路徑）
- 測試結果

### 應該包含

- 發現的問題與修正方式
- 對其他模組的影響
- 待辦事項或後續工作

### 避免包含

- 過於瑣碎的操作細節（如「安裝了某個套件」）
- 重複的程式碼（用檔案路徑代替）
- 主觀評價或情緒描述

## 檔案位置與結構

開發日誌檔案位於 `doc/dev-log.md`。結構如下：

```markdown
# {專案名稱} 開發日誌

> 本文件記錄每個開發階段的工作摘要，供回顧與追蹤。

---

## Phase 1：...
## Phase 2：...
...

---

## 待辦

- [ ] 尚未完成的項目
- [x] 已完成的項目
```

## 操作流程

1. 讀取現有的 `doc/dev-log.md`（如果存在）
2. 確認目前最新的 Phase 編號
3. 在檔案末尾（待辦區段之前）追加新的 Phase 條目
4. 更新待辦區段
5. 儲存檔案

如果 `doc/dev-log.md` 不存在，建立新檔案並從 Phase 1 開始。

## 與其他紀律的關聯

- **api-dev-workflow**：API 開發完成時，在日誌中記錄新增/修改的端點清單
- **command-execution**：遇到指令執行問題時，在「發現與修正」區段記錄

## 品質標準

一份好的開發日誌條目應該讓一個完全不了解專案的人（或未來的 AI agent）能夠：

1. 理解這個階段做了什麼
2. 知道改了哪些檔案
3. 了解為什麼做這些改動
4. 知道目前的測試狀態
5. 了解有什麼已知問題或待辦事項
