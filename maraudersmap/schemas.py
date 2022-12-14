from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from maraudersmap.extra_types import LatLong
from maraudersmap.models import ItemType, QuestStatus, UnlockMethod


class OrmBase(BaseModel):
    class Config:
        orm_mode = True


class EventBase(OrmBase):
    active_from: datetime
    active_to: datetime


class Event(EventBase):
    id: UUID


class EventCreate(EventBase):
    pass


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


class QuestItemBase(OrmBase):
    location: LatLong | None = None
    unlock_method: UnlockMethod


class QuestItemCreate(QuestItemBase):
    item_id: UUID


class QuestItem(QuestItemBase):
    id: UUID
    item: Item
    quest_id: UUID


class ItemOwnershipBase(OrmBase):
    obtained_at: datetime


class ItemOwnership(ItemOwnershipBase):
    id: UUID
    quest_item: QuestItem
    owner: User


class ItemOwnershipCreate(ItemOwnershipBase):
    quest_item_id: UUID = Field(foreign_key="quest_item_id")


class QuestBase(OrmBase):
    title: str
    description: str
    active_from: datetime
    active_to: datetime | None = None
    unlock_method: UnlockMethod
    location: LatLong
    event_id: UUID


class QuestCreate(QuestBase):
    pass


class Quest(QuestBase):
    id: UUID
    items: list[QuestItem]


class QuestParticipationBase(OrmBase):
    status: QuestStatus


class QuestParticipation(QuestParticipationBase):
    quest: Quest
    user: User


class QuestParticipationCreate(QuestParticipationBase):
    quest_id: UUID


class QuestParticipationUpdate(QuestParticipationBase):
    pass


class QuestDependencyBase(OrmBase):
    quest_to_finish_before_id: UUID = Field(foreign_key="quest_to_finish_before_id")
    quest_to_finish_after_id: UUID = Field(foreign_key="quest_to_finish_after_id")


class QuestDependencyCreate(QuestDependencyBase):
    pass


class EventParticipationBase(OrmBase):
    status: int


class EventParticipationCreate(EventParticipationBase):
    event_id: UUID


class EventParticipation(EventParticipationBase):
    event: Event
    user: User


class EventParticipationUpdate(EventParticipationBase):
    pass


QuestItem.update_forward_refs()
