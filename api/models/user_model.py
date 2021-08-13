from ..utils import mongoObjectId
from pydantic import BaseModel, Field, EmailStr,validator
from bson import ObjectId
from typing import Optional

class UserSchema(BaseModel):
    id: mongoObjectId.PyObjectId = Field(default_factory=mongoObjectId.PyObjectId, alias="_id") 
    first_name: str = Field(...)
    last_name: str = Field(...)
    bio: Optional[str] = ""
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Can",
                "last_name": "Ilgu",
                "bio":"Software Engineer",
                "email": "can@gmail.com",
                "password": "123456"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "can@x.com",
                "password": "123456"
            }
        }