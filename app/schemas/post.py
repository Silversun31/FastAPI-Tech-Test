from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.tag import Tag


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    tag_ids: List[int]


class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]
    tag_ids: Optional[List[int]]


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    tags: List[Tag]

    class Config:
        from_attributes = True
