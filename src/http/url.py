"""URL parsing module."""

from urllib.parse import urlparse


class ParseError(Exception):
    """Raised when URL cannot be parsed."""


class Url:
    """Parsed URL representation."""

    def __init__(self, raw: str):
        self.raw = raw
        self.scheme = "http"
        self.host = ""
        self.port = 80
        self.path = "/"
        self.query = ""
        self.parse()

    def parse(self) -> None:
        """Parse raw URL into components."""
        if not self.raw or not isinstance(self.raw, str):
            raise ParseError(f"Invalid URL: {self.raw!r}")

        raw = self.raw.strip()
        if "://" not in raw:
            if "." not in raw and raw != "localhost":
                raise ParseError(f"Invalid URL format: {self.raw!r}")
            raw = "http://" + raw

        try:
            parsed = urlparse(raw)
        except Exception as exc:
            raise ParseError(f"Cannot parse URL: {self.raw!r}") from exc

        if parsed.scheme not in ("http", "https"):
            raise ParseError(f"Unsupported scheme: {parsed.scheme}")

        if not parsed.hostname:
            raise ParseError(f"No host in URL: {self.raw!r}")

        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.path = parsed.path or "/"
        self.query = parsed.query

        default_port = 443 if self.scheme == "https" else 80
        self.port = parsed.port if parsed.port else default_port

    def __repr__(self) -> str:
        return (
            f"Url(scheme={self.scheme!r}, host={self.host!r}, "
            f"port={self.port}, path={self.path!r}, query={self.query!r})"
        )
