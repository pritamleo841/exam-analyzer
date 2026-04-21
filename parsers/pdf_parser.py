"""
PDF Parser - Extracts questions from exam paper PDFs.
Uses pdfplumber as primary, PyMuPDF as fallback, OCR and AI Vision for scanned PDFs.
"""
import re
import io
from config import Question


def extract_text_from_pdf(
    file_bytes: bytes,
    ai_vision_caller=None,
) -> str:
    """Extract text from PDF bytes.

    Fallback chain: pdfplumber → PyMuPDF → OCR (pytesseract) → AI Vision.

    Args:
        file_bytes: Raw PDF bytes.
        ai_vision_caller: Optional callable(image_bytes_list) -> str for AI-based
            extraction of scanned pages. Accepts a list of JPEG byte strings.
    """
    text = _try_pdfplumber(file_bytes)
    if not text or len(text.strip()) < 50:
        text = _try_pymupdf(file_bytes)
    if not text or len(text.strip()) < 50:
        text = _try_ocr(file_bytes)
    if not text or len(text.strip()) < 50:
        if ai_vision_caller is not None:
            text = _try_ai_vision(file_bytes, ai_vision_caller)
    if not text or len(text.strip()) < 50:
        raise ValueError(
            "Could not extract text from PDF. "
            "The file may be a low-quality scan. Try:\n"
            "1. Install Tesseract OCR (https://github.com/tesseract-ocr/tesseract)\n"
            "2. Or enable AI Vision (OpenAI/Gemini) in sidebar settings.\n"
            "3. Or paste the questions as text using the text input option."
        )
    return text


