from fastapi import APIRouter, Body, Depends,HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import user_model
from ..db.mongo_db import AsyncIOMotorClient, get_database
from ..utils.auth_handler import JwtHandler
from ..utils.auth_bearer import JwtBearer
from ..utils.duplicate_users import check_free_name_and_email
from ..crud.users import register_user,update_user_data
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
            return JSONResponse(status_code = status.HTTP_200_OK, content = login_user.sign_jwt(user_dict["email"]) )
    
    return { "error": "Wrong email / password" }

@router.get("/user", dependencies=[Depends(JwtBearer())],   tags=["Users"])
async def current_user(db:AsyncIOMotorClient = Depends(get_database) , user_mail: str = Depends( JwtBearer() ) ):
    
    get_user = await get_single_student(db, email=user_mail)

    if get_user:

        return JSONResponse(status_code=status.HTTP_200_OK, content=get_user)

@router.put("/user/update", dependencies=[Depends(JwtBearer())], response_model=user_model.UserSchema,tags=["Users"])
async def update_user(db:AsyncIOMotorClient = Depends(get_database), current_user: str = Depends( JwtBearer() ), new_data: user_model.UserUpdateSchema = Body(...)):
    get_user_doc = await get_single_student(db, email=current_user)
    
    user_fields = {k: v for k, v in new_data.dict().items() if v is not None}

    if len(user_fields) >= 1:
        result = await update_user_data(db,get_user_doc['email'],user_fields)
        return result

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Please enter 1 or more field to update.")