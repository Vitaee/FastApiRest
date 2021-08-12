from pydantic import BaseModel, Field, EmailStr,validator
from bson import ObjectId
from typing import Optional, List


"""
MongoDB stores data as BSON. FastAPI encodes and decodes data as JSON strings. 
BSON has support for additional non-JSON-native data types, 
including ObjectId which can't be directly encoded as JSON. 
Because of this, we convert ObjectIds to strings before storing them as the _id.
"""

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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