from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas.post import Post


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    content: Optional[str]
    post_id: Optional[int]


class Comment(CommentBase):
    id: int
    post: Post
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
