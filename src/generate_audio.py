import os
import json
import edge_tts
import nest_asyncio
from output_dir_manager import OutputDirManager
import asyncio

# Enable nested asyncio loops
nest_asyncio.apply()


async def main():
    output_dir_manager = OutputDirManager()
    active_dirs = output_dir_manager.get_active_dirs()

    for dir_name in active_dirs:
        # ディレクトリ内にすでに音声が生成されている場合はスキップ
        dir = os.path.join(
            output_dir_manager.OUTPUT_DIR, output_dir_manager.ACTIVE_DIR, dir_name
        )
        audio_file = os.path.join(dir, "question.mp3")
        if os.path.exists(audio_file):
            print(f"Audio already exists in {dir}. Skipping...")
            continue

        json_file = os.path.join(dir, "question.json")
        await generate_audio_from_question(json_file, dir)


async def generate_audio_from_question(question_file_path, folder_path):
    """
    指定された問題文から音声を生成して保存する

    Args:
        question_file_path (str): 問題文のJSONファイルのパス
        folder_path (str): 音声ファイルを保存するフォルダのパス
    """
    with open(question_file_path, "r") as f:
        question = json.load(f)

    text = (
        "A\n"
        + question["options"]["A"]
        + "\n"
        + "B\n"
        + question["options"]["B"]
        + "\n"
        + "C\n"
        + question["options"]["C"]
        + "\n"
        + "D\n"
        + question["options"]["D"]
        + "\n"
        + "The answer is..."
        + question["answer"]
        + "\n"
        + question["options"][question["answer"]]
    )

    # 読み上げ速度を遅くするために rate を設定
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural", rate="-10%")
    file_path = os.path.join(folder_path, "question.mp3")
    try:
        await communicate.save(file_path)
        print(f"Audio file saved as {file_path}")
    except Exception as e:
        print(f"Error generating audio: {e}")


async def generate_audio(output_folder):

    # Enable nested asyncio loops
    nest_asyncio.apply()

    for i in range(1, 7):
        folder_name = os.path.join(output_folder, str(i))
        json_file_path = os.path.join(folder_name, "question.json")
        with open(json_file_path, "r") as f:
            data = json.load(f)

        question = (
            f"Question {i}\nLook at the picture marked number {i} in your test book."
        )

        text = (
            question
            + " "
            + "A\n"
            + data["options"]["A"]
            + "\n"
            + "B\n"
            + data["options"]["B"]
            + "\n"
            + "C\n"
            + data["options"]["C"]
            + "\n"
            + "D\n"
            + data["options"]["D"]
            + "\n"
            + "The answer is..."
            + data["answer"]
            + "\n"
            + data["options"][data["answer"]]
        )
        # 読み上げ速度を遅くするために rate を設定
        communicate = edge_tts.Communicate(text, "en-US-JennyNeural", rate="-10%")
        file_path = os.path.join(folder_name, "question.mp3")
        try:
            await communicate.save(file_path)
            print(f"Audio file saved as {file_path}")
        except Exception as e:
            print(f"Error generating audio for question {i+1}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
