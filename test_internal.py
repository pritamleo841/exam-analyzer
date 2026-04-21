"""Internal test — import check + unit tests for all new modules."""
import sys
import traceback

sys.path.insert(0, ".")

errors = []

def test(label, fn):
    try:
        fn()
        print(f"  OK  {label}")
    except Exception as e:
        msg = f"FAIL  {label}: {e}"
        print(f"  {msg}")
        errors.append(msg)
        traceback.print_exc()


# ── 1. Import tests ────────────────────────────────────────────
print("=== IMPORT TESTS ===")
test("config", lambda: __import__("config"))
test("categorizers.prompts", lambda: __import__("categorizers.prompts"))
test("categorizers.base", lambda: __import__("categorizers.base"))
test("categorizers.rule_categorizer", lambda: __import__("categorizers.rule_categorizer"))
test("categorizers.ai_categorizer", lambda: __import__("categorizers.ai_categorizer"))
test("parsers.pdf_parser", lambda: __import__("parsers.pdf_parser"))
test("parsers.text_parser", lambda: __import__("parsers.text_parser"))
test("analyzers.frequency", lambda: __import__("analyzers.frequency"))
test("analyzers.trends", lambda: __import__("analyzers.trends"))
test("analyzers.predictor", lambda: __import__("analyzers.predictor"))
test("generators.ca_question_generator", lambda: __import__("generators.ca_question_generator"))
test("generators.question_generator", lambda: __import__("generators.question_generator"))
test("exporters.mock_test_export", lambda: __import__("exporters.mock_test_export"))
test("exporters.pdf_export", lambda: __import__("exporters.pdf_export"))
test("exporters.excel_export", lambda: __import__("exporters.excel_export"))
test("exporters.html_export", lambda: __import__("exporters.html_export"))
test("data.current_affairs", lambda: __import__("data.current_affairs"))
test("data.rbi_grade_b", lambda: __import__("data.rbi_grade_b"))

# ── 2. Config dataclass tests ──────────────────────────────────
print("\n=== DATACLASS TESTS ===")
from config import Question, CategorizedQuestion, Difficulty, GeneratedQuestion

def test_question():
    q = Question(text="What is 2+2?", question_number=1, year=2024, phase="Phase 1", exam_type="RBI Grade B")
    assert q.text == "What is 2+2?"
    assert q.data_set_id is None

test("Question dataclass", test_question)

def test_generated_question():
    gq = GeneratedQuestion(
        text="What is 2+2?",
        options=["(a) 2", "(b) 3", "(c) 4", "(d) 5", "(e) 6"],
        correct_answer=2,
        explanation="2+2=4",
        section="Quantitative Aptitude",
        topic="Simplification & Approximation",
        difficulty="Easy",
    )
    assert gq.correct_answer == 2
    assert gq.section == "Quantitative Aptitude"
    assert gq.data_set_text == ""

test("GeneratedQuestion dataclass", test_generated_question)

# ── 3. Prompt generation tests ─────────────────────────────────
print("\n=== PROMPT TESTS ===")
from categorizers.prompts import (
    get_categorization_prompt, get_question_generation_prompt,
    get_calibrated_question_prompt, get_ca_question_generation_prompt,
)

def test_categorization_prompt():
    taxonomy = {"sections": [{"name": "Quant", "topics": [{"name": "DI", "sub_topics": ["Bar"]}]}]}
    p = get_categorization_prompt(taxonomy, ["What is 2+2?"])
    assert "TAXONOMY" in p
    assert "QUESTION 1" in p
    assert len(p) > 100

test("get_categorization_prompt", test_categorization_prompt)

def test_generation_prompt():
    p = get_question_generation_prompt("DI", "Bar Chart", "Quant", "RBI Grade B", "Medium", 3)
    assert "RBI Grade B" in p
    assert "DI" in p

test("get_question_generation_prompt", test_generation_prompt)

