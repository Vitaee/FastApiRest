from fastapi.exceptions import HTTPException
from ..db.mongo_service import db_mongo
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi import status
from ..utils.auth_handler import JwtHandler
from ..models import user_model
from fastapi.encoders import jsonable_encoder
from .base import BaseService
class UserService(BaseService):
    """
    Service class for Users collection in MongoDB.
    """
    def __init__(self):
        super().__init__("users")

    async def create(self, user) -> JSONResponse:
        auth_user = JwtHandler()
        hashed_password = auth_user.encode_password(user["password"])
        user["password"] = hashed_password
        new_user = await db_mongo.create(self.collection_name, user)
        
        try:
            created_user = await db_mongo.get(self.collection_name, "_id", new_user["_id"], user_model.UserSchema)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(created_user))
        except Exception as err:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error':'We faced unexpected error.' , 'message': err})

    async def update(self, search_by = "email", search_value: str = "", new_data: dict = {}) -> JSONResponse:
        return await db_mongo.update(self.collection_name, search_by, search_value, new_data)

    async def check_login(self, entered_password: str, current_password: str, email: str):
        login_user = JwtHandler()
        if login_user.verify_password(entered_password , current_password):
            return JSONResponse(status_code = status.HTTP_200_OK, content = login_user.sign_jwt(email))