"""
GitHub Pages Site Builder — generates a single, comprehensive HTML page
that consolidates ALL current affairs data into a navigable, searchable,
filterable study portal for RBI Grade B 2026 exam preparation.

This page is designed to be hosted on GitHub Pages and updated incrementally
as new CA PDFs are uploaded and analyzed.

Features:
- Section-wise navigation sidebar
- Full-text search across all facts and questions
- Filter by category, importance, month, probability
- Revision mode: hide answers for self-testing
- Bookmarking: mark facts as "studied" (localStorage)
- Print-friendly layout
- Mobile responsive
"""
import html as html_lib
import json
from datetime import datetime


def build_github_pages_site(analysis: dict, exam_name: str = "RBI Grade B") -> str:
    """Build the complete GitHub Pages site HTML.

    Args:
        analysis: Output from ca_predictor.run_predictive_analysis()
        exam_name: Target exam name

    Returns:
        Complete standalone HTML string with embedded data, CSS, and JS
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

    # Prepare data for JS embedding (all facts + questions as JSON)
    all_facts_json = []
    all_questions_json = []
    for sec in sections:
        for f in sec.get("facts", []):
            all_facts_json.append({
                "fact": f.get("fact", ""),
                "category": f.get("category", sec.get("name", "")),
                "importance": f.get("importance", "Medium"),
                "probability": f.get("probability_score", 0),
                "month": f.get("month", ""),
                "why": f.get("why_it_matters", ""),
                "section": sec.get("name", ""),
                "priority": f.get("priority", ""),
            })
        for q in sec.get("questions", []):
            all_questions_json.append({
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "answer": q.get("answer", 0),
                "explanation": q.get("explanation", ""),
                "category": q.get("category", sec.get("name", "")),
                "importance": q.get("importance", "Medium"),
                "probability": q.get("probability_score", 0),
                "month": q.get("month", ""),
                "section": sec.get("name", ""),
            })

    # Sections metadata for navigation
    nav_sections = []
    for sec in sections:
        if sec["fact_count"] > 0 or sec["question_count"] > 0:
            nav_sections.append({
                "name": sec["name"],
                "icon": _section_icon(sec["name"]),
                "priority": sec["study_priority"],
                "predicted": sec["predicted_questions"],
                "facts": sec["fact_count"],
                "questions": sec["question_count"],
                "weight": sec["weight"],
            })

    data_json = json.dumps({
        "facts": all_facts_json,
        "questions": all_questions_json,
        "sections": nav_sections,
        "top50": [f.get("fact", "") for f in top_50[:50]],
        "metadata": {
            "exam": exam_name,
            "readiness": readiness,
            "totalFacts": total_facts,
            "totalQuestions": total_qs,
            "months": months,
            "pyqYears": pyq_years,
            "generatedAt": generated_at,
        },
        "timeAllocation": time_alloc,
    }, ensure_ascii=False)

    # Build section detail views HTML
    section_views_html = ""
    for idx, sec in enumerate(sections):
        if sec["fact_count"] == 0 and sec["question_count"] == 0:
            continue
        section_views_html += _render_section_view(sec, idx)

    readiness_color = "#4caf50" if readiness >= 70 else "#ff9800" if readiness >= 40 else "#f44336"
    months_str = ", ".join(months) if months else "N/A"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_e(exam_name)} 2026 — CA Study Portal</title>
    <meta name="description" content="Current Affairs Predictions for {_e(exam_name)} 2026 - AI-Powered Study Portal">
    <style>
{_get_css()}
    </style>
</head>
<body>
    <!-- EMBEDDED DATA -->
    <script>
        const SITE_DATA = {data_json};
    </script>

    <!-- TOP BAR -->
    <div class="topbar">
        <div class="topbar-left">
            <button class="hamburger" onclick="toggleSidebar()" title="Toggle menu">☰</button>
            <span class="logo">🎯</span>
            <span class="site-title">{_e(exam_name)} 2026 — CA Study Portal</span>
        </div>
        <div class="topbar-right">
            <div class="search-box">
                <input type="text" id="globalSearch" placeholder="Search facts, questions..." oninput="handleSearch(this.value)">
                <span class="search-count" id="searchCount"></span>
            </div>
            <button class="mode-btn" id="revisionBtn" onclick="toggleRevisionMode()" title="Revision Mode">📝 Revision</button>
            <button class="mode-btn" onclick="toggleDarkMode()" title="Dark Mode">🌙</button>
        </div>
    </div>

    <!-- LAYOUT: Sidebar + Main -->
    <div class="layout">
        <!-- SIDEBAR NAV -->
        <nav class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h3>📚 Sections</h3>
                <div class="sidebar-stats">
                    <span>{total_facts} facts</span> &bull; <span>{total_qs} MCQs</span>
                </div>
            </div>

            <div class="nav-item active" onclick="showView('dashboard')" data-view="dashboard">
                <span class="nav-icon">📊</span>
                <span class="nav-label">Dashboard</span>
            </div>
            <div class="nav-item" onclick="showView('top50')" data-view="top50">
                <span class="nav-icon">🔥</span>
                <span class="nav-label">Top 50 Must-Study</span>
            </div>
            <div class="nav-item" onclick="showView('all-facts')" data-view="all-facts">
                <span class="nav-icon">📋</span>
                <span class="nav-label">All Facts</span>
            </div>
            <div class="nav-item" onclick="showView('all-mcqs')" data-view="all-mcqs">
                <span class="nav-icon">❓</span>
                <span class="nav-label">All MCQs</span>
            </div>
            <div class="nav-item" onclick="showView('revision')" data-view="revision">
                <span class="nav-icon">🧠</span>
                <span class="nav-label">Revision &amp; Recall</span>
            </div>

            <div class="nav-divider">CATEGORIES</div>
            {"".join(_sidebar_nav_item(sec, idx) for idx, sec in enumerate(nav_sections))}

            <div class="nav-divider">TOOLS</div>
            <div class="nav-item" onclick="showView('study-plan')" data-view="study-plan">
                <span class="nav-icon">⏰</span>
                <span class="nav-label">Study Plan</span>
            </div>
            <div class="nav-item" onclick="showView('bookmarks')" data-view="bookmarks">
                <span class="nav-icon">⭐</span>
                <span class="nav-label">Bookmarked</span>
            </div>
            <div class="nav-item" onclick="showView('search-results')" data-view="search-results" style="display:none" id="searchNav">
                <span class="nav-icon">🔍</span>
                <span class="nav-label">Search Results</span>
            </div>

            <div class="sidebar-footer">
                <div class="progress-ring">
                    <span class="progress-pct" style="color:{readiness_color}">{readiness}%</span>
                    <span class="progress-label">Ready</span>
                </div>
                <small>Updated: {generated_at[:10]}</small>
            </div>
        </nav>

        <!-- MAIN CONTENT -->
        <main class="main-content" id="mainContent">
            <!-- DASHBOARD VIEW -->
            <div class="view active" id="view-dashboard">
                <h1>📊 Dashboard</h1>
                <div class="stats-row">
                    <div class="stat-card sc-blue"><div class="sc-value">{total_facts}</div><div class="sc-label">Facts Extracted</div></div>
                    <div class="stat-card sc-green"><div class="sc-value">{total_qs}</div><div class="sc-label">MCQs Generated</div></div>
                    <div class="stat-card sc-orange"><div class="sc-value">{len(months)}</div><div class="sc-label">Months Covered</div></div>
                    <div class="stat-card sc-red"><div class="sc-value">{pyq_years}</div><div class="sc-label">PYQ Years Used</div></div>
                </div>
                <div class="readiness-section">
                    <h2>Exam Readiness</h2>
                    <div class="readiness-bar-track"><div class="readiness-bar-fill" style="width:{readiness}%; background:{readiness_color}">{readiness}%</div></div>
                    <p class="readiness-msg">{_readiness_message(readiness)}</p>
                </div>
                <div class="section-overview">
                    <h2>Section-wise Predictions</h2>
                    <div class="overview-grid">{_render_overview_cards(nav_sections)}</div>
                </div>
                <div class="months-covered">
                    <h2>📅 Months Covered</h2>
                    <div class="month-pills">{_render_month_pills(months)}</div>
                </div>
            </div>

            <!-- TOP 50 VIEW -->
            <div class="view" id="view-top50">
                <h1>🔥 Top 50 Must-Study Facts</h1>
                <p class="view-desc">Highest probability of appearing in the exam. Master these first!</p>
                <div class="filter-bar">
                    <select id="top50ImpFilter" onchange="filterTop50()"><option value="">All Importance</option><option value="High">🔴 High</option><option value="Medium">🟡 Medium</option><option value="Low">🟢 Low</option></select>
                    <select id="top50CatFilter" onchange="filterTop50()"><option value="">All Categories</option></select>
                </div>
                <div id="top50List" class="facts-list"></div>
            </div>

            <!-- ALL FACTS VIEW -->
            <div class="view" id="view-all-facts">
                <h1>📋 All Extracted Facts</h1>
                <div class="filter-bar">
                    <select id="factsImpFilter" onchange="filterFacts()"><option value="">All Importance</option><option value="High">🔴 High Only</option><option value="Medium">🟡 Medium</option><option value="Low">🟢 Low</option></select>
                    <select id="factsCatFilter" onchange="filterFacts()"><option value="">All Categories</option></select>
                    <select id="factsMonthFilter" onchange="filterFacts()"><option value="">All Months</option></select>
                    <select id="factsSortBy" onchange="filterFacts()"><option value="probability">Sort: Probability</option><option value="category">Sort: Category</option><option value="month">Sort: Month</option><option value="importance">Sort: Importance</option></select>
                </div>
                <div class="facts-count" id="factsCount"></div>
                <div id="factsList" class="facts-list"></div>
            </div>

            <!-- ALL MCQS VIEW -->
            <div class="view" id="view-all-mcqs">
                <h1>❓ All Practice MCQs</h1>
                <div class="filter-bar">
                    <select id="mcqsCatFilter" onchange="filterMcqs()"><option value="">All Categories</option></select>
                    <select id="mcqsImpFilter" onchange="filterMcqs()"><option value="">All Importance</option><option value="High">🔴 High</option><option value="Medium">🟡 Medium</option></select>
                    <button class="mode-btn" onclick="resetAllMcqs()">🔄 Reset All</button>
                </div>
                <div class="mcq-score-bar" id="mcqScoreBar">Score: <span id="mcqCorrect">0</span>/<span id="mcqTotal">0</span> (<span id="mcqPct">0</span>%)</div>
                <div id="mcqsList" class="mcqs-list"></div>
            </div>

            <!-- REVISION VIEW -->
            <div class="view" id="view-revision">
                <h1>🧠 Revision &amp; Recall Mode</h1>
                <p class="view-desc">Test yourself! Facts are blurred — click to reveal. Track what you remember.</p>
                <div class="revision-controls">
                    <button class="rev-btn" onclick="startRevision('all')">📋 All Facts</button>
                    <button class="rev-btn" onclick="startRevision('high')">🔴 High Priority</button>
                    <button class="rev-btn" onclick="startRevision('bookmarked')">⭐ Bookmarked</button>
                    <button class="rev-btn" onclick="startRevision('weak')">❌ Weak Areas</button>
                </div>
                <div class="revision-stats" id="revisionStats"></div>
                <div id="revisionList" class="facts-list"></div>
            </div>

            <!-- SECTION DETAIL VIEWS -->
            {section_views_html}

            <!-- STUDY PLAN VIEW -->
            <div class="view" id="view-study-plan">
                <h1>⏰ Study Time Allocation</h1>
                <p class="view-desc">Recommended hours per section. 40 days, ~2h/day for CA.</p>
                {_render_study_plan(time_alloc)}
            </div>

            <!-- BOOKMARKS VIEW -->
            <div class="view" id="view-bookmarks">
                <h1>⭐ Bookmarked Facts</h1>
                <p class="view-desc">Facts you bookmarked for quick revision. Stored in your browser.</p>
                <div id="bookmarksList" class="facts-list"></div>
                <p id="noBookmarks" style="display:none;color:#999;text-align:center;padding:40px;">No bookmarks yet. Click ☆ on any fact to bookmark it.</p>
            </div>

            <!-- SEARCH RESULTS VIEW -->
            <div class="view" id="view-search-results">
                <h1>🔍 Search Results</h1>
                <div id="searchResultsInfo" class="view-desc"></div>
                <div id="searchResultsList" class="facts-list"></div>
            </div>
        </main>
    </div>

    <button class="back-to-top" id="backToTop" onclick="window.scrollTo(0,0)" title="Back to top">↑</button>

    <script>
{_get_site_js()}
    </script>
</body>
</html>"""


