"""
Prompt templates for AI-based question categorization.
"""


def get_categorization_prompt(taxonomy: dict, questions_text: list[str]) -> str:
    """Build a structured prompt for AI categorization of exam questions."""
    # Build topic list from taxonomy
    topic_tree = []
    for section in taxonomy.get("sections", []):
        section_name = section["name"]
        for topic in section.get("topics", []):
            sub_topics_str = ", ".join(topic.get("sub_topics", []))
            topic_tree.append(
                f"  - Section: {section_name} | Topic: {topic['name']} | "
                f"Sub-topics: {sub_topics_str}"
            )

    topic_list = "\n".join(topic_tree)

    # Build questions block
    q_block = "\n\n".join(
        f"---QUESTION {i+1}---\n{q}"
        for i, q in enumerate(questions_text)
    )

    return f"""You are an expert exam question categorizer for competitive exams in India (banking, regulatory).

Given the following topic taxonomy and a set of exam questions, categorize each question.

TAXONOMY:
{topic_list}

QUESTIONS:
{q_block}

For EACH question, respond with a JSON array. Each element must have:
- "question_index": (1-based index matching the question number above)
- "section": (exact section name from taxonomy)
- "topic": (exact topic name from taxonomy)
- "sub_topic": (best matching sub-topic, or empty string if unsure)
- "difficulty": ("Easy", "Medium", or "Hard")
- "confidence": (0.0 to 1.0, how confident you are in the categorization)

If a question doesn't match any topic, use topic="Uncategorized".
Use ONLY topic names that exist in the taxonomy above.

Respond with ONLY the JSON array, no other text.
"""


def get_question_generation_prompt(
    topic: str,
    sub_topic: str,
    section: str,
    exam_name: str,
    difficulty: str = "Medium",
    count: int = 3,
) -> str:
    """Build a prompt to generate predicted questions for a topic."""
    return f"""You are an expert question paper setter for {exam_name} exam in India.

Generate {count} realistic multiple-choice questions for:
- Section: {section}
- Topic: {topic}
- Sub-topic: {sub_topic}
- Difficulty: {difficulty}

Each question should:
1. Be similar in style and difficulty to actual {exam_name} exam questions
2. Have 5 answer options (a, b, c, d, e)
3. Include the correct answer
4. Be self-contained (include any necessary data/context within the question)

Format each question as:
Q: [question text]
(a) [option]
(b) [option]
(c) [option]
(d) [option]
(e) [option]
Answer: [correct option letter]
Explanation: [brief explanation]

Generate the questions now:
"""


def get_calibrated_question_prompt(
    topic: str,
    sub_topic: str,
    section: str,
    exam_name: str,
    difficulty: str = "Medium",
    count: int = 3,
    example_questions: list[str] | None = None,
    difficulty_distribution: dict | None = None,
    topic_pattern_info: str = "",
) -> str:
    """Build a calibrated prompt that uses PYQ examples for style matching.

    Args:
        topic: Topic name (e.g. "Data Interpretation").
        sub_topic: Sub-topic name (e.g. "Table DI").
        section: Section name (e.g. "Quantitative Aptitude").
        exam_name: Target exam.
        difficulty: Target difficulty.
        count: Number of questions to generate.
        example_questions: Actual PYQ texts for few-shot calibration.
        difficulty_distribution: e.g. {"Easy": 10, "Medium": 60, "Hard": 30}.
        topic_pattern_info: Extra context like "DI sets have 5 questions each".
    """
    # Build few-shot examples block
    examples_block = ""
    if example_questions:
        examples_block = "\n\nHere are ACTUAL previous year questions from this topic — " \
                         "match this style, complexity, and language closely:\n"
        for i, eq in enumerate(example_questions[:3], 1):
            examples_block += f"\n--- EXAMPLE {i} ---\n{eq[:500]}\n"

    # Build difficulty distribution hint
    diff_hint = ""
    if difficulty_distribution:
        parts = [f"{k}: {v}%" for k, v in difficulty_distribution.items() if v > 0]
        diff_hint = f"\nHistorical difficulty distribution for this topic: {', '.join(parts)}\n"

    # Topic-specific structural instructions
    topic_rules = _get_topic_specific_rules(topic, section)

    return f"""You are an expert question paper setter for {exam_name} exam in India.
You have deep knowledge of the exact format, difficulty, and style of {exam_name} Phase 1 papers.

Generate {count} REALISTIC multiple-choice questions for:
- Section: {section}
- Topic: {topic}
- Sub-topic: {sub_topic}
- Target difficulty: {difficulty}
{diff_hint}{topic_pattern_info}{examples_block}

{topic_rules}

STRICT FORMAT — respond with a valid JSON array. Each element:
{{
  "question": "full question text including any data/context needed",
  "options": ["(a) ...", "(b) ...", "(c) ...", "(d) ...", "(e) ..."],
  "answer": 0,
  "explanation": "step-by-step solution in 2-3 sentences",
  "difficulty": "Easy|Medium|Hard",
  "sub_topic": "{sub_topic}"
}}

"answer" is the 0-based index of the correct option.

CRITICAL RULES:
1. Questions MUST be self-contained and solvable — no placeholders like [X], [year], etc.
2. Every numerical answer must be verifiable by calculation.
3. All 5 options must be plausible (close numerical values or similar concepts).
4. Include complete data for DI (real numbers in tables/caselets).
5. Puzzles/Seating must have exactly ONE valid solution from the given clues.
6. Do NOT repeat the same question structure — vary the framing.

Respond with ONLY the JSON array, no markdown fences.
"""


