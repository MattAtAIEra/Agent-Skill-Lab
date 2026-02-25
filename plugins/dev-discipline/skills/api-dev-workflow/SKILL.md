---
name: api-dev-workflow
description: This skill should be used when the user asks to "build an API", "create a new endpoint", "add API functionality", or is about to start API development work. Enforces a spec-first discipline for API development to ensure quality and traceability.
version: 1.0.0
---

# API 開發流程紀律

API 開發必須遵循以下流程，不可跳過任何步驟。此紀律確保每個 API 端點都有完整的規格、測試與文件。

## 流程步驟

### 1. 撰寫 API 規格（Spec First）

在寫任何程式碼之前，先在 `doc/api-spec.md`（或專案指定的規格文件）中撰寫完整的 API 規格：

- HTTP Method 與路徑
- Request body（欄位、型別、是否必填、預設值、說明）
- Response body（含範例 JSON）
- 錯誤狀態碼與訊息
- 認證需求
- Query parameters（如適用）

規格格式範例：

```markdown
### POST /api/resources

建立資源。

**Request**
| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| name | string | Y | 資源名稱 |

**Response** `200`
{ "id": 1 }

**Error**
| 狀態碼 | 訊息 |
|--------|------|
| 400 | 缺少必要欄位 |
```

### 2. 取得用戶確認

將規格呈現給用戶審查。明確詢問：

- 端點設計是否符合需求
- 欄位定義是否完整
- 錯誤處理是否涵蓋所有情境
- 認證機制是否正確

**不可在未取得確認的情況下進入開發階段。**

### 3. 實作 API

依照已確認的規格進行開發：

- 建立路由檔案（遵循框架的 file-based routing 慣例）
- 實作 request validation
- 實作商業邏輯
- 實作 error handling（依照規格定義的錯誤碼）
- 確保回應格式與規格一致

### 4. 撰寫測試

針對每個端點撰寫整合測試：

- Happy path（正常流程）
- Validation error（缺少必填欄位、格式錯誤）
- Business logic error（404、409 等）
- 認證測試（如適用：無 token、無效 token、過期 token）

測試必須全部通過才能進入下一步。

### 5. 產出 Postman Collection

更新或建立 Postman Collection JSON：

- 每個端點一個 request
- 依模組分資料夾
- 包含 example request body
- 設定環境變數（baseUrl、token 等）
- 使用 Postman Collection v2.1 格式

### 6. 產出 OpenAPI (Swagger)

更新或建立 OpenAPI YAML：

- 使用 OpenAPI 3.0 格式
- 定義 reusable schemas
- 包含所有端點的完整定義
- 設定 security scheme（如適用）

## 檢查清單

每次 API 開發完成時，確認以下項目：

- [ ] API 規格已撰寫並取得用戶確認
- [ ] 程式碼實作完成
- [ ] 整合測試撰寫完成且全部通過
- [ ] Postman Collection 已更新
- [ ] OpenAPI Swagger 已更新
- [ ] 開發日誌已記錄（配合 `dev-log` skill）

## 常見違規

以下行為違反此紀律，應避免：

- 先寫程式碼再補規格
- 只寫規格不等確認就開始實作
- 跳過測試直接產出文件
- 只做 happy path 測試
- Postman 或 Swagger 只做部分端點
- API 變更後未同步更新規格與文件
