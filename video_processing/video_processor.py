import os
from moviepy.editor import VideoFileClip

def extract_audio(video_file):
    # Extract audio from the video
    ffmpeg_path = '/Users/kanishkarya/opt/anaconda3/lib/python3.9/site-packages/ffmpeg/__init__.py'
    audio_filename = os.path.splitext(video_file)[0] + '.mp3'
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_filename)

    return audio_filename
