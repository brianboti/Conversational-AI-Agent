from __future__ import annotations

import uuid
from datetime import datetime
from flask import g, request, Response, jsonify
from ..config import CFG
from ..logging import log_event


def before_request():
    if request.content_length and request.content_length > CFG.MAX_FORM_BYTES:
        return jsonify(error="payload too large"), 413

    g.req_id = str(uuid.uuid4())
    g.started_at = datetime.utcnow()
    log_event("INFO", "request.start", method=request.method, path=request.path, remote=request.remote_addr)

    if request.path.startswith("/transcripts") and CFG.APP_TRANSCRIPTS_KEY:
        if request.headers.get("X-Auth-Key") != CFG.APP_TRANSCRIPTS_KEY:
            return jsonify(error="unauthorized"), 401

    if request.method == "OPTIONS":
        resp = Response(status=204)
        return after_request(resp)
    return None


def after_request(response: Response) -> Response:
    ms = (datetime.utcnow() - g.started_at).total_seconds() * 1000.0
    log_event("INFO", "request.end", status=response.status_code, elapsed_ms=round(ms, 2))
    return response
