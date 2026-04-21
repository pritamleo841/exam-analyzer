"""
Trend Analysis — detect rising/falling topics, new entries, difficulty shifts.
"""
import pandas as pd
import numpy as np
from config import CategorizedQuestion


def analyze_trends(
    categorized: list[CategorizedQuestion],
) -> dict:
    """
    Analyze trends across years.

    Returns dict with:
    - rising_topics: topics with increasing frequency in recent years
    - falling_topics: topics with decreasing frequency
    - new_topics: topics that appeared only in recent years
    - disappeared_topics: topics that stopped appearing
    - difficulty_trend: overall difficulty trend
    """
    records = [
        {
            "section": cq.section,
            "topic": cq.topic,
            "year": cq.question.year,
            "difficulty": cq.difficulty.value,
        }
        for cq in categorized
    ]

    if not records:
        return {
            "rising_topics": [],
            "falling_topics": [],
            "new_topics": [],
            "disappeared_topics": [],
            "difficulty_trend": "Insufficient data",
            "year_over_year": [],
        }

    df = pd.DataFrame(records)
    years = sorted(df["year"].unique())

    if len(years) < 2:
        return {
            "rising_topics": [],
            "falling_topics": [],
            "new_topics": [],
            "disappeared_topics": [],
            "difficulty_trend": "Need at least 2 years of data",
            "year_over_year": [],
        }

    # Split into recent (last 2 years) and older
    recent_years = years[-2:]
    older_years = years[:-2] if len(years) > 2 else years[:1]

    recent = df[df["year"].isin(recent_years)]
    older = df[df["year"].isin(older_years)]

    # Topic counts per period
    recent_counts = recent.groupby(["section", "topic"]).size().reset_index(name="recent_count")
    older_counts = older.groupby(["section", "topic"]).size().reset_index(name="older_count")

    merged = pd.merge(recent_counts, older_counts, on=["section", "topic"], how="outer").fillna(0)

    # Normalize by number of years
    merged["recent_avg"] = merged["recent_count"] / len(recent_years)
    merged["older_avg"] = merged["older_count"] / max(len(older_years), 1)

    # Calculate change
    merged["change"] = merged["recent_avg"] - merged["older_avg"]
    merged["change_pct"] = np.where(
        merged["older_avg"] > 0,
        (merged["change"] / merged["older_avg"] * 100).round(1),
        100.0  # new topic
    )

    # Rising topics: recent avg significantly higher
    rising = merged[merged["change"] > 0.5].sort_values("change", ascending=False)
    rising_topics = [
        {
            "section": row["section"],
            "topic": row["topic"],
            "recent_avg": round(row["recent_avg"], 1),
            "older_avg": round(row["older_avg"], 1),
            "change_pct": row["change_pct"],
        }
        for _, row in rising.iterrows()
    ]

    # Falling topics: recent avg significantly lower
    falling = merged[merged["change"] < -0.5].sort_values("change", ascending=True)
    falling_topics = [
        {
            "section": row["section"],
            "topic": row["topic"],
            "recent_avg": round(row["recent_avg"], 1),
            "older_avg": round(row["older_avg"], 1),
            "change_pct": row["change_pct"],
        }
        for _, row in falling.iterrows()
    ]

    # New topics: appeared only in recent years
    new = merged[(merged["older_count"] == 0) & (merged["recent_count"] > 0)]
    new_topics = [
        {"section": row["section"], "topic": row["topic"], "count": int(row["recent_count"])}
        for _, row in new.iterrows()
    ]

    # Disappeared topics: appeared in older but not recent
    disappeared = merged[(merged["recent_count"] == 0) & (merged["older_count"] > 0)]
    disappeared_topics = [
        {"section": row["section"], "topic": row["topic"], "last_count": int(row["older_count"])}
        for _, row in disappeared.iterrows()
    ]

    # Difficulty trend
    difficulty_trend = _analyze_difficulty_trend(df, years)

    # Year-over-year summary
    yoy = _year_over_year(df, years)

    return {
        "rising_topics": rising_topics,
        "falling_topics": falling_topics,
        "new_topics": new_topics,
        "disappeared_topics": disappeared_topics,
        "difficulty_trend": difficulty_trend,
        "year_over_year": yoy,
    }


def _analyze_difficulty_trend(df: pd.DataFrame, years: list) -> str:
    """Analyze overall difficulty trend across years."""
    difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3, "Unknown": 2}
    df["diff_score"] = df["difficulty"].map(difficulty_map)

    yearly_avg = df.groupby("year")["diff_score"].mean()
    if len(yearly_avg) < 2:
        return "Insufficient data"

    first_half = yearly_avg.iloc[: len(yearly_avg) // 2].mean()
    second_half = yearly_avg.iloc[len(yearly_avg) // 2 :].mean()

    diff = second_half - first_half
    if diff > 0.3:
        return "Getting Harder — difficulty has increased in recent years"
    elif diff < -0.3:
        return "Getting Easier — difficulty has decreased in recent years"
    return "Stable — difficulty level has remained consistent"


def _year_over_year(df: pd.DataFrame, years: list) -> list[dict]:
    """Calculate year-over-year statistics."""
    yoy = []
    for year in years:
        year_data = df[df["year"] == year]
        yoy.append({
            "year": year,
            "total_questions": len(year_data),
            "sections": year_data["section"].nunique(),
            "topics_covered": year_data["topic"].nunique(),
        })
    return yoy
