import fitz

def extract_text(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    text_content = []

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc,start=1):
            text = page.get_text() # Use "text" to preserve layout
            text_content.append(f"\n--- Page {page_num} ---\n{text.strip()}")
    return "\n".join(text_content)


