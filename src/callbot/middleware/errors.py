from __future__ import annotations

from flask import jsonify, Response, request
from twilio.twiml.voice_response import VoiceResponse
from ..config import CFG
from ..logging import log_event
from ..utils.twiml import say, to_response


def register(app):
    @app.errorhandler(404)
    def not_found(e):
        log_event("WARN", "http.404", path=request.path)
        return Response("Not Found", status=404)

    @app.errorhandler(500)
    def internal_error(e):
        log_event("ERROR", "http.500", error=str(e))
        if request.path.startswith("/transcripts") or "application/json" in (request.headers.get("Accept", "") or ""):
            return jsonify(error="internal server error"), 500
        vr = VoiceResponse()
        say(vr, "Sorry, an error occurred. Please try again later.", CFG.APP_SPEECH_LANG)
        return to_response(vr, 500)
