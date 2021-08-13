from fastapi import APIRouter, Body, Depends,HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import user_model
from ..db.mongo_db import AsyncIOMotorClient, get_database
from ..utils.auth_handler import JwtHandler
from ..utils.auth_bearer import JwtBearer
from ..utils.duplicate_users import check_free_name_and_email
from ..crud.users import register_user
from ..crud.students import get_single_student
router = APIRouter()

@router.post("/user/signup", tags=["Users"])
async def create_user(db:AsyncIOMotorClient = Depends(get_database),user: user_model.UserSchema = Body(...)):
    user_dict = jsonable_encoder(user)
    
    await check_free_name_and_email(db, email=user_dict['email'])

    save_user = await register_user(db, user_dict)

    return save_user


@router.post("/user/login", tags=["Users"])
async def user_login(db:AsyncIOMotorClient = Depends(get_database), user: user_model.UserLoginSchema = Body(...)):
    user_dict = jsonable_encoder(user)
    login_user = JwtHandler()
    get_user = await get_single_student(db, email=user_dict["email"])
    
    if get_user:
    
        if login_user.verify_password(user_dict["password"],get_user["password"]):

            return JSONResponse(status_code = status.HTTP_200_OK, content = login_user.sign_jwt(user.email) )
    
    return { "error": "Wrong email / password" }

@router.get("/user", dependencies=[Depends(JwtBearer())],tags=["Users"])
async def current_user(db:AsyncIOMotorClient = Depends(get_database)):
    return {"msg":"You got user.."}