import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString


def extract_text_epub(epub_path):
    """
    Extracts text from an EPUB file, converting HTML structure to the same
    markdown format that extract.py produces for PDFs.

    Headings become ## lines, bold/strong text gets **wrapped**,
    list items become - bullets, and chapters are separated by --- markers.
    """
    book = epub.read_epub(epub_path, options={"ignore_ncx": True})
    text_content = []
    chapter_num = 0

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        body_html = item.get_body_content()
        if not body_html:
            continue

        soup = BeautifulSoup(body_html, "html.parser")

        # Skip items that have no real text (e.g. cover images, blank pages)
        visible_text = soup.get_text(strip=True)
        if not visible_text:
            continue

        chapter_num += 1
        text_content.append(f"\n--- Chapter {chapter_num} ---\n")

        for element in soup.descendants:
            if isinstance(element, NavigableString):
                continue

            tag = element.name

            # --- Headings ---
            if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                heading_text = element.get_text(strip=True)
                if heading_text:
                    text_content.append(f"## {heading_text}")
                continue

            # --- Paragraphs ---
            if tag == "p":
                line = _process_inline(element)
                if line.strip():
                    text_content.append(line)
                continue

            # --- List items ---
            if tag == "li":
                li_text = _process_inline(element)
                if li_text.strip():
                    text_content.append(f"- {li_text.strip()}")
                continue

            # --- Block quotes / asides (often used for callouts) ---
            if tag in ("blockquote", "aside"):
                bq_text = element.get_text(strip=True)
                if bq_text:
                    text_content.append(f"> {bq_text}")
                continue

        text_content.append("\n")

    return "\n".join(text_content)


def _process_inline(element):
    """
    Walk the children of a block-level element and apply inline formatting.
    Wraps <strong>, <b>, <em>, <i> text with markdown equivalents.
    """
    parts = []

    for child in element.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif child.name in ("strong", "b"):
            inner = child.get_text()
            if inner.strip():
                parts.append(f"**{inner}**")
        elif child.name in ("em", "i"):
            inner = child.get_text()
            if inner.strip():
                parts.append(f"*{inner}*")
        elif child.name == "a":
            # Preserve link text, skip the URL
            parts.append(child.get_text())
        elif child.name == "br":
            parts.append("\n")
        elif child.name in ("span", "sup", "sub", "u", "small", "mark"):
            # Recurse into generic inline wrappers
            parts.append(_process_inline(child))
        else:
            # Fallback: just grab the text
            parts.append(child.get_text())

    return "".join(parts)
