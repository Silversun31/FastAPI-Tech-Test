from typing import cast, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from starlette import status

from app import schemas
from app.models.tag import Tag
from app.models.post import Post
from app.schemas.post import PostCreate


def create_post(db: Session, post: PostCreate, user_id: int):
    tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
    db_post = Post(**post.dict(exclude={"tag_ids"}), owner_id=user_id)
    db_post.tags = tags
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).filter(cast("ColumnElement[bool]", Post.is_deleted == False)).offset(skip).limit(limit)


def get_post(post_id: int, db: Session):
    return db.query(Post).filter(cast("ColumnElement[bool]", Post.is_deleted == False),
                                 cast("ColumnElement[bool]", Post.id == post_id)).first()


def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session, user_id: int):
    post = db.query(Post).filter(cast("ColumnElement[bool]", Post.is_deleted == False),
                                 cast("ColumnElement[bool]", Post.id == post_id))
    # Comprobar si el que hace la peticion es el creador del post
    if post.first().owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not post's owner")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.update(values=post_update.dict(exclude={"tag_ids"}))
    post = post.first()

    if post_update.tag_ids is not None:
        post.tags.clear()
        new_tags = db.query(Tag).filter(Tag.id.in_(post_update.tag_ids)).all()
        post.tags.extend(new_tags)
    db.commit()
    db.refresh(post)

    return post


def delete_post(post_id: int, db: Session, user_id: int):
    post = db.query(Post).filter(cast("ColumnElement[bool]", Post.id == post_id)).first()

    # Comprobar si el que hace la peticion es el creador del post
    if post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not post's owner")

    post.is_deleted = True
    db.commit()
    db.refresh(post)

    return post
