from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()

EXPLANATION_MODEL = os.getenv(
    "EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M",
).strip()

EXPLANATION_BACKEND = os.getenv(
    "EXPLANATION_BACKEND",
    "local",
).strip().lower()

ALLOW_EXPLANATION_FALLBACK = (
    os.getenv("ALLOW_EXPLANATION_FALLBACK", "true").strip().lower() == "true"
)

MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "30000"))
