"""
Root runner script to generate the Sugar Cosmetics Instagram Performance Analytics PDF Report
"""

from src.pdf_generator import build_pdf_report

if __name__ == "__main__":
    print("Initiating PDF generation process...")
    path = build_pdf_report()
    print(f"Report successfully compiled at: {path}")
