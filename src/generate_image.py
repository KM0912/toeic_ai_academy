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
    Create a TOEIC Part 1 image based on the following description.
    
    description: {description}

    However, please make sure that the contents of the choices other than the correct answer apply.
    Please generate an image that clearly narrows down to one answer.

    options:
    {options_text}

    answer: {answer}
    """
    
    return prompt.strip()