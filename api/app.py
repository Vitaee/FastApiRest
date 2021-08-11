from api.db.mongo_db import mongo_connection
from fastapi import APIRouter, HTTPException
from .db import mongo_db

router = APIRouter()
db = mongo_db.mongo_connection()


@router.get("/")
async def root():
    return {"message": "Hello World"}