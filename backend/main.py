from fastapi import FastAPI
from api.v1.user_router import user_router
from api.v1.blog_router import blog_router
from core.config import settings



app = FastAPI(title = settings.PROJECT_TITLE, version = settings.PROJECT_VERSION)

app.include_router(user_router, prefix = "/User", tags = ["User"])
app.include_router(blog_router, prefix = "/Blog", tags = ["Blog"])