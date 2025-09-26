from __future__ import annotations

from flask import Blueprint, render_template, Response
from ..logging import log_event

bp = Blueprint("dashboard", __name__)


@bp.get("/dashboard")
def dashboard() -> Response:
    try:
        return render_template("dashboard.html"), 200
    except Exception as exc:
        log_event("ERROR", "dashboard.render.fail", error=str(exc))
        return Response("Dashboard failed to load", status=500)
