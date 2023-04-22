from ..db.mongo_service import db_mongo
from .base import BaseService
from ..models import student_model
from fastapi.responses import JSONResponse
from fastapi import status

class StudentService(BaseService):
    """
    Service class for Students collection in MongoDB.
    """
    def __init__(self):
        super().__init__("students", student_model.StudentModel)

    async def create(self, data):
        result = await db_mongo.create(self.collection_name, data)
        if result:
            return JSONResponse(status_code = status.HTTP_201_CREATED, content = { "data": result } )
    
        return JSONResponse(status_code = status.HTTP_409_CONFLICT, content = { "data": result } )
