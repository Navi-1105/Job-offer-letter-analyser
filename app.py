from flask import Flask, render_template, request
import os
from extractor.extractor import extract_job_details_from_text, extract_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'offer_letters' not in request.files:
        return render_template('index.html', error="❌ No file uploaded.")

    files = request.files.getlist('offer_letters')
    if not files or all(file.filename == '' for file in files):
        return render_template('index.html', error="❌ No selected file.")

    invalid_files = [f.filename for f in files if not allowed_file(f.filename)]
    if invalid_files:
        return render_template('index.html', error=f"❌ Invalid file(s): {', '.join(invalid_files)}. Only PDF, DOCX, TXT allowed.")

    all_salary = []
    all_benefits = []
    all_perks = []
    all_text = ""

    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        text = extract_text(file_path)
        job_details = extract_job_details_from_text(text)

        all_salary += job_details.get("salary", [])
        all_benefits += job_details.get("benefits", [])
        all_perks += job_details.get("perks", [])
        all_text += f"\n--- {filename} ---\n{text}"

    return render_template(
        'result.html',
        salary=sorted(set(all_salary)),
        benefits=sorted(set(all_benefits)),
        perks=sorted(set(all_perks)),
        full_text=all_text
    )

if __name__ == '__main__':
    app.run(debug=True)
