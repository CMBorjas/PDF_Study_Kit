import re

def extract_toc(text):
    """
    Attempts to identify and extract the Table of Contents.
    Looks for lines with page numbers typical of a TOC.
    """
    toc_entries = []
    lines = text.splitlines()
    in_toc = False
    
    for line in lines:
        if "Table of Contents" in line or "Contents" in line:
            in_toc = True
            continue
            
        if in_toc:
            # Match typical TOC line: Title ..... 12 or Title 12
            # E.g. "Chapter 1: Introduction ..... 4"
            match = re.search(r"^(.*?)(?:\.{2,}|\s+)(\d+)$", line.strip())
            if match:
                title = match.group(1).strip()
                page = match.group(2).strip()
                # avoid short meaningless lines
                if len(title) > 3:
                    toc_entries.append({"title": title, "page": page})
            elif "--- Page" in line and len(toc_entries) > 0:
                # Assume TOC is complete if we hit a new page and already found entries
                # However, TOC can span multiple pages. We'll loosely keep collecting
                pass
            elif len(line.strip()) > 0 and len(toc_entries) > 5 and not match:
                # If we've found several entries and hit regular text, assume TOC is over
                if not line.startswith("---"):
                    break
                
    return toc_entries
