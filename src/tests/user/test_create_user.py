from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from main import app

client = TestClient(app)


def test_create_user():
    user_data = {
        "first_name": "Can",
        "last_name": "Ilgu",
        "bio":"Software Engineer",
        "email": "can@gmail.com",
        "password": "123456"
    }

    response = client.get('/')
    assert response.status_code == 200

    response = client.post("/user/signup/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["password"] != user_data["password"]