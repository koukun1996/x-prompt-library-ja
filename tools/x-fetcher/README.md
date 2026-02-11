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

```bash
cd tools/x-fetcher
cp .env.example .env
# .env を編集して XAI_API_KEY を設定
```

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

# 特定ユーザーの投稿を要約
python fetch.py -t user_recent --handle @openai --hours 12

# トピックの議論を調査
python fetch.py -t topic_search --keyword "生成AI 規制"

# トレンド分析
python fetch.py -t trend_analysis --topic "量子コンピュータ"

# 2アカウントの比較
python fetch.py -t comparative --handle @user1 --handle @user2

# 感情分析
python fetch.py -t sentiment --keyword "iPhone"

# 速報ニュースの反応
python fetch.py -t breaking_news --keyword "地震"
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--handle` | フィルタ対象の X ハンドル（複数指定可、最大10件） |
| `--hours` | 検索対象の時間範囲（時間単位） |
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

| 名前 | 説明 | パラメータ |
|------|------|-----------|
| `user_recent` | 特定ユーザーの直近投稿を要約 | `--handle`, `--hours` |
| `topic_search` | トピックに関する議論を調査 | `--keyword` |
| `trend_analysis` | トレンドを分析 | `--topic` |
| `thread_summary` | スレッドを要約 | `--url` |
| `comparative` | 2アカウントを比較分析 | `--handle` x2 |
| `sentiment` | 感情分析 | `--keyword` |
| `breaking_news` | 速報ニュースの反応を調査 | `--keyword` |
| `freeform` | 自由形式のクエリ | `--keyword`(=query) |

## コスト

- モデル: `grok-4-1-fast` -- 入力 $0.20/1M tokens, 出力 $0.50/1M tokens
- `x_search` / `web_search` ツール: 現在無料
- 新規アカウント: $25 の無料クレジット付き

## 制約事項

- 読み取り専用（投稿・いいね等の書き込みは不可）
- 結果は自然言語で返却（生のツイート JSON ではない）
- ハンドル指定は 1 リクエストあたり最大 10 件
- データはニアリアルタイム（数秒〜数分の遅延あり）
