# serializers/like.py

from pydantic import BaseModel

class LikeSchema(BaseModel):
  id: int
  user_id: int
  comment_id: int

  class Config:
    orm_mode = True