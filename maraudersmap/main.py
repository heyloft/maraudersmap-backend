from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from maraudersmap import ascii, crud, models, schemas
from maraudersmap.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=PlainTextResponse)
def index():
    return ascii.SNAIL


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/itemOwnerships/", response_model=list[schemas.ItemOwnership])
def read_item_ownerships(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    item_ownerships = crud.get_item_ownerships(db, skip=skip, limit=limit)
    return item_ownerships


@app.get("/itemOwnerships/{itemOwnershipId}", response_model=schemas.ItemOwnership)
def read_item_ownership(itemOwnershipId: UUID, db: Session = Depends(get_db)):
    item_ownership = crud.get_item_ownership(db, itemOwnershipId=itemOwnershipId)
    return item_ownership


@app.post("/itemOwnership/", response_model=schemas.ItemOwnership)
def create_item_ownership(
    item_ownership: schemas.ItemOwnershipCreate, db: Session = Depends(get_db)
):
    return crud.create_item_ownership(db=db, item_ownership=item_ownership)


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
