from fastapi.exceptions import HTTPException
from ..db.mongo_db import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi import status



def db_student_status(db_student : list) -> bool:
    if len(db_student) > 1:
        return False
    return True


async def get_single_student(conn: AsyncIOMotorClient, name: str) -> dict:
    db_student = await conn["students"].find_one({'name':name})
     
    if db_student:
        return db_student

async def register_student(conn: AsyncIOMotorClient, student) -> JSONResponse:
    new_student = await conn["students"].insert_one(student)
    
    try:
        created_student = await conn["students"].find_one({"_id": new_student.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error':'We faced unexpected error.' , 'message': err})

async def get_db_student(conn:AsyncIOMotorClient, name:str = "") -> JSONResponse:
    db_student_regex =  await conn["students"].aggregate( [{'$match':{'name':{ "$regex":f'{name}'}}}] ).to_list(length=None)

    if db_student_regex:

        status_student = db_student_status(db_student=db_student_regex)  
        if not status_student:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='To many student results ( > 1 ) please also enter last name of student.')
        
        else: return JSONResponse(status_code=status.HTTP_200_OK,content=db_student_regex)
    else:
        
        raise HTTPException(status_code=404, detail=f"Student {name} not found")
        
async def get_all_students(conn: AsyncIOMotorClient) -> JSONResponse:
    students = await conn["students"].find().to_list(1000)

    return JSONResponse(status_code=status.HTTP_200_OK, content=students)

async def update_the_student(conn: AsyncIOMotorClient, name: str = "", student : dict = {}) -> JSONResponse:
    update_result = await conn["students"].update_one({"name":name}, {"$set":student})

    if update_result.modified_count == 1:
        if updated_student := await conn["students"].find_one({"name":name}) is not None:

            return JSONResponse(status_code= status.HTTP_200_OK, content=updated_student)
    
    if (existing_student := await conn["students"].find_one({"name":name})) is not None:

        return JSONResponse(status_code = status.HTTP_200_OK, content=existing_student)


 
    raise HTTPException(status_code=404, detail=f"Student {name} not found.")

async def delete_student_fromdb(conn: AsyncIOMotorClient, name: str) -> JSONResponse:
    delete_result = await conn["students"].delete_one({"name": name})

    if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"detail":f"Student {name} deleted successfully."})

    raise HTTPException(status_code=404, detail=f"Student {name} not found")