from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from main import app

client = TestClient(app)


def test_create_user():
    user_data = {
        "name": "Can Ilgu",
        "email": "can@example.com",
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "gpa": "3.0",
    }
    response = client.post("/create-student/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["gpa"] == user_data["gpa"]