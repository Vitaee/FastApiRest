from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import student_model
from ..db.mongo_service import db_mongo
from ..crud.students import StudentService
from typing import List

student_service = StudentService()
router = APIRouter()

@router.post("/create-student", response_description="Add new student", response_model=student_model.StudentModel, tags=["Students"])
async def create_student(student: student_model.StudentModel = Body(...)):
    return await student_service.create(jsonable_encoder(student))
    
@router.get("/all-students", response_description="Get all students", response_model=List[student_model.StudentModel], tags=["Students"])
async def list_students():
    return await student_service.get_all(student_model.StudentModel)

@router.get("/student/{student_email}", response_description="Get single student", response_model=student_model.StudentModel,tags=["Students"])
async def get_student(student_email: str = ""):
    return await student_service.get(student_email)

@router.put("/update-student/{student_email}", response_description="Update student", response_model=student_model.StudentModel,tags=["Students"])
async def update_student(student:student_model.UpdateStudentModel = Body(...), student_email: str = ""):
    return await student_service.update(search_value=student_email, new_data=jsonable_encoder(student))
    

@router.delete("/del-student/{student_email}", response_description="Delete a student",tags=["Students"])
async def delete_student( student_email: str = ""):
    return await student_service.delete(email=student_email)


@router.get("/")
async def root():
    return {"message": "Hello World"}
