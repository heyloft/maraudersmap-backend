from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from maraudersmap.extra_types import LatLong
from maraudersmap.models import ItemType, UnlockMethod


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
    item_type: ItemType
    description: str | None = None
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


class QuestItemBase(OrmBase):
    item: Item
    location: LatLong
    unlock_method: UnlockMethod


class QuestItemCreate(QuestItemBase):
    pass


class QuestItem(QuestItemBase):
    id: UUID
    item: ItemBase
    quest: QuestBase

    class Config:
        orm_mode = True


class QuestBase(OrmBase):
    title: str
    description: str
    active_from: datetime
    active_to: datetime | None = None
    unlock_method: UnlockMethod


class QuestCreate(QuestBase):
    pass


class Quest(QuestBase):
    id: UUID
    items: List[ItemBase]
    this_depends_on: List[QuestDependencyBase]
    depend_on_this: List[QuestDependencyBase]

    class Config:
        orm_mode = True


class QuestDependencyBase(OrmBase):
    quest_to_finish_before_id: UUID = Field(foreign_key="quest_to_finish_before_id")
    quest_to_finish_after_id: UUID = Field(foreign_key="quest_to_finish_after_id")


class QuestDependencyCreate(QuestDependencyBase):
    pass


class QuestParticipationBase(OrmBase):
    status: int


class QuestParticipation(QuestParticipationBase):
    quest: Quest
    user: User
