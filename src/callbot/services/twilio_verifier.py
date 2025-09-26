from __future__ import annotations

from typing import Dict
from twilio.request_validator import RequestValidator
from ..logging import log_event


class TwilioRequestVerifier:
    def __init__(self, auth_token: str, enabled: bool) -> None:
        self._enabled = enabled and bool(auth_token)
        self._validator = RequestValidator(auth_token) if auth_token else None

    def is_valid(self, url: str, params: Dict[str, str], signature: str) -> bool:
        if not self._enabled or not self._validator:
            return True
        try:
            return self._validator.validate(url, params, signature or "")
        except Exception as exc:
            log_event("ERROR", "signature.validate.error", error=str(exc))
            return False
