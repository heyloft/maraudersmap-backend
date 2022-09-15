from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from maraudersmap import crud, models, schemas
from maraudersmap.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/pois/", response_model=schemas.POI)
def create_poi(poi: schemas.POICreate, db: Session = Depends(get_db)):
    return crud.create_poi(db=db, poi=poi)


@app.get("/pois/", response_model=list[schemas.POI])
def read_pois(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pois = crud.get_pois(db, skip=skip, limit=limit)
    return pois
