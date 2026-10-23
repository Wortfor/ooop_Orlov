"""Request handlers."""

import json
from datetime import datetime
from ..http.request import Request
from ..http.response import Response


def handle_echo_get(req: Request) -> Response:
    body = b"<html><body><h1>Hello</h1></body></html>"
    return Response(status=200, headers={"Content-Type": "text/html"}, body=body)


def handle_echo_post(req: Request) -> Response:
    ctype = req.headers.get("Content-Type", "application/octet-stream")
    return Response(status=200, headers={"Content-Type": ctype}, body=req.body)


def handle_time(req: Request) -> Response:
    payload = json.dumps({"time": datetime.now().isoformat()}).encode()
    return Response(
        status=200, headers={"Content-Type": "application/json"}, body=payload
    )


def handle_headers(req: Request) -> Response:
    payload = json.dumps(req.headers).encode()
    return Response(
        status=200, headers={"Content-Type": "application/json"}, body=payload
    )
