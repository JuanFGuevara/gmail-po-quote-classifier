from pdfminer.high_level import extract_text

def extract_text_from_pdf(path):
    try:
        text = extract_text(path)
        return text
    except Exception as e:
        print(f"Error extrayendo PDF {path}: {e}")
        return ""
