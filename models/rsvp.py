# models/rsvp.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel

class RsvpModel(BaseModel):

    __tablename__ = "rsvps"

    # a user can only rsvp to each event once
    __table_args__ = (UniqueConstraint("user_id", "event_id"),)

    id = Column(Integer, primary_key=True, index=True)
    # "going" or "maybe"
    status = Column(String, nullable=False, default="going")

    # the user who rsvp'd
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="rsvps")

    # the event they rsvp'd to
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    event = relationship("EventModel", back_populates="rsvps")