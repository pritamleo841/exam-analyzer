"""
Current Affairs Question Generator — parses monthly CA PDFs and generates
exam-level MCQs using AI, then merges them into the existing quiz system.

Enhanced with fact extraction + importance tagging for predictive analysis.
"""
import json
import re
from parsers.pdf_parser import extract_text_from_pdf
from categorizers.prompts import get_ca_question_generation_prompt, get_ca_fact_extraction_prompt


# Maximum characters of CA text to send per AI call (to stay within token limits)
_MAX_CHUNK = 10000


def extract_ca_text(file_bytes: bytes, ai_vision_caller=None) -> str:
    """Extract text from a current affairs PDF (handles text & scanned PDFs)."""
    return extract_text_from_pdf(file_bytes, ai_vision_caller=ai_vision_caller)


def generate_ca_questions(
    ca_text: str,
    ai_caller,
    exam_name: str = "RBI Grade B",
    category: str = "All",
    questions_per_chunk: int = 10,
    difficulty: str = "Medium",
) -> list[dict]:
    """Generate MCQs from current affairs text using AI.

    Args:
        ca_text: Full extracted text from the CA PDF.
        ai_caller: Callable(prompt: str) -> str that calls the AI provider.
        exam_name: Target exam name.
        category: CA category to focus on, or "All".
        questions_per_chunk: Number of questions to generate per text chunk.
        difficulty: Easy / Medium / Hard.

    Returns:
        List of MCQ dicts: {question, options, answer, explanation, category}
    """
    chunks = _split_text_into_chunks(ca_text, _MAX_CHUNK)
    all_questions: list[dict] = []

    for chunk in chunks:
        if len(chunk.strip()) < 100:
            continue
        prompt = get_ca_question_generation_prompt(
            ca_text=chunk,
            exam_name=exam_name,
            category=category,
            count=questions_per_chunk,
            difficulty=difficulty,
        )
        try:
            response = ai_caller(prompt)
            parsed = _parse_ca_response(response)
            all_questions.extend(parsed)
        except Exception:
            continue

    # Deduplicate by question text (case-insensitive)
    seen = set()
    unique: list[dict] = []
    for q in all_questions:
        key = q["question"].strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    return unique


def generate_ca_questions_from_pdfs(
    pdf_files: list[tuple[str, bytes]],
    ai_caller,
    exam_name: str = "RBI Grade B",
    category: str = "All",
    questions_per_chunk: int = 10,
    difficulty: str = "Medium",
    ai_vision_caller=None,
    progress_callback=None,
) -> list[dict]:
    """Process multiple CA PDF files and generate MCQs from all of them.

    Args:
        pdf_files: List of (filename, file_bytes) tuples.
        ai_caller: Text-prompt AI callable.
        exam_name: Target exam.
        category: CA category filter.
        questions_per_chunk: Questions per AI call.
        difficulty: Difficulty level.
        ai_vision_caller: Optional vision AI callable for scanned PDFs.
        progress_callback: Optional callable(current, total, message) for UI progress.

    Returns:
        Merged, deduplicated list of MCQ dicts.
    """
    all_questions: list[dict] = []
    total = len(pdf_files)

    for idx, (filename, file_bytes) in enumerate(pdf_files):
        if progress_callback:
            progress_callback(idx, total, f"Extracting text from {filename}...")

        try:
            ca_text = extract_ca_text(file_bytes, ai_vision_caller=ai_vision_caller)
        except ValueError:
            continue

        if progress_callback:
            progress_callback(idx, total, f"Generating questions from {filename}...")

        qs = generate_ca_questions(
            ca_text=ca_text,
            ai_caller=ai_caller,
            exam_name=exam_name,
            category=category,
            questions_per_chunk=questions_per_chunk,
            difficulty=difficulty,
        )
        # Tag each question with the source file
        for q in qs:
            q["source"] = filename
        all_questions.extend(qs)

    if progress_callback:
        progress_callback(total, total, "Done!")

    # Final deduplication across all files
    seen = set()
    unique: list[dict] = []
    for q in all_questions:
        key = q["question"].strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    return unique


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _split_text_into_chunks(text: str, max_chars: int) -> list[str]:
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current_len + len(para) + 2 > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _parse_ca_response(response: str) -> list[dict]:
    """Parse AI JSON response into a list of MCQ dicts."""
    response = response.strip()
    # Strip markdown code fences if present
    if response.startswith("```"):
        response = response.split("\n", 1)[1] if "\n" in response else response
        if response.endswith("```"):
            response = response[:-3]
        if response.startswith("json"):
            response = response[4:]
        response = response.strip()

    try:
        items = json.loads(response)
    except json.JSONDecodeError:
        return []

    if not isinstance(items, list):
        return []

    valid: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        question = item.get("question", "").strip()
        options = item.get("options", [])
        answer = item.get("answer")
        explanation = item.get("explanation", "")
        category = item.get("category", "General")

        # Validate structure
        if not question or len(options) < 4 or answer is None:
            continue
        if not isinstance(answer, int) or answer < 0 or answer >= len(options):
            continue

        valid.append({
            "question": question,
            "options": [str(o) for o in options[:4]],
            "answer": int(answer),
            "explanation": str(explanation),
            "category": str(category),
        })

    return valid


