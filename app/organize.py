"""
Parse data from output/raw_text.txt and organize it into a structured format.

detects 
    Chater headers
    Section headers
    bullet points
    "Remember this" tips
    etc...

"""

import re 

def parse_raw_text(file_path="/output/raw_text.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chapters = []
    current_chapter = {"title": None, "content": [], "remember": []}

    lines = text.splitlines()
    for line in lines:
        line = line.strip()

        # Detect chapter titles
        if re.match(r"^Chapter \d+", line):
            if current_chapter["title"]:
                chapters.append(current_chapter)
                current_chapter = {"title": None, "content": [], "remember": []}
            current_chapter["title"] = line

        # Collect 'Remember this' tips
        elif "Remember this" in line:
            current_chapter["remember"].append(line)

        # Add regular content
        elif line:
            current_chapter["content"].append(line)

    # Save last chapter
    if current_chapter["title"]:
        chapters.append(current_chapter)

    return chapters