from callbot.services.twilio_verifier import TwilioRequestVerifier

def test_verifier_allows_when_disabled():
    v = TwilioRequestVerifier(auth_token="", enabled=False)
    assert v.is_valid("http://x", {}, "") is True
