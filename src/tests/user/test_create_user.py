import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from tests.fixtures import test_client


def test_create_user(test_client):
    user_data = {
        "first_name": "Can",
        "last_name": "Ilgu",
        "bio":"Software Engineer",
        "email": "can@gmail.com",
        "password": "123456"
    }

    response =  test_client.post("/user/signup", json=user_data)

    assert response.status_code == 201