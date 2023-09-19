import speech_recognition as sr
from pydub import AudioSegment

def perform_stt(audio_file):
    try:
        # Convert the MP3 audio to WAV format using pydub
        audio = AudioSegment.from_mp3(audio_file)
        wav_audio_file = audio_file.replace('.mp3', '.wav')
        audio.export(wav_audio_file, format='wav')

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the audio file
        with sr.AudioFile(wav_audio_file) as source:
            audio_data = recognizer.record(source)

        # Perform speech-to-text (STT) conversion
        text = recognizer.recognize_google(audio_data)

        # Return the recognized text
        return text

    except Exception as e:
        print("Error during speech-to-text conversion:", str(e))
        return None


if __name__ == "__main__":
    audio_file = "audio/your_audio_file.mp3"  # Replace with the path to your audio file

    result = perform_stt(audio_file)
    
    if result:
        print("Text from speech:", result)
    else:
        print("Speech-to-text conversion failed.")