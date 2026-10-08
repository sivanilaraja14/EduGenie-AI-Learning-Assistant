from __future__ import annotations

from gemini_client import generate_content


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage in simple language.

Requirements:
- Preserve the important facts and meaning.
- Remove repetition and unnecessary detail.
- Use short paragraphs or bullet points when helpful.
- Do not add information that is not present in the passage.

Passage:
{text}
""".strip()

    return generate_content(prompt)
