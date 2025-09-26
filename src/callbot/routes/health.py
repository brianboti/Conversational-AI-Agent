from __future__ import annotations

from flask import Blueprint, Response, jsonify

bp = Blueprint("health", __name__)


@bp.get("/")
def root() -> Response:
    return Response("OK", status=200)


@bp.get("/ready")
def ready() -> Response:
    return jsonify(status="ready"), 200