# ═══════════════════════════════════════════════════════════════════════════
# ENHANCED: Fact extraction + importance tagging for predictive analysis
# ═══════════════════════════════════════════════════════════════════════════

def extract_facts_and_questions(
    ca_text: str,
    ai_caller,
    exam_name: str = "RBI Grade B",
    month: str = "",
) -> dict:
    """Extract structured facts + MCQs from CA text using the enhanced prompt.

    Returns:
        {
            "facts": [{fact, category, importance, why_it_matters}, ...],
            "questions": [{question, options, answer, explanation, category, importance}, ...]
        }
    """
    chunks = _split_text_smart(ca_text, _MAX_CHUNK)
    all_facts = []
    all_questions = []

    for chunk in chunks:
        if len(chunk.strip()) < 100:
            continue
        prompt = get_ca_fact_extraction_prompt(
            ca_text=chunk,
            exam_name=exam_name,
            month=month,
        )
        try:
            response = ai_caller(prompt)
            parsed = _parse_fact_extraction_response(response)
            all_facts.extend(parsed.get("facts", []))
            all_questions.extend(parsed.get("questions", []))
        except Exception:
            continue

    # Deduplicate facts by content similarity
    unique_facts = _deduplicate_facts(all_facts)
    # Deduplicate questions
    seen_q = set()
    unique_qs = []
    for q in all_questions:
        key = q.get("question", "").strip().lower()
        if key and key not in seen_q:
            seen_q.add(key)
            unique_qs.append(q)

    return {"facts": unique_facts, "questions": unique_qs}


def extract_facts_from_pdfs(
    pdf_files: list[tuple[str, bytes]],
    ai_caller,
    month_map: dict[str, str] | None = None,
    exam_name: str = "RBI Grade B",
    ai_vision_caller=None,
    progress_callback=None,
) -> dict:
    """Process multiple CA PDFs and extract facts + questions from all.

    Args:
        pdf_files: List of (filename, file_bytes).
        ai_caller: AI callable(prompt) -> str.
        month_map: Optional {filename: month_name} mapping.
        exam_name: Target exam.
        ai_vision_caller: Optional vision AI for scanned PDFs.
        progress_callback: Optional callable(current, total, message)

    Returns:
        {
            "facts": [...all facts across PDFs...],
            "questions": [...all MCQs across PDFs...],
            "by_file": {filename: {facts, questions}}
        }
    """
    month_map = month_map or {}
    all_facts = []
    all_questions = []
    by_file = {}
    total = len(pdf_files)

    for idx, (filename, file_bytes) in enumerate(pdf_files):
        if progress_callback:
            progress_callback(idx, total, f"Extracting text from {filename}...")

        try:
            ca_text = extract_ca_text(file_bytes, ai_vision_caller=ai_vision_caller)
        except (ValueError, Exception):
            if progress_callback:
                progress_callback(idx, total, f"Failed to extract: {filename}")
            continue

        if progress_callback:
            progress_callback(idx, total, f"AI analyzing {filename}...")

        month = month_map.get(filename, "")
        result = extract_facts_and_questions(
            ca_text=ca_text,
            ai_caller=ai_caller,
            exam_name=exam_name,
            month=month,
        )

        # Tag source
        for f in result["facts"]:
            f["source"] = filename
            f["month"] = month
        for q in result["questions"]:
            q["source"] = filename
            q["month"] = month

        by_file[filename] = result
        all_facts.extend(result["facts"])
        all_questions.extend(result["questions"])

    if progress_callback:
        progress_callback(total, total, "Done!")

    # Final deduplication
    unique_facts = _deduplicate_facts(all_facts)
    seen_q = set()
    unique_qs = []
    for q in all_questions:
        key = q.get("question", "").strip().lower()
        if key and key not in seen_q:
            seen_q.add(key)
            unique_qs.append(q)

    return {
        "facts": unique_facts,
        "questions": unique_qs,
        "by_file": by_file,
    }


