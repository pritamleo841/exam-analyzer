# 🎯 Exam Paper Analyzer Pro

AI-powered exam preparation tool for banking & regulatory exams. Analyze previous year papers, predict high-probability topics, study current affairs with AI-generated predictions, and deploy a searchable study portal to GitHub Pages.

**Target Exam:** RBI Grade B 2026 (also supports SEBI Grade A, NABARD Grade A, IBPS PO/Clerk, SBI PO/Clerk, and custom exams)

---

## Features

### 📄 PYQ Analysis
- **PDF & Text Parsing** — Upload PDFs, CSVs, or paste text (4-level fallback: pdfplumber → PyMuPDF → OCR → AI Vision)
- **Auto-Categorization** — Rule-based (free, offline) or AI-powered (OpenAI/Gemini/Ollama)
- **Frequency Analysis** — Topic × Year matrix with probability scoring
- **Trend Detection** — Rising/falling topics, new entries, difficulty shifts
- **Predictions** — Expected topic distribution for the next exam
- **Sample Questions** — Template-based or AI-generated practice questions
- **Export Reports** — Excel (multi-sheet), HTML (interactive dashboard), PDF (formatted report)

### 🔮 CA Predictive Analyzer
- **Monthly CA Processing** — Upload Jan–Jun 2026 CA compilations, AI extracts exam-relevant facts + MCQs
- **PYQ Pattern Learning** — Upload previous year CA papers to learn category weightages
- **Predictive Engine** — Weighted scoring: PYQ frequency (40%) + AI importance (35%) + recency (25%)
- **17 CA Sections** — Union Budget, Economic Survey, RBI & Monetary Policy, Banking & Finance, Reports & Indices, Government Schemes, International Orgs, Financial Markets, Social Issues, Appointments & Awards, Agriculture, External Sector, Insurance & Pension, Science & Technology, Environment, Defence & Security, Sports & Events
- **Sectioned HTML Report** — Standalone report with section navigation, collapsible MCQs, priority badges

### 🚀 GitHub Pages Study Portal
- **One-click deployment** to GitHub Pages — accessible from any device
- **Sidebar navigation** across all 17 CA sections
- **Full-text search** across all facts and questions with highlighting
- **Filters** — by category, importance (High/Medium/Low), month, probability; multiple sort options
- **Revision & Recall mode** — facts blur-hidden, click to reveal, mark as Remembered/Revise Again
- **Bookmarking** — star any fact for quick revision (stored in browser)
- **MCQ practice** with answer checking, scoring, and explanations
- **Study time allocation** chart
- **Dark mode**, mobile responsive, print-friendly

### 📂 Document Folder Auto-Scan
- Drop PDFs into `documents/current_affairs/` and `documents/previous_year_papers/`
- App auto-detects new files by filename pattern, skips already-processed ones
- **Batch processing** — "Process All New" button to ingest everything at once

### 💾 Persistent Storage
- All data saved to `C:\exam_analyzer_data\` — survives app restarts
- Tracks uploaded files, extracted facts, PYQ patterns, analysis results, and reports

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

The app opens at `http://localhost:8501`.

---

## Usage

### PYQ Analysis Workflow
1. **Upload Papers** — Upload PDF/CSV/TXT of previous year papers, tag with year and phase
2. **Choose Categorization** — Rule-based (free) or AI-powered (OpenAI/Gemini/Ollama)
3. **View Dashboard** — Frequency heatmap, section distribution, topic trends, difficulty analysis
4. **Generate Predictions** — Expected topic distribution + sample questions
5. **Export** — Excel, HTML, or PDF reports

### CA Predictive Analysis Workflow
1. **Upload CA PDFs** — Drop monthly CA compilations into `documents/current_affairs/` or upload via the app
2. **Upload PYQ Papers** (optional) — Drop previous year CA papers into `documents/previous_year_papers/` or upload via the app
3. **Run Analysis** — AI scores every fact by exam probability, groups into 17 sections
4. **View Report** — Download standalone HTML or view in-app
5. **Deploy to GitHub Pages** — Push to a GitHub repo for a searchable study portal

### Document Folder Setup
Place your PDFs in the `documents/` folder:
```
documents/
├── current_affairs/
│   ├── january_2026.pdf
│   ├── february_2026.pdf
│   ├── march_2026.pdf
│   ├── april_2026.pdf
│   ├── may_2026.pdf
│   └── june_2026.pdf
└── previous_year_papers/
    ├── rbi_2024_phase1.pdf
    ├── rbi_2023_phase1.pdf
    └── rbi_2022_phase1.pdf
```

**Naming conventions:**
- CA: `{month}_{year}.pdf` or `{month}.pdf` (e.g., `january_2026.pdf`, `jan_2026.pdf`, `march.pdf`)
- PYQ: `{exam}_{year}.pdf` or `pyq_{year}.pdf` (e.g., `rbi_2024.pdf`, `pyq_2023_phase1.pdf`)

The app auto-detects month/year from the filename.

---

## GitHub Pages Deployment

