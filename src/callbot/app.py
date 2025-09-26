from __future__ import annotations

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import CFG
from .middleware import request_context, cors as cors_mw, errors as error_mw
from .routes import health, voice, transcripts, dashboard


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="templates")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    app.before_request(request_context.before_request)
    app.after_request(request_context.after_request)
    app.after_request(cors_mw.add_cors_headers)

    app.register_blueprint(health.bp)
    app.register_blueprint(voice.bp)
    app.register_blueprint(transcripts.bp)
    app.register_blueprint(dashboard.bp)

    error_mw.register(app)
    return app