def _try_pdfplumber(file_bytes: bytes) -> str:
    """Extract text using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception:
        return ""


def _try_pymupdf(file_bytes: bytes) -> str:
    """Extract text using PyMuPDF (fitz)."""
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts)
    except Exception:
        return ""


def _try_ocr(file_bytes: bytes) -> str:
    """Extract text from scanned/image-based PDFs using Tesseract OCR."""
    try:
        from pdf2image import convert_from_bytes
        import pytesseract
        from PIL import ImageFilter, ImageOps

        images = convert_from_bytes(file_bytes, dpi=300)
        text_parts = []
        for img in images:
            # Pre-process for better OCR: grayscale → sharpen → binarize
            img = ImageOps.grayscale(img)
            img = img.filter(ImageFilter.SHARPEN)
            img = img.point(lambda x: 0 if x < 140 else 255, "1")
            page_text = pytesseract.image_to_string(img, lang="eng")
            if page_text and page_text.strip():
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except ImportError:
        return ""
    except Exception:
        return ""


def _try_ai_vision(file_bytes: bytes, ai_caller) -> str:
    """Extract text from scanned PDFs using AI Vision (GPT-4o / Gemini).

    Args:
        file_bytes: Raw PDF bytes.
        ai_caller: Callable that accepts a list of JPEG byte buffers and returns
            the extracted text as a single string.
    """
    try:
        from pdf2image import convert_from_bytes

        images = convert_from_bytes(file_bytes, dpi=200)
        jpeg_buffers = []
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            jpeg_buffers.append(buf.getvalue())

        return ai_caller(jpeg_buffers)
    except ImportError:
        return ""
    except Exception:
        return ""


def split_into_questions(
    text: str,
    year: int,
    phase: str,
    exam_type: str,
) -> list[Question]:
    """
    Split extracted text into individual Question objects.
    Handles multiple numbering formats:
    - Q1. / Q.1 / Q 1 / Q1)
    - 1. / 1) / (1)
    - Question 1: / Question 1.
    """
    # Normalize whitespace
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    # Try to detect section headers
    section_markers = _detect_section_headers(text)

    # Split by question number patterns
    # Order matters — try more specific patterns first
    patterns = [
        # Q1. or Q.1 or Q 1. or Q1) or Q.1)
        r'(?:^|\n)\s*Q\.?\s*(\d+)\s*[.):]',
        # Question 1. or Question 1:
        r'(?:^|\n)\s*Question\s+(\d+)\s*[.):]\s',
        # 1. or 1) — only at line start with a space after
        r'(?:^|\n)\s*(\d+)\s*[.)]\s+(?=[A-Z])',
        # (1) — parenthesized
        r'(?:^|\n)\s*\((\d+)\)\s+',
    ]

    best_splits = []
    for pattern in patterns:
        splits = list(re.finditer(pattern, text, re.MULTILINE))
        if len(splits) >= 5:  # Need at least 5 questions to consider valid
            if len(splits) > len(best_splits):
                best_splits = splits
                best_pattern = pattern
            break  # Use first pattern that works well

    if not best_splits:
        # Fallback: try splitting by double newlines
        return _fallback_split(text, year, phase, exam_type)

    questions = []
    for i, match in enumerate(best_splits):
        q_num = int(match.group(1))
        start = match.end()
        end = best_splits[i + 1].start() if i + 1 < len(best_splits) else len(text)
        q_text = text[start:end].strip()

        # Clean up the question text
        q_text = _clean_question_text(q_text)

        if len(q_text) < 10:  # Skip very short fragments
            continue

        # Determine section from position
        section_hint = _get_section_for_position(match.start(), section_markers)

        questions.append(Question(
            text=q_text,
            question_number=q_num,
            year=year,
            phase=phase,
            exam_type=exam_type,
            section_hint=section_hint,
        ))

    # Group DI / passage-based questions
    questions = _group_data_set_questions(questions)

    return questions


def _detect_section_headers(text: str) -> list[tuple[int, str]]:
    """Detect section header positions in the text."""
    section_keywords = [
        "Quantitative Aptitude", "Quant", "QA",
        "Reasoning Ability", "Reasoning", "Logical Reasoning",
        "English Language", "English",
        "General Awareness", "General Knowledge", "GA", "GK",
        "Computer Knowledge", "Computer Aptitude",
        "Data Analysis", "Data Interpretation",
        "Economic & Social Issues", "ESI",
        "Finance & Management", "FM",
        "Agriculture", "ARD",
    ]
    markers = []
    for kw in section_keywords:
        for m in re.finditer(
            rf'(?:^|\n)\s*(?:Section\s*[-:.]?\s*)?{re.escape(kw)}\s*(?:[-:.]\s*)?(?:\n|$)',
            text,
            re.IGNORECASE | re.MULTILINE,
        ):
            markers.append((m.start(), kw))

    markers.sort(key=lambda x: x[0])
    return markers


def _get_section_for_position(pos: int, markers: list[tuple[int, str]]) -> str:
    """Get the section name for a given text position based on section markers."""
    section = ""
    for marker_pos, marker_name in markers:
        if marker_pos <= pos:
            section = marker_name
        else:
            break
    return section


def _clean_question_text(text: str) -> str:
    """Clean up extracted question text."""
    # Remove common artifacts
    text = re.sub(r'\s*\n\s*', '\n', text)
    # Remove option labels at line starts if they look like answer choices
    # but keep them as part of the question (they help categorization)
    text = text.strip()
    return text


def _group_data_set_questions(questions: list[Question]) -> list[Question]:
    """
    Detect and group questions that share a data set (DI, RC passages, etc.).
    Questions that reference the same data set get a shared data_set_id.
    """
    # Heuristic: if a question contains a large data block (table, chart description)
    # and the next few questions are short, they likely share the data set
    i = 0
    data_set_counter = 0
    while i < len(questions):
        q = questions[i]
        # Check if this question contains a data description (long text before actual question)
        if len(q.text) > 300 or _has_data_indicators(q.text):
            data_set_counter += 1
            ds_id = f"DS_{data_set_counter}"
            q.data_set_id = ds_id

            # Check next questions — if they're short, they likely share this data set
            j = i + 1
            while j < len(questions) and j <= i + 7:  # Max 7 questions per set
                next_q = questions[j]
                if len(next_q.text) < 200 and not _has_data_indicators(next_q.text):
                    next_q.data_set_id = ds_id
                    j += 1
                else:
                    break
            i = j
        else:
            i += 1

    return questions


def _has_data_indicators(text: str) -> bool:
    """Check if text likely contains data for DI/passage questions."""
    indicators = [
        r'(?:following|given)\s+(?:table|chart|graph|data|passage|information)',
        r'(?:study|read|refer)\s+(?:the|to)\s+(?:following|given|below)',
        r'directions?\s*[:.]',
        r'\b(?:year|month|quarter)\b.*\b(?:year|month|quarter)\b',  # Table-like data
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in indicators)


def _fallback_split(
    text: str,
    year: int,
    phase: str,
    exam_type: str,
) -> list[Question]:
    """Fallback: split by double newlines when no numbering pattern is found."""
    paragraphs = re.split(r'\n\s*\n', text)
    questions = []
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if len(para) < 20:
            continue
        questions.append(Question(
            text=para,
            question_number=i + 1,
            year=year,
            phase=phase,
            exam_type=exam_type,
        ))
    return questions
