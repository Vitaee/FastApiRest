from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel
from ..db.mongo_service import db_mongo

class BaseService(ABC):
    """
    Base Service class.
    """
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

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
        return await db_mongo.get(self.collection_name, "email", search_value)

    async def get_all(self) -> List[Dict]:
        """
        Get all documents from MongoDB.
        """
        pass

    @abstractmethod
    async def update(self, object_id: str, data: BaseModel) -> Dict:
        """
        Update a document in MongoDB by object ID.
        """
        pass

    async def delete(self, object_id: str) -> Dict:
        """
        Delete a document from MongoDB by object ID.
        """
        pass