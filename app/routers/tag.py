from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, views, models
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter()


@router.post("/tags/", response_model=schemas.Tag, tags=["Tag"])
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    return views.tag.create_tag(db=db, tag=tag)


@router.get("/tags/", response_model=List[schemas.Tag], tags=["Tag"])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return views.tag.get_tags(db=db, skip=skip, limit=limit)


@router.get("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    if views.tag.get_tag(db=db, tag_id=tag_id):
        return views.tag.get_tag(db=db, tag_id=tag_id)
    raise HTTPException(status_code=404, detail="Tag not found")


@router.patch("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    if views.tag.get_tag(db=db, tag_id=tag_id):
        return views.tag.update_tag(db=db, tag_id=tag_id, tag_update=tag_update)
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
def delete_tag(tag_id: int, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    if views.tag.get_tag(db=db, tag_id=tag_id):
        return views.tag.delete_tag(db=db, tag_id=tag_id)
    raise HTTPException(status_code=404, detail="Tag not found")
