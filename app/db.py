from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

async_engine = create_async_engine(settings.db_url)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
# AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False)
Base = declarative_base()

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

