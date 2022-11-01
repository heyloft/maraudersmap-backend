from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from maraudersmap.database.base_class import Base
from maraudersmap.extra_types import LatLongColumnType


class ItemType(Enum):
    COLLECTIBLE = "COLLECTIBLE"
    VOUCHER = "VOUCHER"
    KEY = "KEY"
    POI = "POI"


class QuestStatus(Enum):
    HIDDEN = "HIDDEN"
    UNSTARTED = "UNSTARTED"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    item_type = Column(SQLEnum(ItemType))
    title = Column(String)
    description = Column(String)
    icon = Column(String)
    instances = relationship("QuestItem", back_populates="item")

    def __repr__(self):
        return "<Item(title='%s')>" % self.title


class UnlockMethod(Enum):
    QR_CODE = "QR_CODE"
    LOCATION = "LOCATION"
    QUEST_COMPLETION = "QUEST_COMPLETION"


class Quest(Base):
    __tablename__ = "quests"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    active_from = Column(DateTime, default=datetime.now)
    active_to = Column(DateTime, nullable=True)
    unlock_method = Column(SQLEnum(UnlockMethod))
    location = Column(LatLongColumnType)
    items = relationship("QuestItem", back_populates="quest")
    quest_participations = relationship("QuestParticipation", back_populates="quest")
    this_depends_on = relationship(
        "QuestDependency",
        foreign_keys="QuestDependency.quest_to_finish_after_id",
        back_populates="quest_to_finish_after",
    )
    depend_on_this = relationship(
        "QuestDependency",
        foreign_keys="QuestDependency.quest_to_finish_before_id",
        back_populates="quest_to_finish_before",
    )
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    event = relationship("Event", back_populates="quests")

    def __repr__(self):
        return "<Quest(title='%s')>" % self.title


class QuestDependency(Base):
    __tablename__ = "questDependencies"

    quest_to_finish_before_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quests.id"),
        primary_key=True,
        index=True,
    )
    quest_to_finish_after_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quests.id"),
        primary_key=True,
        index=True,
    )
    quest_to_finish_before = relationship(
        "Quest",
        foreign_keys=[quest_to_finish_before_id],
        back_populates="depend_on_this",
    )
    quest_to_finish_after = relationship(
        "Quest",
        foreign_keys=[quest_to_finish_after_id],
        back_populates="this_depends_on",
    )


class QuestItem(Base):
    __tablename__ = "questItems"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"))
    quest = relationship("Quest", back_populates="items")
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="instances")
    location = Column(LatLongColumnType)
    unlock_method = Column(SQLEnum(UnlockMethod))
    ownerships = relationship("ItemOwnership", back_populates="quest_item")

    def __repr__(self):
        return "<QuestItem(item.title='%s', quest.title='%s')>" % (
            self.item.title,
            self.quest.title,
        )


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    items = relationship("ItemOwnership", back_populates="owner")
    location: LatLongColumnType = Column(LatLongColumnType, nullable=True)
    quest_participations = relationship("QuestParticipation", back_populates="user")
    event_participations = relationship("EventParticipation", back_populates="user")


class ItemOwnership(Base):
    __tablename__ = "itemOwnerships"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    obtained_at = Column(DateTime, default=datetime.now)
    quest_item_id = Column(UUID(as_uuid=True), ForeignKey("questItems.id"))
    quest_item = relationship("QuestItem", back_populates="ownerships")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")


class QuestParticipation(Base):
    __tablename__ = "questParticipations"

    user_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
    )
    user: User = relationship("User", back_populates="quest_participations")
    quest_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("quests.id"),
        primary_key=True,
        index=True,
    )
    quest: Quest = relationship(
        "Quest", back_populates="quest_participations", lazy="joined"
    )
    status: QuestStatus = Column(SQLEnum(QuestStatus))


class Event(Base):
    __tablename__ = "events"

    id: UUID = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    active_from: datetime = Column(DateTime, default=datetime.now)
    active_to: datetime = Column(DateTime, nullable=True)
    quests: List[Quest] = relationship("Quest", back_populates="event")
    event_participations: List[EventParticipation] = relationship(
        "EventParticipation", back_populates="event"
    )


class EventParticipation(Base):
    __tablename__ = "eventParticipation"

    user_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
    )
    user: User = relationship("User", back_populates="event_participations")
    event_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id"),
        primary_key=True,
        index=True,
    )
    event: Event = relationship("Event", back_populates="event_participations")
    status: int = Column(Integer)
