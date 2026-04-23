"""
Persistent local storage layer — stores all CA analysis data on disk
so it survives Streamlit reruns and app restarts.

Storage location: C:\\exam_analyzer_data\\
"""
import json
import os
import shutil
from pathlib import Path
from datetime import datetime


# Base path on C: drive as requested by user
STORAGE_BASE = Path(r"C:\exam_analyzer_data")

# Sub-directories
UPLOADS_DIR = STORAGE_BASE / "uploads"
EXTRACTED_DIR = STORAGE_BASE / "extracted"
PYQ_PATTERNS_DIR = STORAGE_BASE / "pyq_patterns"
ANALYSIS_DIR = STORAGE_BASE / "analysis"
REPORTS_DIR = STORAGE_BASE / "reports"

ALL_DIRS = [UPLOADS_DIR, EXTRACTED_DIR, PYQ_PATTERNS_DIR, ANALYSIS_DIR, REPORTS_DIR]


def init_storage():
    """Create all storage directories if they don't exist."""
    for d in ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def _safe_filename(name: str) -> str:
    """Sanitize a string for use as a filename."""
    return "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in name)


# ─── CA PDF extracted content ──────────────────────────────────────────────

def save_ca_extracted(month: str, year: int, data: dict):
    """Save extracted CA content for a given month.

    data should contain: {text, facts, questions, source_file, extracted_at}
    """
    init_storage()
    key = _safe_filename(f"{year}_{month}")
    path = EXTRACTED_DIR / f"{key}.json"
    data["_month"] = month
    data["_year"] = year
    data["_saved_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_ca_extracted(month: str, year: int) -> dict | None:
    """Load previously extracted CA content for a month."""
    key = _safe_filename(f"{year}_{month}")
    path = EXTRACTED_DIR / f"{key}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_all_ca_extracted() -> list[dict]:
    """Load all extracted CA content across all months."""
    init_storage()
    results = []
    for path in sorted(EXTRACTED_DIR.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def delete_ca_extracted(month: str, year: int):
    """Delete extracted content for a specific month."""
    key = _safe_filename(f"{year}_{month}")
    path = EXTRACTED_DIR / f"{key}.json"
    if path.exists():
        path.unlink()


# ─── PYQ CA patterns ───────────────────────────────────────────────────────

def save_pyq_pattern(year: int, data: dict):
    """Save extracted PYQ CA pattern for a given year.

    data: {year, total_questions, categories: {cat: {count, pct, difficulty_dist, sample_topics}}}
    """
    init_storage()
    path = PYQ_PATTERNS_DIR / f"pyq_{year}.json"
    data["_year"] = year
    data["_saved_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_pyq_pattern(year: int) -> dict | None:
    """Load PYQ pattern for a specific year."""
    path = PYQ_PATTERNS_DIR / f"pyq_{year}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_all_pyq_patterns() -> list[dict]:
    """Load all PYQ patterns across all years."""
    init_storage()
    results = []
    for path in sorted(PYQ_PATTERNS_DIR.glob("pyq_*.json")):
        with open(path, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def delete_pyq_pattern(year: int):
    """Delete PYQ pattern for a specific year."""
    path = PYQ_PATTERNS_DIR / f"pyq_{year}.json"
    if path.exists():
        path.unlink()


# ─── Analysis results ──────────────────────────────────────────────────────

def save_analysis_results(data: dict):
    """Save the latest predictive analysis results.

    data: {predictions[], category_weights{}, metadata{}}
    """
    init_storage()
    data["_saved_at"] = datetime.now().isoformat()
    path = ANALYSIS_DIR / "latest_analysis.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_analysis_results() -> dict | None:
    """Load the latest analysis results."""
    path = ANALYSIS_DIR / "latest_analysis.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


# ─── Generated reports ──────────────────────────────────────────────────────

def save_report(html_content: str, name: str = "ca_predictions") -> Path:
    """Save a generated HTML report and return its path."""
    init_storage()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{_safe_filename(name)}_{timestamp}.html"
    path = REPORTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return path


def load_latest_report() -> str | None:
    """Load the most recently generated report."""
    reports = sorted(REPORTS_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    if reports:
        with open(reports[0], "r", encoding="utf-8") as f:
            return f.read()
    return None


# ─── Upload tracking ───────────────────────────────────────────────────────

def save_upload_record(filename: str, month: str, year: int, upload_type: str, status: str = "processed"):
    """Track an uploaded file."""
    init_storage()
    manifest_path = UPLOADS_DIR / "manifest.json"
    manifest = []
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    manifest.append({
        "filename": filename,
        "month": month,
        "year": year,
        "type": upload_type,  # "ca_monthly" or "pyq_ca"
        "status": status,
        "uploaded_at": datetime.now().isoformat(),
    })

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def load_upload_manifest() -> list[dict]:
    """Load the upload manifest."""
    manifest_path = UPLOADS_DIR / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ─── Bulk state save/restore ──────────────────────────────────────────────

def save_full_state(state: dict):
    """Save the entire CA predictor state for session restore."""
    init_storage()
    path = ANALYSIS_DIR / "session_state.json"
    state["_saved_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, default=str)


def load_full_state() -> dict | None:
    """Load previously saved session state."""
    path = ANALYSIS_DIR / "session_state.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_storage_summary() -> dict:
    """Get a summary of what's stored."""
    init_storage()
    ca_months = len(list(EXTRACTED_DIR.glob("*.json")))
    pyq_years = len(list(PYQ_PATTERNS_DIR.glob("pyq_*.json")))
    reports = len(list(REPORTS_DIR.glob("*.html")))
    has_analysis = (ANALYSIS_DIR / "latest_analysis.json").exists()
    return {
        "ca_months_uploaded": ca_months,
        "pyq_years_uploaded": pyq_years,
        "reports_generated": reports,
        "has_analysis": has_analysis,
        "storage_path": str(STORAGE_BASE),
    }
