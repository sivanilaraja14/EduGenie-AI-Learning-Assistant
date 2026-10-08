from __future__ import annotations

from functools import lru_cache

from config import ALLOW_EXPLANATION_FALLBACK, EXPLANATION_BACKEND, EXPLANATION_MODEL
from gemini_client import generate_content


@lru_cache(maxsize=1)
def _load_local_model():
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(EXPLANATION_MODEL)
        model = AutoModelForSeq2SeqLM.from_pretrained(EXPLANATION_MODEL)
        model.eval()
        return tokenizer, model, torch
    except Exception as exc:
        raise RuntimeError(
            f"Could not load local explanation model '{EXPLANATION_MODEL}': {exc}"
        ) from exc


def _explain_with_local_model(topic: str) -> str:
    tokenizer, model, torch = _load_local_model()

    prompt = (
        f"Explain the concept of '{topic}' in simple and clear language "
        "for a school student. Use a short definition, a simple example, "
        "and avoid unnecessary jargon."
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=180,
            num_beams=4,
            temperature=0.7,
            do_sample=True,
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    if not result:
        raise RuntimeError("The local explanation model returned no text.")
    return result


def explain_topic(topic: str) -> str:
    if EXPLANATION_BACKEND == "gemini":
        return generate_content(
            f"Explain '{topic}' simply for a beginner. Include a short definition "
            "and one practical example."
        )

    if EXPLANATION_BACKEND == "local":
        try:
            return _explain_with_local_model(topic)
        except Exception as exc:
            if not ALLOW_EXPLANATION_FALLBACK:
                raise
            return generate_content(
                f"Explain '{topic}' simply for a beginner. Include a short definition "
                f"and one practical example. The local explanation model was unavailable: {exc}"
            )

    raise ValueError(
        "EXPLANATION_BACKEND must be either 'local' or 'gemini'."
    )
