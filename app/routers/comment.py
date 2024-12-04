from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, views, models
from app.core.security import get_current_user
from app.database import get_db
from app.exceptions import COMMENT_NOT_FOUND_EXCEPTION

router = APIRouter()


@router.post("/comments/", response_model=schemas.Comment, tags=["Comment"])
async def create_comment(comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    return await views.comment.create_comment(db=db, comment=comment, user_id=current_user.id)


@router.get("/comments/", response_model=List[schemas.Comment], tags=["Comment"])
async def read_comments(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await views.comment.get_comments(db=db, skip=skip, limit=limit)


@router.get("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    return await views.comment.get_comment(db=db, comment_id=comment_id)


@router.put("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
async def update_comment(comment_id: int, comment_update: schemas.CommentUpdate,
                         db: AsyncSession = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    return await views.comment.update_comment(db=db, comment_id=comment_id, comment_update=comment_update)


@router.delete("/comment/{comment_id}/", response_model=schemas.Comment, tags=["Comment"])
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    return await views.comment.delete_comment(db=db, comment_id=comment_id)
