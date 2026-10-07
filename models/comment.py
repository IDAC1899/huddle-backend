# models/comment.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class CommentModel(BaseModel):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    # optional photo, saved as an image link or the image's data from the front end
    image = Column(Text, nullable=True)

    # the user who wrote the comment
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="comments")

    # the event the comment is on
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    event = relationship("EventModel", back_populates="comments")

    # deleting a comment also deletes its likes
    likes = relationship("LikeModel", back_populates="comment", cascade="all, delete-orphan")