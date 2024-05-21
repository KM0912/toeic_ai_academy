import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 生成する動画のサイズ
target_size = (1920, 1080)


def generate_clip(image, audio):
    """
    画像と音声を結合して動画クリップを生成する。
    """
    # 画像クリップを作成
    img_clip = ImageClip(image).set_duration(AudioFileClip(audio).duration)

    # 画像クリップを目標サイズにパディング
    img_clip = img_clip.margin(
        top=(target_size[1] - img_clip.h) // 2,
        bottom=(target_size[1] - img_clip.h) // 2,
        left=(target_size[0] - img_clip.w) // 2,
        right=(target_size[0] - img_clip.w) // 2,
        color=(0, 0, 0),
    )

    # 音声クリップを作成
    audio_clip = AudioFileClip(audio)

    # 画像クリップに音声を追加
    img_clip = img_clip.set_audio(audio_clip)

    return img_clip


def generate_movie(images, audios):
    """
    画像と音声ファイルのパスリストをもとに動画を生成する。
    """
    # タイトル画像を作成
    title_image = os.path.join(script_dir, "../title.png")
    title_clip = ImageClip(title_image).set_duration(3)
    title_clip = title_clip.resize(newsize=target_size)

    video_clips = [title_clip]

    for image, audio in zip(images, audios):
        img_clip = generate_clip(image, audio)
        video_clips.append(img_clip)

    # すべてのクリップを結合
    final_clip = concatenate_videoclips(video_clips)

    # 動画の解像度を設定（1920x1080）
    final_clip = final_clip.resize(newsize=target_size)

    # 出力ファイル名
    output_file = os.path.join(script_dir, "..", "output", "final_video.mp4")

    # 動画を書き出し
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24)

    print(f"動画が正常に作成されました: {output_file}")
