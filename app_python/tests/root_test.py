from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root_endpoint_structure():
    """Test root endpoint returns expected structure and fields"""
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    # Check main sections exist
    assert "service" in data
    assert "system" in data
    assert "runtime" in data
    assert "request" in data
    assert "endpoints" in data

    # Check service fields
    service = data["service"]
    assert "name" in service
    assert "version" in service
    assert "description" in service
    assert "framework" in service
    assert service["framework"] == "FastAPI"

    # Check system fields
    system = data["system"]
    assert "hostname" in system
    assert "platform" in system
    assert "architecture" in system
    assert "python_version" in system

    # Check runtime fields
    runtime = data["runtime"]
    assert "uptime_seconds" in runtime
    assert "uptime_human" in runtime
    assert "current_time" in runtime
    assert "timezone" in runtime
    assert isinstance(runtime["uptime_seconds"], int)
    assert runtime["uptime_seconds"] >= 0

    # Check request fields
    request_info = data["request"]
    assert "client_ip" in request_info
    assert "user_agent" in request_info
    assert "method" in request_info
    assert "path" in request_info
    assert request_info["method"] == "GET"
    assert request_info["path"] == "/"

    # Check endpoints is a list
    assert isinstance(data["endpoints"], list)
    assert len(data["endpoints"]) >= 1
