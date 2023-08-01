from typing import Union
from pydantic import BaseModel


class SongBase(BaseModel):
    name: str
    artist: str
    year: Union[int, None] = None


class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: int

    class Config:
        from_attributes = True