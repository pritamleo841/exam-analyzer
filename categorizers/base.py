"""
Abstract base class for question categorizers.
"""
from abc import ABC, abstractmethod
from config import Question, CategorizedQuestion


class BaseCategorizer(ABC):
    """Base class for all categorizers."""

    def __init__(self, taxonomy: dict):
        """Initialize with an exam taxonomy dict (loaded from JSON)."""
        self.taxonomy = taxonomy

    @abstractmethod
    def categorize(self, question: Question) -> CategorizedQuestion:
        """Categorize a single question."""
        ...

    def categorize_batch(self, questions: list[Question]) -> list[CategorizedQuestion]:
        """Categorize a list of questions. Default: process one at a time."""
        return [self.categorize(q) for q in questions]
