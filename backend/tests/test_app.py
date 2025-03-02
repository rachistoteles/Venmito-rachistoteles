# backend/tests/test_app.py
from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app object

client = TestClient(app)

def test_create_user():
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secretpassword"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201  # HTTP 201 Created
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