def _get_topic_specific_rules(topic: str, section: str) -> str:
    """Return topic-specific generation instructions."""
    rules = {
        "Data Interpretation": """TOPIC-SPECIFIC RULES (Data Interpretation):
- Create a COMPLETE data set (table with 4-6 rows & 3-5 columns of realistic numbers).
- Write the table data directly in the question text.
- Generate 5 questions per data set, covering: ratio, percentage change, average, total, difference.
- Numbers should be realistic (e.g. production in thousands, population in lakhs).
- At least one question should require data from multiple rows/columns.""",

        "Number Series": """TOPIC-SPECIFIC RULES (Number Series):
- Each series must follow a SINGLE clear mathematical pattern (e.g. ×2+1, squares, cubes, alternating).
- Provide 5-7 numbers in the series with one missing (marked ?).
- The pattern must be deterministic — only one correct answer.
- Mix patterns: arithmetic, geometric, squared differences, alternating operations.
- For 'wrong number' type: one number should be off by a small amount.""",

        "Simplification & Approximation": """TOPIC-SPECIFIC RULES (Simplification):
- Use realistic decimal/percentage values like 34.98% of 6001 (≈35% of 6000).
- Chain 2-3 operations: addition, subtraction, multiplication, division.
- Approximation questions should have options spread 50-200 apart.
- Include BODMAS-order expressions with brackets.""",

        "Quadratic Equations": """TOPIC-SPECIFIC RULES (Quadratic Equations):
- Present as: I. x² + ax + b = 0   II. y² + cx + d = 0
- Both equations should have real integer roots.
- Options: (a) x > y, (b) x < y, (c) x ≥ y, (d) x ≤ y, (e) x = y or relationship cannot be determined.
- Ensure roots are calculable and comparison is clear.""",

        "Seating Arrangement": """TOPIC-SPECIFIC RULES (Seating Arrangement):
- Use 6-8 persons (A-H) sitting in a circle or linear row.
- Provide 5-7 clues that together yield EXACTLY ONE valid arrangement.
- Specify facing direction (center/outward for circular, north/south for linear).
- Generate 5 questions from the same arrangement: who sits opposite, how many between, etc.
- Name all persons with single letters A-H.""",

        "Puzzles": """TOPIC-SPECIFIC RULES (Puzzles):
- Use 6-8 entities with 2-3 parameters each (e.g. person, floor, color).
- Provide enough clues for EXACTLY ONE valid assignment.
- Types: floor puzzle, scheduling (days of week), box arrangement, comparison.
- Generate 5 questions from the same puzzle: who is on which floor, which day, etc.""",

        "Syllogism": """TOPIC-SPECIFIC RULES (Syllogism):
- Give 3-4 statements using: All, Some, No, Only a few, At least some.
- Provide 2 conclusions to evaluate (follows / does not follow).
- Options: (a) Only I follows, (b) Only II follows, (c) Both follow, (d) Neither follows, (e) Either I or II.
- Use Venn diagram logic to verify correctness.""",

        "Inequality": """TOPIC-SPECIFIC RULES (Inequality):
- Provide a chain: A ≥ B > C = D < E ≤ F (use 5-7 variables).
- Give 3 conclusions like I. A > D  II. F ≥ C  III. B < E.
- Options should be combinations of which conclusions are true.
- Ensure each conclusion is clearly derivable or not from the chain.""",

        "Coding-Decoding": """TOPIC-SPECIFIC RULES (Coding-Decoding):
- Show 2-3 example encodings, then ask to decode a new word.
- Pattern types: letter shifting (+1, +2, reverse), position-based, symbol substitution.
- The pattern must be consistent and deterministic.""",

        "Blood Relations": """TOPIC-SPECIFIC RULES (Blood Relations):
- Present family relationships in 3-4 sentences.
- Ask to find a specific relationship (e.g. how is A related to B?).
- Include at most 6-8 family members.
- Ensure the relationship chain leads to exactly one answer.""",

        "Arithmetic Word Problems": """TOPIC-SPECIFIC RULES (Arithmetic Word Problems):
- Use real-world scenarios: profit/loss on goods, train speeds, pipe filling, age problems.
- Numbers should yield clean answers (avoid messy fractions unless for Hard difficulty).
- Include all necessary data in the problem statement.
- Match the sub-topic: SI/CI, Time & Work, Speed & Distance, etc.""",

        "Order & Ranking": """TOPIC-SPECIFIC RULES (Order & Ranking):
- Describe relative positions/ranks of 5-7 people.
- Ask: rank from top/bottom, how many between two people, total minimum persons.
- Provide enough data for a unique answer.""",

        "Input-Output": """TOPIC-SPECIFIC RULES (Input-Output):
- Show a machine rearranging words/numbers across 3-4 steps.
- The rearrangement pattern must be consistent (e.g. sort ascending one element at a time).
- Ask for a specific step's output or the final arrangement.""",
    }
    return rules.get(topic, f"Generate high-quality {topic} questions matching {section} exam level.")


