from __future__ import annotations

from flask import Blueprint, jsonify, request
from ..logging import log_event
from ..services.transcripts_repo import TranscriptRepository

bp = Blueprint("transcripts", __name__, url_prefix="/transcripts")
REPO = TranscriptRepository()


@bp.get("")
def list_transcripts():
    try:
        limit_q = request.args.get("limit", "200")
        try:
            limit = max(1, min(500, int(limit_q)))
        except ValueError:
            limit = 200
        items = REPO.list_recent(limit=limit)
        return jsonify(items), 200
    except Exception as exc:
        log_event("ERROR", "transcripts.list.fail", error=str(exc))
        return jsonify(error="failed to list transcripts"), 500


@bp.get("/<sid>")
def get_transcript(sid: str):
    try:
        doc = REPO.get_one(sid)
        if not doc:
            return jsonify(error="not found"), 404
        return jsonify(doc), 200
    except Exception as exc:
        log_event("ERROR", "transcripts.get.fail", error=str(exc))
        return jsonify(error="failed to fetch transcript"), 500
