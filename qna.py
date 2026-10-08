from __future__ import annotations

from gemini_client import generate_content


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a helpful educational tutor.

Answer the student's question accurately and concisely.
Use language appropriate for a learner.
If the question is academic, explain the reasoning briefly when useful.
Do not invent sources, facts, or citations.

Student question:
{question}
""".strip()

    return generate_content(prompt)
