from flask import Flask, render_template, request
import os
from extractor.extractor import extract_job_details, extract_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', job_details=None, full_text=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', job_details=None, full_text=None, error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', job_details=None, full_text=None, error='No selected file')

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    extracted_text = extract_text(file_path)
    job_details = extract_job_details(file_path)

    return render_template('index.html', job_details=job_details, full_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
