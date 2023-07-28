from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .db import AsyncSessionLocal, create_db_and_tables

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI, Docker, and Traefik")

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


# Dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        # async with session.begin():
        yield session

@app.post("/persons/") # , response_model=schemas.Person
async def create_person(person: schemas.PersonCreate, session: AsyncSession = Depends(get_session)):
    db_person = await crud.get_person_by_email(session, email=person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_person(async_db=session, person=person)

@app.get("/persons/")  # , response_model=list[schemas.Person]
async def read_persons(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    persons = await crud.get_persons(session, skip=skip, limit=limit)
    return persons

@app.get("/persons/{person_id}") #, response_model=schemas.Person
async def read_person(person_id: int, session: AsyncSession = Depends(get_session)):
    db_person = await crud.get_person(session, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.post("/persons/{person_id}/items/") # , response_model=schemas.Item
async def create_item_for_person(
    person_id: int, item: schemas.ItemCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_person_item(async_db=session, item=item, person_id=person_id)


@app.get("/items/") # , response_model=list[schemas.Item]
async def read_items(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    items = await crud.get_items(session, skip=skip, limit=limit)
    return items

# @app.post("/personsb/")    # , response_model=schemas.Person
# async def create_personb(person: schemas.PersonCreate):
#     async with AsyncSessionLocal() as session:
#         async with session.begin():
#             db_person = await crud.get_person_by_email(session, email=person.email)
#             if db_person:
#                 raise HTTPException(status_code=400, detail="Email already registered")
#             return await crud.create_person(async_db=session, person=person)


# @app.get("/personsb/", response_model=list[schemas.Person])
# async def read_personsb(skip: int = 0, limit: int = 100):
#     async with AsyncSessionLocal() as session:
#         async with session.begin():
#             persons = await crud.get_persons(session, skip=skip, limit=limit)
#             return persons

# @app.get("/")
# async def read_root():
#     return await models.Person.objects.all()
