from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import re
from thefuzz import fuzz

# ------------------------
# Text extraction by file type
# ------------------------
def extract_text(file_path):
    print(f"File path received: {file_path}")
    if file_path.endswith('.pdf'):
        text = extract_pdf_text(file_path)
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        print("Unsupported file type")
        return ""

    # Save extracted text for debugging
    with open("debug_extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Extracted Text from File:")
    print(text[:500])  # Show preview
    return text

# ------------------------
# Salary Extraction
# ------------------------
def extract_salary(text):
    salary_pattern = r'(?i)(?:INR|Rs\.?|₹|\$|USD)\s?[0-9]{1,3}(?:,[0-9]{3})*(?:\s?(?:per month|monthly|per annum|annually|/hr|hour|stipend))?'
    matches = re.findall(salary_pattern, text)

    fuzzy_salary_clues = ["paid internship", "paid position", "monthly stipend", "salary provided"]
    for clue in fuzzy_salary_clues:
        if fuzz.partial_ratio(clue.lower(), text.lower()) >= 70:
            matches.append(clue)

    return list(set(match.strip() for match in matches if len(match.strip()) > 4))

# ------------------------
# Fuzzy Benefit Detection
# ------------------------
def extract_benefits(text):
    benefit_keywords = [
        "health insurance", "401(k)", "paid time off", "paid leave", "flexible hours",
        "remote work", "dental", "vision", "gym membership", "parental leave",
        "medical coverage", "gratuity", "provident fund", "employee assistance",
        "life insurance", "disability insurance", "tuition reimbursement", "stock options",
        "annual bonus", "profit sharing", "employee stock purchase plan", "wellness programs",
        "childcare assistance", "commuter benefits", "paid holidays", "sabbatical leave",
        "mental health days", "travel allowance", "work from home", "flexible spending account",
        "health savings account", "employee discounts", "legal assistance",
        "identity theft protection", "pet insurance", "relocation assistance",
        "team building activities", "professional development", "career coaching",
        "mentorship programs", "tuition assistance", "student loan repayment",
        "financial planning services", "retirement planning", "stock grants",
        "employee recognition programs", "work-life balance", "community service days",
        "volunteer time off", "wellness stipend", "childcare support",
        "transportation allowance", "full-time", "office-based", "standard working hours"
    ]
    lowered_text = text.lower()
    return sorted(set(k for k in benefit_keywords if fuzz.partial_ratio(k, lowered_text) > 70))

# ------------------------
# Fuzzy Perk Detection
# ------------------------
def extract_perks(text):
    perk_keywords = [
        "free snacks", "stock options", "company retreats", "training budget", "pet-friendly",
        "performance bonus", "equipment allowance", "signing bonus", "learning budget",
        "internet reimbursement", "wellness programs", "free meals", "team outings",
        "work from home", "flexible schedule", "casual dress code", "office games",
        "coffee machine", "nap pods", "transportation allowance", "birthday off",
        "team lunches", "snack bar", "relocation assistance", "tuition reimbursement",
        "mentorship program", "employee discounts", "work-life balance", "career development",
        "community service days", "volunteer time off", "wellness stipend",
        "childcare assistance", "office hours", "team collaboration", "professional guidance"
    ]
    lowered_text = text.lower()
    return sorted(set(k for k in perk_keywords if fuzz.partial_ratio(k, lowered_text) > 70))

# ------------------------
# Combine all details
# ------------------------
def extract_job_details_from_text(text):
    return {
        "salary": extract_salary(text),
        "benefits": extract_benefits(text),
        "perks": extract_perks(text)
    }

def extract_job_details(file_path):
    text = extract_text(file_path)
    if not text:
        print("No text extracted from file:", file_path)
        return {"salary": [], "benefits": [], "perks": []}
    return extract_job_details_from_text(text)

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    file_path = "Realistic_Job_Offer_Letter.pdf"  # Put your file name here
    job_details = extract_job_details(file_path)

    print("\nExtracted Job Details:")
    print("Salary:", job_details['salary'])
    print("Benefits:", job_details['benefits'])
    print("Perks:", job_details['perks'])
   