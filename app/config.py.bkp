# app/config.py

import os

from pydantic import Field
from pydantic import BaseSettings


class Settings(BaseSettings): 
    db_url: str = Field(..., env='DATABASE_URL') 

settings = Settings() # type: ignore