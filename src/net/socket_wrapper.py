"""Socket context manager wrapper."""

import socket


class Socket:
    """Context manager for socket."""

    def __init__(self, sock: socket.socket):
        self._sock = sock

    def __enter__(self) -> "Socket":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        try:
            if self._sock is not None:
                self._sock.close()
        finally:
            self._sock = None

    def send_all(self, data: bytes) -> None:
        self._sock.sendall(data)

    def recv(self, n: int) -> bytes:
        return self._sock.recv(n)

    def settimeout(self, timeout: float) -> None:
        self._sock.settimeout(timeout)

    def connect(self, address) -> None:
        self._sock.connect(address)

    def bind(self, address) -> None:
        self._sock.bind(address)

    def listen(self, backlog: int = 5) -> None:
        self._sock.listen(backlog)

    def accept(self):
        conn, addr = self._sock.accept()
        return Socket(conn), addr

    def setsockopt(self, *args) -> None:
        self._sock.setsockopt(*args)

    def shutdown(self, how) -> None:
        self._sock.shutdown(how)
