from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


def create_comment(db: Session, comment: CommentCreate, user_id: int):
    post = db.query(Post).filter(cast("ColumnElement[bool]", Post.id == comment.post_id)).first()
    db_comment = Comment(**comment.dict(exclude={"post_id"}), owner_id=user_id)
    db_comment.post = post
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).filter(cast("ColumnElement[bool]", Comment.is_deleted == False)).offset(skip).limit(limit)


def get_comment(comment_id: int, db: Session):
    return db.query(Comment).filter(cast("ColumnElement[bool]", Comment.is_deleted == False),
                                    cast("ColumnElement[bool]", Comment.id == comment_id)).first()


def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: Session):
    comment = db.query(Comment).filter(cast("ColumnElement[bool]", Comment.is_deleted == False),
                                       cast("ColumnElement[bool]", Comment.id == comment_id))

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.update(values=comment_update.dict(exclude={"post_id"}))
    comment = comment.first()

    if comment_update.post_id is not None:
        post = db.query(Post).filter(cast("ColumnElement[bool]", Post.id == comment_update.post_id)).first()
        if post:
            comment.post = post
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(comment_id: int, db: Session):
    comment = db.query(Comment).filter(cast("ColumnElement[bool]", Comment.id == comment_id)).first()
    comment.is_deleted = True
    db.commit()
    db.refresh(comment)

    return comment
