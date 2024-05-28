import os
import sys
import openai
import json
import prompts
from output_dir_manager import OutputDirManager
import re


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import settings


def main():
    generate_questions()


def generate_questions() -> None:
    """
    TOEICの問題文を生成し、outputディレクトリに保存する
    """
    questions_json = fetch_questions()
    question_list = parse_questions(questions_json)

    if question_list:
        save_questions(question_list)
        print("Generated questions.")
    else:
        print("No questions generated.")


def parse_questions(questions_json: str) -> list:
    """
    JSON形式の文字列から問題文のリストを解析する

    Args:
        questions_json (str): JSON形式の文字列

    Returns:
        list: 解析された問題文のリスト
    """
    try:
        questions = json.loads(questions_json)
        if "questions" in questions:
            question_list = questions["questions"]
    except json.JSONDecodeError as e:
        print("Error: Failed to parse JSON")
        print(e)

    return question_list


def save_questions(questions: list) -> None:
    """
    生成した問題文を保存する

    Args:
        questions (list): 生成した問題文のリスト
    """
    output_dir_manager = OutputDirManager()
    question_count = output_dir_manager.max_output_dir_number()

    for i, question in enumerate(questions):
        folder_name = f"{output_dir_manager.OUTPUT_DIR}/{output_dir_manager.ACTIVE_DIR}/{question_count + i + 1}"
        os.makedirs(folder_name, exist_ok=True)

        json_file_path = os.path.join(folder_name, output_dir_manager.QUESTION_FILE)
        with open(json_file_path, "w") as f:
            json.dump(question, f, indent=4)


def fetch_questions() -> str:
    """
    TOEICの問題文をOpenAI APIを使って生成する
    プロンプトはsrc/prompts.pyに定義されている

    Returns:
        str: 生成した問題文
    """
    try:
        response = openai.chat.completions.create(
            model=settings.MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompts.GENERATE_TOEIC_QUESTION_PROMPT},
            ],
            max_tokens=settings.MAX_TOKENS,
            n=settings.N,
            stop=settings.STOP,
            temperature=settings.TEMPERATURE,
        )
        response_content = response.choices[0].message.content

        cleaned_response = re.sub(
            r"```.*?```", "", response_content, flags=re.DOTALL
        ).strip()
        return cleaned_response

    except openai.error.OpenAIError as e:
        print("Error: Failed to fetch questions from OpenAI API")
        print(e)
        return ""


if __name__ == "__main__":
    main()
