```bash
pdf-studykit/
├── Dockerfile              # Setup isolation
├── docker-compose.yml      # Future Gui
├── app/
│   ├── main.py             # Starting point
│   ├── extract.py          # PDF extraction logic
│   ├── organize.py         # Structure reconstruction logic
│   ├── mnemonics.py        # Mnemonic generation
│   ├── formatter.py        # Word and Markdown formatting
│   └── utils/
│       ├── toc_parser.py
│       └── keywords.py
├── models/
│   └── (optional for AI/ML mnemonics or NLP models)
├── requirements.txt        # Install all requirement in docker
└── output/
    ├── *.docx
    ├── *.md

```
---

## **Project Goals Checklist**

#### Core Infrastructure

* [X] Create a project directory with a clear modular structure
* [X] Define a `Dockerfile` to containerize the app
* [X] Create a `docker-compose.yml` (optional, for scalability or GUI)
* [X] Prepare `requirements.txt` with all dependencies
* [X] Set up volume mapping for input/output folders in Docker

---

#### PDF Intake and Text Extraction

* [X] Accept and read PDF files
* [X] Extract **all visible text**, preserving:

  * [ ] Headings
  * [ ] Subheadings
  * [ ] Bullet points
  * [ ] Page numbers
* [ ] OCR fallback (optional): Integrate `pytesseract` for scanned PDFs

---

#### Structure Reconstruction

* [ ] Detect and parse the **Table of Contents**
* [x] Extract:
  * [x] Chapter titles
  * [ ] Major points or headings
  * [ ] Keywords (bold/italicized terms)
* [ ] Identify:

  * [ ] Repeated phrases
  * [ ] Glossary terms (if present)
  * [ ] Sidebars, callouts, or summaries

---

#### Mnemonic Generation

* [ ] Generate memory aids for:

  * [ ] Chapter titles
  * [ ] Key points
  * [ ] Important keywords
* [ ] Use:

  * [ ] Wordplay
  * [ ] Absurd imagery
  * [ ] Alliteration or acronyms
* [ ] Keep mnemonics accurate and study-friendly

---

#### Output Format Creation

* [ ] Generate a **Word document (.docx)** with:

  * [ ] Headings/subheadings
  * [ ] Bullet points
  * [ ] Internal hyperlinks (TOC navigation)
  * [ ] Bold/italic formatting
* [ ] Generate a **Markdown (.md)** version with:

  * [ ] Clean formatting
  * [ ] Readability in editors like VS Code or OneNote
* [ ] Generate text file notecards
    * [ ] Each holding a future generated Url of the selected keyword(s).
    

---

#### Reusability & Consistency

* [X] Ensure the full process is **automated inside Docker**
* [x] Create a `main.py` script to orchestrate:

  * [x] Extraction
  * [x] Structuring
  * [ ] Mnemonic generation
  * [ ] Export formatting
* [ ] Validate outputs with test PDFs for consistency
* [ ] (Optional) Add CLI arguments for customization (e.g., "skip TOC", "only output markdown")

---

#### Future Enhancements (Optional but Recommended)

* [ ] Add a simple **Flask or FastAPI GUI**
* [ ] Add drag-and-drop PDF input
* [ ] Save user-defined mnemonics in a local database
* [ ] Export mnemonics to Anki/flashcard format
* [ ] Enable user-defined encoding (e.g., "replace 'confidentiality' with 'secrecy bubble'")

---