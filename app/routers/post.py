from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, views, models
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter()


@router.post("/posts/", response_model=schemas.Post, tags=["Post"])
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    return views.post.create_post(db=db, post=post, user_id=current_user.id)


@router.get("/posts/", response_model=List[schemas.Post], tags=["Post"])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return views.post.get_posts(db=db, skip=skip, limit=limit)


@router.get("/post/{post_id}/", response_model=schemas.Post, tags=["Post"])
def get_post(post_id: int, db: Session = Depends(get_db)):
    if views.post.get_post(db=db, post_id=post_id):
        return views.post.get_post(db=db, post_id=post_id)
    raise HTTPException(status_code=404, detail="Post not found")


@router.put("/post/{post_id}/", response_model=schemas.Post, tags=["Post"])
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    if views.post.get_post(db=db, post_id=post_id):
        return views.post.update_post(db=db, post_id=post_id, post_update=post_update, user_id=current_user.id)
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/post/{post_id}/", response_model=schemas.Post, tags=["Post"])
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    if views.post.get_post(db=db, post_id=post_id):
        return views.post.delete_post(db=db, post_id=post_id, user_id=current_user.id)
    raise HTTPException(status_code=404, detail="Post not found")
