import os
import shutil
import tkinter as tk
from tkinter import filedialog

from extract import extract_text
from organize import parse_raw_text
from mnemonics import generate_mnemonics_for_chapter
from formatter import export_docx, export_md, export_notecards

def get_paths():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    return input_dir, output_dir

def choose_file_gui(input_dir):
    try:
        root = tk.Tk()  
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            initialdir=input_dir,
            filetypes=[("PDF files", "*.pdf")]
        )
        return file_path if file_path else None
    except Exception as e:
        print(f"GUI failed: {e}") # Fallback to CLI
        return None

def choose_file_cli(input_dir):
    print(f"Available PDFs in {input_dir}:")
    for f in os.listdir(input_dir):
        if f.lower().endswith(".pdf"):
            print(f" - {f}")
    filename = input(f"Enter the name of the PDF file to process: ").strip()
    return os.path.join(input_dir, filename)

def main():
    input_dir, output_dir = get_paths()
    file_path = choose_file_gui(input_dir)
    
    if not file_path:
        file_path = choose_file_cli(input_dir)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # If the file isn't in our input directory, copy it there
    if not file_path.startswith(input_dir):
        filename = os.path.basename(file_path)
        dest_path = os.path.join(input_dir, filename)
        shutil.copy(file_path, dest_path)
        file_path = dest_path

    print(f"\nProcessing: {os.path.basename(file_path)}")
    
    # 1. Extract
    print("Extracting text...")
    raw_text = extract_text(file_path)
    
    raw_output_path = os.path.join(output_dir, "raw_text.txt")
    with open(raw_output_path, "w", encoding="utf-8") as f:
        f.write(raw_text)

    # 2. Organize
    print("Organizing structure...")
    chapters, toc = parse_raw_text(raw_output_path)
    
    print(f"Found TOC with {len(toc)} entries.")
    print(f"Parsed {len(chapters)} chapters.")
    
    # 3. Generate Mnemonics
    print("Generating mnemonics...")
    for chapter in chapters:
        chapter["mnemonics"] = generate_mnemonics_for_chapter(chapter)
        
    # 4. Format Output
    print("Exporting outputs...")
    export_docx(chapters, os.path.join(output_dir, "study_guide.docx"))
    export_md(chapters, os.path.join(output_dir, "study_guide.md"))
    export_notecards(chapters, os.path.join(output_dir, "notecards.txt"))

    print("\nProcess complete! Check the 'output' folder for your generated files.")

if __name__ == "__main__":
    main()
