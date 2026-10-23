"""Integration tests: client <-> server."""

import threading
import time
import pytest
from src.server.http_server import HttpServer
from src.server.router import Router
from src.server import handlers
from src.client.http_client import HttpClient


@pytest.fixture
def server():
    router = Router()
    router.route("GET", "/echo", handlers.handle_echo_get)
    router.route("POST", "/echo", handlers.handle_echo_post)
    router.route("GET", "/time", handlers.handle_time)
    router.route("GET", "/headers", handlers.handle_headers)
    srv = HttpServer(router)
    srv.start(port=18080)
    time.sleep(0.3)
    yield srv
    srv.stop()


def test_get_echo(server):
    c = HttpClient()
    resp = c.get("http://localhost:18080/echo")
    assert resp.status == 200
    assert b"Hello" in resp.body


def test_post_echo(server):
    c = HttpClient()
    resp = c.post("http://localhost:18080/echo", b"abc", "text/plain")
    assert resp.status == 200
    assert resp.body == b"abc"


def test_status_404(server):
    c = HttpClient()
    resp = c.get("http://localhost:18080/status/404")
    assert resp.status == 404


def test_nonexistent(server):
    c = HttpClient()
    resp = c.get("http://localhost:18080/nonexistent")
    assert resp.status == 404


def test_time(server):
    c = HttpClient()
    resp = c.get("http://localhost:18080/time")
    assert resp.status == 200
    assert b"time" in resp.body


def test_parallel_requests(server):
    results = []

    def worker():
        c = HttpClient()
        r = c.get("http://localhost:18080/echo")
        results.append(r.status)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(results) == 10
    assert all(s == 200 for s in results)
