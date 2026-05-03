import re
from utils.toc_parser import extract_toc
from utils.keywords import extract_keywords

def parse_raw_text(file_path="output/raw_text.txt"):
    """
    Parses the formatted markdown text extracted from the PDF.
    Returns chapters and the Table of Contents.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Find TOC
    toc = extract_toc(text)
    
    chapters = []
    current_chapter = {"title": "Introduction", "content": [], "remember": [], "keywords": []}
    
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("--- Page"):
            continue
            
        # Detect headings (## Chapter ...)
        # Allowing either explicit "Chapter X" or any large heading that seems like a major section
        if re.match(r"^#{1,3}\s+Chapter\s+\d+", line, re.IGNORECASE):
            # Only save the previous chapter if it has content or a meaningful title
            if current_chapter["title"] != "Introduction" or current_chapter["content"]:
                chapters.append(current_chapter)
            current_chapter = {"title": line.lstrip("# ").strip(), "content": [], "remember": [], "keywords": []}
            
        elif "Remember this" in line or "Note:" in line:
            current_chapter["remember"].append(line)
            
        else:
            current_chapter["content"].append(line)
                
    if current_chapter["title"] and current_chapter["content"]:
        chapters.append(current_chapter)
        
    # Extract keywords for each chapter
    for chapter in chapters:
        chapter_text = "\n".join(chapter["content"])
        chapter["keywords"] = extract_keywords(chapter_text)

    return chapters, toc