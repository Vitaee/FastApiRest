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
    student = jsonable_encoder(student)
    result = await student_service.create(student)
    if result:
        return JSONResponse(status_code = status.HTTP_201_CREATED, content = { "data": result } )
    
    return JSONResponse(status_code = status.HTTP_409_CONFLICT, content = { "data": result } )

@router.get("/all-students", response_description="Get all students", response_model=List[student_model.StudentModel], tags=["Students"])
async def list_students():
    return await student_service.get_all(student_model.StudentModel)

@router.get("/student/{student_email}", response_description="Get single student", response_model=student_model.StudentModel,tags=["Students"])
async def get_student(student_email: str = ""):
    return await student_service.get(student_email)

@router.put("/update-student/{student_email}", response_description="Update student", response_model=student_model.StudentModel,tags=["Students"])
async def update_student(student:student_model.UpdateStudentModel = Body(...), student_email: str = ""):
    new_student_fields = {k: v for k, v in student.dict().items() if v is not None}

    if new_student_fields != {}:
        return await student_service.update(search_value=student_email, new_data=new_student_fields)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Please enter 1 or more field to update.")

@router.delete("/del-student/{student_email}", response_description="Delete a student",tags=["Students"])
async def delete_student( student_email: str = ""):
    return await student_service.delete(email=student_email)


@router.get("/")
async def root():
    return {"message": "Hello World"}
