"""
Exam Paper Analyzer Pro — Streamlit Web App
Analyze previous year exam papers, study current affairs,
practice with quizzes, and predict high-probability topics.
Enhanced with RBI Grade B deep-dive for AIR 1 preparation.
"""
import json
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    Question, CategorizedQuestion, Difficulty,
    EXAM_TYPES, PHASE_OPTIONS, SECTION_OPTIONS, CategorizationMethod,
)
from parsers.pdf_parser import extract_text_from_pdf, split_into_questions
from parsers.text_parser import parse_text_input, parse_csv_input
from categorizers.rule_categorizer import RuleCategorizer
from categorizers.ai_categorizer import AICategorizer
from analyzers.frequency import build_frequency_matrix, build_section_summary, get_top_topics
from analyzers.trends import analyze_trends
from analyzers.predictor import (
    predict_topic_distribution,
    generate_sample_questions_template,
    generate_sample_questions_ai,
)
from exporters.excel_export import export_to_excel
from exporters.html_export import export_to_html
from exporters.pdf_export import export_to_pdf
from data.current_affairs import (
    get_ca_categories, get_key_facts, get_practice_mcqs,
    get_all_mcq_count, get_study_plan, STUDY_PLANS,
)
from data.rbi_grade_b import (
    get_countdown, get_exam_pattern, get_cutoffs, get_air1_targets,
    get_rbi_governors, get_rbi_committees, get_important_acts,
    get_esi_topics, get_fm_topics, get_phase2_mcqs, get_all_phase2_mcq_count,
    get_last30_plan, get_topper_tips, get_quant_shortcuts,
)
from generators.ca_question_generator import generate_ca_questions_from_pdfs, extract_facts_from_pdfs
from generators.question_generator import generate_mock_test_questions
from exporters.mock_test_export import export_mock_test_pdf
from analyzers.ca_pattern_analyzer import (
    analyze_pyq_paper, aggregate_pyq_patterns, get_category_weights,
    load_ca_taxonomy, classify_question_to_ca_category,
)
from analyzers.ca_predictor import run_predictive_analysis
from exporters.ca_html_report import export_ca_predictions_html
from storage.local_store import (
    init_storage, save_ca_extracted, load_all_ca_extracted,
    save_pyq_pattern, load_all_pyq_patterns, delete_pyq_pattern,
    save_analysis_results, load_analysis_results,
    save_report, load_upload_manifest, save_upload_record,
    save_full_state, load_full_state, get_storage_summary,
    delete_ca_extracted,
)
from config import CA_MONTHS, CA_SECTIONS, CA_DOCUMENTS_DIR, PYQ_DOCUMENTS_DIR
from deployer.github_pages import init_site_repo, deploy_site, get_site_status
from exporters.ca_site_builder import build_github_pages_site
from utils.document_scanner import scan_ca_folder, scan_pyq_folder, get_scan_summary
from utils.batch_processor import batch_process_ca, batch_process_pyq

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Exam Analyzer Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem; border-radius: 16px; color: white;
        margin-bottom: 1.5rem; text-align: center;
    }
    .hero h1 { font-size: 2.2rem; margin-bottom: 0.3rem; font-weight: 700; }
    .hero p { font-size: 1.05rem; opacity: 0.92; margin: 0; }
    .feature-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem; margin: 1.5rem 0;
    }
    .feature-card {
        background: white; border: 1px solid #e8ecf1; border-radius: 12px;
        padding: 1.3rem; text-align: center;
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .feature-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }
    .feature-card .icon { font-size: 2.4rem; margin-bottom: 0.6rem; }
    .feature-card h3 { margin: 0 0 0.4rem 0; font-size: 1rem; color: #1a1a2e; }
    .feature-card p { margin: 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4; }
    .stat-row {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.8rem; margin-bottom: 1rem;
    }
    .stat-card {
        background: white; border-radius: 10px; padding: 1rem; text-align: center;
        border-left: 4px solid #667eea; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .stat-card .value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; }
    .stat-card .label { font-size: 0.82rem; color: #6c757d; margin-top: 2px; }
    .countdown-box {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        border-radius: 14px; padding: 1.2rem; color: white; text-align: center;
        margin-bottom: 1rem;
    }
    .countdown-box .days { font-size: 2.5rem; font-weight: 800; color: #ffeb3b; }
    .countdown-box .label { font-size: 0.85rem; opacity: 0.9; }
    .ca-card {
        background: white; border-radius: 12px; padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem; border-left: 5px solid #667eea;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .ca-card:hover { box-shadow: 0 3px 15px rgba(0,0,0,0.1); }
    .ca-card h4 { margin: 0 0 0.3rem 0; color: #1a1a2e; }
    .ca-card .meta { font-size: 0.82rem; color: #6c757d; }
    .quiz-correct { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; }
    .quiz-wrong { background: #ffebee; border-left: 4px solid #f44336; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; }
    .tip-box {
        background: #f0f4ff; border: 1px solid #c5cae9; border-radius: 10px;
        padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.92rem;
    }
    .tip-box strong { color: #3949ab; }
    .air1-box {
        background: linear-gradient(135deg, #ffd54f22, #ff6f0022);
        border: 2px solid #ff8f00; border-radius: 12px;
        padding: 1rem 1.2rem; margin: 0.8rem 0;
    }
    .cutoff-card {
        background: white; border-radius: 10px; padding: 0.8rem 1rem;
        border-left: 4px solid #e53935; margin-bottom: 0.5rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .governor-card {
        background: white; border-radius: 8px; padding: 0.6rem 1rem;
        margin-bottom: 0.4rem; border-left: 3px solid #1565c0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    [data-testid="stSidebar"] { background-color: #fafbfd; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
_defaults = {
    "all_questions": [], "categorized": [], "predictions": [],
    "sample_questions": {}, "processed": False,
    "quiz_answered": {},
    "ca_generated_mcqs": [],
    "mock_test_questions": [],
    # CA Predictor state
    "ca_pred_facts": [],
    "ca_pred_questions": [],
    "ca_pred_analysis": None,
    "ca_pred_pyq_patterns": [],
    "ca_pred_html": None,
    "ca_pred_loaded": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Auto-load persisted data from C: drive on first run
if not st.session_state.ca_pred_loaded:
    init_storage()
    _saved = load_full_state()
    if _saved:
        for _k in ["ca_pred_facts", "ca_pred_questions", "ca_pred_pyq_patterns"]:
            if _k in _saved:
                st.session_state[_k] = _saved[_k]
    _saved_analysis = load_analysis_results()
    if _saved_analysis:
        st.session_state.ca_pred_analysis = _saved_analysis
    _saved_pyqs = load_all_pyq_patterns()
    if _saved_pyqs:
        st.session_state.ca_pred_pyq_patterns = _saved_pyqs
    st.session_state.ca_pred_loaded = True


def load_taxonomy(exam_type: str) -> dict:
    taxonomy_map = {
        "RBI Grade B": "rbi_grade_b.json", "SEBI Grade A": "sebi_grade_a.json",
        "NABARD Grade A": "nabard_grade_a.json",
        "IBPS PO": "banking_generic.json", "IBPS Clerk": "banking_generic.json",
        "SBI PO": "banking_generic.json", "SBI Clerk": "banking_generic.json",
    }
    filename = taxonomy_map.get(exam_type, "banking_generic.json")
    taxonomy_path = Path(__file__).parent / "data" / "taxonomies" / filename
    if taxonomy_path.exists():
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"exam_name": exam_type, "sections": []}


# ═════════════════════════════════════════════════════════════════════════════
# PROCESSING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def _get_provider(method: str) -> str:
    if "OpenAI" in method:
        return "openai"
    elif "Gemini" in method:
        return "gemini"
    elif "Ollama" in method:
        return "ollama"
    return "openai"


def _categorize_all(questions, exam_type, method, api_key, model_name):
    taxonomy = load_taxonomy(exam_type)
    if method == CategorizationMethod.RULE_BASED.value:
        cat = RuleCategorizer(taxonomy)
        result = cat.categorize_batch(questions)
    else:
        provider = _get_provider(method)
        try:
            cat = AICategorizer(taxonomy, provider, api_key, model_name)
            result = cat.categorize_batch(questions)
        except Exception as e:
            st.warning(f"AI failed ({e}). Using rule-based fallback.")
            cat = RuleCategorizer(taxonomy)
            result = cat.categorize_batch(questions)
    st.session_state.categorized = result
    st.session_state.processed = True


def _process_files(file_metadata, exam_type, method, api_key, model_name):
    all_q = list(st.session_state.all_questions)
    progress = st.progress(0, text="Preparing...")
    for i, meta in enumerate(file_metadata):
        f, year, phase = meta["file"], meta["year"], meta["phase"]
        progress.progress((i + 1) / (len(file_metadata) + 1), text=f"Parsing {f.name}...")
        try:
            fb = f.read()
            if f.name.lower().endswith(".pdf"):
                text = extract_text_from_pdf(fb)
                qs = split_into_questions(text, year, phase, exam_type)
            elif f.name.lower().endswith(".csv"):
                qs = parse_csv_input(fb, year, phase, exam_type)
            else:
                qs = parse_text_input(fb.decode("utf-8", errors="replace"), year, phase, exam_type)
            all_q.extend(qs)
            st.toast(f"Done: {f.name}: {len(qs)} questions")
        except Exception as e:
            st.error(f"Error: {f.name}: {e}")
    progress.progress(0.95, text="Categorizing...")
    st.session_state.all_questions = all_q
    _categorize_all(all_q, exam_type, method, api_key, model_name)
    progress.progress(1.0, text="Done!")
    st.rerun()


def _process_text(text, year, phase, exam_type, method, api_key, model_name):
    with st.spinner("Parsing and categorizing..."):
        qs = parse_text_input(text, year, phase, exam_type)
        all_q = list(st.session_state.all_questions) + qs
        st.session_state.all_questions = all_q
        st.toast(f"Done: {len(qs)} questions parsed")
        _categorize_all(all_q, exam_type, method, api_key, model_name)
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Exam Analyzer Pro")
    st.caption("AIR 1 preparation companion")
    st.markdown("---")

    exam_type = st.selectbox(
        "📋 Exam Type", EXAM_TYPES, index=0,
        help="Select your target exam to load the correct topic taxonomy",
    )
    phases = PHASE_OPTIONS.get(exam_type, ["Phase 1", "Phase 2"])

    # Countdown timer — show for RBI Grade B
    if exam_type == "RBI Grade B":
        cd = get_countdown()
        phase1_days = cd["phase1"]
        phase2_days = cd["phase2"]
        notif_days = cd["notification"]

        if notif_days > 0:
            st.markdown(f"""
            <div class="countdown-box">
                <div class="label">Notification in</div>
                <div class="days">{notif_days}</div>
                <div class="label">days ({cd['notification_date']})</div>
            </div>
            """, unsafe_allow_html=True)

        if phase1_days > 0:
            st.markdown(f"""
            <div class="countdown-box" style="background: linear-gradient(135deg, #b71c1c 0%, #c62828 100%);">
                <div class="label">Phase 1 in</div>
                <div class="days">{phase1_days}</div>
                <div class="label">days (~{cd['phase1_date']})</div>
            </div>
            """, unsafe_allow_html=True)

        if phase2_days > 0:
            st.markdown(f"""
            <div class="countdown-box" style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);">
                <div class="label">Phase 2 in</div>
                <div class="days">{phase2_days}</div>
                <div class="label">days (~{cd['phase2_date']})</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("⚙️ AI Settings", expanded=False):
        method = st.selectbox(
            "Categorization Method",
            [m.value for m in CategorizationMethod], index=0,
            help="Rule-based = free & offline. AI = more accurate, needs API key.",
        )
        api_key = ""
        model_name = ""
        if method != CategorizationMethod.RULE_BASED.value:
            api_key = st.text_input(
                "API Key" if method != CategorizationMethod.OLLAMA.value else "Ollama URL",
                type="password" if method != CategorizationMethod.OLLAMA.value else "default",
                value="" if method != CategorizationMethod.OLLAMA.value else "http://localhost:11434",
            )
            model_name = st.text_input("Model (optional)", placeholder="Leave blank for default")

    st.markdown("---")
    q_count = len(st.session_state.all_questions)
    if q_count > 0:
        st.success(f"📦 {q_count} questions loaded")
    else:
        st.info("📭 No papers uploaded yet")


# ═════════════════════════════════════════════════════════════════════════════
# TABS — add RBI Grade B tab when that exam is selected
# ═════════════════════════════════════════════════════════════════════════════
if exam_type == "RBI Grade B":
    tab_home, tab_rbi, tab_upload, tab_dashboard, tab_ca, tab_ca_pred, tab_quiz, tab_predictions, tab_mock, tab_study, tab_export = st.tabs([
        "🏠 Home", "🏦 RBI Grade B", "📁 Upload", "📈 Dashboard", "📰 Current Affairs",
        "🔮 CA Predictor", "❓ Quiz", "📊 Predictions", "📝 Mock Test", "📖 Study Plan", "💾 Export",
    ])
else:
    tab_rbi = None
    tab_home, tab_upload, tab_dashboard, tab_ca, tab_ca_pred, tab_quiz, tab_predictions, tab_mock, tab_study, tab_export = st.tabs([
        "🏠 Home", "📁 Upload", "📈 Dashboard", "📰 Current Affairs",
        "🔮 CA Predictor", "❓ Quiz", "📊 Predictions", "📝 Mock Test", "📖 Study Plan", "💾 Export",
    ])


# ═════════════════════════════════════════════════════════════════════════════
# TAB: HOME
# ═════════════════════════════════════════════════════════════════════════════
with tab_home:
    st.markdown("""
    <div class="hero">
        <h1>🎯 Exam Analyzer Pro</h1>
        <p>Analyze previous year papers &bull; Predict high-probability topics &bull; Master current affairs</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="icon">📁</div><h3>Upload Papers</h3>
            <p>Upload PDFs or paste text from the last 5+ years of previous year papers</p>
        </div>
        <div class="feature-card">
            <div class="icon">🤖</div><h3>Auto-Categorize</h3>
            <p>AI or keyword engine maps every question to section, topic, sub-topic</p>
        </div>
        <div class="feature-card">
            <div class="icon">📊</div><h3>Smart Dashboard</h3>
            <p>Frequency heatmaps, trend lines, probability rankings, difficulty analysis</p>
        </div>
        <div class="feature-card">
            <div class="icon">📰</div><h3>Current Affairs</h3>
            <p>Topic-wise key facts, one-liners & practice MCQs for banking exams</p>
        </div>
        <div class="feature-card">
            <div class="icon">❓</div><h3>Practice Quiz</h3>
            <p>Test yourself with MCQs on banking, economy, RBI, and financial awareness</p>
        </div>
        <div class="feature-card">
            <div class="icon">🔮</div><h3>Predictions</h3>
            <p>See most likely topics with probability scores & sample questions</p>
        </div>
        <div class="feature-card">
            <div class="icon">🏦</div><h3>RBI Grade B</h3>
            <p>Deep-dive: exam pattern, cutoffs, AIR 1 strategy, Phase 2 ESI + FM, committees, acts</p>
        </div>
        <div class="feature-card">
            <div class="icon">💾</div><h3>Export Reports</h3>
            <p>Download Excel, HTML dashboard, or PDF report</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    <div class="tip-box">
        <strong>Step 1:</strong> Select your exam in the sidebar (e.g., RBI Grade B)<br>
        <strong>Step 2:</strong> Go to <strong>📁 Upload</strong> and upload PDFs or paste questions<br>
        <strong>Step 3:</strong> Click <strong>Process</strong> — auto-categorization happens instantly<br>
        <strong>Step 4:</strong> Explore <strong>📈 Dashboard</strong> for analysis & <strong>🔮 Predictions</strong> for forecasts<br>
        <strong>Bonus:</strong> Use <strong>📰 Current Affairs</strong>, <strong>❓ Quiz</strong>, and <strong>🏦 RBI Grade B</strong> anytime — no upload needed!
    </div>
    """, unsafe_allow_html=True)

    total_mcqs = get_all_mcq_count() + get_all_phase2_mcq_count()
    ca_cats = get_ca_categories()
    total_facts = sum(len(get_key_facts(c)) for c in ca_cats)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="value">{len(EXAM_TYPES)-1}</div><div class="label">Exams Supported</div></div>
        <div class="stat-card"><div class="value">{len(ca_cats)}</div><div class="label">CA Topics</div></div>
        <div class="stat-card"><div class="value">{total_facts}+</div><div class="label">Key Facts</div></div>
        <div class="stat-card"><div class="value">{total_mcqs}+</div><div class="label">Practice MCQs</div></div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB: RBI GRADE B (only when exam_type == "RBI Grade B")
# ═════════════════════════════════════════════════════════════════════════════
if tab_rbi is not None:
  with tab_rbi:
    st.markdown("""
    <div class="hero" style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);">
        <h1>🏦 RBI Grade B — AIR 1 Command Center</h1>
        <p>Everything you need to crack RBI Grade B with the top rank</p>
    </div>
    """, unsafe_allow_html=True)

    # Countdown at top
    cd = get_countdown()
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card" style="border-left-color: #ff8f00;"><div class="value">{max(0, cd['notification'])}</div><div class="label">Days to Notification<br>{cd['notification_date']}</div></div>
        <div class="stat-card" style="border-left-color: #c62828;"><div class="value">{max(0, cd['phase1'])}</div><div class="label">Days to Phase 1<br>~{cd['phase1_date']}</div></div>
        <div class="stat-card" style="border-left-color: #2e7d32;"><div class="value">{max(0, cd['phase2'])}</div><div class="label">Days to Phase 2<br>~{cd['phase2_date']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Sub-tabs within RBI tab
    rbi_sub = st.radio(
        "Section:", [
            "📋 Exam Pattern", "🎯 AIR 1 Strategy", "📊 Cut-off Analysis",
            "📚 Phase 2: ESI", "📚 Phase 2: FM", "❓ Phase 2 MCQs",
            "👤 RBI Governors", "📜 Committees", "⚖️ Important Acts",
            "🧮 Quant Shortcuts", "📅 Last 30 Days Plan", "💡 Topper Tips",
        ], horizontal=True, label_visibility="collapsed",
    )

    # ── EXAM PATTERN ──
    if rbi_sub == "📋 Exam Pattern":
        pattern = get_exam_pattern()
        st.markdown("### Phase 1 — Online Objective")
        p1 = pattern["Phase 1"]
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Total Marks", p1["total_marks"])
        with c2: st.metric("Questions", p1["total_questions"])
        with c3: st.metric("Duration", f"{p1['duration_minutes']} min")
        with c4: st.metric("Negative", f"-{p1['negative_marking']}")

        st.info(p1["qualification_note"])

        for sec in p1["sections"]:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                with c1: st.markdown(f"**{sec['name']}**")
                with c2: st.metric("Qs", sec["questions"])
                with c3: st.metric("Marks", sec["marks"])
                with c4: st.metric("Time", f"{sec['time_suggested']}m")
                st.caption(f"Cutoff range: {sec['cutoff_range']} | Strategy: {sec['strategy']}")

        st.markdown("---")
        st.markdown("### Phase 2 — Descriptive + Objective")
        p2 = pattern["Phase 2"]
        st.info(p2["final_merit"])
        for paper in p2["papers"]:
            with st.expander(f"📄 {paper['name']} ({paper['marks']} marks, {paper['duration_minutes']} min)"):
                if "key_topics" in paper:
                    for t in paper["key_topics"]:
                        st.markdown(f"- {t}")
                if "components" in paper:
                    for comp in paper["components"]:
                        st.markdown(f"**{comp['name']}** — {comp['marks']} marks")
                        if "tip" in comp:
                            st.caption(f"Tip: {comp['tip']}")

    # ── AIR 1 STRATEGY ──
    elif rbi_sub == "🎯 AIR 1 Strategy":
        targets = get_air1_targets()

        st.markdown("### 🎯 Phase 1 — Target: " + targets["Phase 1"]["target_score"])
        st.markdown("""
        <div class="air1-box">
            <strong>🏆 AIR 1 Formula:</strong> Accuracy > Attempts. Target 160+ by attempting 165-175 questions with 90%+ accuracy.
            The top rankers don't attempt everything — they attempt smart.
        </div>
        """, unsafe_allow_html=True)

        for sec_name, sec in targets["Phase 1"]["sections"].items():
            with st.expander(f"📌 {sec_name} — Target: {sec['target_score']}", expanded=True):
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Attempts", sec["target_attempts"])
                with c2: st.metric("Accuracy", sec["target_accuracy"])
                with c3: st.metric("Time", f"{sec['time_minutes']} min")
                st.markdown("**Key Strategies:**")
                for s in sec["key_strategy"]:
                    st.markdown(f"- {s}")

        st.markdown("---")
        st.markdown("### 📋 Exam Day Routine")
        for i, step in enumerate(targets["Phase 1"]["exam_day_routine"], 1):
            st.markdown(f"**{i}.** {step}")

        st.markdown("---")
        st.markdown("### 🎯 Phase 2 — Target: " + targets["Phase 2"]["target_score"])
        for paper_key, paper in targets["Phase 2"]["papers"].items():
            with st.expander(f"📄 {paper_key} — Target: {paper['target_score']}"):
                for s in paper["key_strategy"]:
                    st.markdown(f"- {s}")

    # ── CUT-OFF ANALYSIS ──
    elif rbi_sub == "📊 Cut-off Analysis":
        st.markdown("### 📊 Phase 1 Historical Cut-offs (General Category)")
        cutoffs = get_cutoffs()

        # Table
        rows = []
        for year in sorted(cutoffs.keys(), reverse=True):
            c = cutoffs[year]
            rows.append({
                "Year": year, "Overall": c["overall"],
                "GA": c["ga"], "Quant": c["quant"],
                "English": c["english"], "Reasoning": c["reasoning"],
                "Vacancies": c["vacancies"],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Chart
        import plotly.graph_objects as go
        fig = go.Figure()
        years = sorted(cutoffs.keys())
        fig.add_trace(go.Scatter(x=years, y=[cutoffs[y]["overall"] for y in years], mode="lines+markers", name="Overall", line=dict(width=3, color="#e53935")))
        fig.add_trace(go.Bar(x=years, y=[cutoffs[y]["ga"] for y in years], name="GA", marker_color="#1565c0", opacity=0.7))
        fig.add_trace(go.Bar(x=years, y=[cutoffs[y]["reasoning"] for y in years], name="Reasoning", marker_color="#2e7d32", opacity=0.7))
        fig.add_trace(go.Bar(x=years, y=[cutoffs[y]["quant"] for y in years], name="Quant", marker_color="#ff8f00", opacity=0.7))
        fig.add_trace(go.Bar(x=years, y=[cutoffs[y]["english"] for y in years], name="English", marker_color="#6a1b9a", opacity=0.7))
        fig.update_layout(
            height=450, barmode="group", xaxis_title="Year", yaxis_title="Marks",
            legend=dict(orientation="h", y=-0.15), margin=dict(t=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Key Insights")
        avg = sum(cutoffs[y]["overall"] for y in cutoffs) / len(cutoffs)
        mx = max(cutoffs[y]["overall"] for y in cutoffs)
        st.markdown(f"""
        - **Average overall cutoff:** {avg:.1f} marks
        - **Highest cutoff:** {mx} marks (hardest year)
        - **GA cutoff** is always 15-20 — but AIR 1 needs 55-62 in GA
        - **Quant cutoff** is low (7-9) but AIR 1 needs 22-26
        - **Vacancies** affect cutoff inversely — more vacancies = slightly lower cutoff
        """)

    # ── PHASE 2: ESI ──
    elif rbi_sub == "📚 Phase 2: ESI":
        st.markdown("### 📚 Economic & Social Issues (Paper 1)")
        esi = get_esi_topics()
        for topic_name, topic in esi.items():
            with st.expander(f"📌 {topic_name} — {topic['importance']}", expanded=False):
                st.markdown("**Key Concepts to Master:**")
                for c in topic["key_concepts"]:
                    st.markdown(f"- {c}")

    # ── PHASE 2: FM ──
    elif rbi_sub == "📚 Phase 2: FM":
        st.markdown("### 📚 Finance & Management (Paper 3)")
        fm = get_fm_topics()
        for topic_name, topic in fm.items():
            with st.expander(f"📌 {topic_name} — {topic['importance']}", expanded=False):
                st.markdown("**Key Concepts to Master:**")
                for c in topic["key_concepts"]:
                    st.markdown(f"- {c}")

    # ── PHASE 2 MCQs ──
    elif rbi_sub == "❓ Phase 2 MCQs":
        st.markdown("### ❓ Phase 2 Practice MCQs")
        p2_paper = st.radio("Paper:", ["ESI (Economic & Social Issues)", "FM (Finance & Management)"], horizontal=True, key="p2p")
        paper_key = "ESI" if "ESI" in p2_paper else "FM"
        mcqs = get_phase2_mcqs(paper_key)

        st.markdown(f"**{len(mcqs)} questions**")
        # Score
        p2_answered = {k: v for k, v in st.session_state.quiz_answered.items() if k.startswith(f"p2_{paper_key}")}
        if p2_answered:
            corr = sum(1 for v in p2_answered.values() if v)
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Correct", corr)
            with c2: st.metric("Attempted", len(p2_answered))
            with c3: st.metric("Accuracy", f"{corr/len(p2_answered)*100:.0f}%")

        for qi, m in enumerate(mcqs):
            qk = f"p2_{paper_key}_{qi}"
            with st.expander(f"**Q{qi+1}.** {m['question']}", expanded=(qi < 3)):
                ans = st.radio("Answer:", m["options"], key=f"qz_{qk}", index=None)
                if ans is not None:
                    correct = m["options"][m["answer"]]
                    is_right = ans == correct
                    st.session_state.quiz_answered[qk] = is_right
                    if is_right:
                        st.markdown(f'<div class="quiz-correct">✅ <strong>Correct!</strong> {m["explanation"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="quiz-wrong">❌ Correct: <strong>{correct}</strong><br>{m["explanation"]}</div>', unsafe_allow_html=True)

    # ── RBI GOVERNORS ──
    elif rbi_sub == "👤 RBI Governors":
        st.markdown("### 👤 RBI Governors — Complete List")
        st.caption("Frequently asked in GA. Know at least the last 10 + first Indian Governor.")
        governors = get_rbi_governors()
        for g in reversed(governors):
            note = f" — *{g['note']}*" if g["note"] else ""
            highlight = "background: #fff3e0; border-left-color: #ff8f00;" if g["note"] else ""
            st.markdown(f"""<div class="governor-card" style="{highlight}">
                <strong>{g['name']}</strong> ({g['tenure']}){note}
            </div>""", unsafe_allow_html=True)

    # ── COMMITTEES ──
    elif rbi_sub == "📜 Committees":
        st.markdown("### 📜 Important RBI & Banking Committees")
        st.caption("These are asked every year. Know: Committee Name + Topic + Key Recommendation")
        committees = get_rbi_committees()
        for c in committees:
            with st.expander(f"📌 {c['name']} — {c['topic']}"):
                st.markdown(f"**Key Recommendation:** {c['key_reco']}")

    # ── IMPORTANT ACTS ──
    elif rbi_sub == "⚖️ Important Acts":
        st.markdown("### ⚖️ Important Banking & Finance Acts")
        st.caption("Know: Act Name + Year + Purpose + Key Section/Point")
        acts = get_important_acts()
        for a in acts:
            with st.expander(f"📄 {a['act']}"):
                st.markdown(f"**Purpose:** {a['purpose']}")
                st.markdown(f"**Key Point:** {a['key_point']}")

    # ── QUANT SHORTCUTS ──
    elif rbi_sub == "🧮 Quant Shortcuts":
        st.markdown("### 🧮 Quant Formulas & Shortcuts")
        st.caption("Revise these before every mock test")
        shortcuts = get_quant_shortcuts()
        for s in shortcuts:
            with st.expander(f"📐 {s['topic']}", expanded=False):
                for sc in s["shortcuts"]:
                    st.markdown(f"- `{sc}`")

    # ── LAST 30 DAYS PLAN ──
    elif rbi_sub == "📅 Last 30 Days Plan":
        st.markdown("### 📅 Last 30 Days — Battle Plan")
        plan_phase = st.radio("Phase:", ["Phase 1", "Phase 2"], horizontal=True, key="l30p")
        plan = get_last30_plan(plan_phase)
        if plan:
            for w in plan["weeks"]:
                with st.container(border=True):
                    st.markdown(f"### {w['week']}")
                    st.markdown(f"**Target:** {w['targets']}")
                    for s in w["daily_schedule"]:
                        st.markdown(f"- {s}")
            if "exam_eve" in plan:
                st.markdown("---")
                st.markdown("### 🌙 Exam Eve Checklist")
                for e in plan["exam_eve"]:
                    st.markdown(f"- {e}")

    # ── TOPPER TIPS ──
    elif rbi_sub == "💡 Topper Tips":
        st.markdown("### 💡 AIR 1 Mindset — Topper Strategies")
        tips = get_topper_tips()
        for i, t in enumerate(tips, 1):
            with st.container(border=True):
                st.markdown(f"### {i}. {t['title']}")
                st.markdown(t["detail"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB: UPLOAD
# ═════════════════════════════════════════════════════════════════════════════
with tab_upload:
    st.markdown("### 📁 Upload Question Papers")
    st.markdown("""
    <div class="tip-box">
        <strong>💡 Tip:</strong> Upload PDFs of last 5 years' papers for best analysis.
        You can also paste questions or upload CSV. Each question gets auto-categorized by topic.
    </div>
    """, unsafe_allow_html=True)

    upload_method = st.radio(
        "Input method:", ["📄 Upload Files (PDF/CSV/TXT)", "✏️ Type or Paste Text"],
        horizontal=True,
    )

    if upload_method.startswith("📄"):
        uploaded_files = st.file_uploader(
            "Drop your question papers here",
            type=["pdf", "txt", "csv"], accept_multiple_files=True,
            help="Supported: PDF, TXT, CSV. Upload multiple files at once.",
        )
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} file(s).** Tag each with year & phase:")
            file_metadata = []
            for i, f in enumerate(uploaded_files):
                with st.container(border=True):
                    st.markdown(f"📄 **{f.name}**")
                    c1, c2 = st.columns(2)
                    with c1:
                        year = st.number_input("Year", 2015, 2030, 2024, key=f"year_{i}")
                    with c2:
                        phase = st.selectbox("Phase", phases, key=f"phase_{i}")
                    file_metadata.append({"file": f, "year": year, "phase": phase})

            if st.button("🚀 Process All Papers", type="primary", use_container_width=True):
                _process_files(file_metadata, exam_type, method, api_key, model_name)
    else:
        c1, c2 = st.columns(2)
        with c1:
            text_year = st.number_input("Year", 2015, 2030, 2024, key="ty")
        with c2:
            text_phase = st.selectbox("Phase", phases, key="tp")
        pasted = st.text_area(
            "Paste questions below", height=300,
            placeholder="Q1. What is the value of...\nQ2. 8 persons sit around a circular table...",
        )
        if st.button("🚀 Process Text", type="primary", use_container_width=True) and pasted.strip():
            _process_text(pasted, text_year, text_phase, exam_type, method, api_key, model_name)

    if st.session_state.all_questions:
        st.markdown("---")
        st.markdown("### 📦 Loaded Data")
        years = sorted(set(q.year for q in st.session_state.all_questions))
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Questions", len(st.session_state.all_questions))
        with c2:
            st.metric("Years", f"{years[0]}-{years[-1]}" if len(years) > 1 else str(years[0]))
        with c3:
            st.metric("Categorized", len(st.session_state.categorized))

        summary = []
        for y in years:
            cnt = sum(1 for q in st.session_state.all_questions if q.year == y)
            summary.append({"Year": y, "Questions": cnt})
        st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear All Data"):
            for k in _defaults:
                st.session_state[k] = type(_defaults[k])() if isinstance(_defaults[k], (list, dict)) else _defaults[k]
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# TAB: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
with tab_dashboard:
    if not st.session_state.categorized:
        st.markdown('<div class="tip-box"><strong>📈 Dashboard is empty.</strong><br>Upload & process papers in the <strong>📁 Upload</strong> tab first.</div>', unsafe_allow_html=True)
    else:
        categorized = st.session_state.categorized
        freq = build_frequency_matrix(categorized, group_by="topic")
        sections = sorted(set(cq.section for cq in categorized))

        section_filter = st.selectbox("🔍 Filter by Section", ["All Sections"] + sections)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Questions", len(categorized))
        with c2: st.metric("Years", len(set(cq.question.year for cq in categorized)))
        with c3: st.metric("Topics", len(set(cq.topic for cq in categorized)))
        with c4: st.metric("Sections", len(sections))
        st.markdown("---")

        st.markdown("### 📊 Frequency Matrix")
        st.caption("Darker = more questions. Sorted by probability score.")
        if not freq.empty:
            disp = freq.copy()
            if section_filter != "All Sections":
                disp = disp.loc[disp.index.get_level_values("section") == section_filter]
            ycols = [c for c in disp.columns if c.isdigit()]
            st.dataframe(disp.style.background_gradient(cmap="YlGnBu", subset=ycols), use_container_width=True)

        import plotly.graph_objects as go
        import plotly.express as px

        cl, cr = st.columns(2)
        with cl:
            st.markdown("### 🥧 Section Split")
            sc = pd.Series([cq.section for cq in categorized]).value_counts()
            fig = px.pie(values=sc.values, names=sc.index, hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(height=370, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        with cr:
            st.markdown("### 📊 Difficulty")
            dc = pd.Series([cq.difficulty.value for cq in categorized]).value_counts()
            cm = {"Easy": "#66bb6a", "Medium": "#ffa726", "Hard": "#ef5350", "Unknown": "#bdbdbd"}
            fig2 = px.bar(x=dc.index, y=dc.values, color=dc.index, color_discrete_map=cm, text=dc.values)
            fig2.update_layout(height=370, showlegend=False, margin=dict(t=10, b=10))
            fig2.update_traces(textposition="outside")
            st.plotly_chart(fig2, use_container_width=True)

        if not freq.empty:
            ycols = [c for c in freq.columns if c.isdigit()]
            if len(ycols) >= 2:
                st.markdown("### 📈 Trends (Top 8)")
                top8 = freq.head(8)
                fig3 = go.Figure()
                for idx, row in top8.iterrows():
                    _, topic = idx
                    fig3.add_trace(go.Scatter(x=ycols, y=row[ycols].tolist(), mode="lines+markers", name=topic))
                fig3.update_layout(height=420, xaxis_title="Year", yaxis_title="Questions", legend=dict(orientation="h", y=-0.15), margin=dict(t=10))
                st.plotly_chart(fig3, use_container_width=True)

            st.markdown("### 🏆 Probability Ranking")
            top_n = st.slider("Topics to show", 5, 30, 15, key="dash_n")
            df_show = freq if section_filter == "All Sections" else freq.loc[freq.index.get_level_values("section") == section_filter]
            top = df_show.head(top_n)
            labels = [t for _, t in top.index]
            scores = top["ProbabilityScore"].tolist()
            fig4 = go.Figure(data=go.Bar(x=scores, y=labels, orientation="h", marker_color="#667eea", text=[f"{s:.0f}" for s in scores], textposition="auto"))
            fig4.update_layout(height=max(300, top_n*32), yaxis=dict(autorange="reversed"), margin=dict(l=200, t=10))
            st.plotly_chart(fig4, use_container_width=True)

        trends = analyze_trends(categorized)
        st.markdown("### 📋 Trend Summary")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Difficulty:** {trends.get('difficulty_trend', 'N/A')}")
            st.markdown("**🔼 Rising:**")
            for t in trends.get("rising_topics", [])[:5]:
                st.markdown(f"- {t['section']} > **{t['topic']}** `{t['change_pct']:+.0f}%`")
            if not trends.get("rising_topics"): st.caption("None")
        with c2:
            st.markdown("**🔽 Falling:**")
            for t in trends.get("falling_topics", [])[:5]:
                st.markdown(f"- {t['section']} > **{t['topic']}** `{t['change_pct']:+.0f}%`")
            if not trends.get("falling_topics"): st.caption("None")
            st.markdown("**🆕 New:**")
            for t in trends.get("new_topics", []):
                st.markdown(f"- {t['section']} > **{t['topic']}** ({t['count']})")
            if not trends.get("new_topics"): st.caption("None")


# ═════════════════════════════════════════════════════════════════════════════
# TAB: CURRENT AFFAIRS
# ═════════════════════════════════════════════════════════════════════════════
with tab_ca:
    st.markdown("### 📰 Current Affairs & Static GK")
    st.caption("Topic-wise key facts, one-liners, and practice questions for banking & regulatory exams")

    ca_sub_tab1, ca_sub_tab2 = st.tabs(["📚 Built-in CA", "📄 Upload CA PDFs & Generate MCQs"])

    # ── Built-in Current Affairs ─────────────────────────────────────────
    with ca_sub_tab1:
        ca_categories = get_ca_categories()
        selected_cat = st.selectbox(
            "Choose topic:", list(ca_categories.keys()),
            format_func=lambda x: f"{ca_categories[x]['icon']} {x}",
        )
        info = ca_categories[selected_cat]

        st.markdown(f"""
        <div class="ca-card" style="border-left-color: {info['color']};">
            <h4>{info['icon']} {selected_cat}</h4>
            <p>{info['description']}</p>
            <div class="meta">Importance: <strong>{info['importance']}</strong> &nbsp;|&nbsp; Expected Qs: <strong>{info['expected_questions']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        facts = get_key_facts(selected_cat)
        if facts:
            st.markdown("#### 📌 Key Facts & One-Liners")
            ff = st.radio("Show:", ["📋 All", "📚 Static", "🔄 Current"], horizontal=True, key="ff", label_visibility="collapsed")
            show = facts
            if ff == "📚 Static": show = [f for f in facts if f["type"] == "static"]
            elif ff == "🔄 Current": show = [f for f in facts if f["type"] == "current"]
            for i, f in enumerate(show, 1):
                badge = "🔵" if f["type"] == "static" else "🟢"
                st.markdown(f"{badge} **{i}.** {f['fact']}")

        st.markdown("---")
        mcqs = get_practice_mcqs(selected_cat)
        if mcqs:
            st.markdown(f"#### ❓ Quick Practice — {len(mcqs)} questions")
            for qi, m in enumerate(mcqs):
                with st.expander(f"Q{qi+1}: {m['question']}", expanded=False):
                    ans = st.radio("Your answer:", m["options"], key=f"ca_{selected_cat}_{qi}", index=None)
                    if ans is not None:
                        correct = m["options"][m["answer"]]
                        if ans == correct:
                            st.markdown(f'<div class="quiz-correct">✅ <strong>Correct!</strong> {m["explanation"]}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="quiz-wrong">❌ Correct: <strong>{correct}</strong><br>{m["explanation"]}</div>', unsafe_allow_html=True)

    # ── Upload CA PDFs & Generate MCQs ───────────────────────────────────
    with ca_sub_tab2:
        st.markdown("#### 📄 Upload Monthly Current Affairs PDFs")
        st.caption(
            "Upload Jan–June monthly CA compilations / capsules (PDF). "
            "AI will extract facts and generate exam-level MCQs from them.\n\n"
            "**Requires an AI provider** — configure OpenAI / Gemini / Ollama in the sidebar."
        )

        ca_files = st.file_uploader(
            "Upload CA PDFs (one per month)",
            type=["pdf"],
            accept_multiple_files=True,
            key="ca_pdf_upload",
        )

        ca_col1, ca_col2, ca_col3 = st.columns(3)
        with ca_col1:
            ca_cat_filter = st.selectbox(
                "Category focus:",
                ["All"] + list(get_ca_categories().keys()),
                key="ca_gen_cat",
            )
        with ca_col2:
            ca_diff = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"], index=1, key="ca_gen_diff")
        with ca_col3:
            ca_qpc = st.number_input("Questions per chunk:", 5, 25, 10, key="ca_gen_qpc",
                                     help="How many MCQs to generate per ~10K chars of CA text")

        if ca_files:
            st.info(f"📁 {len(ca_files)} PDF(s) uploaded: {', '.join(f.name for f in ca_files)}")

        can_generate = (
            ca_files
            and method != CategorizationMethod.RULE_BASED.value
            and (api_key or method == CategorizationMethod.OLLAMA.value)
        )

        if not ca_files:
            st.markdown('<div class="tip-box"><strong>📄 Upload monthly CA PDFs</strong> above to get started.</div>', unsafe_allow_html=True)
        elif method == CategorizationMethod.RULE_BASED.value or (not api_key and method != CategorizationMethod.OLLAMA.value):
            st.warning("⚠️ AI provider required. Go to **sidebar → ⚙️ AI Settings** and select OpenAI / Gemini / Ollama with an API key.")

        if st.button("🤖 Generate CA Questions", type="primary", use_container_width=True,
                     disabled=not can_generate, key="ca_gen_btn"):
            ai_cat = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
            progress = st.progress(0, text="Starting...")

            def _progress(cur, tot, msg):
                progress.progress(min((cur + 1) / max(tot + 1, 1), 0.99), text=msg)

            pdf_list = [(f.name, f.read()) for f in ca_files]

            generated = generate_ca_questions_from_pdfs(
                pdf_files=pdf_list,
                ai_caller=ai_cat._call_ai,
                exam_name=exam_type,
                category=ca_cat_filter,
                questions_per_chunk=ca_qpc,
                difficulty=ca_diff,
                progress_callback=_progress,
            )
            st.session_state.ca_generated_mcqs = generated
            progress.progress(1.0, text="Done!")
            st.rerun()

        # ── Display generated CA MCQs ────────────────────────────────────
        if st.session_state.ca_generated_mcqs:
            gen_qs = st.session_state.ca_generated_mcqs
            st.success(f"✅ {len(gen_qs)} MCQs generated from your CA PDFs")

            # Group by category
            cat_groups: dict[str, list] = {}
            for q in gen_qs:
                cat = q.get("category", "General")
                cat_groups.setdefault(cat, []).append(q)

            st.markdown("**Category breakdown:**")
            cat_cols = st.columns(min(len(cat_groups), 4))
            for ci, (cat, qs) in enumerate(sorted(cat_groups.items())):
                with cat_cols[ci % len(cat_cols)]:
                    st.metric(cat[:20], len(qs))

            st.markdown("---")

            # Filter by category
            show_cat = st.selectbox(
                "Show category:",
                ["All"] + sorted(cat_groups.keys()),
                key="ca_show_cat",
            )
            show_qs = gen_qs if show_cat == "All" else cat_groups.get(show_cat, [])

            for qi, m in enumerate(show_qs):
                src = f" *({m.get('source', '')})* " if m.get('source') else ""
                with st.expander(f"Q{qi+1}: {m['question'][:100]}{'...' if len(m['question']) > 100 else ''}{src}", expanded=(qi < 3)):
                    st.markdown(f"**{m['question']}**")
                    ans = st.radio("Your answer:", m["options"], key=f"ca_gen_{qi}", index=None)
                    if ans is not None:
                        correct = m["options"][m["answer"]]
                        if ans == correct:
                            st.markdown(f'<div class="quiz-correct">✅ <strong>Correct!</strong> {m["explanation"]}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="quiz-wrong">❌ Correct: <strong>{correct}</strong><br>{m["explanation"]}</div>', unsafe_allow_html=True)

            st.markdown("---")
            # Export generated questions as JSON
            import json as _json
            st.download_button(
                "📥 Download Generated MCQs (JSON)",
                data=_json.dumps(gen_qs, indent=2, ensure_ascii=False),
                file_name=f"{exam_type.replace(' ', '_')}_CA_MCQs.json",
                mime="application/json",
                use_container_width=True,
            )

            if st.button("🗑️ Clear Generated CA Questions", key="ca_clear_btn"):
                st.session_state.ca_generated_mcqs = []
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# TAB: CA PREDICTOR
# ═════════════════════════════════════════════════════════════════════════════
with tab_ca_pred:
    st.markdown("### 🔮 Current Affairs Predictive Analyzer")
    st.caption(
        "Upload monthly CA PDFs (Jan–Jun 2026) + previous year CA papers → "
        "AI predicts high-probability questions for RBI Grade B 2026. "
        "All data is saved to C:\\\\exam_analyzer_data and persists across sessions."
    )

    # Storage summary
    storage_info = get_storage_summary()
    sci1, sci2, sci3, sci4 = st.columns(4)
    with sci1:
        st.metric("📅 CA Months Uploaded", storage_info["ca_months_uploaded"])
    with sci2:
        st.metric("📚 PYQ Years Uploaded", storage_info["pyq_years_uploaded"])
    with sci3:
        st.metric("📊 Reports Generated", storage_info["reports_generated"])
    with sci4:
        st.metric("💾 Analysis Saved", "Yes" if storage_info["has_analysis"] else "No")

    ca_pred_tab1, ca_pred_tab2, ca_pred_tab3, ca_pred_tab4, ca_pred_tab5 = st.tabs([
        "📄 Upload CA PDFs", "📚 Upload PYQ Papers", "🔬 Run Analysis", "📊 View Report", "🚀 GitHub Pages"
    ])

    # ── Sub-tab 1: Upload Monthly CA PDFs ────────────────────────────────
    with ca_pred_tab1:
        st.markdown("#### 📄 Upload Monthly Current Affairs PDFs (Jan–Jun 2026)")
        st.markdown(
            '<div class="tip-box">'
            '<strong>📌 Tip:</strong> Upload one PDF per month. '
            'The AI will extract all exam-relevant facts, tag importance, and generate MCQs. '
            'Each upload is saved to C: drive so you won\'t lose progress.'
            '</div>',
            unsafe_allow_html=True,
        )

        ca_pred_month = st.selectbox(
            "Select month:", CA_MONTHS[:6],  # Jan-Jun
            key="ca_pred_month",
            help="Which month does this CA compilation cover?",
        )
        ca_pred_year = st.number_input("Year:", 2025, 2026, 2026, key="ca_pred_year")

        ca_pred_file = st.file_uploader(
            f"Upload CA PDF for {ca_pred_month} {ca_pred_year}",
            type=["pdf"],
            key="ca_pred_upload",
        )

        can_upload_ca = (
            ca_pred_file
            and method != CategorizationMethod.RULE_BASED.value
            and (api_key or method == CategorizationMethod.OLLAMA.value)
        )

        if not ca_pred_file:
            pass
        elif method == CategorizationMethod.RULE_BASED.value or (not api_key and method != CategorizationMethod.OLLAMA.value):
            st.warning("⚠️ AI provider required. Configure OpenAI / Gemini / Ollama in the sidebar.")

        if st.button("📤 Upload & Analyze", type="primary", use_container_width=True,
                     disabled=not can_upload_ca, key="ca_pred_upload_btn"):
            ai_cat = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
            progress = st.progress(0, text=f"Processing {ca_pred_month} CA PDF...")

            pdf_list = [(ca_pred_file.name, ca_pred_file.read())]
            month_map = {ca_pred_file.name: ca_pred_month}

            def _ca_progress(cur, tot, msg):
                progress.progress(min((cur + 1) / max(tot + 1, 1), 0.99), text=msg)

            result = extract_facts_from_pdfs(
                pdf_files=pdf_list,
                ai_caller=ai_cat._call_ai,
                month_map=month_map,
                exam_name=exam_type,
                progress_callback=_ca_progress,
            )

            # Save to persistent storage
            save_ca_extracted(ca_pred_month, ca_pred_year, {
                "facts": result["facts"],
                "questions": result["questions"],
                "source_file": ca_pred_file.name,
            })
            save_upload_record(ca_pred_file.name, ca_pred_month, ca_pred_year, "ca_monthly")

            # Update session state
            # Reload all from storage for consistency
            all_extracted = load_all_ca_extracted()
            all_facts = []
            all_qs = []
            for ext in all_extracted:
                all_facts.extend(ext.get("facts", []))
                all_qs.extend(ext.get("questions", []))
            st.session_state.ca_pred_facts = all_facts
            st.session_state.ca_pred_questions = all_qs

            # Persist
            save_full_state({
                "ca_pred_facts": all_facts,
                "ca_pred_questions": all_qs,
                "ca_pred_pyq_patterns": st.session_state.ca_pred_pyq_patterns,
            })

            progress.progress(1.0, text="Done!")
            st.success(f"✅ Extracted {len(result['facts'])} facts and {len(result['questions'])} MCQs from {ca_pred_month}")
            st.rerun()

        # Show existing uploaded months
        manifest = load_upload_manifest()
        ca_uploads = [m for m in manifest if m.get("type") == "ca_monthly"]
        if ca_uploads:
            st.markdown("---")
            st.markdown("**📅 Uploaded CA PDFs:**")
            for u in ca_uploads:
                st.markdown(f"✅ **{u['month']} {u.get('year', '')}** — {u['filename']} (uploaded {u.get('uploaded_at', '')[:10]})")

        # Total facts/questions in memory
        if st.session_state.ca_pred_facts:
            st.markdown("---")
            fc1, fc2 = st.columns(2)
            with fc1:
                st.metric("Total Facts Extracted", len(st.session_state.ca_pred_facts))
            with fc2:
                st.metric("Total MCQs Generated", len(st.session_state.ca_pred_questions))

            # Category breakdown
            cat_counts = {}
            for f in st.session_state.ca_pred_facts:
                cat = f.get("category", "General")
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
            st.markdown("**Category breakdown of extracted facts:**")
            cat_cols = st.columns(min(len(cat_counts), 4))
            for ci, (cat, count) in enumerate(sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)):
                with cat_cols[ci % len(cat_cols)]:
                    st.metric(cat[:25], count)

        # ── Folder Scan: Auto-detect CA PDFs ─────────────────────────────
        st.markdown("---")
        with st.expander("📂 Scan Documents Folder", expanded=False):
            st.caption(f"Looking in: `{CA_DOCUMENTS_DIR}`")
            st.markdown(
                "Drop CA PDFs into `documents/current_affairs/` with names like "
                "`january_2026.pdf`, `feb_2026.pdf`, etc. The app auto-detects the month."
            )

            ca_scan = scan_ca_folder()
            if not ca_scan:
                st.info("No PDF files found in documents/current_affairs/. Drop your CA PDFs there.")
            else:
                new_ca = [f for f in ca_scan if f["status"] == "new"]
                done_ca = [f for f in ca_scan if f["status"] == "processed"]

                if done_ca:
                    st.markdown(f"**✅ Already processed ({len(done_ca)}):**")
                    for f in done_ca:
                        st.markdown(f"- ✅ `{f['filename']}` → {f['month']} {f['year']} (processed {f['uploaded_at'][:10]})")

                if new_ca:
                    st.markdown(f"**🆕 New files detected ({len(new_ca)}):**")
                    for f in new_ca:
                        month_label = f["month"] if f["month"] else "⚠️ Unknown month"
                        st.markdown(f"- 🆕 `{f['filename']}` → {month_label} {f['year']}")

                    no_month = [f for f in new_ca if not f["month"]]
                    if no_month:
                        st.warning(f"{len(no_month)} file(s) have unrecognized month names. Rename them to include the month (e.g. january_2026.pdf).")

                    processable = [f for f in new_ca if f["month"]]
                    if processable:
                        can_batch = (
                            method != CategorizationMethod.RULE_BASED.value
                            and (api_key or method == CategorizationMethod.OLLAMA.value)
                        )
                        if not can_batch:
                            st.warning("⚠️ Configure an AI provider in the sidebar to batch-process.")

                        if st.button(
                            f"🚀 Process All {len(processable)} New CA PDFs",
                            type="primary", use_container_width=True,
                            disabled=not can_batch, key="batch_ca_btn",
                        ):
                            ai_cat = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
                            progress = st.progress(0, text="Batch processing CA PDFs...")

                            def _batch_ca_progress(cur, tot, msg):
                                progress.progress(min((cur + 1) / max(tot, 1), 0.99), text=msg)

                            batch_result = batch_process_ca(
                                new_files=processable,
                                ai_caller=ai_cat._call_ai,
                                exam_name=exam_type,
                                progress_callback=_batch_ca_progress,
                            )

                            # Reload all from storage
                            all_extracted = load_all_ca_extracted()
                            all_facts, all_qs = [], []
                            for ext in all_extracted:
                                all_facts.extend(ext.get("facts", []))
                                all_qs.extend(ext.get("questions", []))
                            st.session_state.ca_pred_facts = all_facts
                            st.session_state.ca_pred_questions = all_qs
                            save_full_state({
                                "ca_pred_facts": all_facts,
                                "ca_pred_questions": all_qs,
                                "ca_pred_pyq_patterns": st.session_state.ca_pred_pyq_patterns,
                            })

                            progress.progress(1.0, text="Done!")
                            st.success(
                                f"✅ Batch complete: {batch_result['processed']} PDFs processed, "
                                f"{batch_result['total_facts']} facts, {batch_result['total_questions']} MCQs"
                            )
                            if batch_result["errors"]:
                                for err in batch_result["errors"]:
                                    st.warning(f"⚠️ {err}")
                            st.rerun()
                else:
                    st.success("All files in the folder have been processed!")

    # ── Sub-tab 2: Upload Previous Year CA Papers ────────────────────────
    with ca_pred_tab2:
        st.markdown("#### 📚 Upload Previous Year Question Papers (Current Affairs)")
        st.markdown(
            '<div class="tip-box">'
            '<strong>📌 Why?</strong> By analyzing which CA topics RBI asked in past exams, '
            'the AI learns the pattern — which categories get more questions, what difficulty, '
            'which topics repeat. This dramatically improves prediction accuracy.'
            '</div>',
            unsafe_allow_html=True,
        )

        pyq_col1, pyq_col2 = st.columns(2)
        with pyq_col1:
            pyq_year = st.selectbox("Year of paper:", list(range(2025, 2018, -1)), key="pyq_ca_year")
        with pyq_col2:
            pyq_type = st.selectbox("Paper type:", ["Phase 1 (GA Section)", "Full Paper"], key="pyq_type")

        pyq_file = st.file_uploader(
            f"Upload {pyq_year} paper (PDF or text)",
            type=["pdf", "txt", "csv"],
            key="pyq_ca_upload",
        )

        can_upload_pyq = (
            pyq_file
            and method != CategorizationMethod.RULE_BASED.value
            and (api_key or method == CategorizationMethod.OLLAMA.value)
        )

        if pyq_file and (method == CategorizationMethod.RULE_BASED.value or (not api_key and method != CategorizationMethod.OLLAMA.value)):
            st.warning("⚠️ AI provider recommended for accurate pattern extraction. Rule-based fallback will be less accurate.")
            can_upload_pyq = bool(pyq_file)  # Allow rule-based as fallback

        if st.button("📤 Upload & Extract Patterns", type="primary", use_container_width=True,
                     disabled=not pyq_file, key="pyq_upload_btn"):
            progress = st.progress(0, text=f"Processing {pyq_year} PYQ paper...")

            # Extract text and split into questions
            fb = pyq_file.read()
            if pyq_file.name.lower().endswith(".pdf"):
                text = extract_text_from_pdf(fb)
                qs = split_into_questions(text, pyq_year, "Phase 1", exam_type)
            elif pyq_file.name.lower().endswith(".csv"):
                qs = parse_csv_input(fb, pyq_year, "Phase 1", exam_type)
            else:
                qs = parse_text_input(fb.decode("utf-8", errors="replace"), pyq_year, "Phase 1", exam_type)

            progress.progress(0.3, text=f"Extracted {len(qs)} questions. Classifying into CA categories...")

            # Convert to dicts for pattern analyzer
            q_dicts = [{"text": q.text, "question_number": q.question_number} for q in qs]

            # Use AI or rule-based classification
            ai_caller = None
            if method != CategorizationMethod.RULE_BASED.value and (api_key or method == CategorizationMethod.OLLAMA.value):
                ai_cat = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
                ai_caller = ai_cat._call_ai

            pattern = analyze_pyq_paper(q_dicts, ai_caller=ai_caller)
            pattern["year"] = pyq_year
            pattern["source_file"] = pyq_file.name

            # Save to persistent storage
            save_pyq_pattern(pyq_year, pattern)
            save_upload_record(pyq_file.name, "", pyq_year, "pyq_ca")

            # Reload all patterns
            all_patterns = load_all_pyq_patterns()
            st.session_state.ca_pred_pyq_patterns = all_patterns

            # Persist
            save_full_state({
                "ca_pred_facts": st.session_state.ca_pred_facts,
                "ca_pred_questions": st.session_state.ca_pred_questions,
                "ca_pred_pyq_patterns": all_patterns,
            })

            progress.progress(1.0, text="Done!")
            st.success(f"✅ Extracted pattern from {pyq_year}: {pattern['total_questions']} questions across {len(pattern['categories'])} categories")
            st.rerun()

        # Show existing PYQ patterns
        if st.session_state.ca_pred_pyq_patterns:
            st.markdown("---")
            st.markdown("**📚 Uploaded PYQ Patterns:**")

            for p in st.session_state.ca_pred_pyq_patterns:
                yr = p.get("_year", p.get("year", "?"))
                total = p.get("total_questions", 0)
                cats = p.get("categories", {})
                with st.expander(f"Year {yr} — {total} questions, {len(cats)} categories", expanded=False):
                    for cat, info in sorted(cats.items(), key=lambda x: x[1].get("count", 0), reverse=True):
                        st.markdown(f"- **{cat}**: {info['count']} Qs ({info['percentage']}%)")

            # Show aggregated pattern
            agg = aggregate_pyq_patterns(st.session_state.ca_pred_pyq_patterns)
            if agg.get("categories"):
                st.markdown("---")
                st.markdown("**📊 Aggregated Pattern (All Years):**")
                st.markdown(f"*{agg['years_analyzed']} year(s) analyzed, avg {agg['avg_total_questions']} questions/year*")

                import pandas as pd
                agg_data = []
                for cat, info in sorted(agg["categories"].items(), key=lambda x: x[1]["avg_count"], reverse=True):
                    agg_data.append({
                        "Category": cat,
                        "Avg Qs/Year": info["avg_count"],
                        "Avg %": info["avg_percentage"],
                        "Consistency": f"{info['consistency']}%",
                        "Trend": info["trend"],
                    })
                st.dataframe(pd.DataFrame(agg_data), use_container_width=True, hide_index=True)

        # ── Folder Scan: Auto-detect PYQ Papers ──────────────────────────
        st.markdown("---")
        with st.expander("📂 Scan Documents Folder", expanded=False):
            st.caption(f"Looking in: `{PYQ_DOCUMENTS_DIR}`")
            st.markdown(
                "Drop PYQ papers into `documents/previous_year_papers/` with names like "
                "`rbi_grade_b_2024.pdf`, `pyq_2023.pdf`, etc. The app auto-detects the year."
            )

            pyq_scan = scan_pyq_folder()
            if not pyq_scan:
                st.info("No files found in documents/previous_year_papers/. Drop your PYQ papers there.")
            else:
                new_pyq = [f for f in pyq_scan if f["status"] == "new"]
                done_pyq = [f for f in pyq_scan if f["status"] == "processed"]

                if done_pyq:
                    st.markdown(f"**✅ Already processed ({len(done_pyq)}):**")
                    for f in done_pyq:
                        st.markdown(f"- ✅ `{f['filename']}` → Year {f['year']} (processed {f['uploaded_at'][:10]})")

                if new_pyq:
                    st.markdown(f"**🆕 New files detected ({len(new_pyq)}):**")
                    for f in new_pyq:
                        year_label = str(f["year"]) if f["year"] else "⚠️ Unknown year"
                        st.markdown(f"- 🆕 `{f['filename']}` → Year {year_label}")

                    no_year = [f for f in new_pyq if f["year"] == 0]
                    if no_year:
                        st.warning(f"{len(no_year)} file(s) have unrecognized year. Rename them to include the year (e.g. rbi_2024.pdf).")

                    processable = [f for f in new_pyq if f["year"] != 0]
                    if processable:
                        ai_caller_pyq = None
                        if method != CategorizationMethod.RULE_BASED.value and (api_key or method == CategorizationMethod.OLLAMA.value):
                            ai_cat_pyq = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
                            ai_caller_pyq = ai_cat_pyq._call_ai

                        if st.button(
                            f"🚀 Process All {len(processable)} New PYQ Papers",
                            type="primary", use_container_width=True,
                            key="batch_pyq_btn",
                        ):
                            progress = st.progress(0, text="Batch processing PYQ papers...")

                            def _batch_pyq_progress(cur, tot, msg):
                                progress.progress(min((cur + 1) / max(tot, 1), 0.99), text=msg)

                            batch_result = batch_process_pyq(
                                new_files=processable,
                                ai_caller=ai_caller_pyq,
                                exam_name=exam_type,
                                progress_callback=_batch_pyq_progress,
                            )

                            # Reload all patterns
                            all_patterns = load_all_pyq_patterns()
                            st.session_state.ca_pred_pyq_patterns = all_patterns
                            save_full_state({
                                "ca_pred_facts": st.session_state.ca_pred_facts,
                                "ca_pred_questions": st.session_state.ca_pred_questions,
                                "ca_pred_pyq_patterns": all_patterns,
                            })

                            progress.progress(1.0, text="Done!")
                            st.success(
                                f"✅ Batch complete: {batch_result['processed']} papers processed, "
                                f"{batch_result['total_questions']} questions analyzed"
                            )
                            if batch_result["errors"]:
                                for err in batch_result["errors"]:
                                    st.warning(f"⚠️ {err}")
                            st.rerun()
                else:
                    st.success("All PYQ papers in the folder have been processed!")

    # ── Sub-tab 3: Run Predictive Analysis ───────────────────────────────
    with ca_pred_tab3:
        st.markdown("#### 🔬 Run Predictive Analysis")

        has_facts = len(st.session_state.ca_pred_facts) > 0
        has_pyqs = len(st.session_state.ca_pred_pyq_patterns) > 0

        if not has_facts:
            st.markdown(
                '<div class="tip-box">'
                '<strong>📄 Step 1:</strong> Upload monthly CA PDFs in the "Upload CA PDFs" tab first. '
                'The more months you upload, the better the predictions.'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.success(f"✅ {len(st.session_state.ca_pred_facts)} facts and {len(st.session_state.ca_pred_questions)} MCQs ready for analysis")

        if not has_pyqs:
            st.info("💡 Upload previous year papers in the 'Upload PYQ Papers' tab for pattern-based predictions. Without PYQs, the analysis uses default importance weights.")
        else:
            st.success(f"✅ {len(st.session_state.ca_pred_pyq_patterns)} PYQ year(s) loaded for pattern matching")

        if has_facts:
            st.markdown("---")
            target_qs = st.slider(
                "Expected CA questions in exam:",
                10, 50, 30,
                key="ca_pred_target",
                help="How many current affairs questions do you expect in Phase 1 GA?",
            )

            if st.button("🚀 Run Predictive Analysis", type="primary", use_container_width=True, key="ca_pred_run"):
                with st.spinner("Running AI-powered predictive analysis..."):
                    analysis = run_predictive_analysis(
                        all_facts=st.session_state.ca_pred_facts,
                        all_questions=st.session_state.ca_pred_questions,
                        pyq_patterns=st.session_state.ca_pred_pyq_patterns if has_pyqs else None,
                        target_questions=target_qs,
                    )

                    st.session_state.ca_pred_analysis = analysis
                    save_analysis_results(analysis)

                    # Generate HTML report
                    html_report = export_ca_predictions_html(analysis, exam_name=exam_type)
                    st.session_state.ca_pred_html = html_report
                    report_path = save_report(html_report)

                    st.success(f"✅ Analysis complete! Report saved to {report_path}")
                    st.rerun()

        # Show quick summary if analysis exists
        if st.session_state.ca_pred_analysis:
            analysis = st.session_state.ca_pred_analysis
            st.markdown("---")
            st.markdown("### 📊 Analysis Summary")

            readiness = analysis.get("readiness_score", 0)
            r_color = "green" if readiness >= 70 else "orange" if readiness >= 40 else "red"
            st.markdown(f"**Readiness Score:** :{r_color}[{readiness}%]")

            asum1, asum2, asum3 = st.columns(3)
            with asum1:
                st.metric("Facts Analyzed", analysis.get("total_facts", 0))
            with asum2:
                st.metric("MCQs Available", analysis.get("total_questions", 0))
            with asum3:
                st.metric("Sections Covered", len([s for s in analysis.get("sections", []) if s["fact_count"] > 0]))

            # Top 10 must-study facts
            st.markdown("#### 🔥 Top 10 Must-Study Facts")
            for i, f in enumerate(analysis.get("top_50_facts", [])[:10], 1):
                prob = f.get("probability_score", 0)
                imp = f.get("importance", "Medium")
                imp_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(imp, "⚪")
                cat = f.get("category", "")
                st.markdown(
                    f"**{i}.** {imp_icon} [{prob}%] **{cat}** — {f.get('fact', '')}"
                )

            # Section predictions table
            st.markdown("#### 📋 Section-wise Predictions")
            sec_data = []
            for s in analysis.get("sections", []):
                if s["predicted_questions"] > 0 or s["fact_count"] > 0:
                    sec_data.append({
                        "Section": s["name"],
                        "Priority": s["study_priority"],
                        "Expected Qs": s["predicted_questions"],
                        "Facts": s["fact_count"],
                        "MCQs": s["question_count"],
                        "Coverage": s["coverage_status"],
                    })
            if sec_data:
                st.dataframe(pd.DataFrame(sec_data), use_container_width=True, hide_index=True)

    # ── Sub-tab 4: View & Download Report ────────────────────────────────
    with ca_pred_tab4:
        st.markdown("#### 📊 View & Download Predictions Report")

        if st.session_state.ca_pred_html:
            st.success("✅ Report is ready!")

            st.download_button(
                "📥 Download HTML Report",
                data=st.session_state.ca_pred_html,
                file_name=f"{exam_type.replace(' ', '_')}_CA_Predictions_2026.html",
                mime="text/html",
                use_container_width=True,
                type="primary",
            )

            st.markdown("---")
            st.markdown("**Preview (scroll within the frame):**")
            import streamlit.components.v1 as components
            components.html(st.session_state.ca_pred_html, height=700, scrolling=True)

        elif st.session_state.ca_pred_analysis:
            st.info("Analysis exists but no report generated yet. Go to 'Run Analysis' tab and click 'Run Predictive Analysis'.")
        else:
            st.markdown(
                '<div class="tip-box">'
                '<strong>📊 No report yet.</strong> Follow these steps:<br>'
                '1️⃣ Upload CA PDFs (Jan–Jun) in "Upload CA PDFs" tab<br>'
                '2️⃣ (Optional) Upload PYQ papers in "Upload PYQ Papers" tab<br>'
                '3️⃣ Run analysis in "Run Analysis" tab<br>'
                '4️⃣ Come back here to view and download the report'
                '</div>',
                unsafe_allow_html=True,
            )

        # Also offer JSON download of analysis data
        if st.session_state.ca_pred_analysis:
            st.markdown("---")
            st.download_button(
                "📥 Download Raw Analysis Data (JSON)",
                data=json.dumps(st.session_state.ca_pred_analysis, indent=2, ensure_ascii=False, default=str),
                file_name=f"{exam_type.replace(' ', '_')}_CA_Analysis_2026.json",
                mime="application/json",
                use_container_width=True,
            )

        # Data management
        if st.session_state.ca_pred_facts or st.session_state.ca_pred_pyq_patterns:
            st.markdown("---")
            with st.expander("🗑️ Data Management", expanded=False):
                st.caption(f"Storage path: {storage_info['storage_path']}")
                if st.button("🗑️ Clear All CA Predictor Data", key="ca_pred_clear_all"):
                    st.session_state.ca_pred_facts = []
                    st.session_state.ca_pred_questions = []
                    st.session_state.ca_pred_analysis = None
                    st.session_state.ca_pred_pyq_patterns = []
                    st.session_state.ca_pred_html = None
                    save_full_state({
                        "ca_pred_facts": [],
                        "ca_pred_questions": [],
                        "ca_pred_pyq_patterns": [],
                    })
                    st.rerun()


    # ── Sub-tab 5: GitHub Pages Deployment ───────────────────────────────────
    with ca_pred_tab5:
        st.markdown("#### 🚀 Deploy to GitHub Pages")
        st.caption(
            "Push your CA predictions to a GitHub Pages site for easy access from any device. "
            "Navigate, search, filter and revise — all in one place."
        )

        # Check git availability
        import shutil
        git_available = shutil.which("git") is not None

        if not git_available:
            st.error("❌ Git is not installed or not in PATH. Please install Git first.")
        else:
            st.success("✅ Git is available")

            # Repository setup
            st.markdown("##### 1️⃣ Repository Setup")
            st.info(
                "**First time?** Create a new empty repo on GitHub (e.g. `rbi-ca-predictions`), "
                "then paste the URL below. Make sure you have git credentials configured "
                "(SSH key or credential manager)."
            )

            site_status = get_site_status()

            repo_url = st.text_input(
                "GitHub Repository URL:",
                value=site_status.get("remote_url", ""),
                placeholder="https://github.com/username/rbi-ca-predictions.git",
                key="gh_repo_url",
            )

            if repo_url:
                if st.button("🔗 Initialize / Connect Repository", key="gh_init"):
                    with st.spinner("Setting up repository..."):
                        try:
                            result = init_site_repo(repo_url)
                            st.success(result)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to initialize: {e}")

            # Status display
            if site_status["initialized"]:
                st.markdown("---")
                st.markdown("##### 📡 Site Status")
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown(f"**Remote:** `{site_status['remote_url']}`")
                    st.markdown(f"**Last commit:** {site_status['last_commit']}")
                with sc2:
                    st.markdown(f"**Local dir:** `{site_status['site_dir']}`")
                    if site_status["pages_url"]:
                        st.markdown(f"**🌐 Live site:** [{site_status['pages_url']}]({site_status['pages_url']})")

                # Deploy section
                st.markdown("---")
                st.markdown("##### 2️⃣ Deploy")

                if st.session_state.ca_pred_analysis:
                    analysis = st.session_state.ca_pred_analysis
                    facts_n = analysis.get("total_facts", 0)
                    qs_n = analysis.get("total_questions", 0)
                    secs_n = len([s for s in analysis.get("sections", []) if s["fact_count"] > 0])

                    st.markdown(f"**Ready to deploy:** {facts_n} facts, {qs_n} MCQs across {secs_n} sections")

                    custom_msg = st.text_input(
                        "Commit message (optional):",
                        placeholder="Auto-generated if empty",
                        key="gh_commit_msg",
                    )

                    col_deploy, col_preview = st.columns(2)
                    with col_deploy:
                        if st.button("🚀 Deploy to GitHub Pages", type="primary", use_container_width=True, key="gh_deploy"):
                            with st.spinner("Building site and pushing to GitHub Pages..."):
                                try:
                                    result = deploy_site(
                                        analysis=analysis,
                                        exam_name=exam_type,
                                        commit_msg=custom_msg if custom_msg else "",
                                    )
                                    if "Error" in result or "failed" in result.lower():
                                        st.warning(result)
                                    else:
                                        st.success(result)
                                        updated_status = get_site_status()
                                        if updated_status["pages_url"]:
                                            st.markdown(f"### 🌐 [Visit your site →]({updated_status['pages_url']})")
                                            st.info("Note: GitHub Pages may take 1-2 minutes to update after the first deploy. Enable GitHub Pages from your repo Settings → Pages → Branch: gh-pages.")
                                except Exception as e:
                                    st.error(f"Deployment failed: {e}")

                    with col_preview:
                        if st.button("👁️ Preview Site Locally", use_container_width=True, key="gh_preview"):
                            with st.spinner("Building preview..."):
                                preview_html = build_github_pages_site(analysis, exam_name=exam_type)
                                st.session_state["gh_preview_html"] = preview_html
                                st.success("Preview ready! Scroll down.")

                    if st.session_state.get("gh_preview_html"):
                        st.markdown("---")
                        st.markdown("**Site Preview:**")
                        import streamlit.components.v1 as components
                        components.html(st.session_state["gh_preview_html"], height=700, scrolling=True)

                else:
                    st.warning(
                        "⚠️ No analysis data available. Run the predictive analysis first "
                        "(go to '🔬 Run Analysis' tab)."
                    )
            elif repo_url:
                st.info("👆 Click 'Initialize / Connect Repository' to set up the GitHub Pages site.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB: QUIZ
# ═════════════════════════════════════════════════════════════════════════════
with tab_quiz:
    st.markdown("### ❓ Practice Quiz")
    st.caption("Topic-wise or mixed MCQs — track your score as you go")

    ca_categories = get_ca_categories()
    quiz_topics = [c for c in ca_categories if get_practice_mcqs(c)]

    # Add Phase 2 MCQs option when RBI Grade B is selected
    quiz_modes = ["📌 Topic-wise (CA)", "🔀 Random Mix (CA)"]
    if exam_type == "RBI Grade B":
        quiz_modes.extend(["📚 Phase 2: ESI", "📚 Phase 2: FM", "🎯 Full RBI Mix"])

    qm = st.radio("Mode:", quiz_modes, horizontal=True, key="qm")

    if qm.startswith("📌"):
        qc = st.selectbox("Topic:", quiz_topics, format_func=lambda x: f"{ca_categories[x]['icon']} {x} ({len(get_practice_mcqs(x))} Qs)", key="qts")
        quiz_qs = get_practice_mcqs(qc)
        mode_key = f"topic_{qc}"
    elif qm.startswith("🔀"):
        quiz_qs = []
        for c in quiz_topics:
            for m in get_practice_mcqs(c):
                quiz_qs.append({**m, "_cat": c})
        import random
        random.seed(42)
        random.shuffle(quiz_qs)
        mode_key = "mix"
    elif "ESI" in qm:
        quiz_qs = get_phase2_mcqs("ESI")
        mode_key = "p2quiz_ESI"
    elif "FM" in qm:
        quiz_qs = get_phase2_mcqs("FM")
        mode_key = "p2quiz_FM"
    else:  # Full RBI Mix
        quiz_qs = []
        for c in quiz_topics:
            for m in get_practice_mcqs(c):
                quiz_qs.append({**m, "_cat": c})
        for m in get_phase2_mcqs("ESI"):
            quiz_qs.append({**m, "_cat": "ESI"})
        for m in get_phase2_mcqs("FM"):
            quiz_qs.append({**m, "_cat": "FM"})
        import random
        random.seed(42)
        random.shuffle(quiz_qs)
        mode_key = "fullrbi"

    if quiz_qs:
        st.markdown(f"**{len(quiz_qs)} questions**")

        answered = {k: v for k, v in st.session_state.quiz_answered.items() if k.startswith(mode_key)}
        if answered:
            corr = sum(1 for v in answered.values() if v)
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("✅ Correct", corr)
            with c2: st.metric("📝 Attempted", len(answered))
            with c3: st.metric("📊 Accuracy", f"{corr/len(answered)*100:.0f}%")

        st.markdown("---")
        for qi, m in enumerate(quiz_qs):
            qk = f"{mode_key}_{qi}"
            cat_lbl = f" *({m.get('_cat', '')})*" if '_cat' in m else ""
            with st.expander(f"**Q{qi+1}.** {m['question']}{cat_lbl}", expanded=(qi < 3)):
                ans = st.radio("Answer:", m["options"], key=f"qz_{qk}", index=None)
                if ans is not None:
                    correct = m["options"][m["answer"]]
                    is_right = ans == correct
                    st.session_state.quiz_answered[qk] = is_right
                    if is_right:
                        st.markdown(f'<div class="quiz-correct">✅ <strong>Correct!</strong> {m["explanation"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="quiz-wrong">❌ Correct: <strong>{correct}</strong><br>{m["explanation"]}</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Reset Score"):
            st.session_state.quiz_answered = {}
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# TAB: PREDICTIONS
# ═════════════════════════════════════════════════════════════════════════════
with tab_predictions:
    if not st.session_state.categorized:
        st.markdown('<div class="tip-box"><strong>🔮 Upload papers first</strong> in the <strong>📁 Upload</strong> tab to generate predictions.</div>', unsafe_allow_html=True)
    else:
        st.markdown("### 🔮 Predicted Topics for Next Exam")
        st.caption("Based on frequency, consistency, and recent trends")

        te = st.number_input("Expected total questions (0 = auto)", 0, 500, 0, help="Set 0 to auto-detect from history")
        if st.button("⚡ Generate Predictions", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                preds = predict_topic_distribution(st.session_state.categorized, te if te > 0 else None)
                st.session_state.predictions = preds
                st.session_state.sample_questions = generate_sample_questions_template(preds, top_n=10)

        if st.session_state.predictions:
            pdf = pd.DataFrame(st.session_state.predictions)
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Topics", len(pdf))
            with c2: st.metric("Expected Qs", pdf["predicted_count"].sum())
            with c3: st.metric("#1 Topic", pdf.iloc[0]["topic"] if len(pdf) else "-")

            st.markdown("#### 📋 Prediction Table")
            st.dataframe(
                pdf[["section","topic","predicted_count","probability_score","consistency","trend","historical_total"]].rename(columns={
                    "section":"Section","topic":"Topic","predicted_count":"Expected","probability_score":"Score",
                    "consistency":"Consistency","trend":"Trend","historical_total":"Historical"
                }), use_container_width=True, hide_index=True,
            )

            st.markdown("#### 📂 Section Breakdown")
            for sec in pdf["section"].unique():
                sp = pdf[pdf["section"] == sec]
                with st.expander(f"📌 {sec} — {sp['predicted_count'].sum()} Qs"):
                    for r, (_, p) in enumerate(sp.iterrows(), 1):
                        ic = "🔼" if "Rising" in p["trend"] else "🔽" if "Falling" in p["trend"] else "➡️"
                        pr = "🔴 MUST DO" if r <= 2 else ("🟠 HIGH" if r <= 4 else "🟡 MEDIUM")
                        st.markdown(f"{ic} **{p['topic']}** — {p['predicted_count']} Qs | Score: {p['probability_score']:.0f} | {pr}")

            if st.session_state.sample_questions:
                st.markdown("#### 📝 Sample Questions")
                for key, qs in st.session_state.sample_questions.items():
                    with st.expander(f"📌 {key}"):
                        for i, q in enumerate(qs, 1):
                            st.markdown(f"**Q{i}:** {q}")

            if method != CategorizationMethod.RULE_BASED.value and api_key:
                st.markdown("---")
                if st.button("🤖 Generate AI Questions"):
                    with st.spinner("Generating calibrated questions from PYQ patterns..."):
                        try:
                            ac = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
                            aiq = generate_sample_questions_ai(
                                st.session_state.predictions, exam_type, ac._call_ai, 8, 3,
                                categorized=st.session_state.categorized,
                            )
                            st.session_state.sample_questions = aiq
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# TAB: MOCK TEST
# ═════════════════════════════════════════════════════════════════════════════
with tab_mock:
    st.markdown("### 📝 Generate Mock Test")
    st.caption("AI generates exam-level questions based on your PYQ analysis — download as a printable PDF")

    needs_data = not st.session_state.predictions
    needs_ai = method == CategorizationMethod.RULE_BASED.value or (not api_key and method != CategorizationMethod.OLLAMA.value)

    if needs_data:
        st.markdown('<div class="tip-box"><strong>📝 Upload papers first</strong> in <strong>📁 Upload</strong>, then generate predictions in <strong>🔮 Predictions</strong> before creating a mock test.</div>', unsafe_allow_html=True)
    elif needs_ai:
        st.warning("⚠️ AI provider required. Go to **sidebar → ⚙️ AI Settings** and select OpenAI / Gemini / Ollama with an API key.")
    else:
        available_sections = sorted(set(p["section"] for p in st.session_state.predictions))

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            mock_sections = st.multiselect(
                "Sections to include:",
                available_sections,
                default=available_sections,
                key="mock_sections",
            )
        with mc2:
            mock_total_qs = st.number_input(
                "Total questions:", 10, 200, 30,
                key="mock_total_qs",
                help="Total questions across all selected sections",
            )
        with mc3:
            mock_difficulty = st.selectbox(
                "Difficulty:", ["Easy", "Medium", "Hard", "Mixed"],
                index=1, key="mock_diff",
            )

        mc4, mc5 = st.columns(2)
        with mc4:
            mock_time = st.number_input("Time (minutes):", 10, 300, 120, key="mock_time")
        with mc5:
            mock_set = st.number_input("Set number:", 1, 99, 1, key="mock_set")

        if st.button("🚀 Generate Mock Test", type="primary", use_container_width=True, key="mock_gen_btn"):
            ac = AICategorizer(load_taxonomy(exam_type), _get_provider(method), api_key, model_name)
            progress = st.progress(0, text="Preparing...")

            def _mock_progress(cur, tot, msg):
                progress.progress(min((cur + 1) / max(tot + 1, 1), 0.99), text=msg)

            diff = mock_difficulty if mock_difficulty != "Mixed" else "Medium"

            mock_qs = generate_mock_test_questions(
                predictions=st.session_state.predictions,
                categorized=st.session_state.categorized,
                ai_caller=ac._call_ai,
                exam_name=exam_type,
                sections_filter=mock_sections if mock_sections else None,
                total_questions=mock_total_qs,
                difficulty=diff,
                progress_callback=_mock_progress,
            )
            st.session_state.mock_test_questions = mock_qs
            progress.progress(1.0, text="Done!")
            if not mock_qs:
                st.warning("⚠️ No questions were generated. The AI may have returned invalid output — try again or adjust settings.")
            else:
                st.rerun()

    # Display generated mock test
    if st.session_state.mock_test_questions:
        mock_qs = st.session_state.mock_test_questions
        st.success(f"✅ Mock test generated: {len(mock_qs)} questions")

        # Stats
        sec_counts = {}
        for q in mock_qs:
            sec_counts[q.section] = sec_counts.get(q.section, 0) + 1
        stat_cols = st.columns(min(len(sec_counts) + 1, 5))
        with stat_cols[0]:
            st.metric("Total Qs", len(mock_qs))
        for i, (sec, cnt) in enumerate(sorted(sec_counts.items()), 1):
            if i < len(stat_cols):
                with stat_cols[i]:
                    st.metric(sec[:18], cnt)

        # Download PDF
        st.markdown("---")
        set_num = st.session_state.get("mock_set", 1)
        time_min = st.session_state.get("mock_time", 120)

        pdf_bytes = export_mock_test_pdf(
            questions=mock_qs,
            exam_name=exam_type,
            set_number=set_num,
            time_minutes=time_min,
        )
        st.download_button(
            "📥 Download Mock Test PDF",
            data=pdf_bytes,
            file_name=f"{exam_type.replace(' ', '_')}_Mock_Test_Set{set_num}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )

        # Preview questions
        st.markdown("---")
        st.markdown("#### 👁️ Preview Questions")
        current_section = None
        for qi, q in enumerate(mock_qs):
            if q.section != current_section:
                current_section = q.section
                st.markdown(f"##### 📌 {current_section}")
            with st.expander(f"Q{qi+1}. {q.text[:80]}{'...' if len(q.text) > 80 else ''} [{q.topic}]"):
                st.markdown(f"**{q.text}**")
                for opt in q.options:
                    st.markdown(f"&ensp;{opt}")
                correct_letter = chr(ord('a') + q.correct_answer) if 0 <= q.correct_answer < len(q.options) else '?'
                st.markdown(f"**Answer: ({correct_letter})**")
                if q.explanation:
                    st.caption(f"💡 {q.explanation}")

        st.markdown("---")
        if st.button("🗑️ Clear Mock Test", key="mock_clear"):
            st.session_state.mock_test_questions = []
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# TAB: STUDY PLAN
# ═════════════════════════════════════════════════════════════════════════════
with tab_study:
    st.markdown("### 📖 Study Plan")
    st.caption(f"Week-by-week preparation guide for {exam_type}")

    plan_phase = st.selectbox("Phase:", phases, key="sp")
    plan = get_study_plan(exam_type, plan_phase)

    if plan:
        st.markdown(f"**Duration:** {plan['total_weeks']} weeks")
        st.markdown("---")
        for e in plan["plan"]:
            with st.container(border=True):
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"### Week {e['week']}")
                    st.caption(f"{e['hours_per_day']}h/day")
                with c2:
                    st.markdown(f"**{e['focus']}**")
                    st.markdown(f"*Topics:* {e['topics']}")
    else:
        st.markdown("""
        <div class="tip-box">
            <strong>📖 General Preparation Strategy</strong><br><br>
            <strong>Weeks 1-3:</strong> Quant basics — Percentage, Ratio, SI/CI, Profit & Loss<br>
            <strong>Weeks 4-6:</strong> Core — DI, Series, Seating, Puzzles, Syllogism<br>
            <strong>Weeks 7-8:</strong> English + GA — RC, Cloze, Banking Awareness, Static GK<br>
            <strong>Weeks 9-10:</strong> Current Affairs — Last 6 months focus<br>
            <strong>Weeks 11-12:</strong> Mocks + Revision — 1 mock/day, analyze every mistake<br><br>
            <strong>💡 Tips:</strong> Focus 60% time on high-probability topics. Take 15+ mocks. Revise CA daily in last month.
        </div>
        """, unsafe_allow_html=True)

    # Show last 30-day plan for RBI Grade B
    if exam_type == "RBI Grade B":
        st.markdown("---")
        st.markdown("### 📅 Last 30 Days Intensive Plan")
        l30_phase = st.radio("Phase:", ["Phase 1", "Phase 2"], horizontal=True, key="l30sp")
        l30 = get_last30_plan(l30_phase)
        if l30:
            for w in l30["weeks"]:
                with st.container(border=True):
                    st.markdown(f"#### {w['week']}")
                    st.markdown(f"**Target:** {w['targets']}")
                    for s in w["daily_schedule"]:
                        st.markdown(f"- {s}")

    if st.session_state.predictions:
        st.markdown("---")
        st.markdown("### 🎯 Your Priority Topics")
        st.caption("Based on your paper analysis — focus here first")
        for i, p in enumerate(st.session_state.predictions[:10], 1):
            pr = "🔴" if i <= 3 else ("🟠" if i <= 6 else "🟡")
            st.markdown(f"{pr} **#{i} {p['topic']}** ({p['section']}) — Score: {p['probability_score']:.0f}")


# ═════════════════════════════════════════════════════════════════════════════
# TAB: EXPORT
# ═════════════════════════════════════════════════════════════════════════════
with tab_export:
    if not st.session_state.categorized:
        st.markdown('<div class="tip-box"><strong>💾 No data to export.</strong> Upload & process papers first.</div>', unsafe_allow_html=True)
    else:
        st.markdown("### 💾 Download Reports")
        st.caption("Export analysis in multiple formats")

        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.markdown("#### 📗 Excel")
                st.caption("Multi-sheet: frequency matrix, rankings, trends, predictions, raw data")
                if st.button("Generate", use_container_width=True, key="gx"):
                    with st.spinner("Building..."):
                        data = export_to_excel(st.session_state.categorized, st.session_state.predictions or None, st.session_state.sample_questions or None)
                        st.download_button("📥 Download .xlsx", data=data, file_name=f"{exam_type.replace(' ','_')}_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with c2:
            with st.container(border=True):
                st.markdown("#### 🌐 HTML")
                st.caption("Interactive dashboard — open in any browser, no install needed")
                if st.button("Generate", use_container_width=True, key="gh"):
                    with st.spinner("Building..."):
                        data = export_to_html(st.session_state.categorized, st.session_state.predictions or None, exam_name=exam_type)
                        st.download_button("📥 Download .html", data=data, file_name=f"{exam_type.replace(' ','_')}_dashboard.html", mime="text/html", use_container_width=True)
        with c3:
            with st.container(border=True):
                st.markdown("#### 📕 PDF")
                st.caption("Formatted report with summary, tables, predictions & study priority")
                if st.button("Generate", use_container_width=True, key="gp"):
                    with st.spinner("Building..."):
                        data = export_to_pdf(st.session_state.categorized, st.session_state.predictions or None, st.session_state.sample_questions or None, exam_name=exam_type)
                        st.download_button("📥 Download .pdf", data=data, file_name=f"{exam_type.replace(' ','_')}_report.pdf", mime="application/pdf", use_container_width=True)
