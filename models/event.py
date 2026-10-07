# models/event.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class EventModel(BaseModel):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    area = Column(String, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    # optional header photo, saved as an image link or the image's data from the front end
    image = Column(Text, nullable=True)

    # the user who is hosting the event
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="events")

    # deleting an event also deletes its rsvps and comments
    rsvps = relationship("RsvpModel", back_populates="event", cascade="all, delete-orphan")
    comments = relationship("CommentModel", back_populates="event", cascade="all, delete-orphan")