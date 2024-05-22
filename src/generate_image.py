import openai


def generate_image(prompt):
    """
    指定されたプロンプトに基づいて画像を生成する。
    """
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url


def create_dalle_prompt(data):
    """
    指定されたJSONデータをもとにDALL-Eの画像生成プロンプトを作成する。
    """
    description = data["description"]
    question = data["question"]
    options = data["options"]
    answer = data["answer"]

    # 選択肢をフォーマットしてインデントを調整
    options_text = "\n".join([f"    {v}) {options[v]}" for k, v in enumerate(options)])

    prompt = f"""
    あなたはTOEIC Part 1のリスニング問題のための画像を作成しています。以下の説明に基づいて、質の高い画像を生成してください。

    説明: {description}

    画像の内容は、次の選択肢のいずれかに関連するものにしてください。ただし、1つの選択肢が正解であることが明確にわかるようにしてください。

    選択肢:
    {options_text}

    正解: {answer}

    画像は以下の要件を満たすようにしてください：
    - 描写が詳細で、シーンが明確に伝わること
    - 正解の選択肢が一目でわかるようにすること
    - 他の選択肢も考慮し、それらが関連する要素を含むこと
    - 自然な日常のシーンをリアルに表現すること

    例:
    説明: 男性が公園のベンチに座って本を読んでいる。彼の前には鳥が餌をついばみ、後ろの道には数人が歩いている。
    選択肢:
    A) 彼は寝ている
    B) 彼は本を読んでいる
    C) 彼は鳥に餌をやっている
    D) 彼は道を歩いている
    正解: B
    """

    return prompt.strip()
