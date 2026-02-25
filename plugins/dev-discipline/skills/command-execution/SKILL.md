---
name: command-execution
description: This skill should be used when executing shell commands, "running terminal commands", "starting a dev server", "running build or test commands", or any Bash tool invocation. Prevents blind retries and ensures proper error analysis before reattempting.
version: 1.0.0
---

# 指令執行紀律

執行任何 shell 指令時，必須遵循以下規範，避免盲目重試浪費資源並製造混亂。

## 核心原則

**執行一次 → 檢查結果 → 分析原因 → 再決定下一步**

絕對不可在未確認前次結果的情況下重複執行同一指令。

## 執行前檢查

### 1. 確認工作目錄

在執行指令前，確認當前工作目錄是否正確：

- 專案根目錄 vs 子目錄（如 `app/`、`packages/web/`）
- 指令是否需要在特定目錄下執行（如 `nuxt dev` 需要在含 `nuxt.config.ts` 的目錄）
- 使用絕對路徑或 `--cwd` 參數避免目錄錯誤

錯誤示範：

```bash
# 在專案根目錄執行，但 nuxt.config.ts 在 app/ 下
npx nuxt dev --port 3333
```

正確示範：

```bash
# 明確指定正確目錄
cd /project/app && npx nuxt dev --port 3333
# 或使用 cwd 參數
npx nuxt dev --cwd /project/app --port 3333
```

### 2. 確認前置條件

- 相依服務是否已啟動（如資料庫、其他 server）
- 環境變數是否已設定
- 相依套件是否已安裝（`node_modules` 是否存在）
- Port 是否被佔用

## 執行後檢查

### 3. 檢查執行結果

每次指令執行後，**必須**確認結果：

- 檢查 exit code（0 = 成功，非 0 = 失敗）
- 閱讀 stdout/stderr 輸出
- 對於背景程序，檢查 log 檔確認是否成功啟動

背景程序啟動的正確流程：

```bash
# 1. 啟動
some-server > /tmp/server.log 2>&1 &

# 2. 等待啟動完成
sleep 3

# 3. 檢查 log 確認成功
cat /tmp/server.log

# 4. 或用 health check 確認
curl -s -o /dev/null -w "%{http_code}" http://localhost:3333/
```

### 4. 失敗時的處理流程

當指令失敗時，依以下順序處理：

1. **閱讀完整錯誤訊息** — 不要只看最後一行
2. **分析根本原因** — 是目錄錯誤？缺少依賴？Port 衝突？權限問題？
3. **制定修正方案** — 針對根本原因，不是盲目重試
4. **執行修正後重試** — 一次只改一件事，確認是否解決

禁止行為：

- 不看錯誤訊息就重試
- 同一指令連續執行超過 2 次
- 加 `--force` 或 `sudo` 繞過錯誤而不理解原因
- 同時啟動多個相同的背景程序

## 清理責任

### 5. 背景程序管理

啟動背景程序前，檢查是否已有相同程序在運行：

```bash
# 檢查是否已有 nuxt dev 在跑
ps aux | grep "nuxt dev" | grep -v grep

# 如果有，先停止再重啟
pkill -f "nuxt dev --port 3333"
sleep 1
```

啟動後記錄 PID，結束工作時清理。

## 特殊情境

### Dev Server 啟動

1. 確認工作目錄含框架設定檔
2. 確認 port 未被佔用
3. 背景啟動並等待
4. 檢查 log 確認 "ready" 或 "listening"
5. 用 curl health check 最終確認

### 資料庫操作

1. 確認資料庫服務已啟動
2. 確認連線參數正確
3. 執行前確認操作的影響範圍（DROP 會刪除所有資料）
4. 檢查執行結果，確認無 error

### 測試執行

1. 確認測試環境已就緒（dev server、DB）
2. 先跑一小批確認環境正常
3. 再跑完整測試
4. 失敗時逐一分析，不要重跑期望「自己好」

## 自我檢查

每次使用 Bash tool 時，回答以下問題：

1. 我在正確的目錄嗎？
2. 前置條件都滿足了嗎？
3. 上一次執行的結果我確認了嗎？
4. 如果失敗，我知道為什麼嗎？
