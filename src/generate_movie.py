import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    concatenate_audioclips,
)
from output_dir_manager import OutputDirManager

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 生成する動画のサイズ
target_size = (1920, 1080)


def main():
    generate_movie()


def generate_clip(image, question_audio, options_audio):
    """
    画像と音声を結合して動画クリップを生成する。

    Args:
        image (str): 画像ファイルのパス
        question_audio (str): 問題文の音声ファイルのパス
        options_audio (str): 選択肢の音声ファイルのパス
    """

    # 音声ファイルの長さを取得
    question_clip_duration = AudioFileClip(question_audio).duration
    options_clip_duration = AudioFileClip(options_audio).duration

    # 画像クリップを作成
    img_clip = ImageClip(image).set_duration(
        question_clip_duration + options_clip_duration
    )

    # 画像クリップを目標サイズにパディング
    img_clip = img_clip.margin(
        top=(target_size[1] - img_clip.h) // 2,
        bottom=(target_size[1] - img_clip.h) // 2,
        left=(target_size[0] - img_clip.w) // 2,
        right=(target_size[0] - img_clip.w) // 2,
        color=(0, 0, 0),
    )

    # 音声クリップを作成
    question_clip = AudioFileClip(question_audio)
    options_clip = AudioFileClip(options_audio)
    audio_clip = concatenate_audioclips([question_clip, options_clip])

    # 画像クリップに音声を追加
    img_clip = img_clip.set_audio(audio_clip)

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
    title_clip = title_clip.resize(newsize=target_size)

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
    final_clip = final_clip.resize(newsize=target_size)

    # 動画を書き出し
    # 出力ファイル名
    output_file = os.path.join("output", "final_video.mp4")
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24)

    print(f"動画が正常に作成されました: {output_file}")


if __name__ == "__main__":
    main()
