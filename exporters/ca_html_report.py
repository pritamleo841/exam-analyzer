"""
CA Predictions HTML Report — generates a standalone, interactive HTML page
with sections ordered by importance, probability-scored facts, collapsible
MCQs, and a study-time allocation guide.

Designed for RBI Grade B 2026 exam preparation.
"""
import html as html_lib
from datetime import datetime


def export_ca_predictions_html(analysis: dict, exam_name: str = "RBI Grade B") -> str:
    """Generate a complete standalone HTML report from predictive analysis results.

    Args:
        analysis: Output from ca_predictor.run_predictive_analysis()
        exam_name: Target exam name

    Returns:
        Complete HTML string
    """
    sections = analysis.get("sections", [])
    top_50 = analysis.get("top_50_facts", [])
    metadata = analysis.get("metadata", {})
    readiness = analysis.get("readiness_score", 0)
    time_alloc = analysis.get("study_time_allocation", {})
    total_facts = analysis.get("total_facts", 0)
    total_qs = analysis.get("total_questions", 0)
    months = metadata.get("months_covered", [])
    pyq_years = metadata.get("pyq_years_used", 0)
    generated_at = metadata.get("generated_at", datetime.now().isoformat())

    # Build sections HTML
    sections_html = ""
    for idx, sec in enumerate(sections):
        if sec["fact_count"] == 0 and sec["question_count"] == 0:
            continue
        sections_html += _render_section(sec, idx)

    # Build top 50 facts HTML
    top_50_html = _render_top_50(top_50)

    # Build study time allocation
    time_html = _render_study_time(time_alloc)

    # Build summary stats
    months_str = ", ".join(months) if months else "N/A"
    readiness_color = "#4caf50" if readiness >= 70 else "#ff9800" if readiness >= 40 else "#f44336"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_e(exam_name)} 2026 — Current Affairs Predictions</title>
    <style>
{_get_css()}
    </style>
</head>
<body>
    <!-- HEADER -->
    <div class="header">
        <h1>🎯 {_e(exam_name)} 2026 — Current Affairs Predictions</h1>
        <p>AI-Powered Predictive Analysis &bull; High-Probability Questions &bull; 40-Day Study Optimizer</p>
        <div class="header-stats">
            <span class="stat-pill">📊 {total_facts} Facts Analyzed</span>
            <span class="stat-pill">❓ {total_qs} MCQs Generated</span>
            <span class="stat-pill">📅 Months: {_e(months_str)}</span>
            <span class="stat-pill">📚 PYQ Years: {pyq_years}</span>
            <span class="stat-pill">🕐 Generated: {generated_at[:10]}</span>
        </div>
    </div>

    <div class="container">
        <!-- READINESS SCORE -->
        <div class="card readiness-card">
            <h2>📈 Exam Readiness Score</h2>
            <div class="readiness-bar-container">
                <div class="readiness-bar" style="width: {readiness}%; background: {readiness_color};">
                    {readiness}%
                </div>
            </div>
            <p class="readiness-text">{_readiness_message(readiness)}</p>
        </div>

        <!-- SECTION OVERVIEW -->
        <div class="card">
            <h2>📋 Section Overview — Predicted Question Distribution</h2>
            <p class="card-desc">Based on PYQ patterns + AI importance analysis. Sections ordered by exam likelihood.</p>
            <div class="section-grid">
                {_render_section_overview(sections)}
            </div>
        </div>

        <!-- TOP 50 MUST-STUDY FACTS -->
        <div class="card">
            <h2>🔥 Top 50 Must-Study Facts</h2>
            <p class="card-desc">These facts have the highest probability of appearing in the exam. Study these first!</p>
            {top_50_html}
        </div>

        <!-- DETAILED SECTIONS -->
        <div class="card">
            <h2>📚 Detailed Section-wise Analysis</h2>
            <p class="card-desc">Click any section to expand and see facts + practice questions.</p>
        </div>
        {sections_html}

        <!-- STUDY TIME ALLOCATION -->
        <div class="card">
            <h2>⏰ Recommended Study Time Allocation (40 Days)</h2>
            <p class="card-desc">Based on ~2 hours/day dedicated to current affairs revision.</p>
            {time_html}
        </div>

        <!-- EXAM STRATEGY TIPS -->
        <div class="card">
            <h2>💡 Quick Strategy Tips</h2>
            <div class="tips-grid">
                <div class="tip-item">
                    <span class="tip-icon">🎯</span>
                    <div><strong>Focus on High-Probability</strong><br>Study the 🔴 Must Study facts first. These cover 60-70% of likely questions.</div>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">📊</span>
                    <div><strong>RBI & Budget = Game Changers</strong><br>RBI Monetary Policy + Union Budget alone account for 25-30% of CA questions.</div>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🔄</span>
                    <div><strong>Revise, Don't Just Read</strong><br>Attempt every MCQ in this report. Active recall beats passive reading 3x.</div>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">📅</span>
                    <div><strong>Latest 3 Months Matter Most</strong><br>April-June 2026 facts have the highest recency weight. Prioritize them.</div>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <p>Generated by Exam Analyzer Pro &bull; AI-Powered Predictive Analysis for {_e(exam_name)} 2026</p>
            <p class="footer-small">This report uses historical patterns and AI analysis. Actual exam questions may vary.</p>
        </div>
    </div>

    <script>
{_get_js()}
    </script>
