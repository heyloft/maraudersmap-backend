from uuid import UUID

from pydantic import BaseModel

from maraudersmap.extra_types import LatLong


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    location: LatLong | None = None

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    collectible: bool
    location: LatLong


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID

    class Config:
        orm_mode = True
