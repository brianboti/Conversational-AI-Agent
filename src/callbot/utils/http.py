from __future__ import annotations

from typing import Optional
from flask import request


def absolute_url(path: str) -> str:
    return request.url_root.rstrip("/") + "/" + path.lstrip("/")


def trimmed(text: Optional[str], max_len: int = 4000) -> str:
    return (text or "")[:max_len]


def something_or_none(v: Optional[str]) -> Optional[str]:
    v = (v or "").strip()
    return v if v else None
