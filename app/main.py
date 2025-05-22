import tkinter as tk
from tkinter import filedialog
import shutil
import os
from extract import extract_text

def choose_file_gui():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        return file_path if file_path else None
    except Exception as e:
        print(f"⚠️ GUI failed: {e}")
        return None

def choose_file_cli():
    print("📂 Available PDFs in /input:")
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
        print(f"❌ File not found: {file_path}")
        return

    print(f"📄 Processing: {os.path.basename(file_path)}")
    output = extract_text(file_path)

    with open("/output/raw_text.txt", "w", encoding="utf-8") as f:
        f.write(output)

    print("✅ Text extraction complete. Output saved to /output/raw_text.txt")

if __name__ == "__main__":
    main()
