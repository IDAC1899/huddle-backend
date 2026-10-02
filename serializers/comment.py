# serializers/comment.py

from pydantic import BaseModel
from datetime import datetime
from .user import UserPublicSchema

class CommentSchema(BaseModel):
  id: int
  content: str
  event_id: int
  created_at: datetime
  # the user who wrote the comment
  user: UserPublicSchema

  class Config:
    orm_mode = True

class CreateCommentSchema(BaseModel):
  content: str

class UpdateCommentSchema(BaseModel):
  content: str