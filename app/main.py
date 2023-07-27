from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI, Docker, and Traefik")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# async def read_root():
#     return await models.Person.objects.all()

@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.get_person_by_email(db, email=person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_person(db=db, person=person)


@app.get("/persons/", response_model=list[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons


@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.post("/persons/{person_id}/items/", response_model=schemas.Item)
def create_item_for_person(
    person_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_person_item(db=db, item=item, person_id=person_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


from app.db import database, User


# @app.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         await database.connect()
#     # create a dummy entry
#     await models.Person.objects.get_or_create(email="test1@test2.com", hashed_password="fake_hashed_password")

   

# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()

