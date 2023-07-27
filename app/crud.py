from sqlalchemy.orm import Session

from . import models, schemas


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def get_person_by_email(db: Session, email: str):
    return db.query(models.Person).filter(models.Person.email == email).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: schemas.PersonCreate):
    fake_hashed_password = person.password + "notreallyhashed"
    db_person = models.Person(email=person.email, hashed_password=fake_hashed_password)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_person_item(db: Session, item: schemas.ItemCreate, person_id: int):
    db_item = models.Item(**item.dict(), owner_id=person_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
