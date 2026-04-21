"""
AI-based question categorizer supporting OpenAI, Google Gemini, and Ollama.
"""
import json
import hashlib
from pathlib import Path
from config import Question, CategorizedQuestion, Difficulty
from categorizers.base import BaseCategorizer
from categorizers.prompts import get_categorization_prompt

# Simple file-based cache directory
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"


class AICategorizer(BaseCategorizer):
    """Categorize questions using AI models (OpenAI / Gemini / Ollama)."""

    def __init__(self, taxonomy: dict, provider: str, api_key: str = "", model: str = ""):
        """
        Args:
            taxonomy: Exam taxonomy dict
            provider: "openai", "gemini", or "ollama"
            api_key: API key (not needed for Ollama)
            model: Model name override (optional)
        """
        super().__init__(taxonomy)
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model or self._default_model()

    def _default_model(self) -> str:
        defaults = {
            "openai": "gpt-4o-mini",
            "gemini": "gemini-1.5-flash",
            "ollama": "llama3",
        }
        return defaults.get(self.provider, "gpt-4o-mini")

    def categorize(self, question: Question) -> CategorizedQuestion:
        """Categorize a single question (wraps batch for efficiency)."""
        results = self.categorize_batch([question])
        return results[0]

    def categorize_batch(
        self, questions: list[Question], batch_size: int = 15
    ) -> list[CategorizedQuestion]:
        """Categorize questions in batches via AI API."""
        all_results = []
        for i in range(0, len(questions), batch_size):
            batch = questions[i : i + batch_size]
            batch_results = self._process_batch(batch)
            all_results.extend(batch_results)
        return all_results

    def _process_batch(self, questions: list[Question]) -> list[CategorizedQuestion]:
        """Process a single batch of questions."""
        texts = [q.text for q in questions]

        # Check cache
        cache_key = self._cache_key(texts)
        cached = self._load_cache(cache_key)
        if cached:
            return self._parse_ai_response(cached, questions)

        # Build prompt and call AI
        prompt = get_categorization_prompt(self.taxonomy, texts)
        response = self._call_ai(prompt)

        # Cache the response
        self._save_cache(cache_key, response)

        return self._parse_ai_response(response, questions)

    def _call_ai(self, prompt: str) -> str:
        """Call the AI provider and return the response text."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)
        elif self.provider == "ollama":
            return self._call_ollama(prompt)
        raise ValueError(f"Unknown AI provider: {self.provider}")

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert exam question categorizer. Respond only with valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=4000,
        )
        return response.choices[0].message.content or ""

    def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=4000),
        )
        return response.text or ""

    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama API."""
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1},
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")

    def _parse_ai_response(
        self, response: str, questions: list[Question]
    ) -> list[CategorizedQuestion]:
        """Parse AI JSON response into CategorizedQuestion objects."""
        # Extract JSON from response (handle markdown code blocks)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1] if "\n" in response else response
            if response.endswith("```"):
                response = response[:-3]
            # Remove json language tag if present
            if response.startswith("json"):
                response = response[4:]
            response = response.strip()

        try:
            items = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: return uncategorized
            return [
                CategorizedQuestion(
                    question=q,
                    section=q.section_hint or "Unknown",
                    topic="Uncategorized",
                    confidence=0.0,
                )
                for q in questions
            ]

        results = []
        for q in questions:
            # Find matching item by index
            q_idx = questions.index(q) + 1
            match = None
            for item in items:
                if item.get("question_index") == q_idx:
                    match = item
                    break

            if match:
                diff_str = match.get("difficulty", "Unknown")
                try:
                    difficulty = Difficulty(diff_str)
                except ValueError:
                    difficulty = Difficulty.UNKNOWN

                results.append(CategorizedQuestion(
                    question=q,
                    section=match.get("section", q.section_hint or "Unknown"),
                    topic=match.get("topic", "Uncategorized"),
                    sub_topic=match.get("sub_topic", ""),
                    difficulty=difficulty,
                    confidence=float(match.get("confidence", 0.5)),
                ))
            else:
                results.append(CategorizedQuestion(
                    question=q,
                    section=q.section_hint or "Unknown",
                    topic="Uncategorized",
                    confidence=0.0,
                ))

        return results

    # --- Caching ---

    def _cache_key(self, texts: list[str]) -> str:
        combined = f"{self.provider}:{self.model}:" + "||".join(texts)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _load_cache(self, key: str) -> str | None:
        cache_file = CACHE_DIR / f"{key}.json"
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")
        return None

    def _save_cache(self, key: str, response: str) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{key}.json"
        cache_file.write_text(response, encoding="utf-8")
