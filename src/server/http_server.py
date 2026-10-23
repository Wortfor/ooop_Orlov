"""Threaded HTTP server."""

import logging
import socket
import threading
from ..http.parser import Parser, ParseError
from ..http.response import Response
from ..http.serializer import Serializer
from .router import Router

logger = logging.getLogger(__name__)


class HttpServer:
    """HTTP server running in a background thread."""

    def __init__(self, router: Router, log_callback=None):
        self.router = router
        self.log_callback = log_callback
        self._thread: threading.Thread | None = None
        self._sock: socket.socket | None = None
        self._running = False
        self._lock = threading.Lock()

    @property
    def running(self) -> bool:
        return self._running

    def start(self, port: int = 8080) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._serve, args=(port,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _serve(self, port: int) -> None:
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind(("0.0.0.0", port))
            self._sock.listen(10)
            self._sock.settimeout(0.5)
            logger.info("Server started on port %d", port)
        except OSError as exc:
            logger.error("Cannot start server: %s", exc)
            self._running = False
            return

        while self._running:
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=self._handle_client, args=(conn, addr), daemon=True
            ).start()

        try:
            self._sock.close()
        except OSError:
            pass
        logger.info("Server stopped")

    def _handle_client(self, conn: socket.socket, addr) -> None:
        req = None
        try:
            conn.settimeout(5.0)
            data = b""
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            try:
                req = Parser.parse_request(data)
            except ParseError:
                resp = Response(
                    status=400, reason="Bad Request", body=b"400 Bad Request"
                )
            else:
                resp = self.router.dispatch(req)

            raw = Serializer.serialize_response(resp)
            conn.sendall(raw)
            if self.log_callback and req is not None:
                self.log_callback(req.method, req.path, resp.status)
        except OSError as exc:
            logger.warning("Client error: %s", exc)
        finally:
            try:
                conn.close()
            except OSError:
                pass
