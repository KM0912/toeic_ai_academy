import os
import sys
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    concatenate_audioclips,
)
from output_dir_manager import OutputDirManager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from settings import TARGET_SIZE


# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))


def main():
    generate_movie()


def generate_clip(image, question_audio, options_audio) -> ImageClip:
    """
    画像と音声を結合して動画クリップを生成する。

    Args:
        image (str): 画像ファイルのパス
        question_audio (str): 問題文の音声ファイルのパス
        options_audio (str): 選択肢の音声ファイルのパス
    """

    # 音声ファイルを作成
    audio_clip = generate_audio_clip(question_audio, options_audio)

    # 画像クリップを作成 (音声の長さに合わせる)
    img_clip: ImageClip = ImageClip(image).set_duration(audio_clip.duration)

    # 画像クリップに音声を追加
    img_clip = img_clip.set_audio(audio_clip)

    # 画像クリップを目標サイズにパディング
    img_clip = adjust_image_clip_margin(img_clip, TARGET_SIZE)

    return img_clip


def generate_movie():
    """
    画像と音声ファイルのパスリストをもとに動画を生成する。
    """

    output_dir_manager = OutputDirManager()

    # outputフォルダ内に６問以上の問題文があることを確認
    active_dirs = output_dir_manager.get_active_dirs()
    # タイトル画像を作成
    title_image = "./title.png"
    title_clip = ImageClip(title_image).set_duration(3)
    title_clip = title_clip.resize(newsize=TARGET_SIZE)

    video_clips = [title_clip]

    for i, active_dir in enumerate(active_dirs):
        folder_path = os.path.join(
            output_dir_manager.OUTPUT_DIR, output_dir_manager.ACTIVE_DIR, active_dir
        )
        image_path = os.path.join(folder_path, "image.png")
        question_audio_path = f"./assets/audios/question_audios/question{i+1}.mp3"
        options_audio_path = os.path.join(folder_path, "question.mp3")
        img_clip = generate_clip(image_path, question_audio_path, options_audio_path)
        video_clips.append(img_clip)

        # 6問作成したら動画生成
        if i == 5:
            break

    # すべてのクリップを結合
    final_clip = concatenate_videoclips(video_clips)

    # 動画の解像度を設定（1920x1080）
    final_clip = final_clip.resize(newsize=TARGET_SIZE)

    # 動画を書き出し
    # 出力ファイル名
    output_file = os.path.join("output", "final_video.mp4")
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24)

    print(f"動画が正常に作成されました: {output_file}")


def adjust_image_clip_margin(
    img_clip: ImageClip, target_size: tuple[int, int]
) -> ImageClip:
    """
    画像クリップのマージンを調整する。

    Args:
        img_clip (ImageClip): 画像クリップ
        target_size (tuple[int, int]): 目標サイズ

    Returns:
        ImageClip: マージンが調整された画像クリップ
    """
    # 画像のサイズを取得
    image_height = img_clip.h
    image_width = img_clip.w

    # 画像クリップを目標サイズにパディング
    img_clip = img_clip.margin(
        top=(target_size[1] - image_height) // 2,
        bottom=(target_size[1] - image_height) // 2,
        left=(target_size[0] - image_width) // 2,
        right=(target_size[0] - image_width) // 2,
        color=(0, 0, 0),
    )

    return img_clip


def generate_audio_clip(question_audio, options_audio) -> AudioFileClip:
    """
    音声クリップを作成する。

    Args:
        question_audio (str): 問題文の音声ファイルのパス
        options_audio (str): 選択肢の音声ファイルのパス

    Returns:
        AudioFileClip: 音声クリップ
    """
    question_clip = AudioFileClip(question_audio)
    options_clip = AudioFileClip(options_audio)

    audio_clip: AudioFileClip = concatenate_audioclips([question_clip, options_clip])

    return audio_clip


if __name__ == "__main__":
    main()
