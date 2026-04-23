"""
CA Pattern Analyzer — extracts patterns from Previous Year Question papers
for Current Affairs, building a historical model of what categories get
how many questions, at what difficulty, and which specific topics appear.
"""
import json
from pathlib import Path


def load_ca_taxonomy() -> dict:
    """Load the current affairs taxonomy."""
    path = Path(__file__).parent.parent / "data" / "taxonomies" / "ca_taxonomy.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def classify_question_to_ca_category(question_text: str, taxonomy: dict | None = None) -> str:
    """Rule-based classification of a question into a CA category using keywords.

    Returns the best-matching category name, or 'General' if no match.
    """
    if taxonomy is None:
        taxonomy = load_ca_taxonomy()

    text_lower = question_text.lower()
    best_cat = "General"
    best_score = 0

    for section in taxonomy.get("sections", []):
        score = 0
        for kw in section.get("keywords", []):
            if kw.lower() in text_lower:
                score += len(kw)  # longer keyword matches = more specific
        for topic in section.get("topics", []):
            for kw in topic.get("keywords", []):
                if kw.lower() in text_lower:
                    score += len(kw)
        if score > best_score:
            best_score = score
            best_cat = section["name"]

    return best_cat


def analyze_pyq_paper(
    questions: list[dict],
    ai_caller=None,
    taxonomy: dict | None = None,
) -> dict:
    """Analyze a Previous Year Question paper to extract CA patterns.

    Args:
        questions: List of dicts with at minimum {"text": "...", "question_number": N}
                   Can also have "category" if pre-classified.
        ai_caller: Optional AI callable for better classification.
                   If None, uses rule-based keyword matching.
        taxonomy: CA taxonomy dict. Loaded from file if None.

    Returns:
        Pattern dict: {
            total_questions: int,
            categories: {
                "Union Budget": {count, percentage, sample_topics: [...]},
                ...
            }
        }
    """
    if taxonomy is None:
        taxonomy = load_ca_taxonomy()

    category_counts: dict[str, list[str]] = {}

    if ai_caller:
        # Use AI for batch classification
        classified = _ai_classify_batch(questions, ai_caller, taxonomy)
        for q_text, cat in classified:
            category_counts.setdefault(cat, []).append(q_text[:150])
    else:
        # Rule-based fallback
        for q in questions:
            text = q.get("text", "") or q.get("question", "")
            cat = q.get("category") or classify_question_to_ca_category(text, taxonomy)
            category_counts.setdefault(cat, []).append(text[:150])

    total = sum(len(v) for v in category_counts.values())
    categories = {}
    for cat, samples in category_counts.items():
        categories[cat] = {
            "count": len(samples),
            "percentage": round(len(samples) / total * 100, 1) if total else 0,
            "sample_topics": samples[:5],
        }

    return {
        "total_questions": total,
        "categories": categories,
    }


def aggregate_pyq_patterns(patterns: list[dict]) -> dict:
    """Aggregate patterns across multiple years into a unified model.

    Args:
        patterns: List of per-year pattern dicts (from analyze_pyq_paper).

    Returns:
        Aggregated pattern: {
            years_analyzed: int,
            avg_total_questions: float,
            categories: {
                "Union Budget": {
                    avg_count, avg_percentage, consistency (0-100),
                    min_count, max_count, trend
                }, ...
            }
        }
    """
    if not patterns:
        return {"years_analyzed": 0, "categories": {}}

    # Collect all categories across all years
    all_cats: dict[str, list[dict]] = {}
    for p in patterns:
        for cat, info in p.get("categories", {}).items():
            all_cats.setdefault(cat, []).append(info)

    n_years = len(patterns)
    avg_total = sum(p.get("total_questions", 0) for p in patterns) / n_years

    aggregated = {}
    for cat, yearly_data in all_cats.items():
        counts = [d.get("count", 0) for d in yearly_data]
        avg_count = sum(counts) / n_years  # divide by total years, not just years present
        avg_pct = sum(d.get("percentage", 0) for d in yearly_data) / n_years
        consistency = len(yearly_data) / n_years * 100  # % of years this cat appeared

        # Trend: compare last year vs earlier years
        if len(counts) >= 2:
            recent = counts[-1]
            earlier_avg = sum(counts[:-1]) / len(counts[:-1])
            if recent > earlier_avg * 1.3:
                trend = "Rising"
            elif recent < earlier_avg * 0.7:
                trend = "Falling"
            else:
                trend = "Stable"
        else:
            trend = "Stable"

        aggregated[cat] = {
            "avg_count": round(avg_count, 1),
            "avg_percentage": round(avg_pct, 1),
            "consistency": round(consistency),
            "min_count": min(counts),
            "max_count": max(counts),
            "trend": trend,
        }

    return {
        "years_analyzed": n_years,
        "avg_total_questions": round(avg_total, 1),
        "categories": aggregated,
    }


