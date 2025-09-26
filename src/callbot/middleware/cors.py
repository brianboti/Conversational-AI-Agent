from __future__ import annotations

from flask import Response
from ..config import CFG


def add_cors_headers(resp: Response) -> Response:
    origins = ",".join(CFG.cors_origin_set())
    resp.headers["Access-Control-Allow-Origin"] = origins if origins else "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Auth-Key"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp
