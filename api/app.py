from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}