</body>
</html>"""


def _e(text: str) -> str:
    """HTML-escape text."""
    return html_lib.escape(str(text))


def _render_section_overview(sections: list[dict]) -> str:
    """Render the grid of section cards in the overview."""
    html = ""
    for sec in sections:
        if sec["fact_count"] == 0 and sec["question_count"] == 0 and sec["predicted_questions"] == 0:
            continue
        priority_class = sec["study_priority"].lower().replace(" ", "-")
        icon = _section_icon(sec["name"])
        coverage_badge = _coverage_badge(sec["coverage_status"])

        html += f"""
        <div class="section-overview-card priority-{priority_class}">
            <div class="soc-header">
                <span class="soc-icon">{icon}</span>
                <span class="soc-name">{_e(sec['name'])}</span>
            </div>
            <div class="soc-stats">
                <div class="soc-stat">
                    <span class="soc-num">{sec['predicted_questions']}</span>
                    <span class="soc-label">Expected Qs</span>
                </div>
                <div class="soc-stat">
                    <span class="soc-num">{sec['fact_count']}</span>
                    <span class="soc-label">Facts</span>
                </div>
                <div class="soc-stat">
                    <span class="soc-num">{sec['question_count']}</span>
                    <span class="soc-label">MCQs</span>
                </div>
            </div>
            <div class="soc-footer">
                <span class="priority-badge badge-{priority_class}">{_e(sec['study_priority'])}</span>
                {coverage_badge}
            </div>
        </div>"""
    return html


def _render_top_50(facts: list[dict]) -> str:
    """Render the top 50 must-study facts as a numbered list."""
    if not facts:
        return "<p>No facts extracted yet. Upload CA PDFs to generate predictions.</p>"

    html = '<div class="top-facts-list">'
    for i, f in enumerate(facts, 1):
        prob = f.get("probability_score", 0)
        badge = _importance_badge(f.get("importance", "Medium"))
        cat_badge = f'<span class="cat-badge">{_e(f.get("category", ""))}</span>'
        month_tag = f' <span class="month-tag">{_e(f.get("month", ""))}</span>' if f.get("month") else ""
        prob_bar = f'<span class="prob-score" style="--prob: {prob}%">{prob}</span>'

        html += f"""
        <div class="fact-item {'fact-must-study' if prob >= 70 else 'fact-medium' if prob >= 45 else 'fact-low'}">
            <span class="fact-num">{i}</span>
            <div class="fact-content">
                <div class="fact-text">{_e(f.get('fact', ''))}</div>
                <div class="fact-meta">
                    {badge} {cat_badge} {month_tag} {prob_bar}
                </div>
                {"<div class='fact-why'><em>" + _e(f.get('why_it_matters', '')) + "</em></div>" if f.get('why_it_matters') else ""}
            </div>
        </div>"""
    html += '</div>'
    return html


def _render_section(sec: dict, idx: int) -> str:
    """Render a single detailed section with facts and MCQs."""
    icon = _section_icon(sec["name"])
    priority_class = sec["study_priority"].lower().replace(" ", "-")
    is_expanded = idx < 3  # First 3 sections expanded by default

    # Facts HTML
    facts_html = ""
    for i, f in enumerate(sec.get("facts", [])[:30], 1):  # Cap at 30 per section
        prob = f.get("probability_score", 0)
        badge = _importance_badge(f.get("importance", "Medium"))
        month_tag = f' <span class="month-tag">{_e(f.get("month", ""))}</span>' if f.get("month") else ""

        facts_html += f"""
            <div class="section-fact {'sf-high' if prob >= 70 else 'sf-med' if prob >= 45 else 'sf-low'}">
                <span class="sf-num">{i}.</span>
                <span class="sf-text">{_e(f.get('fact', ''))}</span>
                <span class="sf-score">{prob}</span>
                {badge} {month_tag}
            </div>"""

    # MCQs HTML
    mcqs_html = ""
    for i, q in enumerate(sec.get("questions", [])[:20], 1):  # Cap at 20 per section
        options_html = ""
        correct_idx = q.get("answer", 0)
        for j, opt in enumerate(q.get("options", [])):
            is_correct = j == correct_idx
            options_html += f"""
                    <div class="mcq-option" data-correct="{'true' if is_correct else 'false'}"
                         onclick="checkAnswer(this)">
                        {_e(opt)}
                    </div>"""

        prob = q.get("probability_score", 0)
        mcqs_html += f"""
            <div class="mcq-item">
                <div class="mcq-header">
                    <span class="mcq-num">Q{i}.</span>
                    <span class="mcq-prob">{prob}%</span>
                </div>
                <div class="mcq-question">{_e(q.get('question', ''))}</div>
                <div class="mcq-options">{options_html}</div>
                <div class="mcq-explanation" style="display:none;">
                    <strong>Explanation:</strong> {_e(q.get('explanation', ''))}
                </div>
            </div>"""

    # Historical pattern
    hist = sec.get("historical", {})
    hist_html = ""
    if hist:
        hist_html = f"""
            <div class="hist-info">
                <strong>Historical Pattern:</strong>
                Avg {hist.get('avg_count', '?')} Qs/year &bull;
                Consistency: {hist.get('consistency', '?')}% &bull;
                Trend: {hist.get('trend', 'N/A')}
            </div>"""

    return f"""
    <div class="section-card" id="section-{idx}">
        <div class="section-header priority-border-{priority_class}" onclick="toggleSection({idx})">
            <div class="sh-left">
                <span class="sh-icon">{icon}</span>
                <span class="sh-name">{_e(sec['name'])}</span>
                <span class="priority-badge badge-{priority_class}">{_e(sec['study_priority'])}</span>
            </div>
            <div class="sh-right">
                <span class="sh-stat">📊 {sec['predicted_questions']} expected</span>
                <span class="sh-stat">📝 {sec['fact_count']} facts</span>
                <span class="sh-stat">❓ {sec['question_count']} MCQs</span>
                <span class="sh-toggle" id="toggle-{idx}">{'▼' if is_expanded else '▶'}</span>
            </div>
        </div>
        <div class="section-body" id="body-{idx}" style="display: {'block' if is_expanded else 'none'};">
            {hist_html}

            <div class="section-tab-bar">
                <button class="stab active" onclick="showSubTab({idx}, 'facts')">📌 Key Facts ({sec['fact_count']})</button>
                <button class="stab" onclick="showSubTab({idx}, 'mcqs')">❓ Practice MCQs ({sec['question_count']})</button>
            </div>

            <div class="section-content" id="content-facts-{idx}">
                {facts_html if facts_html else '<p class="no-data">No facts extracted for this section. Upload more CA PDFs.</p>'}
            </div>
            <div class="section-content" id="content-mcqs-{idx}" style="display:none;">
                {mcqs_html if mcqs_html else '<p class="no-data">No MCQs generated for this section yet.</p>'}
            </div>
        </div>
    </div>"""


def _render_study_time(time_alloc: dict) -> str:
    """Render study time allocation as a horizontal bar chart."""
    if not time_alloc:
        return "<p>Upload CA PDFs and run analysis to get study time recommendations.</p>"

    max_hours = max(time_alloc.values()) if time_alloc else 1
    html = '<div class="time-alloc">'
    for section, hours in sorted(time_alloc.items(), key=lambda x: x[1], reverse=True):
        pct = hours / max_hours * 100
        html += f"""
        <div class="time-row">
            <span class="time-label">{_e(section)}</span>
            <div class="time-bar-bg">
                <div class="time-bar" style="width: {pct}%;">{hours}h</div>
            </div>
        </div>"""
    total = sum(time_alloc.values())
    html += f'<div class="time-total">Total: {round(total, 1)} hours (~{round(total/40, 1)}h/day for 40 days)</div>'
    html += '</div>'
    return html


def _importance_badge(importance: str) -> str:
    colors = {"High": "#e53935", "Medium": "#fb8c00", "Low": "#43a047"}
    icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    color = colors.get(importance, "#757575")
    icon = icons.get(importance, "⚪")
    return f'<span class="imp-badge" style="color:{color}">{icon} {importance}</span>'


def _coverage_badge(status: str) -> str:
    colors = {
        "Well Covered": "#43a047",
        "Needs More Questions": "#fb8c00",
        "Gap - Need Material": "#e53935",
        "Low Priority": "#9e9e9e",
    }
    color = colors.get(status, "#757575")
    return f'<span class="coverage-badge" style="background:{color};">{_e(status)}</span>'


def _section_icon(name: str) -> str:
    icons = {
        "Union Budget": "💰",
        "Economic Survey": "📊",
        "RBI & Monetary Policy": "🏦",
        "Banking & Finance": "🏛️",
        "Reports & Indices": "📈",
        "Government Schemes": "🏗️",
        "International Organizations & Summits": "🌍",
        "Financial Markets & Regulations": "📉",
        "Social Issues & Development": "👥",
        "Appointments & Awards": "🏆",
        "Agriculture & Rural Economy": "🌾",
        "External Sector & Trade": "🚢",
        "Insurance & Pension": "🛡️",
        "Science & Technology": "🔬",
        "Environment & Sustainability": "🌿",
        "Defence & Security": "🛡️",
        "Sports & Events": "🏅",
        "General": "📌",
    }
    return icons.get(name, "📌")


def _readiness_message(score: float) -> str:
    if score >= 80:
        return "Excellent coverage! Focus on revising the top facts and attempting all MCQs."
    elif score >= 60:
        return "Good progress. Some sections need more material. Check the 'Gap' sections below."
    elif score >= 40:
        return "Moderate coverage. Upload more monthly CA PDFs and PYQ papers to improve predictions."
    elif score >= 20:
        return "Getting started. Upload all 6 months of CA PDFs for best results."
    else:
        return "Upload CA PDFs (Jan-Jun) and previous year papers to begin your analysis."


def _get_css() -> str:
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; color: #1a1a2e; line-height: 1.6; }

        .header {
            background: linear-gradient(135deg, #0d47a1, #1565c0, #1976d2);
            color: white; padding: 35px 40px; text-align: center;
        }
        .header h1 { font-size: 30px; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 15px; margin-bottom: 15px; }
        .header-stats { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }
        .stat-pill {
            background: rgba(255,255,255,0.18); padding: 5px 14px; border-radius: 20px;
            font-size: 13px; backdrop-filter: blur(5px);
        }

        .container { max-width: 1300px; margin: 0 auto; padding: 24px; }

        .card {
            background: white; border-radius: 14px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.07);
            margin: 20px 0; padding: 28px;
        }
        .card h2 { color: #0d47a1; margin-bottom: 10px; font-size: 22px; }
        .card-desc { color: #666; font-size: 14px; margin-bottom: 18px; }

        /* Readiness */
        .readiness-card { text-align: center; }
        .readiness-bar-container { background: #e8eaf6; border-radius: 12px; height: 38px; margin: 15px auto; max-width: 600px; overflow: hidden; }
        .readiness-bar { height: 100%; border-radius: 12px; color: white; font-weight: bold; font-size: 16px; line-height: 38px; transition: width 1s; min-width: 50px; }
        .readiness-text { color: #555; font-size: 14px; margin-top: 8px; }

        /* Section overview grid */
        .section-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }
        .section-overview-card {
            border-radius: 10px; padding: 16px; border-left: 5px solid #ccc;
            background: #fafafa; transition: transform 0.2s;
        }
        .section-overview-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .priority-critical { border-left-color: #e53935; }
        .priority-high { border-left-color: #fb8c00; }
        .priority-medium { border-left-color: #1e88e5; }
        .priority-low { border-left-color: #9e9e9e; }
        .soc-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .soc-icon { font-size: 22px; }
        .soc-name { font-weight: 600; font-size: 14px; }
        .soc-stats { display: flex; justify-content: space-around; margin: 10px 0; }
        .soc-stat { text-align: center; }
        .soc-num { display: block; font-size: 20px; font-weight: 700; color: #0d47a1; }
        .soc-label { font-size: 11px; color: #888; }
        .soc-footer { display: flex; gap: 8px; flex-wrap: wrap; }

        .priority-badge { padding: 2px 10px; border-radius: 10px; font-size: 11px; font-weight: 600; color: white; }
        .badge-critical { background: #e53935; }
        .badge-high { background: #fb8c00; }
        .badge-medium { background: #1e88e5; }
        .badge-low { background: #9e9e9e; }
        .coverage-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; color: white; }

        /* Top 50 facts */
        .top-facts-list { max-height: 800px; overflow-y: auto; }
        .fact-item { display: flex; align-items: flex-start; gap: 12px; padding: 10px 14px; border-bottom: 1px solid #eee; }
        .fact-item:hover { background: #f5f7ff; }
        .fact-must-study { border-left: 4px solid #e53935; }
        .fact-medium { border-left: 4px solid #fb8c00; }
        .fact-low { border-left: 4px solid #43a047; }
        .fact-num { font-weight: 700; color: #0d47a1; min-width: 28px; font-size: 14px; padding-top: 2px; }
        .fact-content { flex: 1; }
        .fact-text { font-size: 14px; margin-bottom: 5px; }
        .fact-meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
        .fact-why { font-size: 12px; color: #666; margin-top: 4px; }
        .imp-badge { font-size: 12px; font-weight: 600; }
        .cat-badge { background: #e8eaf6; color: #283593; padding: 1px 8px; border-radius: 8px; font-size: 11px; }
        .month-tag { background: #e3f2fd; color: #1565c0; padding: 1px 8px; border-radius: 8px; font-size: 11px; }
        .prob-score {
            background: linear-gradient(90deg, #e8eaf6 var(--prob), #fff var(--prob));
            padding: 1px 8px; border-radius: 8px; font-size: 11px; font-weight: 700;
            color: #0d47a1; border: 1px solid #c5cae9;
        }

        /* Detailed sections */
        .section-card { background: white; border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin: 14px 0; overflow: hidden; }
        .section-header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 18px 24px; cursor: pointer; transition: background 0.2s;
        }
        .section-header:hover { background: #f5f7ff; }
        .priority-border-critical { border-left: 5px solid #e53935; }
        .priority-border-high { border-left: 5px solid #fb8c00; }
        .priority-border-medium { border-left: 5px solid #1e88e5; }
        .priority-border-low { border-left: 5px solid #9e9e9e; }
        .sh-left { display: flex; align-items: center; gap: 10px; }
        .sh-icon { font-size: 24px; }
        .sh-name { font-weight: 700; font-size: 17px; }
        .sh-right { display: flex; align-items: center; gap: 16px; }
        .sh-stat { font-size: 13px; color: #555; }
        .sh-toggle { font-size: 16px; color: #999; margin-left: 8px; }

        .section-body { padding: 0 24px 24px; }
        .hist-info { background: #fff3e0; padding: 10px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 14px; }

        .section-tab-bar { display: flex; gap: 6px; margin-bottom: 14px; }
        .stab {
            padding: 7px 18px; border: 1px solid #c5cae9; border-radius: 8px;
            background: white; cursor: pointer; font-size: 13px; transition: all 0.2s;
        }
        .stab:hover { background: #e8eaf6; }
        .stab.active { background: #0d47a1; color: white; border-color: #0d47a1; }

        /* Section facts */
        .section-fact { display: flex; align-items: center; gap: 8px; padding: 7px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; flex-wrap: wrap; }
        .sf-high { }
        .sf-med { opacity: 0.9; }
        .sf-low { opacity: 0.75; }
        .sf-num { font-weight: 600; color: #888; min-width: 30px; }
        .sf-text { flex: 1; min-width: 200px; }
        .sf-score {
            background: #e8eaf6; color: #283593; padding: 2px 8px;
            border-radius: 6px; font-weight: 700; font-size: 12px;
        }

        /* MCQs */
        .mcq-item { border: 1px solid #e0e0e0; border-radius: 10px; padding: 16px; margin: 10px 0; }
        .mcq-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .mcq-num { font-weight: 700; color: #0d47a1; }
        .mcq-prob { font-size: 12px; color: #888; }
        .mcq-question { font-size: 14px; font-weight: 500; margin-bottom: 10px; }
        .mcq-options { display: flex; flex-direction: column; gap: 6px; }
        .mcq-option {
            padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px;
            cursor: pointer; transition: all 0.2s; font-size: 13px;
        }
        .mcq-option:hover { background: #e8eaf6; border-color: #9fa8da; }
        .mcq-option.correct { background: #e8f5e9; border-color: #4caf50; color: #2e7d32; font-weight: 600; }
        .mcq-option.wrong { background: #ffebee; border-color: #ef5350; color: #c62828; }
        .mcq-option.reveal { background: #e8f5e9; border-color: #4caf50; }
        .mcq-explanation { margin-top: 10px; padding: 10px; background: #f3e5f5; border-radius: 8px; font-size: 13px; color: #4a148c; }

        .no-data { color: #999; font-style: italic; padding: 20px; text-align: center; }

        /* Study time */
        .time-alloc { max-width: 700px; }
        .time-row { display: flex; align-items: center; gap: 12px; margin: 6px 0; }
        .time-label { min-width: 220px; font-size: 13px; font-weight: 500; text-align: right; }
        .time-bar-bg { flex: 1; background: #e8eaf6; border-radius: 6px; height: 22px; overflow: hidden; }
        .time-bar { height: 100%; background: linear-gradient(90deg, #1565c0, #42a5f5); border-radius: 6px; color: white; font-size: 11px; font-weight: 600; line-height: 22px; padding: 0 8px; min-width: 30px; }
        .time-total { text-align: center; margin-top: 12px; font-weight: 600; color: #0d47a1; }

        /* Tips */
        .tips-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .tip-item { display: flex; gap: 12px; padding: 14px; background: #f5f7ff; border-radius: 10px; }
        .tip-icon { font-size: 28px; }

        .footer { text-align: center; padding: 30px 0 10px; color: #888; font-size: 13px; }
        .footer-small { font-size: 11px; color: #bbb; margin-top: 4px; }

        /* Print styles */
        @media print {
            .header { padding: 15px; }
            .container { padding: 10px; }
            .card { box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }
            .section-body { display: block !important; }
            .mcq-option { border: 1px solid #ccc; }
            .mcq-explanation { display: block !important; }
        }
        @media (max-width: 768px) {
            .section-grid { grid-template-columns: 1fr; }
            .tips-grid { grid-template-columns: 1fr; }
            .sh-right { flex-wrap: wrap; }
            .time-label { min-width: 120px; font-size: 12px; }
            .header h1 { font-size: 22px; }
        }
    """


