from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from ..models import student_model
from ..db.mongo_db import AsyncIOMotorClient, get_database
from ..crud.students import register_student, get_all_students, get_db_student
from ..utils.duplicate_users import check_free_name_and_email

router = APIRouter()


@router.post("/create-student", response_description="Add new student", response_model=student_model.StudentModel)
async def create_student(db: AsyncIOMotorClient = Depends(get_database), student: student_model.StudentModel = Body(...)):
    student = jsonable_encoder(student)

    await check_free_name_and_email(db, student['name'])

    dbstudent = await register_student(db, student)

    return dbstudent

@router.get("/all-students", response_description="Get all students", response_model=student_model.StudentModel)
async def list_students(db: AsyncIOMotorClient = Depends(get_database)):
    all_students = await get_all_students(db)

    return all_students


@router.get("/student/{student_name}", response_description="Get single student", response_model=student_model.StudentModel)
async def get_student(db: AsyncIOMotorClient = Depends(get_database), student_name: str = ""):
    the_student = await get_db_student(db, student_name)
 
    return the_student


@router.get("/")
async def root():
    return {"message": "Hello World"}