def test_calibrated_prompt():
    p = get_calibrated_question_prompt(
        topic="Data Interpretation", sub_topic="Table DI",
        section="Quantitative Aptitude", exam_name="RBI Grade B",
        count=2, example_questions=["Sample Q about a table..."],
        difficulty_distribution={"Easy": 10, "Medium": 60, "Hard": 30},
        topic_pattern_info="DI sets have 5 questions each",
    )
    assert "ACTUAL previous year" in p
    assert "EXAMPLE 1" in p
    assert "Table DI" in p
    assert "Easy: 10%" in p

test("get_calibrated_question_prompt", test_calibrated_prompt)

def test_calibrated_prompt_no_examples():
    p = get_calibrated_question_prompt(
        topic="Number Series", sub_topic="",
        section="Quantitative Aptitude", exam_name="RBI Grade B",
        count=3,
    )
    assert "EXAMPLE" not in p
    assert "Number Series" in p

test("calibrated_prompt without examples", test_calibrated_prompt_no_examples)

def test_ca_prompt():
    p = get_ca_question_generation_prompt(
        ca_text="RBI raised repo rate to 6.5% in April 2026.",
        exam_name="RBI Grade B", category="RBI & Monetary Policy",
        count=5, difficulty="Medium",
    )
    assert "repo rate" in p
    assert "RBI & Monetary Policy" in p
    assert "JSON array" in p

test("get_ca_question_generation_prompt", test_ca_prompt)

def test_ca_prompt_all():
    p = get_ca_question_generation_prompt(
        ca_text="Some text", exam_name="RBI Grade B", category="All",
    )
    assert "Focus primarily" not in p

test("ca_prompt with category=All", test_ca_prompt_all)

# ── 4. Topic-specific rules test ───────────────────────────────
print("\n=== TOPIC RULES TESTS ===")
from categorizers.prompts import _get_topic_specific_rules

def test_topic_rules():
    topics_with_rules = [
        "Data Interpretation", "Number Series", "Simplification & Approximation",
        "Quadratic Equations", "Seating Arrangement", "Puzzles", "Syllogism",
        "Inequality", "Coding-Decoding", "Blood Relations",
        "Arithmetic Word Problems", "Order & Ranking", "Input-Output",
    ]
    for t in topics_with_rules:
        r = _get_topic_specific_rules(t, "Test")
        assert len(r) > 50, f"No rules for {t}"

    # Unknown topic should get a generic rule
    r = _get_topic_specific_rules("Unknown Topic XYZ", "Section")
    assert "Unknown Topic XYZ" in r

test("topic-specific rules (13 topics)", test_topic_rules)

# ── 5. Question generator unit tests ──────────────────────────
print("\n=== GENERATOR TESTS ===")
from generators.question_generator import (
    collect_pyq_examples, compute_difficulty_distribution, _parse_generated_json,
)

def test_collect_pyq():
    q1 = Question(text="DI Q1", question_number=1, year=2023, phase="Phase 1", exam_type="RBI Grade B")
    q2 = Question(text="Series Q1", question_number=2, year=2023, phase="Phase 1", exam_type="RBI Grade B")
    cq1 = CategorizedQuestion(question=q1, section="Quant", topic="DI")
    cq2 = CategorizedQuestion(question=q2, section="Quant", topic="Series")
    examples = collect_pyq_examples([cq1, cq2], "DI", "Quant", max_examples=5)
    assert len(examples) == 1
    assert examples[0] == "DI Q1"

test("collect_pyq_examples", test_collect_pyq)

def test_difficulty_dist():
    q = Question(text="Q", question_number=1, year=2023, phase="P1", exam_type="RBI")
    cqs = [
        CategorizedQuestion(question=q, section="Q", topic="DI", difficulty=Difficulty.EASY),
        CategorizedQuestion(question=q, section="Q", topic="DI", difficulty=Difficulty.MEDIUM),
        CategorizedQuestion(question=q, section="Q", topic="DI", difficulty=Difficulty.MEDIUM),
        CategorizedQuestion(question=q, section="Q", topic="DI", difficulty=Difficulty.HARD),
    ]
    dist = compute_difficulty_distribution(cqs, "DI")
    assert dist["Easy"] == 25
    assert dist["Medium"] == 50
    assert dist["Hard"] == 25

