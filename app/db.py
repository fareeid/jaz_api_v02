from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

async_engine = create_async_engine(settings.db_url)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
# AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False)
Base = declarative_base()

from .template.models import Person, Item, Note
from .songs_app.models import Song

# Dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        # async with session.begin():
        yield session

# async def create_db_and_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

