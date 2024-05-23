import os
import openai
import json
import prompts
from config import load_settings
from output_dir_manager import OutputDirManager

app_settings = load_settings("settings.toml").app


def main():
    questions = []
    for i in range(10):
        toeic_questions = generate_toeic_questions()
        try:
            toeic_questions = json.loads(toeic_questions)
            questions = questions + toeic_questions["questions"]
        except json.JSONDecodeError as e:
            print("Error: Failed to parse JSON")
            continue

    print("Generated TOEIC Part 1 questions.")

    # これまでに生成した問題数を取得
    output_dir_manager = OutputDirManager()
    question_count = output_dir_manager.max_output_dir_number()

    # 問題文を保存
    for i, question in enumerate(questions):
        folder_name = os.path.join(
            output_dir_manager.OUTPUT_DIR,
            output_dir_manager.ACTIVE_DIR,
            str(question_count + i + 1),
        )
        os.makedirs(folder_name, exist_ok=True)

        json_file_path = os.path.join(folder_name, "question.json")
        with open(json_file_path, "w") as f:
            json.dump(question, f, indent=4)


def generate_toeic_questions():
    """
    TOEIC Part 1の問題を生成する
    プロンプトはsrc/prompts.pyに定義されている
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompts.GENERATE_TOEIC_QUESTION_PROMPT},
        ],
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    main()
