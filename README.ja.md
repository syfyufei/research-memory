[**English**](README.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

Academic research really works like:

1. **研究のサイクルは、思っていたよりずっと長くなります。**
2. **同時に進めるリポジトリは、思っていたよりずっと多くなります。**
3. **プロジェクトに戻ってくると、どこまで進めたか忘れてしまいます。**

AIアシスタントと開発する皆さんなら、こんな光景に見覚えがあるでしょう：

> 3ヶ月も放置されていたリポジトリを開き、
> `git log` を上から下までスクロールし、
> notebook、スクリプト、論文の草案はすべてそこにあるのに、
> 頭に浮かぶのはたった一つの問い：
> **「前回、どこまで進んでたっけ？」**

さらに厄介なのが：
**あなたも忘れたし、AIアシスタントも忘れてしまった。**
新しい対話を始めると、AIアシスタントは「現在の数画面のコンテキスト」しか知らず、
過去数ヶ月のプロジェクトでの試行錯誤や、回り道、ブレークスルーについては全く理解していません。

`research-memory` は、開発プロセスにおいて**真に「長期的な」プロジェクトレベルの記憶層**を構築することを目指しています：

- 汎用RAGシステムを目指すのではなく、文献の記憶を助けるわけでもありません；
- このプロジェクトであなたとAIアシスタントが成し遂げたことを忠実に記録します：
  **何をしたか、どうしたか、なぜその方法を選んだか、次に何をするか**。

つまり：

> 「未来のあなた + 現在のAIアシスタント」が、
> 「過去のあなた」がたどった道をシームレスに引き継げるようにし、
> 毎回空白の会話から一からやり直すのではなくします。


## 機能概要（手短に）

`research-memory` は、学術研究プロジェクト専用に設計されたClaude Codeスキル/Pythonツールで、3つの重要な機能を提供します：

1. **セッション開始：`research_memory_bootstrap`**
   - `memory/` ディレクトリから取得：
     - プロジェクト概要（研究課題、仮説、データソース...）
     - 最近のN件のdevlogエントリ
     - 現在のTODOリスト
   - 自動的に「最近の進捗 + 推奨作業計画」を生成

2. **セッション記録：`research_memory_log_session`**
   - 研究作業を構造化して記録：
     - `devlog.md`：研究フェーズ別に整理（DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes）
     - `experiments.csv`：実験ごとに1行（hypothesis/dataset/model/metrics/notes...）
     - `decisions.md`：重要な決定とその理由/代替案
     - `todos.md`：新しい項目を追加し、完了したものを `[x]` としてマーク

3. **履歴検索：`research_memory_query_history`**
   - キーワード + シンプルなフィルター（日付 / フェーズ / タイプ）で検索：
     - `devlog.md`
     - `decisions.md`
     - `experiments.csv`
   - 要約 + 重要な抜粋を返します。

**すべてローカルテキストファイル（Markdown + CSV）ベースで、Gitと相性が良く、手動で編集可能で、外部サービス依存は一切ありません。**

---

## アーキテクチャ概要

全体構造：

```text
research-memory/
├── handlers.py        # スキルのPython実装とCLIエントリーポイント
├── SKILL.md           # Claude Codeスキル記述（ツール定義）
├── config/
│   └── config.json    # スキル動作設定
├── .claude/
│   ├── CLAUDE.md      # プロジェクトレベル指示、Claudeにいつこのスキルを使用するかを伝える
│   └── settings.local.json  # Claude Codeローカル設定例
└── memory/            # 実際の「プロジェクト記憶層」（自動作成可能）
    ├── project-overview.md  # 長期的プロジェクト情報
    ├── devlog.md            # 開発/分析ログ（セッション + フェーズ別）
    ├── decisions.md         # 重要決定記録
    ├── experiments.csv      # 実験テーブル（構造化）
    └── todos.md             # TODO / 未解決問題
```

コアコンポーネント：

* **スキル層**

  * `SKILL.md`は3つのツールを定義：

    * `research_memory_bootstrap`
    * `research_memory_log_session`
    * `research_memory_query_history`
  * Claude Codeが`handlers.py`内の対応する関数を呼び出す。

* **バックエンド層**

  * `MemoryBackend`はすべてのファイルI/O、設定読み込み、TODO処理ロジックをカプセル化：

    * 現在はローカルMarkdown + CSV；
    * 将来的にはSQLite / ベクトルデータベース / MCPサーバーに置換可能で、外側インターフェースは変更不要。

---

## インストール

### システム要件

* **Claude Code**（デスクトップ版 / VS Code / JetBrainsプラグインすべて動作）
* その他の追加依存関係はありません

### プラグインマーケットプレイスインストール（推奨）

Adrianの個人プラグインマーケットプレイスを使用してResearch Memoryをインストール：

1. **マーケットプレイスを追加**：

   ```bash
   claude plugin marketplace add https://github.com/syfyufei/adrian-marketplace
   ```

2. **Research Memoryをインストール**：

   ```bash
   claude plugin install research-memory@adrian-marketplace
   ```

3. **インストールを確認**：

   ```bash
   # プラグインは任意のClaude Codeセッションで使用可能です
   ```

### 手動インストール（代替案）

手動インストールを希望する場合やマーケットプレイスで問題が発生した場合：

### インストールの確認

ファイルがプロジェクトに正しくコピーされたか確認：

```bash
ls -la your-research-project/
```

以下のキーファイルが表示されるはずです：
- `handlers.py`
- `config/config.json`
- `.claude/CLAUDE.md`
- `SKILL.md`

### クイックスタート

インストール後、Claude Codeで自然言語を使用するだけです：

```
"ねえ Research Memory、プロジェクトの状況を把握して"
"この作業セッションをResearch Memoryに記録して"
"空間ラグモデルに関する決定を検索して"
```

Research Memoryは初回使用時に必要なファイルとディレクトリを自動的に作成します。

### アンインストール

**マーケットプレイス経由でインストールした場合**：

```bash
claude plugin uninstall research-memory
```

**手動でインストールした場合**：

```bash
# プロジェクトからスキルファイルを削除
rm -f handlers.py config/config.json .claude/CLAUDE.md SKILL.md
rm -rf config/ .claude/ memory/
```

---

## 設定：`config/config.json`

すべての動作は1つのJSON設定ファイルによって制御され、デフォルト設定は以下のようになります（抜粋）：

```jsonc
{
  "memory_directory": "memory",
  "encoding": "utf-8",
  "csv_delimiter": ",",
  "timestamp_format": "ISO8601",

  "bootstrap": {
    "recent_entries_count": 5,
    "include_todos": true,
    "suggest_work_plan": true
  },

  "logging": {
    "auto_timestamp": true,
    "phase_sections": [
      "DGP",
      "data_preprocess",
      "data_analyse",
      "modeling",
      "robustness",
      "writing",
      "infra",
      "notes"
    ],
    "experiment_schema": [
      "hypothesis",
      "dataset",
      "model",
      "metrics",
      "notes"
    ]
  },

  "search": {
    "max_results": 10,
    "include_context": true,
    "context_lines": 3
  }
}
```

主要フィールド説明：

* `memory_directory`：記憶ファイルディレクトリ（プロジェクトルート相対）；

* `encoding`：ファイルエンコーディング（デフォルト`utf-8`、`gbk`などにも変更可能）；

* `timestamp_format`：

  * `"ISO8601"` → 例：`2025-12-03T19:30:00+09:00`
  * `"YYYY-MM-DD_HH-MM-SS"` → ファイル名 / 人間の読み取りに適している
  * `"timestamp"` → Unixタイムスタンプ（秒）；

* `bootstrap.recent_entries_count`：起動時に表示する最近のdevlogエントリ数；

* `logging.phase_sections`：サポートする研究フェーズタグ；

* `logging.experiment_schema`：`experiments.csv`の必須フィールド；

* `search.*`：クエリ時の返却結果数とコンテキストの有無。

必要に応じて`config.json`を変更でき、すべての設定項目は`MemoryBackend`で有効です。

---

## Claude Codeでの使用

### 典型的な使用シナリオ

**1. 1日の開始：コンテキスト復元**

> 「research-memoryを使って前回どこまで進めたかを復元し、今日の計画を立ててください。」

スキルの動作：

* `research_memory_bootstrap`を呼び出す：

  * `project-overview.md`を読み込む（既に書かれている場合）；
  * 最近のN件のdevlogエントリを抽出（タイムスタンプ + フェーズ情報付き）；
  * 現在の未完了TODOを要約；
  * 「今日の作業提案計画」を生成。

---

**2. フェーズ完了：このセッションを記録**

> 「この期間の作業をDGP / data_analyse / modelingでセグメント化し、research-memoryに記録するよう整理してください。」

Claudeは以下を行います：

1. 現在の対話内容と今行ったことに基づき、ペイロードを構築、例：

   ```jsonc
   {
     "session_goal": "MCIB_v1.3で空間DiDを実行し、H2を検証",
     "changes_summary": [
       "01_clean_mcib.Rを更新し、treat_window_180変数を追加",
       "サンプル数 < 100の自治体をフィルタリング"
     ],
     "phases": {
       "DGP": "処置効果が0-180日以内に徐々に出現すると仮定し、距離閾値50kmで重み行列を構築。",
       "data_analyse": "処置群/対照群のベースライン期間認知平均比較をプロット、明白な事前傾向交差は観察されず。",
       "modeling": "2つの特定を推定：TWFE + municipalityでクラスタリング；州別時間傾向の拡張特定。",
       "robustness": "シンプルなプラセボ：処置時間を全体で1年ずらすと、結果が有意にならない。"
     },
     "experiments": [
       {
         "hypothesis": "H2",
         "dataset": "MCIB_v1.3",
         "model": "50km binary contiguity Wを用いた空間DiD",
         "metrics": {
           "ATT": 0.153,
           "p_value": 0.021
         },
         "notes": "結果は窓設定に敏感で、さらなる堅牢性検証が必要。"
       }
     ],
     "decisions": [
       {
         "title": "暫定的にモデルBを主要特定として採用",
         "rationale": "州別時間傾向追加後、事前傾向がより滑らかになり、係数がより安定。",
         "alternatives": [
           "シンプルなTWFEを主要特定として継続使用",
           "event-study形式を試す"
         ]
       }
     ],
     "todos": [
       "k-nearest neighborsベースの空間重み行列比較を追加",
       "プラセボ/代替特定結果を体系的に整理しpaper.qmdに記述"
     ],
     "completed_todos": [
       "方法セクションに空間重み行列構築説明を追加"
     ]
   }
   ```

2. `research_memory_log_session(payload)`を呼び出し、自動的に：

   * `devlog.md`にタイムスタンプ付きセッション記録を追加；
   * `experiments.csv`に完全な実験情報行を挿入；
   * `decisions.md`に決定ブロックを記述；
   * `todos.md`に新しいTODOを追加し、`completed_todos`の項目を完了としてマーク。

その後、「今何をしたか」を自然に記述するだけで、スキルが長期的に検索可能な構造化記憶に変換してくれます。

---

**3. 履歴レビュー：過去の決定と実験を見る**

> 「なぜ以前に空間ラグモデルを放棄したのか？」
> 「H2で行ったすべての実験を確認。」
> 「hksarg_parser.Rに関する変更記録を見る。」

このときClaudeは以下を呼び出します：

```python
query_history(query, filters=None)
```

スキルは以下を行います：

* `devlog.md` / `decisions.md` / `experiments.csv`でキーワードマッチング；
* 設定に従い最大`search.max_results`件のマッチを返却；
* 必要なコンテキスト（前後数行）を添付；
* 簡単な要約を生成し、以下を伝える：

  * その時の決定は何であったか；
  * どの実験が行われたか；
  * どの代替表現/特定が放棄されたか。

---

## コマンドライン使用（オプション）

Claude Code経由で呼び出すことに加え、コマンドラインから直接`handlers.py`を操作することも可能—Claudeが一時的に利用できない場合や、スクリプトで一括処理したい場合に適しています。

### 1. ブートストラップ

```bash
python handlers.py bootstrap
```

以下を含むJSONを出力：

* `project_context`
* `recent_progress`
* `current_todos`
* `work_plan_suggestions`
* `timestamp`

### 2. セッション記録

```bash
python handlers.py log-session \
  --payload-json '{
    "session_goal": "CLIログテスト",
    "changes_summary": ["README例を更新"],
    "phases": {"notes": "初めてコマンドラインでresearch-memoryを使用"},
    "todos": ["このツールをpaper.qmdで引用"]
  }'
```

### 3. 履歴クエリ

```bash
# 最もシンプル：キーワードで検索
python handlers.py query --question "空間ラグモデル"

# フィルタ付き：時間 + フェーズ + タイプ
python handlers.py query \
  --question "H2" \
  --from-date 2025-01-01 \
  --to-date 2025-12-31 \
  --phase modeling \
  --type experiments \
  --limit 5
```

CLIはJSONを出力し、他のスクリプトで継続使用するのに便利です。

---

## ファイル形式例

### `memory/devlog.md`

```markdown
# Development Log

## 2025-12-03 10:15

**Session Goal**: MCIB_v1.3で空間DiDを実行し、H2を検証

**Changes Summary**:
- 01_clean_mcib.Rを更新し、treat_window_180変数を追加
- サンプル数 < 100の自治体を除外

### DGP
処置効果が0-180日以内に徐々に出現すると仮定し、50km閾値でバイナリ空間重み行列を構築し行標準化。

### data_analyse
処置群/対照群のベースライン期間認知平均比較をプロット、明白な事前傾向交差は観察されず。

### modeling
2つの特定を推定：モデルA（TWFE）、モデルB（TWFE + 州別時間傾向）、H2係数は両方で方向が一致。

### robustness
シンプルなプラセボ検定を実施（処置時間を全体で1年ずらす）、効果は有意でない。

### notes
さらなるevent-studyと異なる空間重み行列を試す必要あり。

---

```

### `memory/experiments.csv`（ヘッダー例）

```csv
timestamp,experiment_id,hypothesis,dataset,model,metrics,notes,research_phase
2025-12-03T10:15:00+09:00,exp_20251203_101500,H2,MCIB_v1.3,"空間DiD, W=50km",{"ATT":0.153,"p_value":0.021},"プラセボ結果不安定","DGP,data_analyse,modeling,robustness"
```

### `memory/todos.md`

```markdown
# Project TODOs

- [ ] k-nearest neighborsベースの空間重み行列比較を追加
- [x] 方法セクションに空間重み行列構築説明を追加（完了：2025-12-03 - log_session経由）
```

### `memory/decisions.md`

```markdown
# Key Decisions

## 2025-12-03 10:20 — 暫定的にモデルBを主要特定として採用

**Decision**
州別時間傾向付きTWFEを主要特定として使用。

**Rationale**
事前傾向がより滑らかになり、異なるサブサンプルで推定結果がより安定。

**Alternatives**
- シンプルなTWFEを主要特定として維持
- event-study + group-specific trendsに切り替え
```

---

## 設計原則

* **ローカルファースト**：すべてがローカルテキストファイル、Git管理可能、手動編集可能；
* **スキルファースト**：Claude Codeはスキルツール経由で呼び出し、特定のファイルパスを気にする必要なし；
* **拡張可能**：`MemoryBackend`抽象化層を通じて、将来的にはデータベース / MCP / リモートサービスにシームレスに切り替え可能；
* **研究ワークフローと意味的に整合**：

  * DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes
  * 「今日は少しコードを変更した」といった数行の書き方ではなく。

---

## ロードマップ

現在のバージョンは**v0.x（ファイルバックエンド版）**、将来の考慮事項：

* SQLite / DuckDBをバックエンドとしてサポート（より強力なクエリ能力、集約分析をサポート）；
* ベクトル検索を追加し、長いdevlogに対してファジーマッチングを提供；
* MCP / HTTPサービスモード、複数のプロジェクト / エージェントで共有可能；
* マルチユーザー協業シナリオでのロックとマージ戦略。

---

## ライセンスと著者

* **ライセンス**：MIT
* **著者**：Yufei Sun (Adrian) `<syfyufei@gmail.com>`
* **リポジトリ**：[https://github.com/syfyufei/research-memory](https://github.com/syfyufei/research-memory)

---

もしあなたが複数の大規模プロジェクトを同時に進行し、
毎回「昨日の自分が何を考えていたか」を思い出すのに半日も費やすことを嫌うなら、
研究リポジトリに `research-memory` をインストールしてみてください—
Claude Codeを**プロジェクト全体の履歴を真に記憶している**パートナーにし、
現在の対話しか記憶していないチャットインターフェースではなくしてください。

```
::contentReference[oaicite:0]{index=0}
```