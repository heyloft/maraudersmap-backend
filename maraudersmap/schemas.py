from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from maraudersmap.models import ItemType


class OrmBase(BaseModel):
    class Config:
        orm_mode = True


class UserBase(OrmBase):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID


class ItemBase(OrmBase):
    title: str
    description: str | None = None
    item_type: ItemType
    icon: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID


class ItemOwnershipBase(OrmBase):
    obtained_at: datetime


class ItemOwnership(ItemOwnershipBase):
    id: UUID
    item: ItemBase
    owner: UserBase


class ItemOwnershipCreate(ItemOwnershipBase):
    owner_id: UUID = Field(foreign_key="user.id")
    item_id: UUID = Field(foreign_key="item.id")


class QuestBase(OrmBase):
    title: str


class Quest(QuestBase):
    id: UUID


class QuestParticipationBase(OrmBase):
    status: int


class QuestParticipation(QuestParticipationBase):
    quest: Quest
    user: User
