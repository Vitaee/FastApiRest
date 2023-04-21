from ..db.mongo_service import db_mongo
from .base import BaseService
from ..models import student_model

class StudentService(BaseService):
    """
    Service class for Students collection in MongoDB.
    """
    def __init__(self):
        super().__init__("students", student_model.StudentModel)

    async def create(self, data):
        return await db_mongo.create(self.collection_name, data)