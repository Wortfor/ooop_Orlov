"""TCP client using Socket wrapper."""

import socket
from .socket_wrapper import Socket


class ConnectionError(Exception):
    """Raised on connection problems."""


class TimeoutError(Exception):
    """Raised on timeout."""


class TcpClient:
    """Simple TCP client."""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def connect(self, host: str, port: int) -> Socket:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))
            return Socket(sock)
        except socket.timeout as exc:
            raise TimeoutError(f"Timeout connecting to {host}:{port}") from exc
        except OSError as exc:
            raise ConnectionError(f"Cannot connect to {host}:{port}: {exc}") from exc

    def request(self, host: str, port: int, data: bytes) -> bytes:
        with self.connect(host, port) as sock:
            sock.send_all(data)
            chunks = []
            while True:
                try:
                    chunk = sock.recv(4096)
                except socket.timeout as exc:
                    raise TimeoutError("Timeout reading response") from exc
                if not chunk:
                    break
                chunks.append(chunk)
            return b"".join(chunks)
