from dotenv import load_dotenv
from pathlib import Path
import os
import motor.motor_asyncio

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path = dotenv_path)

def mongo_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DB_URL'))
    db_name = os.getenv('DB_NAME')
    db = client.db_name
    
    print("\t  [LOG] Mongodb Connected.")
    return db

