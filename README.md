# PDF Study Kit

A modular Python tool that extracts text from **PDF** and **EPUB** files, reconstructs document structure, generates AI-powered mnemonics via a local Ollama instance, and exports polished study guides in multiple formats.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Ollama** running locally (optional — needed only for mnemonic generation)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/PDF_Study_Kit.git
cd PDF_Study_Kit

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create input/output directories
mkdir -p input output

# 5. Place your PDF or EPUB files in the input/ folder
cp /path/to/your/book.epub input/

# 6. Run the application
python app/main.py
```

The CLI will list available files in `input/` — type the full filename (including extension) and press Enter.

### Docker Setup

```bash
# 1. Create input/output directories and add your files
mkdir -p input output
cp /path/to/your/book.pdf input/

# 2. Build and run with Docker Compose
docker compose up --build
```

Volume mounts (`./input:/input` and `./output:/output`) keep your files accessible on the host.

### Mnemonic Generation (Optional)

Mnemonics require a local **Ollama** server with a model pulled:

```bash
# Install Ollama (https://ollama.com)
# Then pull a model:
ollama pull dolphin-llama3

# Ollama runs on http://localhost:11434 by default
```

If Ollama is not running, the pipeline still completes — mnemonics will show a fallback placeholder instead.
To use a different model, edit the `model` field in `app/mnemonics.py`.

### Output

After processing, check the `output/` folder:

| File                 | Description                                   |
|----------------------|-----------------------------------------------|
| `raw_text.txt`       | Extracted markdown-formatted text              |
| `study_guide.docx`   | Word document with headings, bullets, mnemonics|
| `study_guide.md`     | Markdown version for VS Code / note-taking     |
| `notecards.txt`      | `keyword | mnemonic` pairs, one per line       |

---

## Project Structure

```
PDF_Study_Kit/
├── Dockerfile              # Container setup
├── docker-compose.yml      # Docker orchestration with volume mounts
├── requirements.txt        # Python dependencies
├── input/                  # Drop PDF / EPUB files here
├── output/                 # Generated study materials
├── app/
│   ├── main.py             # CLI entry point and pipeline orchestrator
│   ├── extract.py          # PDF text extraction (PyMuPDF)
│   ├── extract_epub.py     # EPUB text extraction (ebooklib + BeautifulSoup)
│   ├── organize.py         # Structure reconstruction (chapters, TOC, keywords)
│   ├── mnemonics.py        # AI mnemonic generation via Ollama API
│   ├── formatter.py        # Export to .docx, .md, and notecards
│   └── utils/
│       ├── toc_parser.py   # Table of Contents detection
│       └── keywords.py     # Bold-term keyword extraction
└── models/                 # (Optional) future AI/NLP model files
```

---

## Project Goals Checklist

#### Core Infrastructure

* [x] Create a project directory with a clear modular structure
* [x] Define a `Dockerfile` to containerize the app
* [x] Create a `docker-compose.yml` (optional, for scalability or GUI)
* [x] Prepare `requirements.txt` with all dependencies
* [x] Set up volume mapping for input/output folders in Docker

---

#### PDF Intake and Text Extraction

* [x] Accept and read PDF files
* [x] Extract **all visible text**, preserving:
  * [x] Headings (detected via font size heuristics)
  * [x] Subheadings (same heuristic, `## ` markdown prefix)
  * [x] Bullet points (`•` and `-` converted to `- ` markdown)
  * [x] Page numbers (`--- Page N ---` separators)
* [ ] OCR fallback (optional): Integrate `pytesseract` for scanned PDFs

---

#### EPUB Intake and Text Extraction

* [x] Accept and read EPUB files via `ebooklib`
* [x] Extract all visible text, preserving:
  * [x] Headings (h1–h6 → `##` markdown)
  * [x] Bold / italic inline formatting
  * [x] Bullet points / list items
  * [x] Blockquotes / callouts
* [x] Output matches PDF extractor format for seamless pipeline reuse

---

#### Structure Reconstruction

* [x] Detect and parse the **Table of Contents** (via `toc_parser.py`)
* [x] Extract:
  * [x] Chapter titles (regex match on `## Chapter N` headings)
  * [x] Major points or headings (all `##` lines preserved in content)
  * [x] Keywords (bold/`**` terms extracted via `keywords.py`)
* [ ] Identify:
  * [ ] Repeated phrases
  * [ ] Glossary terms (if present)
  * [ ] Sidebars, callouts, or summaries

---

#### Mnemonic Generation

* [x] Generate memory aids for:
  * [x] Important keywords (all bold terms extracted per chapter)
  * [ ] Chapter titles
  * [ ] Key points
* [x] Use Ollama API with prompt requesting:
  * [x] Wordplay
  * [x] Absurd imagery
  * [x] Alliteration or acronyms
* [ ] Keep mnemonics accurate and study-friendly (depends on model quality)

---

#### Output Format Creation

* [x] Generate a **Word document (.docx)** with:
  * [x] Headings/subheadings
  * [x] Bullet points
  * [ ] Internal hyperlinks (TOC navigation)
  * [ ] Bold/italic formatting (currently stripped for simplicity)
* [x] Generate a **Markdown (.md)** version with:
  * [x] Clean formatting
  * [x] Readability in editors like VS Code or OneNote
* [x] Generate text file notecards
  * [ ] Each holding a future generated URL of the selected keyword(s)

---

#### Reusability & Consistency

* [x] Ensure the full process is **automated inside Docker**
* [x] Create a `main.py` script to orchestrate:
  * [x] Extraction
  * [x] Structuring
  * [x] Mnemonic generation
  * [x] Export formatting
* [ ] Validate outputs with test PDFs/EPUBs for consistency
* [ ] (Optional) Add CLI arguments for customization (e.g., "skip TOC", "only output markdown")

---

#### Future Enhancements (Optional but Recommended)

* [ ] Add a simple **Flask or FastAPI GUI**
* [ ] Add drag-and-drop PDF input
* [ ] Save user-defined mnemonics in a local database
* [ ] Export mnemonics to Anki/flashcard format
* [ ] Enable user-defined encoding (e.g., "replace 'confidentiality' with 'secrecy bubble'")

---