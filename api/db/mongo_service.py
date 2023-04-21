from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import BaseModel
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import dotenv
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

class MongoModel(BaseModel):
    id: Optional[str] = str(ObjectId())

class MongoService:
    def __init__(self, model_cls = None):
        self.mongo_client = None
        self.model_cls = model_cls
    
    async def connect_to_mongo(self):
        self.mongo_client = AsyncIOMotorClient('{}'.format(os.getenv('DB_URL')))

    async def close_mongo_connection(self):
        self.mongo_client.close()

    async def get_database(self) -> AsyncIOMotorClient:
        return self.mongo_client["studentPortal_dev"]

    async def create(self, collection_name: str, obj: MongoModel) -> MongoModel:
        result = await self.mongo_client["studentPortal_dev"][collection_name].insert_one(obj)
        obj["id"] = str(result.inserted_id)
        return obj
    
    async def get(self, collection_name: str, search_by: str, search_value: str) -> Optional[MongoModel]:
        result = await self.mongo_client["studentPortal_dev"][collection_name].find_one({f"{search_by}": search_value})
        if result:
            return result
        return None
    
    async def update(self, collection_name: str, update_search_by: str, update_search_value: str, obj: MongoModel) -> MongoModel:
        result = await self.mongo_client["studentPortal_dev"][collection_name].replace_one({f"{update_search_by}": update_search_value}, obj)
        if result.modified_count == 1:
            return result
        raise HTTPException(status_code=404, detail="Object not found")
    
    async def delete(self, collection_name, delete_by: str, delete_value: str) -> None:
        result = await self.mongo_client["studentPortal_dev"][collection_name].delete_one({f"{delete_by}": delete_value})
        if result.deleted_count != 1:
            raise HTTPException(status_code=404, detail="Object not found")
    
    async def get_all(self, collection_name: str, skip: int = 0, limit: int = 5, sort_by: Optional[str] = None) -> List[MongoModel]:
        query = {}
        sort = []
        if sort_by:
            sort.append((sort_by, 1))
        result = await self.mongo_client["studentPortal_dev"][collection_name].find(query, skip=skip, limit=limit, sort=sort)
        return [self.model_cls(**doc) async for doc in result]
    
db_mongo = MongoService()