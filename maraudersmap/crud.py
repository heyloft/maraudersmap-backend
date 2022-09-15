from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_pois(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.POI).offset(skip).limit(limit).all()


def create_poi(db: Session, poi: schemas.POICreate):
    db_poi = models.POI(**poi.dict())
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi
