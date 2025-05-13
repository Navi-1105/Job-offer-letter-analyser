import unittest
from extractor.extractor import extract_job_details

class TestExtractor(unittest.TestCase):

    def test_salary_extraction(self):
        text = "You will receive a monthly stipend of INR 20,000."
        result = extract_job_details(text)
        self.assertTrue(any("20000" in s.replace(",", "") for s in result['salary']))

    def test_perk_detection(self):
        text = "We also offer company retreats and free snacks in the pantry."
        result = extract_job_details(text)
        self.assertIn("free snacks", result['perks'])

    def test_benefit_detection(self):
        text = "The job includes health insurance and paid leave."
        result = extract_job_details(text)
        self.assertTrue(
            any("paid leave" in b.lower() for b in result['benefits']) or 
            any("paid time off" in b.lower() for b in result['benefits'])
        )

if __name__ == '__main__':
    unittest.main()
