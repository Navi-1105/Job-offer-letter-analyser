from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import re

# Function to extract text based on file type
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_pdf_text(file_path)
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return "Unsupported file type"

# Function to extract salary information
def extract_salary(text):
    # Common salary formats: $60,000, 60000 USD, $30/hr
    salary_pattern = r'\$\s?\d{2,3}(?:,\d{3})?(?:\s?(?:USD|usd))?|\d{2,3}(?:,\d{3})?\s?(?:USD|usd)?(?:\s?\/hr)?'
    matches = re.findall(salary_pattern, text)
    return matches

# Function to extract benefits like health insurance, PTO, etc.
def extract_benefits(text):
    benefits_keywords = [
        "health insurance", "401(k)", "paid time off", "flexible hours",
        "remote work", "dental", "vision", "gym membership", "parental leave"
    ]
    found = [b for b in benefits_keywords if b.lower() in text.lower()]
    return found

# Function to extract perks like stock options, free snacks, etc.
def extract_perks(text):
    perk_keywords = [
        "free snacks", "stock options", "company retreats", "training budget",
        "pet-friendly", "performance bonus", "equipment allowance"
    ]
    found = [p for p in perk_keywords if p.lower() in text.lower()]
    return found

# Main function to extract job details (salary, benefits, perks)
def extract_job_details(file_path):
    text = extract_text(file_path)
    return {
        "salary": extract_salary(text),
        "benefits": extract_benefits(text),
        "perks": extract_perks(text)
    }
