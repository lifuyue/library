from fastapi.testclient import TestClient

# Import the FastAPI app from backend root (container copies backend/ into /app)
from main import app


client = TestClient(app)


def test_health_endpoint_returns_200():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("status") == "healthy"


def test_root_endpoint_returns_200():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_healthz_endpoint_returns_200():
    resp = client.get("/api/healthz")
    assert resp.status_code == 200
    assert resp.json().get("status") == "healthy"


def test_root_healthz_returns_200():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json().get("status") == "healthy"