def _e(text: str) -> str:
    return html_lib.escape(str(text))


def _section_icon(name: str) -> str:
    icons = {
        "Union Budget": "💰", "Economic Survey": "📊",
        "RBI & Monetary Policy": "🏦", "Banking & Finance": "🏛️",
        "Reports & Indices": "📈", "Government Schemes": "🏗️",
        "International Organizations & Summits": "🌍",
        "Financial Markets & Regulations": "📉",
        "Social Issues & Development": "👥", "Appointments & Awards": "🏆",
        "Agriculture & Rural Economy": "🌾", "External Sector & Trade": "🚢",
        "Insurance & Pension": "🛡️", "Science & Technology": "🔬",
        "Environment & Sustainability": "🌿", "Defence & Security": "⚔️",
        "Sports & Events": "🏅", "General": "📌",
    }
    return icons.get(name, "📌")


def _sidebar_nav_item(sec: dict, idx: int) -> str:
    priority_cls = sec["priority"].lower().replace(" ", "-")
    return f"""
            <div class="nav-item" onclick="showView('section-{idx}')" data-view="section-{idx}">
                <span class="nav-icon">{sec['icon']}</span>
                <span class="nav-label">{_e(sec['name'])}</span>
                <span class="nav-badge badge-{priority_cls}">{sec['facts']}</span>
            </div>"""


