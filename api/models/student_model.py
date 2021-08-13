from pydantic import BaseModel, Field, EmailStr,validator
from bson import ObjectId
from typing import Optional, List
from ..utils import mongoObjectId



class StudentModel(BaseModel):
    id: mongoObjectId.PyObjectId = Field(default_factory=mongoObjectId.PyObjectId, alias="_id")
    name: str = Field(...)

    @validator('name')
    def name_must_contain_space(cls, v):
        if len(v.split(" ")) == 1:
            raise ValueError('Value must contains space.')

        return " ".join(v.split(" "))

    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Can Ilgu",
                "email": "can@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Can Ilgu",
                "email": "can@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.2",
            }
        }