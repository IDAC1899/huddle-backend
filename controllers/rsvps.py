# controllers/rsvps.py

from fastapi import APIRouter, Depends, HTTPException

# models
from models.event import EventModel
from models.rsvp import RsvpModel
from models.user import UserModel

# serializers
from serializers.rsvp import RsvpSchema, CreateRsvpSchema, UpdateRsvpSchema

# db
from sqlalchemy.orm import Session
from database import get_db

# auth
from dependencies.get_current_user import get_current_user

router = APIRouter()

# the only statuses an rsvp can have
VALID_STATUSES = ["going", "maybe"]

# any logged in user can rsvp once to an event that isn't full
@router.post("/events/{event_id}/rsvps", response_model=RsvpSchema, status_code=201)
def create_rsvp(event_id: int, rsvp: CreateRsvpSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    if rsvp.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Status must be going or maybe")

    # check if the user already rsvp'd to this event
    rsvp_in_database = db.query(RsvpModel).filter(RsvpModel.event_id == event_id, RsvpModel.user_id == current_user.id).first()

    if rsvp_in_database:
        raise HTTPException(status_code=409, detail="You have already RSVP'd to this event")

    # count the people already going
    going_count = len([existing_rsvp for existing_rsvp in event_in_database.rsvps if existing_rsvp.status == "going"])

    if rsvp.status == "going" and going_count >= event_in_database.capacity:
        raise HTTPException(status_code=400, detail="This event is full")

    new_rsvp = RsvpModel(**rsvp.dict(), event_id=event_id, user_id=current_user.id)

    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)

    return new_rsvp

# only the rsvp's owner can change between going and maybe
@router.put("/rsvps/{rsvp_id}", response_model=RsvpSchema)
def update_rsvp(rsvp_id: int, rsvp: UpdateRsvpSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    rsvp_in_database = db.query(RsvpModel).filter(RsvpModel.id == rsvp_id).first()

    if not rsvp_in_database:
        raise HTTPException(status_code=404, detail="RSVP not found")

    # check if the current user made the rsvp
    if rsvp_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    if rsvp.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Status must be going or maybe")

    # switching from maybe to going takes a spot, so check the event isn't full
    if rsvp.status == "going" and rsvp_in_database.status != "going":
        event_in_database = rsvp_in_database.event
        going_count = len([existing_rsvp for existing_rsvp in event_in_database.rsvps if existing_rsvp.status == "going"])

        if going_count >= event_in_database.capacity:
            raise HTTPException(status_code=400, detail="This event is full")

    rsvp_in_database.status = rsvp.status

    db.commit()
    db.refresh(rsvp_in_database)

    return rsvp_in_database

# only the rsvp's owner can cancel it
@router.delete("/rsvps/{rsvp_id}", status_code=204)
def delete_rsvp(rsvp_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    rsvp_in_database = db.query(RsvpModel).filter(RsvpModel.id == rsvp_id).first()

    if not rsvp_in_database:
        raise HTTPException(status_code=404, detail="RSVP not found")

    # check if the current user made the rsvp
    if rsvp_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(rsvp_in_database)
    db.commit()

    return None