"""HTTP request/response serializer."""

from .request import Request
from .response import Response


class Serializer:
    """Serializes Request/Response into raw HTTP bytes."""

    @staticmethod
    def serialize_request(req: Request) -> bytes:
        lines = [f"{req.method} {req.path} {req.version}"]
        headers = dict(req.headers)
        if "Host" not in headers and "host" not in {k.lower() for k in headers}:
            headers["Host"] = "localhost"
        if req.body:
            headers["Content-Length"] = str(len(req.body))
        for name, value in headers.items():
            lines.append(f"{name}: {value}")
        lines.append("")
        lines.append("")
        head = "\r\n".join(lines).encode("ascii", errors="replace")
        return head + req.body

    @staticmethod
    def serialize_response(resp: Response) -> bytes:
        reason = resp.reason or {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        }.get(resp.status, "")
        lines = [f"{resp.version} {resp.status} {reason}"]
        headers = dict(resp.headers)
        headers["Content-Length"] = str(len(resp.body))
        for name, value in headers.items():
            lines.append(f"{name}: {value}")
        lines.append("")
        lines.append("")
        head = "\r\n".join(lines).encode("ascii", errors="replace")
        return head + resp.body
