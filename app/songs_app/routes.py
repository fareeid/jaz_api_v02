from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session

from . import schemas, service

router = APIRouter(
    prefix="/alembic_try"
)

@router.get("/ping/")
async def pong():
    return {"ping": "pong!"}

@router.get("/songs/", response_model=list[schemas.Song])  # , response_model=list[schemas.Song]
async def read_songs(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    songs = await service.get_songs(session, skip=skip, limit=limit)
    print("From Songs Asyn version ---******************************------")
    print(type(songs))
    print(type(songs[0]))
    return songs

@router.post("/songs/") # , response_model=schemas.Person
async def create_song(song: schemas.SongCreate, session: AsyncSession = Depends(get_session)):
    db_song = await service.get_song_by_name(session, name=song.name)
    if db_song:
        raise HTTPException(status_code=400, detail="Song already created")
    return await service.create_song(async_db=session, song=song)