import PyPDF2
import io

def extract_text_from_pdf(file_content):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def extract_text_from_txt(file_content):
    """Extracts text from a TXT file."""
    try:
        return file_content.decode('utf-8')
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return None

def clean_text(text):
    """Basic text cleaning."""
    if not text:
        return ""
    # Remove extra whitespace
    text = " ".join(text.split())
    return text
