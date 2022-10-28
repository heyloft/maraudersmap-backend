from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from maraudersmap import ascii, crud, models, schemas
from maraudersmap.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


# This makes function names for generatad clients more readable,
# but also puts more trust in the endpoint author to define unique names!
def readable_route_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(
    title="Marauder’s Map API",
    generate_unique_id_function=readable_route_id,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=PlainTextResponse, tags=["index"])
def index():
    return ascii.SNAIL


@app.get("/events/", response_model=list[schemas.Event], tags=["events"])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_events(db, skip=skip, limit=limit)


@app.post("/events/", response_model=schemas.Event, tags=["events"])
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.post("/quests/", response_model=schemas.Quest, tags=["quests"])
def create_quest(quest: schemas.QuestCreate, db: Session = Depends(get_db)):
    return crud.create_quest(db=db, quest=quest)


@app.get(
    "/quests/{quest_id}/items", response_model=list[schemas.QuestItem], tags=["quests"]
)
def read_quest_items(
    quest_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    if crud.get_quest(db=db, quest_id=quest_id) is None:
        raise HTTPException(status_code=404, detail="Quest not found")
    return crud.get_quest_items(db=db, quest_id=quest_id, skip=skip, limit=limit)


@app.post(
    "/quests/{quest_id}/items/", response_model=schemas.QuestItem, tags=["quests"]
)
def create_quest_item(
    quest_id: UUID, quest_item: schemas.QuestItemCreate, db: Session = Depends(get_db)
):
    if crud.get_quest(db=db, quest_id=quest_id) is None:
        raise HTTPException(status_code=404, detail="Quest not found")
    return crud.create_quest_item(db=db, quest_id=quest_id, quest_item=quest_item)


@app.post(
    "/questDependencies/", response_model=schemas.QuestDependencyBase, tags=["quests"]
)
def create_quest_dependency(
    quest_dependency: schemas.QuestDependencyCreate, db: Session = Depends(get_db)
):
    return crud.create_quest_dependency(db=db, quest_dependency=quest_dependency)


@app.get("/items/", response_model=list[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)


@app.post("/items/", response_model=schemas.Item, tags=["items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    create_user = crud.create_user(db=db, user=user)
    if create_user is None:
        raise HTTPException(status_code=400, detail="Username is already in use")
    return create_user


@app.get("/users/by_username/{username}", response_model=schemas.User, tags=["users"])
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, user_username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.post(
    "/users/{user_id}/eventParticipations/",
    response_model=schemas.EventParticipation,
    tags=["events"],
)
def create_event_participation(
    user_id: UUID,
    event_participation: schemas.EventParticipationCreate,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_event_participation(
        db=db, user_id=user_id, event_participation=event_participation
    )


@app.get(
    "/users/{user_id}/eventParticipations/{event_id}/",
    response_model=schemas.EventParticipation,
    tags=["events"],
)
def read_event_participation(
    user_id: UUID, event_id: UUID, db: Session = Depends(get_db)
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    eventParticipation = crud.get_event_participation(
        db=db, user_id=user_id, event_id=event_id
    )
    if eventParticipation is None:
        raise HTTPException(status_code=404, detail="EventParticipation not found")
    return eventParticipation


@app.put(
    "/users/{user_id}/eventParticipations/{event_id}/",
    response_model=schemas.EventParticipation,
    tags=["events"],
)
def update_event_participation(
    user_id: UUID,
    event_id: UUID,
    event_participation: schemas.EventParticipationUpdate,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_event_participation(
        db=db,
        user_id=user_id,
        event_id=event_id,
        event_participation=event_participation,
    )


@app.get(
    "/users/{user_id}/questParticipations/",
    response_model=list[schemas.QuestParticipation],
    tags=["quests"],
)
def read_user_quest_participations(
    user_id: UUID,
    event_id: UUID = None,
    status: models.QuestStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_quests_by_status(
        db=db, user_id=user_id, event_id=event_id, status=status, skip=skip, limit=limit
    )


@app.post(
    "/users/{user_id}/questParticipations",
    response_model=schemas.QuestParticipation,
    tags=["quests"],
)
def create_quest_participation(
    user_id: UUID,
    quest_participation: schemas.QuestParticipationCreate,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_quest_participation(
        db=db, user_id=user_id, quest_participation=quest_participation
    )


@app.put(
    "/users/{user_id}/questParticipations/{quest_id}",
    response_model=schemas.QuestParticipation,
    tags=["quests"],
)
def update_quest_participation(
    user_id: UUID,
    quest_id: UUID,
    quest_participation: schemas.QuestParticipationUpdate,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_quest_participation(
        db=db,
        user_id=user_id,
        quest_id=quest_id,
        quest_participation=quest_participation,
    )


@app.get(
    "/users/{user_id}/itemOwnerships/",
    response_model=list[schemas.ItemOwnership],
    tags=["items"],
)
def read_item_ownerships(
    user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_item_ownerships(db=db, user_id=user_id, skip=skip, limit=limit)


@app.post(
    "/users/{user_id}/itemOwnerships/",
    response_model=schemas.ItemOwnership,
    tags=["items"],
)
def create_item_ownership(
    user_id: UUID,
    item_ownership: schemas.ItemOwnershipCreate,
    db: Session = Depends(get_db),
):
    if crud.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    create_ownership_res = crud.create_item_ownership(
        db=db, user_id=user_id, item_ownership=item_ownership
    )
    # TODO: Make ItemOwnership between User and QuestItem (not just Item),
    # so that quest_id is more accessible
    quest_id = (
        db.query(models.QuestItem)
        .filter_by(id=item_ownership.quest_item_id)
        .one()
        .quest_id
    )
    crud.sync_quest_participation_progress(db=db, user_id=user_id, quest_id=quest_id)
    return create_ownership_res
