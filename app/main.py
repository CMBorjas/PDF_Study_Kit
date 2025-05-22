import os
import shutil
import tkinter as tk
from tkinter import filedialog

from extract import extract_text # Assuming extract.py is in the same directory
from organize import parse_raw_text # Assuming organize.py is in the same directory


def choose_file_gui():
    try:
        root = tk.Tk()  
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        return file_path if file_path else None
    except Exception as e:
        print(f"GUI failed: {e}") # Fallback to CLI
        return None

def choose_file_cli():
    """
    CLI file selection for PDF files.
    """
    print("Available PDFs in /input:")
    for f in os.listdir("/input"):
        if f.lower().endswith(".pdf"):
            print(f" - {f}")
    filename = input("Enter the name of the PDF file to process (from /input): ").strip()
    return f"/input/{filename}"

def main():
    file_path = choose_file_gui()
    
    if not file_path:
        file_path = choose_file_cli()

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    # use a host path for the file
    if not file_path.startswith("/input/"):
        filename = os.path.basename(file_path)
        dest_path = f"/input/{filename}"
        shutil.copy(file_path, dest_path)
        file_path = dest_path

    print(f" Processing: {os.path.basename(file_path)}")
    output = extract_text(file_path)

    with open("/output/raw_text.txt", "w", encoding="utf-8") as f:
        f.write(output)

    print("Text extraction complete. Output saved to /output/raw_text.txt")

    
    chapters = parse_raw_text()
    print(f"\nParsed {len(chapters)} chapters.")
    for chapter in chapters:
        print(f"\n{chapter['title']}")
        print(f"{len(chapter['content'])} lines of content")
        print(f"{len(chapter['remember'])} 'Remember this' tips")

if __name__ == "__main__":
    main()
