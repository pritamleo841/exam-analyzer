"""
Frequency Matrix Builder — core analysis engine.
Builds topic × year frequency tables, calculates probability scores,
and ranks topics by likelihood of appearing in the next exam.
"""
import pandas as pd
import numpy as np
from config import CategorizedQuestion


def build_frequency_matrix(
    categorized: list[CategorizedQuestion],
    group_by: str = "topic",
) -> pd.DataFrame:
    """
    Build a topic × year frequency matrix.

    Args:
        categorized: List of categorized questions
        group_by: "topic", "sub_topic", or "section"

    Returns:
        DataFrame with topics as rows, years as columns, question counts as values.
        Extra columns: Total, Percentage, Consistency, ProbabilityScore
    """
    records = []
    for cq in categorized:
        records.append({
            "section": cq.section,
            "topic": cq.topic,
            "sub_topic": cq.sub_topic or cq.topic,
            "year": cq.question.year,
            "phase": cq.question.phase,
            "difficulty": cq.difficulty.value,
        })

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    years = sorted(df["year"].unique())

    # Pivot: count questions per topic per year
    pivot = df.pivot_table(
        index=["section", group_by],
        columns="year",
        values="difficulty",  # just counting
        aggfunc="count",
        fill_value=0,
    )

    # Flatten column names
    pivot.columns = [str(y) for y in pivot.columns]

    # Add summary columns
    year_cols = [str(y) for y in years]
    pivot["Total"] = pivot[year_cols].sum(axis=1)
    total_questions = pivot["Total"].sum()
    pivot["Percentage"] = (pivot["Total"] / total_questions * 100).round(1) if total_questions > 0 else 0

    # Consistency: how many years did this topic appear (out of total years)
    pivot["Consistency"] = (pivot[year_cols] > 0).sum(axis=1)
    pivot["ConsistencyPct"] = (pivot["Consistency"] / len(years) * 100).round(0)

    # Probability Score (0-100): weighted combination of frequency and consistency
    # Formula: 0.5 * normalized_frequency + 0.3 * consistency + 0.2 * recent_trend
    max_total = pivot["Total"].max() if pivot["Total"].max() > 0 else 1
    freq_score = pivot["Total"] / max_total * 100

    consistency_score = pivot["ConsistencyPct"]

    # Recent trend: average of last 2 years vs overall average
    if len(years) >= 3:
        recent_cols = [str(y) for y in years[-2:]]
        overall_avg = pivot[year_cols].mean(axis=1)
        recent_avg = pivot[recent_cols].mean(axis=1)
        # Trend: positive if recent > overall, capped at +/-50
        trend_score = np.clip(
            ((recent_avg - overall_avg) / overall_avg.replace(0, 1) * 50 + 50),
            0, 100
        )
    else:
        trend_score = 50  # neutral

    pivot["ProbabilityScore"] = (
        0.5 * freq_score + 0.3 * consistency_score + 0.2 * trend_score
    ).round(1)

    # Sort by probability score descending
    pivot = pivot.sort_values("ProbabilityScore", ascending=False)

    return pivot


def build_section_summary(categorized: list[CategorizedQuestion]) -> pd.DataFrame:
    """Build a summary table of question counts per section per year."""
    records = [
        {"section": cq.section, "year": cq.question.year}
        for cq in categorized
    ]
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    pivot = df.pivot_table(
        index="section",
        columns="year",
        values="section",
        aggfunc="count",
        fill_value=0,
    )
    pivot.columns = [str(y) for y in pivot.columns]
    pivot["Total"] = pivot.sum(axis=1)
    return pivot


def build_difficulty_distribution(categorized: list[CategorizedQuestion]) -> pd.DataFrame:
    """Build difficulty distribution per section and topic."""
    records = [
        {
            "section": cq.section,
            "topic": cq.topic,
            "difficulty": cq.difficulty.value,
        }
        for cq in categorized
    ]
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    pivot = df.pivot_table(
        index=["section", "topic"],
        columns="difficulty",
        values="section",
        aggfunc="count",
        fill_value=0,
    )
    pivot["Total"] = pivot.sum(axis=1)
    return pivot


def get_top_topics(
    frequency_matrix: pd.DataFrame,
    n: int = 10,
    section_filter: str | None = None,
) -> pd.DataFrame:
    """Get top N topics by probability score, optionally filtered by section."""
    df = frequency_matrix.copy()
    if section_filter:
        df = df.loc[df.index.get_level_values("section") == section_filter]
    return df.head(n)
