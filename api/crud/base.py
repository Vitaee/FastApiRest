from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel
from ..db.mongo_service import db_mongo

class BaseService(ABC):
    """
    Base Service class.
    """
    def __init__(self, collection_name: str, model_cls: BaseModel):
        self.collection_name = collection_name
        self.model_cls = model_cls

    @abstractmethod
    async def create(self, data: BaseModel) -> Dict:
        """
        Create a document in MongoDB.
        """
        pass

    async def get(self, search_value: str) -> Dict:
        """
        Get a document from MongoDB service.
        """
        return await db_mongo.get(self.collection_name, "email", search_value, self.model_cls)

    async def get_all(self, model):
        """
        Get all documents from MongoDB.
        """
        return await db_mongo.get_all(self.collection_name, model_cls=model)

    async def update(self, search_by: str = "email", search_value: str = "", new_data: BaseModel = None):
        """
        Update a document in MongoDB by object ID.
        """
        return await db_mongo.update(self.collection_name, search_by, search_value, new_data)


    async def delete(self, email: str) -> Dict:
        """
        Delete a document from MongoDB by object ID.
        """
        return await db_mongo.delete(self.collection_name, email )
