# TOEIC Part 1の問題を生成するためのプロンプト
GENERATE_TOEIC_QUESTION_PROMPT = """
    あなたはTOEIC Part 1のリスニング問題を作成しています。以下の形式で10個のJSONオブジェクトとして写真の説明、選択肢、正解を生成し、それらをquestionsというキーのバリューに配列として格納してください。写真の説明は日常の活動やシーンに関連するもので、各シチュエーションはできるだけ異なるものにしてください。以下は形式の例です。

    例:
    {
        "questions": [
            {
                "description": "A man is sitting on a bench in a park. He is holding a book and reading it intently. Birds are feeding on the ground nearby, and a few people are walking on the path behind him. The man is wearing glasses and a hat, and there is a backpack next to him on the bench.",
                "options": {
                    "A" : "He is dozing off while holding a book.",
                    "B" : "He is intently reading a book.",
                    "C" : "He is feeding birds with bread crumbs.",
                    "D" : "He is engaging in a conversation with a passerby."
                },
                "answer": "B"
            },
            {
                "description": "A woman is standing at a bus stop. She is looking at her phone and holding a shopping bag in one hand. A bus is approaching the stop, and a few other people are waiting. The woman is wearing a coat and a scarf, and there is a street sign next to the bus stop indicating the bus route.",
                "options": {
                    "A" : "She is perusing a book while standing.",
                    "B" : "She is engaged in a phone conversation.",
                    "C" : "She is glancing at her mobile device.",
                    "D" : "She is preparing to board the approaching bus."
                },
                "answer": "C"
            }
        ]
    }

    生成するオブジェクトもこの形式に従ってください。10問作成してください。説明は具体的で詳細にし、各シチュエーションが異なるようにしてください。
    また、問題の選択肢はTOEIC800点レベルに相当する難易度にしてください。
    レスポンスはコードブロックを含まないクリーンなJSON形式の文字列として返してください。
    """
