from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, service
from ..db import get_session

router = APIRouter(
    prefix="/template"
)

@router.post("/persons/") # , response_model=schemas.Person
async def create_person(person: schemas.PersonCreate, session: AsyncSession = Depends(get_session)):
    db_person = await service.get_person_by_email(session, email=person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await service.create_person(async_db=session, person=person)

@router.get("/persons/", response_model=list[schemas.Person])  # , response_model=list[schemas.Person]
async def read_persons(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    persons = await service.get_persons(session, skip=skip, limit=limit)
    print("From Asyn version ******************************")
    print(type(persons))
    print(type(persons[0]))
    return persons

@router.get("/persons/{person_id}", response_model=schemas.Person) #, response_model=schemas.Person
async def read_person(person_id: int, session: AsyncSession = Depends(get_session)):
    db_person = await service.get_person(session, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    print(type(db_person))
    return db_person


@router.post("/persons/{person_id}/items/") # , response_model=schemas.Item
async def create_item_for_person(
    person_id: int, item: schemas.ItemCreate, session: AsyncSession = Depends(get_session)
):
    return await service.create_person_item(async_db=session, item=item, person_id=person_id)


@router.get("/items/") # , response_model=list[schemas.Item]
async def read_items(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    items = await service.get_items(session, skip=skip, limit=limit)
    return items

@router.post("/notes/", response_model=schemas.Note) # 
async def create_note(note: schemas.NoteIn, session: AsyncSession = Depends(get_session)):
    new_db_note = await service.create_note(async_db=session, note=note)
    print(type(new_db_note))
    return new_db_note

@router.get("/notes/{note_id}", response_model=list[schemas.Note]) # , response_model=list[schemas.Note]
async def read_note(note_id: int, session: AsyncSession = Depends(get_session)):
    db_note = await service.get_note_by_id(session, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    print(type(db_note[0]))
    return db_note

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
