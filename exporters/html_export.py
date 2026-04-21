"""
HTML Dashboard Exporter — generates an interactive standalone HTML file
with Plotly charts for frequency heatmaps, trends, and topic analysis.
"""
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from config import CategorizedQuestion
from analyzers.frequency import build_frequency_matrix, build_section_summary
from analyzers.trends import analyze_trends


def export_to_html(
    categorized: list[CategorizedQuestion],
    predictions: list[dict] | None = None,
    exam_name: str = "Exam",
) -> str:
    """
    Generate an interactive HTML dashboard.

    Returns:
        Complete HTML string with embedded Plotly charts
    """
    freq = build_frequency_matrix(categorized, group_by="topic")
    section_summary = build_section_summary(categorized)
    trends = analyze_trends(categorized)

    # Build individual chart HTML fragments
    charts = []

    # 1. Frequency Heatmap
    if not freq.empty:
        charts.append(_create_heatmap(freq, exam_name))

    # 2. Section-wise distribution pie chart
    if not section_summary.empty:
        charts.append(_create_section_pie(section_summary))

    # 3. Topic trend line chart (top 8 topics)
    if not freq.empty:
        charts.append(_create_trend_lines(freq))

    # 4. Difficulty distribution
    charts.append(_create_difficulty_chart(categorized))

    # 5. Probability score bar chart
    if not freq.empty:
        charts.append(_create_probability_bar(freq))

    # 6. Year-over-year summary
    if trends.get("year_over_year"):
        charts.append(_create_yoy_chart(trends["year_over_year"]))

    # 7. Predictions table
    if predictions:
        charts.append(_create_predictions_table(predictions))

    # Combine into full HTML
    charts_html = "\n".join(charts)

    # Trend summary text
    trend_text = _format_trend_summary(trends)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{exam_name} — Previous Year Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; color: #333; }}
        .header {{ background: linear-gradient(135deg, #1a237e, #283593); color: white; padding: 30px 40px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.85; font-size: 14px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                 margin: 20px 0; padding: 24px; }}
        .card h2 {{ color: #1a237e; margin-bottom: 16px; font-size: 20px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .trend-box {{ background: #e8eaf6; border-radius: 8px; padding: 16px; margin: 8px 0; }}
        .trend-box h3 {{ color: #283593; font-size: 15px; margin-bottom: 8px; }}
        .trend-box ul {{ margin-left: 20px; font-size: 14px; line-height: 1.8; }}
        .rising {{ border-left: 4px solid #4caf50; }}
        .falling {{ border-left: 4px solid #f44336; }}
        .new-topic {{ border-left: 4px solid #2196f3; }}
        .disappeared {{ border-left: 4px solid #9e9e9e; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ background: #1a237e; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #e0e0e0; }}
        tr:nth-child(even) {{ background: #f5f5f5; }}
        @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{exam_name} — Previous Year Paper Analysis</h1>
        <p>Interactive dashboard generated from {len(categorized)} questions across {len(set(cq.question.year for cq in categorized))} years</p>
    </div>
    <div class="container">
        {charts_html}

        <div class="card">
            <h2>Trend Summary</h2>
            {trend_text}
        </div>
    </div>
</body>
</html>"""

    return html


def _create_heatmap(freq: pd.DataFrame, exam_name: str) -> str:
    """Create a frequency heatmap chart."""
    year_cols = [c for c in freq.columns if c.isdigit()]
    if not year_cols:
        return ""

    labels = [f"{s} > {t}" for s, t in freq.index]
    z = freq[year_cols].values.tolist()

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=year_cols,
        y=labels,
        colorscale="YlGnBu",
        text=z,
        texttemplate="%{text}",
        hovertemplate="Topic: %{y}<br>Year: %{x}<br>Questions: %{z}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Topic × Year Frequency Matrix",
        height=max(400, len(labels) * 28),
        xaxis_title="Year",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=300),
    )
    div_id = "heatmap"
    return f'<div class="card"><h2>Frequency Heatmap</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_section_pie(section_summary: pd.DataFrame) -> str:
    """Create section distribution pie chart."""
    fig = go.Figure(data=go.Pie(
        labels=section_summary.index.tolist(),
        values=section_summary["Total"].tolist(),
        hole=0.4,
        textinfo="label+percent",
    ))
    fig.update_layout(title="Section-wise Question Distribution", height=400)
    div_id = "section_pie"
    return f'<div class="card"><h2>Section Distribution</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_trend_lines(freq: pd.DataFrame) -> str:
    """Create trend line chart for top topics."""
    year_cols = [c for c in freq.columns if c.isdigit()]
    if len(year_cols) < 2:
        return ""

    top = freq.head(8)

    fig = go.Figure()
    for idx, row in top.iterrows():
        section, topic = idx
        fig.add_trace(go.Scatter(
            x=year_cols,
            y=row[year_cols].tolist(),
            mode="lines+markers",
            name=f"{topic}",
            hovertemplate=f"{topic}<br>Year: %{{x}}<br>Questions: %{{y}}<extra></extra>",
        ))

    fig.update_layout(
        title="Top Topics — Year-over-Year Trend",
        xaxis_title="Year",
        yaxis_title="Number of Questions",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
    )
    div_id = "trend_lines"
    return f'<div class="card"><h2>Topic Trends</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_difficulty_chart(categorized: list[CategorizedQuestion]) -> str:
    """Create difficulty distribution bar chart."""
    difficulty_counts = {}
    for cq in categorized:
        d = cq.difficulty.value
        difficulty_counts[d] = difficulty_counts.get(d, 0) + 1

    colors = {"Easy": "#4caf50", "Medium": "#ff9800", "Hard": "#f44336", "Unknown": "#9e9e9e"}

    fig = go.Figure(data=go.Bar(
        x=list(difficulty_counts.keys()),
        y=list(difficulty_counts.values()),
        marker_color=[colors.get(d, "#999") for d in difficulty_counts.keys()],
        text=list(difficulty_counts.values()),
        textposition="auto",
    ))
    fig.update_layout(title="Difficulty Distribution", height=350, xaxis_title="Difficulty", yaxis_title="Count")
    div_id = "difficulty"
    return f'<div class="card"><h2>Difficulty Distribution</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_probability_bar(freq: pd.DataFrame) -> str:
    """Create probability score bar chart."""
    top = freq.head(15)
    labels = [f"{t}" for _, t in top.index]
    scores = top["ProbabilityScore"].tolist()

    fig = go.Figure(data=go.Bar(
        x=scores,
        y=labels,
        orientation="h",
        marker_color="steelblue",
        text=[f"{s:.0f}" for s in scores],
        textposition="auto",
    ))
    fig.update_layout(
        title="Top 15 Topics by Probability Score",
        height=500,
        xaxis_title="Probability Score",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=200),
    )
    div_id = "probability"
    return f'<div class="card"><h2>Topic Probability Ranking</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_yoy_chart(yoy: list[dict]) -> str:
    """Create year-over-year summary chart."""
    years = [str(y["year"]) for y in yoy]
    totals = [y["total_questions"] for y in yoy]
    topics = [y["topics_covered"] for y in yoy]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=years, y=totals, name="Total Questions", marker_color="steelblue"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=years, y=topics, name="Topics Covered", mode="lines+markers",
                   marker_color="orange"),
        secondary_y=True,
    )
    fig.update_layout(title="Year-over-Year Overview", height=400)
    fig.update_yaxes(title_text="Total Questions", secondary_y=False)
    fig.update_yaxes(title_text="Topics Covered", secondary_y=True)

    div_id = "yoy"
    return f'<div class="card"><h2>Year-over-Year Overview</h2><div id="{div_id}"></div></div>' + \
           f'<script>Plotly.newPlot("{div_id}", {fig.to_json()});</script>'


def _create_predictions_table(predictions: list[dict]) -> str:
    """Create an HTML table for predictions."""
    rows = ""
    for p in predictions[:20]:
        trend_color = "#4caf50" if "Rising" in p.get("trend", "") else \
                      "#f44336" if "Falling" in p.get("trend", "") else "#999"
        rows += f"""<tr>
            <td>{p['section']}</td>
            <td><strong>{p['topic']}</strong></td>
            <td>{p['predicted_count']}</td>
            <td>{p['probability_score']:.0f}</td>
            <td>{p['consistency']}</td>
            <td style="color:{trend_color};font-weight:bold">{p['trend']}</td>
        </tr>"""

    return f"""<div class="card">
        <h2>Predicted Topic Distribution (Next Exam)</h2>
        <table>
            <thead><tr>
                <th>Section</th><th>Topic</th><th>Expected Qs</th>
                <th>Probability</th><th>Consistency</th><th>Trend</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def _format_trend_summary(trends: dict) -> str:
    """Format trend analysis as HTML."""
    html = f'<p><strong>Difficulty Trend:</strong> {trends.get("difficulty_trend", "N/A")}</p>'

    def _topic_list(items, key_fn):
        if not items:
            return "<li><em>None detected</em></li>"
        return "".join(f"<li>{key_fn(t)}</li>" for t in items[:5])

    html += f"""
    <div class="grid">
        <div class="trend-box rising">
            <h3>Rising Topics (increasing frequency)</h3>
            <ul>{_topic_list(trends.get("rising_topics", []),
                lambda t: f"{t['section']} > {t['topic']} ({t['change_pct']:+.0f}%)")}</ul>
        </div>
        <div class="trend-box falling">
            <h3>Falling Topics (decreasing frequency)</h3>
            <ul>{_topic_list(trends.get("falling_topics", []),
                lambda t: f"{t['section']} > {t['topic']} ({t['change_pct']:+.0f}%)")}</ul>
        </div>
        <div class="trend-box new-topic">
            <h3>New Topics (recent only)</h3>
            <ul>{_topic_list(trends.get("new_topics", []),
                lambda t: f"{t['section']} > {t['topic']} ({t['count']} Qs)")}</ul>
        </div>
        <div class="trend-box disappeared">
            <h3>Disappeared Topics</h3>
            <ul>{_topic_list(trends.get("disappeared_topics", []),
                lambda t: f"{t['section']} > {t['topic']}")}</ul>
        </div>
    </div>"""

    return html
