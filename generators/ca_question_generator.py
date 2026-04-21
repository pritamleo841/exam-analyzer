"""
Current Affairs Question Generator — parses monthly CA PDFs and generates
exam-level MCQs using AI, then merges them into the existing quiz system.
"""
import json
from parsers.pdf_parser import extract_text_from_pdf
from categorizers.prompts import get_ca_question_generation_prompt


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
