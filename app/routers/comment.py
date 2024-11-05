from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, views, models
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter()


@router.post("/comments/", response_model=schemas.Comment, tags=["Comment"])
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    return views.comment.create_comment(db=db, comment=comment, user_id=current_user.id)


@router.get("/comments/", response_model=List[schemas.Comment], tags=["Comment"])
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return views.comment.get_comments(db=db, skip=skip, limit=limit)


@router.get("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    if views.comment.get_comment(db=db, comment_id=comment_id):
        return views.comment.get_comment(db=db, comment_id=comment_id)
    raise HTTPException(status_code=404, detail="Comment not found")


@router.patch("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    if views.comment.get_comment(db=db, comment_id=comment_id):
        return views.comment.update_comment(db=db, comment_id=comment_id, comment_update=comment_update)
    raise HTTPException(status_code=404, detail="Comment not found")


@router.delete("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    if views.comment.get_comment(db=db, comment_id=comment_id):
        return views.comment.delete_comment(db=db, comment_id=comment_id)
    raise HTTPException(status_code=404, detail="Comment not found")