def _render_overview_cards(nav_sections: list[dict]) -> str:
    html = ""
    for sec in nav_sections:
        p = sec["priority"]
        cls = p.lower().replace(" ", "-")
        html += f"""
        <div class="ov-card ov-{cls}" onclick="showView('section-{nav_sections.index(sec)}')" style="cursor:pointer">
            <div class="ov-icon">{sec['icon']}</div>
            <div class="ov-name">{_e(sec['name'])}</div>
            <div class="ov-nums"><span>{sec['predicted']} expected</span> &bull; <span>{sec['facts']} facts</span> &bull; <span>{sec['questions']} MCQs</span></div>
            <span class="ov-badge badge-{cls}">{_e(p)}</span>
        </div>"""
    return html


def _render_month_pills(months: list[str]) -> str:
    all_months = ["January", "February", "March", "April", "May", "June"]
    html = ""
    for m in all_months:
        active = "mp-active" if m in months else "mp-missing"
        html += f'<span class="month-pill {active}">{m[:3]}</span>'
    return html


def _render_section_view(sec: dict, idx: int) -> str:
    icon = _section_icon(sec["name"])
    priority = sec.get("study_priority", "Medium")
    cls = priority.lower().replace(" ", "-")

    facts_html = ""
    for i, f in enumerate(sec.get("facts", [])[:50]):
        prob = f.get("probability_score", 0)
        imp = f.get("importance", "Medium")
        imp_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(imp, "⚪")
        month = f.get("month", "")
        facts_html += f"""
            <div class="fact-row" data-importance="{imp}" data-prob="{prob}">
                <span class="fact-bm" onclick="toggleBookmarkIdx(this, {i})" title="Bookmark">☆</span>
                <span class="fact-num">{i+1}.</span>
                <div class="fact-body">
                    <div class="fact-text">{_e(f.get('fact', ''))}</div>
                    <div class="fact-tags">
                        <span class="tag-imp">{imp_icon} {imp}</span>
                        <span class="tag-prob">📊 {prob}%</span>
                        {"<span class='tag-month'>📅 " + _e(month) + "</span>" if month else ""}
                    </div>
                    {"<div class='fact-why'>" + _e(f.get('why_it_matters', '')) + "</div>" if f.get('why_it_matters') else ""}
                </div>
            </div>"""

    mcqs_html = ""
    for i, q in enumerate(sec.get("questions", [])[:30]):
        options_html = ""
        for j, opt in enumerate(q.get("options", [])):
            is_correct = j == q.get("answer", 0)
            options_html += f'<div class="opt" data-correct="{str(is_correct).lower()}" onclick="checkOpt(this)">{_e(opt)}</div>'
        prob = q.get("probability_score", 0)
        mcqs_html += f"""
            <div class="mcq-card">
                <div class="mcq-head"><span>Q{i+1}</span><span class="mcq-prob-tag">{prob}%</span></div>
                <div class="mcq-text">{_e(q.get('question', ''))}</div>
                <div class="mcq-opts">{options_html}</div>
                <div class="mcq-expl" style="display:none">✅ <strong>Explanation:</strong> {_e(q.get('explanation', ''))}</div>
            </div>"""

    hist = sec.get("historical", {})
    hist_html = ""
    if hist:
        hist_html = f'<div class="hist-box">📚 Historical: Avg <strong>{hist.get("avg_count", "?")}</strong> Qs/year &bull; Consistency: <strong>{hist.get("consistency", "?")}%</strong> &bull; Trend: <strong>{hist.get("trend", "N/A")}</strong></div>'

    return f"""
            <div class="view" id="view-section-{idx}">
                <div class="section-title-bar sb-{cls}">
                    <h1>{icon} {_e(sec['name'])}</h1>
                    <div class="stb-meta">
                        <span class="stb-badge badge-{cls}">{_e(priority)}</span>
                        <span>📊 {sec['predicted_questions']} expected</span>
                        <span>📝 {sec['fact_count']} facts</span>
                        <span>❓ {sec['question_count']} MCQs</span>
                    </div>
                </div>
                {hist_html}
                <div class="sec-tabs">
                    <button class="sec-tab active" onclick="secTab(this, 'facts-{idx}')">📌 Key Facts</button>
                    <button class="sec-tab" onclick="secTab(this, 'mcqs-{idx}')">❓ Practice MCQs</button>
                </div>
                <div class="sec-panel active" id="panel-facts-{idx}">{facts_html if facts_html else '<p class="empty">No facts for this section yet.</p>'}</div>
                <div class="sec-panel" id="panel-mcqs-{idx}">{mcqs_html if mcqs_html else '<p class="empty">No MCQs for this section yet.</p>'}</div>
            </div>"""


