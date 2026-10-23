"""HTTP Request dataclass."""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Request:
    """Represents an HTTP request."""

    method: str
    path: str
    version: str = "HTTP/1.1"
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""
