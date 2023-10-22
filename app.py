from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import logging
import webbrowser

from video_processing.video_processor import extract_audio
from speech_2_txt.stt import perform_stt
from grammar.grammar_check import gc
from translation.translate import translate_text
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
from gtts import gTTS  # Import Google Text-to-Speech (gTTS)

app = Flask(__name__)

# Configure the upload and audio directories
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'
app.config['OUTPUT_FOLDER'] = 'static/output'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

# Logging configuration
log_format = '%(asctime)s [%(levelname)s] - %(message)s'
logging.basicConfig(filename='log.txt', level=logging.INFO, format=log_format)

# Define a mapping of language names to language codes
language_mapping = {
    'Hindi': 'hi',
    'Tamil': 'ta',
    'Telugu': 'te',
    # Add more languages as needed
}

# Ensure upload, audio, and output directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

# Define the original_video_path as a global variable
original_video_path = None 
target_language = None

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    global original_video_path  # Declare original_video_path as a global variable

    if 'file' not in request.files:
        message = 'No file part'
        app.logger.error(message)
        return render_template('upload.html', message=message)

    file = request.files['file']

    if file.filename == '':
        message = 'No selected file'
        app.logger.error(message)
        return render_template('upload.html', message=message)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)

        audio_filename = f"{app.config['AUDIO_FOLDER']}/{filename}.mp3"
        
        if extract_audio(filename, audio_filename):
            log_message = f'Audio extraction successful for file: {filename}'
            app.logger.info(log_message)

            # Save the path of the original video file
            original_video_path = os.path.abspath(filename)

            # After performing STT conversion
            recognized_text = perform_stt(audio_filename)
            corrected_text = gc(recognized_text)

            # Redirect to the audio review page
            return render_template('audio_review.html', text=corrected_text, original_video_path=original_video_path)
        else:
            log_message = f'Audio extraction failed for file: {filename}'
            app.logger.error(log_message)
            return 'Audio extraction failed.'

    return 'Invalid file format.'

@app.route('/review_audio', methods=['GET', 'POST'])
def review_audio():
    global target_language
    if request.method == 'POST':
        # Handle the form submission
        corrected_text = request.form['text']

        # Get the selected target language name from the form
        selected_language_name = request.form['target_language']
        
        # Get the corresponding language code from the mapping
        target_language = language_mapping.get(selected_language_name)

        if target_language:
            # Perform translation based on the selected target language code
            translated_text = translate_text(corrected_text, target_language)

            # Redirect to the translation review page
            return render_template('translation_review.html', text=translated_text, target_language=target_language)
        else:
            return 'Invalid target language selected.'
    else:
        # Render the review page
        return render_template('audio_review.html')

@app.route('/review_translation', methods=['GET', 'POST'])
def review_translation():
    # Handle the form submission
    final_text = request.form['text']

    video_filename = f'static/output/{os.path.basename(original_video_path)}_{target_language}.mp4'
    audio_filename = f'static/output/{os.path.basename(original_video_path)}_{target_language}.mp3'

    # Create a video clip from the original video file
    video_clip = VideoFileClip(original_video_path)

    # Create an audio clip from the translated text
    tts = gTTS(final_text, lang=target_language)
    tts.save(audio_filename)
    audio_clip = AudioFileClip(audio_filename)

    # Combine the video and audio clips
    final_clip = video_clip.set_audio(audio_clip)

    # Write the final video to a file
    final_clip.write_videofile(video_filename)

    # Get the output file path
    output_file_path = f'/{video_filename}'

    # Render the template with the appropriate variables
    return render_template('display_video.html', video_filename=output_file_path, target_language=target_language)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
'''
Ok, so firstly you fill in the last name or surname. Then go on to the next line fill in the given name or your first name. Next fill in the date of birth. You will find a drop-down menu. Click on that, and you will get the year of birth. Scroll down and get the year of birth first then fill in the documentation number and finally the country of citizenship, that again will be a drop-down menu.
'''