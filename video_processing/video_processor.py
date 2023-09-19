from moviepy.editor import VideoFileClip
#from moviepy.editor import AudioFileClip

def extract_audio(video_file, output_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_file)
        
        # Extract audio from the video
        audio_clip = video_clip.audio

        # Write the audio to the specified output path
        audio_clip.write_audiofile(output_path)

        # Close the video and audio clips to release resources
        video_clip.close()
        audio_clip.close()

        return True  # Extraction succeeded
    except Exception as e:
        # Handle any errors that occurred during extraction
        print("Error during audio extraction:", str(e))
        return False  # Extraction failed

if __name__ == "__main__":
    # Example usage:
    input_video_file = "uploads/*.mp4"
    output_audio_file = "path_to_output_audio.mp3"

    if extract_audio(input_video_file, output_audio_file):
        print("Audio extraction successful.")
    else:
        print("Audio extraction failed.")
