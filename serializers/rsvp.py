# serializers/rsvp.py

from pydantic import BaseModel
from .user import UserPublicSchema

class RsvpSchema(BaseModel):
  id: int
  status: str
  event_id: int
  # the user who rsvp'd
  user: UserPublicSchema

  class Config:
    orm_mode = True

class CreateRsvpSchema(BaseModel):
  # "going" or "maybe"
  status: str = "going"

class UpdateRsvpSchema(BaseModel):
  status: str