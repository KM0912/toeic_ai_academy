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
    options = data["options"]
    answer = data["answer"]

    # 選択肢をフォーマットしてインデントを調整
    options_text = "\n".join([f"    {v}) {options[v]}" for k, v in enumerate(options)])

    prompt = f"""
    あなたはTOEIC Part 1のリスニング問題のための画像を作成しています。以下の説明に基づいて、日常のシーンをリアルに描写した画像を生成してください。

    説明: {description}

    画像の内容は次の選択肢のいずれかに関連するものにしてください。ただし、正解の選択肢が明確にわかるようにしてください。

    選択肢:
    {options_text}

    正解: {answer}

    画像の要件:
    - 画像は詳細で、説明されたシーンが明確に描写されていること。
    - 正解の選択肢が画像から一目でわかるようにすること。
    - 他の選択肢も考慮するが、正解の選択肢だけが明確に描かれていること。
    - 日常のシーンをリアルに自然に表現すること。
    - 画像にテキストや選択肢を含めないこと。
    - 画像は白黒にすること。

    例:
    説明:  A man is sitting on a bench in a park, reading a book. Birds are feeding on the ground in front of him, and a few people are walking on the path behind him.
    選択肢:
    A) He is sleeping
    B) He is reading a book
    C) He is feeding the birds
    D) He is walking on the path
    正解: B
    """

    return prompt.strip()


if __name__ == "__main__":
    main()
