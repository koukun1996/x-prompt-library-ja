"""
x-fetcher: xAI API (Grok) を使って X (Twitter) からデータを取得するツール

Claude Code から直接呼び出して使用する。
自然言語のクエリを受け取り、Grok の x_search / web_search を活用して
X のリアルタイムデータを取得・分析する。

使用例:
  python fetch.py "query" [@handle1 @handle2] [--hours 24] [--web] [--raw]
  python fetch.py "@elonmusk の最新投稿を要約して"
  python fetch.py "AI規制に関する議論を分析して" --hours 48
  python fetch.py --template user_recent --handle @openai --hours 12
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompts import build_prompt, TEMPLATES

# .env ファイルを読み込み（プロジェクトルートまたは同階層）
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent.parent / ".env")


def create_client() -> OpenAI:
    """xAI API クライアントを生成する。"""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print(
            "エラー: XAI_API_KEY が設定されていません。\n"
            ".env ファイルに XAI_API_KEY=xai-xxxxx を設定してください。",
            file=sys.stderr,
        )
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")


def fetch(
    query: str,
    *,
    handles: list[str] | None = None,
    hours: int | None = None,
    enable_web_search: bool = False,
    model: str = "grok-4-1-fast",
    raw: bool = False,
) -> str:
    """
    xAI Responses API を呼び出して X データを取得する。

    Args:
        query: 自然言語のクエリ（またはテンプレートで生成したプロンプト）
        handles: フィルタ対象の X ハンドル（最大10件）
        hours: 検索対象の時間範囲（時間単位）
        enable_web_search: Web 検索も有効にするか
        model: 使用する Grok モデル
        raw: True の場合、API レスポンス全体を JSON で返す

    Returns:
        Grok の応答テキスト（raw=True の場合は JSON 文字列）
    """
    client = create_client()

    # ツール設定
    tools = []

    # x_search ツールの構築
    x_search_tool = {"type": "x_search"}
    if handles:
        # @プレフィクスを除去してハンドル名のみにする
        clean_handles = [h.lstrip("@") for h in handles[:10]]
        x_search_tool["allowed_x_handles"] = clean_handles

    if hours:
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        from_date = now - timedelta(hours=hours)
        x_search_tool["from_date"] = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        x_search_tool["to_date"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    tools.append(x_search_tool)

    if enable_web_search:
        tools.append({"type": "web_search"})

    # API 呼び出し
    response = client.responses.create(
        model=model,
        tools=tools,
        input=query,
    )

    if raw:
        return response.model_dump_json(indent=2)

    # テキスト部分を抽出
    output_texts = []
    for item in response.output:
        if hasattr(item, "text"):
            output_texts.append(item.text)
        elif hasattr(item, "content"):
            for content_block in item.content:
                if hasattr(content_block, "text"):
                    output_texts.append(content_block.text)

    return "\n".join(output_texts) if output_texts else "(応答なし)"


def main():
    parser = argparse.ArgumentParser(
        description="xAI API (Grok) を使って X からデータを取得する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python fetch.py "AIに関する最新の議論を教えて"
  python fetch.py "@openai の最近の投稿を要約して" --hours 24
  python fetch.py "半導体業界のトレンドを分析して" --web
  python fetch.py --template user_recent --handle @elonmusk --hours 12
  python fetch.py --template topic_search --keyword "生成AI 規制"
  python fetch.py --list-templates
        """,
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="自然言語のクエリ（テンプレート使用時は不要）",
    )
    parser.add_argument(
        "--template", "-t",
        choices=list(TEMPLATES.keys()),
        help="使用するプロンプトテンプレート名",
    )
    parser.add_argument(
        "--handle",
        action="append",
        default=[],
        help="フィルタ対象の X ハンドル（複数指定可、最大10件）",
    )
    parser.add_argument(
        "--hours",
        type=int,
        help="検索対象の時間範囲（時間単位）",
    )
    parser.add_argument(
        "--keyword",
        help="テンプレートの {keyword} に挿入する値",
    )
    parser.add_argument(
        "--topic",
        help="テンプレートの {topic} に挿入する値",
    )
    parser.add_argument(
        "--url",
        help="テンプレートの {url} に挿入する値",
    )
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Web 検索も有効にする",
    )
    parser.add_argument(
        "--model", "-m",
        default="grok-4-1-fast",
        help="使用する Grok モデル（デフォルト: grok-4-1-fast）",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="API レスポンス全体を JSON で出力する",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="利用可能なテンプレート一覧を表示する",
    )

    args = parser.parse_args()

    # テンプレート一覧表示
    if args.list_templates:
        print("利用可能なテンプレート:")
        print("-" * 60)
        for name, info in TEMPLATES.items():
            print(f"  {name}")
            print(f"    説明: {info['description']}")
            print(f"    パラメータ: {', '.join(info['params'])}")
            print()
        return

    # クエリの構築
    if args.template:
        template_params = {}
        if args.handle:
            template_params["handle"] = args.handle[0]
            if len(args.handle) > 1:
                template_params["handle1"] = args.handle[0]
                template_params["handle2"] = args.handle[1]
        if args.hours:
            template_params["hours"] = str(args.hours)
        if args.keyword:
            template_params["keyword"] = args.keyword
        if args.topic:
            template_params["topic"] = args.topic
        if args.url:
            template_params["url"] = args.url

        query = build_prompt(args.template, **template_params)
    elif args.query:
        query = args.query
    else:
        parser.error("クエリまたは --template を指定してください")
        return

    # 実行
    result = fetch(
        query,
        handles=args.handle if args.handle else None,
        hours=args.hours,
        enable_web_search=args.web,
        model=args.model,
        raw=args.raw,
    )

    print(result)


if __name__ == "__main__":
    main()
