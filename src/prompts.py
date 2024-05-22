# TOEIC Part 1の問題を生成するためのプロンプト
GENERATE_TOEIC_QUESTION_PROMPT = """
    あなたはTOEIC Part 1のリスニング問題を作成しています。以下の形式で2つのJSONオブジェクトとして写真の説明、質問、選択肢、正解を生成し、それらをquestionsというキーのバリューに配列として格納してください。写真の説明は日常の活動やシーンに関連するものにしてください。以下は形式の例です。descriptionと説明はOpenAIが考えてください。

    例:
    {
        "questions": [
            {
                "description": "A man is sitting on a bench in the park. He is holding a book in his hands and appears to be reading it. There are birds feeding in front of him and a few people are walking on the path behind him.",
                "question": "What is the man doing?",
                "options": {
                    "A" : "He is sleeping",
                    "B" : "He is reading a book",
                    "C" : "He is feeding the birds",
                    "D" : "He is walking on the path"
                },
                "answer": "B"
            },
            {
                "description": "A woman is standing at a bus stop. She is looking at her phone and holding a shopping bag. A bus is approaching the stop and a few other people are waiting.",
                "question": "What is the woman doing?",
                "options": {
                    "A" : "She is reading a book",
                    "B" : "She is talking on the phone",
                    "C" : "She is looking at her phone",
                    "D" : "She is boarding the bus"
                },
                "answer": "C"
            }
        ]
    }

    生成するオブジェクトもこの形式に従ってください。2問作成してください。

    説明は明確で簡潔にし、英語を学ぶ非ネイティブに適したものにしてください。
    """
