# models/like.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel

class LikeModel(BaseModel):

    __tablename__ = "likes"

    # a user can only like each comment once
    __table_args__ = (UniqueConstraint("user_id", "comment_id"),)

    id = Column(Integer, primary_key=True, index=True)

    # the user who liked the comment
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel")

    # the comment that was liked
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    comment = relationship("CommentModel", back_populates="likes")