def get_ca_question_generation_prompt(
    ca_text: str,
    exam_name: str,
    category: str,
    count: int = 10,
    difficulty: str = "Medium",
) -> str:
    """Build a prompt to generate MCQs from current affairs content.

    Args:
        ca_text: Extracted text from a current affairs PDF (a monthly capsule / compilation).
        exam_name: Target exam (e.g. "RBI Grade B").
        category: CA category to focus on, or "All" for mixed.
        count: Number of questions to generate.
        difficulty: Easy / Medium / Hard.
    """
    category_hint = ""
    if category and category != "All":
        category_hint = f"\nFocus primarily on facts related to: {category}\n"

    return f"""You are an expert question paper setter for the {exam_name} exam in India.

Below is an extract from a monthly current affairs compilation / capsule.
Your task is to generate {count} **exam-quality multiple-choice questions (MCQs)** from the factual content in this material.
{category_hint}
CURRENT AFFAIRS CONTENT:
\"\"\"
{ca_text[:12000]}
\"\"\"

RULES — follow these strictly:
1. Every question must be answerable **solely from the content** above.
2. Each question must have exactly **4 options** labelled (a), (b), (c), (d).
3. Exactly **one option must be correct**. The other three must be plausible but wrong.
4. Cover a variety of facts — avoid repeating the same fact across questions.
5. Question types to include (mix them):
   - Direct factual: "Which organisation launched X?"
   - Fill-in-the-blank: "The RBI set the repo rate at ___"
   - "Which of the following is correct/incorrect" with statement combinations
   - Match-the-pair or chronological-order (occasionally)
6. Difficulty level: {difficulty}
7. Include questions on: appointments, indices/reports, policy rates, schemes, summits, agreements, banking/financial events, and international events — wherever the content provides them.

FORMAT — respond with a valid JSON array. Each element:
{{
  "question": "...",
  "options": ["(a) ...", "(b) ...", "(c) ...", "(d) ..."],
  "answer": 0,
  "explanation": "brief 1-2 sentence explanation",
  "category": "one of: RBI & Monetary Policy | Banking & Finance | Government Schemes | Appointments & Awards | International Organizations | Economic Survey | Union Budget | Financial Markets | Insurance & Pension | Agriculture & Rural | External Sector | Summits & Agreements | General"
}}

"answer" is the **0-based index** of the correct option in the "options" array.

Respond with ONLY the JSON array, no markdown fences, no extra text.
"""


