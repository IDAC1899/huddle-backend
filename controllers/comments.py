# controllers/comments.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List

# models
from models.event import EventModel
from models.comment import CommentModel
from models.user import UserModel

# serializers
from serializers.comment import CommentSchema, CreateCommentSchema, UpdateCommentSchema

# db
from sqlalchemy.orm import Session
from database import get_db

# auth
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/events/{event_id}/comments", response_model=List[CommentSchema])
def get_comments_for_event(event_id: int, db: Session = Depends(get_db)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_in_database.comments

@router.get("/comments/{comment_id}", response_model=CommentSchema)
def get_single_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_in_database = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment_in_database:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment_in_database

# any logged in user can comment on an event
@router.post("/events/{event_id}/comments", response_model=CommentSchema, status_code=201)
def create_comment(event_id: int, comment: CreateCommentSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    event_in_database = db.query(EventModel).filter(EventModel.id == event_id).first()

    if not event_in_database:
        raise HTTPException(status_code=404, detail="Event not found")

    # the logged in user becomes the comment's owner
    new_comment = CommentModel(**comment.dict(), event_id=event_id, user_id=current_user.id)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# only the comment's owner can edit it
@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment: UpdateCommentSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    comment_in_database = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment_in_database:
        raise HTTPException(status_code=404, detail="Comment not found")

    # check if the current user wrote the comment
    if comment_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    comment_in_database.content = comment.content
    comment_in_database.image = comment.image

    db.commit()
    db.refresh(comment_in_database)

    return comment_in_database

# only the comment's owner can delete it
@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    comment_in_database = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment_in_database:
        raise HTTPException(status_code=404, detail="Comment not found")

    # check if the current user wrote the comment
    if comment_in_database.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(comment_in_database)
    db.commit()

    return None