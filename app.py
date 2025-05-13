from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from extractor.extractor import extract_text, extract_job_details

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("[INFO] Upload endpoint hit")

    if 'offer_letter' not in request.files:
        print("[ERROR] No file part in request")
        return "No file part in request"
    
    file = request.files['offer_letter']

    if file.filename == '':
        print("[ERROR] No file selected")
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"[INFO] File saved to: {filepath}")

        try:
            extracted_text = extract_text(filepath)
            job_info = extract_job_details(extracted_text)
            print("[INFO] Extraction completed")
            print("Extracted Info:", job_info)
        except Exception as e:
            print(f"[ERROR] Extraction failed: {e}")
            return f"Error during analysis: {str(e)}"

        return render_template('result.html', 
                               salary=job_info.get('salary', []), 
                               benefits=job_info.get('benefits', []), 
                               perks=job_info.get('perks', []),
                               full_text=extracted_text)

    print("[ERROR] Unsupported file format")
    return "Unsupported file format. Please upload a PDF, DOCX, or TXT."

if __name__ == '__main__':
    app.run(debug=True)
    