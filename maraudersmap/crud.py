from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_active_quests(
    db: Session, event_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100
):
    return get_quests_by_status(
        db, event_id, user_id, models.QuestStatus.ACTIVE, skip, limit
    )


def get_unstarted_quests(
    db: Session, event_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100
):
    return get_quests_by_status(
        db, event_id, user_id, models.QuestStatus.UNSTARTED, skip, limit
    )


def get_quests_by_status(
    db: Session,
    user_id: UUID,
    event_id: UUID = None,
    status: models.QuestStatus = None,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(models.QuestParticipation)
        .where(
            models.QuestParticipation.user_id == user_id,
            event_id is None or models.QuestParticipation.quest.has(event_id=event_id),
            status is None or models.QuestParticipation.status == status,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_quest_items(
    db: Session, quest_id: UUID, skip: int = 0, limit: int = 100
) -> list[models.QuestItem]:
    return (
        db.query(models.QuestItem)
        .filter_by(quest_id=quest_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_quest_item(
    db: Session, quest_id: UUID, quest_item: schemas.QuestItemCreate
) -> models.QuestItem:
    db_quest_item = models.QuestItem(quest_id=quest_id, **quest_item.dict())
    db.add(db_quest_item)
    db.commit()
    db.refresh(db_quest_item)
    return db_quest_item


def get_user_item_ownerships(
    db: Session, user_id: UUID, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.ItemOwnership)
        .filter_by(owner_id=user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


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


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_item_ownership(
    db: Session, user_id: UUID, item_ownership: schemas.ItemOwnershipCreate
):
    db_item_ownership = models.ItemOwnership(owner_id=user_id, **item_ownership.dict())
    db.add(db_item_ownership)
    db.commit()
    db.refresh(db_item_ownership)
    return db_item_ownership


def create_quest_participation(
    db: Session, user_id: UUID, quest_participation: schemas.QuestParticipationCreate
):
    db_quest_participation = models.QuestParticipation(
        user_id=user_id, **quest_participation.dict()
    )
    db.add(db_quest_participation)
    db.commit()
    db.refresh(db_quest_participation)
    return db_quest_participation


def update_quest_participation(
    db: Session,
    user_id: UUID,
    quest_id: UUID,
    quest_participation: schemas.QuestParticipationUpdate,
):
    db_quest_participation_query = db.query(models.QuestParticipation).filter(
        models.QuestParticipation.user_id == user_id,
        models.QuestParticipation.quest_id == quest_id,
    )
    if db_quest_participation_query.count() > 1:
        raise Exception(
            "Multiple QuestParticipation instances for the given primary key!"
        )
    db_quest_participation_query.update(quest_participation.dict())
    db.commit()
    return db_quest_participation_query.one()


def sync_quest_participation_progress(db: Session, user_id: UUID, quest_id: UUID):
    db_participation = db.query(models.QuestParticipation).get(
        {"user_id": user_id, "quest_id": quest_id}
    )
    if db_participation.status != models.QuestStatus.ACTIVE:
        # Not in progress, nothing will change at this point
        print("Quest not active, ignoring progress sync request.")
        return db_participation
    db_quest_keys_count = (
        db.query(models.QuestItem)
        .filter(
            models.QuestItem.quest_id == quest_id,
            models.QuestItem.item.has(item_type=models.ItemType.KEY),
        )
        .count()
    )
    if db_quest_keys_count <= 0:
        # Edge case: quest does not have any keys.
        # Currently not letting these quests be finished.
        print("Quest does not have any keys, ignoring progress sync request.")
        return db_participation
    db_user_keys_count = (
        db.query(models.ItemOwnership)
        .join(models.QuestItem)
        .join(models.Item)
        .filter(
            models.ItemOwnership.owner_id == user_id,
            # models.ItemOwnership.quest_item.item.has(item_type=models.ItemType.KEY),
            models.Item.item_type == models.ItemType.KEY,
        )
        .count()
    )
    if db_user_keys_count < db_quest_keys_count:
        # Not finished, no status change required
        return db_participation
    db_participation.status = models.QuestStatus.FINISHED

    db.add(db_participation)
    db.add_all(
        build_quest_completion_item_ownerships(
            db=db, user_id=user_id, quest_id=quest_id
        )
    )
    db.commit()
    db.refresh(db_participation)
    db.commit()
    # Deletes all ItemOwnerships related to user and quest.
    # Currently throws error, but is a start. Also lacks the check for voucher for now
    # db.query(models.ItemOwnership).filter(
    #     models.ItemOwnership.quest_item.has(quest_id=quest_id)).delete(synchronize_session='fetch')
    # db.commit()
    return db_participation


def build_quest_completion_item_ownerships(db: Session, user_id: UUID, quest_id: UUID):
    db_quest_completion_items: list[models.QuestItem] = (
        db.query(models.QuestItem)
        .filter_by(
            quest_id=quest_id, unlock_method=models.UnlockMethod.QUEST_COMPLETION
        )
        .all()
    )
    return [
        models.ItemOwnership(owner_id=user_id, quest_item_id=item.id)
        for item in db_quest_completion_items
    ]


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


def get_user(db: Session, user_id: UUID):
    return db.query(models.User).get(user_id)


def get_user_by_username(db: Session, user_username: str):
    return db.query(models.User).filter_by(username=user_username).one_or_none()


def get_quest(db: Session, quest_id: UUID):
    return db.query(models.Quest).get(quest_id)


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


def get_event_participation(db: Session, user_id: UUID, event_id: UUID):
    return db.query(models.EventParticipation).get(
        {"user_id": user_id, "event_id": event_id}
    )


def create_event_participation(
    db: Session, user_id: UUID, event_participation: schemas.EventParticipationCreate
):
    db_event_participation = models.EventParticipation(
        user_id=user_id, **event_participation.dict()
    )
    db.add(db_event_participation)
    db_quests = db.query(models.Event).get(event_participation.event_id).quests
    for quest in db_quests:
        quest_participation = models.QuestParticipation(
            status=models.QuestStatus.UNSTARTED,
            quest_id=quest.id,
            user_id=user_id,
        )
        db.add(quest_participation)

    db.commit()
    db.refresh(db_event_participation)
    return db_event_participation


def update_event_participation(
    db: Session,
    user_id: UUID,
    event_id: UUID,
    event_participation: schemas.EventParticipation,
):
    db_event_participation_query = db.query(models.EventParticipation).filter(
        models.EventParticipation.user_id == user_id,
        models.EventParticipation.event_id == event_id,
    )
    if db_event_participation_query.count() > 1:
        raise Exception(
            "Multiple EventParticipation instances for the given primary key!"
        )
    db_event_participation_query.update(event_participation.dict())
    db.commit()
    return db_event_participation_query.one()
