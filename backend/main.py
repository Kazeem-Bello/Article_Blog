from fastapi import FastAPI
from api.user_router import user_router
from core.config import settings


app = FastAPI(title = settings.PROJECT_TITLE, version = settings.PROJECT_VERSION)

app.include_router(user_router, prefix = "/User", tags = ["User"])