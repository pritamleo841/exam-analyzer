# 📂 Documents Folder

Place your exam preparation PDFs here. The app will auto-detect and process them.

## Folder Structure

```
documents/
├── current_affairs/          ← Monthly CA compilation PDFs
│   ├── january_2026.pdf
│   ├── february_2026.pdf
│   ├── march_2026.pdf
│   ├── april_2026.pdf
│   ├── may_2026.pdf
│   └── june_2026.pdf
│
└── previous_year_papers/     ← Previous year question papers
    ├── rbi_grade_b_2025.pdf
    ├── rbi_grade_b_2024.pdf
    ├── rbi_grade_b_2023.pdf
    └── ...
```

## Naming Conventions

### Current Affairs PDFs
The app infers the month from the filename. Use any of these patterns:
- `january_2026.pdf` or `jan_2026.pdf`
- `february.pdf` (year defaults to 2026)
- `march_ca_2026.pdf`
- `ca_april_2026.pdf`
- `2026_may.pdf`
- Case doesn't matter: `JUNE_2026.pdf` works too

### Previous Year Papers
The app infers the year from the filename:
- `rbi_grade_b_2024.pdf`
- `pyq_2023.pdf`
- `2022_phase1.pdf`
- Any filename with a 4-digit year (2018–2026) will be detected

## How It Works
1. Drop PDFs into the appropriate folder
2. Open the app → CA Predictor tab
3. Click "📂 Scan Documents Folder" 
4. The app shows detected files — new ones are highlighted
5. Click "🚀 Process All New" to batch-process everything
6. Already-processed files are automatically skipped

## Notes
- PDF files are **gitignored** (too large for version control)
- Processed data is saved to `C:\exam_analyzer_data\` and persists across sessions
- You can still use the manual upload feature alongside folder scanning
