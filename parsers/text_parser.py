"""
Text Parser - Handles plain text, CSV, and structured text input.
Converts raw text input into Question objects.
"""
import re
import csv
import io
from config import Question


def parse_text_input(
    text: str,
    year: int,
    phase: str,
    exam_type: str,
) -> list[Question]:
    """
    Parse plain text containing exam questions.
    Supports multiple formats:
    - Numbered questions (1. / Q1. / (1) etc.)
    - Section headers before question groups
    - Free-form text split by blank lines
    """
    from parsers.pdf_parser import split_into_questions
    return split_into_questions(text, year, phase, exam_type)


def parse_csv_input(
    file_bytes: bytes,
    year: int,
    phase: str,
    exam_type: str,
) -> list[Question]:
    """
    Parse CSV file with questions.
    Expected columns (flexible matching):
    - question / text / q / question_text — the question text (required)
    - number / q_no / question_number — question number (optional)
    - section — section name (optional)
    - topic — topic name (optional)
    - sub_topic — sub-topic (optional)
    - year — override year (optional)
    - phase — override phase (optional)
    """
    text = file_bytes.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    # Normalize column names
    if reader.fieldnames is None:
        raise ValueError("CSV file appears to be empty or has no headers.")

    col_map = _map_csv_columns(reader.fieldnames)
    if "question" not in col_map:
        raise ValueError(
            f"CSV must have a question/text column. Found columns: {reader.fieldnames}"
        )

    questions = []
    for i, row in enumerate(reader):
        q_text = row.get(col_map["question"], "").strip()
        if not q_text:
            continue

        q_num = i + 1
        if "number" in col_map:
            try:
                q_num = int(row.get(col_map["number"], i + 1))
            except (ValueError, TypeError):
                q_num = i + 1

        q_year = year
        if "year" in col_map:
            try:
                q_year = int(row.get(col_map["year"], year))
            except (ValueError, TypeError):
                q_year = year

        q_phase = row.get(col_map.get("phase", ""), phase) or phase
        section_hint = row.get(col_map.get("section", ""), "") or ""

        questions.append(Question(
            text=q_text,
            question_number=q_num,
            year=q_year,
            phase=q_phase,
            exam_type=exam_type,
            section_hint=section_hint,
        ))

    return questions


def _map_csv_columns(fieldnames: list[str]) -> dict[str, str]:
    """Map CSV column names to standard field names."""
    mapping = {}
    field_lower = {f.strip().lower(): f for f in fieldnames}

    # Question text column
    for key in ["question", "text", "q", "question_text", "ques", "question text"]:
        if key in field_lower:
            mapping["question"] = field_lower[key]
            break

    # Question number
    for key in ["number", "q_no", "question_number", "qno", "sl", "sr", "sno", "s.no", "q.no"]:
        if key in field_lower:
            mapping["number"] = field_lower[key]
            break

    # Section
    for key in ["section", "subject", "sec"]:
        if key in field_lower:
            mapping["section"] = field_lower[key]
            break

    # Topic
    for key in ["topic", "chapter", "type"]:
        if key in field_lower:
            mapping["topic"] = field_lower[key]
            break

    # Sub-topic
    for key in ["sub_topic", "subtopic", "sub topic", "sub-topic"]:
        if key in field_lower:
            mapping["sub_topic"] = field_lower[key]
            break

    # Year
    for key in ["year", "yr"]:
        if key in field_lower:
            mapping["year"] = field_lower[key]
            break

    # Phase
    for key in ["phase", "paper", "stage"]:
        if key in field_lower:
            mapping["phase"] = field_lower[key]
            break

    return mapping
