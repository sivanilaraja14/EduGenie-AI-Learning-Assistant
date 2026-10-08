from __future__ import annotations

from gemini_client import generate_content


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, an educational learning-path planner.

Create a structured learning path for: {topic}

Organize it from beginner to intermediate to advanced.
For each level include:
- estimated learning time
- key topics
- practice suggestions
- useful resource types such as tutorials, documentation, books, or videos

Keep the plan practical and adaptable to a learner's pace.
Do not invent specific URLs.
""".strip()

    return generate_content(prompt)
