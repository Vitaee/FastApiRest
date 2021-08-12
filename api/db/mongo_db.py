from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None

db_mongo = Database()

async def get_database() -> AsyncIOMotorClient:
    return db_mongo.client['fastapi']