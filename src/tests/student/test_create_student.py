import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from tests.fixtures import test_client


def test_create_user(test_client):
    test_student = {
        "name": "Can Ilgu",
        "email": "can@example.com",
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "gpa": "3.0",
    }
    response = test_client.post("/create-student", json=test_student)
    assert response.status_code == 201