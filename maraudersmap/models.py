
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from maraudersmap.database.base_class import Base
from maraudersmap.extra_types import LatLongColumnType


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    icon = Column(String)
    instances = relationship("QuestItem", back_populates="item")
    ownerships = relationship("ItemOwnership", back_populates="item")

    def __repr__(self):
        return "<Item(title='%s')>" % self.title


class Quest(Base):
    __tablename__ = "quests"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    active_from = Column(DateTime, default=datetime.now)
    active_to = Column(DateTime, nullable=True)
    unlock_method = Column(Integer)
    items = relationship("QuestItem", back_populates="quest")
    this_depends_on = relationship(
        "QuestDependency", back_populates="quest_to_finish_after"
    )
    depends_on_this = relationship(
        "QuestDependency", back_populates="quest_to_finish_before"
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
        default=uuid.uuid4,
    )
    quest_to_finish_after_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quests.id"),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    quest_to_finish_before = relationship("Quest", back_populates="depends_on_this")
    quest_to_finish_after = relationship("Quest", back_populates="this_depends_on")


class QuestItem(Base):
    __tablename__ = "questItems"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"))
    quest = relationship("Quest", back_populates="items")
    item_type = Column(Integer, default=False) # 0 = collectible, 1 = key, 2 = point of interest
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="instances")
    location = Column(LatLongColumnType)

    def __repr__(self):
        return "<QuestItem(item.title='%s', quest.title='%s')>" % (
            self.item.title,
            self.quest.title,
        )

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String)
    location = Column(LatLongColumnType)

class ItemOwnership(Base):
    __tablename__ = "itemOwnerships"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    obtained_at = Column(DateTime, default=datetime.now)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="ownerships")


class QuestParticipation(Base):
    __tablename__ = "questParticipations"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    quest_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quests.id"),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    status = Column(Integer)

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    active_from = Column(DateTime, default=datetime.now)
    active_to = Column(DateTime, nullable=True)
    quests = relationship("Quest", back_populates="events")

class EventParticipation(Base):
    __tablename__ = "eventParticipation"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    quest_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id"),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    status = Column(Integer)