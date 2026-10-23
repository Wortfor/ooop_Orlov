"""Simple URL router."""

from typing import Callable, Dict, Tuple
from ..http.request import Request
from ..http.response import Response

Handler = Callable[[Request], Response]


class Router:
    """Maps (method, path) to handler."""

    def __init__(self):
        self._routes: Dict[Tuple[str, str], Handler] = {}

    def route(self, method: str, path: str, handler: Handler) -> None:
        self._routes[(method.upper(), path)] = handler

    def dispatch(self, req: Request) -> Response:
        key = (req.method.upper(), req.path.split("?")[0])
        if key in self._routes:
            return self._routes[key](req)

        if req.path.startswith("/status/"):
            try:
                code = int(req.path.split("/")[-1].split("?")[0])
                return Response(status=code, body=b"")
            except ValueError:
                pass

        return Response(status=404, reason="Not Found", body=b"404 Not Found")
