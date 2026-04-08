"""Configuration loaded from environment variables."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


SCREENER_API_BASE_URL: str = os.getenv("SCREENER_API_BASE_URL", "http://127.0.0.1:8098").rstrip("/")
SCREENER_API_KEY: str | None = os.getenv("SCREENER_API_KEY") or None
REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
