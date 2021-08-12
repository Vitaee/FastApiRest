from ..db.mongo_db import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi import status

async def register_student(conn: AsyncIOMotorClient, student) -> JSONResponse:
    new_student = await conn["students"].insert_one(student)
    
    try:
        created_student = await conn["students"].find_one({"_id": new_student.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error':'We faced unexpected error.' , 'message': err})


async def get_student(conn: AsyncIOMotorClient, name: str) -> dict:
    db_student = await conn["students"].find_one({'name':name})
    if db_student:
        return db_student