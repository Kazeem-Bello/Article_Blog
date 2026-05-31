from fastapi import APIRouter
from api.v1.user_router import user_router
from api.v1.blog_router import blog_router
from api.v1.auth_router import auth_router


api_router = APIRouter(prefix="/api/v1")


api_router.include_router(user_router, prefix = "/user", tags = ["User"])
api_router.include_router(blog_router, prefix = "/blog", tags = ["Blog"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])