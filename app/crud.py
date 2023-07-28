from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas


async def get_person(async_db: AsyncSession, person_id: int):
    person = await async_db.get(models.Person, person_id)
    return person


async def get_person_by_email(async_db: AsyncSession, email: str):
    result = await async_db.execute(select(models.Person).where(models.Person.email==email))
    return result.scalars().all()


async def get_persons(async_db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await async_db.execute(select(models.Person))
    return result.scalars().all()


async def create_person(async_db: AsyncSession, person: schemas.PersonCreate):
    fake_hashed_password = person.hashed_password + "notreallyhashed"
    db_person = models.Person(email=person.email, hashed_password=fake_hashed_password)
    async_db.add(db_person)
    await async_db.commit()
    await async_db.refresh(db_person)
    return db_person


async def get_items(async_db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await async_db.execute(select(models.Item))
    return result.scalars().all()


async def create_person_item(async_db: AsyncSession, item: schemas.ItemCreate, person_id: int):
    db_item = models.Item(**item.dict(), owner_id=person_id)
    async_db.add(db_item)
    await async_db.commit()
    await async_db.refresh(db_item)
    return db_item

async def create_note(async_db: AsyncSession, note: schemas.NoteIn):
    db_note = models.Note(text=note.text, completed=note.completed)
    async_db.add(db_note)
    await async_db.commit()
    await async_db.refresh(db_note)
    return db_note

async def get_note_by_id(async_db: AsyncSession, note_id: int):
    result = await async_db.execute(select(models.Note).where(models.Note.id==note_id))
    return result.scalars().all()