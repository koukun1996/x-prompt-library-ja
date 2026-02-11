# x-prompt-library-ja

日本語のプロンプトライブラリ。AI ツールとの対話を効率化するためのプロンプトテンプレートやユーティリティを提供します。

## ツール

### x-fetcher

xAI API (Grok) を使って X (Twitter) からリアルタイムデータを取得・分析するコマンドラインツール。

Grok の `x_search` 機能を活用し、自然言語のクエリで X の投稿を検索・分析できます。

#### 主な機能

- **自由形式クエリ** - 自然言語で X の情報を検索
- **プロンプトテンプレート** - 目的別に最適化された 8 種類のテンプレートを用意
- **Claude Code 連携** - Claude Code セッションから直接呼び出して利用可能

#### テンプレート一覧

| テンプレート | 説明 |
|-------------|------|
| `user_monitor` | 特定ユーザーの直近投稿を監視・要約 |
| `topic_research` | トピックに関する議論を調査 |
| `trend_analysis` | トレンドを分析 |
| `thread_summary` | スレッドを要約 |
| `comparative` | 2 アカウントの発言を比較分析 |
| `sentiment` | トピックに対する感情分析 |
| `breaking_news` | 速報ニュースの反応を調査 |
| `freeform` | 自由形式のクエリ |

#### クイックスタート

```bash
# セットアップ
pip install -r tools/x-fetcher/requirements.txt
# XAI_API_KEY を環境変数に設定（https://console.x.ai/ で取得）

# 自由形式で検索
python tools/x-fetcher/fetch.py "AIに関する最新の議論を教えて"

# テンプレートを使用
python tools/x-fetcher/fetch.py -t user_monitor --handle @openai --hours 12
python tools/x-fetcher/fetch.py -t trend_analysis
python tools/x-fetcher/fetch.py -t sentiment --keyword "iPhone"
```

詳細は [tools/x-fetcher/README.md](tools/x-fetcher/README.md) を参照してください。

## リポジトリ構成

```
x-prompt-library-ja/
├── README.md
├── CLAUDE.md
├── .gitignore
└── tools/
    └── x-fetcher/
        ├── README.md
        ├── fetch.py
        ├── prompts.py
        ├── requirements.txt
        └── .env.example
```

## 必要環境

- Python 3.10+
- xAI API キー（[console.x.ai](https://console.x.ai/) で取得）

## ライセンス

このプロジェクトは初期段階にあります。ライセンスは今後決定予定です。