test("compute_difficulty_distribution", test_difficulty_dist)

def test_difficulty_dist_empty():
    dist = compute_difficulty_distribution([], "DI")
    assert dist == {"Easy": 10, "Medium": 60, "Hard": 30}

test("difficulty_distribution (empty)", test_difficulty_dist_empty)

def test_parse_json():
    raw = '''[
        {"question": "What is 2+2?", "options": ["(a) 2","(b) 3","(c) 4","(d) 5","(e) 6"], "answer": 2, "explanation": "Math"},
        {"question": "Bad Q", "options": ["a"], "answer": 0}
    ]'''
    result = _parse_generated_json(raw)
    assert len(result) == 1  # second one has too few options
    assert result[0]["question"] == "What is 2+2?"

test("_parse_generated_json", test_parse_json)

def test_parse_json_with_fences():
    raw = '```json\n[{"question":"Q","options":["a","b","c","d","e"],"answer":0,"explanation":"E"}]\n```'
    result = _parse_generated_json(raw)
    assert len(result) == 1

test("_parse_generated_json (markdown fences)", test_parse_json_with_fences)

def test_parse_json_invalid():
    assert _parse_generated_json("not json at all") == []

test("_parse_generated_json (invalid)", test_parse_json_invalid)

# ── 6. CA generator tests ─────────────────────────────────────
print("\n=== CA GENERATOR TESTS ===")
from generators.ca_question_generator import _parse_ca_response, _split_text_into_chunks

def test_parse_ca_response():
    raw = '[{"question":"Q1","options":["a","b","c","d"],"answer":0,"explanation":"E","category":"General"}]'
    result = _parse_ca_response(raw)
    assert len(result) == 1
    assert result[0]["category"] == "General"

test("_parse_ca_response", test_parse_ca_response)

def test_parse_ca_response_invalid_answer():
    raw = '[{"question":"Q","options":["a","b","c","d"],"answer":5,"explanation":"E","category":"G"}]'
    result = _parse_ca_response(raw)
    assert len(result) == 0

test("_parse_ca_response (invalid answer idx)", test_parse_ca_response_invalid_answer)

def test_parse_ca_response_bad_json():
    assert _parse_ca_response("not json") == []

test("_parse_ca_response (bad json)", test_parse_ca_response_bad_json)

def test_split_chunks():
    text = "\n\n".join([f"Paragraph {i} with some text content" for i in range(50)])
    chunks = _split_text_into_chunks(text, 200)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 250  # Allow some overflow due to paragraph boundaries

test("_split_text_into_chunks", test_split_chunks)

def test_split_chunks_small():
    chunks = _split_text_into_chunks("Short text", 10000)
    assert len(chunks) == 1

test("_split_text_into_chunks (small)", test_split_chunks_small)

# ── 7. Mock test PDF export tests ─────────────────────────────
print("\n=== MOCK TEST PDF TESTS ===")
from exporters.mock_test_export import export_mock_test_pdf, _escape_xml

def test_escape_xml():
    assert _escape_xml("a < b & c > d") == "a &lt; b &amp; c &gt; d"
    assert _escape_xml("normal text") == "normal text"

test("_escape_xml", test_escape_xml)

