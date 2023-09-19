from flask import Flask, request, render_template
import os
import logging
import webbrowser
from video_processing.video_processor import extract_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'

log_format = '%(asctime)s [%(levelname)s] - %(message)s'
logging.basicConfig(filename='log.txt', level=logging.INFO, format=log_format)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'No file part'
            app.logger.error(message)
            return render_template('upload.html', message=message)

        file = request.files['file']

        if file.filename == '':
            message = 'No selected file'
            app.logger.error(message)
            return render_template('upload.html', message=message)

        allowed_extensions = {'mp4', 'avi', 'mkv'}
        if not allowed_file(file.filename, allowed_extensions):
            message = 'Invalid file format'
            app.logger.error(message)
            return render_template('upload.html', message=message)

        target_language = request.form['target_language']

        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Use the extract_audio function from video_processor
        audio_filename = extract_audio(filename)

        log_message = f'File uploaded successfully! Target language: {target_language}'
        app.logger.info(log_message)

        return 'File uploaded successfully! Target language: {}'.format(target_language)

    return render_template('upload.html')

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
