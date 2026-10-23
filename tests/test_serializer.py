"""Unit tests for HTTP serializer."""

from src.http.serializer import Serializer
from src.http.request import Request
from src.http.response import Response


def test_serialize_request_ends_with_blank_line():
    req = Request(method="GET", path="/", headers={"Host": "x"})
    raw = Serializer.serialize_request(req)
    assert raw.startswith(b"GET / HTTP/1.1\r\n")
    assert b"\r\n\r\n" in raw


def test_serialize_request_with_body():
    req = Request(method="POST", path="/echo", headers={"Host": "x"}, body=b"hello")
    raw = Serializer.serialize_request(req)
    assert b"Content-Length: 5\r\n" in raw
    assert raw.endswith(b"hello")


def test_serialize_response_has_content_length():
    resp = Response(status=200, body=b"hi")
    raw = Serializer.serialize_response(resp)
    assert raw.startswith(b"HTTP/1.1 200 OK\r\n")
    assert b"Content-Length: 2\r\n" in raw


def test_serialize_response_404():
    resp = Response(status=404, reason="Not Found", body=b"nope")
    raw = Serializer.serialize_response(resp)
    assert b"404 Not Found" in raw


def test_serialize_response_empty_body():
    resp = Response(status=204)
    raw = Serializer.serialize_response(resp)
    assert b"Content-Length: 0" in raw
