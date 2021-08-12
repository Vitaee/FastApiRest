from fastapi import APIRouter, HTTPException, Request, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models import student_model
from ..db.mongo_db import AsyncIOMotorClient, get_database
from ..crud.students import register_student
from ..utils.duplicate_users import check_free_name_and_email

router = APIRouter()


@router.post("/create-student", response_description="Add new student", response_model=student_model.StudentModel)
async def create_student(db: AsyncIOMotorClient = Depends(get_database), student: student_model.StudentModel = Body(...)):
    student = jsonable_encoder(student)

    await check_free_name_and_email(db, student['name'])

    dbstudent = await register_student(db, student)

    return dbstudent


@router.get("/")
async def root():
    return {"message": "Hello World"}