def _render_study_plan(time_alloc: dict) -> str:
    if not time_alloc:
        return '<p class="empty">Run analysis first to get study recommendations.</p>'
    max_h = max(time_alloc.values()) if time_alloc else 1
    total = sum(time_alloc.values())
    html = '<div class="sp-chart">'
    for section, hours in sorted(time_alloc.items(), key=lambda x: x[1], reverse=True):
        pct = hours / max_h * 100
        html += f'<div class="sp-row"><span class="sp-label">{_e(section)}</span><div class="sp-bar-bg"><div class="sp-bar" style="width:{pct}%">{hours}h</div></div></div>'
    html += f'<div class="sp-total">Total: {round(total, 1)}h (~{round(total/40, 1)}h/day for 40 days)</div></div>'
    return html


def _readiness_message(score: float) -> str:
    if score >= 80: return "Excellent! Focus on revision and MCQ practice."
    elif score >= 60: return "Good progress. Fill the gaps in missing sections."
    elif score >= 40: return "Moderate. Upload more CA PDFs for better results."
    elif score >= 20: return "Getting started. Upload all 6 months for best results."
    return "Upload CA PDFs to begin analysis."


def _get_css() -> str:
    return """
        :root{--bg:#f0f2f5;--card:#fff;--text:#1a1a2e;--text2:#555;--border:#e0e0e0;--accent:#0d47a1;--accent2:#1565c0;--sidebar-bg:#fafbff;--sidebar-w:270px;--topbar-h:54px;--success:#43a047;--warning:#fb8c00;--danger:#e53935;--blue-light:#e3f2fd}
        body.dark{--bg:#121212;--card:#1e1e1e;--text:#e0e0e0;--text2:#aaa;--border:#333;--accent:#90caf9;--accent2:#64b5f6;--sidebar-bg:#1a1a2e;--blue-light:#1a237e}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text)}
        .topbar{position:fixed;top:0;left:0;right:0;height:var(--topbar-h);background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 16px;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.15)}
        .topbar-left{display:flex;align-items:center;gap:10px}
        .hamburger{background:none;border:none;color:#fff;font-size:22px;cursor:pointer;display:none;padding:4px 8px}
        .logo{font-size:24px}.site-title{font-size:15px;font-weight:700}
        .topbar-right{display:flex;align-items:center;gap:8px}
        .search-box{position:relative}
        .search-box input{width:260px;padding:7px 12px;border-radius:20px;border:none;font-size:13px;background:rgba(255,255,255,.2);color:#fff;outline:none}
        .search-box input::placeholder{color:rgba(255,255,255,.65)}
        .search-box input:focus{background:rgba(255,255,255,.3);width:320px;transition:width .3s}
        .search-count{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:11px;color:rgba(255,255,255,.7)}
        .mode-btn{background:rgba(255,255,255,.15);border:none;color:#fff;padding:5px 10px;border-radius:8px;cursor:pointer;font-size:12px}
        .mode-btn:hover{background:rgba(255,255,255,.3)}.mode-btn.active{background:var(--warning)}
        .layout{display:flex;margin-top:var(--topbar-h);min-height:calc(100vh - var(--topbar-h))}
        .sidebar{width:var(--sidebar-w);background:var(--sidebar-bg);border-right:1px solid var(--border);position:fixed;top:var(--topbar-h);bottom:0;left:0;overflow-y:auto;padding:12px 0;z-index:50;transition:transform .3s}
        .sidebar-header{padding:0 14px 10px;border-bottom:1px solid var(--border)}
        .sidebar-header h3{font-size:14px;color:var(--accent)}
        .sidebar-stats{font-size:11px;color:var(--text2);margin-top:3px}
        .nav-item{display:flex;align-items:center;gap:7px;padding:8px 14px;cursor:pointer;font-size:13px;transition:all .12s;border-left:3px solid transparent}
        .nav-item:hover{background:var(--blue-light)}.nav-item.active{background:var(--blue-light);border-left-color:var(--accent);font-weight:600}
        .nav-icon{font-size:15px;min-width:20px;text-align:center}.nav-label{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
        .nav-badge{font-size:10px;padding:1px 6px;border-radius:10px;color:#fff;font-weight:600}
        .badge-critical{background:var(--danger)}.badge-high{background:var(--warning)}.badge-medium{background:#1e88e5}.badge-low{background:#9e9e9e}
        .nav-divider{font-size:10px;font-weight:700;color:var(--text2);padding:12px 14px 3px;text-transform:uppercase;letter-spacing:1px}
        .sidebar-footer{padding:14px;border-top:1px solid var(--border);text-align:center}
        .progress-pct{font-size:26px;font-weight:800;display:block}.progress-label{font-size:11px;color:var(--text2)}
        .main-content{margin-left:var(--sidebar-w);flex:1;padding:24px 28px;max-width:1100px}
        .view{display:none}.view.active{display:block}
        .view h1{font-size:22px;color:var(--accent);margin-bottom:6px}
        .view-desc{color:var(--text2);font-size:13px;margin-bottom:16px}
        .stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
        .stat-card{background:var(--card);border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 5px rgba(0,0,0,.05);border-top:4px solid #ccc}
        .sc-blue{border-top-color:#1565c0}.sc-green{border-top-color:#43a047}.sc-orange{border-top-color:#fb8c00}.sc-red{border-top-color:#e53935}
        .sc-value{font-size:28px;font-weight:800}.sc-label{font-size:11px;color:var(--text2);margin-top:3px}
        .readiness-section{background:var(--card);border-radius:10px;padding:20px;box-shadow:0 1px 5px rgba(0,0,0,.05);margin-bottom:20px}
        .readiness-bar-track{background:#e8eaf6;border-radius:10px;height:30px;overflow:hidden;margin:10px 0}
        .readiness-bar-fill{height:100%;border-radius:10px;color:#fff;font-weight:700;font-size:13px;line-height:30px;padding:0 12px;min-width:45px;transition:width 1s}
        .readiness-msg{font-size:13px;color:var(--text2)}
        .overview-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
        .ov-card{background:var(--card);border-radius:10px;padding:12px;border-left:4px solid #ccc;transition:transform .15s;box-shadow:0 1px 4px rgba(0,0,0,.04)}
        .ov-card:hover{transform:translateY(-2px)}.ov-critical{border-left-color:var(--danger)}.ov-high{border-left-color:var(--warning)}.ov-medium{border-left-color:#1e88e5}.ov-low{border-left-color:#9e9e9e}
        .ov-icon{font-size:22px}.ov-name{font-weight:600;font-size:13px;margin:3px 0}.ov-nums{font-size:11px;color:var(--text2)}.ov-badge{display:inline-block;margin-top:5px}
        .month-pills{display:flex;gap:8px;flex-wrap:wrap}.month-pill{padding:5px 16px;border-radius:20px;font-size:12px;font-weight:600}
        .mp-active{background:#e8f5e9;color:#2e7d32;border:1px solid #a5d6a7}.mp-missing{background:#ffebee;color:#c62828;border:1px solid #ef9a9a}
        .filter-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;padding:10px 14px;background:var(--card);border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
        .filter-bar select{padding:5px 10px;border-radius:6px;border:1px solid var(--border);font-size:12px;background:var(--card);color:var(--text)}
        .facts-count{font-size:12px;color:var(--text2);margin-bottom:8px}
        .fact-row{display:flex;align-items:flex-start;gap:7px;padding:10px 12px;border-bottom:1px solid var(--border);transition:background .12s}
        .fact-row:hover{background:var(--blue-light)}
        .fact-bm{cursor:pointer;font-size:16px;color:#ccc;transition:color .2s;user-select:none}.fact-bm.bookmarked{color:#ffc107}
        .fact-num{font-weight:700;color:var(--accent);min-width:28px;font-size:13px}
        .fact-body{flex:1}.fact-text{font-size:13px;line-height:1.5}
        .fact-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:4px}
        .tag-imp{font-size:11px;font-weight:600}.tag-prob{font-size:10px;background:#e8eaf6;color:#283593;padding:1px 7px;border-radius:7px}
        .tag-month{font-size:10px;background:#e3f2fd;color:#1565c0;padding:1px 7px;border-radius:7px}
        .fact-why{font-size:11px;color:var(--text2);margin-top:3px;font-style:italic}
        .fact-row.hidden-reveal .fact-text{filter:blur(5px);cursor:pointer}.fact-row.hidden-reveal:hover .fact-text,.fact-row.revealed .fact-text{filter:none}
        .section-title-bar{padding:18px;border-radius:10px 10px 0 0;margin-bottom:2px;border-left:5px solid #ccc}
        .sb-critical{border-left-color:var(--danger);background:#fff5f5}.sb-high{border-left-color:var(--warning);background:#fff8e1}.sb-medium{border-left-color:#1e88e5;background:#e3f2fd}.sb-low{border-left-color:#9e9e9e;background:#fafafa}
        .stb-meta{display:flex;gap:12px;font-size:12px;color:var(--text2);margin-top:6px;flex-wrap:wrap}.stb-badge{font-size:11px}
        .hist-box{background:#fff3e0;padding:9px 14px;border-radius:7px;font-size:12px;margin-bottom:12px}
        .sec-tabs{display:flex;gap:4px;margin-bottom:12px}
        .sec-tab{padding:7px 16px;border:1px solid var(--border);border-radius:7px;background:var(--card);cursor:pointer;font-size:12px}
        .sec-tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
        .sec-panel{display:none}.sec-panel.active{display:block}
        .mcq-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.03)}
        .mcq-head{display:flex;justify-content:space-between;margin-bottom:6px}
        .mcq-head span:first-child{font-weight:700;color:var(--accent)}.mcq-prob-tag{font-size:11px;color:var(--text2)}
        .mcq-text{font-size:13px;font-weight:500;margin-bottom:10px;line-height:1.5}
        .mcq-opts{display:flex;flex-direction:column;gap:5px}
        .opt{padding:9px 12px;border:1px solid var(--border);border-radius:7px;cursor:pointer;font-size:12px;transition:all .2s}
        .opt:hover{background:var(--blue-light);border-color:#9fa8da}
        .opt.correct{background:#e8f5e9;border-color:var(--success);color:#2e7d32;font-weight:600}
        .opt.wrong{background:#ffebee;border-color:var(--danger);color:#c62828}
        .opt.show-correct{background:#e8f5e9;border-color:var(--success)}
        .mcq-expl{margin-top:8px;padding:9px;background:#f3e5f5;border-radius:7px;font-size:12px;color:#4a148c}
        .mcq-score-bar{background:var(--card);padding:9px 14px;border-radius:7px;font-size:13px;font-weight:600;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
        .revision-controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
        .rev-btn{padding:8px 18px;border-radius:8px;border:1px solid var(--border);background:var(--card);cursor:pointer;font-size:12px;font-weight:500}
        .rev-btn:hover{background:var(--blue-light)}
        .revision-stats{font-size:13px;margin-bottom:12px;padding:10px;background:var(--card);border-radius:8px}
        .sp-chart{max-width:650px}.sp-row{display:flex;align-items:center;gap:10px;margin:6px 0}
        .sp-label{min-width:190px;font-size:12px;font-weight:500;text-align:right}
        .sp-bar-bg{flex:1;background:#e8eaf6;border-radius:5px;height:22px;overflow:hidden}
        .sp-bar{height:100%;background:linear-gradient(90deg,#1565c0,#42a5f5);border-radius:5px;color:#fff;font-size:10px;font-weight:600;line-height:22px;padding:0 7px;min-width:28px}
        .sp-total{text-align:center;margin-top:12px;font-weight:600;color:var(--accent)}
        .empty{color:#999;text-align:center;padding:36px;font-style:italic}
        .back-to-top{position:fixed;bottom:20px;right:20px;width:40px;height:40px;border-radius:50%;background:var(--accent);color:#fff;border:none;font-size:18px;cursor:pointer;opacity:0;transition:opacity .3s;box-shadow:0 2px 8px rgba(0,0,0,.2);z-index:99}
        .back-to-top.visible{opacity:1}
        @media print{.topbar,.sidebar,.filter-bar,.mode-btn,.back-to-top,.search-box,.hamburger{display:none!important}.main-content{margin-left:0!important;padding:8px!important}.view{display:block!important;page-break-inside:avoid}.mcq-expl{display:block!important}.fact-row.hidden-reveal .fact-text{filter:none!important}}
        @media(max-width:900px){.hamburger{display:block}.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.main-content{margin-left:0;padding:14px}.stats-row{grid-template-columns:repeat(2,1fr)}.overview-grid{grid-template-columns:1fr}.search-box input{width:140px}.search-box input:focus{width:180px}.site-title{display:none}}
    """


