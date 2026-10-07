# serializers/comment.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import UserPublicSchema
from .like import LikeSchema

class CommentSchema(BaseModel):
  id: int
  content: str
  image: Optional[str] = None
  event_id: int
  created_at: datetime
  # the user who wrote the comment
  user: UserPublicSchema
  likes: List[LikeSchema] = []

  class Config:
    orm_mode = True

class CreateCommentSchema(BaseModel):
  content: str
  image: Optional[str] = None

class UpdateCommentSchema(BaseModel):
  content: str
  image: Optional[str] = None