def get_ca_fact_extraction_prompt(
    ca_text: str,
    exam_name: str = "RBI Grade B",
    month: str = "",
) -> str:
    """Build a prompt to extract structured facts from CA content AND generate MCQs.

    This is a more thorough extraction than get_ca_question_generation_prompt —
    it also extracts the underlying facts with importance tags.
    """
    month_hint = f" for the month of {month}" if month else ""

    return f"""You are an expert current affairs analyst specializing in Indian banking and regulatory exams, particularly {exam_name}.

Below is an extract from a monthly current affairs compilation{month_hint}.

CONTENT:
\"\"\"
{ca_text[:14000]}
\"\"\"

YOUR TASK — do TWO things:

**PART A: Extract Key Facts**
Extract every exam-relevant fact from the content. For each fact, provide:
- The fact itself (1-2 sentences, precise with numbers/names/dates)
- Category (from the list below)
- Importance: "High" (very likely in exam — policy changes, major appointments, landmark numbers),
  "Medium" (could appear — schemes, reports, indices), or "Low" (less likely but possible)
- Why it matters for {exam_name} exam (1 sentence)

**PART B: Generate MCQs**
For every HIGH importance fact, generate 1-2 MCQs.
For every MEDIUM importance fact, generate 1 MCQ.
Skip LOW importance facts for MCQs.

CATEGORIES (use exactly these names):
Union Budget | Economic Survey | RBI & Monetary Policy | Banking & Finance |
Reports & Indices | Government Schemes | International Organizations & Summits |
Financial Markets & Regulations | Social Issues & Development | Appointments & Awards |
Agriculture & Rural Economy | External Sector & Trade | Insurance & Pension |
Science & Technology | Environment & Sustainability | Defence & Security |
Sports & Events | General

FORMAT — respond with a valid JSON object:
{{
  "facts": [
    {{
      "fact": "The RBI kept the repo rate unchanged at 6.50% in its April 2026 MPC meeting.",
      "category": "RBI & Monetary Policy",
      "importance": "High",
      "why_it_matters": "RBI policy rates are asked in almost every banking exam."
    }}
  ],
  "questions": [
    {{
      "question": "What is the current repo rate as of April 2026?",
      "options": ["(a) 6.25%", "(b) 6.50%", "(c) 6.75%", "(d) 7.00%"],
      "answer": 1,
      "explanation": "The RBI MPC kept the repo rate unchanged at 6.50% in April 2026.",
      "category": "RBI & Monetary Policy",
      "importance": "High"
    }}
  ]
}}

RULES:
1. Extract ALL exam-relevant facts, not just the obvious ones — aim for 15-30 facts per chunk.
2. Questions must be answerable from the content. No guessing.
3. Each question must have exactly 4 options. Only one correct.
4. Plausible wrong options — close numbers, similar names, related organizations.
5. Include variety: direct factual, fill-in-blank, which-is-correct-incorrect, match-pair.
6. Focus on facts most likely to appear in {exam_name} Phase 1 General Awareness.

Respond with ONLY the JSON object, no markdown fences.
"""


def get_ca_predictive_prompt(
    facts_summary: str,
    pyq_pattern_summary: str,
    exam_name: str = "RBI Grade B",
    target_questions: int = 30,
) -> str:
    """Build a prompt for AI to rank facts by exam appearance probability.

    Uses both the current CA facts and historical PYQ patterns to predict
    which topics are most likely to appear.
    """
    return f"""You are a senior exam prediction analyst for {exam_name} in India.
You have deep knowledge of what topics RBI typically asks in Phase 1 General Awareness.

TASK: Rank the following current affairs facts by their probability of appearing
in the {exam_name} 2026 exam. The exam is expected to have ~{target_questions} current affairs questions.

HISTORICAL PATTERN FROM PREVIOUS YEARS:
{pyq_pattern_summary}

CURRENT AFFAIRS FACTS TO RANK:
{facts_summary}

For each fact, assign a probability score (0-100) based on:
1. Historical pattern match — does this category get questions historically?
2. Significance — is this a landmark event, policy change, or first-of-its-kind?
3. RBI relevance — directly related to banking/finance/economy?
4. Recency — more recent facts are more likely to appear
5. Uniqueness — one-time events vs routine updates

FORMAT — respond with a JSON array sorted by probability (highest first):
[
  {{
    "fact_id": 0,
    "probability": 95,
    "reasoning": "RBI policy rates asked every year. This is a key change."
  }}
]

"fact_id" is the 0-based index of the fact in the list above.
Respond with ONLY the JSON array.
"""
