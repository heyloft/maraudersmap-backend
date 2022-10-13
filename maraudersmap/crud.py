from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_ownerships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemOwnership).offset(skip).limit(limit).all()


def get_item_ownership(db: Session, itemOwnershipId: UUID):
    return db.query(models.ItemOwnership).get(itemOwnershipId)


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
