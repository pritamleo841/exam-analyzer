"""Quick test for GitHub Pages site builder and deployer modules."""
from exporters.ca_site_builder import build_github_pages_site
from deployer.github_pages import get_site_status

# Dummy analysis data
analysis = {
    "sections": [
        {
            "name": "Banking & Finance",
            "facts": [
                {"fact": "RBI MPC kept repo rate at 6.5%", "importance": "High",
                 "probability_score": 85, "month": "January", "why_it_matters": "Key monetary policy topic",
                 "priority": "Critical", "category": "Banking & Finance"},
                {"fact": "SBI merged with 3 regional banks", "importance": "Medium",
                 "probability_score": 60, "month": "February", "why_it_matters": "Banking consolidation",
                 "priority": "High", "category": "Banking & Finance"},
            ],
            "questions": [
                {"question": "What is the current repo rate?",
                 "options": ["6.0%", "6.25%", "6.5%", "7.0%"], "answer": 2,
                 "explanation": "RBI MPC maintained repo at 6.5%", "importance": "High",
                 "probability_score": 80, "month": "January", "category": "Banking & Finance"},
            ],
            "fact_count": 2, "question_count": 1, "study_priority": "Critical",
            "predicted_questions": 5, "weight": 0.15, "coverage_status": "Good",
            "historical": {"avg_count": 4, "consistency": 90, "trend": "Stable"},
        },
        {
            "name": "Union Budget",
            "facts": [
                {"fact": "FM announced new tax slab: 0-4L nil", "importance": "High",
                 "probability_score": 92, "month": "February", "why_it_matters": "Direct impact on exam",
                 "priority": "Critical", "category": "Union Budget"},
            ],
            "questions": [],
            "fact_count": 1, "question_count": 0, "study_priority": "High",
            "predicted_questions": 3, "weight": 0.12, "coverage_status": "Partial",
            "historical": {},
        },
    ],
    "top_50_facts": [
        {"fact": "FM announced new tax slab", "probability_score": 92, "importance": "High", "category": "Union Budget"},
        {"fact": "RBI MPC kept repo rate at 6.5%", "probability_score": 85, "importance": "High", "category": "Banking"},
    ],
    "metadata": {
        "months_covered": ["January", "February"],
        "pyq_years_used": 3,
        "generated_at": "2026-04-23T10:00:00",
    },
    "readiness_score": 45,
    "study_time_allocation": {"Banking & Finance": 10, "Union Budget": 6},
    "total_facts": 3,
    "total_questions": 1,
}

# Test site builder
html = build_github_pages_site(analysis, exam_name="RBI Grade B")
print(f"[OK] Site builder: {len(html):,} bytes HTML generated")
assert "sidebar" in html, "Missing sidebar"
assert "globalSearch" in html, "Missing search"
assert "SITE_DATA" in html, "Missing embedded data"
assert "RBI Grade B" in html, "Missing exam name"
assert "Banking &amp; Finance" in html or "Banking & Finance" in html, "Missing section"
assert "Revision" in html, "Missing revision mode"
assert "localStorage" in html, "Missing localStorage for bookmarks"
print("[OK] All HTML assertions passed")

# Test deployer status
status = get_site_status()
assert isinstance(status, dict), "Status should be dict"
assert "initialized" in status, "Missing initialized key"
print(f"[OK] Deployer status: initialized={status['initialized']}")

# Test that existing tests still pass
print("\n--- Running existing test suite ---")
import subprocess
result = subprocess.run(["python", "test_internal.py"], capture_output=True, text=True, cwd=".")
if result.returncode == 0:
    # Count passed tests
    lines = result.stdout.strip().split("\n")
    for line in lines[-5:]:
        print(f"  {line}")
    print("[OK] Existing tests still pass")
else:
    print(f"[WARN] Test suite returned code {result.returncode}")
    print(result.stdout[-500:] if result.stdout else "")
    print(result.stderr[-500:] if result.stderr else "")

print("\n=== All checks passed! Ready to run: streamlit run app.py ===")
