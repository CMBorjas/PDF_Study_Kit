import re

def extract_keywords(text):
    """
    Extracts bold terms from markdown-formatted text.
    Assumes keywords are wrapped in **
    """
    keywords = set()
    # Find all text between ** **
    matches = re.findall(r"\*\*(.*?)\*\*", text)
    for match in matches:
        clean_match = match.strip()
        # Filter out very long bold phrases or single characters
        if 2 < len(clean_match) < 40:
            keywords.add(clean_match)
            
    return list(keywords)
