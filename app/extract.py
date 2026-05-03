import fitz

def extract_text(pdf_path):
    """
    Extracts text from a PDF file, preserving headings and bold text as markdown.
    """
    text_content = []
    
    with fitz.open(pdf_path) as doc:
        # Pass 1: find average font size to heuristically identify headings
        font_sizes = {}
        for page in doc:
            blocks = page.get_text("dict").get("blocks", [])
            for block in blocks:
                if block.get("type") == 0:  # text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            size = round(span["size"], 1)
                            font_sizes[size] = font_sizes.get(size, 0) + len(span["text"].strip())
        
        # The most common font size is likely the body text
        if font_sizes:
            body_size = max(font_sizes.items(), key=lambda x: x[1])[0]
        else:
            body_size = 11.0 # fallback

        # Pass 2: Extract text and format it
        for page_num, page in enumerate(doc, start=1):
            text_content.append(f"\n--- Page {page_num} ---\n")
            blocks = page.get_text("dict").get("blocks", [])
            for block in blocks:
                if block.get("type") == 0: # text block
                    for line in block.get("lines", []):
                        line_text = ""
                        is_heading = False
                        
                        for span in line.get("spans", []):
                            text = span["text"]
                            if not text.strip():
                                line_text += text
                                continue
                            
                            size = round(span["size"], 1)
                            font_name = span.get("font", "").lower()
                            flags = span.get("flags", 0)
                            
                            is_bold = "bold" in font_name or "black" in font_name or "heavy" in font_name or (flags & 2**4)
                            
                            if size > body_size + 1:
                                is_heading = True
                                
                            if is_bold and not is_heading:
                                # Escape existing asterisks or handle carefully, but simple wrap is fine
                                line_text += f"**{text}**"
                            else:
                                line_text += text
                        
                        if is_heading and line_text.strip():
                            line_text = f"## {line_text.strip()}"
                        
                        stripped = line_text.strip()
                        if stripped.startswith("•") or stripped.startswith("- "):
                            line_text = f"- {stripped.lstrip('•- ')}"
                            
                        text_content.append(line_text)
                    text_content.append("\n")
    
    return "\n".join(text_content)
