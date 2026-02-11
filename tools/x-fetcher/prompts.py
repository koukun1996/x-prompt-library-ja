"""
プロンプトテンプレート集

目的別のプロンプトテンプレートを定義する。
テンプレートは自然言語ベースで、パラメータを埋め込むことで動的にプロンプトを生成する。
"""

TEMPLATES: dict[str, dict] = {
    "user_recent": {
        "description": "特定ユーザーの直近の投稿を要約する",
        "params": ["handle", "hours"],
        "template": (
            "X (Twitter) ユーザー {handle} の直近 {hours} 時間の投稿を取得し、"
            "以下の形式で要約してください:\n"
            "1. 投稿の概要（主要なトピック・テーマ）\n"
            "2. 注目すべき投稿（エンゲージメントが高そうなもの）\n"
            "3. 全体的なトーン・スタンス"
        ),
    },
    "topic_search": {
        "description": "特定トピックに関する X の議論を調査する",
        "params": ["keyword"],
        "template": (
            "X (Twitter) で「{keyword}」に関する最新の議論を調査してください。\n"
            "以下を含めてください:\n"
            "1. 主要な意見・立場の整理\n"
            "2. 影響力のあるユーザーの発言\n"
            "3. 議論の傾向（賛否の割合、感情的トーン）\n"
            "4. 関連するハッシュタグやキーワード"
        ),
    },
    "trend_analysis": {
        "description": "特定トピックのトレンドを分析する",
        "params": ["topic"],
        "template": (
            "X (Twitter) で「{topic}」に関するトレンドを分析してください。\n"
            "以下を含めてください:\n"
            "1. 現在の話題の中心（何が議論されているか）\n"
            "2. 主要な意見の対立軸\n"
            "3. インフルエンサーや専門家の見解\n"
            "4. 今後の展開予測"
        ),
    },
    "thread_summary": {
        "description": "特定のスレッドやディスカッションを要約する",
        "params": ["url"],
        "template": (
            "以下の X (Twitter) スレッドまたはディスカッションを要約してください:\n"
            "{url}\n\n"
            "以下を含めてください:\n"
            "1. スレッドの主旨\n"
            "2. 主要なポイント（箇条書き）\n"
            "3. 注目すべき返信やリアクション\n"
            "4. 結論または要点のまとめ"
        ),
    },
    "comparative": {
        "description": "2つのアカウントの発言を比較分析する",
        "params": ["handle1", "handle2"],
        "template": (
            "X (Twitter) ユーザー {handle1} と {handle2} の直近の発言を比較分析してください。\n"
            "以下を含めてください:\n"
            "1. それぞれの主要な発言内容\n"
            "2. 共通点と相違点\n"
            "3. トーンやスタンスの違い\n"
            "4. 相互のやり取り（あれば）"
        ),
    },
    "sentiment": {
        "description": "特定トピックに対する感情分析を行う",
        "params": ["keyword"],
        "template": (
            "X (Twitter) で「{keyword}」に対する感情（センチメント）を分析してください。\n"
            "以下を含めてください:\n"
            "1. ポジティブ・ネガティブ・ニュートラルの割合（推定）\n"
            "2. ポジティブな意見の代表例\n"
            "3. ネガティブな意見の代表例\n"
            "4. 全体的な世論の傾向"
        ),
    },
    "breaking_news": {
        "description": "速報・ニュースに関する X の反応を調査する",
        "params": ["keyword"],
        "template": (
            "「{keyword}」に関する X (Twitter) での最新の反応を調査してください。\n"
            "以下を含めてください:\n"
            "1. 事実関係の整理（確認済み情報と未確認情報）\n"
            "2. 主要メディアや公式アカウントの発信\n"
            "3. 一般ユーザーの反応\n"
            "4. 誤情報や憶測の有無"
        ),
    },
    "freeform": {
        "description": "自由形式のクエリをそのまま送信する",
        "params": ["query"],
        "template": "{query}",
    },
}


def build_prompt(template_name: str, **kwargs) -> str:
    """
    テンプレート名とパラメータからプロンプト文字列を生成する。

    Args:
        template_name: テンプレート名（TEMPLATES のキー）
        **kwargs: テンプレートに埋め込むパラメータ

    Returns:
        生成されたプロンプト文字列

    Raises:
        KeyError: 指定されたテンプレートが存在しない場合
        KeyError: 必要なパラメータが不足している場合
    """
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise KeyError(
            f"テンプレート '{template_name}' が見つかりません。"
            f"利用可能: {available}"
        )

    template_info = TEMPLATES[template_name]
    template = template_info["template"]
    required_params = template_info["params"]

    # 必要なパラメータの確認
    missing = [p for p in required_params if p not in kwargs]
    if missing:
        raise KeyError(
            f"テンプレート '{template_name}' に必要なパラメータが不足しています: "
            f"{', '.join(missing)}"
        )

    return template.format(**kwargs)
