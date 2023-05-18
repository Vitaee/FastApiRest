import sys, os, pytest
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from main import app
from src.config.mongo_service import db_mongo


@pytest.mark.anyio
async def test_create_user():
    user_data = {
        "name": "Can Ilgu",
        "email": "can@example.com",
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "gpa": "3.0",
    }

    

    async with AsyncClient(app=app, base_url="http://localhost:5002") as ac:
        await db_mongo.connect_to_mongo()
        response = await ac.post("/create-student", json=user_data)
        
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["gpa"] == user_data["gpa"]
    await db_mongo.close_mongo_connection()