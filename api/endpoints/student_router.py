from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from ..models import student_model
from ..db.mongo_service import db_mongo
from ..crud.students import register_student, get_all_students, get_db_student, update_the_student, delete_student_fromdb
from ..utils.duplicate_users import check_free_name_and_email
from ..crud.students import StudentService

student_service = StudentService()
router = APIRouter()

@router.post("/create-student", response_description="Add new student", response_model=student_model.StudentModel, tags=["Students"])
async def create_student(db: AsyncIOMotorClient = Depends(db_mongo.get_database), student: student_model.StudentModel = Body(...)):
    student = jsonable_encoder(student)

    await check_free_name_and_email(db, student['name'])

    dbstudent = await register_student(db, student)

    return dbstudent

@router.get("/all-students", response_description="Get all students", response_model=student_model.StudentModel, tags=["Students"])
async def list_students(db: AsyncIOMotorClient = Depends(db_mongo.get_database)):
    all_students = await get_all_students(db)

    return all_students


@router.get("/student/{student_name}", response_description="Get single student", response_model=student_model.StudentModel,tags=["Students"])
async def get_student(db: AsyncIOMotorClient = Depends(db_mongo.get_database), student_name: str = ""):
    the_student = await get_db_student(db, student_name)
 
    return the_student

@router.put("/update-student/{student_name}", response_description="Update student", response_model=student_model.StudentModel,tags=["Students"])
async def update_student(db:AsyncIOMotorClient = Depends(db_mongo.get_database), student:student_model.UpdateStudentModel = Body(...), student_name: str = ""):
    # check given student name if results is more than 1 raise exception.
    await get_db_student(db, student_name) 

    # check given fields if less than 1 raise exception.
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        result = await update_the_student(db,student_name,student)
        return result

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Please enter 1 or more field to update.")

@router.delete("/del-student/{student_name}", response_description="Delete a student",tags=["Students"])
async def delete_student(db: AsyncIOMotorClient = Depends(db_mongo.get_database), student_name: str = ""):
    await get_db_student(db, student_name) 

    delete_student = delete_student_fromdb(db , student_name)

    return delete_student


@router.get("/")
async def root():
    return {"message": "Hello World"}
