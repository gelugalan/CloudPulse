from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "CloudPulse API is running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Test task"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data