import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def clean_text(text):
    """
    Cleans and prepares the text for processing.
    """
    if not text:
        return ""
    # Remove excessive newlines and spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # You can add more specific cleaning rules here based on your PDF's content
    return text

if __name__ == "__main__":
    # Specify the path to your HR policy PDF file
    pdf_file_path = "documents/your_hr_policy.pdf"  # IMPORTANT: Change this to your actual filename

    # 1. Extract text
    raw_text = extract_text_from_pdf(pdf_file_path)

    if raw_text:
        # 2. Clean and prepare the text
        cleaned_text = clean_text(raw_text)

        print("Document ingestion complete.")
        print(f"Raw text length: {len(raw_text)} characters.")
        print(f"Cleaned text length: {len(cleaned_text)} characters.")
        print("\n--- First 500 characters of the cleaned text ---")
        print(cleaned_text[:500])
    else:
        print("Failed to ingest document.")