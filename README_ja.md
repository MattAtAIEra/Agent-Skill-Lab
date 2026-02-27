<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">「勝手にやるな、手順を踏め」—— AIエージェントに開発規律を仕込むプラグイン集</h3>

<p align="center">
  <a href="README.md">English</a> &bull;
  <a href="README_zh_TW.md">繁體中文</a> &bull;
  <strong>日本語</strong> &bull;
  <a href="README_de.md">Deutsch</a> &bull;
  <a href="README_ko.md">한국어</a>
</p>

<p align="center">
  <a href="#インストール">30秒でインストール</a> &bull;
  <a href="#プラグイン一覧">プラグイン一覧</a> &bull;
  <a href="#コントリビュート">コントリビュート</a>
</p>

---

## 課題

AIコーディングエージェントは優秀です。ただし手綱を緩めると、仕様をすっ飛ばし、テストを書かず、コケたコマンドを闇雲にリトライし、ドキュメントゼロのAPIを量産します。「AIに任せて効率化」のはずが、気づけばエージェントのお守り係になっている——そんな経験はありませんか？

## 解決策

**Agent Skill Lab** は [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 向けのプラグインマーケットプレイスです。エンジニアリングのベストプラクティスを、インストール可能なスキルとして提供します。仕様駆動のAPI開発、コマンド実行の衛生管理、構造化された開発ログ、SQL DDL規約——各プラグインがシニアエンジニアと同じ水準の規律をエージェントに徹底させます。

## インストール

```bash
# 1. マーケットプレイスを追加（初回のみ）
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. 必要なプラグインをインストール
claude plugin install dev-discipline@agent-skill-lab
claude plugin install sql-ddl-convention@agent-skill-lab
claude plugin install skill-and-agent-authoring@agent-skill-lab
```

## プラグイン一覧

| プラグイン | スキル | 規律の内容 |
|-----------|--------|-----------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | 仕様駆動API開発、安全なコマンド実行、構造化開発ログ |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL設計標準——監査カラム、インデックス、命名規約、Mermaid ERD生成 |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | プラグイン作成のためのYAMLフロントマターとディレクトリ構成ガイド |

### dev-discipline

エージェントの開発フローを隙なく管理する3つのスキル：

- **api-dev-workflow** — 仕様駆動開発を徹底：API仕様の作成 → ユーザー確認 → 実装 → テスト → Postman Collection & OpenAPIドキュメント生成。工程の飛ばしは一切許しません。
- **command-execution** — 闇雲なリトライを防止。一度実行 → 結果確認 → 原因分析 → 次のアクションを判断。作業ディレクトリの検証、前提条件チェック、バックグラウンドプロセス管理をカバー。
- **dev-log** — 各開発フェーズを `doc/dev-log.md` に自動記録。実施内容、発見事項、テスト状況を構造化エントリで残します。

### sql-ddl-convention

包括的なSQL DDLルールセット：

- `BIGINT` 主キー、必須監査カラム（`creator`、`createDate`、`modifier`、`modifyDate`、`removed`）
- 外部キー命名規則 `<tableName>_id`、FK制約なし（アプリケーション層で管理）
- インデックスルール、デフォルト `NOT NULL`、`camelCase` 命名、ENUM禁止、金額に `FLOAT` 禁止
- DDL出力と同時にMermaid ERダイアグラムを自動生成

### skill-and-agent-authoring

メタプラグイン：新しいスキルやエージェントを作成するためのガイド。YAMLフロントマター、トリガーフレーズの慣例、ディレクトリ構成、ツール設定を網羅。

## プロジェクト構成

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── dev-discipline/         # APIワークフロー、コマンド安全性、開発ログ
│   ├── sql-ddl-convention/     # SQL DDL標準 + Mermaid ERD
│   └── skill-and-agent-authoring/  # プラグイン作成ガイド
├── banner.svg
└── README.md
```

## コントリビュート

あなたのチームで培った開発規律、プラグインにして共有しませんか？PRをお待ちしています。

1. このリポジトリをフォーク
2. `plugins/your-plugin-name/` 配下にプラグインを作成
3. **skill-and-agent-authoring** プラグインをフォーマットガイドとして参照
4. PRを提出

## ライセンス

MIT

---

<p align="center">
  <sub>自分に課す基準を、AIにも。そういうエンジニアのために作りました。</sub>
</p>
