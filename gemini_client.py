from __future__ import annotations

import time

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


_client = None


# Models to try if the configured model is temporarily unavailable.
# The first model is always the one from .env.
FALLBACK_MODELS = [
    GEMINI_MODEL,
    "gemini-3.7-flash",
    "gemini-3.5-flash",
]


def get_client():
    global _client

    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Add your Gemini API key to the .env file."
            )

        _client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    return _client


def generate_content(prompt: str) -> str:
    client = get_client()

    last_error = None

    # Remove duplicates while preserving order.
    models_to_try = list(dict.fromkeys(FALLBACK_MODELS))

    for model in models_to_try:

        # Try each model up to 2 times.
        for attempt in range(2):

            try:
                print(
                    f"Gemini request: model={model}, "
                    f"attempt={attempt + 1}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if not response.text:
                    raise RuntimeError(
                        f"Gemini returned an empty response from {model}."
                    )

                print(
                    f"Gemini request successful: model={model}"
                )

                return response.text.strip()

            except Exception as exc:

                last_error = exc

                error_text = str(exc)

                print(
                    f"Gemini request failed: "
                    f"model={model}, "
                    f"attempt={attempt + 1}, "
                    f"error={error_text}"
                )

                # 503 = temporary service overload.
                # Wait and retry before moving to another model.
                if "503" in error_text or "UNAVAILABLE" in error_text:

                    if attempt == 0:
                        wait_seconds = 2

                        print(
                            f"Temporary Gemini service issue. "
                            f"Retrying in {wait_seconds} seconds..."
                        )

                        time.sleep(wait_seconds)

                    continue

                # 429 = quota/rate-limit problem.
                # Retry once, then try the next model.
                if "429" in error_text:

                    if attempt == 0:
                        wait_seconds = 3

                        print(
                            f"Gemini rate limit encountered. "
                            f"Retrying in {wait_seconds} seconds..."
                        )

                        time.sleep(wait_seconds)

                    continue

                # For other errors, don't repeatedly retry.
                break

    raise RuntimeError(
        f"Gemini request failed after trying "
        f"{len(models_to_try)} models. "
        f"Last error: {last_error}"
    ) from last_error