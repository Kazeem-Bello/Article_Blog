from fastapi import APIRouter, status, HTTPException

from fastapi import HTTPException

user_router = APIRouter()


@user_router.get("/", status_code = status.HTTP_200_OK)
async def home():
    return {"message": "welcome home"}