def _get_js() -> str:
    return """
    function toggleSection(idx) {
        var body = document.getElementById('body-' + idx);
        var toggle = document.getElementById('toggle-' + idx);
        if (body.style.display === 'none') {
            body.style.display = 'block';
            toggle.textContent = '▼';
        } else {
            body.style.display = 'none';
            toggle.textContent = '▶';
        }
    }

    function showSubTab(sectionIdx, tab) {
        var factsEl = document.getElementById('content-facts-' + sectionIdx);
        var mcqsEl = document.getElementById('content-mcqs-' + sectionIdx);
        if (!factsEl || !mcqsEl) return;

        // Toggle content
        if (tab === 'facts') {
            factsEl.style.display = 'block';
            mcqsEl.style.display = 'none';
        } else {
            factsEl.style.display = 'none';
            mcqsEl.style.display = 'block';
        }

        // Toggle tab active state
        var card = factsEl.closest('.section-card') || factsEl.parentElement;
        var tabs = card.querySelectorAll('.stab');
        tabs.forEach(function(t, i) {
            if ((tab === 'facts' && i === 0) || (tab === 'mcqs' && i === 1)) {
                t.classList.add('active');
            } else {
                t.classList.remove('active');
            }
        });
    }

    function checkAnswer(el) {
        // Prevent re-clicking
        var parent = el.closest('.mcq-options');
        if (parent.classList.contains('answered')) return;
        parent.classList.add('answered');

        var isCorrect = el.getAttribute('data-correct') === 'true';
        if (isCorrect) {
            el.classList.add('correct');
        } else {
            el.classList.add('wrong');
            // Reveal correct answer
            var options = parent.querySelectorAll('.mcq-option');
            options.forEach(function(opt) {
                if (opt.getAttribute('data-correct') === 'true') {
                    opt.classList.add('reveal');
                }
            });
        }

        // Show explanation
        var mcqItem = el.closest('.mcq-item');
        var expl = mcqItem.querySelector('.mcq-explanation');
        if (expl) expl.style.display = 'block';
    }
    """