1. Create an **empty GitHub repository** (e.g., `rbi-ca-predictions`)
2. In the app, go to **CA Predictor → 🚀 GitHub Pages** tab
3. Paste the repo URL → **Initialize / Connect Repository**
4. Run analysis first (Upload CAs → Run Analysis)
5. Click **🚀 Deploy to GitHub Pages**
6. In your GitHub repo: **Settings → Pages → Branch: gh-pages** → Save
7. Site will be live at `https://username.github.io/repo-name/`

Every re-deploy updates the site with all accumulated data.

---

## AI Providers

| Method | Accuracy | Cost | Speed | Offline |
|--------|----------|------|-------|---------|
| Rule-Based | ~60-75% | Free | Instant | ✅ Yes |
| OpenAI GPT | ~85-95% | ~$0.01-0.05/paper | Fast | ❌ No |
| Google Gemini | ~85-90% | Free tier available | Fast | ❌ No |
| Ollama (Local) | ~75-85% | Free | Slower | ✅ Yes |

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
├── app.py                          # Streamlit web app (main entry point)
├── config.py                       # Data models, exam configs, CA settings
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── parsers/
│   ├── pdf_parser.py               # PDF text extraction (4-level fallback)
│   └── text_parser.py              # Text/CSV input handling
│
├── categorizers/
│   ├── base.py                     # Abstract categorizer interface
│   ├── rule_categorizer.py         # Keyword-based categorization
│   ├── ai_categorizer.py           # AI-powered categorization
│   └── prompts.py                  # AI prompt templates (incl. CA fact extraction)
│
├── analyzers/
│   ├── frequency.py                # Frequency matrix & probability scoring
│   ├── trends.py                   # Trend detection & analysis
│   ├── predictor.py                # Topic prediction & question generation
│   ├── ca_pattern_analyzer.py      # PYQ CA pattern extraction
│   └── ca_predictor.py             # CA predictive engine (weighted scoring)
│
├── generators/
│   ├── question_generator.py       # Mock test question generation
│   └── ca_question_generator.py    # CA fact extraction + MCQ generation
│
├── exporters/
│   ├── excel_export.py             # Multi-sheet Excel report
│   ├── html_export.py              # Interactive HTML dashboard
│   ├── pdf_export.py               # Formatted PDF report
│   ├── mock_test_export.py         # Mock test PDF export
│   ├── ca_html_report.py           # Standalone CA predictions HTML report
│   └── ca_site_builder.py          # GitHub Pages study portal builder
│
├── deployer/
│   └── github_pages.py             # GitHub Pages git deploy (init/push/status)
│
├── storage/
│   └── local_store.py              # Persistent storage at C:\exam_analyzer_data
│
├── utils/
│   ├── document_scanner.py         # Auto-detect new PDFs in documents/ folder
│   └── batch_processor.py          # Batch process all new documents
│
├── documents/
│   ├── current_affairs/            # Drop monthly CA PDFs here
│   ├── previous_year_papers/       # Drop PYQ papers here
│   └── README.md                   # Naming conventions guide
│
├── data/
│   ├── current_affairs.py          # Built-in CA facts & MCQs
│   ├── rbi_grade_b.py              # RBI Grade B study material
│   └── taxonomies/                 # Pre-built topic trees per exam
│       ├── rbi_grade_b.json
│       ├── sebi_grade_a.json
│       ├── nabard_grade_a.json
│       ├── banking_generic.json
│       └── ca_taxonomy.json        # 17-section CA taxonomy
```

---

## Persistent Storage

All data is saved to `C:\exam_analyzer_data\` and persists across app restarts:

```
C:\exam_analyzer_data\
├── uploads/manifest.json           # Track all uploaded files
├── extracted/                      # CA facts+questions per month
│   ├── 2026_january.json
│   └── ...
├── pyq_patterns/                   # PYQ analysis per year
│   ├── pyq_2024.json
│   └── ...
├── analysis/latest_analysis.json   # Predictive analysis results
├── reports/                        # Generated HTML reports
└── gh-pages-site/                  # GitHub Pages local repo
```

---

## Troubleshooting

**"Could not extract text from PDF"**
- The PDF may be scanned/image-based. The app tries pdfplumber → PyMuPDF → OCR → AI Vision automatically.
- For best results, use text-based PDFs (most CA compilations are text-based).

**"AI categorization failed"**
- Check your API key is valid
- For Ollama: make sure it's running (`ollama serve`)
- The app will automatically fall back to rule-based if AI fails

**"GitHub Pages deploy failed"**
- Make sure Git is installed and in PATH
- Set up git credentials (SSH key or credential manager)
- Ensure the GitHub repo exists and you have push access

**Charts not loading**
- Make sure `plotly` is installed: `pip install plotly`
- Try refreshing the browser page

**Scanner not detecting my PDFs**
- Check filename follows the naming convention (see `documents/README.md`)
- Month names should be in the filename: `january`, `jan`, `feb`, etc.
- Year (4 digits) should be in the filename for PYQ papers

---

## License

This project is for personal/educational use.
