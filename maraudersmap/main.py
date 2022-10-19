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


@app.get("/events/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.post("/questParticipations/", response_model=schemas.QuestParticipation)
def create_quest_participation(
    quest_participation: schemas.QuestParticipationCreate, db: Session = Depends(get_db)
):
    return crud.create_quest_participation(
        db=db, quest_participation=quest_participation
    )


@app.put(
    "/questParticipations/{user_id}/{quest_id}",
    response_model=schemas.QuestParticipation,
)
def update_quest_participation(
    user_id: UUID,
    quest_id: UUID,
    quest_participation: schemas.QuestParticipationUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_quest_participation(
        db=db,
        user_id=user_id,
        quest_id=quest_id,
        quest_participation=quest_participation,
    )


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get(
    "/events/{event_id}/user/{user_id}/activeQuests",
    response_model=list[schemas.QuestParticipation],
)
def read_active_quests(
    event_id: UUID,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    active_quests = crud.get_active_quests(
        db, event_id, user_id, skip=skip, limit=limit
    )
    return active_quests


@app.get(
    "/events/{event_id}/user/{user_id}/unstartedQuests",
    response_model=list[schemas.QuestParticipation],
)
def read_unstarted_quests(event_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    unstarted_quests = crud.get_unstarted_quests(db, event_id, user_id)
    return unstarted_quests


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


@app.post("/itemOwnerships/", response_model=schemas.ItemOwnership)
def create_item_ownership(
    item_ownership: schemas.ItemOwnershipCreate, db: Session = Depends(get_db)
):
    return crud.create_item_ownership(db=db, item_ownership=item_ownership)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    create_user = crud.create_user(db=db, user=user)
    if create_user is None:
        raise HTTPException(status_code=400, detail="Username is already in use")
    return create_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.get("/users/by_username/{username}", response_model=schemas.User)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, user_username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.get("/quests/{quest_id}/items", response_model=list[schemas.QuestItem])
def read_quest_items(
    quest_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_quest_items(db=db, quest_id=quest_id, skip=skip, limit=limit)


@app.post("/quests/{quest_id}/items/", response_model=schemas.QuestItem)
def create_quest_item(
    quest_id: UUID, quest_item: schemas.QuestItemCreate, db: Session = Depends(get_db)
):
    return crud.create_quest_item(db=db, quest_id=quest_id, quest_item=quest_item)


@app.post("/quests/", response_model=schemas.Quest)
def create_quest(quest: schemas.QuestCreate, db: Session = Depends(get_db)):
    return crud.create_quest(db=db, quest=quest)


@app.post("/questDependencies/", response_model=schemas.QuestDependencyBase)
def create_quest_dependency(
    quest_dependency: schemas.QuestDependencyCreate, db: Session = Depends(get_db)
):
    return crud.create_quest_dependency(db=db, quest_dependency=quest_dependency)


@app.post("/eventParticipations/", response_model=schemas.EventParticipationCreate)
def create_event_participation(
    event_participation: schemas.EventParticipationCreate, db: Session = Depends(get_db)
):
    return crud.create_event_participation(
        db=db, event_participation=event_participation
    )


@app.put(
    "/eventParticipations/{user_id}/{event_id}",
    response_model=schemas.EventParticipation,
)
def update_event_participation(
    user_id: UUID,
    event_id: UUID,
    event_participation: schemas.EventParticipationUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_event_participation(
        db=db,
        user_id=user_id,
        event_id=event_id,
        event_participation=event_participation,
    )
