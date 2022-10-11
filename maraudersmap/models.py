import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from maraudersmap.database.base_class import Base
from maraudersmap.extra_types import LatLongColumnType


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), 
    primary_key=True,
    index=True, 
    default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    collectible = Column(Boolean)
    location = Column(LatLongColumnType)
    quest_items = relationship("QuestItem", back_populates="item")

    def __repr__(self):
        return "<Item(title='%s')>" % self.title


class Quest(Base):
    __tablename__ = "quests"

    id = Column(UUID(as_uuid=True), 
    primary_key=True, 
    index=True, 
    default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    active_from = Column(DateTime, default=datetime.now)
    active_to = Column(DateTime, nullable=True)
    unlock_method = Column(Integer)
    quest_items = relationship("QuestItem", back_populates="quest")
    this_depends_on = relationship(
        "QuestDependency", back_populates="quest_to_finish_after"
    )
    depends_on_this = relationship(
        "QuestDependency", back_populates="quest_to_finish_before"
    )

    def __repr__(self):
        return "<Quest(title='%s')>" % self.title


class QuestDependency(Base):
    __tablename__ = "questDependencies"

    quest_to_finish_before_id = Column(
        ForeignKey("quests.id"),
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    quest_to_finish_after_id = Column(
        ForeignKey("quests.id"),
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    quest_to_finish_before = relationship("Quest", back_populates="depends_on_this")
    quest_to_finish_after = relationship("Quest", back_populates="this_depends_on")


class QuestItem(Base):
    __tablename__ = "questItems"

    id = Column(UUID(as_uuid=True), 
    primary_key=True, 
    index=True, 
    default=uuid.uuid4)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"))
    quest = relationship("Quest", back_populates="quest_items")
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="quest_items")

    def __repr__(self):
        return "<QuestItem(item.title='%s', quest.title='%s')>" % (
            self.item.title,
            self.quest.title,
        )
