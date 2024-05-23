import os
import openai
import json
from download_image import download_image
from output_dir_manager import OutputDirManager


def main():
    """
    画像を生成する。
    """
    output_dir_manager = OutputDirManager()
    active_dirs = output_dir_manager.get_active_dirs()

    for dir_name in active_dirs:
        # ディレクトリ内にすでに画像が生成されている場合はスキップ
        dir = os.path.join(
            output_dir_manager.OUTPUT_DIR, output_dir_manager.ACTIVE_DIR, dir_name
        )
        image_file = os.path.join(dir, "image.png")
        if os.path.exists(image_file):
            print(f"Image already exists in {dir}. Skipping...")
            continue

        question_file = os.path.join(dir, "question.json")
        with open(question_file, "r") as f:
            # プロンプトの生成
            data = json.load(f)
            dalle_prompt = create_dalle_prompt(data)

            # 画像の生成
            image_url = generate_image(dalle_prompt)

        # 画像の保存
        download_image(image_url, image_file)

    print("Generated images.")


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


if __name__ == "__main__":
    main()
