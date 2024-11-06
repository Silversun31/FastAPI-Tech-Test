from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, views, models
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter()


@router.post("/tags/", response_model=schemas.Tag, tags=["Tag"])
async def create_tag(tag: schemas.TagCreate, db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    return await views.tag.create_tag(db=db, tag=tag)


@router.get("/tags/", response_model=List[schemas.Tag], tags=["Tag"])
async def read_tags(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await views.tag.get_tags(db=db, skip=skip, limit=limit)


@router.get("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    return await views.tag.get_tag(db=db, tag_id=tag_id)


@router.put("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
async def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    return await views.tag.update_tag(db=db, tag_id=tag_id, tag_update=tag_update)


@router.delete("/tag/{tag_id}/", response_model=schemas.Tag, tags=["Tag"])
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    return await views.tag.delete_tag(db=db, tag_id=tag_id)
