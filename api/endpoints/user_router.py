from fastapi import APIRouter, Body, Depends,HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from ..models import user_model
from ..db.mongo_service import db_mongo
from ..utils.auth_handler import JwtHandler
from ..utils.auth_bearer import JwtBearer
from ..utils.duplicate_users import check_free_name_and_email
from ..crud.users import UserService
from ..crud.students import get_single_student

router = APIRouter()
user_service = UserService()

@router.post("/user/signup", tags=["Users"])
async def create_user(db:AsyncIOMotorClient = Depends(db_mongo.get_database),user: user_model.UserSchema = Body(...)):
    user_dict = jsonable_encoder(user)
    await check_free_name_and_email(db, email=user_dict['email'])
    return await user_service.create(user_dict)

@router.post("/user/login", tags=["Users"])
async def user_login(user: user_model.UserLoginSchema = Body(...)):
    user_dict = jsonable_encoder(user)
    get_user = await user_service.get(user_dict["email"])
    if get_user:
        return await user_service.check_login(entered_password=user_dict["password"], current_password=get_user["password"], email=user_dict["email"])
       
    return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = { "error": "Wrong email / password" } )

@router.get("/user", dependencies=[Depends(JwtBearer())],   tags=["Users"])
async def current_user(user_mail: str = Depends( JwtBearer() ) ):
    return await user_service.get(user_mail)

@router.put("/user/update", dependencies=[Depends(JwtBearer())], response_model=user_model.UserSchema,tags=["Users"])
async def update_user(current_user: str = Depends( JwtBearer() ), new_data: user_model.UserUpdateSchema = Body(...)):    
    new_user_fields = {k: v for k, v in new_data.dict().items() if v is not None}

    if len(new_user_fields) >= 1:
        return await user_service.update(search_value=current_user, new_data=new_user_fields)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Please enter 1 or more field to update.")