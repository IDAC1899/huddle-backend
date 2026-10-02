# serializers/event.py

from pydantic import BaseModel
from typing import List
from datetime import datetime
from .user import UserPublicSchema
from .rsvp import RsvpSchema
from .comment import CommentSchema

class EventSchema(BaseModel):
  id: int
  title: str
  description: str
  area: str
  starts_at: datetime
  capacity: int
  # the user hosting the event
  user: UserPublicSchema
  rsvps: List[RsvpSchema] = []
  comments: List[CommentSchema] = []

  class Config:
    orm_mode = True

class CreateEventSchema(BaseModel):
  title: str
  description: str
  area: str
  starts_at: datetime
  capacity: int

class UpdateEventSchema(BaseModel):
  title: str
  description: str
  area: str
  starts_at: datetime
  capacity: int

# events the signed in user is hosting and going to
class MyEventsSchema(BaseModel):
  hosting: List[EventSchema]
  attending: List[EventSchema]