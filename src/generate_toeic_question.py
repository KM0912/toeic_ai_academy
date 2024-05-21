import openai
import prompts

def generate_toeic_question():
    """
    TOEIC Part 1の問題を生成する
    プロンプトはsrc/prompts.pyに定義されている
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompts.GENERATE_TOEIC_QUESTION_PROMPT}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content