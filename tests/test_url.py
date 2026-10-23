"""Unit tests for URL parser."""

import pytest
from src.http.url import Url, ParseError


def test_parse_full():
    u = Url("http://host:8080/path?q=1")
    assert u.host == "host"
    assert u.port == 8080
    assert u.path == "/path"
    assert u.query == "q=1"


def test_parse_default_port():
    u = Url("http://host/path")
    assert u.port == 80


def test_parse_https_default_port():
    u = Url("https://host/path")
    assert u.port == 443


def test_parse_garbage():
    with pytest.raises(ParseError):
        Url("garbage")


def test_parse_empty():
    with pytest.raises(ParseError):
        Url("")


def test_parse_no_host():
    with pytest.raises(ParseError):
        Url("http://")


def test_parse_root_path():
    u = Url("http://example.com")
    assert u.path == "/"


def test_parse_query():
    u = Url("http://example.com/search?q=test&p=1")
    assert u.query == "q=test&p=1"
