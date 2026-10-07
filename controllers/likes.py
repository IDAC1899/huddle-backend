# controllers/likes.py

from fastapi import APIRouter, Depends, HTTPException

# models
from models.comment import CommentModel
from models.like import LikeModel
from models.user import UserModel

# serializers
from serializers.like import LikeSchema

# db
from sqlalchemy.orm import Session
from database import get_db

# auth
from dependencies.get_current_user import get_current_user

router = APIRouter()

# any logged in user can like someone else's comment once
@router.post("/comments/{comment_id}/likes", response_model=LikeSchema, status_code=201)
def create_like(comment_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    comment_in_database = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment_in_database:
        raise HTTPException(status_code=404, detail="Comment not found")

    # users can't like their own comments
    if comment_in_database.user_id == current_user.id:
        raise HTTPException(status_code=403, detail="You can't like your own comment")

    # check if the user already liked this comment
    like_in_database = db.query(LikeModel).filter(LikeModel.comment_id == comment_id, LikeModel.user_id == current_user.id).first()

    if like_in_database:
        raise HTTPException(status_code=409, detail="You have already liked this comment")

    new_like = LikeModel(comment_id=comment_id, user_id=current_user.id)

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like

# only the user who liked can take the like back
@router.delete("/likes/{like_id}", status_code=204)
def delete_like(like_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    like_in_database = db.query(LikeModel).filter(LikeModel.id == like_id).first()

    if not like_in_database:
        raise HTTPException(status_code=404, detail="Like not found")

    # check if the current user made the like
    if like_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(like_in_database)
    db.commit()

    return None