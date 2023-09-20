from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import logging
import webbrowser
import sys
import language_tool_python
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

from video_processing.video_processor import extract_audio
from speech_2_txt.stt import perform_stt

nltk.download('punkt')  # Download the necessary data for NLTK tokenization

app = Flask(__name__)

# Configure the upload and audio directories
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

# Logging configuration
log_format = '%(asctime)s [%(levelname)s] - %(message)s'
logging.basicConfig(filename='log.txt', level=logging.INFO, format=log_format)

# Initialize the LanguageTool for grammar checking
grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Ensure upload and audio directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
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

            # After performing STT conversion
            recognized_text = perform_stt(audio_filename)

            # Tokenize sentences and words using NLTK
            sentences = sent_tokenize(recognized_text)
            tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

            # Perform grammar checking and text correction
            corrected_sentences = [grammar_tool.correct(" ".join(tokens)) for tokens in tokenized_sentences]
            corrected_text = " ".join(corrected_sentences)

            # Log the corrected text
            log_message = f'Grammar checking and text correction completed. Corrected text: {corrected_text}'
            app.logger.info(log_message)

            # Return the corrected text to the user
            return f'Grammar checking and text correction completed. Corrected text: {corrected_text}'
        else:
            log_message = f'Audio extraction failed for file: {filename}'
            app.logger.error(log_message)
            return 'Audio extraction failed.'

    return 'Invalid file format.'

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
