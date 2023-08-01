from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .db import AsyncSessionLocal  #, create_db_and_tables
from .template import router as template
from .songs_app import routes as songs_app

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI, Docker, and Traefik")

# @app.on_event("startup")
# async def on_startup():
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()

app.include_router(template.router)
app.include_router(songs_app.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
