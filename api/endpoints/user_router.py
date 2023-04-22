from fastapi import APIRouter, Body, Depends,HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import user_model
from ..db.mongo_service import db_mongo
from ..utils.auth_bearer import JwtBearer
from ..crud.users import UserService

router = APIRouter()
user_service = UserService()

@router.post("/user/signup", tags=["Users"])
async def create_user(user: user_model.UserSchema = Body(...)):
    user_dict = jsonable_encoder(user)
    return await user_service.create(user_dict)

@router.post("/user/login", tags=["Users"])
async def user_login(user: user_model.UserLoginSchema = Body(...)):
    get_user = await user_service.get(user.email)
    if get_user:
        return await user_service.check_login(entered_password=user.password, current_password=get_user.password, email=user.email)
    
    return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = { "error": "Wrong email / password" } )

@router.get("/user", dependencies=[Depends(JwtBearer())],   tags=["Users"])
async def current_user(user_mail: str = Depends( JwtBearer() ) ):
    return await user_service.get(user_mail)

@router.put("/user/update", dependencies=[Depends(JwtBearer())], response_model=user_model.UserSchema,tags=["Users"])
async def update_user(current_user: str = Depends( JwtBearer() ), new_data: user_model.UserUpdateSchema = Body(...)):    
    return await user_service.update(search_value=current_user, new_data=jsonable_encoder(new_data))

