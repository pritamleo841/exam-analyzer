"""
Batch Processor — processes all new PDFs from the documents/ folder in one go.
Reads files from disk, calls existing extraction/analysis functions, saves results.
"""
from pathlib import Path

from parsers.pdf_parser import extract_text_from_pdf, split_into_questions
from parsers.text_parser import parse_text_input, parse_csv_input
from generators.ca_question_generator import extract_facts_from_pdfs
from analyzers.ca_pattern_analyzer import analyze_pyq_paper
from storage.local_store import (
    save_ca_extracted, save_upload_record, load_all_ca_extracted,
    save_pyq_pattern, load_all_pyq_patterns, save_full_state,
)


def batch_process_ca(
    new_files: list[dict],
    ai_caller,
    exam_name: str = "RBI Grade B",
    progress_callback=None,
) -> dict:
    """Process all new CA PDFs from the documents folder.

    Args:
        new_files: List from scan_ca_folder() filtered to status=="new".
                   Each dict has: path, filename, month, year
        ai_caller: AI callable(prompt) -> str
        exam_name: Target exam name
        progress_callback: Optional callable(current, total, message)

    Returns:
        {"processed": int, "skipped": int, "total_facts": int, "total_questions": int, "errors": list}
    """
    result = {"processed": 0, "skipped": 0, "total_facts": 0, "total_questions": 0, "errors": []}
    total = len(new_files)

    for i, file_info in enumerate(new_files):
        path: Path = file_info["path"]
        fname = file_info["filename"]
        month = file_info["month"]
        year = file_info["year"]

        if not month:
            result["skipped"] += 1
            result["errors"].append(f"{fname}: Could not infer month from filename. Rename to include month (e.g. january_2026.pdf).")
            if progress_callback:
                progress_callback(i, total, f"Skipped {fname} — unknown month")
            continue

        if progress_callback:
            progress_callback(i, total, f"Processing {fname} ({month} {year})...")

        try:
            file_bytes = path.read_bytes()
            pdf_list = [(fname, file_bytes)]
            month_map = {fname: month}

            extraction = extract_facts_from_pdfs(
                pdf_files=pdf_list,
                ai_caller=ai_caller,
                month_map=month_map,
                exam_name=exam_name,
            )

            facts = extraction.get("facts", [])
            questions = extraction.get("questions", [])

            # Save to persistent storage
            save_ca_extracted(month, year, {
                "facts": facts,
                "questions": questions,
                "source_file": fname,
            })
            save_upload_record(fname, month, year, "ca_monthly")

            result["processed"] += 1
            result["total_facts"] += len(facts)
            result["total_questions"] += len(questions)

        except Exception as e:
            result["skipped"] += 1
            result["errors"].append(f"{fname}: {e}")

    if progress_callback:
        progress_callback(total, total, "Batch processing complete!")

    return result


def batch_process_pyq(
    new_files: list[dict],
    ai_caller=None,
    exam_name: str = "RBI Grade B",
    progress_callback=None,
) -> dict:
    """Process all new PYQ papers from the documents folder.

    Args:
        new_files: List from scan_pyq_folder() filtered to status=="new".
                   Each dict has: path, filename, year
        ai_caller: Optional AI callable(prompt) -> str
        exam_name: Target exam name
        progress_callback: Optional callable(current, total, message)

    Returns:
        {"processed": int, "skipped": int, "total_questions": int, "errors": list}
    """
    result = {"processed": 0, "skipped": 0, "total_questions": 0, "errors": []}
    total = len(new_files)

    for i, file_info in enumerate(new_files):
        path: Path = file_info["path"]
        fname = file_info["filename"]
        year = file_info["year"]

        if year == 0:
            result["skipped"] += 1
            result["errors"].append(f"{fname}: Could not infer year from filename. Rename to include year (e.g. rbi_2024.pdf).")
            if progress_callback:
                progress_callback(i, total, f"Skipped {fname} — unknown year")
            continue

        if progress_callback:
            progress_callback(i, total, f"Processing {fname} (Year {year})...")

        try:
            file_bytes = path.read_bytes()
            suffix = path.suffix.lower()

            # Parse based on file type
            if suffix == ".pdf":
                text = extract_text_from_pdf(file_bytes)
                qs = split_into_questions(text, year, "Phase 1", exam_name)
            elif suffix == ".csv":
                qs = parse_csv_input(file_bytes, year, "Phase 1", exam_name)
            else:  # .txt
                qs = parse_text_input(
                    file_bytes.decode("utf-8", errors="replace"),
                    year, "Phase 1", exam_name,
                )

            q_dicts = [{"text": q.text, "question_number": q.question_number} for q in qs]

            pattern = analyze_pyq_paper(q_dicts, ai_caller=ai_caller)
            pattern["year"] = year
            pattern["source_file"] = fname

            save_pyq_pattern(year, pattern)
            save_upload_record(fname, "", year, "pyq_ca")

            result["processed"] += 1
            result["total_questions"] += pattern.get("total_questions", len(q_dicts))

        except Exception as e:
            result["skipped"] += 1
            result["errors"].append(f"{fname}: {e}")

    if progress_callback:
        progress_callback(total, total, "Batch processing complete!")

    return result