def _get_site_js() -> str:
    return """
    let revisionMode=false,mcqScore={correct:0,total:0};
    function getBookmarks(){try{return JSON.parse(localStorage.getItem('ca_bm')||'{}')}catch(e){return{}}}
    function saveBookmarks(b){localStorage.setItem('ca_bm',JSON.stringify(b))}
    function getRevState(){try{return JSON.parse(localStorage.getItem('ca_rev')||'{}')}catch(e){return{}}}
    function saveRevState(r){localStorage.setItem('ca_rev',JSON.stringify(r))}

    function showView(id){
        document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
        var el=document.getElementById('view-'+id);if(el)el.classList.add('active');
        var nav=document.querySelector('.nav-item[data-view="'+id+'"]');if(nav)nav.classList.add('active');
        window.scrollTo(0,0);
        if(id==='bookmarks')showBookmarks();
        // Close sidebar on mobile
        document.getElementById('sidebar').classList.remove('open');
    }

    function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open')}

    function secTab(btn,panelId){
        var p=btn.closest('.view');
        p.querySelectorAll('.sec-tab').forEach(t=>t.classList.remove('active'));
        p.querySelectorAll('.sec-panel').forEach(p2=>p2.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('panel-'+panelId).classList.add('active');
    }

    function handleSearch(q){
        q=q.trim().toLowerCase();
        var sn=document.getElementById('searchNav');
        if(q.length<2){sn.style.display='none';document.getElementById('searchCount').textContent='';return}
        var mf=SITE_DATA.facts.filter(f=>f.fact.toLowerCase().includes(q)||f.category.toLowerCase().includes(q)||(f.why||'').toLowerCase().includes(q));
        var mq=SITE_DATA.questions.filter(x=>x.question.toLowerCase().includes(q)||(x.explanation||'').toLowerCase().includes(q));
        var tot=mf.length+mq.length;
        document.getElementById('searchCount').textContent=tot+' found';
        sn.style.display=tot>0?'':'none';
        var h='';
        if(mf.length){
            h+='<h3 style="margin:8px 0">📌 Facts ('+mf.length+')</h3>';
            mf.forEach(function(f,i){
                var imp={'High':'🔴','Medium':'🟡','Low':'🟢'}[f.importance]||'⚪';
                h+='<div class="fact-row"><span class="fact-num">'+(i+1)+'.</span><div class="fact-body"><div class="fact-text">'+hl(f.fact,q)+'</div><div class="fact-tags"><span class="tag-imp">'+imp+' '+f.importance+'</span><span class="tag-prob">📊 '+f.probability+'%</span><span class="tag-month">'+f.category+'</span></div></div></div>';
            });
        }
        if(mq.length){
            h+='<h3 style="margin:14px 0 8px">❓ Questions ('+mq.length+')</h3>';
            mq.forEach(function(x,i){
                h+='<div class="mcq-card"><div class="mcq-head"><span>Q'+(i+1)+'</span></div><div class="mcq-text">'+hl(x.question,q)+'</div><div class="mcq-opts">';
                x.options.forEach(function(o,j){h+='<div class="opt'+(j===x.answer?' show-correct':'')+'">'+o+'</div>'});
                h+='</div>';if(x.explanation)h+='<div class="mcq-expl" style="display:block">✅ '+x.explanation+'</div>';
                h+='</div>';
            });
        }
        document.getElementById('searchResultsInfo').textContent=tot+' results for "'+q+'"';
        document.getElementById('searchResultsList').innerHTML=h;
        showView('search-results');
    }
    function hl(t,q){if(!q)return t;return t.replace(new RegExp('('+q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','gi'),'<mark>$1</mark>')}

    function renderTop50(facts){
        var list=document.getElementById('top50List');
        if(!facts)facts=SITE_DATA.facts.slice().sort(function(a,b){return b.probability-a.probability}).slice(0,50);
        var h='';
        facts.forEach(function(f,i){
            var imp={'High':'🔴','Medium':'🟡','Low':'🟢'}[f.importance]||'⚪';
            h+='<div class="fact-row" data-importance="'+f.importance+'" data-category="'+f.category+'"><span class="fact-bm" onclick="bmByIdx(this,'+i+')" title="Bookmark">☆</span><span class="fact-num">'+(i+1)+'.</span><div class="fact-body"><div class="fact-text">'+f.fact+'</div><div class="fact-tags"><span class="tag-imp">'+imp+' '+f.importance+'</span><span class="tag-prob">📊 '+f.probability+'%</span><span class="tag-month">'+f.category+'</span>'+(f.month?'<span class="tag-month">📅 '+f.month+'</span>':'')+'</div>'+(f.why?'<div class="fact-why">'+f.why+'</div>':'')+'</div></div>';
        });
        list.innerHTML=h;restoreBm();
    }
    function filterTop50(){
        var imp=document.getElementById('top50ImpFilter').value,cat=document.getElementById('top50CatFilter').value;
        var f=SITE_DATA.facts.slice().sort(function(a,b){return b.probability-a.probability}).slice(0,50);
        if(imp)f=f.filter(function(x){return x.importance===imp});
        if(cat)f=f.filter(function(x){return x.category===cat});
        renderTop50(f);
    }

    function renderFacts(facts){
        var list=document.getElementById('factsList');
        if(!facts)facts=SITE_DATA.facts;
        document.getElementById('factsCount').textContent='Showing '+facts.length+' of '+SITE_DATA.facts.length+' facts';
        var h='';
        facts.forEach(function(f,i){
            var imp={'High':'🔴','Medium':'🟡','Low':'🟢'}[f.importance]||'⚪';
            h+='<div class="fact-row" data-importance="'+f.importance+'"><span class="fact-bm" onclick="bmByIdx(this,'+i+')" title="Bookmark">☆</span><span class="fact-num">'+(i+1)+'.</span><div class="fact-body"><div class="fact-text">'+f.fact+'</div><div class="fact-tags"><span class="tag-imp">'+imp+' '+f.importance+'</span><span class="tag-prob">📊 '+f.probability+'%</span><span class="tag-month">'+f.category+'</span>'+(f.month?'<span class="tag-month">📅 '+f.month+'</span>':'')+'</div>'+(f.why?'<div class="fact-why">'+f.why+'</div>':'')+'</div></div>';
        });
        list.innerHTML=h;restoreBm();
    }
    function filterFacts(){
        var imp=document.getElementById('factsImpFilter').value,cat=document.getElementById('factsCatFilter').value,
            month=document.getElementById('factsMonthFilter').value,sort=document.getElementById('factsSortBy').value;
        var f=SITE_DATA.facts.slice();
        if(imp)f=f.filter(function(x){return x.importance===imp});
        if(cat)f=f.filter(function(x){return x.category===cat});
        if(month)f=f.filter(function(x){return x.month===month});
        if(sort==='probability')f.sort(function(a,b){return b.probability-a.probability});
        else if(sort==='category')f.sort(function(a,b){return a.category.localeCompare(b.category)});
        else if(sort==='month')f.sort(function(a,b){return(a.month||'').localeCompare(b.month||'')});
        else if(sort==='importance'){var o={'High':0,'Medium':1,'Low':2};f.sort(function(a,b){return(o[a.importance]||9)-(o[b.importance]||9)})}
        renderFacts(f);
    }

    function renderMcqs(qs){
        var list=document.getElementById('mcqsList');if(!qs)qs=SITE_DATA.questions;
        mcqScore={correct:0,total:0};updateScore();
        var h='';
        qs.forEach(function(q,i){
            h+='<div class="mcq-card"><div class="mcq-head"><span>Q'+(i+1)+'</span><span class="mcq-prob-tag">'+q.probability+'% • '+q.category+'</span></div><div class="mcq-text">'+q.question+'</div><div class="mcq-opts">';
            q.options.forEach(function(o,j){h+='<div class="opt" data-correct="'+(j===q.answer)+'" onclick="checkOpt(this)">'+o+'</div>'});
            h+='</div><div class="mcq-expl" style="display:none">✅ <strong>Explanation:</strong> '+(q.explanation||'')+'</div></div>';
        });
        list.innerHTML=h;
    }
    function filterMcqs(){
        var cat=document.getElementById('mcqsCatFilter').value,imp=document.getElementById('mcqsImpFilter').value;
        var q=SITE_DATA.questions.slice();
        if(cat)q=q.filter(function(x){return x.category===cat});
        if(imp)q=q.filter(function(x){return x.importance===imp});
        renderMcqs(q);
    }
    function resetAllMcqs(){renderMcqs()}

    function checkOpt(el){
        var p=el.closest('.mcq-opts');if(p.classList.contains('answered'))return;
        p.classList.add('answered');mcqScore.total++;
        if(el.getAttribute('data-correct')==='true'){el.classList.add('correct');mcqScore.correct++}
        else{el.classList.add('wrong');p.querySelectorAll('.opt').forEach(function(o){if(o.getAttribute('data-correct')==='true')o.classList.add('show-correct')})}
        el.closest('.mcq-card').querySelector('.mcq-expl').style.display='block';
        updateScore();
    }
    function updateScore(){
        document.getElementById('mcqCorrect').textContent=mcqScore.correct;
        document.getElementById('mcqTotal').textContent=mcqScore.total;
        document.getElementById('mcqPct').textContent=mcqScore.total>0?Math.round(mcqScore.correct/mcqScore.total*100):0;
    }

    function bmByIdx(el,idx){var b=getBookmarks(),k='f_'+idx;if(b[k]){delete b[k];el.textContent='☆';el.classList.remove('bookmarked')}else{b[k]=true;el.textContent='★';el.classList.add('bookmarked')}saveBookmarks(b)}
    function toggleBookmarkIdx(el,idx){bmByIdx(el,idx)}
    function restoreBm(){var b=getBookmarks();document.querySelectorAll('.fact-bm').forEach(function(el){var m=(el.getAttribute('onclick')||'').match(/(\\d+)/);if(m&&b['f_'+m[1]]){el.textContent='★';el.classList.add('bookmarked')}})}
    function showBookmarks(){
        var b=getBookmarks(),keys=Object.keys(b),list=document.getElementById('bookmarksList'),no=document.getElementById('noBookmarks');
        if(!keys.length){list.innerHTML='';no.style.display='block';return}no.style.display='none';
        var sf=SITE_DATA.facts.slice().sort(function(a,b2){return b2.probability-a.probability}),h='',c=0;
        sf.forEach(function(f,i){if(b['f_'+i]){c++;var imp={'High':'🔴','Medium':'🟡','Low':'🟢'}[f.importance]||'⚪';
        h+='<div class="fact-row"><span class="fact-bm bookmarked" onclick="bmByIdx(this,'+i+')">★</span><span class="fact-num">'+c+'.</span><div class="fact-body"><div class="fact-text">'+f.fact+'</div><div class="fact-tags"><span class="tag-imp">'+imp+' '+f.importance+'</span><span class="tag-prob">📊 '+f.probability+'%</span><span class="tag-month">'+f.category+'</span></div></div></div>'}});
        list.innerHTML=h;
    }

    function toggleRevisionMode(){revisionMode=!revisionMode;document.getElementById('revisionBtn').classList.toggle('active',revisionMode);
        document.querySelectorAll('.mcq-expl').forEach(function(e){e.style.display='none'});
        document.querySelectorAll('.mcq-opts').forEach(function(o){o.classList.remove('answered')});
        document.querySelectorAll('.opt').forEach(function(o){o.classList.remove('correct','wrong','show-correct')})}

    function startRevision(mode){
        var facts=SITE_DATA.facts.slice().sort(function(a,b){return b.probability-a.probability}),rs=getRevState();
        if(mode==='high')facts=facts.filter(function(f){return f.importance==='High'});
        else if(mode==='bookmarked'){var bm=getBookmarks();facts=facts.filter(function(f,i){return bm['f_'+i]})}
        else if(mode==='weak')facts=facts.filter(function(f,i){return rs['f_'+i]==='weak'});
        var list=document.getElementById('revisionList'),stats=document.getElementById('revisionStats');
        stats.innerHTML='Total: '+facts.length+' facts. Click to reveal, then mark as ✅ Remembered or ❌ Need revision.';
        var h='';
        facts.forEach(function(f,i){var imp={'High':'🔴','Medium':'🟡','Low':'🟢'}[f.importance]||'⚪';
            h+='<div class="fact-row hidden-reveal" onclick="revealFact(this)"><span class="fact-num">'+(i+1)+'.</span><div class="fact-body"><div class="fact-text">'+f.fact+'</div><div class="fact-tags" style="display:none"><span class="tag-imp">'+imp+' '+f.importance+'</span><span class="tag-prob">📊 '+f.probability+'%</span><span class="tag-month">'+f.category+'</span></div><div class="rev-actions" style="display:none;margin-top:6px"><button class="rev-btn" onclick="markRev(event,'+i+',\\'ok\\')" style="background:#e8f5e9">✅ Remembered</button> <button class="rev-btn" onclick="markRev(event,'+i+',\\'weak\\')" style="background:#ffebee">❌ Revise Again</button></div></div></div>';
        });
        list.innerHTML=h;
    }
    function revealFact(el){el.classList.remove('hidden-reveal');el.classList.add('revealed');el.querySelector('.fact-tags').style.display='flex';var a=el.querySelector('.rev-actions');if(a)a.style.display='block'}
    function markRev(e,idx,status){e.stopPropagation();var rs=getRevState();rs['f_'+idx]=status;saveRevState(rs);var el=e.target.closest('.fact-row');el.style.opacity=status==='ok'?'0.4':'1';el.style.borderLeft=status==='ok'?'4px solid #43a047':'4px solid #e53935'}

    function toggleDarkMode(){document.body.classList.toggle('dark');localStorage.setItem('ca_dark',document.body.classList.contains('dark')?'1':'0')}

    document.addEventListener('DOMContentLoaded',function(){
        if(localStorage.getItem('ca_dark')==='1')document.body.classList.add('dark');
        var cats=[...new Set(SITE_DATA.facts.map(function(f){return f.category}))].sort();
        var months=[...new Set(SITE_DATA.facts.map(function(f){return f.month}).filter(Boolean))].sort();
        ['top50CatFilter','factsCatFilter','mcqsCatFilter'].forEach(function(id){
            var sel=document.getElementById(id);if(sel)cats.forEach(function(c){var o=document.createElement('option');o.value=c;o.textContent=c;sel.appendChild(o)})});
        var ms=document.getElementById('factsMonthFilter');
        if(ms)months.forEach(function(m){var o=document.createElement('option');o.value=m;o.textContent=m;ms.appendChild(o)});
        renderTop50();renderFacts();renderMcqs();
        window.addEventListener('scroll',function(){document.getElementById('backToTop').classList.toggle('visible',window.scrollY>400)});
    });
    """
