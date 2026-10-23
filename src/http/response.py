"""HTTP Response dataclass."""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Response:
    """Represents an HTTP response."""

    status: int
    reason: str = ""
    version: str = "HTTP/1.1"
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""
