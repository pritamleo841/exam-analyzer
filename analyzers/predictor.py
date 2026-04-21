"""
Question Predictor — predicts likely topics and generates sample questions
for the upcoming exam based on frequency analysis and trend data.
"""
import json
from config import CategorizedQuestion, Difficulty
from analyzers.frequency import build_frequency_matrix
from categorizers.prompts import get_question_generation_prompt, get_calibrated_question_prompt


def predict_topic_distribution(
    categorized: list[CategorizedQuestion],
    total_questions_estimate: int | None = None,
) -> list[dict]:
    """
    Predict the expected topic distribution for the next exam.

    Args:
        categorized: Historical categorized questions
        total_questions_estimate: Expected total questions in next exam (auto-detected if None)

    Returns:
        List of dicts: {section, topic, predicted_count, probability_score, trend}
    """
    freq = build_frequency_matrix(categorized, group_by="topic")
    if freq.empty:
        return []

    # Auto-detect total questions per exam from historical average
    years = set(cq.question.year for cq in categorized)
    if total_questions_estimate is None:
        total_per_year = len(categorized) / max(len(years), 1)
        total_questions_estimate = int(total_per_year)

    # Calculate predicted distribution
    total_prob = freq["ProbabilityScore"].sum()
    predictions = []

    for idx, row in freq.iterrows():
        section, topic = idx
        prob_share = row["ProbabilityScore"] / total_prob if total_prob > 0 else 0
        predicted_count = max(1, round(prob_share * total_questions_estimate))

        # Determine trend
        year_cols = [c for c in freq.columns if c.isdigit()]
        if len(year_cols) >= 3:
            recent = row[year_cols[-2:]].mean()
            overall = row[year_cols].mean()
            if recent > overall * 1.3:
                trend = "Rising ↑"
            elif recent < overall * 0.7:
                trend = "Falling ↓"
            else:
                trend = "Stable →"
        else:
            trend = "Stable →"

        predictions.append({
            "section": section,
            "topic": topic,
            "predicted_count": predicted_count,
            "probability_score": row["ProbabilityScore"],
            "consistency": f"{row['ConsistencyPct']:.0f}%",
            "trend": trend,
            "historical_total": int(row["Total"]),
        })

    # Sort by probability score descending
    predictions.sort(key=lambda x: x["probability_score"], reverse=True)

    # Adjust predicted counts to match total estimate
    current_total = sum(p["predicted_count"] for p in predictions)
    if current_total > 0 and total_questions_estimate > 0:
        scale = total_questions_estimate / current_total
        for p in predictions:
            p["predicted_count"] = max(1, round(p["predicted_count"] * scale))

    return predictions


def generate_sample_questions_ai(
    predictions: list[dict],
    exam_name: str,
    ai_caller,  # callable(prompt) -> response_text
    top_n: int = 10,
    questions_per_topic: int = 2,
    categorized: list[CategorizedQuestion] | None = None,
) -> dict[str, list[str]]:
    """
    Generate sample questions for top predicted topics using AI.

    Args:
        predictions: Topic predictions from predict_topic_distribution
        exam_name: Name of the exam
        ai_caller: Function that takes a prompt string and returns AI response
        top_n: Number of top topics to generate questions for
        questions_per_topic: How many questions per topic
        categorized: Historical questions for PYQ-calibrated prompts (optional)

    Returns:
        Dict mapping "Section > Topic" to list of generated question strings
    """
    generated = {}
    for pred in predictions[:top_n]:
        section = pred["section"]
        topic = pred["topic"]
        key = f"{section} > {topic}"

        # Use calibrated prompt if we have historical data
        if categorized:
            from generators.question_generator import (
                collect_pyq_examples, compute_difficulty_distribution,
            )
            examples = collect_pyq_examples(categorized, topic, section)
            diff_dist = compute_difficulty_distribution(categorized, topic)

            prompt = get_calibrated_question_prompt(
                topic=topic,
                sub_topic="",
                section=section,
                exam_name=exam_name,
                difficulty="Medium",
                count=questions_per_topic,
                example_questions=examples if examples else None,
                difficulty_distribution=diff_dist,
            )
        else:
            prompt = get_question_generation_prompt(
                topic=topic,
                sub_topic="",
                section=section,
                exam_name=exam_name,
                difficulty="Medium",
                count=questions_per_topic,
            )

        try:
            response = ai_caller(prompt)
            generated[key] = _parse_generated_questions(response)
        except Exception as e:
            generated[key] = [f"(Could not generate: {e})"]

    return generated


def generate_sample_questions_template(
    predictions: list[dict],
    top_n: int = 10,
) -> dict[str, list[str]]:
    """
    Generate template-based sample questions for top topics (no AI needed).
    Returns basic question templates based on topic type.
    """
    templates = {
        "Data Interpretation": [
            "Study the following table/chart showing [data about X for Y years]. "
            "What is the ratio of [A] to [B] in [year]?",
            "What is the approximate percentage increase in [metric] from [year1] to [year2]?",
            "What is the average [metric] across all given years?",
        ],
        "Number Series": [
            "What should come in place of the question mark? 2, 5, 11, 23, 47, ?",
            "Find the wrong number in the series: 3, 7, 15, 31, 65, 127",
        ],
        "Simplification & Approximation": [
            "What is the approximate value of: 39.97% of 4999 + 24.98% of 8001 = ?",
            "Simplify: (15 × 12 + 8²) ÷ 4 - 13 = ?",
        ],
        "Quadratic Equations": [
            "I. x² - 11x + 30 = 0    II. y² - 12y + 35 = 0\nFind the relationship between x and y.",
        ],
        "Seating Arrangement": [
            "8 persons A-H sit around a circular table facing the center. "
            "A sits 3rd to the left of B. C sits opposite to A...",
        ],
        "Puzzles": [
            "7 people live on 7 different floors of a building (1-7). "
            "P lives above Q but below R. S lives on an odd floor...",
        ],
        "Syllogism": [
            "Statements: All cats are dogs. Some dogs are birds. No bird is a fish.\n"
            "Conclusions: I. Some cats are birds. II. No fish is a cat.",
        ],
        "Coding-Decoding": [
            "If GARDEN is coded as ICVHGP, how is FLOWER coded in the same language?",
        ],
        "Inequality": [
            "Statements: P ≥ Q > R = S < T ≤ U\n"
            "Conclusions: I. P > S  II. U > R  III. T ≥ Q",
        ],
        "Reading Comprehension": [
            "Read the passage about [economic/social topic] and answer:\n"
            "What is the author's main argument? / What can be inferred from para 2?",
        ],
        "Cloze Test": [
            "Fill in the blanks with appropriate words in the given passage about [topic].",
        ],
        "Blood Relations": [
            "A is the mother of B. C is the father of D. B is the sister of D. "
            "How is A related to C?",
        ],
    }

    generated = {}
    for pred in predictions[:top_n]:
        section = pred["section"]
        topic = pred["topic"]
        key = f"{section} > {topic}"

        topic_templates = templates.get(topic, [
            f"[Sample {topic} question — use AI mode for realistic questions]"
        ])
        generated[key] = topic_templates

    return generated


def _parse_generated_questions(response: str) -> list[str]:
    """Parse AI response into individual question strings."""
    questions = []
    current = []

    for line in response.strip().split("\n"):
        line = line.strip()
        if line.startswith("Q:") or line.startswith("Q ") or (
            line and line[0].isdigit() and "." in line[:3]
        ):
            if current:
                questions.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)

    if current:
        questions.append("\n".join(current))

    return questions if questions else [response]
