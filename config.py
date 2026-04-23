"""
Exam Paper Analyzer - Configuration & Data Models
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    UNKNOWN = "Unknown"


class CategorizationMethod(str, Enum):
    RULE_BASED = "Rule-Based (Free, Offline)"
    OPENAI = "OpenAI GPT"
    GEMINI = "Google Gemini"
    OLLAMA = "Ollama (Local, Free)"


@dataclass
class Question:
    """A single parsed question from a paper."""
    text: str
    question_number: int
    year: int
    phase: str  # "Phase 1", "Phase 2", "Prelims", "Mains", etc.
    exam_type: str  # "RBI Grade B", "SEBI Grade A", etc.
    section_hint: str = ""  # Detected from paper headers if available
    data_set_id: Optional[str] = None  # Groups DI/passage questions together


@dataclass
class CategorizedQuestion:
    """A question with its categorization results."""
    question: Question
    section: str  # "Quantitative Aptitude", "Reasoning", etc.
    topic: str  # "Data Interpretation", "Seating Arrangement", etc.
    sub_topic: str = ""  # "Bar Chart DI", "Circular Seating", etc.
    difficulty: Difficulty = Difficulty.UNKNOWN
    confidence: float = 0.0  # 0-1 confidence of categorization


@dataclass
class TopicInfo:
    """Topic metadata from a taxonomy."""
    name: str
    sub_topics: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class SectionInfo:
    """Section metadata from a taxonomy."""
    name: str
    topics: list[TopicInfo] = field(default_factory=list)
    typical_question_count: int = 0


@dataclass
class ExamTaxonomy:
    """Full taxonomy definition for an exam type."""
    exam_name: str
    phases: list[str] = field(default_factory=list)
    sections: list[SectionInfo] = field(default_factory=list)
    marks_per_question: float = 1.0
    negative_marking: float = 0.25
    total_time_minutes: int = 120


@dataclass
class GeneratedQuestion:
    """A single AI-generated question for a mock test."""
    text: str
    options: list[str]  # 5 options, e.g. ["(a) ...", "(b) ...", ...]
    correct_answer: int  # 0-based index into options
    explanation: str = ""
    section: str = ""
    topic: str = ""
    sub_topic: str = ""
    difficulty: str = "Medium"
    data_set_text: str = ""  # Shared context for DI/puzzle sets


# Supported exam types
EXAM_TYPES = [
    "RBI Grade B",
    "SEBI Grade A",
    "NABARD Grade A",
    "IBPS PO",
    "IBPS Clerk",
    "SBI PO",
    "SBI Clerk",
    "Custom",
]

# Phase options per exam
PHASE_OPTIONS = {
    "RBI Grade B": ["Phase 1", "Phase 2"],
    "SEBI Grade A": ["Paper 1", "Paper 2"],
    "NABARD Grade A": ["Prelims", "Mains"],
    "IBPS PO": ["Prelims", "Mains"],
    "IBPS Clerk": ["Prelims", "Mains"],
    "SBI PO": ["Prelims", "Mains"],
    "SBI Clerk": ["Prelims", "Mains"],
    "Custom": ["Phase 1", "Phase 2"],
}

# Section options per exam + phase
SECTION_OPTIONS = {
    "RBI Grade B": {
        "Phase 1": ["Quantitative Aptitude", "Reasoning", "English Language", "General Awareness"],
        "Phase 2": ["Economic & Social Issues", "Finance & Management", "English (Descriptive)"],
    },
    "SEBI Grade A": {
        "Paper 1": ["Quantitative Aptitude", "Reasoning", "English Language", "General Awareness"],
        "Paper 2": ["Commerce/Economics/Law/IT/Engineering"],
    },
    "NABARD Grade A": {
        "Prelims": ["Quantitative Aptitude", "Reasoning", "English Language", "General Awareness",
                     "Computer Knowledge", "Agriculture & Rural Development"],
        "Mains": ["Economic & Social Issues", "Agriculture & Rural Development (Descriptive)",
                   "English (Descriptive)"],
    },
    "IBPS PO": {
        "Prelims": ["Quantitative Aptitude", "Reasoning", "English Language"],
        "Mains": ["Quantitative Aptitude", "Reasoning & Computer Aptitude",
                   "English Language", "General/Economy/Banking Awareness", "Data Analysis & Interpretation"],
    },
    "IBPS Clerk": {
        "Prelims": ["Quantitative Aptitude", "Reasoning", "English Language"],
        "Mains": ["Quantitative Aptitude", "Reasoning & Computer Aptitude",
                   "English Language", "General/Financial Awareness"],
    },
    "SBI PO": {
        "Prelims": ["Quantitative Aptitude", "Reasoning", "English Language"],
        "Mains": ["Quantitative Aptitude", "Reasoning & Computer Aptitude",
                   "English Language", "General/Economy/Banking Awareness", "Data Analysis & Interpretation"],
    },
    "SBI Clerk": {
        "Prelims": ["Quantitative Aptitude", "Reasoning", "English Language"],
        "Mains": ["Quantitative Aptitude", "Reasoning & Computer Aptitude",
                   "English Language", "General/Financial Awareness"],
    },
    "Custom": {
        "Phase 1": ["Section 1", "Section 2", "Section 3"],
        "Phase 2": ["Section 1", "Section 2"],
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# CA PREDICTOR SETTINGS
# ═════════════════════════════════════════════════════════════════════════════

# Persistent storage location
STORAGE_BASE_PATH = r"C:\exam_analyzer_data"

# Documents folder (in-repo folder for PDFs)
import os as _os
DOCUMENTS_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "documents")
CA_DOCUMENTS_DIR = _os.path.join(DOCUMENTS_DIR, "current_affairs")
PYQ_DOCUMENTS_DIR = _os.path.join(DOCUMENTS_DIR, "previous_year_papers")

# Months available for CA upload
CA_MONTHS = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]

# CA categories used for prediction/sectioning
CA_SECTIONS = [
    "Union Budget",
    "Economic Survey",
    "RBI & Monetary Policy",
    "Banking & Finance",
    "Reports & Indices",
    "Government Schemes",
    "International Organizations & Summits",
    "Financial Markets & Regulations",
    "Social Issues & Development",
    "Appointments & Awards",
    "Agriculture & Rural Economy",
    "External Sector & Trade",
    "Insurance & Pension",
    "Science & Technology",
    "Environment & Sustainability",
    "Defence & Security",
    "Sports & Events",
    "General",
]

# Prediction weights
PREDICTION_WEIGHTS = {
    "pyq_frequency": 0.40,   # How often this category appeared in past exams
    "ai_importance": 0.35,   # AI-assessed importance of the fact
    "recency": 0.25,         # More recent = more likely to appear
}

# Expected CA questions in RBI Grade B Phase 1 GA section
EXPECTED_CA_QUESTIONS_PHASE1 = 30
