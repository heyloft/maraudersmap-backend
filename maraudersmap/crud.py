from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_active_quests(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(models.QuestParticipation)
        .where(
            models.QuestParticipation.user_id == user_id
            and models.QuestParticipation.status == 1
        )
        .all()
    )


def get_item_ownerships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemOwnership).offset(skip).limit(limit).all()


def get_item_ownership(db: Session, item_ownership_id: UUID):
    return db.query(models.ItemOwnership).get(item_ownership_id)


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_item_ownership(db: Session, item_ownership: schemas.ItemOwnershipCreate):
    db_item_ownership = models.ItemOwnership(**item_ownership.dict())
    db.add(db_item_ownership)
    db.commit()
    db.refresh(db_item_ownership)
    return db_item_ownership


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_quest(db: Session, quest: schemas.QuestCreate):
    db_quest = models.Quest(**quest.dict())
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


def create_quest_dependency(
    db: Session, quest_dependency: schemas.QuestDependencyCreate
):
    db_quest_dep = models.QuestDependency(**quest_dependency.dict())
    db.add(db_quest_dep)
    db.commit()
    db.refresh(db_quest_dep)
    return db_quest_dep
