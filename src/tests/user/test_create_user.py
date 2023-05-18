from httpx import AsyncClient
import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from main import app
from src.config.mongo_service import db_mongo

@pytest.mark.anyio
async def test_create_user():
    user_data = {
        "first_name": "Can",
        "last_name": "Ilgu",
        "bio":"Software Engineer",
        "email": "can@gmail.com",
        "password": "123456"
    }

    async with AsyncClient(app=app, base_url="http://localhost:5002") as ac:
        await db_mongo.connect_to_mongo()
        response = await ac.post("/user/signup", json=user_data)

    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["password"] != user_data["password"]
    await db_mongo.close_mongo_connection()