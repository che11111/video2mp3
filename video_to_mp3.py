from moviepy.editor import AudioFileClip
import os

def convert_video_to_mp3(video_path, output_dir=None):
    """
    将视频文件转换为MP3音频
    :param video_path: 视频文件路径
    :param output_dir: 输出目录（可选）
    :return: 转换后的MP3文件路径
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")

        # 设置输出路径
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir or os.path.dirname(video_path), f"{base_name}.mp3")

        # 转换视频为MP3
        audio_clip = AudioFileClip(video_path)
        audio_clip.write_audiofile(output_path, verbose=False, logger=None)
        audio_clip.close()

        return output_path

    except Exception as e:
        raise Exception(f"转换失败: {str(e)}")
