# 📊 Exam Paper Analyzer

Analyze previous year question papers for banking & regulatory exams, identify high-probability topics, and predict what's coming next.

**Supported Exams:** RBI Grade B, SEBI Grade A, NABARD Grade A, IBPS PO/Clerk, SBI PO/Clerk, and custom exams.

---

## Features

- **PDF & Text Parsing** — Upload PDFs, CSVs, or paste text directly
- **Auto-Categorization** — Rule-based (free, offline) or AI-powered (OpenAI/Gemini/Ollama)
- **Frequency Analysis** — Topic × Year matrix with probability scoring
- **Trend Detection** — Rising/falling topics, new entries, difficulty shifts
- **Predictions** — Expected topic distribution for the next exam
- **Sample Questions** — Template-based or AI-generated practice questions
- **Export Reports** — Excel (multi-sheet), HTML (interactive dashboard), PDF (formatted report)

---

## Quick Start

### 1. Install Python 3.11+

Download from [python.org](https://www.python.org/downloads/) if not installed.

### 2. Install Dependencies

```bash
cd C:\exam-analyzer
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Usage

### Step 1 — Upload Papers
- Upload PDF/CSV/TXT files of previous year question papers
- Tag each file with the **year** and **phase** (Phase 1, Phase 2, Prelims, Mains)
- You can also paste questions directly as text

### Step 2 — Choose Categorization Method
- **Rule-Based (default):** Free, works offline, no API key needed. Uses keyword matching against built-in topic taxonomies. ~60-75% accuracy.
- **AI-Powered (OpenAI/Gemini/Ollama):** More accurate (~85-95%). Needs API key (except Ollama which runs locally).

### Step 3 — View Dashboard
- Interactive charts: frequency heatmap, section distribution, topic trends, difficulty analysis
- Filter by section
- See probability rankings for each topic

### Step 4 — Generate Predictions
- Click "Generate Predictions" to see expected topic distribution for the next exam
- View sample questions for top topics

### Step 5 — Export Reports
- **Excel:** Multi-sheet workbook with frequency matrix, rankings, trends, predictions
- **HTML:** Standalone interactive dashboard (share with anyone — no software needed)
- **PDF:** Formatted report with executive summary and study priority recommendations

---

## Categorization Methods

| Method | Accuracy | Cost | Speed | Offline |
|--------|----------|------|-------|---------|
| Rule-Based | ~60-75% | Free | Instant | ✅ Yes |
| OpenAI GPT | ~85-95% | ~$0.01-0.05/paper | Fast | ❌ No |
| Google Gemini | ~85-90% | Free tier available | Fast | ❌ No |
| Ollama (Local) | ~75-85% | Free | Slower | ✅ Yes |

### Setting up AI Providers

**OpenAI:** Get API key from [platform.openai.com](https://platform.openai.com/api-keys)

**Google Gemini:** Get API key from [aistudio.google.com](https://aistudio.google.com/apikey)

**Ollama (Local, Free):**
1. Install from [ollama.com](https://ollama.com)
2. Run: `ollama pull llama3`
3. Keep Ollama running in background
4. Select "Ollama" in the app — no API key needed

---

## Project Structure

```
exam-analyzer/
├── app.py                      # Streamlit web app (main entry point)
├── config.py                   # Data models, exam configs
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── parsers/
│   ├── pdf_parser.py           # PDF text extraction & question splitting
│   └── text_parser.py          # Text/CSV input handling
├── categorizers/
│   ├── base.py                 # Abstract categorizer interface
│   ├── rule_categorizer.py     # Keyword-based categorization
│   ├── ai_categorizer.py       # AI-powered categorization (OpenAI/Gemini/Ollama)
│   └── prompts.py              # AI prompt templates
├── analyzers/
│   ├── frequency.py            # Frequency matrix & probability scoring
│   ├── trends.py               # Trend detection & analysis
│   └── predictor.py            # Topic prediction & question generation
├── exporters/
│   ├── excel_export.py         # Multi-sheet Excel report
│   ├── html_export.py          # Interactive HTML dashboard
│   └── pdf_export.py           # Formatted PDF report
└── data/
    └── taxonomies/             # Pre-built topic trees per exam
        ├── rbi_grade_b.json
        ├── sebi_grade_a.json
        ├── nabard_grade_a.json
        └── banking_generic.json
```

---

## Troubleshooting

**"Could not extract text from PDF"**
- The PDF may be scanned/image-based. Convert it to text first using any OCR tool, or use the text input option.

**"AI categorization failed"**
- Check your API key is valid
- For Ollama: make sure it's running (`ollama serve`)
- The app will automatically fall back to rule-based if AI fails

**Charts not loading**
- Make sure `plotly` is installed: `pip install plotly`
- Try refreshing the browser page

---

## License

This project is for personal/educational use.