def test_mock_pdf_generation():
    qs = [
        GeneratedQuestion(
            text="What is the value of 15% of 200?",
            options=["(a) 20", "(b) 25", "(c) 30", "(d) 35", "(e) 40"],
            correct_answer=2,
            explanation="15% of 200 = 30",
            section="Quantitative Aptitude",
            topic="Simplification & Approximation",
            difficulty="Easy",
        ),
        GeneratedQuestion(
            text="If A sits 3rd to the left of B in a circular arrangement of 8 persons, who sits opposite A?",
            options=["(a) C", "(b) D", "(c) E", "(d) F", "(e) G"],
            correct_answer=1,
            explanation="In a circular arrangement of 8, opposite = 4 seats away.",
            section="Reasoning",
            topic="Seating Arrangement",
            difficulty="Medium",
        ),
        GeneratedQuestion(
            text="What comes next? 2, 6, 18, 54, ?",
            options=["(a) 108", "(b) 162", "(c) 150", "(d) 216", "(e) 180"],
            correct_answer=1,
            explanation="Each number x3: 54x3=162",
            section="Quantitative Aptitude",
            topic="Number Series",
            difficulty="Medium",
        ),
    ]
    pdf_bytes = export_mock_test_pdf(qs, exam_name="RBI Grade B", set_number=1, time_minutes=120)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes[:5] == b"%PDF-"

test("export_mock_test_pdf (3 Qs)", test_mock_pdf_generation)

def test_mock_pdf_empty():
    try:
        export_mock_test_pdf([], exam_name="RBI Grade B")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

test("export_mock_test_pdf (empty)", test_mock_pdf_empty)

def test_mock_pdf_special_chars():
    qs = [
        GeneratedQuestion(
            text="If x > y and y < z, what is the relationship between x & z?",
            options=["(a) x > z", "(b) x < z", "(c) x = z", "(d) Cannot determine", "(e) x >= z"],
            correct_answer=3,
            explanation="x>y and y<z doesn't give x vs z relationship",
            section="Reasoning",
            topic="Inequality",
            difficulty="Hard",
        ),
    ]
    pdf_bytes = export_mock_test_pdf(qs)
    assert len(pdf_bytes) > 500
    assert pdf_bytes[:5] == b"%PDF-"

test("export_mock_test_pdf (special chars)", test_mock_pdf_special_chars)

# ── 8. PDF parser OCR fallback chain test ─────────────────────
print("\n=== PDF PARSER TESTS ===")
from parsers.pdf_parser import extract_text_from_pdf, _try_ocr, _try_ai_vision

def test_parser_text_pdf():
    # Create a minimal valid-ish text PDF to test the chain
    # (pdfplumber and pymupdf should handle this)
    try:
        extract_text_from_pdf(b"not a pdf at all")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Could not extract" in str(e)

test("pdf_parser rejects garbage bytes", test_parser_text_pdf)

def test_ocr_import_graceful():
    # _try_ocr should return "" if pytesseract is not installed, not crash
    result = _try_ocr(b"not a pdf")
    assert result == ""

test("_try_ocr graceful on missing deps", test_ocr_import_graceful)

def test_ai_vision_no_caller():
    # _try_ai_vision should return "" if no pdf2image
    result = _try_ai_vision(b"not a pdf", lambda x: "text")
    assert result == ""

test("_try_ai_vision graceful fallback", test_ai_vision_no_caller)

# ── 9. Predictor with calibrated call path ────────────────────
print("\n=== PREDICTOR TESTS ===")
from analyzers.predictor import generate_sample_questions_ai

def test_predictor_calibrated_path():
    """Verify the calibrated path doesn't crash when categorized is provided."""
    predictions = [{"section": "Quant", "topic": "DI", "predicted_count": 5, "probability_score": 80.0,
                    "consistency": "100%", "trend": "Stable", "historical_total": 25}]
    q = Question(text="DI sample Q", question_number=1, year=2024, phase="P1", exam_type="RBI")
    cqs = [CategorizedQuestion(question=q, section="Quant", topic="DI")]

    call_count = [0]
    def fake_ai(prompt):
        call_count[0] += 1
        assert "ACTUAL previous year" in prompt  # Should use calibrated prompt
        return '[]'  # Empty but valid

    result = generate_sample_questions_ai(predictions, "RBI Grade B", fake_ai, 1, 2, categorized=cqs)
    assert call_count[0] == 1
    assert "Quant > DI" in result

