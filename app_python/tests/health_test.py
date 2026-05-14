from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_endpoint():
    """Test health endpoint returns correct status"""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "timestamp" in data
    assert "uptime_seconds" in data

    assert data["status"] == "healthy"
    assert isinstance(data["uptime_seconds"], int)
    assert data["uptime_seconds"] >= 0
