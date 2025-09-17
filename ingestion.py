import re
import os
import pdfplumber  # better PDF text extraction

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber for better word handling.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"  # keep paragraphs separate
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def clean_text(text):
    """
    Cleans and prepares the text:
    - Removes excessive newlines and spaces
    - Fixes split words like 'resour ce' -> 'resource'
    - Converts text to lowercase
    - Preserves headings in all caps
    """
    if not text:
        return ""

    # Replace letter splits inside words (like 'resour ce' -> 'resource')
    text = re.sub(r'(?<=\w) (?=\w)', '', text)

    # Replace multiple spaces/newlines/tabs with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    # Convert to lowercase
    text = text.lower()


    headings = re.findall(r'([A-Z][A-Z\s]{3,})', text)
    for heading in headings:
        text = text.replace(heading.lower(), heading)

    return text

if __name__ == "__main__":
    # PDF path
    pdf_file_path = "documents/HR-Policy .pdf"  

    # Output path
    cleaned_file_path = "data/HR_policy_cleaned.txt"

    # Ensure data folder exists
    os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

    # 1. Extract text
    raw_text = extract_text_from_pdf(pdf_file_path)

    if raw_text:
        # 2. Clean text
        cleaned_text = clean_text(raw_text)

        # 3. Save full cleaned text
        with open(cleaned_file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print("Document ingestion complete.")
        print(f"Raw text length: {len(raw_text)} characters.")
        print(f"Cleaned text length: {len(cleaned_text)} characters.")
    else:
        print("Failed to ingest document.")
