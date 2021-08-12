import dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from .mongo_db import db_mongo
from pathlib import Path
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)



async def connect_to_mongo():
    db_mongo.client = AsyncIOMotorClient('{}'.format(os.getenv('DB_URL')))

async def close_mongo_connection():
    db_mongo.client.close()
