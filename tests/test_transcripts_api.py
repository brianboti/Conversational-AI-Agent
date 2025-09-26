import os
from callbot import create_app

def test_transcripts_requires_auth_when_key_set(monkeypatch):
    monkeypatch.setenv("APP_TRANSCRIPTS_KEY", "sek")
    app = create_app()
    c = app.test_client()
    r = c.get("/transcripts")
    assert r.status_code == 401
