# deploy-preflight

Production 部署前環境檢查 plugin。在產生或修改部署腳本前，自動向使用者確認目標主機環境資訊，診斷潛在風險，並在腳本中加入防護措施。

## 包含的 Skill

### deploy-preflight

在產生 `setup.sh`、`deploy.sh` 等部署腳本之前觸發，執行以下流程：

1. **詢問目標環境** — 雲端供應商、OS、記憶體、swap、磁碟空間等
2. **產出診斷報告** — 標示各項目的風險等級（HIGH / MEDIUM / LOW）
3. **自動加入防護** — 根據診斷結果在腳本中加入 swap 建立、磁碟檢查、tmux 提醒等前置步驟

## 觸發時機

- 手動：`/deploy-preflight`
- 自然語言：「幫我寫一個 setup.sh」、「deploy to EC2」、「建立部署腳本」等
