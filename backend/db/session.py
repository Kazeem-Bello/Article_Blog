from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from core.config import settings


DB_URL = settings.POSTGRES_URL

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit = False, autoflush = False, bind = engine
)



AsyncSessionLocal = sessionmaker(
    bind = engine, class_ = AsyncSession, expire_on_commit = False
)

class Base(DeclarativeBase):
    pass