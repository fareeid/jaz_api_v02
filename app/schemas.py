from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class PersonBase(BaseModel):
    email: str


class PersonCreate(PersonBase):
    hashed_password: str


class Person(PersonBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True