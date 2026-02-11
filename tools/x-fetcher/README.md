# x-fetcher

xAI API (Grok) を使って X (Twitter) からリアルタイムデータを取得するツール。

Grok の `x_search` 機能を活用し、自然言語のクエリで X の投稿を検索・分析する。

## セットアップ

### 1. xAI API キーの取得

1. https://console.x.ai/ にアクセス
2. アカウントを作成（X アカウントまたは Google アカウントでサインイン）
3. ダッシュボードで API キーを生成（`xai-` プレフィクスのキー）
4. 新規アカウントには $25 の無料クレジットが付与される

### 2. 環境設定

Windows のシステム環境変数に `XAI_API_KEY` を設定する（推奨）:

1. スタートメニュー → 「環境変数」で検索 → 「システム環境変数の編集」
2. 「環境変数」→ ユーザー環境変数の「新規」
3. 変数名: `XAI_API_KEY` / 変数値: 取得したキー
4. ターミナルを再起動して反映

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方

### 自由形式のクエリ

```bash
python fetch.py "AIに関する最新の議論を教えて"
python fetch.py "@openai の最近の投稿を要約して" --hours 24
python fetch.py "半導体業界のトレンドを分析して" --web
```

### テンプレートを使用

```bash
# テンプレート一覧を表示
python fetch.py --list-templates

# ユーザー監視: 特定ユーザーの直近投稿を調査
python fetch.py -t user_monitor --handle @openai --hours 12

# トピック調査: 特定キーワードに関する議論を調査
python fetch.py -t topic_research --keyword "生成AI 規制"
python fetch.py -t topic_research --keyword "半導体" --hours 48

# トレンド分析: 今話題のトピックを把握
python fetch.py -t trend_analysis
python fetch.py -t trend_analysis --topic "量子コンピュータ"

# スレッド要約: 特定スレッドの内容を要約
python fetch.py -t thread_summary --url "https://x.com/user/status/123"

# 2アカウント比較: 2つのアカウントの発言を比較
python fetch.py -t comparative --handle @user1 --handle @user2
python fetch.py -t comparative --handle @user1 --handle @user2 --hours 24

# 感情分析: トピックに対する賛否を分析
python fetch.py -t sentiment --keyword "iPhone"
python fetch.py -t sentiment --keyword "iPhone" --hours 24

# 速報ニュース: ニュースに関するXの反応を調査
python fetch.py -t breaking_news --keyword "地震"
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--handle` | フィルタ対象の X ハンドル（複数指定可、最大10件） |
| `--hours` | 検索対象の時間範囲（時間単位） |
| `--keyword` | テンプレートのキーワード |
| `--topic` | テンプレートのトピック |
| `--url` | テンプレートの URL |
| `--web` / `-w` | Web 検索も有効にする |
| `--model` / `-m` | Grok モデルを指定（デフォルト: `grok-4-1-fast`） |
| `--raw` | API レスポンス全体を JSON で出力 |
| `--template` / `-t` | プロンプトテンプレートを使用 |
| `--list-templates` | 利用可能なテンプレート一覧を表示 |

### Claude Code からの利用

Claude Code セッション内で直接実行できる:

```
あなた: 「@OpenAI の最近の発表を調べて」
Claude: fetch.py を実行して結果を取得・整理
```

## テンプレート一覧

| 名前 | 説明 | 必須パラメータ | 任意パラメータ |
|------|------|---------------|---------------|
| `user_monitor` | 特定ユーザーの直近投稿を監視・要約 | `--handle`, `--hours` | — |
| `topic_research` | トピックに関する議論を調査 | `--keyword` | `--hours` |
| `trend_analysis` | トレンドを分析（トピック未指定で全般） | — | `--topic` |
| `thread_summary` | スレッドを要約 | `--url` | — |
| `comparative` | 2アカウントの発言を比較分析 | `--handle` x2 | `--hours` |
| `sentiment` | トピックに対する感情分析 | `--keyword` | `--hours` |
| `breaking_news` | 速報ニュースの反応を調査 | `--keyword` | — |
| `freeform` | 自由形式のクエリ | (クエリ直接指定) | — |

## コスト

- モデル: `grok-4-1-fast` -- 入力 $0.20/1M tokens, 出力 $0.50/1M tokens
- `x_search` / `web_search` ツール: 現在無料
- 新規アカウント: $25 の無料クレジット付き

## 制約事項

- 読み取り専用（投稿・いいね等の書き込みは不可）
- 結果は自然言語で返却（生のツイート JSON ではない）
- ハンドル指定は 1 リクエストあたり最大 10 件
- データはニアリアルタイム（数秒〜数分の遅延あり）
