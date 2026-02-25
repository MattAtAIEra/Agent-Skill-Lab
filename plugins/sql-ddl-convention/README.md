# sql-ddl-convention

SQL DDL schema 設計規範 plugin，確保團隊在建立資料表時遵循一致的命名、主鍵、審計欄位與索引規則。

## 安裝

將此 plugin 複製或 symlink 到 Claude Code plugins 目錄：

```bash
ln -s /path/to/sql-ddl-convention ~/.claude/plugins/sql-ddl-convention
```

## 規則摘要

| 規則 | 說明 |
|------|------|
| 主鍵 | `id BIGINT`，所有表統一 |
| 審計欄位 | `creator`、`createDate`、`modifier`、`modifyDate`、`removed` |
| 外鍵 | `<tableName>_id BIGINT`，不建立 FK constraint |
| 索引 | 審計欄位 + 外鍵欄位皆建立索引，命名 `idx_<table>_<column>` |
| 命名 | 表名單數 camelCase、欄位 camelCase |
| NOT NULL | 預設 NOT NULL，nullable 需說明原因 |
| 禁用 | ENUM、FLOAT/DOUBLE 金額、資料庫專有功能 |
| 軟刪除 | 查詢預設 `WHERE removed = FALSE` |
| Many-to-Many | 複合主鍵、無審計欄位、表名 `<tableA>_<tableB>` |

## 包含內容

- **Skill**: `sql-ddl-convention` — 完整 DDL 設計規範與範例模板
- **Agent**: `schema-reviewer` — DDL 審查器，產出結構化審查報告

## 使用方式

### 產生 DDL

直接請 Claude 建立資料表，規範會自動套用：

> 幫我建立一個 user 表，包含 email 和 name

### 審查 DDL

請 Claude 使用 schema-reviewer agent 審查現有 DDL：

> 請幫我審查這段 DDL 是否符合規範
