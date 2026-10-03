# controllers/events.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List

# models
from models.event import EventModel
from models.user import UserModel

# serializers
from serializers.event import EventSchema, CreateEventSchema, UpdateEventSchema, MyEventsSchema

# db
from sqlalchemy.orm import Session
from database import get_db

# auth
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/events", response_model=List[EventSchema])
def get_events(db: Session = Depends(get_db)):
    # soonest events first
    events = db.query(EventModel).order_by(EventModel.starts_at).all()

    return events

@router.get("/events/{event_id}", response_model=EventSchema)
def get_single_event(event_id: int, db: Session = Depends(get_db)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_in_database

# any logged in user can host an event
@router.post("/events", response_model=EventSchema, status_code=201)
def create_event(event: CreateEventSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # the logged in user becomes the host
    new_event = EventModel(**event.dict(), user_id=current_user.id)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

# only the host can update their event
@router.put("/events/{event_id}", response_model=EventSchema)
def update_event(event_id: int, event: UpdateEventSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    # check if the current user is the host
    if event_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    event_data = event.dict(exclude_unset=True)

    # replace each field with the new value
    for key, value in event_data.items():
        setattr(event_in_database, key, value)

    db.commit()
    db.refresh(event_in_database)

    return event_in_database

# only the host can delete their event
@router.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    # check if the current user is the host
    if event_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(event_in_database)
    db.commit()

    return None

# events the logged in user is hosting and has rsvp'd to
@router.get("/my-events", response_model=MyEventsSchema)
def get_my_events(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    hosting = db.query(EventModel).filter(EventModel.user_id == current_user.id).order_by(EventModel.starts_at).all()

    # each rsvp points to the event it belongs to
    attending = [rsvp.event for rsvp in current_user.rsvps]

    return {"hosting": hosting, "attending": attending}