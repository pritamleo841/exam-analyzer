"""
Rule-based question categorizer using keyword matching against taxonomy.
Free, offline, no API keys needed.
"""
import re
from config import Question, CategorizedQuestion, Difficulty
from categorizers.base import BaseCategorizer


class RuleCategorizer(BaseCategorizer):
    """Categorize questions using keyword pattern matching."""

    def categorize(self, question: Question) -> CategorizedQuestion:
        """Categorize a single question by matching keywords from taxonomy."""
        text = question.text.lower()
        section_hint = question.section_hint.lower()

        best_section = ""
        best_topic = ""
        best_sub_topic = ""
        best_score = 0

        for section in self.taxonomy.get("sections", []):
            section_name = section["name"]
            section_bonus = 0

            # Boost score if section_hint matches
            if section_hint and any(
                kw in section_hint
                for kw in section_name.lower().split()
                if len(kw) > 2
            ):
                section_bonus = 5

            for topic in section.get("topics", []):
                score = section_bonus
                matched_keywords = []

                for keyword in topic.get("keywords", []):
                    kw_lower = keyword.lower()
                    if kw_lower in text:
                        # Weight by keyword specificity (longer = more specific = higher weight)
                        weight = 1 + len(kw_lower.split()) * 0.5
                        score += weight
                        matched_keywords.append(keyword)

                if score > best_score:
                    best_score = score
                    best_section = section_name
                    best_topic = topic["name"]
                    # Try to determine sub-topic
                    best_sub_topic = self._match_sub_topic(
                        text, topic.get("sub_topics", [])
                    )

            # Also check topic name itself as a keyword
            for topic in section.get("topics", []):
                if topic["name"].lower() in text:
                    name_score = section_bonus + 3
                    if name_score > best_score:
                        best_score = name_score
                        best_section = section_name
                        best_topic = topic["name"]
                        best_sub_topic = self._match_sub_topic(
                            text, topic.get("sub_topics", [])
                        )

        # If no match, assign to section based on hint, topic as "Uncategorized"
        if not best_topic:
            best_section = self._guess_section_from_hint(section_hint)
            best_topic = "Uncategorized"

        # Estimate difficulty
        difficulty = self._estimate_difficulty(question.text)

        # Confidence based on score
        confidence = min(best_score / 10.0, 1.0) if best_score > 0 else 0.0

        return CategorizedQuestion(
            question=question,
            section=best_section,
            topic=best_topic,
            sub_topic=best_sub_topic,
            difficulty=difficulty,
            confidence=confidence,
        )

    def _match_sub_topic(self, text: str, sub_topics: list[str]) -> str:
        """Try to match a specific sub-topic from the list."""
        for st in sub_topics:
            # Check if sub-topic name keywords appear in the question
            st_words = [w for w in st.lower().split() if len(w) > 2]
            if st_words and all(w in text for w in st_words):
                return st

        # Partial match — any key word from sub-topic
        for st in sub_topics:
            st_words = [w for w in st.lower().split() if len(w) > 3]
            if any(w in text for w in st_words):
                return st

        return sub_topics[0] if sub_topics else ""

    def _guess_section_from_hint(self, hint: str) -> str:
        """Guess section from the section hint text."""
        hint = hint.lower()
        section_map = {
            "quant": "Quantitative Aptitude",
            "math": "Quantitative Aptitude",
            "numerical": "Quantitative Aptitude",
            "reason": "Reasoning",
            "logic": "Reasoning",
            "english": "English Language",
            "verbal": "English Language",
            "aware": "General Awareness",
            "gk": "General Awareness",
            "ga": "General Awareness",
            "current": "General Awareness",
            "computer": "Computer Knowledge",
        }
        for key, section in section_map.items():
            if key in hint:
                return section
        return "Unknown Section"

    def _estimate_difficulty(self, text: str) -> Difficulty:
        """Rough difficulty estimate based on text characteristics."""
        text_lower = text.lower()
        word_count = len(text.split())

        hard_indicators = 0
        easy_indicators = 0

        # Length-based
        if word_count > 150:
            hard_indicators += 2
        elif word_count < 40:
            easy_indicators += 1

        # Complexity keywords
        hard_keywords = [
            "probability", "permutation", "combination", "if and only if",
            "maximum possible", "minimum possible", "at most", "at least",
            "neither", "except", "unless", "necessarily",
        ]
        easy_keywords = [
            "simplify", "find the value", "what is", "how many",
        ]

        for kw in hard_keywords:
            if kw in text_lower:
                hard_indicators += 1
        for kw in easy_keywords:
            if kw in text_lower:
                easy_indicators += 1

        if hard_indicators >= 3:
            return Difficulty.HARD
        elif hard_indicators >= 1 and easy_indicators == 0:
            return Difficulty.MEDIUM
        elif easy_indicators >= 1:
            return Difficulty.EASY
        return Difficulty.MEDIUM
