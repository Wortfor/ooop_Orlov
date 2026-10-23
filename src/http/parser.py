"""HTTP request/response parser."""

from .request import Request
from .response import Response


class ParseError(Exception):
    """Raised when HTTP message cannot be parsed."""


MAX_HEADER_SIZE = 8192


class Parser:
    """Parses raw HTTP bytes into Request/Response objects."""

    @staticmethod
    def parse_request(data: bytes) -> Request:
        if not data:
            raise ParseError("Empty request")
        if len(data) > MAX_HEADER_SIZE * 4:
            raise ParseError("Request too large")

        head, _, body = data.partition(b"\r\n\r\n")
        lines = head.split(b"\r\n")
        if not lines or not lines[0]:
            raise ParseError("Missing request line")

        parts = lines[0].split(b" ")
        if len(parts) != 3:
            raise ParseError("Malformed request line")

        method = parts[0].decode("ascii", errors="replace")
        path = parts[1].decode("ascii", errors="replace")
        version = parts[2].decode("ascii", errors="replace")

        headers = {}
        for line in lines[1:]:
            if not line:
                continue
            if len(line) > MAX_HEADER_SIZE:
                raise ParseError("Header too large")
            if b":" not in line:
                raise ParseError(f"Malformed header: {line!r}")
            name, _, value = line.partition(b":")
            headers[name.decode("ascii", errors="replace").strip()] = value.decode(
                "ascii", errors="replace"
            ).strip()

        return Request(
            method=method, path=path, version=version, headers=headers, body=body
        )

    @staticmethod
    def parse_response(data: bytes) -> Response:
        if not data:
            raise ParseError("Empty response")

        head, _, body = data.partition(b"\r\n\r\n")
        lines = head.split(b"\r\n")
        if not lines or not lines[0]:
            raise ParseError("Missing status line")

        parts = lines[0].split(b" ", 2)
        if len(parts) < 2:
            raise ParseError("Malformed status line")

        version = parts[0].decode("ascii", errors="replace")
        try:
            status = int(parts[1])
        except ValueError as exc:
            raise ParseError("Invalid status code") from exc
        reason = parts[2].decode("ascii", errors="replace") if len(parts) > 2 else ""

        headers = {}
        for line in lines[1:]:
            if not line:
                continue
            if b":" not in line:
                continue
            name, _, value = line.partition(b":")
            headers[name.decode("ascii", errors="replace").strip()] = value.decode(
                "ascii", errors="replace"
            ).strip()

        return Response(
            status=status, reason=reason, version=version, headers=headers, body=body
        )
