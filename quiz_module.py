from __future__ import annotations

import json
import re
from typing import Any

from gemini_client import generate_content


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")

    validated = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = item.get("question")
        options = item.get("options")
        answer = item.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Question {index} has no valid question text.")

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain exactly 4 options.")

        options = [str(option).strip() for option in options]
        if any(not option for option in options):
            raise ValueError(f"Question {index} contains an empty option.")

        if not isinstance(answer, str) or answer.strip() not in options:
            raise ValueError(
                f"Question {index}'s answer must exactly match one of its options."
            )

        validated.append(
            {
                "question": question.strip(),
                "options": options,
                "answer": answer.strip(),
            }
        )

    return validated


def generate_quiz(text: str) -> list[dict[str, Any]]:
    prompt = f"""
You are a quiz generator for EduGenie.

From the educational text below, create exactly 3 multiple-choice questions.
Each question must have exactly 4 options and exactly one correct answer.

Return ONLY valid JSON. Do not use Markdown fences.

Required JSON shape:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

Educational text:
{text}
""".strip()

    raw = generate_content(prompt)
    cleaned = clean_json_block(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid quiz JSON: {exc}. Raw response: {raw}"
        ) from exc

    return _validate_quiz(data)
