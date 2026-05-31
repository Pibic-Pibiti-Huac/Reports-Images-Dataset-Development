import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path: str, page_idx=0) -> str:
    try:
        reader = PdfReader(file_path)
        page = reader.pages[page_idx]
        text = page.extract_text()
        return text
    except Exception as e:
        print(f"Error: {e}")


def filter_text(text: str, pattern: str) -> str:
    try:
        result = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if result:
            return result.group(1).strip()
    except Exception as e:
        print(f"Error: {e}")
