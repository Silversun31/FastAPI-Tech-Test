from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas
from app.exceptions import TAG_NOT_FOUND_EXCEPTION, DUPLICATED_TAG_NAME
from app.models.tag import Tag
from app.schemas.tag import TagCreate


async def create_tag(db: AsyncSession, tag: TagCreate):
    existing_tag = await db.execute(
        select(Tag).filter(Tag.is_deleted == False, Tag.name == tag.name)
    )
    if existing_tag.scalar_one_or_none():
        raise DUPLICATED_TAG_NAME

    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag


async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Tag).filter(Tag.is_deleted == False).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_tag(tag_id: int, db: AsyncSession):
    result = await db.execute(
        select(Tag).filter(Tag.is_deleted == False, Tag.id == tag_id)
    )
    tag = result.scalar_one_or_none()
    if not tag:
        raise TAG_NOT_FOUND_EXCEPTION
    return tag


async def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: AsyncSession):
    result = await db.execute(
        select(Tag).filter(Tag.id == tag_id)
    )
    tag = result.scalar_one_or_none()

    if not tag:
        raise TAG_NOT_FOUND_EXCEPTION

    # Actualizar el tag
    for key, value in tag_update.dict().items():
        setattr(tag, key, value)

    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(tag_id: int, db: AsyncSession):
    result = await db.execute(
        select(Tag).filter(Tag.is_deleted == False, Tag.id == tag_id)
    )
    tag = result.scalar_one_or_none()

    if not tag:
        raise TAG_NOT_FOUND_EXCEPTION

    tag.is_deleted = True
    await db.commit()
    await db.refresh(tag)

    return tag
