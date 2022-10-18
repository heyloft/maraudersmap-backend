from uuid import UUID

from sqlalchemy.orm import Session, joinedload, lazyload

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_active_quests(
    db: Session, event_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.QuestParticipation)
        # .join(models.QuestParticipation.quest)
        # .options(lazyload(models.QuestParticipation.quest))
        .where(
            models.QuestParticipation.quest.event_id
            == event_id
            # and models.QuestParticipation.user_id == user_id
            # and models.QuestParticipation.status == 1
        ).all()
    )


def get_unstarted_quests(
    db: Session, event_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.QuestParticipation)
        .where(
            models.QuestParticipation.quest.event_id == event_id
            and models.QuestParticipation.user_id == user_id
            and models.QuestParticipation.status == 2
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


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def create_item_ownership(db: Session, item_ownership: schemas.ItemOwnershipCreate):
    db_item_ownership = models.ItemOwnership(**item_ownership.dict())
    db.add(db_item_ownership)
    db.commit()
    db.refresh(db_item_ownership)
    return db_item_ownership


def create_quest_participation(
    db: Session, quest_participation: schemas.QuestParticipationCreate
):
    db_quest_participation = models.QuestParticipation(**quest_participation.dict())
    db.add(db_quest_participation)
    db.commit()
    db.refresh(db_quest_participation)
    return db_quest_participation


def create_user(db: Session, user: schemas.UserCreate):
    user_check = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if user_check is not None:
        return None
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


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
