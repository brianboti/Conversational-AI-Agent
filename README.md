# Callbot (Flask + Twilio + Firestore)

Production-ready structure with modular routes, services, and middleware.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env  # fill TWILIO_AUTH_TOKEN etc.
PYTHONPATH=src gunicorn -c gunicorn.conf.py wsgi:app
```

## Env / Security
- Set `APP_TRANSCRIPTS_KEY` and send it as `X-Auth-Key` for `/transcripts*`.
- Prefer explicit `CORS_ALLOWED_ORIGINS` in prod.
- Keep `APP_ALLOW_INSECURE=0` to enforce Twilio signature validation.