def _split_text_smart(text: str, max_chars: int) -> list[str]:
    """Split text at topic boundaries (headings, bold markers) when possible,
    falling back to paragraph splits.
    """
    # Try to detect topic headings (common in CA compilations)
    heading_pattern = re.compile(
        r'\n(?=[A-Z][A-Z\s&:–-]{5,}\n)|'           # ALL CAPS lines
        r'\n(?=\d+\.\s+[A-Z])|'                      # Numbered headings "1. Topic"
        r'\n(?=#+\s)|'                                # Markdown headings
        r'\n(?=\*\*[A-Z])',                           # Bold headings **Topic
        re.MULTILINE,
    )

    # Split by headings first
    parts = heading_pattern.split(text)
    if len(parts) <= 1:
        # No headings found — fall back to paragraph-based split
        return _split_text_into_chunks(text, max_chars)

    # Merge small parts and split large ones
    chunks = []
    current = []
    current_len = 0

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if current_len + len(part) > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [part]
            current_len = len(part)
        else:
            current.append(part)
            current_len += len(part) + 2

    if current:
        chunks.append("\n\n".join(current))

    # Split any oversized chunks further
    final = []
    for chunk in chunks:
        if len(chunk) > max_chars * 1.5:
            final.extend(_split_text_into_chunks(chunk, max_chars))
        else:
            final.append(chunk)

    return final


def _parse_fact_extraction_response(response: str) -> dict:
    """Parse AI response from the fact extraction prompt."""
    response = response.strip()
    # Strip markdown code fences
    if response.startswith("```"):
        response = response.split("\n", 1)[1] if "\n" in response else response
        if response.endswith("```"):
            response = response[:-3]
        if response.startswith("json"):
            response = response[4:]
        response = response.strip()

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return {"facts": [], "questions": []}

    if not isinstance(data, dict):
        return {"facts": [], "questions": []}

    # Validate facts
    valid_facts = []
    for f in data.get("facts", []):
        if isinstance(f, dict) and f.get("fact"):
            valid_facts.append({
                "fact": str(f["fact"]),
                "category": str(f.get("category", "General")),
                "importance": str(f.get("importance", "Medium")),
                "why_it_matters": str(f.get("why_it_matters", "")),
            })

    # Validate questions
    valid_qs = _parse_ca_response(
        json.dumps(data.get("questions", []))
    )
    # Carry over importance tag
    raw_qs = data.get("questions", [])
    for i, vq in enumerate(valid_qs):
        if i < len(raw_qs):
            vq["importance"] = str(raw_qs[i].get("importance", "Medium"))

    return {"facts": valid_facts, "questions": valid_qs}


def _deduplicate_facts(facts: list[dict]) -> list[dict]:
    """Deduplicate facts by checking for high content overlap."""
    if not facts:
        return []
    unique = []
    seen_keys = set()
    for f in facts:
        # Create a normalized key: first 80 chars, lowered, stripped of spaces
        key = re.sub(r'\s+', ' ', f.get("fact", "").lower().strip())[:80]
        if key and key not in seen_keys:
            seen_keys.add(key)
            unique.append(f)
    return unique