test("predictor uses calibrated prompt with PYQ", test_predictor_calibrated_path)

def test_predictor_uncalibrated_path():
    """Without categorized, should use the basic prompt."""
    predictions = [{"section": "Quant", "topic": "DI", "predicted_count": 5, "probability_score": 80.0,
                    "consistency": "100%", "trend": "Stable", "historical_total": 25}]
    def fake_ai(prompt):
        assert "ACTUAL previous year" not in prompt
        return 'Q: What is 2+2?\n(a) 2\n(b) 3\n(c) 4\n(d) 5\n(e) 6\nAnswer: c'

    result = generate_sample_questions_ai(predictions, "RBI Grade B", fake_ai, 1, 2)
    assert "Quant > DI" in result

test("predictor uses basic prompt without PYQ", test_predictor_uncalibrated_path)

# ── 10. Question generator orchestration ─────────────────────
print("\n=== MOCK TEST GENERATOR TESTS ===")
from generators.question_generator import generate_mock_test_questions

def test_generate_mock_questions():
    """Simulate mock test generation with a fake AI caller."""
    predictions = [
        {"section": "Quantitative Aptitude", "topic": "Number Series", "predicted_count": 3,
         "probability_score": 70, "consistency": "80%", "trend": "Stable", "historical_total": 10},
        {"section": "Reasoning", "topic": "Syllogism", "predicted_count": 2,
         "probability_score": 60, "consistency": "70%", "trend": "Stable", "historical_total": 8},
    ]
    q = Question(text="Series Q", question_number=1, year=2024, phase="P1", exam_type="RBI")
    cqs = [CategorizedQuestion(question=q, section="Quantitative Aptitude", topic="Number Series")]

    def fake_ai(prompt):
        return '''[
            {"question":"What comes next: 2, 5, 11, 23, ?","options":["(a) 35","(b) 47","(c) 45","(d) 46","(e) 48"],"answer":1,"explanation":"Pattern: x2+1","difficulty":"Medium","sub_topic":"Missing Number"},
            {"question":"Find wrong: 3, 7, 15, 31, 65, 127","options":["(a) 7","(b) 15","(c) 31","(d) 65","(e) 127"],"answer":3,"explanation":"Should be 63","difficulty":"Hard","sub_topic":"Wrong Number"}
        ]'''

    result = generate_mock_test_questions(
        predictions=predictions, categorized=cqs, ai_caller=fake_ai,
        exam_name="RBI Grade B", total_questions=5,
    )
    assert len(result) > 0
    assert all(isinstance(q, GeneratedQuestion) for q in result)
    assert result[0].text == "What comes next: 2, 5, 11, 23, ?"

test("generate_mock_test_questions", test_generate_mock_questions)

def test_generate_mock_section_filter():
    """Only generate for selected sections."""
    predictions = [
        {"section": "Quantitative Aptitude", "topic": "DI", "predicted_count": 5,
         "probability_score": 80, "consistency": "100%", "trend": "Stable", "historical_total": 25},
        {"section": "Reasoning", "topic": "Puzzles", "predicted_count": 3,
         "probability_score": 60, "consistency": "80%", "trend": "Stable", "historical_total": 15},
    ]
    def fake_ai(prompt):
        return '[]'

    result = generate_mock_test_questions(
        predictions=predictions, categorized=[], ai_caller=fake_ai,
        sections_filter=["Reasoning"], total_questions=3,
    )
    # Should only call for Reasoning topics
    assert isinstance(result, list)

test("generate_mock_questions (section filter)", test_generate_mock_section_filter)

def test_generate_mock_empty_predictions():
    result = generate_mock_test_questions(
        predictions=[], categorized=[], ai_caller=lambda p: "[]", total_questions=10,
    )
    assert result == []

test("generate_mock_questions (empty preds)", test_generate_mock_empty_predictions)

# ── Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
if errors:
    print(f"FAILED: {len(errors)} test(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")
    sys.exit(0)
