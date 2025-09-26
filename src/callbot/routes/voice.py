from __future__ import annotations

import uuid
from typing import Dict
from flask import Blueprint, Response, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from google.cloud import firestore as gfs

from ..config import CFG
from ..logging import log_event
from ..services.twilio_verifier import TwilioRequestVerifier
from ..services.transcripts_repo import TranscriptRepository
from ..utils.http import absolute_url, trimmed, something_or_none
from ..utils.twiml import say, to_response

bp = Blueprint("voice", __name__, url_prefix="")

VERIFIER = TwilioRequestVerifier(
    auth_token=CFG.TWILIO_AUTH_TOKEN,
    enabled=not CFG.APP_ALLOW_INSECURE,
)
TRANSCRIPTS = TranscriptRepository()


def _forbid_twiml() -> Response:
    vr = VoiceResponse()
    say(vr, "Access denied.", CFG.APP_SPEECH_LANG)
    return to_response(vr, 403)


def _validate_twilio() -> bool:
    sig = request.headers.get("X-Twilio-Signature", "") or ""
    params: Dict[str, str] = request.form.to_dict(flat=True)
    return VERIFIER.is_valid(request.url, params, sig)


# ---------------------------
# TTS FLOW (single Gather)
# ---------------------------
@bp.post("/voice_tts")
def voice_tts() -> Response:
    if not _validate_twilio():
        log_event("WARN", "signature.invalid")
        return _forbid_twiml()

    vr = VoiceResponse()

    # 1) Greeting
    say(vr, CFG.APP_GREETING_TTS, CFG.APP_SPEECH_LANG)

    # 2) Speak-now + single speech gather
    gather = Gather(
        input="speech",
        action=absolute_url("/handle_speech_tts"),
        method="POST",
        language=CFG.APP_SPEECH_LANG,
        speech_timeout=CFG.APP_SPEECH_TIMEOUT,
        action_on_empty_result=True,
    )
    say(gather, CFG.APP_SPEAK_NOW_TTS, CFG.APP_SPEECH_LANG)
    vr.append(gather)

    # 3) If no speech captured, end politely
    say(vr, CFG.APP_FAREWELL_TTS, CFG.APP_SPEECH_LANG)
    vr.hangup()
    return to_response(vr)


@bp.post("/handle_speech_tts")
def handle_speech_tts() -> Response:
    if not _validate_twilio():
        log_event("WARN", "signature.invalid")
        return _forbid_twiml()

    form = request.form.to_dict(flat=True)
    headers = {k: v for k, v in request.headers.items() if k.lower().startswith("x-twilio") or k == "User-Agent"}
    log_event("INFO", "tts.payload", form=form, headers=headers)

    said = trimmed(form.get("SpeechResult"))
    confidence = form.get("Confidence")
    call_sid = form.get("CallSid")
    account_sid = form.get("AccountSid")

    log_event(
        "INFO",
        "tts.transcript",
        call_sid=call_sid,
        account_sid=account_sid,
        said=something_or_none(said),
        confidence=something_or_none(confidence),
    )

    # Persist transcript (best-effort)
    try:
        doc = {
            "call_sid": call_sid,
            "account_sid": account_sid,
            "from_": form.get("From"),
            "to": form.get("To"),
            "speech_result": said,
            "confidence": float(confidence) if confidence else None,
            "language": form.get("Language"),
            "created_at": gfs.SERVER_TIMESTAMP,
            "raw": form,
        }
        TRANSCRIPTS.save_transcript(call_sid or str(uuid.uuid4()), doc)
        log_event("INFO", "tts.saved", call_sid=call_sid)
    except Exception as exc:
        log_event("ERROR", "firestore.save.fail", error=str(exc))

    # Minimal reply then end call
    vr = VoiceResponse()
    say(vr, CFG.APP_FAREWELL_TTS, CFG.APP_SPEECH_LANG)
    vr.hangup()
    return to_response(vr)


# ---------------------------
# MP3 FLOW (optional)
# ---------------------------
@bp.post("/voice_mp3")
def voice_mp3() -> Response:
    if not _validate_twilio():
        log_event("WARN", "signature.invalid")
        return _forbid_twiml()

    vr = VoiceResponse()

    # 1) Greeting
    say(vr, CFG.APP_GREETING_TTS, CFG.APP_SPEECH_LANG)

    # 2) Speak-now + single speech gather
    gather = Gather(
        input="speech",
        action=absolute_url("/handle_speech_mp3"),
        method="POST",
        language=CFG.APP_SPEECH_LANG,
        speech_timeout=CFG.APP_SPEECH_TIMEOUT,
        action_on_empty_result=True,
    )
    say(gather, CFG.APP_SPEAK_NOW_TTS, CFG.APP_SPEECH_LANG)
    vr.append(gather)

    # 3) If no speech captured, end politely
    say(vr, CFG.APP_FAREWELL_TTS, CFG.APP_SPEECH_LANG)
    vr.hangup()
    return to_response(vr)


@bp.post("/handle_speech_mp3")
def handle_speech_mp3() -> Response:
    if not _validate_twilio():
        log_event("WARN", "signature.invalid")
        return _forbid_twiml()

    said = trimmed(request.form.get("SpeechResult"))
    confidence = request.form.get("Confidence")
    call_sid = request.form.get("CallSid")
    log_event(
        "INFO",
        "mp3.transcript",
        call_sid=call_sid,
        said=something_or_none(said),
        confidence=something_or_none(confidence),
    )

    vr = VoiceResponse()
    # Only play if explicitly configured; otherwise keep it minimal
    mp3 = getattr(CFG, "APP_STATIC_REPLY_MP3", None)
    if mp3:
        vr.play(absolute_url(mp3))

    say(vr, CFG.APP_FAREWELL_TTS, CFG.APP_SPEECH_LANG)
    vr.hangup()
    return to_response(vr)
