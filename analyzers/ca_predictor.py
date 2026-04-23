"""
CA Predictor — the core predictive engine that combines:
1. Extracted CA facts from monthly PDFs (Jan-Jun)
2. PYQ CA patterns (historical frequency per category)
3. AI-assessed importance scores

To produce a probability-ranked list of facts & questions per category,
optimized for RBI Grade B Phase 1 General Awareness preparation.
"""
import json
from datetime import datetime
from config import CA_SECTIONS, PREDICTION_WEIGHTS, EXPECTED_CA_QUESTIONS_PHASE1
from analyzers.ca_pattern_analyzer import (
    load_ca_taxonomy,
    aggregate_pyq_patterns,
    get_category_weights,
    _default_weights_from_taxonomy,
)


def run_predictive_analysis(
    all_facts: list[dict],
    all_questions: list[dict],
    pyq_patterns: list[dict] | None = None,
    ai_caller=None,
    target_questions: int = EXPECTED_CA_QUESTIONS_PHASE1,
) -> dict:
    """Run the full predictive analysis pipeline.

    Args:
        all_facts: Extracted facts from CA PDFs [{fact, category, importance, month, ...}]
        all_questions: Generated MCQs from CA PDFs [{question, options, answer, category, importance, ...}]
        pyq_patterns: Previous year patterns (from ca_pattern_analyzer.analyze_pyq_paper)
        ai_caller: Optional AI callable for enhanced ranking
        target_questions: Expected number of CA questions in the exam

    Returns:
        {
            "sections": [
                {
                    "name": "Union Budget",
                    "weight": 85.0,
                    "predicted_questions": 4,
                    "facts": [{fact, importance, probability_score, ...}],
                    "questions": [{question, options, answer, probability_score, ...}],
                    "study_priority": "Critical",
                    "coverage_status": "Well Covered" | "Needs Attention" | "Gap"
                }, ...
            ],
            "top_50_facts": [...],
            "total_facts": int,
            "total_questions": int,
            "readiness_score": float,
            "study_time_allocation": {...},
            "metadata": {...}
        }
    """
    taxonomy = load_ca_taxonomy()

    # Step 1: Get category weights from PYQ patterns (or defaults)
    if pyq_patterns:
        aggregated = aggregate_pyq_patterns(pyq_patterns)
        category_weights = get_category_weights(aggregated)
    else:
        aggregated = None
        category_weights = _default_weights_from_taxonomy()

    # Step 2: Score each fact
    scored_facts = _score_facts(all_facts, category_weights, taxonomy)

    # Step 3: Score each question
    scored_questions = _score_questions(all_questions, category_weights, scored_facts)

    # Step 4: Build sections with predictions
    sections = _build_sections(
        scored_facts, scored_questions, category_weights,
        target_questions, taxonomy, aggregated,
    )

    # Step 5: Extract top 50 must-study facts
    top_50 = sorted(scored_facts, key=lambda f: f.get("probability_score", 0), reverse=True)[:50]

    # Step 6: Calculate readiness metrics
    readiness = _calculate_readiness(sections, scored_facts)

    # Step 7: Study time allocation
    time_alloc = _calculate_study_time(sections)

    return {
        "sections": sections,
        "top_50_facts": top_50,
        "total_facts": len(scored_facts),
        "total_questions": len(scored_questions),
        "readiness_score": readiness,
        "study_time_allocation": time_alloc,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "target_questions": target_questions,
            "pyq_years_used": len(pyq_patterns) if pyq_patterns else 0,
            "months_covered": list(set(f.get("month", "") for f in all_facts if f.get("month"))),
        },
    }


def _score_facts(
    facts: list[dict],
    category_weights: dict[str, float],
    taxonomy: dict,
) -> list[dict]:
    """Assign probability_score (0-100) to each fact."""
    # Month recency scoring (Jan=1 -> lowest, Jun=6 -> highest for a Jun exam)
    month_scores = {
        "January": 40, "February": 50, "March": 60, "April": 70,
        "May": 80, "June": 90,
        "July": 35, "August": 30, "September": 25, "October": 20,
        "November": 15, "December": 10,
    }

    importance_scores = {"High": 90, "Medium": 55, "Low": 20}

    w = PREDICTION_WEIGHTS
    scored = []

    for fact in facts:
        cat = fact.get("category", "General")
        imp = fact.get("importance", "Medium")
        month = fact.get("month", "")

        # Component scores
        cat_weight = category_weights.get(cat, 30)  # PYQ frequency component
        imp_score = importance_scores.get(imp, 55)   # AI importance component
        recency = month_scores.get(month, 50)         # Recency component

        # Weighted combination
        prob = (
            w["pyq_frequency"] * cat_weight +
            w["ai_importance"] * imp_score +
            w["recency"] * recency
        )
        prob = min(100, max(0, round(prob, 1)))

        scored.append({
            **fact,
            "probability_score": prob,
            "priority": _priority_label(prob),
        })

    scored.sort(key=lambda f: f["probability_score"], reverse=True)
    return scored


