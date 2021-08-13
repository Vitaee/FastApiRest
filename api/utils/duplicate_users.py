from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ..db.mongo_db import AsyncIOMotorClient
from ..crud.students import get_single_student


async def check_free_name_and_email(conn:AsyncIOMotorClient, name: Optional[str] = None, email: Optional[EmailStr] = None) -> None:
    if name:
        user_by_name = await get_single_student(conn, name=name)

        if user_by_name:
            raise HTTPException( status_code= HTTP_422_UNPROCESSABLE_ENTITY, 
            detail= "User with this name already exists.")

    if email:
        user_by_email = await get_single_student(conn, email=email)
        if user_by_email:
            raise HTTPException( status_code= HTTP_422_UNPROCESSABLE_ENTITY, 
            detail= "User with this email already exists.")
