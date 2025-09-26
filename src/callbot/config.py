from __future__ import annotations
import os
from typing import Optional, Set
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    PORT: int = int(os.getenv("PORT", "8080"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    MAX_FORM_BYTES: int = int(os.getenv("APP_MAX_FORM_BYTES", "256000"))

    # Twilio security
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    APP_ALLOW_INSECURE: bool = os.getenv("APP_ALLOW_INSECURE", "0") == "1"

    # Voice prompts (single source of truth)
    APP_GREETING_TTS: str = os.getenv(
        "APP_GREETING_TTS",
        "Hello, you’ve reached Brian’s AI assistant. Thank you for calling.",
    )
    APP_SPEAK_NOW_TTS: str = os.getenv(
        "APP_SPEAK_NOW_TTS",
        "When you’re ready, please share your message.",
    )
    APP_FAREWELL_TTS: str = os.getenv(
        "APP_FAREWELL_TTS",
        "Thank you for sharing your message. Goodbye, and have a great day.",
    )

    # Speech recognition settings
    APP_SPEECH_LANG: str = os.getenv("APP_SPEECH_LANG", "en-US")
    APP_SPEECH_TIMEOUT: str = os.getenv("APP_SPEECH_TIMEOUT", "2")  # "auto" or seconds

    # Optional read API protection
    APP_TRANSCRIPTS_KEY: Optional[str] = os.getenv("APP_TRANSCRIPTS_KEY") or None

    # CORS / Security headers
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS", "*")  # comma-separated
    ENABLE_SECURITY_HEADERS: bool = True

    def cors_origin_set(self) -> Set[str]:
        vals = [v.strip() for v in self.CORS_ALLOWED_ORIGINS.split(",") if v.strip()]
        return set(vals or ["*"])


CFG = Settings()
