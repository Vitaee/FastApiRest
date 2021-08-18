from fastapi.exceptions import HTTPException
from ..db.mongo_db import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi import status
from ..utils.auth_handler import JwtHandler



async def register_user(conn:AsyncIOMotorClient, user) -> JSONResponse:
    auth_user = JwtHandler()
    hashed_password = auth_user.encode_password(user["password"])
    user["password"] = hashed_password
    new_user = await conn["users"].insert_one(user)
    
    try:
        created_user = await conn["users"].find_one({"_id": new_user.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error':'We faced unexpected error.' , 'message': err})


async def update_user_data(conn:AsyncIOMotorClient, email, new_data: dict = {}) -> JSONResponse:
    update_result = await conn["users"].update_one({"email":email}, {"$set":new_data})

    if update_result.modified_count == 1:
        if updated_user := await conn["users"].find_one({"email":email}) is not None:

            return JSONResponse(status_code= status.HTTP_200_OK, content=updated_user)
    
    if (existing_user := await conn["users"].find_one({"email":email})) is not None:

        return JSONResponse(status_code = status.HTTP_200_OK, content=existing_user)


 
    raise HTTPException(status_code=500, detail=f"We can't find any user with this {email} email.")
