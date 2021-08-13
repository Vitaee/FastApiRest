from fastapi.exceptions import HTTPException
from ..db.mongo_db import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi import status
from ..utils.auth_handler import JwtHandler



async def register_user(conn:AsyncIOMotorClient, user):
    auth_user = JwtHandler()
    hashed_password = auth_user.encode_password(user["password"])
    user["password"] = hashed_password
    new_user = await conn["users"].insert_one(user)
    
    try:
        created_user = await conn["users"].find_one({"_id": new_user.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error':'We faced unexpected error.' , 'message': err})

