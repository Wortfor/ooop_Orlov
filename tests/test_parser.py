"""Unit tests for HTTP parser."""

import pytest
from src.http.parser import Parser, ParseError


def test_parse_request_simple():
    raw = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    req = Parser.parse_request(raw)
    assert req.method == "GET"
    assert req.path == "/"
    assert req.version == "HTTP/1.1"
    assert req.headers["Host"] == "example.com"


def test_parse_request_with_body():
    raw = b"POST /echo HTTP/1.1\r\nHost: x\r\n" b"Content-Length: 5\r\n\r\nhello"
    req = Parser.parse_request(raw)
    assert req.method == "POST"
    assert req.body == b"hello"


def test_parse_request_empty():
    with pytest.raises(ParseError):
        Parser.parse_request(b"")


def test_parse_request_malformed():
    with pytest.raises(ParseError):
        Parser.parse_request(b"GARBAGE\r\n\r\n")


def test_parse_response_simple():
    raw = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nhi"
    resp = Parser.parse_response(raw)
    assert resp.status == 200
    assert resp.reason == "OK"
    assert resp.body == b"hi"


def test_parse_response_404():
    raw = b"HTTP/1.1 404 Not Found\r\n\r\n"
    resp = Parser.parse_response(raw)
    assert resp.status == 404
    assert resp.reason == "Not Found"


def test_parse_response_invalid_status():
    with pytest.raises(ParseError):
        Parser.parse_response(b"HTTP/1.1 ABC\r\n\r\n")


def test_header_too_large():
    raw = b"GET / HTTP/1.1\r\nX-Long: " + b"a" * 9000 + b"\r\n\r\n"
    with pytest.raises(ParseError):
        Parser.parse_request(raw)
