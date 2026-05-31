from fastapi import FastAPI, Request
from api.main import api_router
from core.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI(title = settings.PROJECT_TITLE, version = settings.PROJECT_VERSION)


app.include_router(api_router)


app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


# Frontend HTML files
app.mount(
    "/",
    StaticFiles(directory="../frontend/templates", html=True),
    name="frontend"
)

templates = Jinja2Templates(directory="../frontend/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", 
                                      context={"request": request})



