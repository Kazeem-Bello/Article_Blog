from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings


DB_URL = settings.POSTGRES_URL

print(DB_URL)