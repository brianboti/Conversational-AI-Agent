from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from flask import request, g


def log_event(level: str, event: str, **fields: Any) -> None:
    payload: Dict[str, Any] = {"level": level, "event": event, "ts": datetime.utcnow().isoformat() + "Z"}
    try:
        hdr = request.headers.get("X-Cloud-Trace-Context", "")
        trace_id = hdr.split("/", 1)[0] if hdr else ""
        if trace_id:
            payload["trace"] = trace_id
    except Exception:
        pass

    if hasattr(g, "req_id"):
        payload["req_id"] = g.req_id

    payload.update(fields)
    print(payload, flush=True)
