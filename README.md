# Agent-as-Coder Challenge – Bank Statement Parser

This project implements an **AI agent** that can automatically generate custom parsers for bank statement PDFs.  
The agent follows a loop: **plan → generate code → run tests → self-fix** (up to 3 attempts).  

---

## 🚀 How to Run

### 1. Clone the repo & set up environment
```bash
git clone <your-repo-url>
cd karbon_ai_challenge
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate sample PDF (for ICICI example)
```bash
python generate_sample_pdf.py
```

### 4. Run the agent
```bash
python b1.py --target icici
```

This will:
- Read `data/icici/icici_sample.pdf` and `.csv`
- Generate `custom_parser/icici_parser.py` if missing
- Parse the PDF and compare output with the CSV

### 5. Run tests
```bash
pytest -q
```

If successful, you should see:
```
.
1 passed in 0.7s
```

---

## 🧩 Agent Loop Diagram

```
 ┌─────────────┐
 │   Planner   │  ← decides which parser code to generate
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Code Writer │  ← writes parser (e.g., icici_parser.py)
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Test Runner │  ← runs parse() and compares with CSV
 └─────┬───────┘
       │ pass/fail
       ▼
 ┌─────────────┐
 │ Self-Fixer  │  ← if fail, regenerates parser (max 3 tries)
 └─────────────┘
```

---

## 📂 Project Structure
```
karbon_ai_challenge/
│── b1.py                   # Main agent loop
│── requirements.txt
│── generate_sample_pdf.py   # Creates dummy ICICI PDF
│── custom_parser/
│     ├── __init__.py
│     ├── base_parser.py
│     └── icici_parser.py
│── data/
│     └── icici/
│          ├── icici_sample.csv
│          └── icici_sample.pdf
│── tests/
│     ├── __init__.py
│     └── test_parser.py
```

---

## ✨ Notes
- Currently the agent retries with a template parser.  
- For higher autonomy, it can be extended with LLMs (e.g., Google Gemini, Groq, OpenAI) to refine the parser dynamically.  
- Demo requirement: run from a fresh clone → install deps → run agent → pytest green (≤ 60s).  
