from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas

async def get_songs(async_db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await async_db.execute(select(models.Song))
    return result.scalars().all()

async def get_song_by_name(async_db: AsyncSession, name: str):
    result = await async_db.execute(select(models.Song).where(models.Song.name==name))
    return result.scalars().all()

async def create_song(async_db: AsyncSession, song: schemas.SongCreate):
    db_song = models.Song(name=song.name, artist=song.artist, year=song.year)
    async_db.add(db_song)
    await async_db.commit()
    await async_db.refresh(db_song)
    return db_song