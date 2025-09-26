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

    # Voice UX
    APP_GREETING: str = os.getenv(
        "APP_GREETING",
        "Hello, this is Brian. Thanks for calling my project demo. Please share your message when you’re ready.",
    )
    APP_FAREWELL: str = os.getenv("APP_FAREWELL", "Thanks for your time—have a great day.")
    APP_STATIC_REPLY_TTS: str = os.getenv("APP_STATIC_REPLY_TTS", "Thank you. Your message has been recorded.")
    APP_STATIC_REPLY_MP3: str = os.getenv("APP_STATIC_REPLY_MP3", "/static/reply.mp3")

    # STT
    APP_SPEECH_LANG: str = os.getenv("APP_SPEECH_LANG", "en-US")
    APP_SPEECH_TIMEOUT: str = os.getenv("APP_SPEECH_TIMEOUT", "6")  # "auto" or seconds

    # Optional read API protection
    APP_TRANSCRIPTS_KEY: Optional[str] = os.getenv("APP_TRANSCRIPTS_KEY") or None

    # CORS / Security headers
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS", "*")  # comma-separated
    ENABLE_SECURITY_HEADERS: bool = True

    def cors_origin_set(self) -> Set[str]:
        vals = [v.strip() for v in self.CORS_ALLOWED_ORIGINS.split(",") if v.strip()]
        return set(vals or ["*"])


CFG = Settings()
