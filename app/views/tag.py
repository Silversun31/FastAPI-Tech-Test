from typing import cast

from sqlalchemy.orm import Session

from app import schemas
from app.models.tag import Tag
from app.schemas.tag import TagCreate


def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tag).filter(cast("ColumnElement[bool]", Tag.is_deleted == False)).offset(skip).limit(limit)


def get_tag(tag_id: int, db: Session):
    return db.query(Tag).filter(cast("ColumnElement[bool]", Tag.is_deleted == False),
                                cast("ColumnElement[bool]", Tag.id == tag_id)).first()


def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: Session):
    tag = db.query(Tag).filter(cast("ColumnElement[bool]", Tag.id == tag_id))
    tag.update(values=tag_update.dict())
    db.commit()
    tag = tag.first()
    db.refresh(tag)

    return tag


def delete_tag(tag_id: int, db: Session):
    tag = db.query(Tag).filter(cast("ColumnElement[bool]", Tag.id == tag_id)).first()
    tag.is_deleted = True
    db.commit()
    db.refresh(tag)

    return tag