def get_category_weights(aggregated_pattern: dict) -> dict[str, float]:
    """Convert aggregated patterns into category weights (0-100) for prediction.

    Higher weight = more likely to appear in the exam.
    """
    cats = aggregated_pattern.get("categories", {})
    if not cats:
        # Fallback: use taxonomy importance
        return _default_weights_from_taxonomy()

    weights = {}
    for cat, info in cats.items():
        # Weight = 0.5 * normalized_avg_count + 0.3 * consistency + 0.2 * trend_bonus
        max_count = max(c["avg_count"] for c in cats.values()) or 1
        norm_count = info["avg_count"] / max_count * 100
        consistency = info["consistency"]
        trend_bonus = {"Rising": 80, "Stable": 50, "Falling": 20}.get(info["trend"], 50)

        weights[cat] = round(0.5 * norm_count + 0.3 * consistency + 0.2 * trend_bonus, 1)

    return weights


def _default_weights_from_taxonomy() -> dict[str, float]:
    """Generate default weights from taxonomy importance levels when no PYQ data."""
    taxonomy = load_ca_taxonomy()
    importance_map = {
        "Very High": 90,
        "High": 75,
        "Medium-High": 60,
        "Medium": 45,
        "Low-Medium": 30,
        "Low": 15,
    }
    weights = {}
    for section in taxonomy.get("sections", []):
        imp = section.get("importance", "Medium")
        weights[section["name"]] = importance_map.get(imp, 45)
    return weights


def _ai_classify_batch(
    questions: list[dict],
    ai_caller,
    taxonomy: dict,
) -> list[tuple[str, str]]:
    """Use AI to classify questions into CA categories in batches."""
    ca_sections = [s["name"] for s in taxonomy.get("sections", [])]
    sections_list = "\n".join(f"- {s}" for s in ca_sections)

    results = []
    batch_size = 15

    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        q_block = "\n\n".join(
            f"---Q{j+1}---\n{q.get('text', '') or q.get('question', '')}"
            for j, q in enumerate(batch)
        )

        prompt = f"""You are an expert at categorizing current affairs questions for Indian banking exams.

Classify each question below into EXACTLY ONE of these categories:
{sections_list}

QUESTIONS:
{q_block}

Respond with a JSON array. Each element: {{"index": 1, "category": "exact category name from list above"}}
Respond with ONLY the JSON array."""

        try:
            response = ai_caller(prompt)
            parsed = _parse_classify_response(response)
            for item in parsed:
                idx = item.get("index", 0) - 1
                cat = item.get("category", "General")
                if 0 <= idx < len(batch):
                    text = batch[idx].get("text", "") or batch[idx].get("question", "")
                    # Validate category exists
                    if cat not in ca_sections:
                        cat = classify_question_to_ca_category(text, taxonomy)
                    results.append((text, cat))
        except Exception:
            # Fallback to rule-based
            for q in batch:
                text = q.get("text", "") or q.get("question", "")
                cat = classify_question_to_ca_category(text, taxonomy)
                results.append((text, cat))

    return results


def _parse_classify_response(response: str) -> list[dict]:
    """Parse AI classification response."""
    response = response.strip()
    if response.startswith("```"):
        response = response.split("\n", 1)[1] if "\n" in response else response
        if response.endswith("```"):
            response = response[:-3]
        if response.startswith("json"):
            response = response[4:]
        response = response.strip()
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return []
