from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/activeQuests/{user_id}", response_model=list[schemas.QuestParticipation])
def read_active_quests(
    user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    active_quests = crud.get_active_quests(db, user_id, skip=skip, limit=limit)
    return active_quests


@app.get("/itemOwnerships/", response_model=list[schemas.ItemOwnership])
def read_item_ownerships(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    item_ownerships = crud.get_item_ownerships(db, skip=skip, limit=limit)
    return item_ownerships


@app.get("/itemOwnerships/{item_ownership_id}", response_model=schemas.ItemOwnership)
def read_item_ownership(item_ownership_id: UUID, db: Session = Depends(get_db)):
    item_ownership = crud.get_item_ownership(db, item_ownership_id=item_ownership_id)
    return item_ownership


@app.post("/itemOwnership/", response_model=schemas.ItemOwnership)
def create_item_ownership(
    item_ownership: schemas.ItemOwnershipCreate, db: Session = Depends(get_db)
):
    return crud.create_item_ownership(db=db, item_ownership=item_ownership)


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.post("/quest/", response_model=schemas.Quest)
def create_quest(quest: schemas.QuestCreate, db: Session = Depends(get_db)):
    return crud.create_quest(db=db, quest=quest)


@app.post("/questdependency/", response_model=schemas.QuestDependencyBase)
def create_quest_dependency(
    quest_dependency: schemas.QuestDependencyCreate, db: Session = Depends(get_db)
):
    return crud.create_quest_dependency(db=db, quest_dependency=quest_dependency)
