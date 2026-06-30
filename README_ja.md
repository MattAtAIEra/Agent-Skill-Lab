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

# 2. 必要なプラグインをインストール（名前は下の表を参照）
claude plugin install dev-discipline@agent-skill-lab
claude plugin install narrated-deck@agent-skill-lab
# …他のプラグインも同じ形式：  <plugin-name>@agent-skill-lab
```

> Claude Code セッション内では slash コマンドでも操作できます——`/plugin marketplace add …`、`/plugin install …`、その後 `/reload-plugins`。`/plugin` で対話的ブラウザが開きます。

## 更新

プラグインは `git pull` では更新**されません**。Claude Code は `~/.claude/plugins/` 配下に独自の管理コピーを保持するため、このリポジトリを手動で pull しても何も変わりません。新バージョンが公開されたら、Claude Code 内で再取得してください：

```bash
# 1. このマーケットプレイスのカタログを再取得
claude plugin marketplace update agent-skill-lab

# 2. プラグインを最新バージョンに更新
claude plugin update narrated-deck@agent-skill-lab

# 3. 再読み込みして新バージョンを反映（再起動不要）
/reload-plugins
```

- **自動ではありません**：本マーケットプレイスのようなサードパーティ市場は自動更新が**デフォルトで無効**です。更新は手動（または `/plugin` UI からマーケットプレイスごとに有効化）。
- **バージョン管理**：プラグインの `version`（`plugin.json` 内）が更新を制御します。メンテナーがバージョンを上げない限り変更は届かず、バージョンを上げずに commit を push してもインストール済みコピーには反映されません。

## プラグイン一覧

| プラグイン | スキル | 機能 |
|-----------|--------|------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | 仕様駆動API開発、安全なコマンド実行、構造化開発ログ |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL設計標準——監査カラム、インデックス、命名規約、Mermaid ERD生成 |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | プラグイン作成のためのYAMLフロントマターとディレクトリ構成ガイド |
| **narrated-deck** | `narrated-deck` | PPT／PDF／アウトラインを自己完結型のナレーション付きHTMLページに——字幕ごとのTTS音声、シーン遷移、内蔵プレーヤー |
| **research-discipline** | `government-research-stance` | 政府委託研究を技術スタッフの立場に保ち、立法・規制側への越境を防ぐ |
| **deploy-preflight** | `deploy-preflight` | 本番デプロイのプリフライト——対象ホストのリソースを診断し、デプロイスクリプトに安全策を組み込む |
| **notebooklm-cleaner** | `notebooklm-watermark-remover` | エクスポートしたPDFからNotebookLMの透かしを除去 |

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
│   ├── skill-and-agent-authoring/  # プラグイン作成ガイド
│   ├── narrated-deck/          # PPT/PDF/アウトライン → ナレーション付きHTML（TTS）
│   ├── research-discipline/    # 政府研究のスタンスと論調
│   ├── deploy-preflight/       # 本番デプロイのプリフライトチェック
│   └── notebooklm-cleaner/     # NotebookLMのPDF透かしを除去
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
