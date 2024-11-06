from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.exceptions.exceptions import POST_NOT_FOUND_EXCEPTION, NOT_POST_OWNER_EXCEPTION
from app.models.tag import Tag
from app.models.post import Post
from app.schemas.post import PostCreate


async def create_post(db: AsyncSession, post: PostCreate, user_id: int):
    result = await db.execute(select(Tag).filter(Tag.id.in_(post.tag_ids)))
    tags = result.scalars().all()
    db_post = Post(**post.dict(exclude={"tag_ids"}), owner_id=user_id)
    db_post.tags = tags
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Post).filter(Post.is_deleted == False).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_post(post_id: int, db: AsyncSession):
    result = await db.execute(
        select(Post).filter(
            cast("ColumnElement[bool]", Post.is_deleted == False),
            cast("ColumnElement[bool]", Post.id == post_id)
        )
    )
    if not result:
        raise POST_NOT_FOUND_EXCEPTION
    return result.scalar_one_or_none()


async def update_post(post_id: int, post_update: schemas.PostUpdate, db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Post).filter(
            cast("ColumnElement[bool]", Post.is_deleted == False),
            cast("ColumnElement[bool]", Post.id == post_id)
        )
    )
    post = result.scalar_one_or_none()

    if not post:
        raise POST_NOT_FOUND_EXCEPTION

    # Comprobar si el que hace la petición es el creador del post
    if post.owner_id != user_id:
        raise NOT_POST_OWNER_EXCEPTION

    # Actualizar los valores
    for key, value in post_update.dict(exclude={"tag_ids"}).items():
        setattr(post, key, value)

    if post_update.tag_ids is not None:
        post.tags.clear()
        result = await db.execute(select(Tag).filter(Tag.id.in_(post_update.tag_ids)))
        new_tags = result.scalars().all()
        post.tags.extend(new_tags)

    await db.commit()
    await db.refresh(post)

    return post


async def delete_post(post_id: int, db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Post).filter(cast("ColumnElement[bool]", Post.id == post_id),
                            cast("ColumnElement[bool]", Post.is_deleted == False))
    )
    post = result.scalar_one_or_none()

    if not post:
        raise POST_NOT_FOUND_EXCEPTION

    # Comprobar si el que hace la petición es el creador del post
    if post.owner_id != user_id:
        raise NOT_POST_OWNER_EXCEPTION

    post.is_deleted = True
    await db.commit()
    await db.refresh(post)

    return post
