# TOEIC Part 1の問題を生成するためのプロンプト
GENERATE_TOEIC_QUESTION_PROMPT =  """
    Create a high-quality TOEIC Part 1 question in JSON format. The question should be based on a realistic and detailed scene description, with a clear corresponding question. Provide four distinct and plausible options, and indicate the correct answer. Ensure that the correct answer is the only possible interpretation based on the scene description. The JSON should have the following structure:

    {
        "description": "A detailed and realistic description of the scene, including relevant objects, actions, and context.",
        "question": "A clear and specific question related to the scene.",
        "options": {
            "A" : "A plausible option related to the scene",
            "B" : "Another plausible option related to the scene",
            "C" : "Yet another plausible option related to the scene",
            "D" : "The correct answer, which should be clearly supported by the scene description"
        },
        "answer": "The correct answer from the options provided"
    }
    
    Example of a high-quality TOEIC Part 1 question:

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
    }

    Please generate a similar question following this structure and quality.
    """
