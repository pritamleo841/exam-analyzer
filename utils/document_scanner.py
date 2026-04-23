"""
Document Scanner — detects PDFs in the documents/ folder,
infers month/year from filenames, and reports which are new vs. already processed.
"""
import re
from pathlib import Path

from config import CA_DOCUMENTS_DIR, PYQ_DOCUMENTS_DIR, CA_MONTHS
from storage.local_store import load_upload_manifest

# Month name → canonical month mapping (handles abbreviations)
_MONTH_MAP: dict[str, str] = {}
for _m in CA_MONTHS:
    _MONTH_MAP[_m.lower()] = _m
    _MONTH_MAP[_m[:3].lower()] = _m  # jan, feb, ...

# Regex to find a 4-digit year in a filename
_YEAR_RE = re.compile(r"(20[12]\d)")

# Regex to find a month name/abbreviation in a filename
_MONTH_RE = re.compile(
    r"(january|february|march|april|may|june|july|august|september|october|november|december"
    r"|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
    re.IGNORECASE,
)


def _infer_month(filename: str) -> str:
    """Infer the month from a filename. Returns canonical month name or ''."""
    m = _MONTH_RE.search(filename.lower())
    if m:
        return _MONTH_MAP.get(m.group(1).lower(), "")
    return ""


def _infer_year(filename: str, default: int = 2026) -> int:
    """Infer a 4-digit year from a filename. Returns default if not found."""
    m = _YEAR_RE.search(filename)
    if m:
        return int(m.group(1))
    return default


def scan_ca_folder() -> list[dict]:
    """Scan documents/current_affairs/ for PDF files.

    Returns a list of dicts:
        [{"path": Path, "filename": str, "month": str, "year": int,
          "status": "new"|"processed", "uploaded_at": str}]
    """
    folder = Path(CA_DOCUMENTS_DIR)
    if not folder.exists():
        return []

    manifest = load_upload_manifest()
    processed_files = {
        m["filename"] for m in manifest if m.get("type") == "ca_monthly"
    }

    results = []
    for pdf in sorted(folder.glob("*.pdf")):
        fname = pdf.name
        month = _infer_month(fname)
        year = _infer_year(fname)

        is_processed = fname in processed_files
        uploaded_at = ""
        if is_processed:
            for m in manifest:
                if m.get("filename") == fname and m.get("type") == "ca_monthly":
                    uploaded_at = m.get("uploaded_at", "")
                    break

        results.append({
            "path": pdf,
            "filename": fname,
            "month": month,
            "year": year,
            "status": "processed" if is_processed else "new",
            "uploaded_at": uploaded_at,
        })

    return results


def scan_pyq_folder() -> list[dict]:
    """Scan documents/previous_year_papers/ for PDF/TXT/CSV files.

    Returns a list of dicts:
        [{"path": Path, "filename": str, "year": int,
          "status": "new"|"processed", "uploaded_at": str}]
    """
    folder = Path(PYQ_DOCUMENTS_DIR)
    if not folder.exists():
        return []

    manifest = load_upload_manifest()
    processed_files = {
        m["filename"] for m in manifest if m.get("type") == "pyq_ca"
    }

    results = []
    for ext in ("*.pdf", "*.txt", "*.csv"):
        for f in sorted(folder.glob(ext)):
            fname = f.name
            year = _infer_year(fname, default=0)

            is_processed = fname in processed_files
            uploaded_at = ""
            if is_processed:
                for m in manifest:
                    if m.get("filename") == fname and m.get("type") == "pyq_ca":
                        uploaded_at = m.get("uploaded_at", "")
                        break

            results.append({
                "path": f,
                "filename": fname,
                "year": year,
                "status": "processed" if is_processed else "new",
                "uploaded_at": uploaded_at,
            })

    return results


def get_scan_summary() -> dict:
    """Quick summary of what's in the documents folder."""
    ca_files = scan_ca_folder()
    pyq_files = scan_pyq_folder()
    return {
        "ca_total": len(ca_files),
        "ca_new": sum(1 for f in ca_files if f["status"] == "new"),
        "ca_processed": sum(1 for f in ca_files if f["status"] == "processed"),
        "pyq_total": len(pyq_files),
        "pyq_new": sum(1 for f in pyq_files if f["status"] == "new"),
        "pyq_processed": sum(1 for f in pyq_files if f["status"] == "processed"),
    }
