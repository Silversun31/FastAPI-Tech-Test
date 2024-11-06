from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas
from app.exceptions import COMMENT_NOT_FOUND_EXCEPTION, POST_NOT_FOUND_EXCEPTION
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(db: AsyncSession, comment: CommentCreate, user_id: int):
    result = await db.execute(select(Post).filter(Post.id == comment.post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise POST_NOT_FOUND_EXCEPTION

    db_comment = Comment(**comment.dict(exclude={"post_id"}), owner_id=user_id)
    db_comment.post = post
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comments(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Comment).filter(Comment.is_deleted == False).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_comment(comment_id: int, db: AsyncSession):
    result = await db.execute(
        select(Comment).filter(Comment.is_deleted == False, Comment.id == comment_id)
    )
    comment = result.scalar_one_or_none()
    if not comment:
        raise COMMENT_NOT_FOUND_EXCEPTION
    return comment


async def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: AsyncSession):
    result = await db.execute(
        select(Comment).filter(Comment.is_deleted == False, Comment.id == comment_id)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise COMMENT_NOT_FOUND_EXCEPTION

    # Actualizar el comentario
    for key, value in comment_update.dict(exclude={"post_id"}).items():
        setattr(comment, key, value)

    if comment_update.post_id is not None:
        result_post = await db.execute(select(Post).filter(Post.id == comment_update.post_id))
        post = result_post.scalar_one_or_none()
        if post:
            comment.post = post
        else:
            raise POST_NOT_FOUND_EXCEPTION

    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, db: AsyncSession):
    result = await db.execute(
        select(Comment).filter(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise COMMENT_NOT_FOUND_EXCEPTION

    comment.is_deleted = True
    await db.commit()
    await db.refresh(comment)

    return comment
