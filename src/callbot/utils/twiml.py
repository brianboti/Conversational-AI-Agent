from __future__ import annotations

from flask import Response
from twilio.twiml.voice_response import VoiceResponse


def say(vr: VoiceResponse, text: str, language: str) -> None:
    vr.say(text, voice="alice", language=language)


def to_response(vr: VoiceResponse, status: int = 200) -> Response:
    return Response(str(vr), mimetype="application/xml", status=status)
