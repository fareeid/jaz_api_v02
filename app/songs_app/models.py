from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from ..db import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    year = Column(Integer, nullable=True)