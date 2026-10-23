"""High-level HTTP client."""

from ..http.url import Url
from ..http.request import Request
from ..http.response import Response
from ..http.parser import Parser
from ..http.serializer import Serializer
from ..net.tcp_client import TcpClient, ConnectionError, TimeoutError


class HttpError(Exception):
    """HTTP status error."""

    def __init__(self, status: int, reason: str = ""):
        self.status = status
        self.reason = reason
        super().__init__(f"HTTP {status} {reason}")


class HttpClient:
    """HTTP client with get/post methods."""

    def __init__(self, timeout_ms: int = 5000):
        self.timeout = timeout_ms / 1000.0
        self.tcp = TcpClient(timeout=self.timeout)
        self.last_response: Response | None = None
        self._current_url = ""

    def set_timeout(self, ms: int) -> None:
        self.timeout = ms / 1000.0
        self.tcp.timeout = self.timeout

    def _send(self, req: Request) -> Response:
        url = Url(self._current_url)
        raw = Serializer.serialize_request(req)
        try:
            data = self.tcp.request(url.host, url.port, raw)
        except (ConnectionError, TimeoutError):
            raise
        resp = Parser.parse_response(data)
        self.last_response = resp
        return resp

    def get(self, url: str, headers: dict | None = None) -> Response:
        self._current_url = url
        u = Url(url)
        path = u.path
        if u.query:
            path += "?" + u.query
        h = {"Host": u.host, "Connection": "close"}
        if headers:
            h.update(headers)
        req = Request(method="GET", path=path, headers=h)
        return self._send(req)

    def post(
        self,
        url: str,
        body: bytes,
        content_type: str = "text/plain",
        headers: dict | None = None,
    ) -> Response:
        self._current_url = url
        u = Url(url)
        path = u.path
        if u.query:
            path += "?" + u.query
        h = {"Host": u.host, "Connection": "close", "Content-Type": content_type}
        if headers:
            h.update(headers)
        if isinstance(body, str):
            body = body.encode("utf-8")
        req = Request(method="POST", path=path, headers=h, body=body)
        return self._send(req)