def _score_questions(
    questions: list[dict],
    category_weights: dict[str, float],
    scored_facts: list[dict],
) -> list[dict]:
    """Score questions based on their associated fact scores."""
    # Build a lookup of average probability by category
    cat_avg = {}
    for f in scored_facts:
        cat = f.get("category", "General")
        cat_avg.setdefault(cat, []).append(f.get("probability_score", 50))

    for cat in cat_avg:
        vals = cat_avg[cat]
        cat_avg[cat] = sum(vals) / len(vals)

    scored = []
    for q in questions:
        cat = q.get("category", "General")
        imp = q.get("importance", "Medium")
        importance_bonus = {"High": 15, "Medium": 0, "Low": -15}.get(imp, 0)

        base_score = cat_avg.get(cat, 50)
        prob = min(100, max(0, round(base_score + importance_bonus, 1)))

        scored.append({
            **q,
            "probability_score": prob,
            "priority": _priority_label(prob),
        })

    scored.sort(key=lambda q: q["probability_score"], reverse=True)
    return scored


def _build_sections(
    scored_facts: list[dict],
    scored_questions: list[dict],
    category_weights: dict[str, float],
    target_questions: int,
    taxonomy: dict,
    aggregated_pattern: dict | None,
) -> list[dict]:
    """Build section-wise breakdown with predictions."""
    # Group facts and questions by category
    fact_groups: dict[str, list] = {}
    q_groups: dict[str, list] = {}

    for f in scored_facts:
        fact_groups.setdefault(f.get("category", "General"), []).append(f)
    for q in scored_questions:
        q_groups.setdefault(q.get("category", "General"), []).append(q)

    # Predict question distribution across categories
    total_weight = sum(category_weights.values()) or 1
    predicted_dist = {}
    for cat, w in category_weights.items():
        predicted_dist[cat] = max(0, round(w / total_weight * target_questions))

    # Ensure total matches target
    total_predicted = sum(predicted_dist.values())
    if total_predicted > 0:
        diff = target_questions - total_predicted
        # Add/subtract from top categories
        sorted_cats = sorted(predicted_dist.keys(), key=lambda c: category_weights.get(c, 0), reverse=True)
        for i, cat in enumerate(sorted_cats):
            if diff == 0:
                break
            if diff > 0:
                predicted_dist[cat] += 1
                diff -= 1
            elif diff < 0 and predicted_dist[cat] > 0:
                predicted_dist[cat] -= 1
                diff += 1

    # Get expected ranges from taxonomy
    tax_sections = {s["name"]: s for s in taxonomy.get("sections", [])}

    sections = []
    # Process all categories from taxonomy (ordered by weight)
    all_cats = sorted(
        set(list(category_weights.keys()) + list(fact_groups.keys()) + list(q_groups.keys())),
        key=lambda c: category_weights.get(c, 0),
        reverse=True,
    )

    for cat in all_cats:
        facts = fact_groups.get(cat, [])
        questions = q_groups.get(cat, [])
        weight = category_weights.get(cat, 0)
        predicted = predicted_dist.get(cat, 0)
        tax_info = tax_sections.get(cat, {})

        # Sort within section by probability
        facts.sort(key=lambda f: f.get("probability_score", 0), reverse=True)
        questions.sort(key=lambda q: q.get("probability_score", 0), reverse=True)

        # Coverage status
        if len(facts) >= 5 and len(questions) >= predicted:
            coverage = "Well Covered"
        elif len(facts) >= 2:
            coverage = "Needs More Questions"
        elif predicted > 0:
            coverage = "Gap - Need Material"
        else:
            coverage = "Low Priority"

        # Study priority
        if weight >= 70:
            priority = "Critical"
        elif weight >= 50:
            priority = "High"
        elif weight >= 30:
            priority = "Medium"
        else:
            priority = "Low"

        # Historical info from aggregated pattern
        hist_info = {}
        if aggregated_pattern:
            hist_cats = aggregated_pattern.get("categories", {})
            if cat in hist_cats:
                hist_info = hist_cats[cat]

        sections.append({
            "name": cat,
            "weight": weight,
            "predicted_questions": predicted,
            "expected_range": tax_info.get("expected_questions", "0-1"),
            "importance": tax_info.get("importance", "Medium"),
            "facts": facts,
            "questions": questions,
            "fact_count": len(facts),
            "question_count": len(questions),
            "study_priority": priority,
            "coverage_status": coverage,
            "historical": hist_info,
        })

    return sections


def _calculate_readiness(sections: list[dict], all_facts: list[dict]) -> float:
    """Calculate overall readiness score (0-100).

    Based on: how well the high-priority categories are covered.
    """
    if not sections:
        return 0

    total_weight = sum(s["weight"] for s in sections) or 1
    covered_weight = 0

    for s in sections:
        if s["coverage_status"] in ("Well Covered", "Needs More Questions"):
            covered_weight += s["weight"]
        elif s["fact_count"] > 0:
            covered_weight += s["weight"] * 0.3  # partial credit

    return round(covered_weight / total_weight * 100, 1)


def _calculate_study_time(sections: list[dict]) -> dict:
    """Suggest study time allocation (hours) per section based on weight and coverage."""
    total_hours = 80  # ~2 hours/day for 40 days
    total_weight = sum(s["weight"] for s in sections if s["predicted_questions"] > 0) or 1

    allocation = {}
    for s in sections:
        if s["predicted_questions"] > 0 or s["weight"] >= 30:
            hours = round(s["weight"] / total_weight * total_hours, 1)
            # Boost sections with gaps
            if s["coverage_status"] in ("Gap - Need Material",):
                hours = round(hours * 1.3, 1)
            allocation[s["name"]] = max(1, hours)

    return allocation


def _priority_label(score: float) -> str:
    """Convert probability score to a human-readable priority."""
    if score >= 75:
        return "Must Study"
    elif score >= 55:
        return "High Priority"
    elif score >= 35:
        return "Medium Priority"
    else:
        return "Low Priority"
