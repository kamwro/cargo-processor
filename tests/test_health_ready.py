from fastapi.testclient import TestClient

from app.api import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def test_health_ok():
    client = _client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    assert r.headers.get("content-type", "").startswith("application/json")


def test_ready_ok():
    client = _client()
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}
    assert r.headers.get("content-type", "").startswith("application/json")
