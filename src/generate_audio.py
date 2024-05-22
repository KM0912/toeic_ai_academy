import os
import json
import edge_tts
import nest_asyncio

async def generate_audio(output_folder):

    # Enable nested asyncio loops
    nest_asyncio.apply()

    for i in range(1, 7):
        folder_name = os.path.join(output_folder, str(i))
        json_file_path = os.path.join(folder_name, "question.json")
        with open(json_file_path, "r") as f:
            data = json.load(f)

        question = f"Question {i}\nLook at the picture marked number {i} in your test book."

        text = (question + " "
        + "A\n" + data["options"]["A"] + "\n" 
        + "B\n" + data["options"]["B"] + "\n" 
        + "C\n" + data["options"]["C"] + "\n" 
        + "D\n" + data["options"]["D"] + "\n" 
        + "The answer is..." + data["answer"] + "\n" + data["options"][data["answer"]]) 
        # 読み上げ速度を遅くするために rate を設定
        communicate = edge_tts.Communicate(text, 'en-US-JennyNeural', rate='-10%')
        file_path = os.path.join(folder_name, "question.mp3")
        try:
            await communicate.save(file_path)
            print(f"Audio file saved as {file_path}")
        except Exception as e:
            print(f"Error generating audio for question {i+1}: {e}")