"""
Question Generator — generates exam-level, solvable questions for mock tests
using calibrated AI prompts with PYQ pattern matching.
"""
import json
from config import CategorizedQuestion, GeneratedQuestion
from categorizers.prompts import get_calibrated_question_prompt


def collect_pyq_examples(
    categorized: list[CategorizedQuestion],
    topic: str,
    section: str,
    max_examples: int = 3,
) -> list[str]:
    """Collect actual PYQ texts for a topic to use as few-shot examples."""
    examples = []
    for cq in categorized:
        if cq.topic == topic and cq.section == section:
            examples.append(cq.question.text)
            if len(examples) >= max_examples:
                break
    return examples


def compute_difficulty_distribution(
    categorized: list[CategorizedQuestion],
    topic: str,
) -> dict[str, int]:
    """Compute percentage breakdown of Easy/Medium/Hard for a topic."""
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    total = 0
    for cq in categorized:
        if cq.topic == topic and cq.difficulty.value in counts:
            counts[cq.difficulty.value] += 1
            total += 1
    if total == 0:
        return {"Easy": 10, "Medium": 60, "Hard": 30}
    return {k: round(v * 100 / total) for k, v in counts.items()}


def generate_mock_test_questions(
    predictions: list[dict],
    categorized: list[CategorizedQuestion],
    ai_caller,
    exam_name: str = "RBI Grade B",
    sections_filter: list[str] | None = None,
    total_questions: int = 30,
    difficulty: str = "Medium",
    progress_callback=None,
) -> list[GeneratedQuestion]:
    """Generate a full set of mock-test questions based on predicted distribution.

    Args:
        predictions: From predict_topic_distribution().
        categorized: Historical categorized questions (for PYQ examples).
        ai_caller: callable(prompt) -> str.
        exam_name: Target exam.
        sections_filter: Only generate for these sections (None = all).
        total_questions: Target number of questions.
        difficulty: Overall difficulty level.
        progress_callback: Optional callable(current, total, message).

    Returns:
        List of GeneratedQuestion ready for mock-test export.
    """
    # Filter predictions to requested sections
    preds = predictions
    if sections_filter:
        preds = [p for p in preds if p["section"] in sections_filter]

    if not preds:
        return []

    # Compute how many questions per topic (proportional to predicted_count)
    total_predicted = sum(p["predicted_count"] for p in preds)
    topic_allocations: list[tuple[dict, int]] = []
    allocated = 0

    for p in preds:
        if total_predicted > 0:
            share = p["predicted_count"] / total_predicted
            count = max(1, round(share * total_questions))
        else:
            count = 1
        topic_allocations.append((p, count))
        allocated += count

    # Trim or expand to hit total_questions exactly
    diff = allocated - total_questions
    if diff > 0:
        # Remove from lowest-priority topics
        for i in range(len(topic_allocations) - 1, -1, -1):
            if diff <= 0:
                break
            p, c = topic_allocations[i]
            reduce = min(c - 1, diff)
            if reduce > 0:
                topic_allocations[i] = (p, c - reduce)
                diff -= reduce
    elif diff < 0:
        # Add to highest-priority topics
        for i in range(len(topic_allocations)):
            if diff >= 0:
                break
            p, c = topic_allocations[i]
            topic_allocations[i] = (p, c + 1)
            diff += 1

    # Generate questions for each topic
    all_questions: list[GeneratedQuestion] = []
    done = 0
    total_topics = len(topic_allocations)

    for idx, (pred, count) in enumerate(topic_allocations):
        if count <= 0:
            continue

        section = pred["section"]
        topic = pred["topic"]

        if progress_callback:
            progress_callback(idx, total_topics, f"Generating {topic} ({count} Qs)...")

        # Gather PYQ examples and difficulty distribution
        examples = collect_pyq_examples(categorized, topic, section)
        diff_dist = compute_difficulty_distribution(categorized, topic)

        # Build pattern info for set-based topics
        pattern_info = ""
        if topic in ("Data Interpretation", "Seating Arrangement", "Puzzles"):
            set_size = 5
            num_sets = max(1, count // set_size)
            remainder = count - num_sets * set_size
            pattern_info = (
                f"\nGenerate {num_sets} complete set(s) of {set_size} questions each"
                f"{f' plus {remainder} standalone questions' if remainder > 0 else ''}. "
                f"Each set should share a common data/puzzle context.\n"
            )
            count = num_sets * set_size + remainder

        prompt = get_calibrated_question_prompt(
            topic=topic,
            sub_topic="",
            section=section,
            exam_name=exam_name,
            difficulty=difficulty,
            count=count,
            example_questions=examples,
            difficulty_distribution=diff_dist,
            topic_pattern_info=pattern_info,
        )

        try:
            response = ai_caller(prompt)
            parsed = _parse_generated_json(response)
            for item in parsed:
                gq = GeneratedQuestion(
                    text=item.get("question", ""),
                    options=item.get("options", []),
                    correct_answer=item.get("answer", 0),
                    explanation=item.get("explanation", ""),
                    section=section,
                    topic=topic,
                    sub_topic=item.get("sub_topic", ""),
                    difficulty=item.get("difficulty", difficulty),
                )
                all_questions.append(gq)
        except Exception:
            pass

        done += count

    if progress_callback:
        progress_callback(total_topics, total_topics, "Done!")

    return all_questions


def _parse_generated_json(response: str) -> list[dict]:
    """Parse AI JSON response into list of question dicts."""
    response = response.strip()
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

    valid = []
    for item in items:
        if not isinstance(item, dict):
            continue
        q = item.get("question", "").strip()
        opts = item.get("options", [])
        ans = item.get("answer")

        if not q or len(opts) < 4 or ans is None:
            continue
        if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
            continue

        valid.append(item)

    return valid
